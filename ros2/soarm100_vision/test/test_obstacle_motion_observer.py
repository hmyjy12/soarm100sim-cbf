"""障碍物运动 observer 的纯 Python 数值回归测试。"""

from pathlib import Path
import sys

import numpy as np
import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "ros2" / "soarm100_vision"))
from soarm100_vision.control.obstacle_motion_observer import (  # noqa: E402
    ObstacleMotionObserver,
    ObstacleObserverConfig,
)


def test_initialization_sets_position_zero_velocity_and_valid_covariance():
    observer = ObstacleMotionObserver(ObstacleObserverConfig())
    measured = np.array([0.12, -0.03, 0.25])

    snapshot = observer.update(measured, 10.0)

    assert observer.initialized is True
    assert observer.last_stamp_s == 10.0
    assert np.allclose(snapshot["position_m"], measured)
    assert np.allclose(snapshot["velocity_m_s"], 0.0)
    assert observer.covariance.shape == (6, 6)
    assert np.all(np.isfinite(observer.covariance))
    assert np.all(np.diag(observer.covariance) >= 0.0)


def test_static_obstacle_velocity_converges_to_zero_without_drift():
    observer = ObstacleMotionObserver(ObstacleObserverConfig())
    measured = np.array([0.10, 0.02, 0.20])
    for index in range(12):
        snapshot = observer.update(measured, index * 0.1)

    assert np.linalg.norm(snapshot["velocity_m_s"]) < 1e-8
    assert np.allclose(snapshot["position_m"], measured, atol=1e-8)
    assert np.all(np.isfinite(observer.covariance))


def test_constant_velocity_has_correct_direction_and_reasonable_scale():
    observer = ObstacleMotionObserver(ObstacleObserverConfig())
    expected_velocity_m_s = 0.10
    for index in range(12):
        stamp = index * 0.1
        snapshot = observer.update(np.array([expected_velocity_m_s * stamp, 0.0, 0.0]), stamp)

    assert snapshot["velocity_m_s"][0] > 0.0
    assert np.isclose(snapshot["velocity_m_s"][0], expected_velocity_m_s, atol=0.02)
    assert np.allclose(snapshot["velocity_m_s"][1:], 0.0, atol=1e-8)


def test_velocity_clamp_limits_extreme_measurement_jump():
    max_velocity_m_s = 0.20
    observer = ObstacleMotionObserver(
        ObstacleObserverConfig(max_velocity_m_s=max_velocity_m_s)
    )
    observer.update(np.zeros(3), 0.0)
    snapshot = observer.update(np.array([10.0, 0.0, 0.0]), 0.1)

    assert np.linalg.norm(snapshot["velocity_m_s"]) <= max_velocity_m_s + 1e-12
    assert snapshot["velocity_m_s"][0] > 0.0


def test_reset_clears_state_and_next_measurement_reinitializes():
    observer = ObstacleMotionObserver(ObstacleObserverConfig())
    observer.update(np.zeros(3), 0.0)
    observer.update(np.array([0.05, 0.0, 0.0]), 0.1)

    observer.reset()

    assert observer.initialized is False
    assert observer.last_stamp_s is None
    assert np.allclose(observer.state, 0.0)
    assert np.allclose(observer.covariance, np.eye(6))
    restarted = observer.update(np.array([0.3, 0.1, 0.2]), 3.0)
    assert np.allclose(restarted["position_m"], [0.3, 0.1, 0.2])
    assert np.allclose(restarted["velocity_m_s"], 0.0)


def test_covariance_and_uncertainty_outputs_remain_finite_and_bounded():
    config = ObstacleObserverConfig()
    observer = ObstacleMotionObserver(config)
    for index in range(10):
        stamp = index * 0.1
        snapshot = observer.update(np.array([0.02 * stamp, 0.0, 0.0]), stamp)

    assert observer.covariance.shape == (6, 6)
    assert np.all(np.isfinite(observer.covariance))
    assert np.all(np.diag(observer.covariance) >= -1e-12)
    assert np.isfinite(snapshot["position_uncertainty_m"])
    assert np.isfinite(snapshot["velocity_uncertainty_m_s"])
    assert config.min_position_uncertainty_m <= snapshot["position_uncertainty_m"] <= config.max_position_uncertainty_m
    assert 0.0 <= snapshot["velocity_uncertainty_m_s"] <= config.max_velocity_m_s
    assert np.isclose(
        snapshot["innovation_norm_m"], np.linalg.norm(snapshot["innovation_m"])
    )


def test_short_zero_and_negative_timestamp_intervals_are_ignored():
    observer = ObstacleMotionObserver(ObstacleObserverConfig(min_dt_s=0.03))
    initial = observer.update(np.array([1.0, 0.0, 0.0]), 1.0)
    zero_dt = observer.update(np.array([3.0, 0.0, 0.0]), 1.0)
    short_dt = observer.update(np.array([3.0, 0.0, 0.0]), 1.02)
    negative_dt = observer.update(np.array([3.0, 0.0, 0.0]), 0.5)

    for snapshot in (zero_dt, short_dt, negative_dt):
        assert np.allclose(snapshot["position_m"], initial["position_m"])
        assert np.allclose(snapshot["velocity_m_s"], initial["velocity_m_s"])
    assert observer.last_stamp_s == 1.0


def test_long_timestamp_gap_resets_and_reinitializes_from_measurement():
    observer = ObstacleMotionObserver(ObstacleObserverConfig(max_dt_s=1.0))
    observer.update(np.zeros(3), 0.0)
    observer.update(np.array([0.1, 0.0, 0.0]), 0.1)

    snapshot = observer.update(np.array([1.0, 2.0, 3.0]), 2.0)

    assert observer.initialized is True
    assert observer.last_stamp_s == 2.0
    assert np.allclose(snapshot["position_m"], [1.0, 2.0, 3.0])
    assert np.allclose(snapshot["velocity_m_s"], 0.0)


def test_observer_is_deterministic_and_rejects_nonfinite_input():
    sequence = [
        (np.array([0.0, 0.0, 0.0]), 0.0),
        (np.array([0.01, -0.01, 0.0]), 0.1),
        (np.array([0.02, -0.02, 0.0]), 0.2),
        (np.array([0.03, -0.03, 0.0]), 0.3),
    ]
    first = ObstacleMotionObserver(ObstacleObserverConfig())
    second = ObstacleMotionObserver(ObstacleObserverConfig())
    for measurement, stamp in sequence:
        first_snapshot = first.update(measurement, stamp)
        second_snapshot = second.update(measurement, stamp)
        for key in ("position_m", "velocity_m_s", "innovation_m"):
            assert np.allclose(first_snapshot[key], second_snapshot[key])
        for key in (
            "position_uncertainty_m",
            "velocity_uncertainty_m_s",
            "innovation_norm_m",
        ):
            assert first_snapshot[key] == second_snapshot[key]

    with pytest.raises(ValueError, match="non-finite obstacle observation"):
        first.update(np.array([np.nan, 0.0, 0.0]), 0.4)
    with pytest.raises(ValueError, match="non-finite obstacle observation"):
        first.update(np.zeros(3), float("inf"))
