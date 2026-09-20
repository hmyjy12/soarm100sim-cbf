"""双臂 CBF 的纯数学、几何与 QP 回归测试。

这些测试刻意用解析几何和 mock 约束避开 MuJoCo 模型、ROS 与真实硬件；
双臂 FK/Jacobian 的模型级回归仍需另行运行。
"""

from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "mujoco"))
import cbf as cbf_core  # noqa: E402


ARM_DIM = cbf_core.ACTION_DIM
DUAL_DIM = 2 * ARM_DIM


def _capsule_pair(
    separation: float,
    *,
    left_radius: float = 0.1,
    right_radius: float = 0.1,
    d_safe: float = 0.1,
) -> cbf_core.CapsulePairBarrier:
    """构造两条平行、长度相同且可人工验证的 capsule。"""
    jac = np.zeros((3, ARM_DIM), dtype=np.float64)
    jac[1, 0] = 1.0
    return cbf_core.capsule_pair_h_and_grads(
        "left",
        "right",
        np.array([0.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        jac,
        jac,
        left_radius,
        np.array([0.0, separation, 0.0]),
        np.array([1.0, separation, 0.0]),
        jac,
        jac,
        right_radius,
        d_safe,
    )


def test_current_dual_dimension_is_derived_from_action_dim():
    assert ARM_DIM == 7
    assert DUAL_DIM == 2 * ARM_DIM == 14


def _empty_env_info() -> dict:
    return {
        "h_min": float("inf"),
        "worst_monitor": "",
        "worst_obstacle": "",
        "n_constraints": 0,
    }


def _empty_inter_info() -> dict:
    return {
        "h_LR_min": float("inf"),
        "distance_LR_min": float("inf"),
        "worst_left_link": "",
        "worst_right_link": "",
        "n_interarm_constraints": 0,
    }


def test_closest_points_parallel_segments_are_separated_and_bounded():
    s, t, p_left, p_right = cbf_core.closest_points_on_segments(
        np.array([0.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
    )

    assert 0.0 <= s <= 1.0
    assert 0.0 <= t <= 1.0
    assert np.isclose(np.linalg.norm(p_left - p_right), 1.0)


def test_closest_points_intersection_endpoint_degenerate_and_symmetry():
    _, _, p_left, p_right = cbf_core.closest_points_on_segments(
        np.array([-1.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, -1.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
    )
    assert np.allclose(p_left, p_right, atol=1e-12)

    s, t, p_left, p_right = cbf_core.closest_points_on_segments(
        np.array([0.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        np.array([2.0, 1.0, 0.0]),
        np.array([2.0, 2.0, 0.0]),
    )
    assert np.isclose(s, 1.0)
    assert np.isclose(t, 0.0)
    assert np.allclose(p_left, [1.0, 0.0, 0.0])
    assert np.allclose(p_right, [2.0, 1.0, 0.0])

    _, _, degenerate_left, degenerate_right = cbf_core.closest_points_on_segments(
        np.zeros(3),
        np.zeros(3),
        np.array([1.0, -1.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
    )
    assert np.all(np.isfinite(degenerate_left))
    assert np.all(np.isfinite(degenerate_right))
    assert np.allclose(degenerate_left, [0.0, 0.0, 0.0])
    assert np.allclose(degenerate_right, [1.0, 0.0, 0.0])

    _, _, swap_left, swap_right = cbf_core.closest_points_on_segments(
        np.array([2.0, 1.0, 0.0]),
        np.array([2.0, 2.0, 0.0]),
        np.array([0.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
    )
    assert np.allclose(swap_left, p_right)
    assert np.allclose(swap_right, p_left)


def test_capsule_pair_barrier_has_expected_sign_shapes_and_gradient_directions():
    safe = _capsule_pair(0.5)
    boundary = _capsule_pair(0.3)
    unsafe = _capsule_pair(0.2)

    assert safe.h > 0.0
    assert np.isclose(boundary.h, 0.0, atol=1e-12)
    assert unsafe.h < 0.0
    assert safe.distance == np.linalg.norm(safe.p_left - safe.p_right)
    assert safe.normal.shape == (3,)
    assert safe.grad_left.shape == (ARM_DIM,)
    assert safe.grad_right.shape == (ARM_DIM,)
    assert np.all(np.isfinite(safe.normal))
    assert np.all(np.isfinite(safe.grad_left))
    assert np.all(np.isfinite(safe.grad_right))
    assert np.isclose(safe.grad_left[0], -1.0)
    assert np.isclose(safe.grad_right[0], 1.0)


def test_capsule_pair_gradients_match_finite_difference_away_from_switches():
    left_a = np.array([-1.0, 0.0, 0.0])
    left_b = np.array([1.0, 0.0, 0.0])
    right_a = np.array([0.2, -1.0, 0.8])
    right_b = np.array([0.2, 1.0, 0.8])
    jac = np.zeros((3, ARM_DIM), dtype=np.float64)
    jac[:, :3] = np.eye(3)

    base = cbf_core.capsule_pair_h_and_grads(
        "left",
        "right",
        left_a,
        left_b,
        jac,
        jac,
        0.02,
        right_a,
        right_b,
        jac,
        jac,
        0.02,
        0.03,
    )
    eps = 1e-6

    def h_with_left_delta(delta: np.ndarray) -> float:
        return cbf_core.capsule_pair_h_and_grads(
            "left", "right", left_a + delta, left_b + delta, jac, jac, 0.02,
            right_a, right_b, jac, jac, 0.02, 0.03,
        ).h

    def h_with_right_delta(delta: np.ndarray) -> float:
        return cbf_core.capsule_pair_h_and_grads(
            "left", "right", left_a, left_b, jac, jac, 0.02,
            right_a + delta, right_b + delta, jac, jac, 0.02, 0.03,
        ).h

    numeric_left = np.empty(3)
    numeric_right = np.empty(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = eps
        numeric_left[i] = (h_with_left_delta(delta) - h_with_left_delta(-delta)) / (2 * eps)
        numeric_right[i] = (h_with_right_delta(delta) - h_with_right_delta(-delta)) / (2 * eps)

    assert np.allclose(base.grad_left[:3], numeric_left, atol=1e-5, rtol=1e-4)
    assert np.allclose(base.grad_right[:3], numeric_right, atol=1e-5, rtol=1e-4)
    assert np.allclose(base.grad_left[3:], 0.0)
    assert np.allclose(base.grad_right[3:], 0.0)


def test_lift_arm_constraint_to_dual_keeps_metadata_and_does_not_cross_wires():
    single = cbf_core.CbfConstraint(
        name="environment",
        source="environment",
        a=np.arange(ARM_DIM, dtype=np.float64),
        b_total=0.4,
        b_delta=0.3,
        h=-0.2,
        active=True,
        debug={"tag": "keep"},
    )
    left = cbf_core.lift_arm_constraint_to_dual(single, "left", ARM_DIM)
    right = cbf_core.lift_arm_constraint_to_dual(single, "right", ARM_DIM)

    assert left.a.shape == (DUAL_DIM,)
    assert right.a.shape == (DUAL_DIM,)
    assert np.allclose(left.a[:ARM_DIM], single.a)
    assert np.allclose(left.a[ARM_DIM:], 0.0)
    assert np.allclose(right.a[:ARM_DIM], 0.0)
    assert np.allclose(right.a[ARM_DIM:], single.a)
    for result, source in ((left, "left_env"), (right, "right_env")):
        assert result.source == source
        assert result.b_total == single.b_total
        assert result.b_delta == single.b_delta
        assert result.h == single.h
        assert result.debug == single.debug


def test_inter_arm_constraint_uses_existing_cbf_inequality_sign():
    pair = cbf_core.CapsulePairBarrier(
        left_name="left",
        right_name="right",
        h=-0.1,
        distance=0.1,
        normal=np.array([1.0, 0.0, 0.0]),
        s_left=0.5,
        t_right=0.5,
        p_left=np.zeros(3),
        p_right=np.array([-0.1, 0.0, 0.0]),
        grad_left=np.r_[1.0, np.zeros(ARM_DIM - 1)],
        grad_right=np.r_[-1.0, np.zeros(ARM_DIM - 1)],
    )
    dq_nominal = np.zeros(DUAL_DIM)
    dq_nominal[0] = 0.01
    dq_nominal[ARM_DIM] = -0.02
    constraint = cbf_core.inter_arm_constraint_from_capsule_pair(
        pair, dq_nominal, gamma=0.8, activate_margin=0.06
    )
    safe_correction = np.zeros(DUAL_DIM)
    safe_correction[0] = 0.03
    safe_correction[ARM_DIM] = -0.02
    reverse_correction = -safe_correction

    assert constraint.a.shape == (DUAL_DIM,)
    assert constraint.active is True
    assert np.isclose(constraint.b_total, 0.08)
    assert np.isclose(constraint.b_delta, 0.05)
    assert constraint.a @ (dq_nominal + safe_correction) >= constraint.b_total - 1e-12
    assert constraint.a @ (dq_nominal + reverse_correction) < constraint.b_total


def test_inter_arm_top_k_selects_lowest_h_and_zero_means_all(monkeypatch):
    values = {
        ("left_0", "right_0"): 0.4,
        ("left_0", "right_1"): -0.2,
        ("left_1", "right_0"): 0.1,
        ("left_1", "right_1"): -0.5,
    }

    def fake_endpoint_states(*_args):
        return np.zeros(3), np.zeros((3, ARM_DIM)), np.ones(3), np.zeros((3, ARM_DIM))

    def fake_pair(*, left_name, right_name, **_kwargs):
        h = values[(left_name, right_name)]
        return cbf_core.CapsulePairBarrier(
            left_name=left_name,
            right_name=right_name,
            h=h,
            distance=h + 1.0,
            normal=np.array([1.0, 0.0, 0.0]),
            s_left=0.0,
            t_right=0.0,
            p_left=np.zeros(3),
            p_right=np.zeros(3),
            grad_left=np.zeros(ARM_DIM),
            grad_right=np.zeros(ARM_DIM),
        )

    monkeypatch.setattr(cbf_core, "_capsule_endpoint_states", fake_endpoint_states)
    monkeypatch.setattr(cbf_core, "capsule_pair_h_and_grads", fake_pair)
    left = [cbf_core.CapsuleMonitor(f"left_{i}", 0, 1, 0.02) for i in range(2)]
    right = [cbf_core.CapsuleMonitor(f"right_{i}", 0, 1, 0.02) for i in range(2)]
    cfg = cbf_core.DualArmCbfConfig(top_k_inter_arm=3, activate_margin_inter_arm=1.0)
    constraints, info = cbf_core.build_inter_arm_constraints_from_capsules(
        None, None, None, None, left, right, np.zeros(DUAL_DIM), cfg
    )

    assert [item.name for item in constraints] == [
        "left_1<->right_1",
        "left_0<->right_1",
        "left_1<->right_0",
    ]
    assert info["n_interarm_candidates"] == 4
    assert info["n_interarm_selected"] == 3
    assert info["n_interarm_constraints"] == 3

    all_constraints, all_info = cbf_core.build_inter_arm_constraints_from_capsules(
        None,
        None,
        None,
        None,
        left,
        right,
        np.zeros(DUAL_DIM),
        cbf_core.DualArmCbfConfig(top_k_inter_arm=0, activate_margin_inter_arm=1.0),
    )
    assert len(all_constraints) == 4
    assert all_info["n_interarm_selected"] == 4

    large_constraints, large_info = cbf_core.build_inter_arm_constraints_from_capsules(
        None,
        None,
        None,
        None,
        left,
        right,
        np.zeros(DUAL_DIM),
        cbf_core.DualArmCbfConfig(top_k_inter_arm=10, activate_margin_inter_arm=1.0),
    )
    assert len(large_constraints) == 4
    assert large_info["n_interarm_selected"] == 4

    values[("left_0", "right_0")] = -0.5
    tied_constraints, tied_info = cbf_core.build_inter_arm_constraints_from_capsules(
        None,
        None,
        None,
        None,
        left,
        right,
        np.zeros(DUAL_DIM),
        cbf_core.DualArmCbfConfig(top_k_inter_arm=2, activate_margin_inter_arm=1.0),
    )
    assert len(tied_constraints) == 2
    assert tied_info["n_interarm_selected"] == 2


def test_dual_arm_qp_safe_case_returns_zero_correction(monkeypatch):
    monkeypatch.setattr(
        cbf_core,
        "build_environment_constraints_for_arm",
        lambda *_args: ([], _empty_env_info()),
    )
    monkeypatch.setattr(
        cbf_core,
        "build_inter_arm_constraints_from_capsules",
        lambda *_args, **_kwargs: ([], _empty_inter_info()),
    )
    correction_left, correction_right, info = cbf_core.solve_dual_arm_cbf_correction(
        None,
        None,
        None,
        None,
        np.zeros(ARM_DIM),
        np.zeros(ARM_DIM),
        cbf_core.DualArmCbfConfig(),
        [],
        [],
        [],
        None,
        None,
    )

    assert correction_left.shape == (ARM_DIM,)
    assert correction_right.shape == (ARM_DIM,)
    assert np.allclose(correction_left, 0.0)
    assert np.allclose(correction_right, 0.0)
    assert info["dual_cbf_active"] is False


def test_dual_arm_qp_unsafe_constraint_corrects_in_safe_direction_and_respects_bounds(monkeypatch):
    a = np.zeros(DUAL_DIM)
    a[0] = 1.0
    a[ARM_DIM] = -1.0
    unsafe = cbf_core.CbfConstraint(
        name="left<->right",
        source="inter_arm",
        a=a,
        b_total=0.06,
        b_delta=0.06,
        h=-0.1,
        active=True,
    )
    inter_info = {
        **_empty_inter_info(),
        "h_LR_min": -0.1,
        "distance_LR_min": 0.1,
        "worst_left_link": "left",
        "worst_right_link": "right",
        "n_interarm_constraints": 1,
    }
    monkeypatch.setattr(
        cbf_core,
        "build_environment_constraints_for_arm",
        lambda *_args: ([], _empty_env_info()),
    )
    monkeypatch.setattr(
        cbf_core,
        "build_inter_arm_constraints_from_capsules",
        lambda *_args, **_kwargs: ([unsafe], inter_info),
    )
    cfg = cbf_core.DualArmCbfConfig(dq_max=0.05)
    correction_left, correction_right, info = cbf_core.solve_dual_arm_cbf_correction(
        None,
        None,
        None,
        None,
        np.zeros(ARM_DIM),
        np.zeros(ARM_DIM),
        cfg,
        [],
        [],
        [],
        None,
        None,
    )
    correction = np.concatenate([correction_left, correction_right])

    assert info["dual_cbf_active"] is True
    assert np.all(np.isfinite(correction))
    assert a @ correction >= unsafe.b_total - 1e-6
    assert correction_left[0] > 0.0
    assert correction_right[0] < 0.0
    assert np.all(np.abs(correction) <= cfg.dq_max + 1e-12)
