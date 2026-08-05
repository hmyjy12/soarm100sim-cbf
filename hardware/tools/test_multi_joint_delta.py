#!/usr/bin/env python3
"""Guarded synchronized motion for at most two policy-space joints."""

from __future__ import annotations

import argparse
import json
import math
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

from hardware.so100_plus.config import MOTORS, MUJOCO_LIMITS_RAD
from hardware.so100_plus.joint_mapping import MOTOR_ORDER, PolicyJointMapping


CONFIRMATION = "MOVE_MULTI_JOINT"
COUNTS_PER_TURN = 4095
MAX_DELTA_RAD = math.radians(2.0)
ANGLE_EPSILON_RAD = 1.0e-6
RAW_MARGIN = 100
POSITION_TOLERANCE = 8


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
    parser.add_argument("--deltas-rad", required=True)
    parser.add_argument("--duration", type=float, default=2.0)
    parser.add_argument("--hold", type=float, default=0.5)
    parser.add_argument("--keep-target", action="store_true")
    parser.add_argument("--rate", type=float, default=20.0)
    parser.add_argument("--settle-timeout", type=float, default=1.5)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    if args.confirm != CONFIRMATION:
        parser.error(f"--confirm must be exactly {CONFIRMATION}")
    args.deltas = tuple(float(v) for v in args.deltas_rad.split(","))
    if len(args.deltas) != 7 or not all(math.isfinite(v) for v in args.deltas):
        parser.error("--deltas-rad must contain seven finite comma-separated values")
    active = [i for i, value in enumerate(args.deltas) if abs(value) > 1.0e-9]
    if not active or len(active) > 2:
        parser.error("exactly one or two non-zero joint deltas are required")
    if any(
        abs(args.deltas[i]) > MAX_DELTA_RAD + ANGLE_EPSILON_RAD
        for i in active
    ):
        parser.error("each non-zero delta must be within +/-2 degrees")
    if args.duration < 1.0 or args.rate < 10 or args.rate > 50:
        parser.error("--duration >= 1.0 and --rate within [10, 50] are required")
    if args.hold < 0 or args.hold > 5 or args.settle_timeout < 0.2:
        parser.error("invalid hold or settle timeout")
    args.active_indices = active
    return args


def load_calibration(path: Path) -> dict[str, MotorCalibration]:
    raw = json.loads(path.read_text())
    return {name: MotorCalibration(**raw[name]) for name in MOTOR_ORDER}


def policy_to_normalized(
    mapping: PolicyJointMapping, policy: dict[str, float]
) -> dict[str, float]:
    result = {}
    for motor in MOTOR_ORDER:
        cfg = mapping.data["joints"][motor]
        value = policy[cfg["policy_joint"]]
        if motor == "gripper":
            result[motor] = (
                value - cfg["zero_offset_rad"]
            ) / cfg["scale_rad_per_percent"]
        else:
            result[motor] = math.degrees(
                (value - cfg["zero_offset_rad"]) / cfg["sign"]
            )
    return result


def normalized_to_raw(
    normalized: dict[str, float],
    calibration: dict[str, MotorCalibration],
) -> dict[str, int]:
    result = {}
    for motor in MOTOR_ORDER:
        cal = calibration[motor]
        if motor == "gripper":
            result[motor] = int(
                normalized[motor] / 100.0 * (cal.range_max - cal.range_min)
                + cal.range_min
            )
        else:
            midpoint = (cal.range_min + cal.range_max) / 2.0
            result[motor] = int(
                normalized[motor] * COUNTS_PER_TURN / 360.0 + midpoint
            )
    return result


def validate_policy_recovery_move(
    joint: str,
    current: float,
    target: float,
    low: float,
    high: float,
) -> str:
    """Allow an out-of-range joint only to move monotonically toward its range."""
    if low <= current <= high:
        if low <= target <= high:
            return "inside_range"
        raise RuntimeError(
            f"{joint} target {target:+.4f} outside policy limit "
            f"[{low:+.4f}, {high:+.4f}]"
        )
    if current < low:
        if current < target <= high:
            return "recovering_from_below_limit"
        raise RuntimeError(
            f"{joint} is below policy limit at {current:+.4f}; target "
            f"{target:+.4f} must move toward [{low:+.4f}, {high:+.4f}]"
        )
    if low <= target < current:
        return "recovering_from_above_limit"
    raise RuntimeError(
        f"{joint} is above policy limit at {current:+.4f}; target "
        f"{target:+.4f} must move toward [{low:+.4f}, {high:+.4f}]"
    )


