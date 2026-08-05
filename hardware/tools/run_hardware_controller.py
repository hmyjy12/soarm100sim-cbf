#!/usr/bin/env python3
"""Persistent seven-axis Feetech controller using JSON lines on stdin/stdout."""

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

from hardware.so100_plus.config import MOTORS, MUJOCO_LIMITS_RAD
from hardware.so100_plus.joint_mapping import MOTOR_ORDER, PolicyJointMapping
from hardware.tools.test_multi_joint_delta import (
    normalized_to_raw,
    policy_to_normalized,
)


RAW_MARGIN = 100
MAX_COMMAND_DELTA_RAD = math.radians(20.0)
MAX_SPEED_RAD_S = math.radians(20.0)
SAFE_POSE_MAX_DELTA_RAD = math.radians(120.0)
SAFE_POSE_MAX_SPEED_RAD_S = math.radians(10.0)
POSITION_TOLERANCE = 12
TEMPERATURE_LIMIT_C = 55
SHOULDER_LIFT = "shoulder_lift"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument(
        "--calibration", type=Path,
        default=Path("hardware/calibration/lerobot/so100_plus_7dof.json"),
    )
    parser.add_argument(
        "--mapping", type=Path,
        default=Path("hardware/calibration/policy_joint_mapping.json"),
    )
    parser.add_argument(
        "--safe-pose", type=Path,
        default=Path("hardware/calibration/hardware_safe_pose.json"),
    )
    parser.add_argument("--rate", type=float, default=20.0)
    parser.add_argument("--shoulder-lift-p", type=int, default=16)
    parser.add_argument("--baseline-shoulder-lift-p", type=int, default=16)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    if not 10.0 <= args.rate <= 50.0:
        parser.error("--rate must be within [10, 50]")
    if not 1 <= args.shoulder_lift_p <= 64:
        parser.error("--shoulder-lift-p must be within [1, 64]")
    if not 1 <= args.baseline_shoulder_lift_p <= 64:
        parser.error("--baseline-shoulder-lift-p must be within [1, 64]")
    return args


def emit(**values) -> None:
    print(json.dumps(values, ensure_ascii=True), flush=True)


