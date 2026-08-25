from pathlib import Path

import numpy as np

from soarm100_vision.control.bounded_policy_target_tracker import (
    BoundedPolicyTargetTracker,
)


JOINTS = ("j0", "j1", "gripper")


def write_config(path: Path) -> None:
    path.write_text(
        '{"mode":"bounded","max_lead_rad":{"j0":0.20,"j1":0.20,"gripper":0.0}}',
        encoding="utf-8",
    )


def test_tracker_accumulates_toward_policy_target_and_caps_lead(tmp_path):
    path = tmp_path / "tracker.json"
    write_config(path)
    tracker = BoundedPolicyTargetTracker.from_config(path, JOINTS)
    q = np.zeros(3)
    result = None
    for _ in range(30):
        result = tracker.apply(
            q,
            np.array([-0.25, 0.25, 0.25]),
            np.array([-0.20, 0.20, 0.20]),
            np.full(3, -3.0),
            np.full(3, 3.0),
            0.05,
            np.array([False, False, True]),
        )

    assert result is not None
    assert np.allclose(result["q_cmd"], [-0.20, 0.20, 0.0])
    assert np.all(result["lead_clamped"][:2])


def test_tracker_does_not_overshoot_smaller_policy_target(tmp_path):
    path = tmp_path / "tracker.json"
    write_config(path)
    tracker = BoundedPolicyTargetTracker.from_config(path, JOINTS)
    result = tracker.apply(
        np.zeros(3),
        np.array([0.03, -0.04, 0.0]),
        np.array([0.20, -0.20, 0.0]),
        np.full(3, -3.0),
        np.full(3, 3.0),
        1.0,
    )

    assert np.allclose(result["q_cmd"], [0.03, -0.04, 0.0])


def test_target_reversal_does_not_jump_across_measurement(tmp_path):
    path = tmp_path / "tracker.json"
    write_config(path)
    tracker = BoundedPolicyTargetTracker.from_config(path, JOINTS)
    tracker.tracked_command = np.array([0.20, -0.20, 0.0])
    result = tracker.apply(
        np.zeros(3),
        np.array([-0.25, 0.25, 0.0]),
        np.array([-0.20, 0.20, 0.0]),
        np.full(3, -3.0),
        np.full(3, 3.0),
        0.05,
    )

    assert np.allclose(result["q_cmd"], [0.19, -0.19, 0.0])