def read_telemetry(
    bus: FeetechMotorsBus,
    active_motors: list[str],
    goals: dict[str, int],
    phase: str,
) -> dict:
    position = bus.sync_read(
        "Present_Position", active_motors, normalize=False, num_retry=2
    )
    current = bus.sync_read(
        "Present_Current", active_motors, normalize=False, num_retry=2
    )
    load = bus.sync_read(
        "Present_Load", active_motors, normalize=False, num_retry=2
    )
    temperatures = [
        bus.sync_read(
            "Present_Temperature", active_motors, normalize=False, num_retry=2
        )
    ]
    if any(int(v) >= 45 for v in temperatures[0].values()):
        for _ in range(2):
            time.sleep(0.02)
            temperatures.append(
                bus.sync_read(
                    "Present_Temperature",
                    active_motors,
                    normalize=False,
                    num_retry=2,
                )
            )
    temperature = {
        name: sorted(int(sample[name]) for sample in temperatures)[
            len(temperatures) // 2
        ]
        for name in active_motors
    }
    if any(value >= 55 for value in temperature.values()):
        raise RuntimeError(f"temperature protection triggered: {temperature}")
    return {
        "timestamp": datetime.now().astimezone().isoformat(),
        "phase": phase,
        "goal_raw": {name: int(goals[name]) for name in active_motors},
        "position_raw": {name: int(position[name]) for name in active_motors},
        "error_counts": {
            name: int(goals[name]) - int(position[name]) for name in active_motors
        },
        "current_raw": {name: int(current[name]) for name in active_motors},
        "load_raw": {name: int(load[name]) for name in active_motors},
        "temperature_c": temperature,
    }


def write_row(log_file, row: dict) -> None:
    log_file.write(json.dumps(row, ensure_ascii=True) + "\n")
    log_file.flush()


def move_segment(
    bus,
    active_motors,
    start,
    end,
    duration,
    rate,
    phase,
    log_file,
) -> None:
    steps = max(2, round(duration * rate))
    for index in range(1, steps + 1):
        ratio = index / steps
        goals = {
            name: round(start[name] + (end[name] - start[name]) * ratio)
            for name in active_motors
        }
        bus.sync_write("Goal_Position", goals, normalize=False)
        write_row(log_file, read_telemetry(bus, active_motors, goals, phase))
        time.sleep(duration / steps)


def settle(
    bus,
    active_motors,
    goals,
    timeout,
    rate,
    phase,
    log_file,
) -> None:
    deadline = time.monotonic() + timeout
    consecutive = 0
    last = None
    while time.monotonic() < deadline:
        bus.sync_write("Goal_Position", goals, normalize=False)
        last = read_telemetry(bus, active_motors, goals, phase)
        write_row(log_file, last)
        if all(
            abs(last["error_counts"][name]) <= POSITION_TOLERANCE
            for name in active_motors
        ):
            consecutive += 1
            if consecutive >= 3:
                return
        else:
            consecutive = 0
        time.sleep(1.0 / rate)
    raise RuntimeError(
        f"{phase} did not converge: errors={last['error_counts'] if last else None}"
    )


