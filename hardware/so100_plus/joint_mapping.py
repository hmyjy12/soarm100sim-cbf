"""Convert calibrated LeRobot observations to SO-100 Plus policy radians."""

from __future__ import annotations

import json
import math
from pathlib import Path


MOTOR_ORDER = (
    "shoulder_pan",
    "shoulder_lift",
    "elbow_flex",
    "wrist_flex",
    "wrist_yaw",
    "wrist_roll",
    "gripper",
)


class PolicyJointMapping:
    def __init__(self, path: Path):
        self.path = path
        self.data = json.loads(path.read_text())
        joints = self.data.get("joints", {})
        if tuple(joints) != MOTOR_ORDER:
            raise ValueError(f"mapping joint order mismatch: {tuple(joints)}")
        if not self.data.get("approved_for_read_only_joint_state", False):
            raise ValueError("mapping is not approved for read-only joint state")
        for name, values in joints.items():
            if values.get("status") != "verified":
                raise ValueError(f"joint mapping is not verified: {name}")

    @property
    def policy_joint_names(self) -> tuple[str, ...]:
        return tuple(self.data["joints"][name]["policy_joint"] for name in MOTOR_ORDER)

    def convert(self, lerobot_values: dict[str, float]) -> dict[str, float]:
        if set(lerobot_values) != set(MOTOR_ORDER):
            raise ValueError("LeRobot observation does not contain exactly seven motors")

        result = {}
        for motor_name in MOTOR_ORDER:
            cfg = self.data["joints"][motor_name]
            if motor_name == "gripper":
                value = (
                    cfg["scale_rad_per_percent"] * float(lerobot_values[motor_name])
                    + cfg["zero_offset_rad"]
                )
                low, high = cfg["policy_clip_rad"]
                value = min(high, max(low, value))
            else:
                value = (
                    cfg["sign"] * math.radians(float(lerobot_values[motor_name]))
                    + cfg["zero_offset_rad"]
                )
            result[cfg["policy_joint"]] = value
        return result

