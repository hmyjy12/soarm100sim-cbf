import numpy as np

from soarm100_vision.control.policy_command_shaper import (
    PolicyCommandShaper,
    ShaperConfig,
)
from soarm100_vision.control.joint_limit_cbf import (
    JointLimitCbfConfig,
    JointLimitCbfFilter,
)


def make_shaper() -> PolicyCommandShaper:
    return PolicyCommandShaper(
        ShaperConfig(
            nominal_rate_hz=20.0,
            max_velocity_rad_s=0.2,
            max_acceleration_rad_s2=0.8,
        )
    )


def test_reference_acceleration_is_bounded_across_reversal():
    shaper = make_shaper()
    q = np.zeros(7)
    limits = np.full(7, 3.0)
    observation = shaper.observe(q, 1.0)
    first = shaper.shape(q, np.ones(7), -limits, limits, observation["dt_s"])
    second = shaper.shape(q, -np.ones(7), -limits, limits, 0.05)

    assert np.all(np.abs(first["reference_velocity_rad_s"]) <= 0.04 + 1e-12)
    assert np.all(
        np.abs(
            second["reference_velocity_rad_s"]
            - first["reference_velocity_rad_s"]
        )
        <= 0.04 + 1e-12
    )


def test_reference_is_reanchored_to_latest_measurement():
    shaper = make_shaper()
    limits = np.full(7, 3.0)
    q0 = np.zeros(7)
    obs = shaper.observe(q0, 1.0)
    result0 = shaper.shape(q0, np.ones(7), -limits, limits, obs["dt_s"])
    q1 = np.full(7, 0.001)
    obs = shaper.observe(q1, 1.05)
    result1 = shaper.shape(q1, np.ones(7), -limits, limits, obs["dt_s"])

    expected = q1 + result1["reference_velocity_rad_s"] * obs["dt_s"]
    assert np.allclose(result1["q_ref"], expected)
    assert np.allclose(
        result1["policy_target"],
        q1 + shaper.cfg.action_scale_rad * result1["filtered_action"],
    )


def test_reference_does_not_wind_up_and_frozen_joint_holds_measurement():
    shaper = make_shaper()
    limits = np.full(7, 3.0)
    q = np.zeros(7)
    obs = shaper.observe(q, 1.0)
    frozen = np.array([False] * 6 + [True])
    for _ in range(100):
        result = shaper.shape(q, np.ones(7), -limits, limits, obs["dt_s"], frozen)

    expected_step = shaper.cfg.max_velocity_rad_s * obs["dt_s"]
    assert np.all(np.abs(result["tracking_error_rad"][:6]) <= expected_step + 1e-12)
    assert result["q_ref"][6] == 0.0


def test_previous_command_lag_is_diagnostic_and_does_not_shift_next_origin():
    shaper = make_shaper()
    limits = np.full(7, 3.0)
    q = np.zeros(7)
    obs = shaper.observe(q, 1.0)
    shaper.q_ref = np.full(7, 0.30)

    result = shaper.shape(q, np.ones(7), -limits, limits, obs["dt_s"])

    assert np.all(result["tracking_exceeded"])
    assert not np.any(result["tracking_clamped"])
    assert np.all(result["q_ref"] <= 0.04 * obs["dt_s"] + 1e-12)


def test_joint_limit_cbf_tightens_velocity_toward_upper_limit():
    cbf = JointLimitCbfFilter(JointLimitCbfConfig(alpha=4.0))
    q = np.array([0.99, 0.0])
    bounds = cbf.velocity_bounds(q, np.array([-1.0, -1.0]), np.array([1.0, 1.0]))

    assert np.isclose(bounds["velocity_high_rad_s"][0], 0.04)
    assert bounds["velocity_high_rad_s"][1] == 4.0
    assert bounds["active"].tolist() == [True, False]


def test_joint_limit_cbf_requires_recovery_when_outside():
    cbf = JointLimitCbfFilter(
        JointLimitCbfConfig(alpha=4.0, recovery_velocity_rad_s=0.05)
    )
    bounds = cbf.velocity_bounds(
        np.array([1.01]), np.array([-1.0]), np.array([1.0])
    )

    assert bounds["outside"].tolist() == [True]
    assert bounds["velocity_high_rad_s"][0] <= -0.05


def test_shaper_applies_external_safety_velocity_bounds_before_integration():
    shaper = make_shaper()
    q = np.zeros(7)
    limits = np.full(7, 3.0)
    obs = shaper.observe(q, 1.0)
    velocity_low = np.full(7, -1.0)
    velocity_high = np.full(7, 1.0)
    velocity_high[2] = 0.01
    result = shaper.shape(
        q,
        np.ones(7),
        -limits,
        limits,
        obs["dt_s"],
        safety_velocity_low=velocity_low,
        safety_velocity_high=velocity_high,
    )

    assert result["reference_velocity_rad_s"][2] <= 0.01 + 1e-12
    assert result["safety_velocity_clamped"][2]


def test_projected_velocity_is_applied_after_nominal_acceleration_preview():
    shaper = make_shaper()
    q = np.zeros(7)
    limits = np.full(7, 3.0)
    obs = shaper.observe(q, 1.0)
    action = shaper.filter_action(np.ones(7), obs["dt_s"])
    preview = shaper.preview_velocity(action["filtered_action"], obs["dt_s"])
    projected = preview["acceleration_limited_velocity_rad_s"].copy()
    projected[0] = -0.01
    result = shaper.shape_filtered(
        q,
        action["filtered_action"],
        -limits,
        limits,
        obs["dt_s"],
        projected_velocity_rad_s=projected,
        raw_action=action["raw_action"],
        action_filter_alpha=action["action_filter_alpha"],
    )

    assert np.isclose(result["reference_velocity_rad_s"][0], -0.01)
    assert np.isclose(result["q_ref"][0], -0.01 * obs["dt_s"])
