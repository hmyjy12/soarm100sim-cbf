from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "mujoco"))
import cbf as cbf_core  # noqa: E402


def test_obstacle_step_tightens_discrete_cbf_constraint():
    config = cbf_core.CbfConfig(gamma=0.5, activate_margin=0.10)
    nominal = np.zeros(7, dtype=np.float64)
    base_record = {
        "h": 0.01,
        "grad_q": np.asarray([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        "obs_step": 0.002,
    }
    moving_obstacle_record = dict(base_record, obs_step=0.006)

    _, base_rhs, _ = cbf_core._build_constraints([base_record], config, nominal)
    _, moving_rhs, _ = cbf_core._build_constraints(
        [moving_obstacle_record], config, nominal
    )

    assert np.isclose(moving_rhs[0] - base_rhs[0], 0.004)


def test_zero_velocity_dynamic_padding_preserves_static_constraint():
    config = cbf_core.CbfConfig(
        gamma=0.5,
        activate_margin=0.10,
        dynamic_obstacle_lookahead_steps=2.0,
    )
    nominal = np.zeros(7, dtype=np.float64)
    static_record = {
        "h": 0.01,
        "grad_q": np.asarray([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        "obs_step": 0.002,
        "obs_speed": 0.0,
    }
    _, rhs_with_padding, _ = cbf_core._build_constraints(
        [static_record], config, nominal
    )
    config.dynamic_obstacle_lookahead_steps = 0.0
    _, rhs_without_padding, _ = cbf_core._build_constraints(
        [static_record], config, nominal
    )

    assert np.allclose(rhs_with_padding, rhs_without_padding)


def test_point_cloud_obstacle_inflate_reduces_clearance():
    obstacle = cbf_core.PointCloudSdfObstacle(
        name="test",
        points=np.asarray([[0.0, 0.0, 0.0]]),
        inflate=0.01,
    )
    h, grad = cbf_core.pointcloud_sdf_h_and_grad_p(
        np.asarray([0.05, 0.0, 0.0]),
        obstacle,
        d_safe=0.02,
        r_link=0.01,
    )

    assert np.isclose(h, 0.01)
    assert np.allclose(grad, [1.0, 0.0, 0.0])
