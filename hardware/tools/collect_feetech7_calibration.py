#!/usr/bin/env python3
"""Interactively collect candidate seven-axis centers and safe ranges without writes."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Support direct execution as `python hardware/tools/collect_feetech7_calibration.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTOR_TO_POLICY_JOINT, MOTORS, MUJOCO_LIMITS_RAD

ENCODER_RESOLUTION = 4096


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("hardware/calibration/so100_plus_candidate.json"),
    )
    parser.add_argument("--period", type=float, default=0.05)
    parser.add_argument(
        "--range-seconds",
        type=float,
        default=15.0,
        help="Read duration for each joint while it is moved manually",
    )
    parser.add_argument(
        "--margin-counts",
        type=int,
        default=30,
        help="Safety margin removed from both observed range ends",
    )
    return parser.parse_args()


def read_positions(bus: FeetechMotorsBus) -> dict[str, int]:
    values = bus.sync_read("Present_Position", normalize=False, num_retry=2)
    return {name: int(value) for name, value in values.items()}


def wrapped_delta(raw: int, reference: int) -> int:
    """Return the shortest signed encoder displacement from reference to raw."""
    half = ENCODER_RESOLUTION // 2
    return (raw - reference + half) % ENCODER_RESOLUTION - half


def main() -> int:
    args = parse_args()
    if args.period <= 0 or args.range_seconds <= 0:
        raise ValueError("--period and --range-seconds must be positive")
    if args.margin_counts < 0:
        raise ValueError("--margin-counts cannot be negative")

    bus = FeetechMotorsBus(port=args.port, motors=MOTORS, calibration={})
    try:
        print("[collect_calibration] STRICT_READ_ONLY: torque and EEPROM are never written")
        print("[collect_calibration] Support the arm before continuing; Torque_Enable must be 0")
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=2)
        enabled = [name for name, value in torque.items() if int(value) != 0]
        if enabled:
            raise RuntimeError(f"refusing collection because torque is enabled: {enabled}")

        input(
            "Place all joints at comfortable reference positions, support the arm, "
            "then press ENTER to capture centers..."
        )
        center = read_positions(bus)
        print(f"[collect_calibration] centers={center}")

        ranges: dict[str, tuple[int, int]] = {}
        raw_endpoints: dict[str, tuple[int, int]] = {}
        for motor in MOTORS:
            input(
                f"\nPrepare to move only '{motor}' through its SAFE physical range. "
                "Do not pull cables. Press ENTER to start..."
            )
            reference = center[motor]
            minimum_delta = maximum_delta = wrapped_delta(
                read_positions(bus)[motor], reference
            )
            deadline = time.monotonic() + args.range_seconds
            while time.monotonic() < deadline:
                value = read_positions(bus)[motor]
                delta = wrapped_delta(value, reference)
                minimum_delta = min(minimum_delta, delta)
                maximum_delta = max(maximum_delta, delta)
                remaining = max(0.0, deadline - time.monotonic())
                print(
                    f"\r[{motor}] raw={value} relative={delta:+d} "
                    f"observed_relative=[{minimum_delta:+d}, {maximum_delta:+d}] "
                    f"remaining={remaining:4.1f}s",
                    end="",
                    flush=True,
                )
                time.sleep(args.period)
            print()
            safe_min_delta = minimum_delta + args.margin_counts
            safe_max_delta = maximum_delta - args.margin_counts
            if safe_min_delta >= 0 or safe_max_delta <= 0:
                raise RuntimeError(
                    f"{motor} was not moved far enough on both sides of its reference. "
                    f"observed relative range=[{minimum_delta}, {maximum_delta}], "
                    f"margin={args.margin_counts}. Re-run and place the reference nearer "
                    "the middle of this joint's safe range."
                )
            ranges[motor] = (safe_min_delta, safe_max_delta)
            raw_endpoints[motor] = (
                (reference + safe_min_delta) % ENCODER_RESOLUTION,
                (reference + safe_max_delta) % ENCODER_RESOLUTION,
            )

        motors = {}
        for name, motor in MOTORS.items():
            relative_min, relative_max = ranges[name]
            raw_at_min, raw_at_max = raw_endpoints[name]
            motors[name] = {
                "id": motor.id,
                "policy_joint": MOTOR_TO_POLICY_JOINT[name],
                "center_raw": center[name],
                "safe_relative_min": relative_min,
                "safe_relative_max": relative_max,
                "raw_at_safe_relative_min": raw_at_min,
                "raw_at_safe_relative_max": raw_at_max,
                "crosses_encoder_wrap": raw_at_min > raw_at_max,
                "direction": None,
                "zero_offset_rad": None,
                "mujoco_limit_rad": list(MUJOCO_LIMITS_RAD[name]),
                "approved": False,
            }

        result = {
            "schema_version": 1,
            "timestamp": datetime.now().astimezone().isoformat(),
            "port": args.port,
            "read_only_collection": True,
            "margin_counts": args.margin_counts,
            "approved_for_motion": False,
            "motors": motors,
            "notes": [
                "Candidate only; nothing has been written to the servos.",
                "direction and zero_offset_rad require model-to-hardware alignment.",
                "Ranges are signed displacements around center_raw and handle encoder wrap.",
                "wrist_roll range must be finite and cable-limited.",
            ],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n")
        print(f"[collect_calibration] candidate saved: {args.output.resolve()}")
        print("[collect_calibration] NOT approved for motion")
        return 0
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    raise SystemExit(main())
