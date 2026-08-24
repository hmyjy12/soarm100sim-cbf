#!/usr/bin/env python3
"""Safely move one calibrated Feetech joint by a small angle and return."""

from __future__ import annotations

import argparse
import json
import signal
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


COUNTS_PER_TURN = 4095
CONFIRMATION = "MOVE_SINGLE_JOINT"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--calibration",
        type=Path,
        default=Path("hardware/calibration/lerobot/so100_plus_7dof.json"),
    )
    parser.add_argument("--joint", choices=tuple(MOTORS), default="wrist_roll")
    parser.add_argument(
        "--delta-deg",
        type=float,
        default=1.0,
        help="Signed test displacement; absolute value cannot exceed 5 degrees",
    )
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--hold", type=float, default=0.5)
    parser.add_argument("--rate", type=float, default=20.0)
    parser.add_argument("--settle-timeout", type=float, default=1.0)
    parser.add_argument("--position-tolerance-counts", type=int, default=8)
    parser.add_argument("--limit-margin-counts", type=int, default=100)
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("log/runtime/hardware/single_joint_test.jsonl"),
    )
    parser.add_argument(
        "--confirm",
        required=True,
        help=f"Must be exactly {CONFIRMATION}",
    )
    args = parser.parse_args()
    if args.confirm != CONFIRMATION:
        parser.error(f"--confirm must be exactly {CONFIRMATION}")
    if args.delta_deg == 0 or abs(args.delta_deg) > 5.0:
        parser.error("--delta-deg must be non-zero and within [-5, +5]")
    if args.duration < 0.5:
        parser.error("--duration must be at least 0.5 seconds")
    if args.hold < 0 or args.rate < 5 or args.rate > 50:
        parser.error("--hold must be nonnegative and --rate must be within [5, 50]")
    if args.settle_timeout < 0.2 or args.settle_timeout > 5.0:
        parser.error("--settle-timeout must be within [0.2, 5.0]")
    if not 1 <= args.position_tolerance_counts <= 20:
        parser.error("--position-tolerance-counts must be within [1, 20]")
    if args.limit_margin_counts < 20:
        parser.error("--limit-margin-counts must be at least 20")
    return args


def load_calibration(path: Path) -> dict[str, MotorCalibration]:
    raw = json.loads(path.read_text())
    if set(raw) != set(MOTORS):
        raise ValueError(
            f"calibration motors do not match expected seven motors: {sorted(raw)}"
        )
    return {name: MotorCalibration(**values) for name, values in raw.items()}


def telemetry(
    bus: FeetechMotorsBus,
    joint: str,
    phase: str,
    goal_raw: int,
) -> dict:
    position = int(bus.read("Present_Position", joint, normalize=False, num_retry=2))
    temperature_samples = [
        int(bus.read("Present_Temperature", joint, normalize=False, num_retry=2))
    ]
    if temperature_samples[0] >= 45:
        # A single serial read has occasionally returned 80 C immediately after
        # several stable 34 C samples. Confirm before treating it as real heat.
        for _ in range(2):
            time.sleep(0.02)
            temperature_samples.append(
                int(
                    bus.read(
                        "Present_Temperature",
                        joint,
                        normalize=False,
                        num_retry=2,
                    )
                )
            )
    confirmed_temperature = sorted(temperature_samples)[len(temperature_samples) // 2]
    row = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "phase": phase,
        "joint": joint,
        "goal_raw": goal_raw,
        "position_raw": position,
        "error_counts": goal_raw - position,
        "load_raw": int(bus.read("Present_Load", joint, normalize=False, num_retry=2)),
        "current_raw": int(
            bus.read("Present_Current", joint, normalize=False, num_retry=2)
        ),
        "temperature_c": confirmed_temperature,
        "temperature_samples_c": temperature_samples,
        "temperature_single_read_glitch": (
            len(temperature_samples) > 1
            and temperature_samples[0] >= 45
            and confirmed_temperature < 55
        ),
        "voltage_raw": int(
            bus.read("Present_Voltage", joint, normalize=False, num_retry=2)
        ),
    }
    if confirmed_temperature >= 55:
        raise RuntimeError(f"temperature protection triggered: {row}")
    return row


def move_segment(
    bus: FeetechMotorsBus,
    joint: str,
    start_raw: int,
    end_raw: int,
    duration: float,
    rate: float,
    phase: str,
    log_file,
) -> None:
    steps = max(2, round(duration * rate))
    period = duration / steps
    for index in range(1, steps + 1):
        ratio = index / steps
        goal = round(start_raw + (end_raw - start_raw) * ratio)
        bus.write("Goal_Position", joint, goal, normalize=False, num_retry=2)
        row = telemetry(bus, joint, phase, goal)
        log_file.write(json.dumps(row, ensure_ascii=True) + "\n")
        log_file.flush()
        print(
            f"\r[{phase}] goal={goal} pos={row['position_raw']} "
            f"err={row['error_counts']:+d} current={row['current_raw']} "
            f"load={row['load_raw']} temp={row['temperature_c']}C",
            end="",
            flush=True,
        )
        time.sleep(period)
    print()


