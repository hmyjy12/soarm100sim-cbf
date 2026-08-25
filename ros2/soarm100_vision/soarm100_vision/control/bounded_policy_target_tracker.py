"""Bounded absolute target tracking for real-hardware policy commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

import numpy as np


class BoundedPolicyTargetTracker:
    """Accumulate shaped motion toward the current policy target without windup.

    The tracked command may lead measured joints so the position servos can
    move under load. It is bounded around measurement and by the policy target,
    training limits and hardware-facing command limits.
    """

    def __init__(self, joint_names: Sequence[str], max_lead_rad: np.ndarray) -> None:
        self.joint_names = tuple(joint_names)
        self.max_lead_rad = np.asarray(max_lead_rad, dtype=np.float64).reshape(-1)
        if self.max_lead_rad.size != len(self.joint_names):
            raise ValueError("policy-target lead limits do not match joint count")
        if np.any(~np.isfinite(self.max_lead_rad)) or np.any(self.max_lead_rad < 0.0):
            raise ValueError("policy-target lead limits must be finite and non-negative")
        if np.any(self.max_lead_rad > 0.20 + 1.0e-12):
            raise ValueError("policy-target lead limits must not exceed 0.20 rad")
        self.tracked_command: np.ndarray | None = None

    @classmethod
    def from_config(
        cls, path: Path, joint_names: Sequence[str]
    ) -> "BoundedPolicyTargetTracker":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if str(payload.get("mode", "")) != "bounded":
            raise ValueError("policy-target tracker config mode must be bounded")
        configured = payload.get("max_lead_rad", {})
        if not isinstance(configured, dict):
            raise ValueError("max_lead_rad must be a joint-name mapping")
        unknown = set(configured) - set(joint_names)
        if unknown:
            raise ValueError(f"unknown policy-target tracker joints: {sorted(unknown)}")
        limits = np.asarray(
            [float(configured.get(name, 0.0)) for name in joint_names],
            dtype=np.float64,
        )
        return cls(joint_names, limits)

    def reset(self, measured_q: np.ndarray | None = None) -> None:
        self.tracked_command = (
            None
            if measured_q is None
            else np.asarray(measured_q, dtype=np.float64).reshape(-1).copy()
        )

    def apply(
        self,
        measured_q: np.ndarray,
        policy_target: np.ndarray,
        shaped_velocity_rad_s: np.ndarray,
        q_low: np.ndarray,
        q_high: np.ndarray,
        dt_s: float,
        frozen_mask: np.ndarray | None = None,
    ) -> dict:
        q = np.asarray(measured_q, dtype=np.float64).reshape(-1)
        target = np.asarray(policy_target, dtype=np.float64).reshape(q.shape)
        velocity = np.asarray(shaped_velocity_rad_s, dtype=np.float64).reshape(q.shape)
        low = np.asarray(q_low, dtype=np.float64).reshape(q.shape)
        high = np.asarray(q_high, dtype=np.float64).reshape(q.shape)
        mask = (
            np.zeros(q.size, dtype=bool)
            if frozen_mask is None
            else np.asarray(frozen_mask, dtype=bool).reshape(q.shape)
        )
        if q.size != len(self.joint_names):
            raise ValueError("policy-target tracker command size does not match joints")
        if not np.isfinite(dt_s) or dt_s <= 0.0:
            raise ValueError("policy-target tracker dt must be positive and finite")
        if self.tracked_command is None:
            self.tracked_command = q.copy()

        previous = self.tracked_command
        candidate = previous + velocity * float(dt_s)
        # Clamp only a genuine overshoot along the current movement direction.
        # If the policy target jumps across the previous command, retain the
        # acceleration-shaped reversal instead of jumping directly across q.
        step = candidate - previous
        target_delta = target - previous
        overshot = (step * target_delta > 0.0) & (
            np.abs(step) > np.abs(target_delta)
        )
        candidate[overshot] = target[overshot]

        lead_low = q - self.max_lead_rad
        lead_high = q + self.max_lead_rad
        tracked = np.clip(candidate, np.maximum(low, lead_low), np.minimum(high, lead_high))
        tracked[mask] = q[mask]
        self.tracked_command = tracked.copy()
        return {
            "q_cmd": tracked,
            "lead_rad": tracked - q,
            "lead_limit_rad": self.max_lead_rad.copy(),
            "lead_clamped": np.abs(tracked - candidate) > 1.0e-9,
            "candidate_q": candidate,
        }
