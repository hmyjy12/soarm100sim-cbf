#!/usr/bin/env python3
"""Move the real arm to an approved pose before starting a learned policy."""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_srvs.srv import Trigger

from soarm100_interfaces.srv import MoveJointTarget


JOINT_ORDER = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)

TRAINING_LIMITS_RAD = (
    (-2.2, 2.2),
    (-3.14158, 0.2),
    (0.0, 3.14158),
    (-2.0, 1.8),
    (-1.45, 1.45),
    (-3.14158, 3.14158),
    (-0.2, 2.0),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pose", type=Path, required=True)
    parser.add_argument("--duration", type=float, default=6.0)
    parser.add_argument("--settle-seconds", type=float, default=0.75)
    parser.add_argument("--tolerance-rad", type=float, default=0.20)
    parser.add_argument("--training-margin-rad", type=float, default=0.10)
    parser.add_argument("--startup-timeout", type=float, default=10.0)
    args = parser.parse_args()
    if not 0.5 <= args.duration <= 30.0:
        parser.error("--duration must be within [0.5, 30] seconds")
    if not 0.2 <= args.settle_seconds <= 5.0:
        parser.error("--settle-seconds must be within [0.2, 5.0]")
    if not 0.01 <= args.tolerance_rad <= 0.30:
        parser.error("--tolerance-rad must be within [0.01, 0.30]")
    if not 0.0 <= args.training_margin_rad <= 0.30:
        parser.error("--training-margin-rad must be within [0, 0.30]")
    return args


def load_pose(path: Path, margin: float) -> list[float]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload.get("approved_for_recovery_motion", False):
        raise ValueError(f"pose is not approved_for_recovery_motion: {path}")
    if tuple(payload.get("policy_joint_order", ())) != JOINT_ORDER:
        raise ValueError("policy-ready pose joint order is not canonical")
    values = [float(value) for value in payload.get("policy_position_rad", ())]
    if len(values) != 7 or not all(math.isfinite(value) for value in values):
        raise ValueError("policy-ready pose must contain seven finite radians")
    violations = []
    for name, value, (low, high) in zip(JOINT_ORDER, values, TRAINING_LIMITS_RAD):
        inner_low = low + margin
        inner_high = high - margin
        if inner_low > inner_high or not inner_low <= value <= inner_high:
            violations.append(
                f"{name}={value:+.4f} outside interior "
                f"[{inner_low:+.4f},{inner_high:+.4f}]"
            )
    if violations:
        raise ValueError("; ".join(violations))
    return values


class PolicyPoseInitializer(Node):
    def __init__(self) -> None:
        super().__init__("policy_pose_initializer")
        self.current: dict[str, float] | None = None
        self.last_feedback_monotonic = 0.0
        self.create_subscription(JointState, "/joint_states", self._on_joint_state, 10)
        self.client = self.create_client(MoveJointTarget, "/hardware/move_joint_target")
        self.rollback_client = self.create_client(
            Trigger, "/hardware/return_to_startup_pose"
        )

    def _on_joint_state(self, msg: JointState) -> None:
        observed = dict(zip(msg.name, msg.position))
        if all(name in observed for name in JOINT_ORDER):
            self.current = {name: float(observed[name]) for name in JOINT_ORDER}
            self.last_feedback_monotonic = time.monotonic()

    def wait_ready(self, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        while rclpy.ok() and time.monotonic() < deadline:
            if self.client.wait_for_service(timeout_sec=0.1):
                rclpy.spin_once(self, timeout_sec=0.1)
                if self.current is not None:
                    return
        raise TimeoutError("hardware move service or /joint_states did not become ready")

    def return_to_startup_pose(self) -> None:
        print("[policy_init] initialization failed; returning to captured startup pose...")
        if not self.rollback_client.wait_for_service(timeout_sec=3.0):
            raise RuntimeError("INIT_ROLLBACK_UNAVAILABLE")
        future = self.rollback_client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(self, future, timeout_sec=25.0)
        response = future.result()
        if response is None:
            raise RuntimeError("INIT_ROLLBACK_TIMEOUT")
        if not response.success:
            raise RuntimeError(f"INIT_ROLLBACK_FAILED: {response.message}")
        print(f"[policy_init] INIT_ROLLBACK_SUCCESS: {response.message}")

    def move_and_verify(
        self,
        target: list[float],
        duration: float,
        settle_seconds: float,
        tolerance: float,
        training_margin: float,
    ) -> None:
        assert self.current is not None
        print("[policy_init] current -> ready pose (policy radians):")
        for name, goal in zip(JOINT_ORDER, target):
            now = self.current[name]
            print(f"  {name:28s} {now:+.4f} -> {goal:+.4f}  delta={goal-now:+.4f}")

        request = MoveJointTarget.Request()
        request.position_rad = target
        request.duration = duration
        request.confirmation = "MOVE_JOINT_TARGET"
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=duration + 20.0)
        response = future.result()
        if response is None:
            raise RuntimeError("INIT_SERVICE_TIMEOUT: no move service response")
        if not response.success:
            raise RuntimeError(f"INIT_MOVE_REJECTED: {response.reason}")

        stable_since: float | None = None
        deadline = time.monotonic() + max(3.0, settle_seconds + 2.0)
        last_errors: dict[str, float] = {}
        actual_range_violations: list[str] = []
        while rclpy.ok() and time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
            if self.current is None:
                continue
            last_errors = {
                name: self.current[name] - goal
                for name, goal in zip(JOINT_ORDER, target)
            }
            actual_range_violations = []
            for name, (low, high) in zip(JOINT_ORDER, TRAINING_LIMITS_RAD):
                value = self.current[name]
                if not low + training_margin <= value <= high - training_margin:
                    actual_range_violations.append(
                        f"{name}={value:+.4f} outside "
                        f"[{low + training_margin:+.4f},{high - training_margin:+.4f}]"
                    )
            within_target = max(abs(value) for value in last_errors.values()) <= tolerance
            if within_target and not actual_range_violations:
                if stable_since is None:
                    stable_since = time.monotonic()
                if time.monotonic() - stable_since >= settle_seconds:
                    print(
                        "[policy_init] INIT_SUCCESS max_error_rad="
                        f"{max(abs(value) for value in last_errors.values()):.4f}"
                    )
                    return
            else:
                stable_since = None
        details = ", ".join(f"{name}={value:+.4f}" for name, value in last_errors.items())
        range_detail = "; ".join(actual_range_violations)
        raise RuntimeError(
            f"INIT_NOT_CONVERGED: errors=[{details}]"
            + (f" training_range=[{range_detail}]" if range_detail else "")
        )


def main() -> None:
    args = parse_args()
    pose_path = args.pose.expanduser().resolve()
    target = load_pose(pose_path, args.training_margin_rad)
    rclpy.init()
    node = PolicyPoseInitializer()
    try:
        node.wait_ready(args.startup_timeout)
        try:
            node.move_and_verify(
                target,
                args.duration,
                args.settle_seconds,
                args.tolerance_rad,
                args.training_margin_rad,
            )
        except Exception as init_error:
            try:
                node.return_to_startup_pose()
            except Exception as rollback_error:
                raise RuntimeError(
                    f"{init_error}; rollback_error={rollback_error}"
                ) from init_error
            raise
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
