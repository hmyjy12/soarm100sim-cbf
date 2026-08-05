#!/usr/bin/env python3
"""Read the hardware pose corresponding to policy home without writing motors."""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors import MotorCalibration
from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTOR_TO_POLICY_JOINT, MOTORS


POLICY_HOME_RAD = {
    "shoulder_pan": 0.0,
    "shoulder_lift": -math.pi / 2,
    "elbow_flex": math.pi / 2,
    "wrist_flex": 0.0,
    "wrist_yaw": 0.0,
    "wrist_roll": 0.0,
    "gripper": 0.0,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--calibration",
        type=Path,
        default=Path("hardware/calibration/lerobot/so100_plus_7dof.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("hardware/calibration/policy_home_capture.json"),
    )
    return parser.parse_args()


def load_calibration(path: Path) -> dict[str, MotorCalibration]:
    raw = json.loads(path.read_text())
    if set(raw) != set(MOTORS):
        raise ValueError("calibration does not contain the expected seven motors")
    return {name: MotorCalibration(**values) for name, values in raw.items()}


def main() -> int:
    args = parse_args()
    calibration = load_calibration(args.calibration)
    bus = FeetechMotorsBus(args.port, MOTORS, calibration)
    try:
        print("[capture_policy_home] STRICT_READ_ONLY: no motor register will be written")
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=2)
        enabled = [name for name, value in torque.items() if int(value) != 0]
        if enabled:
            raise RuntimeError(f"refusing capture because torque is enabled: {enabled}")

        raw = bus.sync_read("Present_Position", normalize=False, num_retry=3)
        normalized = bus.sync_read("Present_Position", normalize=True, num_retry=3)
        motors = {}
        for name in MOTORS:
            motors[name] = {
                "id": MOTORS[name].id,
                "policy_joint": MOTOR_TO_POLICY_JOINT[name],
                "raw_position": int(raw[name]),
                "lerobot_value": float(normalized[name]),
                "lerobot_unit": "percent" if name == "gripper" else "degree",
                "policy_home_rad": POLICY_HOME_RAD[name],
                "policy_sign": None,
                "policy_zero_offset_rad": None,
            }
            print(
                f"{name:15s} raw={int(raw[name]):4d} "
                f"lerobot={float(normalized[name]):+8.3f} "
                f"policy_home={POLICY_HOME_RAD[name]:+8.4f}rad"
            )

        result = {
            "schema_version": 1,
            "timestamp": datetime.now().astimezone().isoformat(),
            "mode": "STRICT_READ_ONLY",
            "reference_pose": "policy_home",
            "policy_joint_order": list(MOTOR_TO_POLICY_JOINT.values()),
            "approved": False,
            "motors": motors,
            "notes": [
                "The arm was manually aligned to MuJoCo policy HOME_QPOS.",
                "Signs must be confirmed before zero offsets are computed.",
                "Gripper uses LeRobot range percent rather than motor degrees.",
            ],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n")
        print(f"[capture_policy_home] saved: {args.output.resolve()}")
        return 0
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    raise SystemExit(main())
