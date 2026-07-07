#!/usr/bin/env python3
"""MuJoCo CBF 避障批量评测：固定杆场景，同一批目标 idx 对比无 CBF / CBF v2。

  cd soarm100sim
  python mujoco/eval_cbf.py --num-episodes 256 --seed 42
  python mujoco/eval_cbf.py --indices-file logs/eval/cbf_fixed_rod/indices_seed42_n256.json
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import mujoco
import numpy as np

_THIS = Path(__file__).resolve().parent
_RL_ROOT = _THIS.parent / "rl"
if str(_RL_ROOT) not in sys.path:
    sys.path.insert(0, str(_RL_ROOT))

# 固定杆位置（与 scene_plus.xml 一致；评测范围见 mujoco/log.md）
FIXED_ROD_BODY = "obstacle_rod"
FIXED_ROD_POS_M = (0.15, 0.09, 0.17)

POS_THRESH_M = (0.01, 0.02, 0.03)
ORIENT_BINS_DEG = (10.0, 20.0, 30.0)
H_SAFE_EPS_M = 0.0
H_NEAR_EPS_M = -0.005


def _load_local(mod_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


_c = _load_local("so100_mj_constants_eval", _THIS / "constants.py")
_pol = _load_local("so100_mj_policy_eval", _THIS / "policy.py")
_rt = _load_local("so100_mj_runtime_eval", _THIS / "runtime.py")
_cbf = _load_local("so100_mj_cbf_eval", _THIS / "cbf.py")

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
CbfConfig = _cbf.CbfConfig
SkrlGaussianPolicy = _pol.SkrlGaussianPolicy
ReachStepper = _rt.ReachStepper
load_target_bank = _rt.load_target_bank
reset_home = _rt.reset_home
resolve_robot_ids = _rt.resolve_robot_ids
set_ctrl = _rt.set_ctrl
tcp_pose_w = _rt.tcp_pose_w


def _ori_deg(quat_dot: float) -> float:
    d = min(1.0, max(0.0, abs(quat_dot)))
    return float(2.0 * math.degrees(math.acos(d)))


def difficulty_tier(tx: float, ty: float, tz: float) -> str:
    """按目标相对固定杆的大致路径难度分层（启发式）。"""
    del tz
    if ty > 0.05 and 0.12 < tx < 0.32:
        return "hard"
    if -0.05 <= ty <= 0.05:
        return "medium"
    return "easy"


@dataclass
class CbfEpisodeStats:
    steps: int = 0
    active_steps: int = 0
    infeasible_steps: int = 0
    correction_steps: int = 0
    h_min_ep: float = float("inf")
    max_dq_cbf: float = 0.0
    worst_monitor_counts: Counter = field(default_factory=Counter)

    def update(self, info: dict) -> None:
        self.steps += 1
        h = float(info.get("h_min", float("inf")))
        self.h_min_ep = min(self.h_min_ep, h)
        if info.get("cbf_active"):
            self.active_steps += 1
        if info.get("cbf_active") and not info.get("cbf_feasible", True):
            self.infeasible_steps += 1
        dq_cbf = float(info.get("dq_cbf_norm", 0.0))
        if dq_cbf > 1e-6:
            self.correction_steps += 1
            self.max_dq_cbf = max(self.max_dq_cbf, dq_cbf)
        mon = info.get("cbf_worst_monitor")
        if mon:
            self.worst_monitor_counts[str(mon)] += 1


@dataclass
class EpisodeResult:
    idx: int
    tier: str
    target_pos: np.ndarray
    enable_cbf: bool
    best_dist_m: float
    best_ori_deg: float
    end_dist_m: float
    contact_steps: int
    h_min_ep_m: float | None = None
    infeas_steps: int = 0
    corrected_steps: int = 0
    max_dq_cbf: float = 0.0
    worst_monitor: str = ""


def _resolve_obstacle_geom_id(model: mujoco.MjModel, geom_name: str) -> int:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, geom_name)
    if gid < 0:
        raise ValueError(f"obstacle geom not found: {geom_name}")
    return int(gid)


def _count_obstacle_contacts(data: mujoco.MjData, obstacle_gid: int) -> int:
    n = 0
    for i in range(int(data.ncon)):
        c = data.contact[i]
        if int(c.geom1) == obstacle_gid or int(c.geom2) == obstacle_gid:
            n += 1
    return n


def run_episode(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    stepper: ReachStepper,
    target_pos: np.ndarray,
    target_quat: np.ndarray,
    steps_per_ep: int,
    obstacle_gid: int,
    enable_cbf: bool,
    idx: int,
    tier: str,
) -> EpisodeResult:
    reset_home(model, data, ids)
    stepper.reset_filter()
    if enable_cbf:
        stepper.refresh_cbf_obstacles(data)

    best_dist = float("inf")
    best_ori = float("inf")
    contact_steps = 0
    cbf_stats = CbfEpisodeStats() if enable_cbf else None

    for _ in range(steps_per_ep):
        tgt, info = stepper.compute_targets(model, data, target_pos, target_quat)
        if cbf_stats is not None:
            cbf_stats.update(info)
        set_ctrl(data, ids, tgt)
        for _ in range(int(DECIMATION)):
            mujoco.mj_step(model, data)
        if _count_obstacle_contacts(data, obstacle_gid) > 0:
            contact_steps += 1

        dist = float(info["distance"])
        ori = _ori_deg(float(info["quat_dot"]))
        best_dist = min(best_dist, dist)
        best_ori = min(best_ori, ori)

    tcp, _ = tcp_pose_w(data, ids)
    end_dist = float(np.linalg.norm(tcp - target_pos))

    if cbf_stats is not None:
        worst_mon = ""
        if cbf_stats.worst_monitor_counts:
            worst_mon = cbf_stats.worst_monitor_counts.most_common(1)[0][0]
        h_min = cbf_stats.h_min_ep if math.isfinite(cbf_stats.h_min_ep) else float("nan")
        return EpisodeResult(
            idx=idx,
            tier=tier,
            target_pos=target_pos.copy(),
            enable_cbf=True,
            best_dist_m=best_dist,
            best_ori_deg=best_ori,
            end_dist_m=end_dist,
            contact_steps=contact_steps,
            h_min_ep_m=h_min,
            infeas_steps=cbf_stats.infeasible_steps,
            corrected_steps=cbf_stats.correction_steps,
            max_dq_cbf=cbf_stats.max_dq_cbf,
            worst_monitor=worst_mon,
        )

    return EpisodeResult(
        idx=idx,
        tier=tier,
        target_pos=target_pos.copy(),
        enable_cbf=False,
        best_dist_m=best_dist,
        best_ori_deg=best_ori,
        end_dist_m=end_dist,
        contact_steps=contact_steps,
    )


def load_or_create_indices(
    bank_size: int,
    num_episodes: int,
    seed: int,
    indices_path: Path | None,
) -> list[int]:
    if indices_path is not None and indices_path.is_file():
        payload = json.loads(indices_path.read_text(encoding="utf-8"))
        indices = [int(x) for x in payload["indices"]]
        if len(indices) != num_episodes:
            raise ValueError(
                f"indices file has {len(indices)} entries, expected {num_episodes}"
            )
        return indices

    rng = np.random.default_rng(int(seed))
    indices = [int(rng.integers(0, bank_size)) for _ in range(num_episodes)]
    if indices_path is not None:
        indices_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "seed": int(seed),
            "num_episodes": int(num_episodes),
            "bank_size": int(bank_size),
            "indices": indices,
        }
        indices_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return indices


def _rate(mask: np.ndarray) -> float:
    return float(mask.mean()) if mask.size else float("nan")


def _bucket_stats(
    best_dist: np.ndarray,
    best_ori: np.ndarray,
    h_min: np.ndarray | None,
    contact_steps: np.ndarray,
    safe_mask: np.ndarray | None,
) -> dict:
    out: dict[str, float] = {
        **{f"pos_le_{int(t * 100)}cm": _rate(best_dist <= t) for t in POS_THRESH_M},
        **{f"ori_le_{int(t)}deg": _rate(best_ori <= t) for t in ORIENT_BINS_DEG},
        "joint_pos1cm_ori20": _rate((best_dist <= 0.01) & (best_ori <= 20.0)),
        "median_best_dist_mm": float(np.median(best_dist) * 1000.0),
        "p90_best_dist_mm": float(np.percentile(best_dist, 90) * 1000.0),
        "no_contact_rate": _rate(contact_steps == 0),
    }
    if h_min is not None and safe_mask is not None:
        out["cbf_safe_rate"] = _rate(safe_mask)
        out["cbf_near_safe_rate"] = _rate(h_min >= H_NEAR_EPS_M)
        out["h_min_p10_mm"] = float(np.percentile(h_min, 10) * 1000.0)
        out["h_min_median_mm"] = float(np.median(h_min) * 1000.0)
        out["safe_reach_2cm"] = _rate(safe_mask & (best_dist <= 0.02))
        out["safe_reach_1cm_ori20"] = _rate(
            safe_mask & (best_dist <= 0.01) & (best_ori <= 20.0)
        )
    return out


def write_episodes_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build_summary_md(
    meta: dict,
    overall: dict,
    by_tier: dict[str, dict],
) -> str:
    lines = [
        "# CBF 固定杆评测汇总",
        "",
        f"- 生成时间：{meta['timestamp']}",
        f"- Git commit：`{meta.get('git_commit', 'unknown')}`",
        f"- Checkpoint：`{meta['checkpoint']}`",
        f"- MJCF：`{meta['mjcf']}`",
        f"- NPZ：`{meta['npz']}`",
        f"- Episodes：{meta['num_episodes']}（seed={meta['seed']}）",
        f"- **障碍物：固定细杆 `{FIXED_ROD_BODY}` @ {FIXED_ROD_POS_M} m（见 mujoco/log.md）**",
        f"- CBF：d_safe={meta['cbf_d_safe']} γ={meta['cbf_gamma']} activate<{meta['cbf_activate_margin']}",
        "",
        "## 总体对比",
        "",
        "| 指标 | 无 CBF | CBF v2 | Δ (CBF−base) |",
        "|------|--------|--------|--------------|",
    ]

    def _cell(d: dict, key: str, scale: float = 100.0, suffix: str = "%") -> str:
        if key not in d:
            return "—"
        v = d[key] * scale if suffix == "%" else d[key]
        return f"{v:.1f}{suffix}"

    keys = [
        ("pos_le_1cm", "%"),
        ("pos_le_2cm", "%"),
        ("joint_pos1cm_ori20", "%"),
        ("cbf_safe_rate", "%"),
        ("safe_reach_2cm", "%"),
        ("safe_reach_1cm_ori20", "%"),
        ("no_contact_rate", "%"),
        ("median_best_dist_mm", "mm"),
        ("h_min_median_mm", "mm"),
    ]
    b = overall["baseline"]
    c = overall["cbf"]
    for key, suffix in keys:
        if key == "cbf_safe_rate" or key == "safe_reach_2cm" or key == "safe_reach_1cm_ori20":
            bl = "—"
        elif key == "h_min_median_mm":
            bl = "—"
        else:
            bl = _cell(b, key, suffix=suffix)
        cv = _cell(c, key, suffix=suffix) if key in c else "—"
        if suffix == "%" and key in b and key in c:
            delta = f"{(c[key] - b[key]) * 100:+.1f} pt"
        elif suffix == "mm" and key in b and key in c:
            delta = f"{c[key] - b[key]:+.1f} mm"
        elif key == "median_best_dist_mm" and "median_best_dist_mm" in b and "median_best_dist_mm" in c:
            delta = f"{c['median_best_dist_mm'] - b['median_best_dist_mm']:+.1f} mm"
        else:
            delta = "—"
        label = key.replace("_", " ")
        lines.append(f"| {label} | {bl} | {cv} | {delta} |")

    if "delta_best_dist_mm" in overall:
        d = overall["delta_best_dist_mm"]
        lines.extend(
            [
                "",
                "## 到达代价（同 idx 配对）",
                "",
                f"- Δbest_dist 中位数：**{d['median_mm']:+.1f} mm**",
                f"- Δbest_dist p90：**{d['p90_mm']:+.1f} mm**",
                f"- 退化 >10 mm 比例：**{d['worse_10mm_rate'] * 100:.1f}%**",
            ]
        )

    lines.extend(["", "## 按难度分层", "", "| 档位 | N | SafeReach@2cm (CBF) | pos≤2cm base | pos≤2cm CBF | h_min 中位 (CBF) |", "|------|---|---------------------|-------------|-------------|------------------|"])
    for tier in ("hard", "medium", "easy"):
        if tier not in by_tier:
            continue
        t = by_tier[tier]
        lines.append(
            f"| {tier} | {t['count']} | {t['cbf'].get('safe_reach_2cm', float('nan')) * 100:.1f}% | "
            f"{t['baseline'].get('pos_le_2cm', float('nan')) * 100:.1f}% | "
            f"{t['cbf'].get('pos_le_2cm', float('nan')) * 100:.1f}% | "
            f"{t['cbf'].get('h_min_median_mm', float('nan')):.1f} mm |"
        )
    lines.append("")
    return "\n".join(lines)


def _git_commit_short() -> str:
    try:
        import subprocess

        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(_THIS.parent),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except Exception:
        return "unknown"


def evaluate(args: argparse.Namespace) -> int:
    ckpt = Path(args.checkpoint).expanduser().resolve()
    mjcf = Path(args.mjcf).expanduser().resolve()
    npz = Path(args.npz).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for p, label in ((ckpt, "checkpoint"), (mjcf, "mjcf"), (npz, "npz")):
        if not p.is_file():
            print(f"[ERROR] {label} not found: {p}", file=sys.stderr)
            return 1

    bank_pos, bank_quat = load_target_bank(npz)
    indices_path = (
        Path(args.indices_file).expanduser().resolve()
        if args.indices_file
        else out_dir / f"indices_seed{args.seed}_n{args.num_episodes}.json"
    )
    indices = load_or_create_indices(
        bank_size=bank_pos.shape[0],
        num_episodes=int(args.num_episodes),
        seed=int(args.seed),
        indices_path=indices_path,
    )
    print(f"[eval_cbf] indices → {indices_path}")

    model = mujoco.MjModel.from_xml_path(str(mjcf))
    model.opt.timestep = float(SIM_DT)
    data = mujoco.MjData(model)
    ids = resolve_robot_ids(model)
    policy = SkrlGaussianPolicy(ckpt)
    obstacle_gid = _resolve_obstacle_geom_id(model, FIXED_ROD_BODY)

    cbf_cfg = CbfConfig(
        d_safe=float(args.cbf_d_safe),
        gamma=float(args.cbf_gamma),
        lambda_cbf=float(args.cbf_lambda),
        dq_max=float(args.action_scale),
        activate_margin=float(args.cbf_activate_margin),
    )
    stepper_base = ReachStepper(
        policy=policy,
        ids=ids,
        model=model,
        action_scale=float(args.action_scale),
        filter_tau=float(args.filter_tau),
        sim_dt=float(SIM_DT),
        decimation=int(DECIMATION),
        enable_cbf=False,
    )
    stepper_cbf = ReachStepper(
        policy=policy,
        ids=ids,
        model=model,
        action_scale=float(args.action_scale),
        filter_tau=float(args.filter_tau),
        sim_dt=float(SIM_DT),
        decimation=int(DECIMATION),
        enable_cbf=True,
        cbf_cfg=cbf_cfg,
    )

    steps_per_ep = int(round(EPISODE_LENGTH_S / (SIM_DT * DECIMATION)))
    baseline_results: list[EpisodeResult] = []
    cbf_results: list[EpisodeResult] = []
    t0 = time.perf_counter()

    for i, idx in enumerate(indices):
        target_pos = bank_pos[idx].copy()
        target_quat = bank_quat[idx].copy()
        target_quat /= max(float(np.linalg.norm(target_quat)), 1e-12)
        tier = difficulty_tier(float(target_pos[0]), float(target_pos[1]), float(target_pos[2]))

        if not args.cbf_only:
            baseline_results.append(
                run_episode(
                    model,
                    data,
                    ids,
                    stepper_base,
                    target_pos,
                    target_quat,
                    steps_per_ep,
                    obstacle_gid,
                    enable_cbf=False,
                    idx=idx,
                    tier=tier,
                )
            )
        if not args.baseline_only:
            cbf_results.append(
                run_episode(
                    model,
                    data,
                    ids,
                    stepper_cbf,
                    target_pos,
                    target_quat,
                    steps_per_ep,
                    obstacle_gid,
                    enable_cbf=True,
                    idx=idx,
                    tier=tier,
                )
            )

        if (i + 1) % max(1, int(args.log_every)) == 0 or (i + 1) == len(indices):
            elapsed = time.perf_counter() - t0
            print(f"[eval_cbf] {i + 1}/{len(indices)}  elapsed={elapsed:.1f}s")

    csv_rows: list[dict] = []
    if baseline_results and cbf_results:
        for bi, ci in zip(baseline_results, cbf_results):
            assert bi.idx == ci.idx
            delta_mm = (ci.best_dist_m - bi.best_dist_m) * 1000.0
            safe = bool(ci.h_min_ep_m is not None and ci.h_min_ep_m >= H_SAFE_EPS_M)
            csv_rows.append(
                {
                    "idx": bi.idx,
                    "tier": bi.tier,
                    "target_x": f"{bi.target_pos[0]:.6f}",
                    "target_y": f"{bi.target_pos[1]:.6f}",
                    "target_z": f"{bi.target_pos[2]:.6f}",
                    "baseline_best_dist_mm": f"{bi.best_dist_m * 1000:.3f}",
                    "baseline_best_ori_deg": f"{bi.best_ori_deg:.3f}",
                    "baseline_end_dist_mm": f"{bi.end_dist_m * 1000:.3f}",
                    "baseline_contact_steps": bi.contact_steps,
                    "cbf_best_dist_mm": f"{ci.best_dist_m * 1000:.3f}",
                    "cbf_best_ori_deg": f"{ci.best_ori_deg:.3f}",
                    "cbf_end_dist_mm": f"{ci.end_dist_m * 1000:.3f}",
                    "cbf_h_min_ep_mm": f"{(ci.h_min_ep_m or float('nan')) * 1000:.3f}",
                    "cbf_infeas_steps": ci.infeas_steps,
                    "cbf_corrected_steps": ci.corrected_steps,
                    "cbf_max_dq_cbf": f"{ci.max_dq_cbf:.6f}",
                    "cbf_worst_monitor": ci.worst_monitor,
                    "cbf_contact_steps": ci.contact_steps,
                    "cbf_safe": int(safe),
                    "delta_best_dist_mm": f"{delta_mm:.3f}",
                }
            )
    elif baseline_results:
        for bi in baseline_results:
            csv_rows.append(
                {
                    "idx": bi.idx,
                    "tier": bi.tier,
                    "target_x": f"{bi.target_pos[0]:.6f}",
                    "target_y": f"{bi.target_pos[1]:.6f}",
                    "target_z": f"{bi.target_pos[2]:.6f}",
                    "baseline_best_dist_mm": f"{bi.best_dist_m * 1000:.3f}",
                    "baseline_best_ori_deg": f"{bi.best_ori_deg:.3f}",
                    "baseline_end_dist_mm": f"{bi.end_dist_m * 1000:.3f}",
                    "baseline_contact_steps": bi.contact_steps,
                }
            )
    elif cbf_results:
        for ci in cbf_results:
            safe = bool(ci.h_min_ep_m is not None and ci.h_min_ep_m >= H_SAFE_EPS_M)
            csv_rows.append(
                {
                    "idx": ci.idx,
                    "tier": ci.tier,
                    "target_x": f"{ci.target_pos[0]:.6f}",
                    "target_y": f"{ci.target_pos[1]:.6f}",
                    "target_z": f"{ci.target_pos[2]:.6f}",
                    "cbf_best_dist_mm": f"{ci.best_dist_m * 1000:.3f}",
                    "cbf_best_ori_deg": f"{ci.best_ori_deg:.3f}",
                    "cbf_end_dist_mm": f"{ci.end_dist_m * 1000:.3f}",
                    "cbf_h_min_ep_mm": f"{(ci.h_min_ep_m or float('nan')) * 1000:.3f}",
                    "cbf_infeas_steps": ci.infeas_steps,
                    "cbf_corrected_steps": ci.corrected_steps,
                    "cbf_max_dq_cbf": f"{ci.max_dq_cbf:.6f}",
                    "cbf_worst_monitor": ci.worst_monitor,
                    "cbf_contact_steps": ci.contact_steps,
                    "cbf_safe": int(safe),
                }
            )

    episodes_csv = out_dir / "episodes.csv"
    if csv_rows:
        write_episodes_csv(episodes_csv, csv_rows)
        print(f"[eval_cbf] episodes → {episodes_csv}")

    if baseline_results and cbf_results:
        b_dist = np.array([r.best_dist_m for r in baseline_results])
        b_ori = np.array([r.best_ori_deg for r in baseline_results])
        b_contact = np.array([r.contact_steps for r in baseline_results])
        c_dist = np.array([r.best_dist_m for r in cbf_results])
        c_ori = np.array([r.best_ori_deg for r in cbf_results])
        c_contact = np.array([r.contact_steps for r in cbf_results])
        c_hmin = np.array([r.h_min_ep_m or float("nan") for r in cbf_results])
        safe_mask = c_hmin >= H_SAFE_EPS_M

        overall = {
            "baseline": _bucket_stats(b_dist, b_ori, None, b_contact, None),
            "cbf": _bucket_stats(c_dist, c_ori, c_hmin, c_contact, safe_mask),
            "delta_best_dist_mm": {
                "median_mm": float(np.median((c_dist - b_dist) * 1000.0)),
                "p90_mm": float(np.percentile((c_dist - b_dist) * 1000.0, 90)),
                "worse_10mm_rate": float(np.mean((c_dist - b_dist) > 0.01)),
            },
        }

        by_tier: dict[str, dict] = {}
        tiers = sorted({r.tier for r in baseline_results})
        for tier in tiers:
            mask = np.array([r.tier == tier for r in baseline_results])
            by_tier[tier] = {
                "count": int(mask.sum()),
                "baseline": _bucket_stats(b_dist[mask], b_ori[mask], None, b_contact[mask], None),
                "cbf": _bucket_stats(
                    c_dist[mask],
                    c_ori[mask],
                    c_hmin[mask],
                    c_contact[mask],
                    safe_mask[mask],
                ),
            }

        meta = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "git_commit": _git_commit_short(),
            "checkpoint": str(ckpt),
            "mjcf": str(mjcf),
            "npz": str(npz),
            "num_episodes": int(args.num_episodes),
            "seed": int(args.seed),
            "indices_file": str(indices_path),
            "cbf_d_safe": float(args.cbf_d_safe),
            "cbf_gamma": float(args.cbf_gamma),
            "cbf_activate_margin": float(args.cbf_activate_margin),
            "fixed_rod_body": FIXED_ROD_BODY,
            "fixed_rod_pos_m": list(FIXED_ROD_POS_M),
        }
        summary_json = out_dir / "summary.json"
        summary_json.write_text(
            json.dumps({"meta": meta, "overall": overall, "by_tier": by_tier}, indent=2),
            encoding="utf-8",
        )
        summary_md = build_summary_md(meta, overall, by_tier)
        summary_path = out_dir / "summary.md"
        summary_path.write_text(summary_md, encoding="utf-8")
        print(f"[eval_cbf] summary → {summary_path}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MuJoCo CBF fixed-rod batch eval")
    p.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument("--npz", type=str, default=str(DEFAULT_NPZ_TEST))
    p.add_argument("--out-dir", type=str, default=str(_THIS.parent / "logs" / "eval" / "cbf_fixed_rod"))
    p.add_argument("--num-episodes", type=int, default=256)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--indices-file",
        type=str,
        default="",
        help="复用已有 idx 列表；缺省则生成到 out-dir/indices_seed{N}_n{E}.json",
    )
    p.add_argument("--baseline-only", action="store_true")
    p.add_argument("--cbf-only", action="store_true")
    p.add_argument("--log-every", type=int, default=32)
    p.add_argument("--action-scale", type=float, default=ACTION_SCALE)
    p.add_argument("--filter-tau", type=float, default=ACTION_FILTER_TAU)
    p.add_argument("--cbf-d-safe", type=float, default=CBF_D_SAFE)
    p.add_argument("--cbf-gamma", type=float, default=CBF_GAMMA)
    p.add_argument("--cbf-lambda", type=float, default=CBF_LAMBDA)
    p.add_argument("--cbf-activate-margin", type=float, default=CBF_ACTIVATE_MARGIN)
    return p


if __name__ == "__main__":
    cli = build_parser()
    raise SystemExit(evaluate(cli.parse_args()))
