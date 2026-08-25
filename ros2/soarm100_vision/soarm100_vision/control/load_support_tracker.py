"""Optional position bias for gravity-loaded real-hardware joints."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
@dataclass(frozen=True)
class JointLoadSupportConfig:
    direction: float
    bias_rad: float
    max_bias_rad: float
    ramp_rate_rad_s: float

    def __post_init__(self) -> None:
        if self.direction not in (-1.0, 1.0):
            raise ValueError("load-support direction must be exactly -1 or +1")
        if not 0.0 <= self.bias_rad <= self.max_bias_rad <= 0.20:
            raise ValueError("load-support bias must satisfy 0 <= bias <= max <= 0.20 rad")
        if not 0.001 <= self.ramp_rate_rad_s <= 0.20:
            raise ValueError("load-support ramp rate must be within [0.001, 0.20] rad/s")


class PositionGravityBias:
    """Add a bounded, ramped position bias before hardware mapping.

    This is not torque-model gravity compensation. It deliberately creates a
    small position error so the servo's internal position loop can generate
    holding effort. The module is real-hardware-only and disabled by default.
    """

    def __init__(
        self,
        joint_names: Sequence[str],
        joint_configs: dict[str, JointLoadSupportConfig],
    ) -> None:
        self.joint_names = tuple(joint_names)
        unknown = set(joint_configs) - set(self.joint_names)
        if unknown:
            raise ValueError(f"unknown load-support joints: {sorted(unknown)}")
        self.configs = dict(joint_configs)
        self.bias_state_rad = np.zeros(len(self.joint_names), dtype=np.float64)

    @classmethod
    def from_config(
        cls, path: Path, joint_names: Sequence[str]
    ) -> "PositionGravityBias":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if str(payload.get("mode", "")) != "position_gravity_bias":
            raise ValueError("load-support config mode must be position_gravity_bias")
        entries = payload.get("joints", {})
        if not isinstance(entries, dict) or not entries:
            raise ValueError("load-support config must contain at least one joint")
        configs = {
            str(name): JointLoadSupportConfig(
                direction=float(values["direction"]),
                bias_rad=float(values["bias_rad"]),
                max_bias_rad=float(values["max_bias_rad"]),
                ramp_rate_rad_s=float(values["ramp_rate_rad_s"]),
            )
            for name, values in entries.items()
        }
        return cls(joint_names, configs)

    def reset(self) -> None:
        self.bias_state_rad.fill(0.0)

    def apply(
        self,
        base_command: np.ndarray,
        q_low: np.ndarray,
        q_high: np.ndarray,
        dt_s: float,
    ) -> dict:
        command = np.asarray(base_command, dtype=np.float64).reshape(-1)
        low = np.asarray(q_low, dtype=np.float64).reshape(command.shape)
        high = np.asarray(q_high, dtype=np.float64).reshape(command.shape)
        if command.size != len(self.joint_names):
            raise ValueError("load-support command size does not match joint names")
        if not np.isfinite(dt_s) or dt_s <= 0.0:
            raise ValueError("load-support dt must be positive and finite")

        requested_bias = np.zeros_like(command)
        for name, cfg in self.configs.items():
            index = self.joint_names.index(name)
            target = min(cfg.bias_rad, cfg.max_bias_rad)
            step = cfg.ramp_rate_rad_s * float(dt_s)
            current = self.bias_state_rad[index]
            self.bias_state_rad[index] = current + np.clip(target - current, -step, step)
            requested_bias[index] = cfg.direction * self.bias_state_rad[index]

        supported = np.clip(command + requested_bias, low, high)
        applied_bias = supported - command
        return {
            "q_cmd": supported,
            "requested_bias_rad": requested_bias,
            "applied_bias_rad": applied_bias,
            "bias_magnitude_rad": self.bias_state_rad.copy(),
            "limit_clamped": np.abs(applied_bias - requested_bias) > 1.0e-9,
        }
