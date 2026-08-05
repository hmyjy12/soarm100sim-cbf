#!/usr/bin/env python3
"""Emergency helper to disable torque on all seven Feetech motors."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors import MotorCalibration
from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTORS


CONFIRMATION = "DISABLE_ALL_TORQUE"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--calibration",
        type=Path,
        default=Path("hardware/calibration/lerobot/so100_plus_7dof.json"),
    )
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    if args.confirm != CONFIRMATION:
        parser.error(f"--confirm must be exactly {CONFIRMATION}")

    raw = json.loads(args.calibration.read_text())
    calibration = {
        name: MotorCalibration(**values) for name, values in raw.items()
    }
    bus = FeetechMotorsBus(args.port, MOTORS, calibration)
    try:
        bus.connect(handshake=True)
        before = bus.sync_read("Torque_Enable", normalize=False, num_retry=2)
        print(f"[disable_all_torque] before={before}")
        bus.disable_torque(num_retry=5)
        after = bus.sync_read("Torque_Enable", normalize=False, num_retry=3)
        print(f"[disable_all_torque] after={after}")
        if any(int(value) != 0 for value in after.values()):
            raise RuntimeError(f"torque disable verification failed: {after}")
        print("[disable_all_torque] verified: all seven motors torque=0")
        return 0
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    raise SystemExit(main())
