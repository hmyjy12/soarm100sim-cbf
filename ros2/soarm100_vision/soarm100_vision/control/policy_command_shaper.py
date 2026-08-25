"""Turn discrete policy actions into continuous, bounded joint references."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _alpha(dt: float, tau: float) -> float:
    """Discrete first-order low-pass coefficient for the measured interval."""
    return float(dt / (max(tau, 1.0e-6) + dt))


@dataclass(frozen=True)
class ShaperConfig:
    nominal_rate_hz: float = 20.0
    action_scale_rad: float = 0.25
    action_filter_tau_s: float = 0.08
    velocity_filter_tau_s: float = 0.12
    max_velocity_rad_s: float = 0.20
    max_acceleration_rad_s2: float = 0.80
    # Diagnostic threshold for a previous command that the measured joints did
    # not follow. It does not clamp normal policy commands.
    max_tracking_error_rad: float = 0.25
    action_deadband: float = 0.01
    min_dt_s: float = 0.01
    max_dt_s: float = 0.15

    def __post_init__(self) -> None:
        if not 5.0 <= self.nominal_rate_hz <= 50.0:
            raise ValueError("nominal_rate_hz must be within [5, 50]")
        for name in (
            "action_scale_rad",
            "action_filter_tau_s",
            "velocity_filter_tau_s",
            "max_velocity_rad_s",
            "max_acceleration_rad_s2",
            "max_tracking_error_rad",
        ):
            if float(getattr(self, name)) <= 0.0:
                raise ValueError(f"{name} must be positive")
        if not 0.0 <= self.action_deadband < 1.0:
            raise ValueError("action_deadband must be within [0, 1)")
        if not 0.0 < self.min_dt_s <= self.max_dt_s:
            raise ValueError("invalid dt bounds")


class PolicyCommandShaper:
    """State estimator and command governor shared by real policy controllers.

    Every policy target is anchored to the latest measured joints, matching the
    training contract ``q_target = q_measured + action_scale * action``.  The
    previous command is retained only for tracking diagnostics, never as an
    integration origin for the next command.
    """

    def __init__(self, config: ShaperConfig, joint_count: int = 7) -> None:
        self.cfg = config
        self.n = int(joint_count)
        if self.n <= 0:
            raise ValueError("joint_count must be positive")
        self.reset()

    def reset(self) -> None:
        self.last_time_s: float | None = None
        self.previous_q: np.ndarray | None = None
        self.filtered_qvel = np.zeros(self.n, dtype=np.float64)
        self.filtered_action = np.zeros(self.n, dtype=np.float64)
        self.reference_velocity = np.zeros(self.n, dtype=np.float64)
        self.q_ref: np.ndarray | None = None

    def clear_action_state(self) -> None:
        self.filtered_action.fill(0.0)
        self.reference_velocity.fill(0.0)

    def observe(self, q: np.ndarray, sample_time_s: float) -> dict:
        measured = np.asarray(q, dtype=np.float64).reshape(self.n)
        if not np.all(np.isfinite(measured)) or not np.isfinite(sample_time_s):
            raise ValueError("non-finite measured state")

        nominal_dt = 1.0 / self.cfg.nominal_rate_hz
        if self.previous_q is None or self.last_time_s is None:
            raw_dt = nominal_dt
            qvel_raw = np.zeros(self.n, dtype=np.float64)
            self.filtered_qvel.fill(0.0)
            self.q_ref = measured.copy()
        else:
            raw_dt = float(sample_time_s - self.last_time_s)
            if raw_dt <= 0.0:
                raise ValueError("joint-state timestamps must increase")
            qvel_raw = (measured - self.previous_q) / raw_dt

        dt = float(np.clip(raw_dt, self.cfg.min_dt_s, self.cfg.max_dt_s))
        velocity_alpha = _alpha(dt, self.cfg.velocity_filter_tau_s)
        self.filtered_qvel += velocity_alpha * (qvel_raw - self.filtered_qvel)
        self.previous_q = measured.copy()
        self.last_time_s = float(sample_time_s)
        return {
            "dt_s": dt,
            "raw_dt_s": raw_dt,
            "qvel_raw": qvel_raw.copy(),
            "qvel_filtered": self.filtered_qvel.copy(),
            "velocity_filter_alpha": velocity_alpha,
        }

    def shape(
        self,
        measured_q: np.ndarray,
        raw_action: np.ndarray,
        q_low: np.ndarray,
        q_high: np.ndarray,
        dt_s: float,
        frozen_mask: np.ndarray | None = None,
        safety_velocity_low: np.ndarray | None = None,
        safety_velocity_high: np.ndarray | None = None,
    ) -> dict:
        action = self.filter_action(raw_action, dt_s)
        return self.shape_filtered(
            measured_q,
            action["filtered_action"],
            q_low,
            q_high,
            dt_s,
            frozen_mask,
            safety_velocity_low,
            safety_velocity_high,
            raw_action=action["raw_action"],
            action_filter_alpha=action["action_filter_alpha"],
        )

    def filter_action(self, raw_action: np.ndarray, dt_s: float) -> dict:
        """Advance only the policy-action low-pass state."""
        raw = np.clip(np.asarray(raw_action, dtype=np.float64).reshape(self.n), -1.0, 1.0)
        dt = float(np.clip(dt_s, self.cfg.min_dt_s, self.cfg.max_dt_s))
        action_alpha = _alpha(dt, self.cfg.action_filter_tau_s)
        self.filtered_action += action_alpha * (raw - self.filtered_action)
        filtered = self.filtered_action.copy()
        filtered[np.abs(filtered) < self.cfg.action_deadband] = 0.0
        return {
            "raw_action": raw,
            "filtered_action": filtered,
            "action_filter_alpha": action_alpha,
        }

    def preview_velocity(self, filtered_action: np.ndarray, dt_s: float) -> dict:
        """Preview the acceleration-limited velocity without mutating state."""
        filtered = np.clip(
            np.asarray(filtered_action, dtype=np.float64).reshape(self.n), -1.0, 1.0
        )
        dt = float(np.clip(dt_s, self.cfg.min_dt_s, self.cfg.max_dt_s))
        requested_dq = self.cfg.action_scale_rad * filtered
        desired_velocity = np.clip(
            requested_dq / dt,
            -self.cfg.max_velocity_rad_s,
            self.cfg.max_velocity_rad_s,
        )
        max_dv = self.cfg.max_acceleration_rad_s2 * dt
        velocity_delta = np.clip(
            desired_velocity - self.reference_velocity, -max_dv, max_dv
        )
        return {
            "requested_dq": requested_dq,
            "desired_velocity_rad_s": desired_velocity,
            "acceleration_limited_velocity_rad_s": self.reference_velocity + velocity_delta,
        }

    def shape_filtered(
        self,
        measured_q: np.ndarray,
        filtered_action: np.ndarray,
        q_low: np.ndarray,
        q_high: np.ndarray,
        dt_s: float,
        frozen_mask: np.ndarray | None = None,
        safety_velocity_low: np.ndarray | None = None,
        safety_velocity_high: np.ndarray | None = None,
        *,
        projected_velocity_rad_s: np.ndarray | None = None,
        raw_action: np.ndarray | None = None,
        action_filter_alpha: float = 0.0,
    ) -> dict:
        q = np.asarray(measured_q, dtype=np.float64).reshape(self.n)
        filtered = np.clip(
            np.asarray(filtered_action, dtype=np.float64).reshape(self.n), -1.0, 1.0
        )
        raw = filtered.copy() if raw_action is None else np.clip(
            np.asarray(raw_action, dtype=np.float64).reshape(self.n), -1.0, 1.0
        )
        low = np.asarray(q_low, dtype=np.float64).reshape(self.n)
        high = np.asarray(q_high, dtype=np.float64).reshape(self.n)
        dt = float(np.clip(dt_s, self.cfg.min_dt_s, self.cfg.max_dt_s))
        if self.q_ref is None:
            self.q_ref = q.copy()

        preview = self.preview_velocity(filtered, dt)
        requested_dq = preview["requested_dq"]
        desired_velocity = preview["desired_velocity_rad_s"]
        shaped_velocity = preview["acceleration_limited_velocity_rad_s"]

        if projected_velocity_rad_s is not None:
            projected = np.asarray(projected_velocity_rad_s, dtype=np.float64).reshape(self.n)
            if not np.all(np.isfinite(projected)):
                raise ValueError("projected velocity contains non-finite values")
            shaped_velocity = projected.copy()
        unconstrained_velocity = shaped_velocity.copy()
        safety_clamped = np.zeros(self.n, dtype=bool)
        if safety_velocity_low is not None or safety_velocity_high is not None:
            if safety_velocity_low is None or safety_velocity_high is None:
                raise ValueError("both safety velocity bounds are required")
            safety_low = np.asarray(safety_velocity_low, dtype=np.float64).reshape(self.n)
            safety_high = np.asarray(safety_velocity_high, dtype=np.float64).reshape(self.n)
            if np.any(safety_low > safety_high):
                raise ValueError("invalid safety velocity bounds")
            shaped_velocity = np.clip(shaped_velocity, safety_low, safety_high)
            safety_clamped = np.abs(shaped_velocity - unconstrained_velocity) > 1.0e-9

        mask = (
            np.zeros(self.n, dtype=bool)
            if frozen_mask is None
            else np.asarray(frozen_mask, dtype=bool).reshape(self.n)
        )
        shaped_velocity[mask] = 0.0
        requested_dq[mask] = 0.0

        previous_command_error = self.q_ref - q
        tracking_exceeded = (
            np.abs(previous_command_error) > self.cfg.max_tracking_error_rad
        )

        policy_target = np.clip(q + requested_dq, low, high)
        q_ref_next = np.clip(q + shaped_velocity * dt, low, high)
        q_ref_next[mask] = q[mask]
        shaped_velocity = (q_ref_next - q) / dt
        shaped_velocity[mask] = 0.0
        self.reference_velocity = shaped_velocity.copy()
        self.q_ref = q_ref_next.copy()

        return {
            "q_ref": q_ref_next,
            "policy_target": policy_target,
            "raw_action": raw,
            "filtered_action": filtered,
            "requested_dq": requested_dq,
            "desired_velocity_rad_s": desired_velocity,
            "reference_velocity_rad_s": shaped_velocity,
            "unconstrained_velocity_rad_s": unconstrained_velocity,
            "safety_velocity_clamped": safety_clamped,
            "tracking_error_rad": q_ref_next - q,
            "previous_command_error_rad": previous_command_error,
            "tracking_exceeded": tracking_exceeded,
            # Kept for existing log consumers. No command is clamped by this
            # diagnostic threshold anymore.
            "tracking_clamped": np.zeros(self.n, dtype=bool),
            "action_filter_alpha": float(action_filter_alpha),
        }
