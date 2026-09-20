"""为鲁棒局部 CBF 约束提供短时障碍物状态估计。

当前模块尚未接入真机 CBF。导出的 ``velocity_m_s`` 是严格的 m/s；若未来接入
现有 ``PointCloudSdfObstacle.velocity``，调用方必须乘以 CBF 控制周期 dt，将其
转换为每个控制步的位移，不能直接连接。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ObstacleObserverConfig:
    measurement_std_m: float = 0.006
    acceleration_std_m_s2: float = 0.5
    confidence_sigma: float = 2.0
    innovation_uncertainty_scale: float = 0.5
    min_position_uncertainty_m: float = 0.004
    max_position_uncertainty_m: float = 0.080
    max_velocity_m_s: float = 0.60
    min_dt_s: float = 0.03
    max_dt_s: float = 1.0

    def __post_init__(self) -> None:
        if self.measurement_std_m <= 0.0 or self.acceleration_std_m_s2 <= 0.0:
            raise ValueError("observer noise values must be positive")
        if self.confidence_sigma <= 0.0:
            raise ValueError("observer confidence_sigma must be positive")
        if not 0.0 <= self.innovation_uncertainty_scale <= 2.0:
            raise ValueError("observer innovation uncertainty scale must be within [0, 2]")
        if not 0.0 <= self.min_position_uncertainty_m <= self.max_position_uncertainty_m:
            raise ValueError("invalid observer position uncertainty bounds")
        if self.max_velocity_m_s <= 0.0:
            raise ValueError("observer max velocity must be positive")
        if not 0.0 < self.min_dt_s <= self.max_dt_s:
            raise ValueError("invalid observer dt bounds")


class ObstacleMotionObserver:
    """带有界不确定度的六维位置/速度 Kalman observer。

    常速度状态转移只作为单步名义模型；加速度过程噪声让估计能够响应停止、加速和
    反向。导出的不确定度供未来鲁棒 CBF 项使用；当前主链路尚未接入本 observer。
    """

    def __init__(self, config: ObstacleObserverConfig) -> None:
        self.cfg = config
        self.state = np.zeros(6, dtype=np.float64)
        self.covariance = np.eye(6, dtype=np.float64)
        self.last_stamp_s: float | None = None
        self.initialized = False
        self.innovation = np.zeros(3, dtype=np.float64)

    def reset(self) -> None:
        self.state.fill(0.0)
        self.covariance[:] = np.eye(6, dtype=np.float64)
        self.last_stamp_s = None
        self.initialized = False
        self.innovation.fill(0.0)

    @staticmethod
    def _transition(dt: float) -> np.ndarray:
        f = np.eye(6, dtype=np.float64)
        f[:3, 3:] = np.eye(3, dtype=np.float64) * dt
        return f

    def _process_covariance(self, dt: float) -> np.ndarray:
        q = np.zeros((6, 6), dtype=np.float64)
        accel_var = self.cfg.acceleration_std_m_s2**2
        q[:3, :3] = np.eye(3) * (0.25 * dt**4 * accel_var)
        q[:3, 3:] = np.eye(3) * (0.5 * dt**3 * accel_var)
        q[3:, :3] = q[:3, 3:]
        q[3:, 3:] = np.eye(3) * (dt**2 * accel_var)
        return q

    def update(self, measured_center_m: np.ndarray, stamp_s: float) -> dict:
        measurement = np.asarray(measured_center_m, dtype=np.float64).reshape(3)
        if not np.all(np.isfinite(measurement)) or not np.isfinite(stamp_s):
            raise ValueError("non-finite obstacle observation")

        if not self.initialized:
            self.state[:3] = measurement
            self.state[3:] = 0.0
            pos_var = self.cfg.measurement_std_m**2
            vel_var = (self.cfg.max_velocity_m_s / self.cfg.confidence_sigma) ** 2
            self.covariance = np.diag([pos_var] * 3 + [vel_var] * 3)
            self.last_stamp_s = float(stamp_s)
            self.initialized = True
            self.innovation.fill(0.0)
            return self.snapshot()

        assert self.last_stamp_s is not None
        raw_dt = float(stamp_s) - self.last_stamp_s
        if raw_dt < self.cfg.min_dt_s:
            return self.snapshot()
        if raw_dt > self.cfg.max_dt_s:
            self.reset()
            return self.update(measurement, stamp_s)

        dt = float(np.clip(raw_dt, self.cfg.min_dt_s, self.cfg.max_dt_s))
        f = self._transition(dt)
        predicted_state = f @ self.state
        predicted_covariance = f @ self.covariance @ f.T + self._process_covariance(dt)

        h = np.zeros((3, 6), dtype=np.float64)
        h[:, :3] = np.eye(3)
        r = np.eye(3) * self.cfg.measurement_std_m**2
        self.innovation = measurement - h @ predicted_state
        innovation_covariance = h @ predicted_covariance @ h.T + r
        gain = predicted_covariance @ h.T @ np.linalg.inv(innovation_covariance)
        self.state = predicted_state + gain @ self.innovation
        identity = np.eye(6, dtype=np.float64)
        # Joseph 形式可在数值更新后保持协方差对称且半正定。
        ikh = identity - gain @ h
        self.covariance = ikh @ predicted_covariance @ ikh.T + gain @ r @ gain.T
        self.covariance = 0.5 * (self.covariance + self.covariance.T)

        speed = float(np.linalg.norm(self.state[3:]))
        if speed > self.cfg.max_velocity_m_s:
            # 这是状态的硬限幅，不会同步投影 covariance；因此 clamp 后的速度不确定度
            # 不构成严格 Kalman 后验，只能作为实验性保守量使用。
            self.state[3:] *= self.cfg.max_velocity_m_s / speed
        self.last_stamp_s = float(stamp_s)
        return self.snapshot()

    def snapshot(self) -> dict:
        pos_eigenvalue = max(
            float(np.max(np.linalg.eigvalsh(self.covariance[:3, :3]))), 0.0
        )
        vel_eigenvalue = max(
            float(np.max(np.linalg.eigvalsh(self.covariance[3:, 3:]))), 0.0
        )
        position_radius = (
            self.cfg.confidence_sigma * np.sqrt(pos_eigenvalue)
            + self.cfg.innovation_uncertainty_scale * float(np.linalg.norm(self.innovation))
        )
        position_radius = float(
            np.clip(
                position_radius,
                self.cfg.min_position_uncertainty_m,
                self.cfg.max_position_uncertainty_m,
            )
        )
        velocity_radius = float(
            min(
                self.cfg.confidence_sigma * np.sqrt(vel_eigenvalue),
                self.cfg.max_velocity_m_s,
            )
        )
        return {
            "position_m": self.state[:3].copy(),
            "velocity_m_s": self.state[3:].copy(),
            "position_uncertainty_m": position_radius,
            "velocity_uncertainty_m_s": velocity_radius,
            "innovation_m": self.innovation.copy(),
            "innovation_norm_m": float(np.linalg.norm(self.innovation)),
        }
