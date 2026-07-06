"""SO-100 Plus 单臂 6D Reach 环境（Isaac Lab DirectRLEnv）。"""

from __future__ import annotations

import os
from collections.abc import Sequence

import numpy as np
import torch

import isaaclab.sim as sim_utils
from isaaclab.assets import Articulation
from isaaclab.envs import DirectRLEnv
from isaaclab.markers import VisualizationMarkers
from isaaclab.markers.config import SPHERE_MARKER_CFG
from isaaclab.sensors import ContactSensor, ContactSensorCfg
from isaaclab.utils.math import sample_uniform

from reach_env_cfg import ReachEnvCfg
from sample.tcp_pose import compute_pinch_tcp_pose_torch


class ReachEnv(DirectRLEnv):
    """单臂 Reach：从 workspace NPZ bank 采样起点/目标（可强制最小 TCP 距离）。"""

    cfg: ReachEnvCfg

    def __init__(self, cfg: ReachEnvCfg, render_mode: str | None = None, **kwargs):
        ref = cfg.orientation_desired_reference
        if ref not in ("fixed", "episode_initial", "usd_default", "dataset"):
            raise ValueError(f"无效的 orientation_desired_reference: {ref!r}")
        mode = cfg.orientation_align_mode
        if mode not in ("forward_axis", "full_quaternion"):
            raise ValueError(f"无效的 orientation_align_mode: {mode!r}")

        npz_path = (cfg.workspace_npz_path or "").strip()
        if not npz_path:
            npz_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "workspace_cache",
                "workspace_tcp_merged.npz",
            )
        if not os.path.isfile(npz_path):
            raise FileNotFoundError(
                f"未找到 workspace NPZ: {npz_path}\n"
                "请先运行 rl/sample.py 生成 workspace_cache/workspace_tcp_merged_train.npz"
            )

        with np.load(npz_path) as data:
            if "tcp" in data.files:
                merged = np.asarray(data["tcp"], dtype=np.float64)
            elif "tcp_pos" in data.files:
                merged = np.asarray(data["tcp_pos"], dtype=np.float64)
            else:
                raise KeyError(f"{npz_path} 需要键 'tcp' 或 'tcp_pos'")
            quat_bank = None
            if "tcp_quat_wxyz" in data.files:
                quat_bank = np.asarray(data["tcp_quat_wxyz"], dtype=np.float64)
            joint_bank = None
            if "joint_pos" in data.files:
                joint_bank = np.asarray(data["joint_pos"], dtype=np.float64)

        if merged.ndim != 2 or merged.shape[1] != 3 or merged.shape[0] == 0:
            raise ValueError(f"NPZ 位置数组形状应为 (N,3)，实际: {merged.shape}")
        if ref == "dataset" and quat_bank is None:
            raise KeyError(f"orientation_desired_reference='dataset' 需要 NPZ 含 tcp_quat_wxyz: {npz_path}")
        if cfg.reset_start_from_bank:
            if joint_bank is None:
                raise KeyError(
                    f"reset_start_from_bank=True 需要 NPZ 含 joint_pos: {npz_path}"
                )
            n_arm = len(cfg.arm_joint_names)
            if joint_bank.ndim != 2 or joint_bank.shape[0] != merged.shape[0] or joint_bank.shape[1] != n_arm:
                raise ValueError(
                    f"NPZ joint_pos 形状应为 (N,{n_arm}) 且 N 与 tcp 一致，实际: {joint_bank.shape}"
                )

        self._workspace_npz_path = npz_path
        self._tcp_target_bank_np = merged
        self._tcp_target_quat_bank_np = quat_bank
        self._joint_pos_bank_np = joint_bank

        super().__init__(cfg, render_mode, **kwargs)

        self._arm_joint_ids, _ = self.robot.find_joints(list(cfg.arm_joint_names))
        wr_ids, _ = self.robot.find_bodies(cfg.wrist_roll_body_name)
        gr_ids, _ = self.robot.find_bodies(cfg.gripper_body_name)
        if len(wr_ids) == 0:
            raise RuntimeError(f"未找到 wrist_roll body: {cfg.wrist_roll_body_name!r}")
        if len(gr_ids) == 0:
            raise RuntimeError(f"未找到 gripper body: {cfg.gripper_body_name!r}")
        self._wrist_roll_body_idx = int(wr_ids[0])
        self._gripper_body_idx = int(gr_ids[0])

        self._tcp_target_bank = torch.as_tensor(self._tcp_target_bank_np, device=self.device, dtype=torch.float32)
        self._tcp_target_quat_bank = None
        if self._tcp_target_quat_bank_np is not None:
            quat_t = torch.as_tensor(self._tcp_target_quat_bank_np, device=self.device, dtype=torch.float32)
            self._tcp_target_quat_bank = quat_t / torch.norm(quat_t, dim=-1, keepdim=True).clamp_min(1e-8)
        self._joint_pos_bank = None
        if self._joint_pos_bank_np is not None:
            self._joint_pos_bank = torch.as_tensor(self._joint_pos_bank_np, device=self.device, dtype=torch.float32)

        self._target_pos_w = torch.zeros(self.num_envs, 3, device=self.device)
        self._target_quat_w = torch.zeros(self.num_envs, 4, device=self.device)
        self._target_quat_w[:, 0] = 1.0
        self._episode_ref_ee_quat_w = torch.zeros(self.num_envs, 4, device=self.device)
        self._episode_ref_ee_quat_w[:, 0] = 1.0
        self._usd_ref_quat_w = torch.zeros(self.num_envs, 4, device=self.device)
        self._usd_ref_quat_w[:, 0] = 1.0

        n_act = int(cfg.action_space)
        self._raw_actions = torch.zeros(self.num_envs, n_act, device=self.device)
        self._filtered_actions = torch.zeros(self.num_envs, n_act, device=self.device)
        self._prev_actions = torch.zeros(self.num_envs, n_act, device=self.device)
        self._prev_distance = torch.zeros(self.num_envs, device=self.device)
        self._prev_tcp_pos_w = torch.zeros(self.num_envs, 3, device=self.device)

        self._in_target_success_region = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self._in_orientation_success_region = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self._in_success_region = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self._ever_target_success = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self._ever_orientation_success = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self._ever_success = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self._last_target_success_rate = torch.tensor(0.0, device=self.device)
        self._last_orientation_success_rate = torch.tensor(0.0, device=self.device)
        self._last_success_rate = torch.tensor(0.0, device=self.device)
        self._last_ever_target_success_rate = torch.tensor(0.0, device=self.device)
        self._last_ever_orientation_success_rate = torch.tensor(0.0, device=self.device)
        self._last_ever_success_rate = torch.tensor(0.0, device=self.device)

        # episode 误差跟踪（reset 前快照，供离线评测）
        self._ep_min_pos_err = torch.full((self.num_envs,), float("inf"), device=self.device)
        self._ep_min_ori_deg = torch.full((self.num_envs,), float("inf"), device=self.device)
        self._last_done_pos_err = torch.zeros(0, device=self.device)
        self._last_done_ori_deg = torch.zeros(0, device=self.device)
        self._last_done_min_pos_err = torch.zeros(0, device=self.device)
        self._last_done_min_ori_deg = torch.zeros(0, device=self.device)
        self._last_done_mask = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)

        if cfg.debug_vis:
            self.set_debug_vis(True)

    def _setup_scene(self):
        self.robot = Articulation(self.cfg.robot_cfg)
        self.contact_sensor = None

        sim_utils.GroundPlaneCfg().func("/World/GroundPlane", sim_utils.GroundPlaneCfg())
        light_cfg = sim_utils.DomeLightCfg(intensity=2500.0, color=(0.85, 0.85, 0.85))
        light_cfg.func("/World/DomeLight", light_cfg)

        if self.cfg.enable_contact_sensors:
            self.contact_sensor = ContactSensor(
                ContactSensorCfg(
                    prim_path=self.cfg.contact_prim_path_expr,
                    history_length=3,
                    update_period=0.0,
                    track_air_time=False,
                )
            )
            self.scene.sensors["contact_sensor"] = self.contact_sensor

        self.scene.clone_environments(copy_from_source=False)
        if self.device == "cpu":
            self.scene.filter_collisions(global_prim_paths=[])
        self.scene.articulations["robot"] = self.robot

    def _pre_physics_step(self, actions: torch.Tensor) -> None:
        raw = actions.clone().clamp(-1.0, 1.0)
        self._raw_actions = raw
        if self.cfg.enable_action_filter:
            dt_ctrl = self.cfg.sim.dt * self.cfg.decimation
            tau = max(float(self.cfg.action_filter_tau), 1e-6)
            beta = float(dt_ctrl / (tau + dt_ctrl))
            self._filtered_actions += beta * (raw - self._filtered_actions)
            self._actions = self._filtered_actions
        else:
            self._actions = raw

    def _apply_action(self) -> None:
        curr = self.robot.data.joint_pos[:, self._arm_joint_ids]
        lim = self.robot.data.soft_joint_pos_limits[:, self._arm_joint_ids]
        tgt = curr + self.cfg.action_scale * self._actions
        tgt = torch.clamp(tgt, lim[..., 0], lim[..., 1])
        self.robot.set_joint_position_target(tgt, joint_ids=self._arm_joint_ids)

    def _get_observations(self) -> dict:
        joint_pos = self.robot.data.joint_pos[:, self._arm_joint_ids]
        joint_vel = self.robot.data.joint_vel[:, self._arm_joint_ids]
        root_pos_w = self.robot.data.root_pos_w[:, :3]
        tcp_w, ee_quat_w = self._tcp_pose_w()
        tcp_rel = tcp_w - root_pos_w
        target_rel = self._target_pos_w - root_pos_w
        pos_err = self._target_pos_w - tcp_w

        desired_quat = self._get_desired_quat_w(ee_quat_w)
        ee_u = ee_quat_w / torch.norm(ee_quat_w, dim=-1, keepdim=True).clamp_min(1e-8)
        dq_u = desired_quat / torch.norm(desired_quat, dim=-1, keepdim=True).clamp_min(1e-8)
        quat_err = self._quat_multiply(dq_u, self._quat_conjugate(ee_u))
        quat_err = quat_err / torch.norm(quat_err, dim=-1, keepdim=True).clamp_min(1e-8)
        quat_err = torch.where(quat_err[:, :1] < 0.0, -quat_err, quat_err)

        obs = torch.cat([joint_pos, joint_vel, tcp_rel, target_rel, pos_err, quat_err], dim=-1)
        return {"policy": obs}

    def _get_rewards(self) -> torch.Tensor:
        tcp_w, ee_quat_w = self._tcp_pose_w()
        cur_distance = torch.norm(tcp_w - self._target_pos_w, dim=-1)
        dt = self.cfg.sim.dt * self.cfg.decimation
        tcp_speed = torch.norm(tcp_w - self._prev_tcp_pos_w, dim=-1) / max(dt, 1e-6)

        enter_tgt = cur_distance < self.cfg.success_threshold
        stay_tgt = self._in_target_success_region & (cur_distance < self.cfg.success_exit_threshold)
        self._in_target_success_region = enter_tgt | stay_tgt
        self._ever_target_success |= self._in_target_success_region

        if self.cfg.enable_orientation_constraint:
            desired_quat = self._get_desired_quat_w(ee_quat_w)
            ee_u = ee_quat_w / torch.norm(ee_quat_w, dim=-1, keepdim=True).clamp_min(1e-8)
            dq_u = desired_quat / torch.norm(desired_quat, dim=-1, keepdim=True).clamp_min(1e-8)
            align_quat = (ee_u * dq_u).sum(dim=-1).abs().clamp(0.0, 1.0)
            if self.cfg.orientation_align_mode == "full_quaternion":
                align_metric = align_quat
            else:
                align_metric = torch.sum(self._ee_forward_w(ee_quat_w) * self._ee_forward_w(desired_quat), dim=-1).clamp(
                    -1.0, 1.0
                )
            orient_enter_ok = align_metric >= float(self.cfg.orientation_enter_dot_threshold)
            orient_stay_ok = align_metric >= float(self.cfg.orientation_exit_dot_threshold)
            d_in = float(self.cfg.orientation_success_enter_distance)
            d_out = float(self.cfg.orientation_success_exit_distance)
            enter_ori = (cur_distance < d_in) & orient_enter_ok
            stay_ori = self._in_orientation_success_region & (cur_distance < d_out) & orient_stay_ok
            self._in_orientation_success_region = enter_ori | stay_ori
        else:
            align_quat = torch.ones_like(cur_distance)
            self._in_orientation_success_region = torch.ones_like(self._in_orientation_success_region)

        self._ever_orientation_success |= self._in_orientation_success_region
        self._in_success_region = self._in_target_success_region & self._in_orientation_success_region
        self._ever_success |= self._in_success_region

        rew_dist = self.cfg.rew_distance_scale * (self._prev_distance - cur_distance)
        rew_level1 = self.cfg.one_level_reward_scale * (cur_distance < self.cfg.one_level_threshold).float()
        rew_level2 = self.cfg.two_level_reward_scale * (self.cfg.two_level_threshold - cur_distance).clamp(min=0.0)
        rew_success_bonus = self.cfg.rew_success_scale * self._in_success_region.float()
        rew_success = rew_level1 + rew_level2 + rew_success_bonus
        is_still = tcp_speed < self.cfg.success_still_speed_threshold
        rew_hold = self._in_success_region.float() * is_still.float() * self.cfg.hold_reward_per_sec * dt

        da = self._actions - self._prev_actions
        rew_action_rate = self.cfg.rew_action_rate_scale * torch.sum(torch.square(da), dim=-1)
        active_vel = self.robot.data.joint_vel[:, self._arm_joint_ids]
        rew_joint_vel = self.cfg.rew_joint_vel_scale * torch.sum(torch.square(active_vel), dim=-1)

        if self.contact_sensor is not None:
            force_links = torch.norm(self.contact_sensor.data.net_forces_w, dim=-1)
            contact_excess = (force_links - float(self.cfg.contact_threshold)).clamp(
                min=0.0, max=float(self.cfg.contact_force_clip)
            )
            rew_contact = self.cfg.rew_contact_scale * contact_excess.sum(dim=-1)
        else:
            rew_contact = torch.zeros(self.num_envs, device=self.device)

        if self.cfg.enable_orientation_constraint:
            d_in = float(self.cfg.orientation_reward_distance_threshold)
            d_out = float(self.cfg.orientation_reward_ramp_outer_distance)
            if d_out > d_in + 1e-6:
                orient_w = ((d_out - cur_distance) / (d_out - d_in)).clamp(0.0, 1.0)
            else:
                orient_w = (cur_distance < d_in).float()
            orient_active = (~self._in_success_region).float()
            rew_orientation = self.cfg.rew_orientation_scale * torch.square(align_quat) * orient_w * orient_active
        else:
            rew_orientation = torch.zeros_like(cur_distance)

        self._prev_actions = self._actions.clone()
        self._prev_distance = cur_distance.clone()
        self._prev_tcp_pos_w = tcp_w.clone()

        # 回合内最优误差（供评测：reset 前仍可读）
        ori_deg = (2.0 * torch.acos(align_quat.clamp(0.0, 1.0))) * (180.0 / 3.141592653589793)
        self._ep_min_pos_err = torch.minimum(self._ep_min_pos_err, cur_distance)
        self._ep_min_ori_deg = torch.minimum(self._ep_min_ori_deg, ori_deg)

        total = rew_dist + rew_success + rew_hold + rew_action_rate + rew_joint_vel + rew_contact + rew_orientation
        self.extras["log"] = {
            # 回合结束时统计（episode 完结瞬间的成功率，skrl 每轮 rollout 聚合）
            "Metrics/target_success_rate": self._last_target_success_rate,
            "Metrics/orientation_success_rate": self._last_orientation_success_rate,
            "Metrics/success_rate": self._last_success_rate,
            "Metrics/ever_target_success_rate": self._last_ever_target_success_rate,
            "Metrics/ever_orientation_success_rate": self._last_ever_orientation_success_rate,
            "Metrics/ever_success_rate": self._last_ever_success_rate,
            # 当前步瞬时成功率（是否在成功区内）
            "Metrics/in_target_success_region_rate": self._in_target_success_region.float().mean(),
            "Metrics/in_orientation_success_region_rate": self._in_orientation_success_region.float().mean(),
            "Metrics/in_success_region_rate": self._in_success_region.float().mean(),
            "Metrics/tcp_distance_mean": cur_distance.mean(),
            "Metrics/tcp_speed_mean": tcp_speed.mean(),
            "Rewards/rew_dist_mean": rew_dist.mean(),
            "Rewards/rew_success_mean": rew_success.mean(),
            "Rewards/rew_hold_mean": rew_hold.mean(),
            "Rewards/rew_action_rate_mean": rew_action_rate.mean(),
            "Rewards/rew_joint_vel_mean": rew_joint_vel.mean(),
            "Rewards/rew_contact_mean": rew_contact.mean(),
            "Rewards/rew_orientation_mean": rew_orientation.mean(),
            "Rewards/total_reward_mean": total.mean(),
        }
        return total

    def _get_dones(self) -> tuple[torch.Tensor, torch.Tensor]:
        time_out = self.episode_length_buf >= self.max_episode_length - 1
        terminated = torch.zeros_like(time_out)
        done = terminated | time_out
        self._last_done_mask = done
        if torch.any(done):
            # reset 之前快照：step() 返回后状态可能已恢复到 home
            tcp_w, ee_q = self._tcp_pose_w()
            des_q = self._get_desired_quat_w(ee_q)
            pos_err = torch.norm(tcp_w - self._target_pos_w, dim=-1)
            ee_u = ee_q / torch.norm(ee_q, dim=-1, keepdim=True).clamp_min(1e-8)
            dq_u = des_q / torch.norm(des_q, dim=-1, keepdim=True).clamp_min(1e-8)
            align = (ee_u * dq_u).sum(dim=-1).abs().clamp(0.0, 1.0)
            ori_deg = (2.0 * torch.acos(align)) * (180.0 / 3.141592653589793)
            self._last_done_pos_err = pos_err[done].detach().clone()
            self._last_done_ori_deg = ori_deg[done].detach().clone()
            self._last_done_min_pos_err = self._ep_min_pos_err[done].detach().clone()
            self._last_done_min_ori_deg = self._ep_min_ori_deg[done].detach().clone()

            self._last_target_success_rate = self._in_target_success_region[done].float().mean()
            self._last_orientation_success_rate = self._in_orientation_success_region[done].float().mean()
            self._last_success_rate = self._in_success_region[done].float().mean()
            self._last_ever_target_success_rate = self._ever_target_success[done].float().mean()
            self._last_ever_orientation_success_rate = self._ever_orientation_success[done].float().mean()
            self._last_ever_success_rate = self._ever_success[done].float().mean()
        else:
            self._last_done_pos_err = torch.zeros(0, device=self.device)
            self._last_done_ori_deg = torch.zeros(0, device=self.device)
            self._last_done_min_pos_err = torch.zeros(0, device=self.device)
            self._last_done_min_ori_deg = torch.zeros(0, device=self.device)
        return terminated, time_out

    def _sample_start_target_bank_indices(self, n: int) -> tuple[torch.Tensor, torch.Tensor]:
        """从 bank 抽起点/目标索引；强制不同索引且 TCP 距离 >= 配置阈值。"""
        n_bank = int(self._tcp_target_bank.shape[0])
        if n_bank < 2:
            raise RuntimeError(f"workspace bank 至少需要 2 条样本，当前: {n_bank}")

        min_dist = float(self.cfg.reset_start_target_min_tcp_dist_m)
        start_idx = torch.randint(0, n_bank, (n,), device=self.device)
        start_tcp = self._tcp_target_bank[start_idx]
        target_idx = torch.randint(0, n_bank, (n,), device=self.device)
        best_dist = torch.norm(self._tcp_target_bank[target_idx] - start_tcp, dim=-1)

        for _ in range(32):
            ok = (best_dist >= min_dist) & (target_idx != start_idx)
            if bool(torch.all(ok)):
                break
            cand = torch.randint(0, n_bank, (n,), device=self.device)
            cand_dist = torch.norm(self._tcp_target_bank[cand] - start_tcp, dim=-1)
            # 未达标的 env：接受更远候选；已达标则保持
            take = (~ok) & (cand_dist > best_dist)
            target_idx = torch.where(take, cand, target_idx)
            best_dist = torch.where(take, cand_dist, best_dist)

        same = target_idx == start_idx
        if torch.any(same):
            target_idx = torch.where(same, (start_idx + 1) % n_bank, target_idx)
        return start_idx, target_idx

    def _reset_idx(self, env_ids: Sequence[int] | None):
        if env_ids is None:
            env_ids = self.robot._ALL_INDICES
        elif not torch.is_tensor(env_ids):
            env_ids = torch.as_tensor(env_ids, device=self.device, dtype=torch.long)
        super()._reset_idx(env_ids)

        n = len(env_ids)
        joint_pos = self.robot.data.default_joint_pos[env_ids].clone()
        joint_vel = torch.zeros_like(joint_pos)

        n_bank = int(self._tcp_target_bank.shape[0])
        if self.cfg.reset_start_from_bank:
            start_idx, target_idx = self._sample_start_target_bank_indices(n)
            joint_pos[:, self._arm_joint_ids] = self._joint_pos_bank[start_idx]
        else:
            target_idx = torch.randint(0, n_bank, (n,), device=self.device)

        mag = float(self.cfg.reset_joint_noise_rad)
        if mag > 0.0:
            noise = sample_uniform(-mag, mag, (n, len(self._arm_joint_ids)), device=self.device)
            joint_pos[:, self._arm_joint_ids] += noise

        target_rel = self._tcp_target_bank[target_idx]
        if self._tcp_target_quat_bank is not None:
            self._target_quat_w[env_ids] = self._tcp_target_quat_bank[target_idx]
        else:
            self._target_quat_w[env_ids] = 0.0
            self._target_quat_w[env_ids, 0] = 1.0

        root_state = self.robot.data.default_root_state[env_ids].clone()
        root_state[:, :3] += self.scene.env_origins[env_ids]
        self.robot.write_root_pose_to_sim(root_state[:, :7], env_ids)
        self.robot.write_root_velocity_to_sim(root_state[:, 7:], env_ids)

        if self.cfg.orientation_desired_reference == "usd_default":
            self.robot.write_joint_state_to_sim(joint_pos, joint_vel, None, env_ids)
            _, ref_q = self._tcp_pose_w()
            self._usd_ref_quat_w[env_ids] = ref_q[env_ids] / torch.norm(ref_q[env_ids], dim=-1, keepdim=True).clamp_min(1e-8)

        self.robot.write_joint_state_to_sim(joint_pos, joint_vel, None, env_ids)
        self.robot.set_joint_position_target(joint_pos[:, self._arm_joint_ids], joint_ids=self._arm_joint_ids, env_ids=env_ids)

        self._target_pos_w[env_ids] = target_rel + root_state[:, :3]

        self._raw_actions[env_ids] = 0.0
        self._filtered_actions[env_ids] = 0.0
        self._prev_actions[env_ids] = 0.0

        tcp_w, ee_q = self._tcp_pose_w()
        self._prev_distance[env_ids] = torch.norm(tcp_w[env_ids] - self._target_pos_w[env_ids], dim=-1)
        self._prev_tcp_pos_w[env_ids] = tcp_w[env_ids]
        self._episode_ref_ee_quat_w[env_ids] = ee_q[env_ids] / torch.norm(ee_q[env_ids], dim=-1, keepdim=True).clamp_min(1e-8)

        self._in_target_success_region[env_ids] = False
        self._in_orientation_success_region[env_ids] = not self.cfg.enable_orientation_constraint
        self._in_success_region[env_ids] = False
        self._ever_target_success[env_ids] = False
        self._ever_orientation_success[env_ids] = not self.cfg.enable_orientation_constraint
        self._ever_success[env_ids] = False
        self._ep_min_pos_err[env_ids] = float("inf")
        self._ep_min_ori_deg[env_ids] = float("inf")

        if self.cfg.debug_vis:
            self._ensure_debug_markers()
            self._update_debug_markers()

    def _tcp_pose_w(self) -> tuple[torch.Tensor, torch.Tensor]:
        wr_pos = self.robot.data.body_pos_w[:, self._wrist_roll_body_idx, :]
        wr_quat = self.robot.data.body_quat_w[:, self._wrist_roll_body_idx, :]
        gr_pos = self.robot.data.body_pos_w[:, self._gripper_body_idx, :]
        gr_quat = self.robot.data.body_quat_w[:, self._gripper_body_idx, :]
        return compute_pinch_tcp_pose_torch(wr_pos, wr_quat, gr_pos, gr_quat)

    def _get_desired_quat_w(self, ee_quat_w: torch.Tensor) -> torch.Tensor:
        ref = self.cfg.orientation_desired_reference
        if ref == "episode_initial":
            return self._episode_ref_ee_quat_w.to(dtype=ee_quat_w.dtype)
        if ref == "usd_default":
            return self._usd_ref_quat_w.to(dtype=ee_quat_w.dtype)
        if ref == "dataset":
            return self._target_quat_w.to(dtype=ee_quat_w.dtype)
        fixed = torch.tensor(self.cfg.fixed_ee_quat_wxyz, device=self.device, dtype=ee_quat_w.dtype)
        return fixed.unsqueeze(0).expand(ee_quat_w.shape[0], -1)

    def _ee_forward_w(self, ee_quat_w: torch.Tensor) -> torch.Tensor:
        forward_local = torch.tensor(self.cfg.ee_forward_local, device=self.device, dtype=ee_quat_w.dtype)
        forward_local = forward_local.unsqueeze(0).expand(ee_quat_w.shape[0], -1)
        forward_w = self._quat_rotate(ee_quat_w, forward_local)
        return forward_w / torch.norm(forward_w, dim=-1, keepdim=True).clamp_min(1e-6)

    def _quat_rotate(self, quat_wxyz: torch.Tensor, vec_xyz: torch.Tensor) -> torch.Tensor:
        qw = quat_wxyz[:, :1]
        qxyz = quat_wxyz[:, 1:]
        t = 2.0 * torch.cross(qxyz, vec_xyz, dim=-1)
        return vec_xyz + qw * t + torch.cross(qxyz, t, dim=-1)

    def _quat_conjugate(self, quat_wxyz: torch.Tensor) -> torch.Tensor:
        qc = quat_wxyz.clone()
        qc[:, 1:] = -qc[:, 1:]
        return qc

    def _quat_multiply(self, qa_wxyz: torch.Tensor, qb_wxyz: torch.Tensor) -> torch.Tensor:
        aw, ax, ay, az = qa_wxyz[:, 0], qa_wxyz[:, 1], qa_wxyz[:, 2], qa_wxyz[:, 3]
        bw, bx, by, bz = qb_wxyz[:, 0], qb_wxyz[:, 1], qb_wxyz[:, 2], qb_wxyz[:, 3]
        return torch.stack(
            (
                aw * bw - ax * bx - ay * by - az * bz,
                aw * bx + ax * bw + ay * bz - az * by,
                aw * by - ax * bz + ay * bw + az * bx,
                aw * bz + ax * by - ay * bx + az * bw,
            ),
            dim=-1,
        )

    def _ensure_debug_markers(self) -> None:
        if not self.cfg.debug_vis:
            return
        if self.cfg.debug_show_target_marker and not hasattr(self, "_target_vis"):
            marker_cfg = SPHERE_MARKER_CFG.copy()
            marker_cfg.prim_path = "/Visuals/ReachTargetsSO100"
            marker_cfg.markers["sphere"].radius = float(self.cfg.debug_vis_target_marker_radius)
            marker_cfg.markers["sphere"].visual_material = sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.2, 0.2))
            self._target_vis = VisualizationMarkers(marker_cfg)
        if not hasattr(self, "_tcp_vis"):
            tcp_cfg = SPHERE_MARKER_CFG.copy()
            tcp_cfg.prim_path = "/Visuals/ReachTcpSO100"
            tcp_cfg.markers["sphere"].radius = float(self.cfg.debug_vis_tcp_marker_radius)
            tcp_cfg.markers["sphere"].visual_material = sim_utils.PreviewSurfaceCfg(diffuse_color=(0.2, 0.95, 0.3))
            self._tcp_vis = VisualizationMarkers(tcp_cfg)

    def _update_debug_markers(self) -> None:
        if not self.cfg.debug_vis:
            return
        self._ensure_debug_markers()
        tcp_w, _ = self._tcp_pose_w()
        if hasattr(self, "_tcp_vis"):
            self._tcp_vis.visualize(tcp_w)
        if self.cfg.debug_show_target_marker and hasattr(self, "_target_vis"):
            self._target_vis.visualize(self._target_pos_w)

    def _set_debug_vis_impl(self, debug_vis: bool) -> None:
        if debug_vis:
            self._ensure_debug_markers()
            self._update_debug_markers()
            if hasattr(self, "_target_vis"):
                self._target_vis.set_visibility(self.cfg.debug_show_target_marker)
            if hasattr(self, "_tcp_vis"):
                self._tcp_vis.set_visibility(True)
        else:
            if hasattr(self, "_target_vis"):
                self._target_vis.set_visibility(False)
            if hasattr(self, "_tcp_vis"):
                self._tcp_vis.set_visibility(False)

    def _debug_vis_callback(self, event) -> None:
        if self.cfg.debug_vis:
            self._update_debug_markers()