class Controller:
    def __init__(self, args: argparse.Namespace):
        raw_calibration = json.loads(args.calibration.read_text())
        self.calibration = {
            name: MotorCalibration(**raw_calibration[name])
            for name in MOTOR_ORDER
        }
        self.mapping = PolicyJointMapping(args.mapping)
        self.safe_pose = json.loads(args.safe_pose.read_text())
        if not all(
            self.safe_pose.get(flag) is True
            for flag in (
                "automatic_validation_passed",
                "user_visual_approval",
                "approved_for_recovery_motion",
            )
        ):
            raise RuntimeError("hardware_safe pose is not fully approved")
        self.bus = FeetechMotorsBus(args.port, MOTORS, self.calibration)
        self.rate = args.rate
        self.shoulder_lift_p = args.shoulder_lift_p
        self.baseline_shoulder_lift_p = args.baseline_shoulder_lift_p
        self.log_path = args.log
        self.log_file = None
        self.torque_enabled = False

    def connect_and_hold(self) -> None:
        self.bus.connect(handshake=True)
        torque = self.bus.sync_read("Torque_Enable", normalize=False, num_retry=3)
        if any(int(value) != 0 for value in torque.values()):
            raise RuntimeError(f"startup requires all torque disabled: {torque}")
        modes = self.bus.sync_read("Operating_Mode", normalize=False, num_retry=3)
        if any(int(value) != 0 for value in modes.values()):
            raise RuntimeError(f"all motors must use position mode: {modes}")
        original_p = int(
            self.bus.read(
                "P_Coefficient", SHOULDER_LIFT, normalize=False, num_retry=3
            )
        )
        # Recover the known baseline first in case a previous process was killed.
        if original_p != self.baseline_shoulder_lift_p:
            self.bus.write(
                "P_Coefficient", SHOULDER_LIFT,
                self.baseline_shoulder_lift_p, normalize=False, num_retry=3,
            )
        self.bus.write(
            "P_Coefficient", SHOULDER_LIFT,
            self.shoulder_lift_p, normalize=False, num_retry=3,
        )
        applied_p = int(
            self.bus.read(
                "P_Coefficient", SHOULDER_LIFT, normalize=False, num_retry=3
            )
        )
        if applied_p != self.shoulder_lift_p:
            raise RuntimeError(
                f"shoulder_lift P write verification failed: {applied_p}"
            )
        current = self.bus.sync_read("Present_Position", normalize=False, num_retry=3)
        goals = {name: int(current[name]) for name in MOTOR_ORDER}
        # Seed every target with its current position before enabling torque.
        self.bus.sync_write("Goal_Position", goals, normalize=False)
        self.bus.enable_torque(list(MOTOR_ORDER), num_retry=3)
        self.torque_enabled = True
        time.sleep(0.3)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_path.open("a", encoding="utf-8")
        self._log(
            "startup_hold", goal_raw=goals,
            shoulder_lift_p_original=original_p,
            shoulder_lift_p_applied=applied_p,
        )

    def current_policy(self) -> tuple[dict[str, float], dict[str, int]]:
        normalized = self.bus.sync_read(
            "Present_Position", normalize=True, num_retry=3
        )
        raw = self.bus.sync_read("Present_Position", normalize=False, num_retry=3)
        policy = self.mapping.convert(
            {name: float(normalized[name]) for name in MOTOR_ORDER}
        )
        return policy, {name: int(raw[name]) for name in MOTOR_ORDER}

    def move(self, target_values: list[float], duration: float) -> dict:
        if not self.torque_enabled:
            raise RuntimeError("torque is disabled")
        if len(target_values) != 7 or not all(map(math.isfinite, target_values)):
            raise RuntimeError("target must contain seven finite policy radians")
        names = list(self.mapping.policy_joint_names)
        target_policy = dict(zip(names, target_values))
        safe_values = [
            float(value) for value in self.safe_pose["policy_position_rad"]
        ]
        approved_safe_return = all(
            abs(value - safe) <= 1.0e-4
            for value, safe in zip(target_values, safe_values)
        )
        max_delta = (
            SAFE_POSE_MAX_DELTA_RAD
            if approved_safe_return
            else MAX_COMMAND_DELTA_RAD
        )
        max_speed = (
            SAFE_POSE_MAX_SPEED_RAD_S
            if approved_safe_return
            else MAX_SPEED_RAD_S
        )
        current_policy, start_raw = self.current_policy()
        for motor, joint in zip(MOTOR_ORDER, names):
            low, high = MUJOCO_LIMITS_RAD[motor]
            if not low <= target_policy[joint] <= high:
                raise RuntimeError(
                    f"{joint} target {target_policy[joint]:+.4f} outside "
                    f"[{low:+.4f}, {high:+.4f}]"
                )
            delta = target_policy[joint] - current_policy[joint]
            if abs(delta) > max_delta:
                raise RuntimeError(
                    f"{joint} command delta {math.degrees(delta):+.1f}deg "
                    f"exceeds {'approved-safe-return 120deg' if approved_safe_return else 'first-stage 20deg'} limit"
                )
        required_duration = max(
            abs(target_policy[name] - current_policy[name]) / max_speed
            for name in names
        )
        duration = max(float(duration), required_duration, 0.5)
        target_raw = normalized_to_raw(
            policy_to_normalized(self.mapping, target_policy), self.calibration
        )
        for motor in MOTOR_ORDER:
            low = self.calibration[motor].range_min + RAW_MARGIN
            high = self.calibration[motor].range_max - RAW_MARGIN
            if not low <= target_raw[motor] <= high:
                raise RuntimeError(
                    f"{motor} raw target {target_raw[motor]} outside "
                    f"safe interval [{low}, {high}]"
                )

        steps = max(2, round(duration * self.rate))
        for index in range(1, steps + 1):
            ratio = index / steps
            goals = {
                name: round(
                    start_raw[name]
                    + (target_raw[name] - start_raw[name]) * ratio
                )
                for name in MOTOR_ORDER
            }
            self.bus.sync_write("Goal_Position", goals, normalize=False)
            if index == 1 or index == steps or index % 10 == 0:
                self._check_health(goals, "motion")
            time.sleep(duration / steps)
        deadline = time.monotonic() + 2.0
        consecutive = 0
        telemetry = None
        while time.monotonic() < deadline:
            self.bus.sync_write("Goal_Position", target_raw, normalize=False)
            telemetry = self._check_health(target_raw, "settle")
            if all(
                abs(value) <= POSITION_TOLERANCE
                for value in telemetry["error_counts"].values()
            ):
                consecutive += 1
                if consecutive >= 3:
                    break
            else:
                consecutive = 0
            time.sleep(1.0 / self.rate)
        errors = telemetry["error_counts"] if telemetry else {}
        if consecutive < 3:
            raise RuntimeError(f"target did not converge: errors={errors}")
        return {
            "duration": duration,
            "approved_safe_return": approved_safe_return,
            "target_policy_rad": target_policy,
            "target_raw": target_raw,
            "final_error_counts": errors,
        }

    def _check_health(self, goals: dict[str, int], phase: str) -> dict:
        position = self.bus.sync_read(
            "Present_Position", normalize=False, num_retry=3
        )
        temperature = self.bus.sync_read(
            "Present_Temperature", normalize=False, num_retry=3
        )
        current = self.bus.sync_read(
            "Present_Current", normalize=False, num_retry=3
        )
        load = self.bus.sync_read("Present_Load", normalize=False, num_retry=3)
        temperatures = {name: int(temperature[name]) for name in MOTOR_ORDER}
        if any(value >= 45 for value in temperatures.values()):
            samples = [temperatures]
            for _ in range(2):
                time.sleep(0.02)
                reread = self.bus.sync_read(
                    "Present_Temperature", normalize=False, num_retry=3
                )
                samples.append(
                    {name: int(reread[name]) for name in MOTOR_ORDER}
                )
            temperatures = {
                name: sorted(sample[name] for sample in samples)[1]
                for name in MOTOR_ORDER
            }
        if any(value >= TEMPERATURE_LIMIT_C for value in temperatures.values()):
            raise RuntimeError(f"temperature protection: {temperatures}")
        row = {
            "goal_raw": goals,
            "position_raw": {name: int(position[name]) for name in MOTOR_ORDER},
            "error_counts": {
                name: int(goals[name]) - int(position[name])
                for name in MOTOR_ORDER
            },
            "temperature_c": temperatures,
            "current_raw": {
                name: int(current[name]) for name in MOTOR_ORDER
            },
            "load_raw": {name: int(load[name]) for name in MOTOR_ORDER},
        }
        self._log(phase, **row)
        return row

    def _log(self, phase: str, **values) -> None:
        if not self.log_file:
            return
        row = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "phase": phase,
            **values,
        }
        self.log_file.write(json.dumps(row, ensure_ascii=True) + "\n")
        self.log_file.flush()

    def disable(self) -> None:
        if self.bus.is_connected:
            self.bus.disable_torque(num_retry=5)
            torque = self.bus.sync_read("Torque_Enable", normalize=False, num_retry=3)
            self.torque_enabled = False
            self.bus.write(
                "P_Coefficient", SHOULDER_LIFT,
                self.baseline_shoulder_lift_p, normalize=False, num_retry=3,
            )
            restored_p = int(
                self.bus.read(
                    "P_Coefficient", SHOULDER_LIFT,
                    normalize=False, num_retry=3,
                )
            )
            self._log(
                "torque_off_verification",
                torque_enable={name: int(value) for name, value in torque.items()},
                shoulder_lift_p_restored=restored_p,
            )
            if any(int(value) != 0 for value in torque.values()):
                raise RuntimeError(f"torque-off verification failed: {torque}")
            if restored_p != self.baseline_shoulder_lift_p:
                raise RuntimeError(
                    f"shoulder_lift P restore failed: {restored_p}"
                )

    def close(self) -> None:
        try:
            self.disable()
        finally:
            if self.bus.is_connected:
                self.bus.disconnect(disable_torque=False)
            if self.log_file:
                self.log_file.close()


