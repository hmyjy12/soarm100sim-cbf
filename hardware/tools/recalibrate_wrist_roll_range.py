#!/usr/bin/env python3
"""Re-record and apply only the finite wrist_roll range."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors import MotorCalibration
from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTORS


CONFIRMATION = "APPLY_WRIST_ROLL_RANGE"
JOINT = "wrist_roll"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--calibration",
        type=Path,
        default=Path("hardware/calibration/lerobot/so100_plus_7dof.json"),
    )
    parser.add_argument("--seconds", type=float, default=15.0)
    parser.add_argument("--period", type=float, default=0.05)
    parser.add_argument("--margin-counts", type=int, default=30)
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    if args.confirm != CONFIRMATION:
        parser.error(f"--confirm must be exactly {CONFIRMATION}")
    if args.seconds < 5 or args.period <= 0:
        parser.error("--seconds must be at least 5 and --period must be positive")
    if args.margin_counts < 0:
        parser.error("--margin-counts cannot be negative")
    return args


def load_raw_calibration(path: Path) -> dict:
    data = json.loads(path.read_text())
    if set(data) != set(MOTORS):
        raise ValueError("calibration does not contain the expected seven motors")
    return data


def main() -> int:
    args = parse_args()
    raw_calibration = load_raw_calibration(args.calibration)
    calibration = {
        name: MotorCalibration(**values) for name, values in raw_calibration.items()
    }
    bus = FeetechMotorsBus(args.port, MOTORS, calibration)

    try:
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=2)
        enabled = [name for name, value in torque.items() if int(value) != 0]
        if enabled:
            raise RuntimeError(f"refusing calibration because torque is enabled: {enabled}")

        old = calibration[JOINT]
        start = int(bus.read("Present_Position", JOINT, normalize=False, num_retry=2))
        print(
            f"[wrist_roll_range] old=[{old.range_min}, {old.range_max}] "
            f"start={start} homing_offset={old.homing_offset}"
        )
        print(
            "[wrist_roll_range] Move only wrist_roll through the complete cable-safe "
            "finite range. Do not pull the cable."
        )

        minimum = maximum = start
        deadline = time.monotonic() + args.seconds
        while time.monotonic() < deadline:
            value = int(
                bus.read("Present_Position", JOINT, normalize=False, num_retry=2)
            )
            minimum = min(minimum, value)
            maximum = max(maximum, value)
            remaining = max(0.0, deadline - time.monotonic())
            print(
                f"\r[wrist_roll_range] raw={value} observed=[{minimum}, {maximum}] "
                f"remaining={remaining:4.1f}s",
                end="",
                flush=True,
            )
            time.sleep(args.period)
        print()

        safe_min = minimum + args.margin_counts
        safe_max = maximum - args.margin_counts
        if safe_min >= safe_max:
            raise RuntimeError("observed range is too small after applying the margin")
        if maximum - minimum > 3000:
            raise RuntimeError(
                "observed range spans more than 3000 counts; possible encoder wrap. "
                "No values were written."
            )
        if not safe_min <= start <= safe_max:
            raise RuntimeError(
                f"start position {start} is outside proposed safe range "
                f"[{safe_min}, {safe_max}]. Move farther on both sides and retry."
            )

        print(
            f"[wrist_roll_range] proposed=[{safe_min}, {safe_max}] "
            f"observed=[{minimum}, {maximum}] margin={args.margin_counts}"
        )
        answer = input(
            f"Type {CONFIRMATION} again to write only wrist_roll limits, "
            "or press ENTER to abort: "
        ).strip()
        if answer != CONFIRMATION:
            print("[wrist_roll_range] aborted; no register or file was changed")
            return 1

        updated = MotorCalibration(
            id=old.id,
            drive_mode=old.drive_mode,
            homing_offset=old.homing_offset,
            range_min=safe_min,
            range_max=safe_max,
        )
        bus.write_calibration({JOINT: updated}, cache=False)

        raw_calibration[JOINT]["range_min"] = safe_min
        raw_calibration[JOINT]["range_max"] = safe_max
        args.calibration.write_text(
            json.dumps(raw_calibration, indent=4, ensure_ascii=True) + "\n"
        )

        readback = bus.read_calibration()[JOINT]
        if (
            readback.homing_offset != updated.homing_offset
            or readback.range_min != updated.range_min
            or readback.range_max != updated.range_max
        ):
            raise RuntimeError(f"wrist_roll readback mismatch: {readback} != {updated}")
        print(
            f"[wrist_roll_range] applied and verified: "
            f"[{readback.range_min}, {readback.range_max}]"
        )
        print("[wrist_roll_range] all other motor calibration values were preserved")
        return 0
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    raise SystemExit(main())
