"""SO-100 Plus 单臂 6D Reach 环境配置。"""

from __future__ import annotations

import sys
from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg
from isaaclab.envs import DirectRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.utils import configclass

_RL_ROOT = Path(__file__).resolve().parent
if str(_RL_ROOT) not in sys.path:
    sys.path.insert(0, str(_RL_ROOT))

from sample.constants import GRIPPER_BODY_NAME, REACH_JOINT_NAMES, WRIST_ROLL_BODY_NAME
from sample.robot_cfg import build_so100_plus_cfg, default_usd_path


def _rl_path(*parts: str) -> str:
    return str(_RL_ROOT.joinpath(*parts))


@configclass
class ReachEnvCfg(DirectRLEnvCfg):
    """SO-100 Plus 单臂 Reach：从 workspace NPZ 采样 6D 目标，PPO 控制 7 关节。"""

    seed: int = 42
    decimation: int = 2
    episode_length_s: float = 10.0

    # obs: joint_pos(7) + joint_vel(7) + tcp_rel(3) + target_rel(3) + pos_err(3) + quat_err(4) = 27
    action_space: int = len(REACH_JOINT_NAMES)
    observation_space: int = 27
    state_space: int = 0

    sim: SimulationCfg = SimulationCfg(dt=1.0 / 60.0, render_interval=decimation)

    scene: InteractiveSceneCfg = InteractiveSceneCfg(
        num_envs=256,
        env_spacing=1.5,
        replicate_physics=True,
    )

    robot_cfg: ArticulationCfg = build_so100_plus_cfg(default_usd_path()).replace(
        prim_path="/World/envs/env_.*/Robot"
    )

    # --- 机器人 / TCP（捏合中心，见 sample/tcp_pose.py）---
    arm_joint_names: tuple[str, ...] = REACH_JOINT_NAMES
    wrist_roll_body_name: str = WRIST_ROLL_BODY_NAME
    gripper_body_name: str = GRIPPER_BODY_NAME
    ee_forward_local: tuple[float, float, float] = (0.0, 0.0, 1.0)

    # --- 目标数据集 ---
    workspace_npz_path: str = ""
    workspace_npz_path_train: str = _rl_path("workspace_cache", "workspace_tcp_merged_train.npz")
    workspace_npz_path_test: str = _rl_path("workspace_cache", "workspace_tcp_merged_test.npz")

    # --- 控制 ---
    action_scale: float = 0.25
    reset_joint_noise_rad: float = 0.0
    enable_action_filter: bool = True
    action_filter_tau: float = 0.15

    # --- 姿态目标 ---
    orientation_desired_reference: str = "dataset"  # fixed | episode_initial | usd_default | dataset
    orientation_align_mode: str = "full_quaternion"
    fixed_ee_quat_wxyz: tuple[float, float, float, float] = (1.0, 0.0, 0.0, 0.0)
    enable_orientation_constraint: bool = True

    # --- 接触 ---
    enable_contact_sensors: bool = True
    contact_prim_path_expr: str = "/World/envs/env_.*/Robot/.*"
    contact_threshold: float = 1.5
    contact_force_clip: float = 3.0

    # --- 奖励 ---
    rew_distance_scale: float = 2.0
    rew_success_scale: float = 3.0
    rew_action_rate_scale: float = -0.003
    rew_joint_vel_scale: float = -0.005
    rew_contact_scale: float = -0.3
    # stable baseline（续训/正式默认）：姿态引导权重不宜大于 rew_success_scale
    rew_orientation_scale: float = 2.0
    orientation_reward_ramp_outer_distance: float = 0.2
    orientation_enter_dot_threshold: float = 0.9962
    orientation_exit_dot_threshold: float = 0.994
    orientation_reward_distance_threshold: float = 0.03
    orientation_success_enter_distance: float = 0.05
    orientation_success_exit_distance: float = 0.055
    hold_reward_per_sec: float = 10.0
    success_still_speed_threshold: float = 0.025
    success_exit_threshold: float = 0.013
    one_level_reward_scale: float = 1.0
    two_level_reward_scale: float = 45.0
    one_level_threshold: float = 0.1
    two_level_threshold: float = 0.05
    success_threshold: float = 0.01

    # --- 调试可视化 ---
    debug_vis: bool = True
    debug_show_target_marker: bool = True
    debug_vis_tcp_marker_radius: float = 0.012
    debug_vis_target_marker_radius: float = 0.018
