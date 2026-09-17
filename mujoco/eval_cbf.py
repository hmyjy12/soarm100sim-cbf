#!/usr/bin/env python3
"""MuJoCo CBF 避障批量评测：固定杆场景，同一批目标 idx 对比无 CBF / CBF v2。

  cd soarm100sim
  python mujoco/eval_cbf.py --num-episodes 256 --seed 42
  python mujoco/eval_cbf.py --indices-file log/runtime/eval/cbf_fixed_rod/indices_seed42_n256.json
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

# 固定杆位置（与 scene_plus.xml 一致；评测范围见 docs/development/mujoco实验记录.md）
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
DEFAULT_MJCF_NOROD = _c.DEFAULT_MJCF_NOROD
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
CBF_FILTER_TAU = _c.CBF_FILTER_TAU
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
    total_steps: int = 0
    h_min_ep_m: float | None = None
    infeas_steps: int = 0
    corrected_steps: int = 0
    active_steps: int = 0
    max_dq_cbf: float = 0.0
    worst_monitor: str = ""
    h_unsafe_no_contact: bool = False
    h_safe_with_contact: bool = False


def _try_obstacle_geom_id(model: mujoco.MjModel, geom_name: str) -> int:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, geom_name)
    return int(gid) if gid >= 0 else -1


def _count_obstacle_contacts(data: mujoco.MjData, obstacle_gid: int) -> int:
    if obstacle_gid < 0:
        return 0
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
        if obstacle_gid >= 0 and _count_obstacle_contacts(data, obstacle_gid) > 0:
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
            total_steps=steps_per_ep,
            h_min_ep_m=h_min,
            infeas_steps=cbf_stats.infeasible_steps,
            corrected_steps=cbf_stats.correction_steps,
            active_steps=cbf_stats.active_steps,
            max_dq_cbf=cbf_stats.max_dq_cbf,
            worst_monitor=worst_mon,
            h_unsafe_no_contact=bool(math.isfinite(h_min) and h_min < H_SAFE_EPS_M and contact_steps == 0),
            h_safe_with_contact=bool(math.isfinite(h_min) and h_min >= H_SAFE_EPS_M and contact_steps > 0),
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
        total_steps=steps_per_ep,
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
        if len(indices) < num_episodes:
            raise ValueError(
                f"indices file has {len(indices)} entries, expected at least {num_episodes}"
            )
        if len(indices) > num_episodes:
            indices = indices[:num_episodes]
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


def _compute_conditional_stats(
    b_contact: np.ndarray,
    c_contact: np.ndarray,
    safe_mask: np.ndarray,
    c_dist: np.ndarray,
    c_ori: np.ndarray,
    tiers: np.ndarray | None = None,
) -> dict:
    """碰撞与避障的条件概率（比全局 no_contact_rate 更能反映 CBF 真实作用）。"""
    base_hit = b_contact > 0
    cbf_hit = c_contact > 0
    base_no = ~base_hit
    safe_reach_2cm = safe_mask & (c_dist <= 0.02)
    phys_reach_2cm = (~cbf_hit) & (c_dist <= 0.02)
    phys_reach_1cm_ori20 = (~cbf_hit) & (c_dist <= 0.01) & (c_ori <= 20.0)

    def _one(mask: np.ndarray | None = None) -> dict:
        bh = base_hit if mask is None else base_hit[mask]
        ch = cbf_hit if mask is None else cbf_hit[mask]
        bn = base_no if mask is None else base_no[mask]
        sm = safe_mask if mask is None else safe_mask[mask]
        sr = safe_reach_2cm if mask is None else safe_reach_2cm[mask]
        pr = phys_reach_2cm if mask is None else phys_reach_2cm[mask]
        pr6 = phys_reach_1cm_ori20 if mask is None else phys_reach_1cm_ori20[mask]
        n = int(bh.size)
        n_base_hit = int(bh.sum())
        n_base_no = int(bn.sum())
        resolved = int((bh & ~ch).sum()) if n_base_hit else 0
        new_hit = int((bn & ch).sum()) if n_base_no else 0
        return {
            "n": n,
            "n_baseline_contact": n_base_hit,
            "n_baseline_no_contact": n_base_no,
            "baseline_contact_rate": _rate(bh),
            "cbf_contact_rate": _rate(ch),
            "no_contact_rate_baseline": _rate(~bh),
            "no_contact_rate_cbf": _rate(~ch),
            "no_contact_delta_pt": float((_rate(~ch) - _rate(~bh)) * 100.0),
            "p_cbf_no_contact_given_base_contact": _rate(~ch[bh]) if n_base_hit else float("nan"),
            "p_cbf_contact_given_base_contact": _rate(ch[bh]) if n_base_hit else float("nan"),
            "n_contact_resolved": resolved,
            "contact_resolve_rate_given_base_contact": _rate(~ch[bh]) if n_base_hit else float("nan"),
            "p_new_contact_given_base_no_contact": _rate(ch[bn]) if n_base_no else float("nan"),
            "n_new_contact": new_hit,
            "cbf_safe_rate": _rate(sm),
            "cbf_safe_rate_given_base_contact": _rate(sm[bh]) if n_base_hit else float("nan"),
            "cbf_safe_rate_given_base_no_contact": _rate(sm[bn]) if n_base_no else float("nan"),
            "safe_reach_2cm_rate": _rate(sr),
            "safe_reach_2cm_given_base_contact": _rate(sr[bh]) if n_base_hit else float("nan"),
            "safe_reach_2cm_given_base_no_contact": _rate(sr[bn]) if n_base_no else float("nan"),
            "phys_reach_2cm_rate": _rate(pr),
            "phys_reach_2cm_given_base_contact": _rate(pr[bh]) if n_base_hit else float("nan"),
            "phys_reach_2cm_given_base_no_contact": _rate(pr[bn]) if n_base_no else float("nan"),
            "phys_reach_1cm_ori20_rate": _rate(pr6),
        }

    out = _one()
    if tiers is not None:
        out["by_tier"] = {
            str(tier): _one(mask=(tiers == tier))
            for tier in sorted({str(t) for t in tiers})
        }
    return out


def _bucket_stats(
    best_dist: np.ndarray,
    best_ori: np.ndarray,
    h_min: np.ndarray | None,
    contact_steps: np.ndarray,
    safe_mask: np.ndarray | None,
    total_steps: np.ndarray | None = None,
) -> dict:
    no_contact = contact_steps == 0
    out: dict[str, float] = {
        **{f"pos_le_{int(t * 100)}cm": _rate(best_dist <= t) for t in POS_THRESH_M},
        **{f"ori_le_{int(t)}deg": _rate(best_ori <= t) for t in ORIENT_BINS_DEG},
        "joint_pos1cm_ori20": _rate((best_dist <= 0.01) & (best_ori <= 20.0)),
        "median_best_dist_mm": float(np.median(best_dist) * 1000.0),
        "p75_best_dist_mm": float(np.percentile(best_dist, 75) * 1000.0),
        "p90_best_dist_mm": float(np.percentile(best_dist, 90) * 1000.0),
        "no_contact_rate": _rate(no_contact),
        "cor_episode": _rate(~no_contact),
        "phys_reach_2cm": _rate(no_contact & (best_dist <= 0.02)),
        "phys_reach_1cm_ori20": _rate(
            no_contact & (best_dist <= 0.01) & (best_ori <= 20.0)
        ),
        "success_strict_2cm": _rate(no_contact & (best_dist <= 0.02)),
        "success_strict_1cm_ori20": _rate(
            no_contact & (best_dist <= 0.01) & (best_ori <= 20.0)
        ),
    }
    if total_steps is not None and total_steps.size:
        ts = np.maximum(total_steps.astype(np.float64), 1.0)
        out["cor_step_mean"] = float(np.mean(contact_steps.astype(np.float64) / ts))
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


def _pct(v: float) -> str:
    return "—" if not math.isfinite(v) else f"{v * 100:.1f}%"


def build_summary_md(
    meta: dict,
    overall: dict,
    by_tier: dict[str, dict],
    conditional: dict | None = None,
    diagnostics: dict | None = None,
) -> str:
    cbf_label = meta.get("cbf_label", "CBF")
    scene_note = meta.get(
        "scene_note",
        f"固定细杆 `{FIXED_ROD_BODY}` @ {FIXED_ROD_POS_M} m",
    )
    lines = [
        "# CBF 避障评测汇总",
        "",
        f"- 生成时间：{meta['timestamp']}",
        f"- Git commit：`{meta.get('git_commit', 'unknown')}`",
        f"- Checkpoint：`{meta['checkpoint']}`",
        f"- MJCF：`{meta['mjcf']}`",
        f"- NPZ：`{meta['npz']}`",
        f"- Episodes：{meta['num_episodes']}（seed={meta['seed']}）",
        f"- **场景**：{scene_note}",
        f"- CBF：d_safe={meta['cbf_d_safe']} γ={meta['cbf_gamma']} activate<{meta['cbf_activate_margin']}",
        "",
        "## 总体对比（原有指标，保留）",
        "",
        f"| 指标 | 无 CBF | {cbf_label} | Δ ({cbf_label}−base) |",
        "|------|--------|--------|--------------|",
    ]

    def _cell(d: dict, key: str, scale: float = 100.0, suffix: str = "%") -> str:
        if key not in d:
            return "—"
        v = d[key] * scale if suffix == "%" else d[key]
        return f"{v:.1f}{suffix}"

    legacy_keys = [
        ("pos_le_1cm", "%"),
        ("pos_le_2cm", "%"),
        ("pos_le_3cm", "%"),
        ("ori_le_20deg", "%"),
        ("joint_pos1cm_ori20", "%"),
        ("cbf_safe_rate", "%"),
        ("safe_reach_2cm", "%"),
        ("safe_reach_1cm_ori20", "%"),
        ("no_contact_rate", "%"),
        ("median_best_dist_mm", "mm"),
        ("p90_best_dist_mm", "mm"),
        ("h_min_median_mm", "mm"),
    ]
    cbf_only_keys = {"cbf_safe_rate", "safe_reach_2cm", "safe_reach_1cm_ori20", "h_min_median_mm"}
    b = overall["baseline"]
    c = overall["cbf"]
    for key, suffix in legacy_keys:
        bl = "—" if key in cbf_only_keys else _cell(b, key, suffix=suffix)
        cv = _cell(c, key, suffix=suffix) if key in c else "—"
        if suffix == "%" and key in b and key in c:
            delta = f"{(c[key] - b[key]) * 100:+.1f} pt"
        elif suffix == "mm" and key in b and key in c:
            delta = f"{c[key] - b[key]:+.1f} mm"
        else:
            delta = "—"
        lines.append(f"| {key.replace('_', ' ')} | {bl} | {cv} | {delta} |")

    if "delta_best_dist_mm" in overall:
        d = overall["delta_best_dist_mm"]
        lines.extend(
            [
                "",
                "## 到达代价（同 idx 配对，原有）",
                "",
                f"- Δbest_dist 中位数：**{d['median_mm']:+.1f} mm**",
                f"- Δbest_dist p75：**{d.get('p75_mm', float('nan')):+.1f} mm**",
                f"- Δbest_dist p90：**{d['p90_mm']:+.1f} mm**",
                f"- 退化 >10 mm（Regress@10mm）：**{d['worse_10mm_rate'] * 100:.1f}%**",
                f"- 退化 >20 mm（Regress@20mm）：**{d.get('worse_20mm_rate', 0.0) * 100:.1f}%**",
            ]
        )

    lines.extend(
        [
            "",
            "## P0 扩展：COR / 物理安全到达 / 严格成功",
            "",
            f"| 指标 | 无 CBF | {cbf_label} | Δ |",
            "|------|--------|--------|---|",
        ]
    )
    p0_keys = [
        ("cor_episode", "%"),
        ("phys_reach_2cm", "%"),
        ("phys_reach_1cm_ori20", "%"),
        ("success_strict_2cm", "%"),
        ("success_strict_1cm_ori20", "%"),
        ("cor_step_mean", "%", 100.0),
    ]
    for item in p0_keys:
        key = item[0]
        suffix = item[1]
        scale = item[2] if len(item) > 2 else 100.0
        bl = _cell(b, key, scale=scale, suffix=suffix)
        cv = _cell(c, key, scale=scale, suffix=suffix) if key in c else "—"
        if suffix == "%" and key in b and key in c:
            delta = f"{(c[key] - b[key]) * 100:+.1f} pt"
        else:
            delta = "—"
        lines.append(f"| {key} | {bl} | {cv} | {delta} |")
    lines.append("")
    lines.append(
        "> **COR_episode** = 至少一步碰杆的回合占比（= 1 − no_contact_rate）。"
        " **PhysReach@2cm** = 无碰杆且 best_dist≤2cm。"
        " **success_strict** 与 PhysReach 同义（碰杆即失败，对齐论文精神）。"
    )

    if conditional is not None:
        c = conditional
        lines.extend(
            [
                "",
                "## 条件概率（原有，保留）",
                "",
                "> `no_contact` = 整局 `contact_steps==0`（任意一步未与杆发生物理接触）。",
                "",
                "### 样本构成",
                "",
                f"- baseline 全程无碰杆：**{c['n_baseline_no_contact']}/{c['n']}** "
                f"({_pct(c['no_contact_rate_baseline'])})",
                f"- baseline 有碰杆：**{c['n_baseline_contact']}/{c['n']}** "
                f"({_pct(c['baseline_contact_rate'])})",
                f"- 全局无碰杆率提升：**{c['no_contact_delta_pt']:+.1f} pt** "
                f"({_pct(c['no_contact_rate_baseline'])} → {_pct(c['no_contact_rate_cbf'])})",
                "",
                "### 2×2：baseline 碰杆与否 × CBF 结果",
                "",
                "| baseline | N | CBF 无碰杆 | CBF 仍碰杆 |",
                "|----------|---|-----------|-----------|",
                f"| 有碰杆 | {c['n_baseline_contact']} | "
                f"{_pct(c['p_cbf_no_contact_given_base_contact'])} "
                f"({c['n_contact_resolved']} 局) | "
                f"{_pct(c['p_cbf_contact_given_base_contact'])} |",
                f"| 无碰杆 | {c['n_baseline_no_contact']} | "
                f"{_pct(1.0 - c['p_new_contact_given_base_no_contact'])} | "
                f"{_pct(c['p_new_contact_given_base_no_contact'])} "
                f"({c['n_new_contact']} 局) |",
                "",
                "### 关键条件指标",
                "",
                "| 指标 | 全体 | baseline 有碰 | baseline 无碰 |",
                "|------|------|-------------|-------------|",
                f"| CBF 消除碰杆 P(无碰\\|base有碰) | — | "
                f"**{_pct(c['contact_resolve_rate_given_base_contact'])}** | — |",
                f"| CBF 新引入碰杆 P(碰\\|base无碰) | — | — | "
                f"**{_pct(c['p_new_contact_given_base_no_contact'])}** |",
                f"| CBF 安全率 P(h_min≥0) | {_pct(c['cbf_safe_rate'])} | "
                f"{_pct(c['cbf_safe_rate_given_base_contact'])} | "
                f"{_pct(c['cbf_safe_rate_given_base_no_contact'])} |",
                f"| SafeReach@2cm | {_pct(c['safe_reach_2cm_rate'])} | "
                f"{_pct(c['safe_reach_2cm_given_base_contact'])} | "
                f"{_pct(c['safe_reach_2cm_given_base_no_contact'])} |",
                f"| PhysReach@2cm | {_pct(c['phys_reach_2cm_rate'])} | "
                f"{_pct(c['phys_reach_2cm_given_base_contact'])} | "
                f"{_pct(c['phys_reach_2cm_given_base_no_contact'])} |",
                "",
                "> **读表提示**：全局 +10 pt 无碰杆会被「本来就不会碰」的样本稀释；"
                "应优先看 `P(无碰|base有碰)` 与 hard 档分层。",
            ]
        )
        if "by_tier" in c:
            lines.extend(
                [
                    "",
                    "### 条件概率 · 按难度分层",
                    "",
                    "| 档位 | N | base有碰 | P(无碰\\|base有碰) | P(碰\\|base无碰) | CBF安全\\|base有碰 |",
                    "|------|---|---------|-------------------|------------------|-------------------|",
                ]
            )
            for tier in ("hard", "medium", "easy"):
                if tier not in c["by_tier"]:
                    continue
                t = c["by_tier"][tier]
                lines.append(
                    f"| {tier} | {t['n']} | {t['n_baseline_contact']} | "
                    f"{_pct(t['contact_resolve_rate_given_base_contact'])} | "
                    f"{_pct(t['p_new_contact_given_base_no_contact'])} | "
                    f"{_pct(t['cbf_safe_rate_given_base_contact'])} |"
                )

    if diagnostics is not None:
        lines.extend(
            [
                "",
                "## P1 扩展：CBF 诊断",
                "",
                f"- h<0 且无碰杆（包络偏瘦/滞后）：**{diagnostics['h_unsafe_no_contact_rate'] * 100:.1f}%**",
                f"- h≥0 但有碰杆（包络漏检）：**{diagnostics['h_safe_with_contact_rate'] * 100:.1f}%**",
                f"- CBF 激活步占比均值：**{diagnostics['cbf_active_ratio_mean'] * 100:.1f}%**",
                f"- CBF 修正步占比均值：**{diagnostics['cbf_corrected_ratio_mean'] * 100:.1f}%**",
                "",
                "**worst_monitor 分布（CBF 局内累计）：**",
                "",
            ]
        )
        for name, cnt in diagnostics.get("worst_monitor_counts", {}).items():
            lines.append(f"- `{name}`：{cnt}")
        if not diagnostics.get("worst_monitor_counts"):
            lines.append("- （无）")

    lines.extend(
        [
            "",
            "## 按难度分层（原有 + P0）",
            "",
            "| 档位 | N | SafeReach@2cm | PhysReach@2cm | pos≤2cm base | pos≤2cm CBF | COR base | COR CBF | h_min 中位 |",
            "|------|---|---------------|---------------|-------------|-------------|----------|---------|-----------|",
        ]
    )
    for tier in ("hard", "medium", "easy"):
        if tier not in by_tier:
            continue
        t = by_tier[tier]
        bl = t["baseline"]
        cb = t["cbf"]
        lines.append(
            f"| {tier} | {t['count']} | "
            f"{cb.get('safe_reach_2cm', float('nan')) * 100:.1f}% | "
            f"{cb.get('phys_reach_2cm', float('nan')) * 100:.1f}% | "
            f"{bl.get('pos_le_2cm', float('nan')) * 100:.1f}% | "
            f"{cb.get('pos_le_2cm', float('nan')) * 100:.1f}% | "
            f"{bl.get('cor_episode', float('nan')) * 100:.1f}% | "
            f"{cb.get('cor_episode', float('nan')) * 100:.1f}% | "
            f"{cb.get('h_min_median_mm', float('nan')):.1f} mm |"
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


def _aggregate_results(
    baseline_results: list[EpisodeResult],
    cbf_results: list[EpisodeResult],
) -> tuple[dict, dict[str, dict], dict, dict]:
    b_dist = np.array([r.best_dist_m for r in baseline_results])
    b_ori = np.array([r.best_ori_deg for r in baseline_results])
    b_contact = np.array([r.contact_steps for r in baseline_results])
    b_total = np.array([r.total_steps for r in baseline_results])
    c_dist = np.array([r.best_dist_m for r in cbf_results])
    c_ori = np.array([r.best_ori_deg for r in cbf_results])
    c_contact = np.array([r.contact_steps for r in cbf_results])
    c_total = np.array([r.total_steps for r in cbf_results])
    c_hmin = np.array([r.h_min_ep_m or float("nan") for r in cbf_results])
    tiers = np.array([r.tier for r in baseline_results])
    safe_mask = c_hmin >= H_SAFE_EPS_M

    overall = {
        "baseline": _bucket_stats(b_dist, b_ori, None, b_contact, None, b_total),
        "cbf": _bucket_stats(c_dist, c_ori, c_hmin, c_contact, safe_mask, c_total),
        "delta_best_dist_mm": {
            "median_mm": float(np.median((c_dist - b_dist) * 1000.0)),
            "p75_mm": float(np.percentile((c_dist - b_dist) * 1000.0, 75)),
            "p90_mm": float(np.percentile((c_dist - b_dist) * 1000.0, 90)),
            "worse_10mm_rate": float(np.mean((c_dist - b_dist) > 0.01)),
            "worse_20mm_rate": float(np.mean((c_dist - b_dist) > 0.02)),
        },
    }

    by_tier: dict[str, dict] = {}
    for tier in sorted({r.tier for r in baseline_results}):
        mask = tiers == tier
        by_tier[tier] = {
            "count": int(mask.sum()),
            "baseline": _bucket_stats(
                b_dist[mask], b_ori[mask], None, b_contact[mask], None, b_total[mask]
            ),
            "cbf": _bucket_stats(
                c_dist[mask],
                c_ori[mask],
                c_hmin[mask],
                c_contact[mask],
                safe_mask[mask],
                c_total[mask],
            ),
        }

    conditional = _compute_conditional_stats(
        b_contact, c_contact, safe_mask, c_dist, c_ori, tiers=tiers
    )

    wm = Counter(r.worst_monitor for r in cbf_results if r.worst_monitor)
    active_ratios = [
        r.active_steps / max(r.total_steps, 1) for r in cbf_results if r.total_steps > 0
    ]
    corrected_ratios = [
        r.corrected_steps / max(r.total_steps, 1) for r in cbf_results if r.total_steps > 0
    ]
    diagnostics = {
        "h_unsafe_no_contact_rate": _rate(
            np.array([r.h_unsafe_no_contact for r in cbf_results])
        ),
        "h_safe_with_contact_rate": _rate(
            np.array([r.h_safe_with_contact for r in cbf_results])
        ),
        "cbf_active_ratio_mean": float(np.mean(active_ratios)) if active_ratios else float("nan"),
        "cbf_corrected_ratio_mean": float(np.mean(corrected_ratios))
        if corrected_ratios
        else float("nan"),
        "worst_monitor_counts": dict(wm.most_common()),
    }
    return overall, by_tier, conditional, diagnostics


def _aggregate_baseline_only(baseline_results: list[EpisodeResult]) -> tuple[dict, dict[str, dict]]:
    b_dist = np.array([r.best_dist_m for r in baseline_results])
    b_ori = np.array([r.best_ori_deg for r in baseline_results])
    b_contact = np.array([r.contact_steps for r in baseline_results])
    b_total = np.array([r.total_steps for r in baseline_results])
    tiers = np.array([r.tier for r in baseline_results])
    overall = {"baseline": _bucket_stats(b_dist, b_ori, None, b_contact, None, b_total)}
    by_tier: dict[str, dict] = {}
    for tier in sorted({r.tier for r in baseline_results}):
        mask = tiers == tier
        by_tier[tier] = {
            "count": int(mask.sum()),
            "baseline": _bucket_stats(
                b_dist[mask], b_ori[mask], None, b_contact[mask], None, b_total[mask]
            ),
        }
    return overall, by_tier


def _write_summary(
    out_dir: Path,
    meta: dict,
    overall: dict,
    by_tier: dict[str, dict],
    conditional: dict,
    diagnostics: dict,
) -> None:
    payload = {
        "meta": meta,
        "overall": overall,
        "conditional": conditional,
        "diagnostics": diagnostics,
        "by_tier": by_tier,
    }
    summary_json = out_dir / "summary.json"
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    summary_md = build_summary_md(
        meta, overall, by_tier, conditional=conditional, diagnostics=diagnostics
    )
    summary_path = out_dir / "summary.md"
    summary_path.write_text(summary_md, encoding="utf-8")
    print(f"[eval_cbf] summary → {summary_path}")


def summarize_from_csv(csv_path: Path, out_dir: Path, meta: dict | None = None) -> int:
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    if not rows:
        print(f"[ERROR] empty csv: {csv_path}", file=sys.stderr)
        return 1
    required = {
        "baseline_contact_steps",
        "cbf_contact_steps",
        "cbf_safe",
        "cbf_best_dist_mm",
        "tier",
    }
    if not required.issubset(rows[0].keys()):
        print(f"[ERROR] csv missing paired baseline/cbf columns: {csv_path}", file=sys.stderr)
        return 1

    baseline_results: list[EpisodeResult] = []
    cbf_results: list[EpisodeResult] = []
    for r in rows:
        tier = r["tier"]
        idx = int(r["idx"])
        tp = np.array([float(r["target_x"]), float(r["target_y"]), float(r["target_z"])])
        baseline_results.append(
            EpisodeResult(
                idx=idx,
                tier=tier,
                target_pos=tp,
                enable_cbf=False,
                best_dist_m=float(r["baseline_best_dist_mm"]) / 1000.0,
                best_ori_deg=float(r["baseline_best_ori_deg"]),
                end_dist_m=float(r["baseline_end_dist_mm"]) / 1000.0,
                contact_steps=int(r["baseline_contact_steps"]),
                total_steps=int(r.get("total_steps") or 300),
            )
        )
        h_mm = float(r["cbf_h_min_ep_mm"])
        contact = int(r["cbf_contact_steps"])
        safe = int(r.get("cbf_safe", 0)) == 1
        cbf_results.append(
            EpisodeResult(
                idx=idx,
                tier=tier,
                target_pos=tp,
                enable_cbf=True,
                best_dist_m=float(r["cbf_best_dist_mm"]) / 1000.0,
                best_ori_deg=float(r["cbf_best_ori_deg"]),
                end_dist_m=float(r["cbf_end_dist_mm"]) / 1000.0,
                contact_steps=contact,
                total_steps=int(r.get("total_steps") or 300),
                h_min_ep_m=h_mm / 1000.0,
                infeas_steps=int(r.get("cbf_infeas_steps") or 0),
                corrected_steps=int(r.get("cbf_corrected_steps") or 0),
                active_steps=int(r.get("cbf_active_steps") or 0),
                max_dq_cbf=float(r.get("cbf_max_dq_cbf") or 0.0),
                worst_monitor=str(r.get("cbf_worst_monitor") or ""),
                h_unsafe_no_contact=bool(
                    int(r.get("cbf_h_unsafe_no_contact") or (h_mm < 0 and contact == 0))
                ),
                h_safe_with_contact=bool(
                    int(r.get("cbf_h_safe_with_contact") or (h_mm >= 0 and contact > 0))
                ),
            )
        )

    overall, by_tier, conditional, diagnostics = _aggregate_results(baseline_results, cbf_results)
    if meta is None:
        old_json = out_dir / "summary.json"
        if old_json.is_file():
            meta = json.loads(old_json.read_text(encoding="utf-8")).get("meta", {})
        else:
            meta = {}
    meta = {
        **meta,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "summarized_from_csv": str(csv_path),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_summary(out_dir, meta, overall, by_tier, conditional, diagnostics)
    return 0


def _build_meta(args: argparse.Namespace, ckpt: Path, mjcf: Path, npz: Path, indices_path: Path) -> dict:
    scene_note = "无避障杆（对照上限）" if args.no_obstacle else (
        f"固定细杆 `{FIXED_ROD_BODY}` @ {FIXED_ROD_POS_M} m"
    )
    return {
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
        "cbf_label": str(args.cbf_label),
        "no_obstacle": bool(args.no_obstacle),
        "scene_note": scene_note,
        "fixed_rod_body": FIXED_ROD_BODY,
        "fixed_rod_pos_m": list(FIXED_ROD_POS_M),
    }


def evaluate(args: argparse.Namespace) -> int:
    ckpt = Path(args.checkpoint).expanduser().resolve()
    mjcf = Path(args.mjcf).expanduser().resolve()
    if args.no_obstacle:
        mjcf = Path(args.mjcf_norod).expanduser().resolve()
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
    obstacle_gid = -1 if args.no_obstacle else _try_obstacle_geom_id(model, FIXED_ROD_BODY)
    if not args.no_obstacle and obstacle_gid < 0:
        print(f"[ERROR] obstacle geom not found: {FIXED_ROD_BODY}", file=sys.stderr)
        return 1
    if args.no_obstacle:
        print("[eval_cbf] 无杆对照：仅跑 baseline（忽略 CBF）")
        args.cbf_only = False
        if not args.baseline_only:
            args.baseline_only = True

    cbf_cfg = CbfConfig(
        d_safe=float(args.cbf_d_safe),
        gamma=float(args.cbf_gamma),
        lambda_cbf=float(args.cbf_lambda),
        dq_max=float(args.action_scale),
        activate_margin=float(args.cbf_activate_margin),
        capsule_sample_count=int(args.cbf_capsule_samples),
        qp_metric=str(args.cbf_qp_metric),
        task_preserve_weight=float(args.cbf_task_preserve_weight),
        target_guidance=bool(args.cbf_target_guidance),
        target_guidance_clearance=float(args.cbf_target_guidance_clearance),
        target_guidance_reach=float(args.cbf_target_guidance_reach),
        target_guidance_forward=float(args.cbf_target_guidance_forward),
        target_guidance_dynamic_clearance=float(args.cbf_target_guidance_dynamic_clearance),
        target_guidance_dynamic_forward=float(args.cbf_target_guidance_dynamic_forward),
        target_guidance_dynamic_speed_thresh=float(args.cbf_target_guidance_dynamic_speed_thresh),
        target_guidance_dynamic_closing_speed_thresh=float(args.cbf_target_guidance_dynamic_closing_speed_thresh),
        target_guidance_release_steps=int(args.cbf_target_guidance_release_steps),
        target_guidance_switch_slack=float(args.cbf_target_guidance_switch_slack),
        target_guidance_dynamic_lookahead_steps=float(args.cbf_target_guidance_dynamic_lookahead_steps),
        dynamic_obstacle_lookahead_steps=float(args.cbf_dynamic_lookahead_steps),
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
        cbf_filter_tau=float(args.cbf_filter_tau),
        enable_cbf_correction_filter=bool(args.cbf_correction_filter),
        cbf_bypass_filter_when_unsafe=bool(args.cbf_bypass_filter_when_unsafe),
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
                    "total_steps": bi.total_steps,
                    "baseline_best_dist_mm": f"{bi.best_dist_m * 1000:.3f}",
                    "baseline_best_ori_deg": f"{bi.best_ori_deg:.3f}",
                    "baseline_end_dist_mm": f"{bi.end_dist_m * 1000:.3f}",
                    "baseline_contact_steps": bi.contact_steps,
                    "baseline_cor_episode": int(bi.contact_steps > 0),
                    "cbf_best_dist_mm": f"{ci.best_dist_m * 1000:.3f}",
                    "cbf_best_ori_deg": f"{ci.best_ori_deg:.3f}",
                    "cbf_end_dist_mm": f"{ci.end_dist_m * 1000:.3f}",
                    "cbf_h_min_ep_mm": f"{(ci.h_min_ep_m or float('nan')) * 1000:.3f}",
                    "cbf_infeas_steps": ci.infeas_steps,
                    "cbf_active_steps": ci.active_steps,
                    "cbf_corrected_steps": ci.corrected_steps,
                    "cbf_max_dq_cbf": f"{ci.max_dq_cbf:.6f}",
                    "cbf_worst_monitor": ci.worst_monitor,
                    "cbf_contact_steps": ci.contact_steps,
                    "cbf_cor_episode": int(ci.contact_steps > 0),
                    "cbf_safe": int(safe),
                    "cbf_h_unsafe_no_contact": int(ci.h_unsafe_no_contact),
                    "cbf_h_safe_with_contact": int(ci.h_safe_with_contact),
                    "cbf_phys_reach_2cm": int(ci.contact_steps == 0 and ci.best_dist_m <= 0.02),
                    "delta_best_dist_mm": f"{delta_mm:.3f}",
                    "regress_10mm": int(delta_mm > 10.0),
                    "regress_20mm": int(delta_mm > 20.0),
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
        overall, by_tier, conditional, diagnostics = _aggregate_results(
            baseline_results, cbf_results
        )
        meta = _build_meta(args, ckpt, mjcf, npz, indices_path)
        _write_summary(out_dir, meta, overall, by_tier, conditional, diagnostics)
    elif baseline_results and args.no_obstacle:
        overall, by_tier = _aggregate_baseline_only(baseline_results)
        meta = _build_meta(args, ckpt, mjcf, npz, indices_path)
        empty_cond = {"n": len(baseline_results), "note": "baseline-only norod"}
        empty_diag = {"note": "baseline-only norod"}
        payload = {
            "meta": meta,
            "overall": overall,
            "by_tier": by_tier,
            "conditional": empty_cond,
            "diagnostics": empty_diag,
        }
        (out_dir / "summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        lines = [
            "# 无杆对照（baseline only）",
            "",
            f"- seed={meta['seed']}  N={meta['num_episodes']}",
            f"- pos≤2cm：**{overall['baseline']['pos_le_2cm'] * 100:.1f}%**",
            f"- pos≤1cm：**{overall['baseline']['pos_le_1cm'] * 100:.1f}%**",
            f"- 6D pos≤1cm∧ori≤20°：**{overall['baseline']['joint_pos1cm_ori20'] * 100:.1f}%**",
            "",
            "> 用于计算 obstacle tax：对比同 idx 有杆 baseline 的 Reach@2cm。",
        ]
        (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"[eval_cbf] summary → {out_dir / 'summary.md'}")

    return 0


def _summary_get(d: dict, path: str) -> float:
    cur: object = d
    for p in path.split("."):
        cur = cur[p]  # type: ignore[index]
    return float(cur)


MULTI_SEED_METRICS: list[tuple[str, str]] = [
    ("overall.baseline.pos_le_2cm", "pos≤2cm (base)"),
    ("overall.baseline.no_contact_rate", "无碰杆 (base)"),
    ("overall.baseline.cor_episode", "COR (base)"),
    ("overall.baseline.phys_reach_2cm", "PhysReach@2cm (base)"),
    ("overall.cbf.pos_le_2cm", "pos≤2cm (CBF)"),
    ("overall.cbf.no_contact_rate", "无碰杆 (CBF)"),
    ("overall.cbf.cor_episode", "COR (CBF)"),
    ("overall.cbf.phys_reach_2cm", "PhysReach@2cm (CBF)"),
    ("overall.cbf.safe_reach_2cm", "SafeReach@2cm (CBF)"),
    ("conditional.contact_resolve_rate_given_base_contact", "P(无碰|base有碰)"),
    ("conditional.p_new_contact_given_base_no_contact", "P(新碰|base无碰)"),
    ("overall.delta_best_dist_mm.worse_10mm_rate", "Regress@10mm"),
]


def _aggregate_multi_seed(summaries: list[dict]) -> dict:
    """对多次 seed 的 summary.json 做关键指标均值/标准差。"""
    out: dict[str, dict] = {}
    for key, _label in MULTI_SEED_METRICS:
        vals = [_summary_get(s, key) for s in summaries]
        arr = np.asarray(vals, dtype=np.float64)
        out[key] = {
            "mean": float(arr.mean()),
            "std": float(arr.std(ddof=0)),
            "values": vals,
        }
    return out


def _build_multi_seed_summary_md(
    seeds: list[int],
    summaries: list[dict],
    aggregate: dict,
    cbf_label: str = "CBF",
) -> str:
    lines = [
        "# 多 seed CBF 评测汇总",
        "",
        f"- Seeds：{', '.join(str(s) for s in seeds)}（各 {len(seeds)} 次独立抽样）",
        f"- 每 seed：256 局 baseline + {cbf_label}（见 `seed_XX/summary.md`）",
        "",
        "## 跨 seed 均值 ± 标准差",
        "",
        "| 指标 | mean | std | 各 seed |",
        "|------|------|-----|---------|",
    ]
    for key, label in MULTI_SEED_METRICS:
        if key not in aggregate:
            continue
        a = aggregate[key]
        vals = a["values"]
        per_seed = ", ".join(f"{v * 100:.1f}%" for v in vals)
        lines.append(
            f"| {label} | {a['mean'] * 100:.1f}% | {a['std'] * 100:.1f}% | {per_seed} |"
        )
    lines.extend(
        [
            "",
            "## 各 seed 明细",
            "",
            "| seed | pos≤2cm base | pos≤2cm CBF | COR base | COR CBF | PhysReach CBF | 无碰杆 CBF |",
            "|------|-------------|-------------|----------|---------|---------------|-----------|",
        ]
    )
    for seed, s in zip(seeds, summaries):
        b = s["overall"]["baseline"]
        c = s["overall"]["cbf"]
        lines.append(
            f"| {seed} | {b['pos_le_2cm'] * 100:.1f}% | {c['pos_le_2cm'] * 100:.1f}% | "
            f"{b['cor_episode'] * 100:.1f}% | {c['cor_episode'] * 100:.1f}% | "
            f"{c['phys_reach_2cm'] * 100:.1f}% | {c['no_contact_rate'] * 100:.1f}% |"
        )
    lines.append("")
    lines.append(
        "> 未指定 `--indices-file` 时，每个 seed 独立抽样目标 idx（推荐，用于稳健性）。"
        " 指定同一 indices 文件则各 seed 目标相同（仅作复现校验）。"
    )
    return "\n".join(lines) + "\n"


def run_multi_seed(args: argparse.Namespace) -> int:
    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    if not seeds:
        print("[ERROR] --seeds 为空", file=sys.stderr)
        return 1
    root = Path(args.out_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    summaries: list[dict] = []
    for seed in seeds:
        sub = root / f"seed_{seed}"
        sub_args = argparse.Namespace(**{**vars(args), "seed": seed, "out_dir": str(sub), "seeds": ""})
        print(f"[eval_cbf] multi-seed → seed={seed} out={sub}")
        rc = evaluate(sub_args)
        if rc != 0:
            return rc
        sj = sub / "summary.json"
        if sj.is_file():
            summaries.append(json.loads(sj.read_text(encoding="utf-8")))
    if summaries:
        agg = _aggregate_multi_seed(summaries)
        cbf_label = str(args.cbf_label)
        payload = {
            "seeds": seeds,
            "cbf_label": cbf_label,
            "aggregate": agg,
            "runs": [s.get("meta", {}) for s in summaries],
        }
        json_path = root / "multi_seed_summary.json"
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        md_path = root / "multi_seed_summary.md"
        md_path.write_text(
            _build_multi_seed_summary_md(seeds, summaries, agg, cbf_label=cbf_label),
            encoding="utf-8",
        )
        print(f"[eval_cbf] multi_seed_summary → {json_path}")
        print(f"[eval_cbf] multi_seed_summary → {md_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MuJoCo CBF fixed-rod batch eval")
    p.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument(
        "--mjcf-norod",
        type=str,
        default=str(DEFAULT_MJCF_NOROD),
        help="无杆对照场景（配合 --no-obstacle）",
    )
    p.add_argument("--npz", type=str, default=str(DEFAULT_NPZ_TEST))
    p.add_argument("--out-dir", type=str, default=str(_THIS.parent / "logs" / "eval" / "cbf_fixed_rod"))
    p.add_argument("--num-episodes", type=int, default=256)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--seeds",
        type=str,
        default="",
        help="多 seed 批量：例 42,0,1,100；各写入 out-dir/seed_XX/ 并生成 multi_seed_summary.json",
    )
    p.add_argument(
        "--cbf-label",
        type=str,
        default="CBF",
        help="summary 表头中 CBF 列名称（例：CBF v2.1）",
    )
    p.add_argument(
        "--no-obstacle",
        action="store_true",
        help="无杆对照：仅用 mjcf-norod 跑 baseline（obstacle tax 上限）",
    )
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
    p.add_argument("--cbf-filter-tau", type=float, default=CBF_FILTER_TAU)
    p.add_argument(
        "--cbf-correction-filter",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="是否对 CBF 修正做一阶滤波；共享运行时默认保持开启",
    )
    p.add_argument(
        "--cbf-bypass-filter-when-unsafe",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="仿真增强：h_min<0 时是否绕过 CBF 修正滤波",
    )
    p.add_argument("--cbf-d-safe", type=float, default=CBF_D_SAFE)
    p.add_argument("--cbf-gamma", type=float, default=CBF_GAMMA)
    p.add_argument(
        "--cbf-lambda",
        type=float,
        default=CBF_LAMBDA,
        help="仿真 CBF lambda 兼容参数；task-preserving 权重单独设置",
    )
    p.add_argument("--cbf-activate-margin", type=float, default=CBF_ACTIVATE_MARGIN)
    p.add_argument(
        "--cbf-capsule-samples",
        type=int,
        default=17,
        help="仿真增强配置：每段 capsule 采样数（共享/真机默认仍为 9）",
    )
    p.add_argument(
        "--cbf-qp-metric",
        choices=("identity", "task_preserving"),
        default="task_preserving",
        help="仿真 QP 修正 metric；默认显式启用 task_preserving",
    )
    p.add_argument(
        "--cbf-task-preserve-weight",
        type=float,
        default=5.0,
        help="task_preserving metric 的 TCP Jacobian 权重；不复用 lambda_cbf",
    )
    p.add_argument("--cbf-target-guidance", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--cbf-target-guidance-clearance", type=float, default=0.07)
    p.add_argument("--cbf-target-guidance-reach", type=float, default=0.04)
    p.add_argument("--cbf-target-guidance-forward", type=float, default=0.0)
    p.add_argument("--cbf-target-guidance-dynamic-clearance", type=float, default=0.14)
    p.add_argument("--cbf-target-guidance-dynamic-forward", type=float, default=0.04)
    p.add_argument("--cbf-target-guidance-dynamic-speed-thresh", type=float, default=1e-4)
    p.add_argument("--cbf-target-guidance-dynamic-closing-speed-thresh", type=float, default=1e-4)
    p.add_argument("--cbf-target-guidance-release-steps", type=int, default=32)
    p.add_argument("--cbf-target-guidance-switch-slack", type=float, default=0.05)
    p.add_argument("--cbf-target-guidance-dynamic-lookahead-steps", type=float, default=2.0)
    p.add_argument(
        "--cbf-dynamic-lookahead-steps",
        type=float,
        default=0.0,
        help=(
            "按障碍物速度预测的 lookahead 步数；障碍物速度为 0 时不增加 dynamic padding。"
            "本静态评测入口默认 0.0，属于入口默认而非 shared CBF 全局默认。"
        ),
    )
    p.add_argument(
        "--summarize-only",
        action="store_true",
        help="仅从已有 episodes.csv 重算 summary（不跑仿真）",
    )
    p.add_argument(
        "--episodes-csv",
        type=str,
        default="",
        help="配合 --summarize-only，默认 out-dir/episodes.csv",
    )
    return p


if __name__ == "__main__":
    cli = build_parser()
    ns = cli.parse_args()
    if ns.summarize_only:
        out_dir = Path(ns.out_dir).expanduser().resolve()
        csv_path = (
            Path(ns.episodes_csv).expanduser().resolve()
            if ns.episodes_csv
            else out_dir / "episodes.csv"
        )
        raise SystemExit(summarize_from_csv(csv_path, out_dir))
    if ns.seeds:
        raise SystemExit(run_multi_seed(ns))
    raise SystemExit(evaluate(ns))
