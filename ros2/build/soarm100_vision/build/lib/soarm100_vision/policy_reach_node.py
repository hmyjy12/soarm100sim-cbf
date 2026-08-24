"""Real-hardware policy reach loop with a bounded streaming safety boundary.

This node intentionally uses MuJoCo only for the same FK/TCP/observation code
used by the trained policy. It does not start a simulator or write serial data.
Joint targets are published to the separate ROS2 hardware controller, which
owns the Feetech bus and independently validates every streamed target.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, String

from soarm100_vision.control.policy_command_shaper import (
    PolicyCommandShaper,
    ShaperConfig,
)
from soarm100_vision.control.joint_limit_cbf import (
    JointLimitCbfConfig,
    JointLimitCbfFilter,
)
from soarm100_vision.hardware_joint_limit_filter import HardwareJointLimitFilter


JOINT_NAMES = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)


def _load_training_runtime(repo: Path):
    """Load the real MuJoCo package, not this repository's `mujoco/` folder."""
    repo = repo.resolve()
    os.chdir(repo / "ros2")
    sys.path[:] = [
        entry for entry in sys.path
        if entry and Path(entry).resolve() != repo
    ]
    import mujoco  # type: ignore

    source_dir = str(repo / "mujoco")
    if source_dir not in sys.path:
        sys.path.insert(0, source_dir)
    import policy as reach_policy  # type: ignore
    import runtime as reach_runtime  # type: ignore
    return mujoco, reach_policy, reach_runtime


def _quat_angle_deg(current: np.ndarray, desired: np.ndarray) -> float:
    current = current / max(float(np.linalg.norm(current)), 1e-12)
    desired = desired / max(float(np.linalg.norm(desired)), 1e-12)
    dot = abs(float(np.dot(current, desired)))
    return math.degrees(2.0 * math.acos(float(np.clip(dot, 0.0, 1.0))))