def settle_at_target(
    bus: FeetechMotorsBus,
    joint: str,
    goal_raw: int,
    timeout: float,
    rate: float,
    tolerance_counts: int,
    phase: str,
    log_file,
) -> dict:
    """Hold one goal until feedback converges or the bounded timeout expires."""
    deadline = time.monotonic() + timeout
    period = 1.0 / rate
    consecutive = 0
    last_row = None
    while time.monotonic() < deadline:
        bus.write("Goal_Position", joint, goal_raw, normalize=False, num_retry=2)
        last_row = telemetry(bus, joint, phase, goal_raw)
        log_file.write(json.dumps(last_row, ensure_ascii=True) + "\n")
        log_file.flush()
        if abs(last_row["error_counts"]) <= tolerance_counts:
            consecutive += 1
            if consecutive >= 3:
                print(
                    f"[{phase}] converged pos={last_row['position_raw']} "
                    f"err={last_row['error_counts']:+d} counts"
                )
                return last_row
        else:
            consecutive = 0
        time.sleep(period)

    if last_row is None:
        raise RuntimeError(f"{phase} produced no feedback")
    raise RuntimeError(
        f"{phase} did not converge within {timeout:.2f}s: "
        f"goal={goal_raw} pos={last_row['position_raw']} "
        f"error={last_row['error_counts']:+d} counts "
        f"tolerance={tolerance_counts}"
    )


def main() -> int:
    args = parse_args()

    def interrupt_for_cleanup(_signum, _frame) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupt_for_cleanup)

    calibration = load_calibration(args.calibration)
    selected = calibration[args.joint]
    bus = FeetechMotorsBus(
        port=args.port,
        motors=MOTORS,
        calibration=calibration,
    )
    log_file = None
    torque_enabled = False

    try:
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=2)
        enabled = [name for name, value in torque.items() if int(value) != 0]
        if enabled:
            raise RuntimeError(f"refusing test because torque is already enabled: {enabled}")

        mode = int(bus.read("Operating_Mode", args.joint, normalize=False, num_retry=2))
        if mode != 0:
            raise RuntimeError(
                f"{args.joint} is not in position mode: Operating_Mode={mode}"
            )

        start_raw = int(
            bus.read("Present_Position", args.joint, normalize=False, num_retry=2)
        )
        delta_counts = round(args.delta_deg * COUNTS_PER_TURN / 360.0)
        target_raw = start_raw + delta_counts
        safe_min = selected.range_min + args.limit_margin_counts
        safe_max = selected.range_max - args.limit_margin_counts
        if not safe_min <= start_raw <= safe_max:
            raise RuntimeError(
                f"start position {start_raw} is too close to the calibrated limit; "
                f"required safe interval=[{safe_min}, {safe_max}]. Move it manually "
                "toward the middle while torque is off."
            )
        if not safe_min <= target_raw <= safe_max:
            raise RuntimeError(
                f"target {target_raw} leaves safe interval=[{safe_min}, {safe_max}]"
            )

        args.log.parent.mkdir(parents=True, exist_ok=True)
        log_file = args.log.open("w", encoding="utf-8")
        header = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "phase": "header",
            "port": args.port,
            "joint": args.joint,
            "delta_deg": args.delta_deg,
            "delta_counts": delta_counts,
            "start_raw": start_raw,
            "target_raw": target_raw,
            "calibrated_range": [selected.range_min, selected.range_max],
            "safe_interval": [safe_min, safe_max],
            "other_motors_torque_enabled": False,
        }
        log_file.write(json.dumps(header, ensure_ascii=True) + "\n")
        log_file.flush()

        print("[single_joint_test] Support the arm and keep clear of the mechanism.")
        print(
            f"[single_joint_test] joint={args.joint} start={start_raw} "
            f"target={target_raw} delta={args.delta_deg:+.2f}deg"
        )

        # Prevent a jump when torque is enabled.
        bus.write("Goal_Position", args.joint, start_raw, normalize=False, num_retry=2)
        bus.enable_torque(args.joint, num_retry=2)
        torque_enabled = True
        time.sleep(0.3)

        move_segment(
            bus,
            args.joint,
            start_raw,
            target_raw,
            args.duration,
            args.rate,
            "outbound",
            log_file,
        )
        settle_at_target(
            bus,
            args.joint,
            target_raw,
            args.settle_timeout,
            args.rate,
            args.position_tolerance_counts,
            "outbound_settle",
            log_file,
        )
        time.sleep(args.hold)
        move_segment(
            bus,
            args.joint,
            target_raw,
            start_raw,
            args.duration,
            args.rate,
            "return",
            log_file,
        )
        settle_at_target(
            bus,
            args.joint,
            start_raw,
            args.settle_timeout,
            args.rate,
            args.position_tolerance_counts,
            "return_settle",
            log_file,
        )
        print("[single_joint_test] completed; selected joint torque will be disabled")
        return 0
    finally:
        if bus.is_connected and torque_enabled:
            bus.disable_torque(args.joint, num_retry=2)
            torque_after = bus.sync_read(
                "Torque_Enable", normalize=False, num_retry=3
            )
            verification = {
                "timestamp": datetime.now().astimezone().isoformat(),
                "phase": "torque_off_verification",
                "joint": args.joint,
                "torque_enable": {
                    name: int(value) for name, value in torque_after.items()
                },
                "all_torque_off": all(
                    int(value) == 0 for value in torque_after.values()
                ),
            }
            if log_file:
                log_file.write(json.dumps(verification, ensure_ascii=True) + "\n")
                log_file.flush()
            print(f"[single_joint_test] torque verification={torque_after}")
            if not verification["all_torque_off"]:
                raise RuntimeError(
                    f"torque-off verification failed: {torque_after}"
                )
        if bus.is_connected:
            bus.disconnect(disable_torque=False)
        if log_file:
            log_file.close()


if __name__ == "__main__":
    raise SystemExit(main())
