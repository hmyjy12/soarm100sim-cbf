"""Explicitly approved pose-by-pose driver for real wrist hand-eye capture."""

from __future__ import annotations

import json
import math
from pathlib import Path

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from soarm100_interfaces.srv import MoveJointTarget


class WristHandeyePoseSequence(Node):
    def __init__(self) -> None:
        super().__init__("wrist_handeye_pose_sequence")
        repo_default = str(Path(__file__).resolve().parents[3])
        self.declare_parameter("repo_root", repo_default)
        self.declare_parameter(
            "pose_file", "hardware/calibration/handeye/wrist_handeye_poses.json"
        )
        self.declare_parameter(
            "seed_pose_file", "hardware/calibration/handeye/calibration_seed_pose.json"
        )
        self.declare_parameter("move_duration", 4.0)
        self.declare_parameter("seed_mode", "candidate")
        self.declare_parameter("live_auto_approve", False)
        repo = Path(str(self.get_parameter("repo_root").value)).resolve()
        pose_file = Path(str(self.get_parameter("pose_file").value))
        if not pose_file.is_absolute():
            pose_file = repo / pose_file
        self.pose_file = pose_file.resolve()
        self.payload = json.loads(self.pose_file.read_text(encoding="utf-8"))
        seed_file = Path(str(self.get_parameter("seed_pose_file").value))
        if not seed_file.is_absolute():
            seed_file = repo / seed_file
        self.seed_payload = None
        if str(self.get_parameter("seed_mode").value).strip().lower() != "live":
            self.seed_payload = json.loads(seed_file.resolve().read_text(encoding="utf-8"))
        self.joint_order = tuple(self.payload["joint_order"])
        if len(self.joint_order) != 7:
            raise ValueError("pose sequence must contain seven joints")
        self.poses = list(self.payload["poses"])
        self.joint_limits = (
            (-2.2, 2.2), (-3.14158, 0.2), (0.0, 3.14158),
            (-2.0, 1.8), (-1.45, 1.45), (-3.14158, 3.14158), (-0.2, 2.0),
        )
        self.current: dict[str, float] | None = None
        self.reference: list[float] | None = None
        self.create_subscription(JointState, "/joint_states", self._on_joint_state, 10)
        self.client = self.create_client(MoveJointTarget, "/hardware/move_joint_target")

    def _on_joint_state(self, msg: JointState) -> None:
        values = dict(zip(msg.name, msg.position))
        if all(name in values for name in self.joint_order):
            self.current = {name: float(values[name]) for name in self.joint_order}

    def wait_ready(self) -> None:
        self.get_logger().info(f"pose sequence={self.pose_file} poses={len(self.poses)}")
        while rclpy.ok() and not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for /hardware/move_joint_target")
        while rclpy.ok() and self.current is None:
            rclpy.spin_once(self, timeout_sec=0.2)
            self.get_logger().info("waiting for /joint_states", throttle_duration_sec=2.0)

    def run(self) -> None:
        self.wait_ready()
        assert self.current is not None
        live_reference = [self.current[name] for name in self.joint_order]
        print("\nLive /joint_states startup pose:")
        for name, value in zip(self.joint_order, live_reference):
            print(f"  {name:28s} {value:+.4f} rad")
        reference_violations = [
            f"{name}={value:+.4f} outside [{low:+.4f},{high:+.4f}]"
            for name, value, (low, high) in zip(
                self.joint_order, live_reference, self.joint_limits
            )
            if not low <= value <= high
        ]
        if reference_violations:
            print("ABORTED: live startup pose is outside the valid policy limits:")
            for violation in reference_violations:
                print(f"  {violation}")
            print("Recover to an approved hardware_safe pose before starting this sequence.")
            return
        seed_mode = str(self.get_parameter("seed_mode").value).strip().lower()
        if seed_mode == "live":
            self.reference = list(live_reference)
            print("\nUsing the manually positioned live pose as the hand-eye seed.")
            for name, value in zip(self.joint_order, self.reference):
                print(f"  {name:28s} {value:+.4f} rad")
            if bool(self.get_parameter("live_auto_approve").value):
                print("LIVE SEED APPROVED by the SPACE confirmation in the launcher.")
            else:
                print("\nFIRST APPROVAL: this confirms the manually positioned startup pose.")
                print("Type APPROVE exactly, or type q to abort. Do not type MOVE here.")
                if input("Approval: ").strip() != "APPROVE":
                    print("ABORTED: live hand-eye seed was not approved.")
                    return
                print("LIVE SEED APPROVED. No seed motion was commanded.")
        else:
            if self.seed_payload is None:
                raise RuntimeError("candidate seed mode requires a valid seed pose file")
            seed = [float(value) for value in self.seed_payload["policy_position_rad"]]
            seed_deltas = [math.degrees(goal - now) for goal, now in zip(seed, live_reference)]
            print("\nCalibration seed candidate:")
            for name, value, delta in zip(self.joint_order, seed, seed_deltas):
                print(f"  {name:28s} target={value:+.4f} rad  delta={delta:+.1f} deg")
            if input("Type MOVE_SEED to approve this candidate, or q to abort: ").strip() != "MOVE_SEED":
                print("ABORTED: calibration seed was not approved.")
                return
            request = MoveJointTarget.Request()
            request.position_rad = seed
            request.duration = float(self.get_parameter("move_duration").value)
            request.confirmation = "MOVE_JOINT_TARGET"
            future = self.client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            response = future.result()
            if response is None or not response.success:
                print("SEED MOVE FAILED: " + ("no response" if response is None else response.reason))
                return
            rclpy.spin_once(self, timeout_sec=0.5)
            self.reference = list(seed)
            print("SEED MOVE SUCCEEDED.")
            print("Confirm that the FULL tabletop checkerboard is visible and stable in the Viewer.")
            if input("Type START to use this seed as the sequence center, or anything else to abort: ").strip() != "START":
                print("ABORTED: reposition the board/camera view before starting the sequence.")
                return
        if seed_mode == "live":
            print("Confirm that the FULL tabletop checkerboard remains visible and stable in the Viewer.")
        for index, pose in enumerate(self.poses):
            if not rclpy.ok():
                break
            rclpy.spin_once(self, timeout_sec=0.1)
            offsets = [float(value) for value in pose["offset_rad"]]
            target = [value + offset for value, offset in zip(self.reference, offsets)]
            if len(target) != 7 or not all(math.isfinite(value) for value in target):
                raise ValueError(f"invalid pose {pose}")
            violations = [
                f"{name}={value:+.3f} outside [{low:+.3f},{high:+.3f}]"
                for name, value, (low, high) in zip(self.joint_order, target, self.joint_limits)
                if not low <= value <= high
            ]
            if violations:
                print(f"SKIPPED {pose['name']}: " + "; ".join(violations))
                continue
            current = self.current or dict(zip(self.joint_order, target))
            deltas_deg = [
                math.degrees(value - current[name])
                for name, value in zip(self.joint_order, target)
            ]
            print("\n" + "=" * 72)
            print(f"Candidate {index + 1}/{len(self.poses)}: {pose['name']}")
            print(
                "CAPTURE RECOMMENDED" if bool(pose.get("capture_recommended"))
                else "TRANSITION ONLY - do not capture this repeated center pose"
            )
            print("This pose is limit-checked but NOT collision-certified.")
            for name, value, delta in zip(self.joint_order, target, deltas_deg):
                print(f"  {name:28s} target={value:+.4f} rad  delta={delta:+.1f} deg")
            print("Inspect the real arm, table, camera cable and surrounding workspace.")
            decision = input("Press m=move, q=quit: ").strip().lower()
            if decision == "q":
                break
            if decision != "m":
                print("Invalid input; enter m to move or q to quit.")
                continue
            request = MoveJointTarget.Request()
            request.position_rad = target
            request.duration = float(self.get_parameter("move_duration").value)
            request.confirmation = "MOVE_JOINT_TARGET"
            future = self.client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            response = future.result()
            if response is None or not response.success:
                reason = "no response" if response is None else response.reason
                print(f"MOVE FAILED: {reason}")
                continue
            rclpy.spin_once(self, timeout_sec=0.2)
            self.current = dict(zip(self.joint_order, target))
            print(f"MOVE SUCCEEDED: {pose['name']}")
            print("Check the calibration Viewer. Press SPACE there only when the board is detected and stable.")
            input("After capture (or deciding to reject this view), press ENTER for the next candidate: ")


def main() -> None:
    rclpy.init()
    node = WristHandeyePoseSequence()
    try:
        node.run()
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
