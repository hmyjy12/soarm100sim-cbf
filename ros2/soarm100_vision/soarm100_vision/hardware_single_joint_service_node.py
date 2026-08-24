"""ROS2 service wrapper for the guarded single-joint hardware test."""

from __future__ import annotations

import math
import os
from pathlib import Path
import signal
import subprocess
import threading
from datetime import datetime

import rclpy
from rclpy.node import Node
from soarm100_interfaces.srv import (
    MoveJointDelta,
    MoveNamedPose,
    MoveSingleJoint,
)


MOTOR_NAMES = (
    "shoulder_pan",
    "shoulder_lift",
    "elbow_flex",
    "wrist_flex",
    "wrist_yaw",
    "wrist_roll",
    "gripper",
)
CONFIRMATION = "MOVE_SINGLE_JOINT"


class HardwareSingleJointServiceNode(Node):
    def __init__(self) -> None:
        super().__init__("so100_plus_single_joint_service")
        repo_default = str(Path(__file__).resolve().parents[3])
        self.declare_parameter("repo_root", repo_default)
        self.declare_parameter("port", "/dev/ttyACM0")
        self.declare_parameter("lerobot_env", "lerobot")
        self.declare_parameter("max_delta_deg", 2.0)
        self.declare_parameter("command_timeout", 20.0)
        self._busy_lock = threading.Lock()
        self._service = self.create_service(
            MoveSingleJoint, "/hardware/move_single_joint", self._handle
        )
        self._multi_service = self.create_service(
            MoveJointDelta, "/hardware/move_joint_delta", self._handle_multi
        )
        self._named_pose_service = self.create_service(
            MoveNamedPose, "/hardware/move_named_pose", self._handle_named_pose
        )
        self.get_logger().info(
            "guarded single-joint service ready: /hardware/move_single_joint; "
            "/hardware/move_joint_delta; /hardware/move_named_pose"
        )

    def _handle_named_pose(
        self,
        request: MoveNamedPose.Request,
        response: MoveNamedPose.Response,
    ) -> MoveNamedPose.Response:
        if request.pose_name != "hardware_safe":
            response.reason = "only the approved pose hardware_safe is available"
            return response
        if request.confirmation != "MOVE_NAMED_POSE":
            response.reason = "confirmation must be exactly MOVE_NAMED_POSE"
            return response
        if not math.isfinite(request.duration) or request.duration < 1.0:
            response.reason = "duration must be finite and at least 1.0s"
            return response
        if not math.isfinite(request.hold) or not 0.0 <= request.hold <= 5.0:
            response.reason = "hold must be finite and within [0, 5]s"
            return response
        if not self._busy_lock.acquire(blocking=False):
            response.reason = "hardware command already in progress"
            return response
        try:
            port_users = self._port_users()
            if port_users:
                response.reason = (
                    f"serial port is already in use ({port_users}); stop all "
                    "other hardware readers first"
                )
                return response
            repo = Path(str(self.get_parameter("repo_root").value)).resolve()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            log_path = (
                repo / "log/runtime/hardware" / f"ros2_named_pose_{timestamp}.jsonl"
            )
            command = [
                "conda", "run", "--no-capture-output", "-n",
                str(self.get_parameter("lerobot_env").value),
                "python", str(repo / "hardware/tools/move_to_named_pose.py"),
                "--port", str(self.get_parameter("port").value),
                "--calibration",
                str(repo / "hardware/calibration/lerobot/so100_plus_7dof.json"),
                "--mapping",
                str(repo / "hardware/calibration/policy_joint_mapping.json"),
                "--pose",
                str(repo / "hardware/calibration/hardware_safe_pose.json"),
                "--duration", f"{request.duration:.8g}",
                "--hold", f"{request.hold:.8g}",
                "--log", str(log_path),
                "--confirm", "MOVE_NAMED_POSE",
            ]
            response.log_path = str(log_path)
            self.get_logger().warning(
                f"moving to approved named pose {request.pose_name}"
            )
            process = subprocess.Popen(
                command,
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                output, _ = process.communicate(
                    timeout=float(self.get_parameter("command_timeout").value)
                )
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    output, _ = process.communicate(timeout=3.0)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    output, _ = process.communicate()
                response.reason = "named-pose motion timeout; process group terminated"
                return response
            response.success = process.returncode == 0
            if response.success:
                response.reason = (
                    "approved hardware_safe pose reached; all torque disabled"
                )
                self.get_logger().info(response.reason)
            else:
                response.reason = (
                    f"named-pose motion failed rc={process.returncode}: "
                    f"{output.strip()[-1200:]}"
                )
                self.get_logger().error(response.reason)
        except Exception as exc:
            response.reason = f"service execution failed: {exc}"
            self.get_logger().error(response.reason)
        finally:
            self._busy_lock.release()
        return response

    def _port_users(self) -> str:
        return subprocess.run(
            ["fuser", str(self.get_parameter("port").value)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        ).stdout.strip()

    def _handle(
        self,
        request: MoveSingleJoint.Request,
        response: MoveSingleJoint.Response,
    ) -> MoveSingleJoint.Response:
        reason = self._validate(request)
        if reason:
            response.success = False
            response.reason = reason
            return response
        if not self._busy_lock.acquire(blocking=False):
            response.success = False
            response.reason = "hardware command already in progress"
            return response

        try:
            repo = Path(str(self.get_parameter("repo_root").value)).resolve()
            port = str(self.get_parameter("port").value)
            port_users = self._port_users()
            if port_users:
                response.success = False
                response.reason = (
                    f"serial port is already in use ({port_users}); stop "
                    "run_hardware_state.sh and other serial readers first"
                )
                self.get_logger().error(response.reason)
                return response
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            log_path = (
                repo
                / "log/runtime/hardware"
                / f"ros2_single_joint_{request.joint}_{timestamp}.jsonl"
            )
            command = [
                "conda",
                "run",
                "--no-capture-output",
                "-n",
                str(self.get_parameter("lerobot_env").value),
                "python",
                str(repo / "hardware/tools/test_single_joint.py"),
                "--port",
                port,
                "--calibration",
                str(
                    repo
                    / "hardware/calibration/lerobot/so100_plus_7dof.json"
                ),
                "--joint",
                request.joint,
                "--delta-deg",
                f"{request.delta_deg:.8g}",
                "--duration",
                f"{request.duration:.8g}",
                "--hold",
                f"{request.hold:.8g}",
                "--log",
                str(log_path),
                "--confirm",
                CONFIRMATION,
            ]
            self.get_logger().warning(
                f"executing guarded motion joint={request.joint} "
                f"delta={request.delta_deg:+.2f}deg"
            )
            process = subprocess.Popen(
                command,
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                output, _ = process.communicate(
                    timeout=float(self.get_parameter("command_timeout").value)
                )
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    output, _ = process.communicate(timeout=3.0)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    output, _ = process.communicate()
                response.success = False
                response.reason = (
                    "guarded motion timeout; sent SIGTERM to the complete process "
                    "group so the hardware finally block disables torque"
                )
                self.get_logger().error(response.reason)
                return response

            response.log_path = str(log_path)
            response.success = process.returncode == 0
            output = output.strip()
            if response.success:
                response.reason = "completed_and_returned; selected torque disabled"
                self.get_logger().info(response.reason)
            else:
                tail = output[-1200:] if output else "no subprocess output"
                response.reason = (
                    f"guarded motion failed rc={process.returncode}: {tail}"
                )
                self.get_logger().error(response.reason)
        except Exception as exc:
            response.success = False
            response.reason = f"service execution failed: {exc}"
            self.get_logger().error(response.reason)
        finally:
            self._busy_lock.release()
        return response

    def _handle_multi(
        self,
        request: MoveJointDelta.Request,
        response: MoveJointDelta.Response,
    ) -> MoveJointDelta.Response:
        if request.confirmation != "MOVE_MULTI_JOINT":
            response.reason = "confirmation must be exactly MOVE_MULTI_JOINT"
            return response
        deltas = [float(value) for value in request.delta_rad]
        active = [value for value in deltas if abs(value) > 1.0e-9]
        max_delta = math.radians(2.0)
        if not active or len(active) > 2:
            response.reason = "exactly one or two non-zero deltas are required"
            return response
        if not all(
            math.isfinite(v) and abs(v) <= max_delta + 1.0e-6
            for v in active
        ):
            response.reason = "each active delta must be finite and within +/-2deg"
            return response
        if not math.isfinite(request.duration) or request.duration < 1.0:
            response.reason = "duration must be finite and at least 1.0s"
            return response
        if not math.isfinite(request.hold) or not 0.0 <= request.hold <= 5.0:
            response.reason = "hold must be finite and within [0, 5]s"
            return response
        if not self._busy_lock.acquire(blocking=False):
            response.reason = "hardware command already in progress"
            return response

        try:
            port_users = self._port_users()
            if port_users:
                response.reason = (
                    f"serial port is already in use ({port_users}); stop all "
                    "other hardware readers first"
                )
                return response
            repo = Path(str(self.get_parameter("repo_root").value)).resolve()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            log_path = (
                repo / "log/runtime/hardware" / f"ros2_multi_joint_{timestamp}.jsonl"
            )
            command = [
                "conda", "run", "--no-capture-output", "-n",
                str(self.get_parameter("lerobot_env").value),
                "python", str(repo / "hardware/tools/test_multi_joint_delta.py"),
                "--port", str(self.get_parameter("port").value),
                "--calibration",
                str(repo / "hardware/calibration/lerobot/so100_plus_7dof.json"),
                "--mapping",
                str(repo / "hardware/calibration/policy_joint_mapping.json"),
                "--deltas-rad", ",".join(f"{value:.10g}" for value in deltas),
                "--duration", f"{request.duration:.8g}",
                "--hold", f"{request.hold:.8g}",
                "--log", str(log_path),
                "--confirm", "MOVE_MULTI_JOINT",
            ]
            if request.keep_target:
                command.append("--keep-target")
            response.log_path = str(log_path)
            self.get_logger().warning(
                f"executing guarded synchronized motion delta_rad={deltas}"
            )
            process = subprocess.Popen(
                command,
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                output, _ = process.communicate(
                    timeout=float(self.get_parameter("command_timeout").value)
                )
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    output, _ = process.communicate(timeout=3.0)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    output, _ = process.communicate()
                response.reason = (
                    "synchronized motion timeout; process group terminated"
                )
                return response
            response.success = process.returncode == 0
            if response.success:
                response.reason = (
                    "synchronized motion converged, "
                    + ("target retained" if request.keep_target else "returned")
                    + ", all torque disabled"
                )
                self.get_logger().info(response.reason)
            else:
                response.reason = (
                    f"synchronized motion failed rc={process.returncode}: "
                    f"{output.strip()[-1200:]}"
                )
                self.get_logger().error(response.reason)
        except Exception as exc:
            response.reason = f"service execution failed: {exc}"
            self.get_logger().error(response.reason)
        finally:
            self._busy_lock.release()
        return response

    def _validate(self, request: MoveSingleJoint.Request) -> str:
        if request.confirmation != CONFIRMATION:
            return f"confirmation must be exactly {CONFIRMATION}"
        if request.joint not in MOTOR_NAMES:
            return f"unknown joint {request.joint!r}"
        max_delta = float(self.get_parameter("max_delta_deg").value)
        if not math.isfinite(request.delta_deg):
            return "delta_deg must be finite"
        if request.delta_deg == 0.0 or abs(request.delta_deg) > max_delta:
            return f"delta_deg must be non-zero and within +/-{max_delta:g}"
        if not math.isfinite(request.duration) or request.duration < 0.5:
            return "duration must be finite and at least 0.5 seconds"
        if not math.isfinite(request.hold) or not 0.0 <= request.hold <= 5.0:
            return "hold must be finite and within [0, 5] seconds"
        return ""


def main() -> None:
    rclpy.init()
    node = HardwareSingleJointServiceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
