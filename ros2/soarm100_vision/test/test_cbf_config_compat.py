"""Pure-Python regression coverage for shared CBF configuration boundaries."""

import ast
from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "mujoco"))
import cbf as cbf_core  # noqa: E402


def test_shared_defaults_are_legacy_real_safe():
    cfg = cbf_core.CbfConfig()

    assert cfg.capsule_sample_count == 9
    assert cfg.qp_metric == "identity"
    assert cfg.dynamic_obstacle_lookahead_steps == 0.0


def test_explicit_enhanced_sampling_is_used(monkeypatch):
    calls = []

    def fake_distance(point, obstacle, d_safe, r_link):
        calls.append(np.asarray(point).copy())
        return float(np.linalg.norm(point)), np.array([1.0, 0.0, 0.0])

    monkeypatch.setattr(cbf_core, "obstacle_h_and_grad_p", fake_distance)
    p0 = np.zeros(3)
    p1 = np.array([1.0, 0.0, 0.0])
    jac = np.zeros((3, 7))
    obstacle = cbf_core.AxisAlignedBoxObstacle("box", np.zeros(3), np.ones(3))
    cbf_core.segment_obstacle_h_and_grad(
        p0, p1, jac, jac, obstacle, 0.02, 0.03, n_samples=17
    )

    assert len(calls) == 17
    assert np.allclose(calls[0], p0)
    assert np.allclose(calls[-1], p1)


def test_configured_sampling_reaches_capsule_barrier(monkeypatch):
    calls = []
    capsule = cbf_core.CapsuleMonitor("a->b", 1, 2, 0.03)
    config = cbf_core.CbfConfig(capsule_sample_count=17)
    obstacle = cbf_core.AxisAlignedBoxObstacle("box", np.zeros(3), np.ones(3))

    monkeypatch.setattr(
        cbf_core,
        "body_pos_and_jacobian",
        lambda *args: (np.zeros(3), np.zeros((3, 7))),
    )

    def fake_segment(*args, **kwargs):
        calls.append(kwargs["n_samples"])
        return 1.0, np.zeros(7), np.zeros(3), 0.0

    monkeypatch.setattr(cbf_core, "segment_obstacle_h_and_grad", fake_segment)
    cbf_core._worst_barrier(
        model=None,
        data=None,
        ids=None,
        monitors=[capsule],
        obstacles=[obstacle],
        cfg=config,
        tcp_pose_fn=None,
    )

    assert calls == [17]


def test_identity_metric_is_default_and_task_metric_is_explicit():
    jac = np.eye(3, 7)
    identity = cbf_core.make_qp_metric_hessian(cbf_core.CbfConfig(), 7, jac)
    enhanced_cfg = cbf_core.CbfConfig(
        qp_metric="task_preserving", task_preserve_weight=5.0
    )
    enhanced = cbf_core.make_qp_metric_hessian(enhanced_cfg, 7, jac)

    assert np.allclose(identity, np.eye(7))
    assert np.allclose(enhanced, np.eye(7) + 5.0 * jac.T @ jac)
    assert np.allclose(enhanced, enhanced.T)
    assert np.linalg.eigvalsh(enhanced).min() > 0.0


def test_legacy_constructor_and_single_arm_stack_remain_compatible():
    cfg = cbf_core.CbfConfig(d_safe=0.03, gamma=0.5)
    a, b_total, b_delta = cbf_core._build_constraints([], cfg, np.zeros(7))

    assert a.shape == (0, 7)
    assert b_total.shape == (0,)
    assert b_delta.shape == (0,)


def test_real_policy_pins_legacy_shared_cbf_options():
    source = (REPO_ROOT / "ros2/soarm100_vision/soarm100_vision/policy_reach_node.py").read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "CbfConfig"
    ]
    assert len(calls) == 1
    kwargs = {item.arg: item.value for item in calls[0].keywords}

    assert ast.literal_eval(kwargs["capsule_sample_count"]) == 9
    assert ast.literal_eval(kwargs["qp_metric"]) == "identity"


def test_single_arm_solver_does_not_reference_dual_arm_entrypoint():
    source = Path(cbf_core.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    single = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "solve_cbf_correction"
    )
    calls = [
        node.func.id
        for node in ast.walk(single)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    ]

    assert "solve_dual_arm_cbf_correction" not in calls
