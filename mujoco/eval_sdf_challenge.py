#!/usr/bin/env python3
"""Challenge-set eval for obstacle avoidance.

First selects target indices where the no-CBF baseline contacts the obstacle,
then compares none / analytic geom CBF / ideal point-cloud SDF CBF on that same set.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np

_THIS = Path(__file__).resolve().parent
_RL_ROOT = _THIS.parent / "rl"
if str(_RL_ROOT) not in sys.path:
    sys.path.insert(0, str(_RL_ROOT))


def _load_local(mod_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


_c = _load_local("so100_mj_constants", _THIS / "constants.py")
_pol = _load_local("so100_mj_policy", _THIS / "policy.py")
_rt = _load_local("so100_mj_runtime", _THIS / "runtime.py")
_cbf = _load_local("so100_mj_cbf", _THIS / "cbf.py")
_obs = _load_local("so100_mj_obstacle_source", _THIS / "obstacle_source.py")

DEFAULT_CHECKPOINT = _c.DEFAULT_CHECKPOINT
DEFAULT_MJCF = _c.DEFAULT_MJCF
DEFAULT_NPZ_TEST = _c.DEFAULT_NPZ_TEST
SIM_DT = _c.SIM_DT
DECIMATION = _c.DECIMATION
ACTION_SCALE = _c.ACTION_SCALE
ACTION_FILTER_TAU = _c.ACTION_FILTER_TAU
EPISODE_LENGTH_S = _c.EPISODE_LENGTH_S
CBF_D_SAFE = _c.CBF_D_SAFE
CBF_GAMMA = _c.CBF_GAMMA
CBF_LAMBDA = _c.CBF_LAMBDA
CBF_ACTIVATE_MARGIN = _c.CBF_ACTIVATE_MARGIN


@dataclass
class RunResult:
    idx: int
    method: str
    contact_steps: int
    best_dist_m: float
    end_dist_m: float
    h_min_m: float
    active_steps: int
    corrected_steps: int
    max_dq_cbf: float
    total_steps: int


def _obstacle_gid(model: mujoco.MjModel, geom_name: str) -> int:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, geom_name)
    return int(gid) if gid >= 0 else -1


def _count_contacts(data: mujoco.MjData, obstacle_gid: int) -> int:
    if obstacle_gid < 0:
        return 0
    n = 0
    for i in range(int(data.ncon)):
        c = data.contact[i]
        if int(c.geom1) == obstacle_gid or int(c.geom2) == obstacle_gid:
            n += 1
    return n


def _make_stepper(model: mujoco.MjModel, ids, policy, method: str, args) -> _rt.ReachStepper:
    enable_cbf = method in ("geom", "ideal_sdf")
    cfg = None
    obs_source = None
    if enable_cbf:
        cfg = _cbf.CbfConfig(
            d_safe=float(args.cbf_d_safe),
            gamma=float(args.cbf_gamma),
            lambda_cbf=float(args.cbf_lambda),
            activate_margin=float(args.cbf_activate_margin),
        )
    stepper = _rt.ReachStepper(
        policy=policy,
        ids=ids,
        model=model,
        action_scale=float(args.action_scale),
        filter_tau=float(args.filter_tau),
        sim_dt=float(SIM_DT),
        decimation=int(DECIMATION),
        enable_cbf=enable_cbf,
        cbf_cfg=cfg,
    )
    if method == "ideal_sdf":
        obs_source = _obs.make_obstacle_source("ideal_sdf", model, geom_names=cfg.obstacle_geom_names)
    elif method == "geom":
        obs_source = _obs.make_obstacle_source("geom", model, geom_names=cfg.obstacle_geom_names)
    stepper.cbf_obstacle_source = obs_source
    return stepper


def run_episode(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    stepper,
    method: str,
    idx: int,
    target_pos: np.ndarray,
    target_quat: np.ndarray,
    steps_per_ep: int,
    obstacle_gid: int,
) -> RunResult:
    _rt.reset_home(model, data, ids)
    stepper.reset_filter()
    if method in ("geom", "ideal_sdf"):
        stepper.refresh_cbf_obstacles(data)

    contact_steps = 0
    best_dist = float("inf")
    h_min = float("inf")
    active_steps = 0
    corrected_steps = 0
    max_dq_cbf = 0.0

    for _ in range(steps_per_ep):
        tgt, info = stepper.compute_targets(model, data, target_pos, target_quat)
        _rt.set_ctrl(data, ids, tgt)
        for _sub in range(int(DECIMATION)):
            mujoco.mj_step(model, data)
        if _count_contacts(data, obstacle_gid) > 0:
            contact_steps += 1
        best_dist = min(best_dist, float(info["distance"]))
        h = float(info.get("h_min", float("inf")))
        h_min = min(h_min, h)
        if info.get("cbf_active"):
            active_steps += 1
        dq_cbf = float(info.get("dq_cbf_norm", 0.0))
        if dq_cbf > 1e-6:
            corrected_steps += 1
            max_dq_cbf = max(max_dq_cbf, dq_cbf)

    tcp, _ = _rt.tcp_pose_w(data, ids)
    end_dist = float(np.linalg.norm(tcp - target_pos))
    if not math.isfinite(h_min):
        h_min = float("nan")
    return RunResult(
        idx=int(idx),
        method=method,
        contact_steps=int(contact_steps),
        best_dist_m=float(best_dist),
        end_dist_m=end_dist,
        h_min_m=float(h_min),
        active_steps=int(active_steps),
        corrected_steps=int(corrected_steps),
        max_dq_cbf=float(max_dq_cbf),
        total_steps=int(steps_per_ep),
    )


def _write_csv(path: Path, rows: list[RunResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(RunResult.__dataclass_fields__.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: getattr(r, k) for k in fields})


def _summarize(rows: list[RunResult]) -> dict:
    out = {}
    for method in sorted({r.method for r in rows}):
        rs = [r for r in rows if r.method == method]
        out[method] = {
            "n": len(rs),
            "contact_rate": float(np.mean([r.contact_steps > 0 for r in rs])) if rs else float("nan"),
            "reach_2cm_rate": float(np.mean([r.best_dist_m <= 0.02 for r in rs])) if rs else float("nan"),
            "mean_best_dist_m": float(np.mean([r.best_dist_m for r in rs])) if rs else float("nan"),
            "mean_end_dist_m": float(np.mean([r.end_dist_m for r in rs])) if rs else float("nan"),
            "mean_h_min_m": float(np.nanmean([r.h_min_m for r in rs])) if rs else float("nan"),
            "mean_max_dq_cbf": float(np.mean([r.max_dq_cbf for r in rs])) if rs else float("nan"),
        }
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument("--npz", type=str, default=str(DEFAULT_NPZ_TEST))
    p.add_argument("--out-dir", type=str, default="logs/eval/sdf_challenge")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--scan-count", type=int, default=512)
    p.add_argument("--max-challenges", type=int, default=64)
    p.add_argument("--indices-file", type=str, default="")
    p.add_argument("--obstacle-geom", type=str, default="obstacle_rod")
    p.add_argument("--action-scale", type=float, default=ACTION_SCALE)
    p.add_argument("--filter-tau", type=float, default=ACTION_FILTER_TAU)
    p.add_argument("--cbf-d-safe", type=float, default=CBF_D_SAFE)
    p.add_argument("--cbf-gamma", type=float, default=CBF_GAMMA)
    p.add_argument("--cbf-lambda", type=float, default=CBF_LAMBDA)
    p.add_argument("--cbf-activate-margin", type=float, default=CBF_ACTIVATE_MARGIN)
    p.add_argument("--log-every", type=int, default=16)
    args = p.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    model = mujoco.MjModel.from_xml_path(str(Path(args.mjcf).expanduser().resolve()))
    data = mujoco.MjData(model)
    ids = _rt.resolve_robot_ids(model)
    policy = _pol.SkrlGaussianPolicy(Path(args.checkpoint).expanduser().resolve())
    bank_pos, bank_quat = _rt.load_target_bank(Path(args.npz).expanduser().resolve())
    steps_per_ep = int(round(EPISODE_LENGTH_S / (SIM_DT * DECIMATION)))
    obstacle_gid = _obstacle_gid(model, str(args.obstacle_geom))
    if obstacle_gid < 0:
        raise ValueError(f"obstacle geom not found: {args.obstacle_geom}")

    rng = np.random.default_rng(int(args.seed))
    if args.indices_file:
        challenge_indices = [int(x) for x in json.loads(Path(args.indices_file).read_text(encoding="utf-8"))]
    else:
        candidates = rng.choice(bank_pos.shape[0], size=min(int(args.scan_count), bank_pos.shape[0]), replace=False)
        baseline_stepper = _make_stepper(model, ids, policy, "none", args)
        challenge_indices = []
        print(f"[scan] scanning {len(candidates)} targets for no-CBF contacts")
        for n, idx in enumerate(candidates, 1):
            res = run_episode(
                model,
                data,
                ids,
                baseline_stepper,
                "none",
                int(idx),
                bank_pos[int(idx)].copy(),
                bank_quat[int(idx)].copy(),
                steps_per_ep,
                obstacle_gid,
            )
            if res.contact_steps > 0:
                challenge_indices.append(int(idx))
                print(f"[scan] challenge idx={int(idx)} contact_steps={res.contact_steps} best={res.best_dist_m*1000:.1f}mm")
                if len(challenge_indices) >= int(args.max_challenges):
                    break
            elif n % max(1, int(args.log_every)) == 0:
                print(f"[scan] {n}/{len(candidates)} found={len(challenge_indices)}")
        (out_dir / "challenge_indices.json").write_text(
            json.dumps(challenge_indices, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"[eval] challenge_count={len(challenge_indices)}")
    rows: list[RunResult] = []
    for method in ("none", "geom", "ideal_sdf"):
        stepper = _make_stepper(model, ids, policy, method, args)
        for i, idx in enumerate(challenge_indices, 1):
            quat = bank_quat[int(idx)].copy()
            quat /= max(float(np.linalg.norm(quat)), 1e-12)
            res = run_episode(
                model,
                data,
                ids,
                stepper,
                method,
                int(idx),
                bank_pos[int(idx)].copy(),
                quat,
                steps_per_ep,
                obstacle_gid,
            )
            rows.append(res)
            if i % max(1, int(args.log_every)) == 0 or i == len(challenge_indices):
                print(
                    f"[eval][{method}] {i}/{len(challenge_indices)} "
                    f"idx={idx} contact={res.contact_steps} best={res.best_dist_m*1000:.1f}mm "
                    f"h={res.h_min_m*1000 if math.isfinite(res.h_min_m) else float('nan'):.1f}mm"
                )

    _write_csv(out_dir / "episodes.csv", rows)
    summary = {
        "mjcf": str(Path(args.mjcf).expanduser().resolve()),
        "seed": int(args.seed),
        "scan_count": int(args.scan_count),
        "challenge_indices": challenge_indices,
        "metrics": _summarize(rows),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary["metrics"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
