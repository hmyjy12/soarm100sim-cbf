#!/usr/bin/env python3
"""Read seven motors without writes and stream converted policy joints over UDP."""

from __future__ import annotations

import argparse
import json
import signal
import socket
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lerobot.motors import MotorCalibration
from lerobot.motors.feetech import FeetechMotorsBus

from hardware.so100_plus.config import MOTORS
from hardware.so100_plus.joint_mapping import MOTOR_ORDER, PolicyJointMapping


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
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--udp-port", type=int, default=15001)
    parser.add_argument("--rate", type=float, default=20.0)
    parser.add_argument("--print-period", type=float, default=1.0)
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("log/runtime/hardware/policy_joint_stream.jsonl"),
    )
    args = parser.parse_args()
    if args.rate < 1 or args.rate > 50:
        parser.error("--rate must be within [1, 50]")
    if args.print_period <= 0:
        parser.error("--print-period must be positive")
    return args


def load_calibration(path: Path) -> dict[str, MotorCalibration]:
    raw = json.loads(path.read_text())
    if tuple(raw) != MOTOR_ORDER:
        raise ValueError("calibration does not contain the expected seven motors")
    return {name: MotorCalibration(**values) for name, values in raw.items()}


def main() -> int:
    args = parse_args()
    calibration = load_calibration(args.calibration)
    mapping = PolicyJointMapping(args.mapping)
    bus = FeetechMotorsBus(args.port, MOTORS, calibration)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    log_file = None
    stop_requested = False

    def request_stop(_signum, _frame) -> None:
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    try:
        print("[policy_joint_stream] STRICT_READ_ONLY: no motor register will be written")
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=2)
        enabled = [name for name, value in torque.items() if int(value) != 0]
        if enabled:
            raise RuntimeError(f"refusing stream because torque is enabled: {enabled}")

        args.log.parent.mkdir(parents=True, exist_ok=True)
        log_file = args.log.open("w", encoding="utf-8")
        destination = (args.host, args.udp_port)
        period = 1.0 / args.rate
        sequence = 0
        next_print = time.monotonic()
        print(
            f"[policy_joint_stream] destination={args.host}:{args.udp_port} "
            f"rate={args.rate:.1f}Hz; Ctrl+C to stop"
        )

        while not stop_requested:
            started = time.monotonic()
            normalized = bus.sync_read("Present_Position", normalize=True, num_retry=2)
            raw = bus.sync_read("Present_Position", normalize=False, num_retry=2)
            policy = mapping.convert(
                {name: float(normalized[name]) for name in MOTOR_ORDER}
            )
            packet = {
                "schema_version": 1,
                "sequence": sequence,
                "timestamp": datetime.now().astimezone().isoformat(),
                "source": "so100_plus_feetech_read_only",
                "raw": {name: int(raw[name]) for name in MOTOR_ORDER},
                "lerobot": {name: float(normalized[name]) for name in MOTOR_ORDER},
                "policy": policy,
            }
            encoded = json.dumps(packet, ensure_ascii=True).encode("ascii")
            sock.sendto(encoded, destination)
            log_file.write(encoded.decode("ascii") + "\n")
            log_file.flush()

            now = time.monotonic()
            if now >= next_print:
                compact = ", ".join(
                    f"{name}={value:+.3f}" for name, value in policy.items()
                )
                print(f"[policy_joint_stream] seq={sequence} {compact}")
                next_print = now + args.print_period
            sequence += 1
            time.sleep(max(0.0, period - (time.monotonic() - started)))
    except KeyboardInterrupt:
        print("\n[policy_joint_stream] stopped")
        return 0
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)
        if log_file:
            log_file.close()
        sock.close()
    print("\n[policy_joint_stream] stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
