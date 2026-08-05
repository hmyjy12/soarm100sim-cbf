#!/usr/bin/env python3
"""Move a small offset back to an approved named hardware pose."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors import MotorCalibration
from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTORS
from hardware.so100_plus.joint_mapping import MOTOR_ORDER, PolicyJointMapping


CONFIRMATION = "MOVE_NAMED_POSE"
MAX_ACTIVE_JOINTS = 2
MAX_DELTA_RAD = math.radians(2.0)
POSITION_EPSILON_RAD = math.radians(0.15)


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
        "--pose",
        type=Path,
        default=Path("hardware/calibration/hardware_safe_pose.json"),
    )
    parser.add_argument("--duration", type=float, default=2.5)
    parser.add_argument("--hold", type=float, default=0.5)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    if args.confirm != CONFIRMATION:
        parser.error(f"--confirm must be exactly {CONFIRMATION}")
    if args.duration < 1.0 or not 0.0 <= args.hold <= 5.0:
        parser.error("--duration >= 1.0 and --hold within [0, 5] are required")
    return args


def load_approved_pose(path: Path) -> dict:
    data = json.loads(path.read_text())
    required = (
        "automatic_validation_passed",
        "user_visual_approval",
        "approved_for_recovery_motion",
    )
    failed = [name for name in required if data.get(name) is not True]
    if failed:
        raise RuntimeError(f"pose is not approved; false flags: {failed}")
    if data.get("name") != "hardware_safe":
        raise RuntimeError(f"unexpected pose name: {data.get('name')!r}")
    return data


def read_current_policy(args: argparse.Namespace) -> tuple[list[str], list[float]]:
    calibration_data = json.loads(args.calibration.read_text())
    calibration = {
        name: MotorCalibration(**calibration_data[name]) for name in MOTOR_ORDER
    }
    mapping = PolicyJointMapping(args.mapping)
    bus = FeetechMotorsBus(args.port, MOTORS, calibration)
    try:
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=3)
        if any(int(value) != 0 for value in torque.values()):
            raise RuntimeError(f"refusing because torque is enabled: {torque}")
        normalized = bus.sync_read(
            "Present_Position", normalize=True, num_retry=3
        )
        policy = mapping.convert(
            {name: float(normalized[name]) for name in MOTOR_ORDER}
        )
        names = list(mapping.policy_joint_names)
        return names, [float(policy[name]) for name in names]
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


def main() -> int:
    args = parse_args()
    pose = load_approved_pose(args.pose)
    names, current = read_current_policy(args)
    if list(pose["policy_joint_order"]) != names:
        raise RuntimeError("named pose joint order does not match mapping")
    target = [float(value) for value in pose["policy_position_rad"]]
    deltas = [goal - now for goal, now in zip(target, current)]
    deltas = [0.0 if abs(value) <= POSITION_EPSILON_RAD else value for value in deltas]
    active = [index for index, value in enumerate(deltas) if value != 0.0]

    print("[move_named_pose] current and target policy radians:")
    for name, now, goal, delta in zip(names, current, target, deltas):
        print(f"  {name:28s} {now:+.4f} -> {goal:+.4f} delta={delta:+.4f}")
    if not active:
        print("[move_named_pose] already at hardware_safe pose")
        return 0
    if len(active) > MAX_ACTIVE_JOINTS:
        raise RuntimeError(
            f"first-stage named-pose test permits at most {MAX_ACTIVE_JOINTS} "
            f"active joints; got {[names[i] for i in active]}"
        )
    oversized = [
        f"{names[i]}={math.degrees(deltas[i]):+.2f}deg"
        for i in active
        if abs(deltas[i]) > MAX_DELTA_RAD + 1.0e-6
    ]
    if oversized:
        raise RuntimeError(
            "first-stage named-pose delta exceeds 2deg: " + ", ".join(oversized)
        )

    args.log.parent.mkdir(parents=True, exist_ok=True)
    plan_log = args.log.with_suffix(".plan.json")
    plan_log.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().astimezone().isoformat(),
                "pose_file": str(args.pose.resolve()),
                "joint_order": names,
                "current_policy_rad": current,
                "target_policy_rad": target,
                "delta_rad": deltas,
                "active_joints": [names[i] for i in active],
            },
            indent=2,
        )
        + "\n"
    )
    command = [
        sys.executable,
        str(PROJECT_ROOT / "hardware/tools/test_multi_joint_delta.py"),
        "--port", args.port,
        "--calibration", str(args.calibration),
        "--mapping", str(args.mapping),
        "--deltas-rad", ",".join(f"{value:.10g}" for value in deltas),
        "--duration", f"{args.duration:.8g}",
        "--hold", f"{args.hold:.8g}",
        "--keep-target",
        "--log", str(args.log),
        "--confirm", "MOVE_MULTI_JOINT",
    ]
    return subprocess.run(command, cwd=PROJECT_ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
