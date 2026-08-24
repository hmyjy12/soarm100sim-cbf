import numpy as np

from soarm100_vision.sdf_cbf_core import (
    AttachedThinComponentFilter,
    AttachedThinFilterConfig,
    filter_capsule_self_points,
    filter_oriented_box_self_points,
    nearest_joint_sample,
)


def test_nearest_joint_sample_enforces_timestamp_tolerance():
    samples = [(1.0, np.array([1.0, 2.0])), (1.1, np.array([3.0, 4.0]))]

    q, delta = nearest_joint_sample(samples, 1.08, 0.05)
    assert np.allclose(q, [3.0, 4.0])
    assert np.isclose(delta, 0.02)

    missing, delta = nearest_joint_sample(samples, 1.3, 0.05)
    assert missing is None
    assert np.isclose(delta, 0.2)


def test_capsule_self_filter_removes_only_nearby_points():
    points = np.array(
        [
            [0.5, 0.00, 0.0],
            [0.5, 0.04, 0.0],
            [0.5, 0.08, 0.0],
            [1.2, 0.00, 0.0],
        ]
    )
    capsules = [(np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]), 0.03)]

    filtered, removed = filter_capsule_self_points(points, capsules, margin_m=0.02)

    assert removed == 2
    assert np.allclose(filtered, [[0.5, 0.08, 0.0], [1.2, 0.0, 0.0]])


def _line(start, end, count=20):
    return np.linspace(np.asarray(start), np.asarray(end), count)


def test_attached_thin_filter_removes_wrist_attached_line_only():
    capsule = [(np.array([0.0, 0.0, 0.0]), np.array([0.10, 0.0, 0.0]), 0.02)]
    cable = _line([0.02, 0.035, 0.0], [0.10, 0.035, 0.0])
    remote_rod = _line([0.02, 0.20, 0.0], [0.10, 0.20, 0.0])
    points = np.vstack((cable, remote_rod))
    result = AttachedThinComponentFilter().apply(points, capsule)
    assert result.components_removed == 1
    assert result.removed_points.shape[0] == cable.shape[0]
    assert result.kept_points.shape[0] == remote_rod.shape[0]


def test_attached_thin_filter_keeps_wide_obstacle():
    capsule = [(np.array([0.0, 0.0, 0.0]), np.array([0.10, 0.0, 0.0]), 0.02)]
    x = np.linspace(0.02, 0.10, 10)
    wide = np.array([[xi, y, 0.0] for xi in x for y in (0.035, 0.070)])
    config = AttachedThinFilterConfig(connectivity_m=0.040)
    result = AttachedThinComponentFilter(config).apply(wide, capsule)
    assert result.components_removed == 0
    assert result.kept_points.shape[0] == wide.shape[0]


def test_oriented_box_filter_uses_link_local_axes():
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    center = np.array([0.2, 0.1, 0.3])
    local_points = np.array([[0.015, 0.0, 0.0], [0.0, 0.025, 0.0]])
    world_points = center + local_points @ rotation.T
    filtered, removed = filter_oriented_box_self_points(
        world_points, center, rotation, np.array([0.020, 0.010, 0.010])
    )
    assert removed == 1
    assert np.allclose(filtered, world_points[1:])
