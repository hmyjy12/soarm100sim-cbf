#!/usr/bin/env python3
"""Interactively check individual servos while all seven axes remain powered."""

from __future__ import annotations

import argparse
import json
import math
import select
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


MOTOR_ORDER = tuple(MOTORS)
COUNTS_PER_TURN = 4095
TEMPERATURE_LIMIT_C = 55


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--calibration",
        type=Path,
        default=Path("hardware/calibration/lerobot/so100_plus_new_arm.json"),
    )
    parser.add_argument("--max-angle-deg", type=float, default=20.0)
    parser.add_argument("--speed-deg-s", type=float, default=5.0)
    parser.add_argument("--rate", type=float, default=20.0)
    parser.add_argument("--settle-timeout", type=float, default=2.0)
    parser.add_argument("--position-tolerance-counts", type=int, default=15)
    parser.add_argument("--limit-margin-counts", type=int, default=100)
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("logs/hardware/interactive_joint_check.jsonl"),
    )
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    if args.confirm != "RUN_INTERACTIVE_JOINT_CHECK":
        parser.error("--confirm must be exactly RUN_INTERACTIVE_JOINT_CHECK")
    if not 0.0 < args.max_angle_deg <= 20.0:
        parser.error("--max-angle-deg must be within (0, 20]")
    if not 1.0 <= args.speed_deg_s <= 10.0:
        parser.error("--speed-deg-s must be within [1, 10]")
    if not 10.0 <= args.rate <= 50.0:
        parser.error("--rate must be within [10, 50]")
    if not 0.5 <= args.settle_timeout <= 5.0:
        parser.error("--settle-timeout must be within [0.5, 5.0]")
    if not 5 <= args.position_tolerance_counts <= 30:
        parser.error("--position-tolerance-counts must be within [5, 30]")
    if args.limit_margin_counts < 50:
        parser.error("--limit-margin-counts must be at least 50")
    return args


def load_calibration(path: Path) -> dict[str, MotorCalibration]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if set(raw) != set(MOTOR_ORDER):
        raise RuntimeError("calibration does not contain the expected seven motors")
    return {name: MotorCalibration(**raw[name]) for name in MOTOR_ORDER}


