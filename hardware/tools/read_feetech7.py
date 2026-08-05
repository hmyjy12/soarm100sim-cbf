#!/usr/bin/env python3
"""Read-only diagnostics for the custom seven-motor SO-100 Plus arm."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Support direct execution as `python hardware/tools/read_feetech7.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTORS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ping IDs 1-7 and read raw Feetech registers without writing to the motors."
    )
    parser.add_argument("--port", default="/dev/ttyACM0", help="Feetech controller serial port")
    parser.add_argument("--samples", type=int, default=10, help="Number of samples to read")
    parser.add_argument("--period", type=float, default=0.5, help="Seconds between samples")
    parser.add_argument("--retries", type=int, default=2, help="Read retries per sample")
    parser.add_argument("--log", type=Path, help="Optional JSONL output path")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to an existing log instead of replacing it",
    )
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be at least 1")
    if args.period < 0:
        parser.error("--period cannot be negative")
    if args.retries < 0:
        parser.error("--retries cannot be negative")
    return args


def main() -> int:
    args = parse_args()
    bus = FeetechMotorsBus(port=args.port, motors=MOTORS, calibration={})
    log_file = None

    try:
        if args.log:
            args.log.parent.mkdir(parents=True, exist_ok=True)
            log_file = args.log.open("a" if args.append else "w", encoding="utf-8")

        print(f"[read_feetech7] port={args.port} motors={len(MOTORS)} mode=STRICT_READ_ONLY")
        print("[read_feetech7] no torque, configuration, calibration, or goal register will be written")

        # The handshake pings the expected IDs and reads firmware versions only.
        bus.connect(handshake=True)
        print("[read_feetech7] handshake passed: IDs 1-7 responded as STS3215")

        for index in range(args.samples):
            timestamp = datetime.now().astimezone().isoformat()
            positions = bus.sync_read(
                "Present_Position", normalize=False, num_retry=args.retries
            )
            torque_enabled = bus.sync_read(
                "Torque_Enable", normalize=False, num_retry=args.retries
            )
            row = {
                "timestamp": timestamp,
                "sample": index,
                "port": args.port,
                "raw_position": positions,
                "torque_enable": torque_enabled,
            }
            print(
                f"[{index:03d}] raw_position={positions} "
                f"torque_enable={torque_enabled}"
            )
            if log_file:
                log_file.write(json.dumps(row, ensure_ascii=True) + "\n")
                log_file.flush()
            if index + 1 < args.samples:
                time.sleep(args.period)

        return 0
    finally:
        if bus.is_connected:
            # The LeRobot default is True, which writes Torque_Enable=0.
            bus.disconnect(disable_torque=False)
        if log_file:
            log_file.close()


if __name__ == "__main__":
    raise SystemExit(main())