def main() -> int:
    args = parse_args()
    controller = Controller(args)
    stopping = False

    def request_stop(_signum, _frame) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    try:
        controller.connect_and_hold()
        emit(event="ready", success=True, reason="current position held")
        while not stopping:
            readable, _, _ = select.select([sys.stdin], [], [], 0.5)
            if not readable:
                _policy, current_raw = controller.current_policy()
                controller._check_health(current_raw, "idle_health")
                continue
            line = sys.stdin.readline()
            if not line:
                break
            request = json.loads(line)
            request_id = str(request.get("request_id", ""))
            try:
                action = request.get("action")
                if action == "move":
                    result = controller.move(
                        [float(v) for v in request["position_rad"]],
                        float(request.get("duration", 3.0)),
                    )
                    emit(request_id=request_id, success=True, result=result)
                elif action == "disable":
                    controller.disable()
                    emit(request_id=request_id, success=True, reason="all torque disabled")
                elif action == "status":
                    policy, raw = controller.current_policy()
                    emit(
                        request_id=request_id, success=True,
                        torque_enabled=controller.torque_enabled,
                        policy=policy, raw=raw,
                    )
                else:
                    raise RuntimeError(f"unsupported action: {action!r}")
            except Exception as exc:
                if "temperature protection" in str(exc):
                    controller.disable()
                emit(request_id=request_id, success=False, reason=str(exc))
    except Exception as exc:
        emit(event="fatal", success=False, reason=str(exc))
        return 1
    finally:
        controller.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
