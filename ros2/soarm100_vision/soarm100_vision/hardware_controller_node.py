"""ROS2 proxy for the persistent LeRobot seven-axis hardware controller."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
import queue
import signal
import subprocess
import threading
import time
import uuid

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from soarm100_interfaces.srv import MoveJointTarget, SetHardwareTorque


class HardwareControllerNode(Node):
    def __init__(self) -> None:
        super().__init__("so100_plus_hardware_controller")
        repo_default = str(Path(__file__).resolve().parents[3])
        self.declare_parameter("repo_root", repo_default)
        self.declare_parameter("port", "/dev/ttyACM0")
        self.declare_parameter("lerobot_env", "lerobot")
        self.declare_parameter(
            "calibration_file",
            "hardware/calibration/lerobot/so100_plus_new_arm.json",
        )
        self.declare_parameter("shoulder_lift_p", 16)
        self.declare_parameter("feedback_rate_hz", 20.0)
        self.declare_parameter("driver_rate_hz", 20.0)
        self.declare_parameter("max_stream_command_delta_rad", 0.25)
        self.declare_parameter("command_timeout", 20.0)
        self._command_lock = threading.Lock()
        self._responses: queue.Queue[dict] = queue.Queue()
        self._driver_log_path = ""
        self._process = self._start_driver()
        self._reader = threading.Thread(target=self._read_output, daemon=True)
        self._reader.start()
        ready = self._wait_message("", event="ready", timeout=10.0)
        if not ready.get("success"):
            raise RuntimeError(f"hardware driver failed to start: {ready}")
        self._move_service = self.create_service(
            MoveJointTarget, "/hardware/move_joint_target", self._handle_move
        )
        self._torque_service = self.create_service(
            SetHardwareTorque, "/hardware/set_torque", self._handle_torque
        )
        self._joint_pub = self.create_publisher(JointState, "/joint_states", 10)
        self._stream_target_sub = self.create_subscription(
            JointState,
            "/hardware/joint_target",
            self._on_stream_target,
            1,
        )
        feedback_rate = float(self.get_parameter("feedback_rate_hz").value)
        if not 10.0 <= feedback_rate <= 30.0:
            raise ValueError("feedback_rate_hz must be within [10, 30]")
        self.create_timer(1.0 / feedback_rate, self._publish_joint_state)
        self.get_logger().info(
            "hardware controller ready; current seven-axis position is powered "
            "and held; services=/hardware/move_joint_target,/hardware/set_torque "
            "stream_topic=/hardware/joint_target"
        )

    @staticmethod
    def _joint_names() -> tuple[str, ...]:
        return (
            "shoulder_rotation_joint",
            "shoulder_pitch_joint",
            "ellbow_joint",
            "wrist_pitch_joint",
            "wrist_jaw_joint",
            "wrist_roll_joint",
            "gripper_joint",
        )

    def _on_stream_target(self, msg: JointState) -> None:
        names = self._joint_names()
        if tuple(msg.name) != names or len(msg.position) != len(names):
            self.get_logger().error(
                "rejected /hardware/joint_target: expected the canonical seven-joint order",
                throttle_duration_sec=2.0,
            )
            return
        values = [float(value) for value in msg.position]
        if not all(math.isfinite(value) for value in values):
            self.get_logger().error(
                "rejected /hardware/joint_target: non-finite command",
                throttle_duration_sec=2.0,
            )
            return
        with self._command_lock:
            result = self._request("stream", position_rad=values)
        if not result.get("success"):
            self.get_logger().error(
                f"stream target rejected: {result.get('reason', 'unknown hardware failure')}",
                throttle_duration_sec=1.0,
            )

    def _start_driver(self) -> subprocess.Popen:
        repo = Path(str(self.get_parameter("repo_root").value)).resolve()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self._driver_log_path = str(
            repo / "logs/hardware" / f"controller_{timestamp}.jsonl"
        )
        command = [
            "conda", "run", "--no-capture-output", "-n",
            str(self.get_parameter("lerobot_env").value),
            "python", str(repo / "hardware/tools/run_hardware_controller.py"),
            "--port", str(self.get_parameter("port").value),
            "--calibration",
            str(repo / str(self.get_parameter("calibration_file").value)),
            "--mapping",
            str(repo / "hardware/calibration/policy_joint_mapping.json"),
            "--safe-pose",
            str(repo / "hardware/calibration/hardware_safe_pose.json"),
            "--shoulder-lift-p",
            str(int(self.get_parameter("shoulder_lift_p").value)),
            "--rate",
            str(float(self.get_parameter("driver_rate_hz").value)),
            "--max-stream-command-delta-rad",
            str(float(self.get_parameter("max_stream_command_delta_rad").value)),
            "--log",
            self._driver_log_path,
        ]
        return subprocess.Popen(
            command,
            cwd=repo,
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            start_new_session=True,
        )

    def _read_output(self) -> None:
        assert self._process.stdout is not None
        for line in self._process.stdout:
            try:
                self._responses.put(json.loads(line))
            except json.JSONDecodeError:
                self.get_logger().warning(f"hardware driver output: {line.rstrip()}")
        returncode = self._process.poll()
        self.get_logger().error(
            f"hardware driver exited unexpectedly, returncode={returncode}"
        )
        self._responses.put(
            {
                "event": "process_exit",
                "success": False,
                "reason": f"driver exited returncode={returncode}",
            }
        )

    def _wait_message(
        self, request_id: str, *, event: str | None = None, timeout: float
    ) -> dict:
        deadline = time.monotonic() + timeout
        deferred = []
        try:
            while time.monotonic() < deadline:
                message = self._responses.get(
                    timeout=max(0.01, deadline - time.monotonic())
                )
                if (
                    event is not None and message.get("event") == event
                ) or (
                    event is None and message.get("request_id") == request_id
                ):
                    return message
                if message.get("event") in ("fatal", "process_exit"):
                    return message
                deferred.append(message)
        except queue.Empty:
            pass
        finally:
            for message in deferred:
                self._responses.put(message)
        return {"success": False, "reason": "hardware driver response timeout"}

    def _request(self, action: str, **values) -> dict:
        if self._process.poll() is not None:
            return {"success": False, "reason": "hardware driver is not running"}
        request_id = uuid.uuid4().hex
        payload = {"request_id": request_id, "action": action, **values}
        assert self._process.stdin is not None
        self._process.stdin.write(json.dumps(payload) + "\n")
        self._process.stdin.flush()
        return self._wait_message(
            request_id,
            timeout=float(self.get_parameter("command_timeout").value),
        )

    def _handle_move(
        self, request: MoveJointTarget.Request, response: MoveJointTarget.Response
    ) -> MoveJointTarget.Response:
        if request.confirmation != "MOVE_JOINT_TARGET":
            response.reason = "confirmation must be exactly MOVE_JOINT_TARGET"
            return response
        with self._command_lock:
            result = self._request(
                "move",
                position_rad=[float(value) for value in request.position_rad],
                duration=float(request.duration),
            )
        response.success = bool(result.get("success"))
        response.reason = (
            "target reached and actively held"
            if response.success
            else str(result.get("reason", "unknown hardware failure"))
        )
        response.log_path = self._driver_log_path
        return response

    def _publish_joint_state(self) -> None:
        if not self._command_lock.acquire(blocking=False):
            return
        try:
            result = self._request("status")
        finally:
            self._command_lock.release()
        if not result.get("success"):
            self.get_logger().warning(
                f"hardware feedback unavailable: {result.get('reason')}",
                throttle_duration_sec=3.0,
            )
            return
        policy = result.get("policy", {})
        names = self._joint_names()
        if set(policy) != set(names):
            return
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(names)
        msg.position = [float(policy[name]) for name in names]
        self._joint_pub.publish(msg)

    def _handle_torque(
        self,
        request: SetHardwareTorque.Request,
        response: SetHardwareTorque.Response,
    ) -> SetHardwareTorque.Response:
        if request.confirmation != "SET_HARDWARE_TORQUE":
            response.reason = "confirmation must be exactly SET_HARDWARE_TORQUE"
            return response
        if request.enabled:
            response.reason = (
                "re-enable is intentionally unavailable after torque-off; "
                "restart the controller to seed current goals before power-on"
            )
            return response
        with self._command_lock:
            result = self._request("disable")
        response.success = bool(result.get("success"))
        response.reason = str(result.get("reason", "all torque disabled"))
        return response

    def destroy_node(self) -> bool:
        if hasattr(self, "_process") and self._process.poll() is None:
            try:
                with self._command_lock:
                    self._request("disable")
            except Exception:
                pass
            os.killpg(self._process.pid, signal.SIGTERM)
            try:
                self._process.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                os.killpg(self._process.pid, signal.SIGKILL)
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = HardwareControllerNode()
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
