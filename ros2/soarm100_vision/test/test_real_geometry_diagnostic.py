import importlib.util
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "geometry_diagnostic", ROOT / "ros2/scripts/real/diagnose_obstacle_geometry.py")
diag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diag)
cbf = diag.cbf


def test_uncapped_distance_matches_geometry_beyond_legacy_radius():
    point = np.array([0.20, 0., 0.])
    old = cbf.PointCloudSdfObstacle("old", [[0, 0, 0]], truncation_distance=0.15)
    exact = cbf.PointCloudSdfObstacle("exact", [[0, 0, 0]], truncation_distance=float("inf"))
    h_old, g_old = cbf.pointcloud_sdf_h_and_grad_p(point, old, 0.03, 0.04)
    h, grad = cbf.pointcloud_sdf_h_and_grad_p(point, exact, 0.03, 0.04)
    assert h_old == 0.15 and np.all(g_old == 0)
    assert np.isclose(h, 0.13)
    assert np.allclose(grad, [1, 0, 0])


def test_diagnostic_matches_production_barriers_and_capsule_sampling():
    model = diag.mujoco.MjModel.from_xml_path(str(
        ROOT / "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"))
    data = diag.mujoco.MjData(model)
    ids = diag.runtime.resolve_robot_ids(model)
    q = np.zeros(7)
    points = np.random.default_rng(7).uniform([-0.2, -0.2, 0.05], [0.4, 0.3, 0.4], (200, 3))
    result = diag.evaluate(model, data, ids, points, q, 0.03, 0.005)
    cfg = cbf.CbfConfig(d_safe=0.03)
    monitors = cbf.resolve_monitors(model, cfg.monitor_specs, cfg.capsule_specs)
    obs = cbf.PointCloudSdfObstacle("exact", points, truncation_distance=float("inf"), inflate=0.005)
    records, h, worst = cbf._worst_barrier(model, data, ids, monitors, [obs], cfg, diag.runtime.tcp_pose_w)
    assert np.isclose(h, result["worst"]["h_m"])
    assert worst["monitor"] == result["worst"]["name"]
    for actual, expected in zip(records, result["monitors"]):
        assert np.isclose(actual["h"], expected["h_m"])
        assert expected["continuous_clearance_m"] <= expected["clearance_m"] + 1e-12


def test_successfully_published_depth_is_not_reprocessed_after_mask_callback():
    from soarm100_vision.obstacle_cloud_node import ObstacleCloudNode
    stamp = SimpleNamespace(sec=123, nanosec=42)
    fake = SimpleNamespace(
        _depth=SimpleNamespace(header=SimpleNamespace(stamp=stamp)), _info=object(),
        _param=lambda name: "dynamic", _last_depth_stamp=None,
        _last_published_depth_stamp=(123, 42))
    # No conversion/filter methods exist on fake: execution must return early.
    ObstacleCloudNode._tick(fake)


def test_self_filter_removes_points_25mm_outside_nominal_capsule():
    from soarm100_vision.sdf_cbf_core import filter_capsule_self_points
    a, b, radius = np.zeros(3), np.array([0, 0, 0.2]), 0.04
    points = np.array([[radius+0.025, 0, 0.1], [radius+0.05, 0, 0.1]])
    kept, removed = filter_capsule_self_points(points, [(a, b, radius)], 0.035)
    assert removed == 1
    assert np.allclose(kept, points[1:])


def test_approaching_nominal_action_is_corrected_near_obstacle():
    model = diag.mujoco.MjModel.from_xml_path(str(
        ROOT / "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"))
    data = diag.mujoco.MjData(model)
    ids = diag.runtime.resolve_robot_ids(model)
    diag.mujoco.mj_forward(model, data)
    tcp, jac = cbf.tcp_pos_and_jacobian(model, data, ids, diag.runtime.tcp_pose_w)
    points = np.asarray(tcp).reshape(1, 3) + [0, 0.046, 0]
    obs = cbf.PointCloudSdfObstacle("cup", points, truncation_distance=float("inf"))
    monitors = cbf.resolve_monitors(model, (("tcp", 0.015),), ())
    cfg = cbf.CbfConfig(d_safe=0.03, activate_margin=0.04, dq_max=0.005)
    nominal = np.sign(jac[1]) * 0.005
    nominal[6] = 0
    correction, info = cbf.solve_cbf_correction(
        model, data, ids, nominal, cfg, monitors, [obs], diag.runtime.tcp_pose_w)
    assert info["cbf_active"] and info["cbf_feasible"]
    assert np.linalg.norm(correction) > 0
    assert float(jac[1] @ (nominal + correction)) < float(jac[1] @ nominal)


def test_empty_or_delayed_cloud_cannot_pass_readiness():
    from soarm100_vision.policy_reach_node import PolicyReachNode
    params = {"obstacle_startup_min_clouds": 3, "obstacle_cloud_timeout_s": 3.,
              "obstacle_min_points": 30}
    stops = []
    fake = SimpleNamespace(obstacle_cbf_config=object(), obstacle_cloud_seq=3,
        obstacle_cloud_received_at=10., obstacle_cloud_stamp_s=10.,
        obstacle_cbf_obstacles=[], get_parameter=lambda n: SimpleNamespace(value=params[n]),
        get_clock=lambda: SimpleNamespace(now=lambda: SimpleNamespace(nanoseconds=10_000_000_000)),
        _stop=lambda reason, **fields: stops.append(reason))
    assert not PolicyReachNode._obstacle_cloud_ready(fake, 10.)
    assert stops[-1] == "OBSTACLE_CLOUD_TOO_SPARSE"
    fake.obstacle_cbf_obstacles = [object()]
    fake.obstacle_cloud_stamp_s = 1.
    assert not PolicyReachNode._obstacle_cloud_ready(fake, 10.)
    assert stops[-1] == "OBSTACLE_CLOUD_STALE"
