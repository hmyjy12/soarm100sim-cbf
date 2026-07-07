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

DEFAULT_MJCF_NOROD = (
    REPO_ROOT
    / "SO-ARM100"
    / "Simulation"
    / "SO100"
    / "mujoco"
    / "scene_plus_norod.xml"
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

# CBF（EMBODISTEER 式 QP，默认与 play --enable-cbf 一致）
CBF_D_SAFE = 0.02
CBF_GAMMA = 0.8
CBF_LAMBDA = 0.5
CBF_ACTIVATE_MARGIN = 0.04
CBF_FILTER_TAU = 0.06

HOME_QPOS = (0.0, -1.57079, 1.57079, 0.0, 0.0, 0.0, 0.0)

# 可碰倒细杆（scene_plus.xml）：铰点与直立几何中心
OBSTACLE_ROD_JOINT = "obstacle_rod_joint"
OBSTACLE_ROD_GEOM = "obstacle_rod"
OBSTACLE_ROD_MOUNT_POS_M = (0.15, 0.09, 0.02)
OBSTACLE_ROD_CENTER_POS_M = (0.15, 0.09, 0.17)

# 双相机（sim2real 视觉链路；见 mujoco/camera.py / vision_smoke.py）
SCENE_DEPTH_CAM = "scene_depth"
WRIST_RGB_CAM = "wrist_rgb"
SCENE_CAM_LOOKAT_BODY = "scene_cam_lookat"
SCENE_DEPTH_CAM_MOUNT_POS_M = (0.05, -0.15, 0.50)
SCENE_CAM_LOOKAT_POS_M = (0.20, 0.05, 0.18)
# 腕部 RGB：与定爪指尖 wrist_roll 局部对齐（= TCP_FIXED_FINGER_TIP + z 外壳抬高）
WRIST_RGB_CAM_PARENT = "wrist_roll"
WRIST_RGB_CAM_POS_LOCAL_WRIST_ROLL = (0.0, -0.031, 0.036)
WRIST_RGB_CAM_QUAT_LOCAL_WRIST_ROLL = (0.0, 0.0, 0.9809, 0.1946)
# home 位 gripper 局部近似（定爪指尖同高）：(-0.0204, 0.0052, -0.0322)
WRIST_RGB_CAM_POS_GRIPPER_HINT = (-0.0204, 0.0052, -0.0322)
CAM_WIDTH = 640
CAM_HEIGHT = 480
CAM_FOVY_SCENE = 60.0
CAM_FOVY_WRIST = 55.0
