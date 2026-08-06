import numpy as np

from soarm100_vision.control.policy_command_shaper import (
    PolicyCommandShaper,
    ShaperConfig,
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


def test_reference_is_not_reanchored_to_encoder_noise():
    shaper = make_shaper()
    limits = np.full(7, 3.0)
    q0 = np.zeros(7)
    obs = shaper.observe(q0, 1.0)
    result0 = shaper.shape(q0, np.ones(7), -limits, limits, obs["dt_s"])
    q1 = np.full(7, 0.001)
    obs = shaper.observe(q1, 1.05)
    result1 = shaper.shape(q1, np.ones(7), -limits, limits, obs["dt_s"])

    assert np.all(result1["q_ref"] > result0["q_ref"])
    # The 1 mrad measurement change is not copied directly into q_ref.
    expected_without_measurement_reanchor = (
        result0["q_ref"] + result1["reference_velocity_rad_s"] * obs["dt_s"]
    )
    assert np.allclose(result1["q_ref"], expected_without_measurement_reanchor)


def test_tracking_error_is_bounded_and_frozen_joint_holds_measurement():
    shaper = make_shaper()
    limits = np.full(7, 3.0)
    q = np.zeros(7)
    obs = shaper.observe(q, 1.0)
    frozen = np.array([False] * 6 + [True])
    for _ in range(100):
        result = shaper.shape(q, np.ones(7), -limits, limits, obs["dt_s"], frozen)

    assert np.all(
        np.abs(result["tracking_error_rad"][:6])
        <= shaper.cfg.max_tracking_error_rad + 1e-12
    )
    assert result["q_ref"][6] == 0.0
