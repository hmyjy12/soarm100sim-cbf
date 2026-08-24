#!/usr/bin/env python3
"""Take a read-only snapshot of safety and control registers on all seven motors."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Support direct execution as `python hardware/tools/snapshot_feetech7.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTORS


REGISTERS = (
    "Torque_Enable",
    "Operating_Mode",
    "Present_Position",
    "Min_Position_Limit",
    "Max_Position_Limit",
    "Homing_Offset",
    "P_Coefficient",
    "I_Coefficient",
    "D_Coefficient",
    "Max_Torque_Limit",
    "Protection_Current",
    "Overload_Torque",
    "Present_Load",
    "Present_Current",
    "Present_Voltage",
    "Present_Temperature",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("log/runtime/hardware/feetech7_register_snapshot.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bus = FeetechMotorsBus(port=args.port, motors=MOTORS, calibration={})
    try:
        print("[snapshot_feetech7] STRICT_READ_ONLY: no motor register will be written")
        bus.connect(handshake=True)
        values = {}
        for register in REGISTERS:
            values[register] = bus.sync_read(register, normalize=False, num_retry=2)
            print(f"{register}={values[register]}")

        row = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "port": args.port,
            "mode": "STRICT_READ_ONLY",
            "motors": {name: motor.id for name, motor in MOTORS.items()},
            "registers": values,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(row, indent=2, ensure_ascii=True) + "\n")
        print(f"[snapshot_feetech7] saved: {args.output.resolve()}")
        return 0
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    raise SystemExit(main())
