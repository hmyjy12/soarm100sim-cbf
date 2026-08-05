"""Canonical seven-motor mapping and hardware configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from lerobot.motors import Motor, MotorNormMode


MOTORS = {
    "shoulder_pan": Motor(1, "sts3215", MotorNormMode.DEGREES),
    "shoulder_lift": Motor(2, "sts3215", MotorNormMode.DEGREES),
    "elbow_flex": Motor(3, "sts3215", MotorNormMode.DEGREES),
    "wrist_flex": Motor(4, "sts3215", MotorNormMode.DEGREES),
    "wrist_yaw": Motor(5, "sts3215", MotorNormMode.DEGREES),
    "wrist_roll": Motor(6, "sts3215", MotorNormMode.DEGREES),
    "gripper": Motor(7, "sts3215", MotorNormMode.RANGE_0_100),
}

MOTOR_TO_POLICY_JOINT = {
    "shoulder_pan": "shoulder_rotation_joint",
    "shoulder_lift": "shoulder_pitch_joint",
    "elbow_flex": "ellbow_joint",
    "wrist_flex": "wrist_pitch_joint",
    "wrist_yaw": "wrist_jaw_joint",
    "wrist_roll": "wrist_roll_joint",
    "gripper": "gripper_joint",
}

# Limits from SO-ARM100/Simulation/SO100/mujoco/so100_plus.xml.
# They are model limits, not yet validated physical limits.
MUJOCO_LIMITS_RAD = {
    "shoulder_pan": (-2.2, 2.2),
    "shoulder_lift": (-3.14158, 0.2),
    "elbow_flex": (0.0, 3.14158),
    "wrist_flex": (-2.0, 1.8),
    "wrist_yaw": (-1.45, 1.45),
    "wrist_roll": (-3.14158, 3.14158),
    "gripper": (-0.2, 2.0),
}


@dataclass(frozen=True)
class MotorSafety:
    raw_min: int
    raw_max: int
    center_raw: int
    direction: int
    zero_offset_rad: float
    approved: bool = False

    def __post_init__(self) -> None:
        if self.raw_min >= self.raw_max:
            raise ValueError("raw_min must be below raw_max")
        if not self.raw_min <= self.center_raw <= self.raw_max:
            raise ValueError("center_raw must be inside the raw range")
        if self.direction not in (-1, 1):
            raise ValueError("direction must be -1 or +1")


@dataclass
class SO100PlusHardwareConfig:
    port: str = "/dev/ttyACM0"
    calibration_path: Path = Path("hardware/calibration/so100_plus_candidate.json")
    max_step_deg: float = 0.25
    max_test_delta_deg: float = 2.0
    command_hz: float = 20.0
    position_p_coefficient: int = 16
    position_i_coefficient: int = 0
    position_d_coefficient: int = 32
    gripper_max_torque_limit: int = 500
    gripper_protection_current: int = 250
    motor_safety: dict[str, MotorSafety] = field(default_factory=dict)

