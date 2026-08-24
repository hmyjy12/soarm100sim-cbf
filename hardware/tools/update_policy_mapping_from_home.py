#!/usr/bin/env python3
"""Recompute policy zero offsets from a read-only policy-home capture."""

from __future__ import annotations

import argparse
import json
import math
import shutil
from datetime import datetime
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


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")


def _generate(args: argparse.Namespace) -> int:
    mapping = _load(args.mapping)
    capture = _load(args.home_capture)
    motors = capture.get("motors", {})
    joints = mapping.get("joints", {})
    if tuple(motors) != MOTOR_ORDER or tuple(joints) != MOTOR_ORDER:
        raise ValueError("home capture and mapping must contain the canonical seven motors")
    if args.output.resolve() == args.mapping.resolve():
        raise ValueError("candidate output must not overwrite the approved mapping")

    for name in MOTOR_ORDER:
        sample = motors[name]
        cfg = joints[name]
        value = float(sample["lerobot_value"])
        target = float(sample["policy_home_rad"])
        if name == "gripper":
            zero = target - float(cfg["scale_rad_per_percent"]) * value
            cfg["home_lerobot_percent"] = value
        else:
            zero = target - int(cfg["sign"]) * math.radians(value)
            cfg["home_lerobot_deg"] = value
        cfg["home_policy_rad"] = target
        cfg["zero_offset_rad"] = zero
        cfg["zero_offset_status"] = "pending_mujoco_read_only_validation"

    mapping["source_capture"] = str(args.home_capture)
    mapping["approved_for_read_only_joint_state"] = True
    mapping["approved_for_policy_control"] = False
    mapping["validation_state"] = "pending_mujoco_read_only_validation"
    mapping["validation_note"] = "Zero offsets recomputed from a new home capture; policy control is not approved."
    _write(args.output, mapping)
    print(f"[policy_mapping] candidate saved: {args.output.resolve()}")
    print("[policy_mapping] policy control remains DISABLED until read-only MuJoCo validation passes")
    return 0


def _approve(args: argparse.Namespace) -> int:
    if args.confirm != "MUJOCO_MAPPING_VALIDATED":
        raise ValueError("approval requires --confirm MUJOCO_MAPPING_VALIDATED")
    mapping = _load(args.candidate)
    if mapping.get("validation_state") != "pending_mujoco_read_only_validation":
        raise ValueError("candidate is not waiting for MuJoCo read-only validation")
    if args.output.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = args.output.with_name(f"{args.output.stem}.before_{stamp}{args.output.suffix}")
        shutil.copy2(args.output, backup)
        print(f"[policy_mapping] previous mapping backed up: {backup.resolve()}")

    mapping["approved_for_policy_control"] = True
    mapping["validation_state"] = "mujoco_read_only_validation_passed"
    mapping["validation_note"] = "Operator confirmed all seven joints in the MuJoCo read-only mirror."
    for cfg in mapping["joints"].values():
        cfg.pop("zero_offset_status", None)
    _write(args.output, mapping)
    print(f"[policy_mapping] approved mapping saved: {args.output.resolve()}")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate", help="Generate a non-approved mapping candidate")
    generate.add_argument("--mapping", type=Path, required=True)
    generate.add_argument("--home-capture", type=Path, required=True)
    generate.add_argument("--output", type=Path, required=True)
    generate.set_defaults(func=_generate)

    approve = sub.add_parser("approve", help="Promote a candidate after read-only validation")
    approve.add_argument("--candidate", type=Path, required=True)
    approve.add_argument("--output", type=Path, required=True)
    approve.add_argument("--confirm", required=True)
    approve.set_defaults(func=_approve)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
