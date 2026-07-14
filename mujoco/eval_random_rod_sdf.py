#!/usr/bin/env python3
"""Random rod pose comparison for none / ideal_sdf / workspace_sdf.

For each random rod mount position, this script first finds a target where the
no-CBF baseline reaches near the target and contacts the rod. It then evaluates
the same rod pose and target with the requested methods.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import mujoco
import numpy as np

import eval_sdf_challenge as ev


@dataclass
class RandomRoundRecord:
    round_id: int
    rod_x: float
    rod_y: float
    rod_z: float
    target_idx: int
    method: str
    contact_steps: int
    best_dist_m: float
    end_dist_m: float
    success_latched: bool
    success_step: int
    final_state: str
    h_min_m: float
    active_steps: int
    corrected_steps: int
    max_dq_cbf: float
    total_steps: int


def _set_rod_mount(model: mujoco.MjModel, data: mujoco.MjData, pos: np.ndarray) -> None:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "obstacle_rod_mount")
    if bid < 0:
        raise ValueError("body not found: obstacle_rod_mount")
    model.body_pos[int(bid)] = np.asarray(pos, dtype=np.float64).reshape(3)
    mujoco.mj_forward(model, data)


def _sample_rod_pos(rng: np.random.Generator, args) -> np.ndarray:
    x = float(rng.uniform(float(args.rod_x_min), float(args.rod_x_max)))
    y = float(rng.uniform(float(args.rod_y_min), float(args.rod_y_max)))
    z = float(args.rod_z)
    return np.array([x, y, z], dtype=np.float64)


def _find_challenge_for_pose(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    policy,
    bank_pos: np.ndarray,
    bank_quat: np.ndarray,
    steps_per_ep: int,
    obstacle_gid: int,
    rng: np.random.Generator,
    args,
) -> int | None:
    candidates = rng.choice(
        bank_pos.shape[0],
        size=min(int(args.scan_count), bank_pos.shape[0]),
        replace=False,
    )
    baseline = ev._make_stepper(model, ids, policy, "none", args)
    for idx in candidates:
        quat = bank_quat[int(idx)].copy()
        quat /= max(float(np.linalg.norm(quat)), 1e-12)
        res = ev.run_episode(
            model,
            data,
            ids,
            baseline,
            "none",
            int(idx),
            bank_pos[int(idx)].copy(),
            quat,
            steps_per_ep,
            obstacle_gid,
            args,
        )
        if (
            res.contact_steps >= int(args.min_baseline_contact_steps)
            and res.best_dist_m <= float(args.max_baseline_best_dist)
        ):
            return int(idx)
    return None


def _write_round_csv(path: Path, rows: list[RandomRoundRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(RandomRoundRecord.__dataclass_fields__.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(asdict(row))


def _summarize(rows: list[RandomRoundRecord]) -> dict:
    out = {}
    for method in sorted({r.method for r in rows}):
        rs = [r for r in rows if r.method == method]
        out[method] = {
            "n": len(rs),
            "contact_rate": float(np.mean([r.contact_steps > 0 for r in rs])) if rs else float("nan"),
            "reach_2cm_rate": float(np.mean([r.best_dist_m <= 0.02 for r in rs])) if rs else float("nan"),
            "success_latch_rate": float(np.mean([r.success_latched for r in rs])) if rs else float("nan"),
            "mean_best_dist_m": float(np.mean([r.best_dist_m for r in rs])) if rs else float("nan"),
            "mean_end_dist_m": float(np.mean([r.end_dist_m for r in rs])) if rs else float("nan"),
            "mean_contact_steps": float(np.mean([r.contact_steps for r in rs])) if rs else float("nan"),
            "mean_max_dq_cbf": float(np.mean([r.max_dq_cbf for r in rs])) if rs else float("nan"),
        }
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=str, default=str(ev.DEFAULT_CHECKPOINT))
    p.add_argument("--mjcf", type=str, default=str(ev.DEFAULT_MJCF))
    p.add_argument("--npz", type=str, default=str(ev.DEFAULT_NPZ_TEST))
    p.add_argument("--out-dir", type=str, default="logs/eval/random_rod_sdf")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--rounds", type=int, default=5)
    p.add_argument("--scan-count", type=int, default=256)
    p.add_argument("--methods", nargs="+", default=["none", "ideal_sdf", "workspace_sdf"])
    p.add_argument("--obstacle-geom", type=str, default="obstacle_rod")
    p.add_argument("--rod-x-min", type=float, default=0.10)
    p.add_argument("--rod-x-max", type=float, default=0.22)
    p.add_argument("--rod-y-min", type=float, default=0.02)
    p.add_argument("--rod-y-max", type=float, default=0.16)
    p.add_argument("--rod-z", type=float, default=0.02)
    p.add_argument("--min-baseline-contact-steps", type=int, default=3)
    p.add_argument("--max-baseline-best-dist", type=float, default=0.02)
    p.add_argument("--calib-json", type=str, default=str(ev._THIS.parent / "logs" / "calib" / "camera_calib.json"))
    p.add_argument("--use-sim-cam", action="store_true")
    p.add_argument("--action-scale", type=float, default=ev.ACTION_SCALE)
    p.add_argument("--filter-tau", type=float, default=ev.ACTION_FILTER_TAU)
    p.add_argument("--cbf-d-safe", type=float, default=ev.CBF_D_SAFE)
    p.add_argument("--cbf-gamma", type=float, default=ev.CBF_GAMMA)
    p.add_argument("--cbf-lambda", type=float, default=ev.CBF_LAMBDA)
    p.add_argument("--cbf-activate-margin", type=float, default=ev.CBF_ACTIVATE_MARGIN)
    p.add_argument("--settle-methods", nargs="+", default=["ideal_sdf", "workspace_sdf"])
    p.add_argument("--success-dist", type=float, default=0.04)
    p.add_argument("--success-steps", type=int, default=5)
    p.add_argument("--settle-on-success", type=float, default=1.0)
    p.add_argument("--settle-mode", type=str, default="policy_soft_cbf", choices=("hold_q", "policy_soft_cbf"))
    p.add_argument("--settle-cbf-d-safe", type=float, default=0.005)
    p.add_argument("--settle-cbf-gamma", type=float, default=0.3)
    p.add_argument("--settle-cbf-activate-margin", type=float, default=0.015)
    p.add_argument("--settle-cbf-lambda", type=float, default=0.5)
    p.add_argument("--stop-on-success", action="store_true", default=True)
    args = p.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    model = mujoco.MjModel.from_xml_path(str(Path(args.mjcf).expanduser().resolve()))
    data = mujoco.MjData(model)
    ids = ev._rt.resolve_robot_ids(model)
    policy = ev._pol.SkrlGaussianPolicy(Path(args.checkpoint).expanduser().resolve())
    bank_pos, bank_quat = ev._rt.load_target_bank(Path(args.npz).expanduser().resolve())
    steps_per_ep = int(round(ev.EPISODE_LENGTH_S / (ev.SIM_DT * ev.DECIMATION)))
    obstacle_gid = ev._obstacle_gid(model, str(args.obstacle_geom))
    if obstacle_gid < 0:
        raise ValueError(f"obstacle geom not found: {args.obstacle_geom}")

    rng = np.random.default_rng(int(args.seed))
    rows: list[RandomRoundRecord] = []
    skipped = []
    for round_id in range(int(args.rounds)):
        rod_pos = _sample_rod_pos(rng, args)
        _set_rod_mount(model, data, rod_pos)
        idx = _find_challenge_for_pose(
            model,
            data,
            ids,
            policy,
            bank_pos,
            bank_quat,
            steps_per_ep,
            obstacle_gid,
            rng,
            args,
        )
        if idx is None:
            skipped.append({"round_id": int(round_id), "rod_pos": rod_pos.tolist()})
            print(f"[round {round_id:02d}] skipped rod=({rod_pos[0]:.3f},{rod_pos[1]:.3f}) no baseline challenge", flush=True)
            continue
        print(f"[round {round_id:02d}] rod=({rod_pos[0]:.3f},{rod_pos[1]:.3f},{rod_pos[2]:.3f}) target={idx}", flush=True)
        for method in [str(m).strip() for m in args.methods if str(m).strip()]:
            _set_rod_mount(model, data, rod_pos)
            stepper = ev._make_stepper(model, ids, policy, method, args)
            quat = bank_quat[int(idx)].copy()
            quat /= max(float(np.linalg.norm(quat)), 1e-12)
            res = ev.run_episode(
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
                args,
            )
            row = RandomRoundRecord(
                round_id=int(round_id),
                rod_x=float(rod_pos[0]),
                rod_y=float(rod_pos[1]),
                rod_z=float(rod_pos[2]),
                target_idx=int(idx),
                method=str(method),
                contact_steps=int(res.contact_steps),
                best_dist_m=float(res.best_dist_m),
                end_dist_m=float(res.end_dist_m),
                success_latched=bool(res.success_latched),
                success_step=int(res.success_step),
                final_state=str(res.final_state),
                h_min_m=float(res.h_min_m),
                active_steps=int(res.active_steps),
                corrected_steps=int(res.corrected_steps),
                max_dq_cbf=float(res.max_dq_cbf),
                total_steps=int(res.total_steps),
            )
            rows.append(row)
            print(
                f"  [{method}] contact={row.contact_steps} best={row.best_dist_m*1000:.1f}mm "
                f"end={row.end_dist_m*1000:.1f}mm success={'Y' if row.success_latched else 'n'}",
                flush=True,
            )

    _write_round_csv(out_dir / "rounds.csv", rows)
    summary = {
        "mjcf": str(Path(args.mjcf).expanduser().resolve()),
        "seed": int(args.seed),
        "rounds_requested": int(args.rounds),
        "rounds_valid": len({r.round_id for r in rows}),
        "skipped": skipped,
        "rod_range": {
            "x": [float(args.rod_x_min), float(args.rod_x_max)],
            "y": [float(args.rod_y_min), float(args.rod_y_max)],
            "z": float(args.rod_z),
        },
        "methods": [str(m) for m in args.methods],
        "settle_methods": [str(m) for m in args.settle_methods],
        "success_dist": float(args.success_dist),
        "success_steps": int(args.success_steps),
        "settle_on_success": float(args.settle_on_success),
        "settle_mode": str(args.settle_mode),
        "metrics": _summarize(rows),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary["metrics"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