class PolicyReachNode(Node):
    def __init__(self) -> None:
        super().__init__("so100_plus_policy_reach")
        repo_default = str(Path(__file__).resolve().parents[3])
        self.declare_parameter("repo_root", repo_default)
        self.declare_parameter(
            "checkpoint",
            "rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt",
        )
        self.declare_parameter(
            "mjcf",
            "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml",
        )
        self.declare_parameter(
            "target_config", "ros2/config/real/policy_reach_target.json"
        )
        self.declare_parameter("control_rate_hz", 20.0)
        self.declare_parameter("action_scale", 0.25)
        self.declare_parameter("action_filter_tau_s", 0.08)
        self.declare_parameter("velocity_filter_tau_s", 0.12)
        self.declare_parameter("max_joint_velocity_rad_s", 0.20)
        self.declare_parameter("max_joint_acceleration_rad_s2", 0.80)
        self.declare_parameter("max_tracking_error_rad", 0.25)
        self.declare_parameter("enable_joint_limit_cbf", False)
        self.declare_parameter("hardware_calibration_json", "hardware/calibration/lerobot/so100_plus_new_arm.json")
        self.declare_parameter("hardware_mapping_json", "hardware/calibration/policy_joint_mapping.json")
        self.declare_parameter("hardware_limit_margin_counts", 100)
        self.declare_parameter("joint_limit_cbf_alpha", 4.0)
        self.declare_parameter("joint_limit_cbf_activation_margin_rad", 0.25)
        self.declare_parameter("joint_limit_cbf_recovery_velocity_rad_s", 0.05)
        self.declare_parameter("joint_limit_stall_timeout_s", 2.0)
        self.declare_parameter("joint_limit_stall_min_progress_m", 0.003)
        self.declare_parameter("workspace_min_z_m", 0.01)
        self.declare_parameter("action_deadband", 0.01)
        self.declare_parameter("freeze_gripper", True)
        self.declare_parameter("frozen_gripper_target_rad", -999.0)
        self.declare_parameter("success_position_m", 0.015)
        self.declare_parameter("success_orientation_deg", 10.0)
        self.declare_parameter("success_consecutive_ticks", 5)
        self.declare_parameter("hold_current_duration_s", 3.0)
        self.declare_parameter("timeout_s", 20.0)
        self.declare_parameter("joint_state_timeout_s", 1.5)
        self.declare_parameter("training_range_recovery_margin_rad", 0.05)
        self.declare_parameter("start_on_launch", False)
        self.declare_parameter("log_path", "logs/hardware/policy_reach.jsonl")

        self.repo = Path(str(self.get_parameter("repo_root").value)).resolve()
        self.mujoco, policy_mod, self.runtime = _load_training_runtime(self.repo)
        self.target_pos, self.target_quat, self.hold_current = self._load_target()
        self.model = self.mujoco.MjModel.from_xml_path(
            str(self.repo / str(self.get_parameter("mjcf").value))
        )
        self.data = self.mujoco.MjData(self.model)
        self.ids = self.runtime.resolve_robot_ids(self.model)
        self.policy = policy_mod.SkrlGaussianPolicy(
            self.repo / str(self.get_parameter("checkpoint").value)
        )

        rate = float(self.get_parameter("control_rate_hz").value)
        if not 5.0 <= rate <= 30.0:
            raise ValueError("control_rate_hz must be within [5, 30]")
        self.dt = 1.0 / rate
        self.shaper = PolicyCommandShaper(
            ShaperConfig(
                nominal_rate_hz=rate,
                action_scale_rad=float(self.get_parameter("action_scale").value),
                action_filter_tau_s=float(
                    self.get_parameter("action_filter_tau_s").value
                ),
                velocity_filter_tau_s=float(
                    self.get_parameter("velocity_filter_tau_s").value
                ),
                max_velocity_rad_s=float(
                    self.get_parameter("max_joint_velocity_rad_s").value
                ),
                max_acceleration_rad_s2=float(
                    self.get_parameter("max_joint_acceleration_rad_s2").value
                ),
                max_tracking_error_rad=float(
                    self.get_parameter("max_tracking_error_rad").value
                ),
                action_deadband=float(self.get_parameter("action_deadband").value),
            )
        )
        self.joint_limit_cbf: JointLimitCbfFilter | None = None
        self.hardware_safe_low: np.ndarray | None = None
        self.hardware_safe_high: np.ndarray | None = None
        if bool(self.get_parameter("enable_joint_limit_cbf").value):
            hardware_filter = HardwareJointLimitFilter(
                repo_root=self.repo,
                calibration_json=str(self.get_parameter("hardware_calibration_json").value),
                mapping_json=str(self.get_parameter("hardware_mapping_json").value),
                margin_counts=int(self.get_parameter("hardware_limit_margin_counts").value),
            )
            self.hardware_safe_low, self.hardware_safe_high = hardware_filter.policy_safe_bounds()
            self.joint_limit_cbf = JointLimitCbfFilter(
                JointLimitCbfConfig(
                    alpha=float(self.get_parameter("joint_limit_cbf_alpha").value),
                    activation_margin_rad=float(
                        self.get_parameter("joint_limit_cbf_activation_margin_rad").value
                    ),
                    recovery_velocity_rad_s=float(
                        self.get_parameter("joint_limit_cbf_recovery_velocity_rad_s").value
                    ),
                )
            )
        self.current_q: np.ndarray | None = None
        self.last_joint_time: float | None = None
        self.last_observation: dict | None = None
        self.gripper_hold: float | None = None
        self.hold_q: np.ndarray | None = None
        self.started_at: float | None = None
        self.start_range_reported = False
        self.in_training_range_recovery = False
        self.done = False
        self.success_ticks = 0
        self.tick_index = 0
        self.limit_active_since: float | None = None
        self.limit_active_initial_error: float | None = None
        self.limit_active_best_error: float | None = None
        self.log_file = None

        self.target_pub = self.create_publisher(JointState, "/hardware/joint_target", 1)
        self.status_pub = self.create_publisher(String, "/policy_reach/status", 10)
        self.create_subscription(JointState, "/joint_states", self._on_joint_state, 10)
        self.create_subscription(Bool, "/hardware/joint_state_stale", self._on_stale, 1)
        # Control is driven by fresh joint feedback.  This watchdog never
        # produces commands; it only catches a stopped feedback stream.
        self.create_timer(0.1, self._feedback_watchdog)
        self._open_log()
        self._publish_status("WAITING_FOR_JOINT_STATE")
        self.get_logger().info(
            "policy reach ready: checkpoint loaded, MuJoCo FK only, "
            f"target=({self.target_pos[0]:+.3f},{self.target_pos[1]:+.3f},{self.target_pos[2]:+.3f}), "
            f"feedback-driven rate={rate:.1f}Hz "
            f"vmax={float(self.get_parameter('max_joint_velocity_rad_s').value):.3f}rad/s "
            f"amax={float(self.get_parameter('max_joint_acceleration_rad_s2').value):.3f}rad/s2 "
            f"tracking_limit={float(self.get_parameter('max_tracking_error_rad').value):.3f}rad "
            f"joint_limit_cbf={self.joint_limit_cbf is not None} "
            f"start_on_launch={bool(self.get_parameter('start_on_launch').value)}"
        )

    def _load_target(self) -> tuple[np.ndarray, np.ndarray, bool]:
        path = self.repo / str(self.get_parameter("target_config").value)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if str(payload.get("frame_id", "")) != "base":
            raise ValueError("policy reach target frame_id must be exactly 'base'")
        pos = np.asarray(payload.get("position_m"), dtype=np.float64).reshape(3)
        quat = np.asarray(payload.get("quaternion_wxyz"), dtype=np.float64).reshape(4)
        if not np.all(np.isfinite(pos)) or not np.all(np.isfinite(quat)):
            raise ValueError("target pose contains non-finite values")
        min_z = float(self.get_parameter("workspace_min_z_m").value)
        if not (0.08 <= pos[0] <= 0.45 and -0.30 <= pos[1] <= 0.30 and min_z <= pos[2] <= 0.45):
            raise ValueError(f"target position outside conservative workspace: {pos.tolist()}")
        quat /= max(float(np.linalg.norm(quat)), 1e-12)
        return pos, quat, bool(payload.get("hold_current", False))

    def _open_log(self) -> None:
        path = self.repo / str(self.get_parameter("log_path").value)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.log_file = path.open("a", encoding="utf-8")

    def _log(self, event: str, **values) -> None:
        if self.log_file is None:
            return
        row = {"wall_time": time.time(), "event": event, **values}
        self.log_file.write(json.dumps(row, ensure_ascii=True) + "\n")
        self.log_file.flush()

    def _publish_status(self, status: str, **values) -> None:
        payload = {"status": status, **values}
        self.status_pub.publish(String(data=json.dumps(payload, ensure_ascii=True)))
        self._log("status", **payload)

    def _on_joint_state(self, msg: JointState) -> None:
        if tuple(msg.name) != JOINT_NAMES or len(msg.position) != 7:
            self.get_logger().error("ignored joint state with unexpected joint order", throttle_duration_sec=2.0)
            return
        q = np.asarray(msg.position, dtype=np.float64)
        if not np.all(np.isfinite(q)):
            self.get_logger().error("ignored non-finite joint state", throttle_duration_sec=2.0)
            return
        now = time.monotonic()
        self.current_q = q
        self.last_joint_time = now
        try:
            self.last_observation = self.shaper.observe(q, now)
        except ValueError as exc:
            self.get_logger().error(f"ignored invalid joint-state timing: {exc}")
            return
        if self.gripper_hold is None:
            self.gripper_hold = float(q[6])
        self._control_tick(now)

    def _on_stale(self, msg: Bool) -> None:
        if msg.data and not self.done and self.started_at is not None:
            self._stop("JOINT_STATE_STALE")

    def _feedback_watchdog(self) -> None:
        if self.done or self.started_at is None or self.last_joint_time is None:
            return
        if time.monotonic() - self.last_joint_time > float(
            self.get_parameter("joint_state_timeout_s").value
        ):
            self._stop("JOINT_STATE_TIMEOUT")

    def _set_model_state(self, q: np.ndarray, qvel: np.ndarray) -> None:
        for adr, value in zip(self.ids.qpos_adr, q):
            self.data.qpos[adr] = float(value)
        for adr, value in zip(self.ids.dof_adr, qvel):
            self.data.qvel[adr] = float(value)
        self.mujoco.mj_forward(self.model, self.data)

    def _control_tick(self, now: float) -> None:
        if self.done:
            return
        if self.current_q is None or self.last_joint_time is None or self.last_observation is None:
            return
        if self.started_at is None:
            if not bool(self.get_parameter("start_on_launch").value):
                return
            if not self.start_range_reported:
                self.start_range_reported = True
                outside = []
                for name, value, low, high in zip(
                    JOINT_NAMES, self.current_q, self.ids.q_low, self.ids.q_high
                ):
                    if value < low or value > high:
                        outside.append(
                            f"{name}={value:+.4f}rad outside training [{low:+.4f},{high:+.4f}]"
                        )
                if outside:
                    detail = "; ".join(outside)
                    self.get_logger().warning(
                        "starting from a hardware-safe pose outside the MuJoCo training "
                        f"range; policy success is not guaranteed: {detail}"
                    )
                    self._log("start_outside_training_range", detail=detail)
            self.started_at = now
            if self.hold_current:
                self.hold_q = self.current_q.copy()
            self._publish_status("RUNNING")

        q = self.current_q.copy()
        timing = self.last_observation
        qvel = np.clip(timing["qvel_filtered"], -4.0, 4.0)
        self._set_model_state(q, qvel)
        tcp, quat = self.runtime.tcp_pose_w(self.data, self.ids)
        pos_err = float(np.linalg.norm(self.target_pos - tcp))
        ori_err = _quat_angle_deg(quat, self.target_quat)
        if self.hold_current:
            assert self.hold_q is not None
            self._publish_target(self.hold_q)
            self.tick_index += 1
            self._log(
                "hold_current",
                tick=self.tick_index,
                q=q.tolist(),
                q_cmd=self.hold_q.tolist(),
                raw_dt_s=timing["raw_dt_s"],
                dt_s=timing["dt_s"],
                qvel_raw=timing["qvel_raw"].tolist(),
                qvel_filtered=qvel.tolist(),
                tracking_error_rad=(self.hold_q - q).tolist(),
            )
            if now - self.started_at >= float(
                self.get_parameter("hold_current_duration_s").value
            ):
                self._stop("HOLD_TEST_COMPLETE")
            return
        if now - self.started_at > float(self.get_parameter("timeout_s").value):
            self._stop("TIMEOUT", **self._pose_error_fields(tcp, quat, pos_err, ori_err))
            return

        recovery_margin = float(
            self.get_parameter("training_range_recovery_margin_rad").value
        )
        recovery_low = self.ids.q_low + recovery_margin
        recovery_high = self.ids.q_high - recovery_margin
        recovery_error = np.clip(q, recovery_low, recovery_high) - q
        # The gripper is held throughout reach and does not participate in
        # restoring arm joints to the policy's trained state range.
        recovery_error[6] = 0.0
        if np.any(np.abs(recovery_error[:6]) > 1e-8):
            self.in_training_range_recovery = True
            recovery_action = np.sign(recovery_error)
            frozen = np.array([False] * 6 + [True], dtype=bool)
            command_low = np.minimum(recovery_low, q)
            command_high = np.maximum(recovery_high, q)
            recovery_cbf = None
            if self.joint_limit_cbf is not None:
                assert self.hardware_safe_low is not None
                assert self.hardware_safe_high is not None
                recovery_cbf = self.joint_limit_cbf.velocity_bounds(
                    q, self.hardware_safe_low, self.hardware_safe_high
                )
                recovery_cbf["velocity_low_rad_s"][6] = -np.inf
                recovery_cbf["velocity_high_rad_s"][6] = np.inf
            shaped = self.shaper.shape(
                q,
                recovery_action,
                command_low,
                command_high,
                timing["dt_s"],
                frozen,
                None if recovery_cbf is None else recovery_cbf["velocity_low_rad_s"],
                None if recovery_cbf is None else recovery_cbf["velocity_high_rad_s"],
            )
            q_cmd = shaped["q_ref"]
            self._publish_target(q_cmd)
            self.tick_index += 1
            self._log(
                "training_range_recovery",
                tick=self.tick_index,
                q=q.tolist(),
                q_cmd=q_cmd.tolist(),
                recovery_error=recovery_error.tolist(),
                raw_dt_s=timing["raw_dt_s"],
                dt_s=timing["dt_s"],
                qvel_raw=timing["qvel_raw"].tolist(),
                qvel_filtered=qvel.tolist(),
                reference_velocity_rad_s=shaped["reference_velocity_rad_s"].tolist(),
                tracking_error_rad=shaped["tracking_error_rad"].tolist(),
                joint_limit_cbf_clamped=shaped["safety_velocity_clamped"].tolist(),
                tcp_pos_m=tcp.tolist(),
                pos_err_m=pos_err,
                orientation_err_deg=ori_err,
            )
            if self.tick_index % 10 == 0:
                self.get_logger().info(
                    f"recovery tick={self.tick_index} max_joint_error="
                    f"{float(np.max(np.abs(recovery_error[:6]))):.4f}rad"
                )
            return

        if self.in_training_range_recovery:
            self.in_training_range_recovery = False
            self.shaper.clear_action_state()

        obs, info = self.runtime.make_obs(self.data, self.ids, self.target_pos, self.target_quat)
        raw_action = np.clip(self.policy.act_mean(obs).astype(np.float64), -1.0, 1.0)
        frozen = np.zeros(7, dtype=bool)
        if bool(self.get_parameter("freeze_gripper").value):
            frozen[6] = True
        cbf = None
        if self.joint_limit_cbf is not None:
            assert self.hardware_safe_low is not None and self.hardware_safe_high is not None
            cbf = self.joint_limit_cbf.velocity_bounds(
                q, self.hardware_safe_low, self.hardware_safe_high
            )
            cbf["velocity_low_rad_s"][6] = -np.inf
            cbf["velocity_high_rad_s"][6] = np.inf
        shaped = self.shaper.shape(
            q,
            raw_action,
            recovery_low,
            recovery_high,
            timing["dt_s"],
            frozen,
            None if cbf is None else cbf["velocity_low_rad_s"],
            None if cbf is None else cbf["velocity_high_rad_s"],
        )
        q_cmd = shaped["q_ref"]
        frozen_gripper_target = float(
            self.get_parameter("frozen_gripper_target_rad").value
        )
        if bool(self.get_parameter("freeze_gripper").value) and frozen_gripper_target > -900.0:
            # Preserve a close command during lift instead of replacing it with
            # the measured, object-blocked finger position.
            q_cmd[6] = float(
                np.clip(
                    frozen_gripper_target,
                    q[6] - self.shaper.cfg.max_tracking_error_rad,
                    q[6] + self.shaper.cfg.max_tracking_error_rad,
                )
            )
        dq_cmd = q_cmd - q

        limit_clamped = shaped["safety_velocity_clamped"][:6]
        if np.any(limit_clamped):
            if self.limit_active_since is None:
                self.limit_active_since = now
                self.limit_active_initial_error = pos_err
                self.limit_active_best_error = pos_err
            else:
                assert self.limit_active_initial_error is not None
                assert self.limit_active_best_error is not None
                self.limit_active_best_error = min(self.limit_active_best_error, pos_err)
                active_for = now - self.limit_active_since
                progress = self.limit_active_initial_error - self.limit_active_best_error
                if (
                    active_for >= float(self.get_parameter("joint_limit_stall_timeout_s").value)
                    and progress < float(self.get_parameter("joint_limit_stall_min_progress_m").value)
                ):
                    active_names = [
                        JOINT_NAMES[i] for i in np.flatnonzero(limit_clamped)
                    ]
                    self._publish_target(q)
                    self._stop(
                        "JOINT_LIMIT_STALLED",
                        active_joints=active_names,
                        active_for_s=active_for,
                        progress_m=progress,
                        **self._pose_error_fields(tcp, quat, pos_err, ori_err),
                    )
                    return
        else:
            self.limit_active_since = None
            self.limit_active_initial_error = None
            self.limit_active_best_error = None

        if pos_err <= float(self.get_parameter("success_position_m").value) and ori_err <= float(self.get_parameter("success_orientation_deg").value):
            self.success_ticks += 1
        else:
            self.success_ticks = 0
        if self.success_ticks >= int(self.get_parameter("success_consecutive_ticks").value):
            self._publish_target(q)
            self._stop("SUCCESS", **self._pose_error_fields(tcp, quat, pos_err, ori_err))
            return
        self._publish_target(q_cmd)
        self.tick_index += 1
        self._log(
            "control",
            tick=self.tick_index,
            q=q.tolist(),
            qvel=qvel.tolist(),
            qvel_raw=timing["qvel_raw"].tolist(),
            raw_dt_s=timing["raw_dt_s"],
            dt_s=timing["dt_s"],
            tcp_pos_m=tcp.tolist(),
            tcp_quat_wxyz=quat.tolist(),
            target_pos_m=self.target_pos.tolist(),
            target_quat_wxyz=self.target_quat.tolist(),
            pos_err_m=pos_err,
            orientation_err_deg=ori_err,
            raw_action=raw_action.tolist(),
            filtered_action=shaped["filtered_action"].tolist(),
            dq_policy=shaped["requested_dq"].tolist(),
            dq_cmd=dq_cmd.tolist(),
            q_cmd=q_cmd.tolist(),
            q_ref=q_cmd.tolist(),
            desired_velocity_rad_s=shaped["desired_velocity_rad_s"].tolist(),
            reference_velocity_rad_s=shaped["reference_velocity_rad_s"].tolist(),
            unconstrained_velocity_rad_s=shaped["unconstrained_velocity_rad_s"].tolist(),
            joint_limit_cbf_enabled=cbf is not None,
            joint_limit_cbf_active=(
                [False] * 7 if cbf is None else cbf["active"].tolist()
            ),
            joint_limit_cbf_clamped=shaped["safety_velocity_clamped"].tolist(),
            joint_limit_h_low_rad=(None if cbf is None else cbf["h_low_rad"].tolist()),
            joint_limit_h_high_rad=(None if cbf is None else cbf["h_high_rad"].tolist()),
            tracking_error_rad=shaped["tracking_error_rad"].tolist(),
            tracking_clamped=shaped["tracking_clamped"].tolist(),
            action_filter_alpha=shaped["action_filter_alpha"],
            velocity_filter_alpha=timing["velocity_filter_alpha"],
            action_scale=float(self.get_parameter("action_scale").value),
        )
        if self.tick_index % 10 == 0:
            self.get_logger().info(
                f"reach tick={self.tick_index} pos_err={pos_err * 1000.0:.1f}mm "
                f"ori_err={ori_err:.1f}deg |dq|={float(np.linalg.norm(dq_cmd)):.4f}"
            )

    def _pose_error_fields(
        self,
        tcp: np.ndarray,
        quat: np.ndarray,
        pos_err: float,
        ori_err: float,
    ) -> dict:
        """Scalar + per-axis residuals for terminal/status/jsonl reporting."""
        offset_m = np.asarray(tcp, dtype=np.float64).reshape(3) - self.target_pos
        return {
            "pos_err_m": pos_err,
            "orientation_err_deg": ori_err,
            "tcp_pos_m": np.asarray(tcp, dtype=float).reshape(3).tolist(),
            "target_pos_m": self.target_pos.tolist(),
            "offset_xyz_m": offset_m.tolist(),
            "offset_xyz_mm": (offset_m * 1000.0).tolist(),
            "tcp_quat_wxyz": np.asarray(quat, dtype=float).reshape(4).tolist(),
            "target_quat_wxyz": self.target_quat.tolist(),
        }

    def _publish_target(self, q_cmd: np.ndarray) -> None:
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(JOINT_NAMES)
        msg.position = [float(value) for value in q_cmd]
        self.target_pub.publish(msg)

    def _stop(self, reason: str, **values) -> None:
        if self.done:
            return
        # Replace the last policy offset with the latest measured posture before
        # the launcher tears down the controller. This prevents a timed-out
        # policy target from continuing to load or oscillate the servos.
        if self.current_q is not None:
            self._publish_target(self.current_q)
        self.done = True
        self._publish_status(reason, **values)
        offset = values.get("offset_xyz_mm")
        if isinstance(offset, (list, tuple)) and len(offset) == 3:
            self.get_logger().warning(
                f"policy reach stopped: {reason} "
                f"pos_err_m={values.get('pos_err_m')} "
                f"orientation_err_deg={values.get('orientation_err_deg')} "
                f"offset_xyz_mm="
                f"({float(offset[0]):+.2f},{float(offset[1]):+.2f},{float(offset[2]):+.2f})"
            )
        else:
            self.get_logger().warning(f"policy reach stopped: {reason} {values}")

    def destroy_node(self) -> bool:
        if self.log_file is not None:
            self.log_file.close()
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = PolicyReachNode()
    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
