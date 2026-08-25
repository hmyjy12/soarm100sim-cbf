#!/usr/bin/env python3
"""Approve a validated, read-only pose capture for policy initialization."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path


CONFIRMATION = "APPROVE_POLICY_READY_POSE"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--confirm", required=True)
    return parser.parse_args()


def validate_candidate(data: dict) -> None:
    if data.get("mode") != "STRICT_READ_ONLY":
        raise RuntimeError("candidate was not produced in STRICT_READ_ONLY mode")
    if not data.get("automatic_validation_passed", False):
        failures = data.get("automatic_validation_failures", [])
        raise RuntimeError(f"candidate failed automatic validation: {failures}")

    joint_order = data.get("policy_joint_order")
    positions = data.get("policy_position_rad")
    if not isinstance(joint_order, list) or len(joint_order) != 7:
        raise RuntimeError("candidate must contain seven policy joint names")
    if not isinstance(positions, list) or len(positions) != 7:
        raise RuntimeError("candidate must contain seven policy positions")
    if len(set(joint_order)) != 7:
        raise RuntimeError("candidate policy joint names are not unique")
    if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in positions):
        raise RuntimeError("candidate contains a non-finite policy position")


def main() -> int:
    args = parse_args()
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"--confirm must be exactly {CONFIRMATION}")

    data = json.loads(args.candidate.read_text())
    validate_candidate(data)
    data["name"] = "policy_ready_pose"
    data["user_visual_approval"] = True
    data["approved_for_recovery_motion"] = True
    data["approval_timestamp"] = datetime.now().astimezone().isoformat()
    data["approval_basis"] = (
        "automatic limits passed; pose powered and held; operator visually approved"
    )
    data["source_candidate"] = str(args.candidate.resolve())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
    temporary.replace(args.output)
    print(f"[approve_policy_ready_pose] approved: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
