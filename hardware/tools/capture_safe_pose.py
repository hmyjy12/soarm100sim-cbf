#!/usr/bin/env python3
"""Capture and validate a candidate hardware-safe pose without motor writes."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors import MotorCalibration
from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTORS, MUJOCO_LIMITS_RAD
from hardware.so100_plus.joint_mapping import MOTOR_ORDER, PolicyJointMapping


RAW_MARGIN = 100


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--calibration",
        type=Path,
        default=Path("hardware/calibration/lerobot/so100_plus_7dof.json"),
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=Path("hardware/calibration/policy_joint_mapping.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "hardware/calibration/hardware_safe_pose_candidate.json"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    calibration_raw = json.loads(args.calibration.read_text())
    calibration = {
        name: MotorCalibration(**calibration_raw[name]) for name in MOTOR_ORDER
    }
    mapping = PolicyJointMapping(args.mapping)
    bus = FeetechMotorsBus(args.port, MOTORS, calibration)
    try:
        print("[capture_safe_pose] STRICT_READ_ONLY: no motor register will be written")
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=3)
        enabled = [name for name, value in torque.items() if int(value) != 0]
        if enabled:
            raise RuntimeError(
                f"refusing safe-pose capture because torque is enabled: {enabled}"
            )

        raw = bus.sync_read("Present_Position", normalize=False, num_retry=3)
        normalized = bus.sync_read(
            "Present_Position", normalize=True, num_retry=3
        )
        policy = mapping.convert(
            {name: float(normalized[name]) for name in MOTOR_ORDER}
        )

        raw_checks = {}
        policy_checks = {}
        failures = []
        for motor in MOTOR_ORDER:
            joint = mapping.data["joints"][motor]["policy_joint"]
            raw_low = calibration[motor].range_min + RAW_MARGIN
            raw_high = calibration[motor].range_max - RAW_MARGIN
            raw_ok = raw_low <= int(raw[motor]) <= raw_high
            raw_checks[motor] = {
                "position": int(raw[motor]),
                "safe_min": raw_low,
                "safe_max": raw_high,
                "passed": raw_ok,
            }
            policy_low, policy_high = MUJOCO_LIMITS_RAD[motor]
            policy_ok = policy_low <= policy[joint] <= policy_high
            policy_checks[joint] = {
                "position_rad": policy[joint],
                "min_rad": policy_low,
                "max_rad": policy_high,
                "passed": policy_ok,
            }
            if not raw_ok:
                failures.append(f"{motor}:raw_margin")
            if not policy_ok:
                failures.append(f"{joint}:policy_limit")

        result = {
            "schema_version": 1,
            "timestamp": datetime.now().astimezone().isoformat(),
            "name": "hardware_safe",
            "mode": "STRICT_READ_ONLY",
            "policy_joint_order": list(mapping.policy_joint_names),
            "policy_position_rad": [
                policy[name] for name in mapping.policy_joint_names
            ],
            "policy_position_by_name": policy,
            "motor_raw_position": {
                name: int(raw[name]) for name in MOTOR_ORDER
            },
            "motor_lerobot_value": {
                name: float(normalized[name]) for name in MOTOR_ORDER
            },
            "raw_margin_counts": RAW_MARGIN,
            "raw_checks": raw_checks,
            "policy_checks": policy_checks,
            "automatic_validation_passed": not failures,
            "automatic_validation_failures": failures,
            "user_visual_approval": False,
            "approved_for_recovery_motion": False,
            "manual_checks_required": [
                "arm is mechanically stable after torque is disabled",
                "wrist_roll cable is relaxed with margin in both directions",
                "arm, camera, and gripper do not contact the table or robot",
                "camera mounts and cables are not under tension",
            ],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2, ensure_ascii=True) + "\n"
        )

        print("[capture_safe_pose] policy radians:")
        for joint in mapping.policy_joint_names:
            status = "OK" if policy_checks[joint]["passed"] else "FAIL"
            print(f"  {joint:28s} {policy[joint]:+8.4f}  {status}")
        print("[capture_safe_pose] raw margins:")
        for motor in MOTOR_ORDER:
            check = raw_checks[motor]
            status = "OK" if check["passed"] else "FAIL"
            print(
                f"  {motor:15s} {check['position']:4d} "
                f"[{check['safe_min']:4d}, {check['safe_max']:4d}] {status}"
            )
        print(
            f"[capture_safe_pose] automatic_validation_passed={not failures}"
        )
        print(f"[capture_safe_pose] saved candidate: {args.output.resolve()}")
        if failures:
            raise RuntimeError(
                f"candidate failed automatic validation: {failures}"
            )
        return 0
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    raise SystemExit(main())
