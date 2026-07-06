#!/usr/bin/env python3
"""对比多个 checkpoint 的纯推理指标：位置 & 姿态误差分档（10°/20°/30°）。

示例：
  cd ~/isaac_lab/isaac_ws/IsaacLab
  ./isaaclab.sh -p ../rl_code/soarm100sim/rl/eval_orient_bins.py --headless \\
    --checkpoint-a ../rl_code/soarm100sim/rl/checkpoints/.../agent_102400.pt \\
    --name-a 2026-07-03_cfg1 \\
    --checkpoint-b ../rl_code/soarm100sim/rl/checkpoints/.../best_agent.pt \\
    --name-b 2026-07-06_cfg2_pathA \\
    --num_envs 64 --num-episodes 256
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

RL_ROOT = Path(__file__).resolve().parent

_pre = argparse.ArgumentParser(add_help=False)
_pre.add_argument("--checkpoint-a", type=str, required=True)
_pre.add_argument("--checkpoint-b", type=str, required=True)
_pre.add_argument("--num_envs", type=int, default=64)
_pre_args, _remaining = _pre.parse_known_args()

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="SO-100 Reach orientation-bin eval")
parser.add_argument("--checkpoint-a", type=str, required=True)
parser.add_argument("--checkpoint-b", type=str, required=True)
parser.add_argument("--name-a", type=str, default="ckpt_a")
parser.add_argument("--name-b", type=str, default="ckpt_b")
parser.add_argument("--num_envs", type=int, default=64)
parser.add_argument("--num-episodes", type=int, default=256, help="累计 episode 结束次数（跨 env 总和）")
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--use-train-npz", action="store_true")
parser.add_argument(
    "--home-start",
    action="store_true",
    help="评测时起点固定为 home（reset_start_from_bank=False），便于与历史 A/B 对比",
)
parser.add_argument(
    "--out-json",
    type=str,
    default=str(RL_ROOT / "logs" / "eval" / "orient_bins_compare.json"),
)
parser.add_argument(
    "--out-md",
    type=str,
    default=str(RL_ROOT / "logs" / "eval" / "log.md"),
)
AppLauncher.add_app_launcher_args(parser)
parser.set_defaults(headless=True)
args_cli, hydra_args = parser.parse_known_args()
sys.argv = [sys.argv[0]] + hydra_args

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

sys.path.insert(0, str(RL_ROOT))

import torch
from inference_runtime import create_inference_stack, resolve_checkpoint


ORIENT_BINS_DEG = (10.0, 20.0, 30.0)
POS_THRESH_M = (0.01, 0.02, 0.03)


def _stats_bucket(pos: np.ndarray, ori: np.ndarray) -> dict:
    return {
        "position": {
            "mean_m": float(pos.mean()),
            "median_m": float(np.median(pos)),
            "p90_m": float(np.percentile(pos, 90)),
            **{f"success_le_{int(t * 100)}cm": float((pos <= t).mean()) for t in POS_THRESH_M},
        },
        "orientation": {
            "mean_deg": float(ori.mean()),
            "median_deg": float(np.median(ori)),
            "p90_deg": float(np.percentile(ori, 90)),
            **{f"success_le_{int(t)}deg": float((ori <= t).mean()) for t in ORIENT_BINS_DEG},
        },
        "joint_success": {
            f"pos1cm_ori_le_{int(t)}deg": float(((pos <= 0.01) & (ori <= t)).mean())
            for t in ORIENT_BINS_DEG
        },
    }


def evaluate_checkpoint(
    stack: dict,
    checkpoint: str,
    *,
    name: str,
    num_episodes: int,
) -> dict:
    env = stack["env"]
    reach_env = stack["reach_env"]
    runner = stack["runner"]
    ckpt = resolve_checkpoint(checkpoint)
    runner.agent.load(ckpt)
    runner.agent.set_running_mode("eval")

    obs, _ = env.reset()
    # episode-end（结束瞬间）与 episode-best（回合内最优）
    end_pos: list[float] = []
    end_ori: list[float] = []
    best_pos: list[float] = []
    best_ori: list[float] = []
    waves = 0
    max_waves = max(4, (num_episodes // max(1, reach_env.num_envs)) + 2)

    while len(end_pos) < num_episodes and waves < max_waves:
        with torch.inference_mode():
            outputs = runner.agent.act(obs, timestep=0, timesteps=0)
            actions = outputs[-1].get("mean_actions", outputs[0])
            obs, _rewards, terminated, truncated, _info = env.step(actions)
        done = terminated | truncated
        if not torch.any(done):
            continue
        # 使用 reach_env 在 reset 前缓存的 done 快照（见 ReachEnv._get_dones）
        if reach_env._last_done_pos_err.numel() == 0:
            continue
        end_pos.extend(reach_env._last_done_pos_err.detach().cpu().numpy().reshape(-1).tolist())
        end_ori.extend(reach_env._last_done_ori_deg.detach().cpu().numpy().reshape(-1).tolist())
        best_pos.extend(reach_env._last_done_min_pos_err.detach().cpu().numpy().reshape(-1).tolist())
        best_ori.extend(reach_env._last_done_min_ori_deg.detach().cpu().numpy().reshape(-1).tolist())
        waves += 1
        print(
            f"[{name}] episode_ends={len(end_pos)}/{num_episodes} waves={waves}",
            flush=True,
        )

    end_pos_a = np.asarray(end_pos[:num_episodes], dtype=np.float64)
    end_ori_a = np.asarray(end_ori[:num_episodes], dtype=np.float64)
    best_pos_a = np.asarray(best_pos[:num_episodes], dtype=np.float64)
    best_ori_a = np.asarray(best_ori[:num_episodes], dtype=np.float64)
    n = int(end_pos_a.shape[0])
    if n == 0:
        raise RuntimeError(f"{name}: 未收集到任何 episode 样本")

    out = {
        "name": name,
        "checkpoint": ckpt,
        "num_episodes": n,
        "episode_end": _stats_bucket(end_pos_a, end_ori_a),
        "episode_best": _stats_bucket(best_pos_a, best_ori_a),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2), flush=True)
    return out


def _pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def _table_orient(a_blk: dict, b_blk: dict) -> list[str]:
    rows = [
        "| 阈值 | A (7.3) | B (今日续训) | Δ (B−A) |",
        "|------|---------|--------------|---------|",
    ]
    for t in ORIENT_BINS_DEG:
        key = f"success_le_{int(t)}deg"
        va, vb = a_blk["orientation"][key], b_blk["orientation"][key]
        rows.append(f"| ≤ {int(t)}° | {_pct(va)} | {_pct(vb)} | {100.0 * (vb - va):+.1f} pt |")
    oa, ob = a_blk["orientation"], b_blk["orientation"]
    rows.append(
        f"| 均值 / 中位数 / P90 | {oa['mean_deg']:.1f}° / {oa['median_deg']:.1f}° / {oa['p90_deg']:.1f}° | "
        f"{ob['mean_deg']:.1f}° / {ob['median_deg']:.1f}° / {ob['p90_deg']:.1f}° | — |"
    )
    return rows


def _table_pos(a_blk: dict, b_blk: dict) -> list[str]:
    rows = [
        "| 阈值 | A (7.3) | B (今日续训) | Δ (B−A) |",
        "|------|---------|--------------|---------|",
    ]
    for t in POS_THRESH_M:
        key = f"success_le_{int(t * 100)}cm"
        va, vb = a_blk["position"][key], b_blk["position"][key]
        rows.append(f"| ≤ {t * 100:.0f} cm | {_pct(va)} | {_pct(vb)} | {100.0 * (vb - va):+.1f} pt |")
    pa, pb = a_blk["position"], b_blk["position"]
    rows.append(
        f"| 均值 / 中位数 / P90 | "
        f"{100 * pa['mean_m']:.2f} / {100 * pa['median_m']:.2f} / {100 * pa['p90_m']:.2f} cm | "
        f"{100 * pb['mean_m']:.2f} / {100 * pb['median_m']:.2f} / {100 * pb['p90_m']:.2f} cm | — |"
    )
    return rows


def _table_joint(a_blk: dict, b_blk: dict) -> list[str]:
    rows = [
        "| 条件 | A (7.3) | B (今日续训) | Δ (B−A) |",
        "|------|---------|--------------|---------|",
    ]
    for t in ORIENT_BINS_DEG:
        key = f"pos1cm_ori_le_{int(t)}deg"
        va, vb = a_blk["joint_success"][key], b_blk["joint_success"][key]
        rows.append(f"| pos≤1cm ∧ ori≤{int(t)}° | {_pct(va)} | {_pct(vb)} | {100.0 * (vb - va):+.1f} pt |")
    return rows


def write_markdown(path: str, results: list[dict], meta: dict) -> None:
    a, b = results[0], results[1]
    a_best, b_best = a["episode_best"], b["episode_best"]
    a_end, b_end = a["episode_end"], b["episode_end"]

    lines = [
        "# SO-100 Reach 推理对比日志",
        "",
        f"- 生成时间：{meta['wall_time']}",
        f"- 评测 episode 数（各权重）：{meta['num_episodes']}",
        f"- 并行 env：{meta['num_envs']}，seed={meta['seed']}",
        f"- NPZ：{'train' if meta['use_train_npz'] else 'test'} (`workspace_tcp_merged_{'train' if meta['use_train_npz'] else 'test'}.npz`)",
        "- **主表（推荐）**：回合内最优误差（episode-best，对齐训练 `ever_*`）",
        "- **附表**：episode 结束瞬间误差（可能因震荡略差于 best）",
        "",
        "## 对比对象",
        "",
        "| 代号 | 名称 | Checkpoint |",
        "|------|------|------------|",
        f"| A | {a['name']} | `{a['checkpoint']}` |",
        f"| B | {b['name']} | `{b['checkpoint']}` |",
        "",
        "### 背景简述",
        "",
        "- **A（7.3）**：`ReachEnvCfg`（cfg1）正式训练，最终 `agent_102400.pt`；训练日志位置高、姿态一般。",
        "- **B（今天方案 A 续训）**：从 A 加载，`ReachEnvCfg2`（orient_scale=3、success_scale=8、hold=15、orient_dist_th=0.05）续训 150 iter；`best_agent.pt`。",
        "",
        "## 姿态误差分档成功率（episode-best，主表）",
        "",
        "姿态误差角：\\(\\theta = 2\\arccos(|q\\cdot q_{des}|)\\)（度）。**回合内任意时刻**最小误差计入成功。",
        "",
    ]
    lines += _table_orient(a_best, b_best)
    lines += [
        "",
        "## 位置误差成功率（episode-best）",
        "",
    ]
    lines += _table_pos(a_best, b_best)
    lines += [
        "",
        "## 联合成功 episode-best（位置 ≤1cm 且姿态 ≤阈值）",
        "",
    ]
    lines += _table_joint(a_best, b_best)
    lines += [
        "",
        "## 附表：episode 结束瞬间",
        "",
        "### 姿态",
        "",
    ]
    lines += _table_orient(a_end, b_end)
    lines += [
        "",
        "### 位置",
        "",
    ]
    lines += _table_pos(a_end, b_end)
    lines += [
        "",
        "### 联合",
        "",
    ]
    lines += _table_joint(a_end, b_end)

    ori10_a = a_best["orientation"]["success_le_10deg"]
    ori10_b = b_best["orientation"]["success_le_10deg"]
    pos_a = a_best["position"]["success_le_1cm"]
    pos_b = b_best["position"]["success_le_1cm"]
    if ori10_b >= ori10_a and pos_b >= pos_a - 0.05:
        summary = "B 在姿态分档上整体更优或持平，位置指标未出现大幅崩塌，适合作为姿态向的候选主权重。"
    elif ori10_b > ori10_a and pos_b < pos_a - 0.05:
        summary = "B 姿态更好，但位置成功率有所下降：存在位置–姿态 trade-off；是否采用取决于任务更偏姿态还是位置。"
    elif ori10_b < ori10_a:
        summary = "B 相对 A 姿态收益不明显/变差，建议主用 A，或回查续训与评测设置。"
    else:
        summary = "两版接近，详见上表数值。"

    lines += [
        "",
        "## 结论摘要",
        "",
        summary,
        "",
        "## 说明",
        "",
        "- 误差在 `ReachEnv._get_dones` **reset 之前**快照，避免读到 home 姿态。",
        "- episode-best = 回合内最小位置/姿态误差；更接近训练曲线的 `ever_*`。",
        "- ≤10° 对应训练 `orientation_enter_dot_threshold=0.9962`（\\(\\alpha=\\cos(\\theta/2)\\)）。",
        "- 原始 JSON：`rl/logs/eval/orient_bins_compare.json`。",
        "- 复现：`rl/eval_orient_bins.py`。",
        "",
    ]

    out_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"[DONE] markdown -> {out_path}", flush=True)


# --- main ---
stack = create_inference_stack(
    checkpoint=args_cli.checkpoint_a,
    num_envs=args_cli.num_envs,
    seed=args_cli.seed,
    use_test_npz=not args_cli.use_train_npz,
    enable_contact_sensors=False,
    debug_vis=False,
    reset_start_from_bank=False if args_cli.home_start else None,
)

results = []
for name, ckpt in (
    (args_cli.name_a, args_cli.checkpoint_a),
    (args_cli.name_b, args_cli.checkpoint_b),
):
    results.append(
        evaluate_checkpoint(
            stack,
            ckpt,
            name=name,
            num_episodes=args_cli.num_episodes,
        )
    )

meta = {
    "wall_time": datetime.now().isoformat(timespec="seconds"),
    "num_episodes": args_cli.num_episodes,
    "num_envs": args_cli.num_envs,
    "seed": args_cli.seed,
    "use_train_npz": bool(args_cli.use_train_npz),
    "home_start": bool(args_cli.home_start),
}
os.makedirs(os.path.dirname(os.path.abspath(args_cli.out_json)) or ".", exist_ok=True)
with open(args_cli.out_json, "w", encoding="utf-8") as handle:
    json.dump({"meta": meta, "results": results}, handle, ensure_ascii=False, indent=2)
print(f"[DONE] json -> {args_cli.out_json}", flush=True)

write_markdown(args_cli.out_md, results, meta)

stack["env"].close()
if simulation_app.is_running():
    simulation_app.close()