class InteractiveJointCheck:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.calibration = load_calibration(args.calibration)
        self.bus = FeetechMotorsBus(args.port, MOTORS, self.calibration)
        self.goals: dict[str, int] = {}
        self.log_file = None
        self.torque_enabled = False

    def log(self, phase: str, **values) -> None:
        if self.log_file is None:
            return
        row = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "phase": phase,
            **values,
        }
        self.log_file.write(json.dumps(row, ensure_ascii=True) + "\n")
        self.log_file.flush()

    def start(self) -> None:
        self.bus.connect(handshake=True)
        torque = self.bus.sync_read("Torque_Enable", normalize=False, num_retry=3)
        if any(int(value) != 0 for value in torque.values()):
            raise RuntimeError(f"startup requires all torque disabled: {torque}")
        modes = self.bus.sync_read("Operating_Mode", normalize=False, num_retry=3)
        if any(int(value) != 0 for value in modes.values()):
            raise RuntimeError(f"all motors must be in position mode: {modes}")

        position = self.bus.sync_read("Present_Position", normalize=False, num_retry=3)
        self.goals = {name: int(position[name]) for name in MOTOR_ORDER}
        self.bus.sync_write("Goal_Position", self.goals, normalize=False)
        self.bus.enable_torque(list(MOTOR_ORDER), num_retry=3)
        self.torque_enabled = True
        time.sleep(0.3)

        self.args.log.parent.mkdir(parents=True, exist_ok=True)
        self.log_file = self.args.log.open("w", encoding="utf-8")
        self.log("startup_hold", goal_raw=self.goals)
        print("[joint_check] all seven motors powered; current pose is held")

    def telemetry(self, phase: str) -> dict:
        position = self.bus.sync_read("Present_Position", normalize=False, num_retry=3)
        current = self.bus.sync_read("Present_Current", normalize=False, num_retry=3)
        load = self.bus.sync_read("Present_Load", normalize=False, num_retry=3)
        temperature = self.bus.sync_read(
            "Present_Temperature", normalize=False, num_retry=3
        )
        temperatures = {name: int(temperature[name]) for name in MOTOR_ORDER}
        if any(value >= TEMPERATURE_LIMIT_C for value in temperatures.values()):
            raise RuntimeError(f"temperature protection triggered: {temperatures}")
        row = {
            "goal_raw": self.goals.copy(),
            "position_raw": {name: int(position[name]) for name in MOTOR_ORDER},
            "error_counts": {
                name: self.goals[name] - int(position[name]) for name in MOTOR_ORDER
            },
            "current_raw": {name: int(current[name]) for name in MOTOR_ORDER},
            "load_raw": {name: int(load[name]) for name in MOTOR_ORDER},
            "temperature_c": temperatures,
        }
        self.log(phase, **row)
        return row

    def validate_target(self, motor: str, angle_deg: float) -> tuple[int, int, int]:
        if not math.isfinite(angle_deg) or abs(angle_deg) < 1.0e-9:
            raise ValueError("angle must be finite and non-zero")
        if abs(angle_deg) > self.args.max_angle_deg:
            raise ValueError(
                f"requested {angle_deg:+.2f}deg exceeds "
                f"+/-{self.args.max_angle_deg:.1f}deg per command"
            )
        measured = int(
            self.bus.read("Present_Position", motor, normalize=False, num_retry=3)
        )
        start_goal = self.goals[motor]
        delta_counts = round(angle_deg * COUNTS_PER_TURN / 360.0)
        target = start_goal + delta_counts
        cal = self.calibration[motor]
        safe_low = cal.range_min + self.args.limit_margin_counts
        safe_high = cal.range_max - self.args.limit_margin_counts
        if not safe_low <= target <= safe_high:
            raise ValueError(
                f"target_raw={target} outside safe interval [{safe_low}, {safe_high}]; "
                f"held_raw={start_goal}, measured_raw={measured}"
            )
        if abs(measured - start_goal) > 80:
            raise ValueError(
                f"measured position is {measured - start_goal:+d} counts away from the "
                "held target; inspect load/mechanics before another move"
            )
        return start_goal, target, measured

    def move(self, motor: str, angle_deg: float) -> None:
        start, target, measured = self.validate_target(motor, angle_deg)
        duration = max(abs(angle_deg) / self.args.speed_deg_s, 0.5)
        steps = max(2, round(duration * self.args.rate))
        print(
            f"[joint_check] MOVE id={MOTORS[motor].id} motor={motor} "
            f"angle={angle_deg:+.2f}deg raw={start}->{target} "
            f"measured={measured} duration={duration:.2f}s"
        )
        self.log(
            "command",
            motor=motor,
            motor_id=MOTORS[motor].id,
            angle_deg=angle_deg,
            start_goal_raw=start,
            start_measured_raw=measured,
            target_raw=target,
            duration_s=duration,
        )

        for index in range(1, steps + 1):
            ratio = index / steps
            self.goals[motor] = round(start + (target - start) * ratio)
            self.bus.sync_write("Goal_Position", self.goals, normalize=False)
            if index == 1 or index == steps or index % 10 == 0:
                row = self.telemetry("motion")
                print(
                    f"\r  goal={self.goals[motor]} "
                    f"pos={row['position_raw'][motor]} "
                    f"err={row['error_counts'][motor]:+d} "
                    f"current={row['current_raw'][motor]} "
                    f"load={row['load_raw'][motor]} "
                    f"temp={row['temperature_c'][motor]}C",
                    end="",
                    flush=True,
                )
            time.sleep(duration / steps)
        print()
        self.goals[motor] = target

        deadline = time.monotonic() + self.args.settle_timeout
        consecutive = 0
        last = None
        while time.monotonic() < deadline:
            self.bus.sync_write("Goal_Position", self.goals, normalize=False)
            last = self.telemetry("settle")
            if abs(last["error_counts"][motor]) <= self.args.position_tolerance_counts:
                consecutive += 1
                if consecutive >= 3:
                    break
            else:
                consecutive = 0
            time.sleep(1.0 / self.args.rate)

        assert last is not None
        status = "PASS" if consecutive >= 3 else "NOT_CONVERGED"
        print(
            f"[joint_check] {status} motor={motor} "
            f"goal={target} pos={last['position_raw'][motor]} "
            f"err={last['error_counts'][motor]:+d}counts; new pose remains held"
        )
        self.log("result", status=status, motor=motor, telemetry=last)

    def print_menu(self) -> None:
        print("\nMotor IDs:")
        for name in MOTOR_ORDER:
            cal = self.calibration[name]
            print(
                f"  {MOTORS[name].id}: {name:<14} "
                f"calibrated_raw=[{cal.range_min}, {cal.range_max}]"
            )
        print(
            f"Enter an ID, then a signed relative angle within "
            f"+/-{self.args.max_angle_deg:.1f}deg. Enter q to torque off and quit."
        )

    def prompt(self, text: str) -> str:
        """Wait for terminal input while refreshing hold targets and health checks."""
        print(text, end="", flush=True)
        while True:
            readable, _, _ = select.select([sys.stdin], [], [], 1.0)
            if readable:
                line = sys.stdin.readline()
                if not line:
                    raise EOFError("terminal input closed")
                return line.strip()
            self.bus.sync_write("Goal_Position", self.goals, normalize=False)
            self.telemetry("idle_health")

    def run(self) -> None:
        id_to_motor = {str(MOTORS[name].id): name for name in MOTOR_ORDER}
        self.print_menu()
        while True:
            choice = self.prompt("\nMotor ID [1-7, q]: ").lower()
            if choice == "q":
                return
            motor = id_to_motor.get(choice)
            if motor is None:
                print("REFUSE ID: choose one of 1,2,3,4,5,6,7 or q")
                continue
            value = self.prompt(
                f"Relative angle for {motor} in degrees "
                f"[-{self.args.max_angle_deg:g}, +{self.args.max_angle_deg:g}]: "
            )
            try:
                angle = float(value)
                self.move(motor, angle)
            except ValueError as exc:
                print(f"REFUSE ANGLE: {exc}")

    def close(self) -> None:
        try:
            if self.bus.is_connected and self.torque_enabled:
                self.bus.disable_torque(num_retry=5)
                torque = self.bus.sync_read(
                    "Torque_Enable", normalize=False, num_retry=3
                )
                self.torque_enabled = False
                self.log(
                    "torque_off_verification",
                    torque_enable={name: int(value) for name, value in torque.items()},
                )
                print(f"[joint_check] torque verification={torque}")
                if any(int(value) != 0 for value in torque.values()):
                    raise RuntimeError(f"torque-off verification failed: {torque}")
        finally:
            if self.bus.is_connected:
                self.bus.disconnect(disable_torque=False)
            if self.log_file is not None:
                self.log_file.close()


def main() -> int:
    args = parse_args()
    checker = InteractiveJointCheck(args)

    def interrupt(_signum, _frame) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, interrupt)
    try:
        checker.start()
        checker.run()
        return 0
    except EOFError as exc:
        print(f"\n[joint_check] {exc}; disabling all torque")
        return 1
    except KeyboardInterrupt:
        print("\n[joint_check] interrupted; disabling all torque")
        return 130
    finally:
        checker.close()


if __name__ == "__main__":
    raise SystemExit(main())
