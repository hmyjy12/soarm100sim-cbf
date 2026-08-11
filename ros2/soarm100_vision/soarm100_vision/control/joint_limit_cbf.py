"""Joint-space CBF velocity bounds for calibrated hardware limits."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class JointLimitCbfConfig:
    alpha: float = 4.0
    activation_margin_rad: float = 0.25
    recovery_velocity_rad_s: float = 0.05

    def __post_init__(self) -> None:
        if self.alpha <= 0.0:
            raise ValueError("alpha must be positive")
        if self.activation_margin_rad <= 0.0:
            raise ValueError("activation_margin_rad must be positive")
        if self.recovery_velocity_rad_s <= 0.0:
            raise ValueError("recovery_velocity_rad_s must be positive")


class JointLimitCbfFilter:
    """Build per-joint linear CBF bounds on commanded reference velocity."""

    def __init__(self, config: JointLimitCbfConfig) -> None:
        self.cfg = config

    def velocity_bounds(
        self,
        measured_q: np.ndarray,
        safe_low: np.ndarray,
        safe_high: np.ndarray,
    ) -> dict:
        q = np.asarray(measured_q, dtype=np.float64)
        low = np.asarray(safe_low, dtype=np.float64).reshape(q.shape)
        high = np.asarray(safe_high, dtype=np.float64).reshape(q.shape)
        if (
            np.any(low >= high)
            or not np.all(np.isfinite(q))
            or not np.all(np.isfinite(low))
            or not np.all(np.isfinite(high))
        ):
            raise ValueError("invalid joint CBF state or bounds")

        h_low = q - low
        h_high = high - q
        velocity_low = -self.cfg.alpha * h_low
        velocity_high = self.cfg.alpha * h_high

        below = h_low < 0.0
        above = h_high < 0.0
        velocity_low[below] = np.maximum(
            velocity_low[below], self.cfg.recovery_velocity_rad_s
        )
        velocity_high[above] = np.minimum(
            velocity_high[above], -self.cfg.recovery_velocity_rad_s
        )
        active = (
            (h_low <= self.cfg.activation_margin_rad)
            | (h_high <= self.cfg.activation_margin_rad)
        )
        return {
            "velocity_low_rad_s": velocity_low,
            "velocity_high_rad_s": velocity_high,
            "h_low_rad": h_low,
            "h_high_rad": h_high,
            "active": active,
            "outside": below | above,
        }