def main() -> int:
    args = parse_args()

    def interrupt_for_cleanup(_signum, _frame) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupt_for_cleanup)
    calibration = load_calibration(args.calibration)
    mapping = PolicyJointMapping(args.mapping)
    active_motors = [MOTOR_ORDER[i] for i in args.active_indices]
    bus = FeetechMotorsBus(args.port, MOTORS, calibration)
    log_file = None
    torque_enabled = False
    try:
        bus.connect(handshake=True)
        torque = bus.sync_read("Torque_Enable", normalize=False, num_retry=2)
        if any(int(value) != 0 for value in torque.values()):
            raise RuntimeError(f"refusing because torque is already enabled: {torque}")
        modes = bus.sync_read(
            "Operating_Mode", active_motors, normalize=False, num_retry=2
        )
        if any(int(value) != 0 for value in modes.values()):
            raise RuntimeError(f"selected motor is not in position mode: {modes}")

        normalized = bus.sync_read(
            "Present_Position", normalize=True, num_retry=2
        )
        current_policy = mapping.convert(
            {name: float(normalized[name]) for name in MOTOR_ORDER}
        )
        target_policy = dict(current_policy)
        policy_limit_status = {}
        for index, delta in enumerate(args.deltas):
            joint = mapping.policy_joint_names[index]
            target_policy[joint] += delta
            if index not in args.active_indices:
                continue
            motor = MOTOR_ORDER[index]
            low, high = MUJOCO_LIMITS_RAD[motor]
            policy_limit_status[joint] = validate_policy_recovery_move(
                joint,
                current_policy[joint],
                target_policy[joint],
                low,
                high,
            )

        start_raw_all = bus.sync_read(
            "Present_Position", normalize=False, num_retry=2
        )
        target_raw_all = normalized_to_raw(
            policy_to_normalized(mapping, target_policy), calibration
        )
        start = {name: int(start_raw_all[name]) for name in active_motors}
        target = {name: int(target_raw_all[name]) for name in active_motors}
        raw_limit_status = {}
        for name in active_motors:
            low = calibration[name].range_min + RAW_MARGIN
            high = calibration[name].range_max - RAW_MARGIN
            hard_low = calibration[name].range_min
            hard_high = calibration[name].range_max
            if low <= start[name] <= high and low <= target[name] <= high:
                raw_limit_status[name] = "inside_safe_raw_interval"
                continue
            if (
                args.keep_target
                and hard_low <= start[name] < low
                and start[name] < target[name] <= high
            ):
                raw_limit_status[name] = "recovering_from_below_raw_margin"
                continue
            if (
                args.keep_target
                and high < start[name] <= hard_high
                and low <= target[name] < start[name]
            ):
                raw_limit_status[name] = "recovering_from_above_raw_margin"
                continue
            if not args.keep_target and not low <= start[name] <= high:
                detail = "auto-return would end near the calibrated hard limit"
            else:
                detail = "target does not move safely toward the raw interval"
            raise RuntimeError(
                f"{name} start/target outside safe raw interval "
                f"[{low}, {high}]: {start[name]} -> {target[name]}; {detail}"
            )

        args.log.parent.mkdir(parents=True, exist_ok=True)
        log_file = args.log.open("w", encoding="utf-8")
        write_row(
            log_file,
            {
                "timestamp": datetime.now().astimezone().isoformat(),
                "phase": "header",
                "active_motors": active_motors,
                "policy_joint_order": list(mapping.policy_joint_names),
                "delta_rad": list(args.deltas),
                "start_raw": start,
                "target_raw": target,
                "current_policy_rad": current_policy,
                "target_policy_rad": target_policy,
                "policy_limit_status": policy_limit_status,
                "raw_limit_status": raw_limit_status,
                "keep_target": bool(args.keep_target),
            },
        )

        bus.sync_write("Goal_Position", start, normalize=False)
        bus.enable_torque(active_motors, num_retry=2)
        torque_enabled = True
        time.sleep(0.3)
        move_segment(
            bus, active_motors, start, target, args.duration, args.rate,
            "outbound", log_file
        )
        settle(
            bus, active_motors, target, args.settle_timeout, args.rate,
            "outbound_settle", log_file
        )
        time.sleep(args.hold)
        if not args.keep_target:
            move_segment(
                bus, active_motors, target, start, args.duration, args.rate,
                "return", log_file
            )
            settle(
                bus, active_motors, start, args.settle_timeout, args.rate,
                "return_settle", log_file
            )
        return 0
    finally:
        if bus.is_connected and torque_enabled:
            bus.disable_torque(num_retry=5)
            after = bus.sync_read("Torque_Enable", normalize=False, num_retry=3)
            verification = {
                "timestamp": datetime.now().astimezone().isoformat(),
                "phase": "torque_off_verification",
                "torque_enable": {name: int(v) for name, v in after.items()},
                "all_torque_off": all(int(v) == 0 for v in after.values()),
            }
            if log_file:
                write_row(log_file, verification)
            if not verification["all_torque_off"]:
                raise RuntimeError(f"torque-off verification failed: {after}")
        if bus.is_connected:
            bus.disconnect(disable_torque=False)
        if log_file:
            log_file.close()


if __name__ == "__main__":
    raise SystemExit(main())
