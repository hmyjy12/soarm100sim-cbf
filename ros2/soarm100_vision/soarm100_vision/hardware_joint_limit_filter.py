from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path

import numpy as np


MOTOR_ORDER = (
    "shoulder_pan",
    "shoulder_lift",
    "elbow_flex",
    "wrist_flex",
    "wrist_yaw",
    "wrist_roll",
    "gripper",
)
COUNTS_PER_TURN = 4095.0


@dataclass(frozen=True)
class HardwareLimitCheck:
    accepted: bool
    reason: str
    raw: dict[str, int]


class HardwareJointLimitFilter:
    """Map policy radians to calibrated motor counts and enforce safe ranges."""

    def __init__(
        self,
        *,
        repo_root: Path,
        calibration_json: str,
        mapping_json: str,
        margin_counts: int = 100,
        gripper_rad: float = 0.45,
    ) -> None:
        repo = Path(repo_root).expanduser().resolve()
        self.calibration = self._read_json(repo, calibration_json)
        self.mapping = self._read_json(repo, mapping_json)
        self.margin_counts = max(int(margin_counts), 0)
        self.gripper_rad = float(gripper_rad)
        joints = self.mapping.get("joints", {})
        if tuple(joints) != MOTOR_ORDER:
            raise ValueError(f"hardware mapping order mismatch: {tuple(joints)}")
        for motor in MOTOR_ORDER:
            if motor not in self.calibration:
                raise ValueError(f"hardware calibration missing motor: {motor}")
            if joints[motor].get("status") != "verified":
                raise ValueError(f"hardware mapping is not verified: {motor}")

    @staticmethod
    def _read_json(repo: Path, value: str) -> dict:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = repo / path
        return json.loads(path.read_text(encoding="utf-8"))

    def check_arm_q(self, q: np.ndarray, *, stage: str) -> HardwareLimitCheck:
        arm = np.asarray(q, dtype=np.float64).reshape(-1)
        if arm.size < 6 or not np.all(np.isfinite(arm[:6])):
            return HardwareLimitCheck(False, f"{stage}:invalid_policy_q", {})

        policy_names = [
            self.mapping["joints"][motor]["policy_joint"] for motor in MOTOR_ORDER
        ]
        policy = dict(zip(policy_names[:6], (float(x) for x in arm[:6])))
        policy[policy_names[6]] = self.gripper_rad
        raw: dict[str, int] = {}
        failures: list[str] = []
        for motor in MOTOR_ORDER:
            cfg = self.mapping["joints"][motor]
            cal = self.calibration[motor]
            value = policy[cfg["policy_joint"]]
            if motor == "gripper":
                normalized = (
                    value - float(cfg["zero_offset_rad"])
                ) / float(cfg["scale_rad_per_percent"])
                count = int(
                    normalized / 100.0
                    * (int(cal["range_max"]) - int(cal["range_min"]))
                    + int(cal["range_min"])
                )
            else:
                normalized_deg = math.degrees(
                    (value - float(cfg["zero_offset_rad"])) / float(cfg["sign"])
                )
                midpoint = 0.5 * (
                    int(cal["range_min"]) + int(cal["range_max"])
                )
                count = int(normalized_deg * COUNTS_PER_TURN / 360.0 + midpoint)
            raw[motor] = count
            safe_low = int(cal["range_min"]) + self.margin_counts
            safe_high = int(cal["range_max"]) - self.margin_counts
            if not safe_low <= count <= safe_high:
                failures.append(f"{motor}={count} notin[{safe_low},{safe_high}]")
        reason = f"{stage}:" + ("ok" if not failures else ";".join(failures))
        return HardwareLimitCheck(not failures, reason, raw)

    def policy_safe_bounds(self) -> tuple[np.ndarray, np.ndarray]:
        """Return calibrated safe intervals in policy radians."""
        low = np.empty(len(MOTOR_ORDER), dtype=np.float64)
        high = np.empty(len(MOTOR_ORDER), dtype=np.float64)
        for index, motor in enumerate(MOTOR_ORDER):
            cfg = self.mapping["joints"][motor]
            cal = self.calibration[motor]
            raw_low = int(cal["range_min"]) + self.margin_counts
            raw_high = int(cal["range_max"]) - self.margin_counts
            if raw_low >= raw_high:
                raise ValueError(f"empty hardware safe interval: {motor}")
            if motor == "gripper":
                span = int(cal["range_max"]) - int(cal["range_min"])
                values = [
                    (raw - int(cal["range_min"])) / span * 100.0
                    * float(cfg["scale_rad_per_percent"])
                    + float(cfg["zero_offset_rad"])
                    for raw in (raw_low, raw_high)
                ]
            else:
                midpoint = 0.5 * (
                    int(cal["range_min"]) + int(cal["range_max"])
                )
                values = [
                    float(cfg["sign"])
                    * math.radians((raw - midpoint) * 360.0 / COUNTS_PER_TURN)
                    + float(cfg["zero_offset_rad"])
                    for raw in (raw_low, raw_high)
                ]
            low[index], high[index] = min(values), max(values)
        return low, high
