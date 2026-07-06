"""MuJoCo Reach 推理常量（与 Isaac ReachEnvCfg / train 默认对齐）。"""

from __future__ import annotations

from pathlib import Path

MUJOCO_DIR = Path(__file__).resolve().parent
REPO_ROOT = MUJOCO_DIR.parent
RL_ROOT = REPO_ROOT / "rl"

# 机器人 MJCF（资产仍在 SO-ARM100 目录，避免复制 mesh）
DEFAULT_MJCF = (
    REPO_ROOT
    / "SO-ARM100"
    / "Simulation"
    / "SO100"
    / "mujoco"
    / "scene_plus.xml"
)

# C：2026-07-06 bank-start 重训 best（主用）
DEFAULT_CHECKPOINT = (
    RL_ROOT
    / "checkpoints"
    / "2026-07-06_14-44-29"
    / "PPO"
    / "checkpoints"
    / "best_agent.pt"
)

DEFAULT_NPZ_TEST = RL_ROOT / "workspace_cache" / "workspace_tcp_merged_test.npz"
DEFAULT_NPZ_TRAIN = RL_ROOT / "workspace_cache" / "workspace_tcp_merged_train.npz"

REACH_JOINT_NAMES: tuple[str, ...] = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)

BASE_BODY = "base"
WRIST_ROLL_BODY = "wrist_roll"
GRIPPER_BODY = "gripper"

OBS_DIM = 27
ACTION_DIM = 7

SIM_DT = 1.0 / 60.0
DECIMATION = 2
ACTION_SCALE = 0.25
ACTION_FILTER_TAU = 0.08  # 与 train.py 默认一致
EPISODE_LENGTH_S = 10.0

HOME_QPOS = (0.0, -1.57079, 1.57079, 0.0, 0.0, 0.0, 0.0)
