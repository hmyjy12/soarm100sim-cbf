"""Validation helpers for the read-only Feetech-to-ROS2 UDP bridge."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass


EXPECTED_SOURCE = "so100_plus_feetech_read_only"
JOINT_NAMES = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)


@dataclass(frozen=True)
class HardwareJointPacket:
    sequence: int
    source_timestamp: str
    positions: tuple[float, ...]


def decode_hardware_joint_packet(payload: bytes) -> HardwareJointPacket:
    """Decode one packet and reject incomplete or non-finite joint states."""
    try:
        packet = json.loads(payload.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON packet: {exc}") from exc

    if packet.get("schema_version") != 1:
        raise ValueError("unsupported schema_version")
    if packet.get("source") != EXPECTED_SOURCE:
        raise ValueError("unexpected packet source")

    sequence = packet.get("sequence")
    if not isinstance(sequence, int) or sequence < 0:
        raise ValueError("sequence must be a non-negative integer")

    policy = packet.get("policy")
    if not isinstance(policy, dict) or set(policy) != set(JOINT_NAMES):
        raise ValueError("packet does not contain exactly the seven policy joints")

    positions = tuple(float(policy[name]) for name in JOINT_NAMES)
    if not all(math.isfinite(value) for value in positions):
        raise ValueError("joint positions must be finite")

    return HardwareJointPacket(
        sequence=sequence,
        source_timestamp=str(packet.get("timestamp", "")),
        positions=positions,
    )
