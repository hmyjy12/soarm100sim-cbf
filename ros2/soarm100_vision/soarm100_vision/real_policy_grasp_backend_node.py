"""Execute one planned grasp on real hardware with the trained reach policy."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import threading
import time
from pathlib import Path

import numpy as np
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState

from soarm100_interfaces.action import ExecutePlannedGrasp
from soarm100_vision.policy_backend_core import pose_to_base_from_calib


JOINT_NAMES = (
    "shoulder_rotation_joint", "shoulder_pitch_joint", "ellbow_joint",
    "wrist_pitch_joint", "wrist_jaw_joint", "wrist_roll_joint", "gripper_joint",
)


class RealPolicyGraspBackendNode(Node):
    def __init__(self) -> None:
        super().__init__("soarm100_real_policy_grasp_backend")
        root = str(Path(__file__).resolve().parents[3])
        self.declare_parameter("repo_root", root)
        self.declare_parameter(
            "python_executable",
            str(Path.home() / "miniconda3/envs/vision_seg/bin/python"),
        )
        self.declare_parameter("calib_json", "hardware/calibration/camera/real_camera_calib.json")
        self.declare_parameter("input_camera_name", "scene_depth")
        self.declare_parameter("checkpoint", "rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt")
        self.declare_parameter("mjcf", "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml")
        self.declare_parameter("control_rate_hz", 20.0)
        self.declare_parameter("max_tracking_error_rad", 0.25)
        self.declare_parameter("enable_joint_limit_cbf", False)
        self.declare_parameter("hardware_limit_margin_counts", 0)
        self.declare_parameter("workspace_min_z_m", 0.01)
        self.declare_parameter("reach_timeout_s", 25.0)
        self.declare_parameter("success_position_m", 0.020)
        self.declare_parameter("success_orientation_deg", 12.0)
        self.declare_parameter("open_gripper_rad", 0.45)
        self.declare_parameter("close_gripper_rad", -0.15)
        self.declare_parameter("gripper_velocity_rad_s", 0.35)
        self.declare_parameter("lift_height_m", 0.05)
        self.declare_parameter("log_dir", "log/runtime/hardware/real_single_grasp")

        self.repo = Path(str(self.get_parameter("repo_root").value)).resolve()
        self._q_lock = threading.Lock()
        self._current_q: np.ndarray | None = None
        self._last_joint_time = 0.0
        self._active = False
        group = ReentrantCallbackGroup()
        self._target_pub = self.create_publisher(JointState, "/hardware/joint_target", 1)
        self.create_subscription(
            JointState, "/joint_states", self._on_joint_state, 10,
            callback_group=group,
        )
        self._server = ActionServer(
            self, ExecutePlannedGrasp, "execute_planned_grasp",
            execute_callback=self._execute,
            goal_callback=self._goal,
            cancel_callback=self._cancel,
            callback_group=group,
        )
        self.get_logger().info(
            "real policy grasp backend ready: single plan, tracking=OFF, "
            "replan=OFF, avoidance=OFF"
        )

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _on_joint_state(self, msg: JointState) -> None:
        if tuple(msg.name) != JOINT_NAMES or len(msg.position) != 7:
            return
        q = np.asarray(msg.position, dtype=np.float64)
        if np.all(np.isfinite(q)):
            with self._q_lock:
                self._current_q = q
                self._last_joint_time = time.monotonic()

    def _goal(self, goal) -> GoalResponse:
        if self._active:
            return GoalResponse.REJECT
        if bool(goal.enable_avoidance):
            self.get_logger().error("real single-grasp v1 rejects avoidance=true")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _cancel(self, _goal_handle) -> CancelResponse:
        return CancelResponse.ACCEPT

    def _feedback(self, goal_handle, stage: str, reason: str, lift: float = 0.0) -> None:
        msg = ExecutePlannedGrasp.Feedback()
        msg.stage = stage
        msg.reason = reason
        msg.lift_height = float(lift)
        goal_handle.publish_feedback(msg)
        self.get_logger().info(f"stage={stage} reason={reason}")

    def _fresh_q(self, timeout: float = 5.0) -> np.ndarray:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._q_lock:
                q = None if self._current_q is None else self._current_q.copy()
                age = time.monotonic() - self._last_joint_time
            if q is not None and age < 0.5:
                return q
            time.sleep(0.05)
        raise RuntimeError("joint_state_unavailable_or_stale")

    def _publish_q(self, q: np.ndarray) -> None:
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(JOINT_NAMES)
        msg.position = np.asarray(q, dtype=float).tolist()
        self._target_pub.publish(msg)

    def _move_gripper(self, target: float, duration: float, *, require_reached: bool) -> dict:
        start = self._fresh_q()
        initial = float(start[6])
        velocity = max(float(self._param("gripper_velocity_rad_s")), 0.05)
        duration = max(float(duration), abs(target - initial) / velocity, 0.3)
        steps = max(2, int(round(duration * float(self._param("control_rate_hz")))))
        for index in range(1, steps + 1):
            q = self._fresh_q()
            desired = initial + (target - initial) * (index / steps)
            # Keep every stream request inside the hardware controller's
            # measured-position tracking boundary.
            q[6] = float(np.clip(desired, q[6] - 0.20, q[6] + 0.20))
            self._publish_q(q)
            time.sleep(duration / steps)
        q = self._fresh_q()
        error = float(target - q[6])
        held_target = float(np.clip(target, q[6] - 0.20, q[6] + 0.20))
        self._publish_q(np.array([*q[:6], held_target], dtype=np.float64))
        if require_reached and abs(error) > 0.10:
            raise RuntimeError(f"gripper_open_not_reached:error={error:+.3f}rad")
        return {
            "start_rad": initial,
            "target_rad": target,
            "held_target_rad": held_target,
            "measured_rad": float(q[6]),
            "error_rad": error,
        }

    @staticmethod
    def _pose_arrays(pose) -> tuple[np.ndarray, np.ndarray]:
        p = pose.pose.position
        q = pose.pose.orientation
        return (
            np.array([p.x, p.y, p.z], dtype=np.float64),
            np.array([q.w, q.x, q.y, q.z], dtype=np.float64),
        )

    def _to_base(self, pose):
        return pose_to_base_from_calib(
            pose,
            repo_root=self.repo,
            calib_json=str(self._param("calib_json")),
            input_camera_name=str(self._param("input_camera_name")),
            base_frame="base",
        )

    def _run_policy_pose(self, position: np.ndarray, quat: np.ndarray, stage: str, gripper_target: float) -> dict:
        stamp = time.strftime("%Y%m%d_%H%M%S") + f"_{time.time_ns() % 1_000_000_000:09d}"
        log_dir = self.repo / str(self._param("log_dir"))
        log_dir.mkdir(parents=True, exist_ok=True)
        target_path = log_dir / f"target_{stage.lower()}_{stamp}.json"
        log_path = log_dir / f"policy_{stage.lower()}_{stamp}.jsonl"
        target_path.write_text(json.dumps({
            "frame_id": "base",
            "position_m": position.tolist(),
            "quaternion_wxyz": quat.tolist(),
            "hold_current": False,
        }, indent=2), encoding="utf-8")
        command = [
            str(self._param("python_executable")),
            str(self.repo / "ros2/soarm100_vision/soarm100_vision/policy_reach_node.py"),
            "--ros-args",
            "-p", f"repo_root:={self.repo}",
            "-p", f"checkpoint:={self._param('checkpoint')}",
            "-p", f"mjcf:={self._param('mjcf')}",
            "-p", f"target_config:={target_path.relative_to(self.repo)}",
            "-p", f"control_rate_hz:={float(self._param('control_rate_hz')):.6f}",
            "-p", f"max_tracking_error_rad:={float(self._param('max_tracking_error_rad')):.6f}",
            "-p", f"enable_joint_limit_cbf:={str(bool(self._param('enable_joint_limit_cbf'))).lower()}",
            "-p", f"hardware_limit_margin_counts:={int(self._param('hardware_limit_margin_counts'))}",
            "-p", f"workspace_min_z_m:={float(self._param('workspace_min_z_m')):.6f}",
            "-p", f"timeout_s:={float(self._param('reach_timeout_s')):.6f}",
            "-p", f"success_position_m:={float(self._param('success_position_m')):.6f}",
            "-p", f"success_orientation_deg:={float(self._param('success_orientation_deg')):.6f}",
            "-p", f"frozen_gripper_target_rad:={float(gripper_target):.6f}",
            "-p", "start_on_launch:=true",
            "-p", f"log_path:={log_path.relative_to(self.repo)}",
        ]
        proc = subprocess.run(
            command, cwd=self.repo, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=float(self._param("reach_timeout_s")) + 15.0,
        )
        terminal = None
        if log_path.is_file():
            for line in log_path.read_text(encoding="utf-8").splitlines():
                row = json.loads(line)
                if row.get("event") == "status":
                    terminal = row
        status = str((terminal or {}).get("status", "NO_TERMINAL_STATUS"))
        result = {
            "stage": stage, "status": status, "returncode": proc.returncode,
            "target": position.tolist(), "quat": quat.tolist(),
            "log_path": str(log_path), "stdout_tail": proc.stdout[-3000:],
            "terminal": terminal,
        }
        (log_dir / f"result_{stage.lower()}_{stamp}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        if proc.returncode != 0 or status != "SUCCESS":
            raise RuntimeError(
                f"policy_{stage.lower()}_failed:status={status}:rc={proc.returncode}:"
                f"log={log_path}"
            )
        return result

    def _execute(self, goal_handle):
        result = ExecutePlannedGrasp.Result()
        self._active = True
        started = time.monotonic()
        try:
            raw_pre = goal_handle.request.pregrasp_pose
            raw_grasp = goal_handle.request.grasp_pose
            base_pre = self._to_base(raw_pre)
            base_grasp = self._to_base(raw_grasp)
            pre_pos, pre_quat = self._pose_arrays(base_pre)
            grasp_pos, grasp_quat = self._pose_arrays(base_grasp)
            open_q = float(self._param("open_gripper_rad"))
            close_q = float(self._param("close_gripper_rad"))
            self.get_logger().info(
                f"single grasp target={goal_handle.request.target_prompt} "
                f"pre={pre_pos.tolist()} grasp={grasp_pos.tolist()} "
                f"width={goal_handle.request.gripper_width*1000.0:.1f}mm"
            )

            self._feedback(goal_handle, "OPEN", "opening gripper before policy motion")
            open_result = self._move_gripper(open_q, 1.0, require_reached=True)
            self._feedback(goal_handle, "MOVE_TO_PREGRASP", json.dumps(open_result))
            self._run_policy_pose(pre_pos, pre_quat, "PREGRASP", open_q)
            self._feedback(goal_handle, "FINAL_APPROACH", "pregrasp reached")
            self._run_policy_pose(grasp_pos, grasp_quat, "FINAL", open_q)

            self._feedback(goal_handle, "CLOSE", "final pose reached; tracking remains disabled")
            close_result = self._move_gripper(close_q, 1.2, require_reached=False)
            self._feedback(goal_handle, "LIFT", json.dumps(close_result))
            lift_pos = grasp_pos + np.array([0.0, 0.0, float(self._param("lift_height_m"))])
            self._run_policy_pose(lift_pos, grasp_quat, "LIFT", close_q)

            result.success = True
            result.reason = f"single_grasp_complete elapsed={time.monotonic()-started:.2f}s"
            result.lift_height = float(self._param("lift_height_m"))
            result.return_code = 0
            goal_handle.succeed()
        except subprocess.TimeoutExpired as exc:
            result.reason = f"policy_process_timeout:{exc}"
            result.return_code = 2
            goal_handle.abort()
        except Exception as exc:
            result.reason = str(exc)
            result.return_code = 1
            goal_handle.abort()
        finally:
            self._active = False
        return result


def main() -> None:
    rclpy.init()
    node = RealPolicyGraspBackendNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
