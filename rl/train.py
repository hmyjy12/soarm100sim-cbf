#!/usr/bin/env python3
"""SO-100 Plus 单臂 6D Reach — skrl PPO 训练入口。

任务：从 workspace NPZ 随机采样捏合中心 TCP 6D 目标，PPO 控制 7 关节到达。
观测 27 维、动作 7 维；环境与奖励见 reach_env_cfg.py（稳定默认）/ reach_env_cfg2.py（姿态实验）/ reach_env.py。

================================================================================
启动方式
================================================================================

0) 前置
   - 已完成采样：rl/workspace_cache/workspace_tcp_merged_train.npz（见 sample.py）
   - USD 已生成：rl/assets/so100_plus.usd

1) 默认正式训练（headless，512 env × 500 iter）
   cd ~/isaac_lab/isaac_ws/IsaacLab
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless

2) 小规模试训（快速验证管线）
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless \\
     --num_envs 64 --max_iterations 50

3) 续训（加载已有 checkpoint；新目录名带 _resume，并写 RESUME.txt）
   cd ~/isaac_lab/isaac_ws/IsaacLab
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless \\
     --checkpoint ../rl_code/soarm100sim/rl/checkpoints/2026-07-03_18-11-38/26-07-03_18-11-38-258181_PPO/checkpoints/agent_102400.pt \\
     --max_iterations 150

3b) 指定环境配置（默认 1=稳定；2/ori=姿态实验 cfg2）
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless --env-cfg 1
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless --env-cfg 2 \\
     --checkpoint .../agent_102400.pt --max_iterations 150

4) 指定 workspace NPZ
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless \\
     --workspace-npz ../rl_code/soarm100sim/rl/workspace_cache/workspace_tcp_merged_train.npz

5) 带 GUI 看 TCP/目标球（红=目标，绿=TCP；env 数宜减小）
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --num_envs 16

6) 关闭 debug marker / 动作滤波
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless \\
     --no-debug-vis --disable_action_filter

7) TensorBoard（训练时另开终端）
   tensorboard --logdir ~/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/checkpoints
   # 浏览器 http://localhost:6006
   # 关键标量：Metrics/success_rate, Metrics/orientation_success_rate,
   #           Metrics/ever_success_rate, Rewards/total_reward_mean

8) 训练后推理
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/execute.py \\
     --checkpoint ../rl_code/soarm100sim/rl/checkpoints/<run>/agent.pt

================================================================================
输出路径（默认）
================================================================================
  checkpoints/<YYYY-MM-DD_HH-MM-SS>/            # 新训
  checkpoints/<YYYY-MM-DD_HH-MM-SS>_resume/     # 续训（目录名带 _resume）
    RESUME.txt                                  # 续训元信息（resume_from 等）
    train_run_meta.txt                          # 运行配置摘要
    <skrl_run>/events.out.tfevents.*            # TensorBoard

================================================================================
默认设置摘要（完整项见下方 DEFAULTS；环境奖励见 reach_env_cfg*.py）
================================================================================
  TCP 对齐：捏合中心（sample/tcp_pose.py），目标姿态来自 NPZ tcp_quat_wxyz
  env-cfg=1：reach_env_cfg.ReachEnvCfg（稳定默认，orient_scale=2.0, orient_dist_th=0.03）
  env-cfg=2/ori：reach_env_cfg2.ReachEnvCfg2（姿态实验，orient_scale=5.0, orient_dist_th=0.08）
  num_envs=128, max_iterations=800, seed=42
  PPO：rollouts=128, lr=1e-4, epochs=5, mini_batches=4, network=[256,128,64]
  动作：7 关节增量，action_scale=0.25（reach_env_cfg），滤波 tau=0.08s（本脚本覆盖）
  回合：episode_length_s=10，decimation=2，sim_dt=1/60
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from isaaclab.app import AppLauncher

RL_ROOT = Path(__file__).resolve().parent

# =============================================================================
# 用户常改默认配置（CLI 可覆盖；奖励/阈值等见 reach_env_cfg.py / reach_env_cfg2.py）
# =============================================================================

DEFAULTS = {
    # --- 环境配置：1/default=稳定 ReachEnvCfg；2/ori=姿态实验 ReachEnvCfg2 ---
    "env_cfg": "1",
    # --- 训练规模 ---
    "num_envs": 256,
    "max_iterations": 2000,
    "seed": 42,
    # --- 数据与资产 ---
    "workspace_npz": "",  # 空则 workspace_cache/workspace_tcp_merged_train.npz
    "usd_path": str(RL_ROOT / "assets" / "so100_plus.usd"),
    "checkpoints_root": str(RL_ROOT / "checkpoints"),
    # --- 控制（写入 ReachEnvCfg；action_scale 等在 reach_env_cfg.py）---
    "disable_action_filter": False,
    "action_filter_tau": 0.08,
    "debug_vis": True,
    # --- PPO / skrl（改此处后 agent_cfg 同步生效）---
    "rollouts": 128,
    "learning_epochs": 5,
    "mini_batches": 4,
    "learning_rate": 1e-4,
    "discount_factor": 0.99,
    "lambda": 0.95,
    "ratio_clip": 0.2,
    "value_clip": 0.2,
    "grad_norm_clip": 1.0,
    "entropy_loss_scale": 0.0,
    "value_loss_scale": 2.0,
    "rewards_shaper_scale": 0.05,
    "policy_hidden_layers": (256, 128, 64),
    "value_hidden_layers": (256, 128, 64),
    "activation": "elu",
    # --- 续训 ---
    "checkpoint": None,
}

parser = argparse.ArgumentParser(description="SO-100 Plus 单臂 Reach PPO 训练")
parser.add_argument("--num_envs", type=int, default=DEFAULTS["num_envs"], help="并行环境数量")
parser.add_argument("--max_iterations", type=int, default=DEFAULTS["max_iterations"], help="训练迭代次数")
parser.add_argument("--checkpoint", type=str, default=DEFAULTS["checkpoint"], help="续训 checkpoint(.pt)")
parser.add_argument("--seed", type=int, default=DEFAULTS["seed"], help="随机种子（环境 + agent）")
parser.add_argument(
    "--disable_action_filter",
    action="store_true",
    default=DEFAULTS["disable_action_filter"],
    help="关闭动作一阶低通滤波",
)
parser.add_argument(
    "--action_filter_tau",
    type=float,
    default=DEFAULTS["action_filter_tau"],
    help="动作滤波时间常数 tau（秒）",
)
parser.add_argument(
    "--workspace-npz",
    type=str,
    default=DEFAULTS["workspace_npz"],
    help="训练用 workspace NPZ（默认 workspace_cache/workspace_tcp_merged_train.npz）",
)
parser.add_argument(
    "--no-debug-vis",
    action="store_true",
    help="关闭 TCP/目标 marker 可视化",
)
parser.add_argument(
    "--env-cfg",
    type=str,
    default=DEFAULTS["env_cfg"],
    choices=("1", "default", "2", "ori"),
    help="环境配置：1/default=reach_env_cfg（稳定）；2/ori=reach_env_cfg2（姿态实验）",
)
AppLauncher.add_app_launcher_args(parser)
args_cli, hydra_args = parser.parse_known_args()
sys.argv = [sys.argv[0]] + hydra_args

_train_npz = (args_cli.workspace_npz or "").strip() or str(RL_ROOT / "workspace_cache" / "workspace_tcp_merged_train.npz")
_usd_path = Path(DEFAULTS["usd_path"])
if not os.path.isfile(_train_npz):
    raise FileNotFoundError(
        f"训练用 workspace NPZ 不存在: {_train_npz}\n"
        "请先运行 rl/sample.py 完成采样与 train/test 划分。"
    )
if not _usd_path.is_file():
    raise FileNotFoundError(
        f"USD 不存在: {_usd_path}\n"
        "请先按 rl/sample.py 顶部说明将 URDF 转为 USD。"
    )

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

sys.path.insert(0, str(RL_ROOT))

from reach_env import ReachEnv
from reach_env_cfg import ReachEnvCfg
from reach_env_cfg2 import ReachEnvCfg2

from isaaclab_rl.skrl import SkrlVecEnvWrapper
from skrl.utils.runner.torch import Runner

_env_cfg_key = str(args_cli.env_cfg).strip().lower()
if _env_cfg_key in ("2", "ori"):
    _env_cfg_name = "ReachEnvCfg2"
    _env_cfg_module = "reach_env_cfg2"
    env_cfg = ReachEnvCfg2()
else:
    _env_cfg_name = "ReachEnvCfg"
    _env_cfg_module = "reach_env_cfg"
    env_cfg = ReachEnvCfg()
env_cfg.seed = args_cli.seed
env_cfg.scene.num_envs = args_cli.num_envs
env_cfg.enable_action_filter = not args_cli.disable_action_filter
env_cfg.action_filter_tau = args_cli.action_filter_tau
if (args_cli.workspace_npz or "").strip():
    env_cfg.workspace_npz_path = os.path.abspath(args_cli.workspace_npz)
elif (env_cfg.workspace_npz_path_train or "").strip():
    env_cfg.workspace_npz_path = os.path.abspath(env_cfg.workspace_npz_path_train)
if args_cli.no_debug_vis:
    env_cfg.debug_vis = False

reach_env = ReachEnv(env_cfg)
if env_cfg.debug_vis:
    if reach_env.set_debug_vis(True):
        print("[INFO] debug_vis: 红球=目标位置, 绿球=TCP（需 GUI，headless 不可见）")
    else:
        print("[WARN] debug_vis 未启用")
else:
    print("[INFO] debug_vis 已关闭 (--no-debug-vis)")
env = SkrlVecEnvWrapper(reach_env, ml_framework="torch")

_is_resume = bool((args_cli.checkpoint or "").strip())
_resume_ckpt = os.path.abspath(args_cli.checkpoint) if _is_resume else ""
if _is_resume and not os.path.isfile(_resume_ckpt):
    raise FileNotFoundError(f"续训 checkpoint 不存在: {_resume_ckpt}")

_run_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
_run_tag = f"{_run_stamp}_resume" if _is_resume else _run_stamp
log_dir = os.path.abspath(os.path.join(DEFAULTS["checkpoints_root"], _run_tag))
os.makedirs(log_dir, exist_ok=True)

_rollouts = int(DEFAULTS["rollouts"])
total_timesteps = args_cli.max_iterations * _rollouts

_policy_layers = list(DEFAULTS["policy_hidden_layers"])
_value_layers = list(DEFAULTS["value_hidden_layers"])
_activation = str(DEFAULTS["activation"])
# skrl 实验名带 resume，TensorBoard 看图时可一眼区分续训 run
_experiment_name = f"PPO_resume" if _is_resume else "PPO"

agent_cfg = {
    "seed": args_cli.seed,
    "models": {
        "separate": False,
        "policy": {
            "class": "GaussianMixin",
            "clip_actions": False,
            "clip_log_std": True,
            "min_log_std": -20.0,
            "max_log_std": 2.0,
            "initial_log_std": 0.0,
            "network": [
                {
                    "name": "net",
                    "input": "OBSERVATIONS",
                    "layers": _policy_layers,
                    "activations": _activation,
                }
            ],
            "output": "ACTIONS",
        },
        "value": {
            "class": "DeterministicMixin",
            "clip_actions": False,
            "network": [
                {
                    "name": "net",
                    "input": "OBSERVATIONS",
                    "layers": _value_layers,
                    "activations": _activation,
                }
            ],
            "output": "ONE",
        },
    },
    "memory": {"class": "RandomMemory", "memory_size": -1},
    "agent": {
        "class": "PPO",
        "rollouts": _rollouts,
        "learning_epochs": int(DEFAULTS["learning_epochs"]),
        "mini_batches": int(DEFAULTS["mini_batches"]),
        "discount_factor": float(DEFAULTS["discount_factor"]),
        "lambda": float(DEFAULTS["lambda"]),
        "learning_rate": float(DEFAULTS["learning_rate"]),
        "learning_rate_scheduler": "KLAdaptiveLR",
        "learning_rate_scheduler_kwargs": {"kl_threshold": 0.01},
        "state_preprocessor": "RunningStandardScaler",
        "state_preprocessor_kwargs": None,
        "value_preprocessor": "RunningStandardScaler",
        "value_preprocessor_kwargs": None,
        "random_timesteps": 0,
        "learning_starts": 0,
        "grad_norm_clip": float(DEFAULTS["grad_norm_clip"]),
        "ratio_clip": float(DEFAULTS["ratio_clip"]),
        "value_clip": float(DEFAULTS["value_clip"]),
        "clip_predicted_values": True,
        "entropy_loss_scale": float(DEFAULTS["entropy_loss_scale"]),
        "value_loss_scale": float(DEFAULTS["value_loss_scale"]),
        "rewards_shaper_scale": float(DEFAULTS["rewards_shaper_scale"]),
        "time_limit_bootstrap": True,
        "experiment": {
            "directory": log_dir,
            "experiment_name": _experiment_name,
            "write_interval": "auto",
            "checkpoint_interval": "auto",
        },
    },
    "trainer": {
        "class": "SequentialTrainer",
        "timesteps": total_timesteps,
        "environment_info": "log",
    },
}

_run_mode = "续训 (RESUME)" if _is_resume else "新训 (SCRATCH)"
_meta_lines = [
    f"mode={_run_mode}",
    f"is_resume={_is_resume}",
    f"wall_time={datetime.now().isoformat(timespec='seconds')}",
    f"log_dir={log_dir}",
    f"resume_from={_resume_ckpt if _is_resume else ''}",
    f"env_cfg_key={_env_cfg_key}",
    f"env_cfg_module={_env_cfg_module}",
    f"env_cfg_class={_env_cfg_name}",
    f"workspace_npz={env_cfg.workspace_npz_path}",
    f"seed={args_cli.seed}",
    f"num_envs={args_cli.num_envs}",
    f"max_iterations={args_cli.max_iterations}",
    f"rollouts={_rollouts}",
    f"total_timesteps={total_timesteps}",
    f"action_filter={env_cfg.enable_action_filter}",
    f"action_filter_tau={env_cfg.action_filter_tau}",
    f"rew_orientation_scale={env_cfg.rew_orientation_scale}",
    f"orientation_reward_distance_threshold={env_cfg.orientation_reward_distance_threshold}",
    f"rew_distance_scale={env_cfg.rew_distance_scale}",
    f"rew_success_scale={env_cfg.rew_success_scale}",
    f"two_level_reward_scale={env_cfg.two_level_reward_scale}",
]
_meta_text = "\n".join(_meta_lines) + "\n"
with open(os.path.join(log_dir, "train_run_meta.txt"), "w", encoding="utf-8") as handle:
    handle.write(_meta_text)
if _is_resume:
    _resume_text = (
        "本目录为续训 (RESUME)，非从零训练。\n"
        f"resume_from={_resume_ckpt}\n"
        f"wall_time={datetime.now().isoformat(timespec='seconds')}\n"
        f"max_iterations={args_cli.max_iterations}\n"
        f"env_cfg_key={_env_cfg_key}\n"
        f"env_cfg_class={_env_cfg_name}\n"
        f"rew_orientation_scale={env_cfg.rew_orientation_scale}\n"
        f"orientation_reward_distance_threshold={env_cfg.orientation_reward_distance_threshold}\n"
    )
    with open(os.path.join(log_dir, "RESUME.txt"), "w", encoding="utf-8") as handle:
        handle.write(_resume_text)
    with open(os.path.join(log_dir, "resume_meta.json"), "w", encoding="utf-8") as handle:
        json.dump(
            {
                "mode": "resume",
                "resume_from": _resume_ckpt,
                "log_dir": log_dir,
                "max_iterations": args_cli.max_iterations,
                "env_cfg_key": _env_cfg_key,
                "env_cfg_module": _env_cfg_module,
                "env_cfg_class": _env_cfg_name,
                "rew_orientation_scale": env_cfg.rew_orientation_scale,
                "orientation_reward_distance_threshold": env_cfg.orientation_reward_distance_threshold,
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )

print("=" * 72, flush=True)
print(f"[TRAIN] mode={_run_mode}", flush=True)
if _is_resume:
    print(f"[TRAIN] resume_from={_resume_ckpt}", flush=True)
    print(f"[TRAIN] 续训日志: {os.path.join(log_dir, 'RESUME.txt')}", flush=True)
print(f"[TRAIN] log_dir={log_dir}", flush=True)
print(f"[TRAIN] env_cfg={_env_cfg_key} ({_env_cfg_module}.{_env_cfg_name})", flush=True)
print("=" * 72, flush=True)
print(f"[INFO] TensorBoard: python -m tensorboard.main --logdir {DEFAULTS['checkpoints_root']} --port 6006")
print(f"[INFO] workspace NPZ: {env_cfg.workspace_npz_path}")
print(
    f"[INFO] seed={args_cli.seed} | num_envs={args_cli.num_envs} | "
    f"iter={args_cli.max_iterations} | rollouts={_rollouts} | "
    f"obs={env_cfg.observation_space} act={env_cfg.action_space} | "
    f"action_filter={env_cfg.enable_action_filter} tau={env_cfg.action_filter_tau:.3f}s"
)
print(
    f"[INFO] reward: orient_scale={env_cfg.rew_orientation_scale} "
    f"orient_dist_th={env_cfg.orientation_reward_distance_threshold} "
    f"dist_scale={env_cfg.rew_distance_scale} success_scale={env_cfg.rew_success_scale}"
)

runner = Runner(env, agent_cfg)
if _is_resume:
    runner.agent.load(_resume_ckpt)
    print(f"[TRAIN][RESUME] 已加载权重: {_resume_ckpt}", flush=True)
    print(f"[TRAIN][RESUME] 本 run TensorBoard 落在: {log_dir}", flush=True)

runner.run()

if _is_resume:
    print("=" * 72, flush=True)
    print(f"[TRAIN][RESUME] 续训结束。checkpoint / TB 在: {log_dir}", flush=True)
    print(f"[TRAIN][RESUME] resume_from={_resume_ckpt}", flush=True)
    print("=" * 72, flush=True)

env.close()
simulation_app.close()
