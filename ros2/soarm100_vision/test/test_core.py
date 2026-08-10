from pathlib import Path

import numpy as np

from soarm100_vision.grasp_core import (
    GraspObservation,
    GraspPhase,
    GraspPlan,
    GraspStateMachine,
    GraspThresholds,
    TrackingObservation,
)
from soarm100_vision.policy_backend_core import (
    MujocoExternalGraspConfig,
    PlannedGraspCommand,
    PoseWxyz,
    build_mujoco_external_grasp_cmd,
)
from soarm100_vision.mujoco_inprocess_runner import (
    MujocoInProcessRunner,
    MujocoRunnerConfig,
)
from soarm100_vision.sdf_cbf_core import TableFilter, VoxelPersistence, WorkspaceCrop
from soarm100_vision.vision_utils import color_components, hsv_color_mask, parse_rgb
from soarm100_vision.hardware_joint_bridge import (
    JOINT_NAMES,
    decode_hardware_joint_packet,
)
from soarm100_vision.target_segmenter_node import (
    normalize_model_names,
    resolve_fixed_class_id,
)


def test_fixed_detector_class_names_support_dict_and_list():
    assert normalize_model_names({0: "jpgCat", 1: "Chiikawa"}) == {
        0: "jpgCat",
        1: "Chiikawa",
    }
    assert normalize_model_names(["jpgCat", "Chiikawa"]) == {
        0: "jpgCat",
        1: "Chiikawa",
    }


def test_fixed_detector_class_resolution_is_case_insensitive():
    assert resolve_fixed_class_id(
        {0: "jpgCat", 1: "Chiikawa", 2: "tissue"}, "chiikawa"
    ) == (1, "Chiikawa")


def test_fixed_detector_unknown_class_reports_available_names():
    import pytest

    with pytest.raises(RuntimeError, match="available=jpgCat,Chiikawa,tissue"):
        resolve_fixed_class_id(
            {0: "jpgCat", 1: "Chiikawa", 2: "tissue"}, "cube"
        )


def test_hardware_joint_packet_decode_orders_policy_joints():
    import json

    policy = {name: index * 0.1 for index, name in enumerate(reversed(JOINT_NAMES))}
    payload = json.dumps(
        {
            "schema_version": 1,
            "sequence": 42,
            "timestamp": "2026-07-30T12:00:00+08:00",
            "source": "so100_plus_feetech_read_only",
            "policy": policy,
        }
    ).encode("ascii")
    packet = decode_hardware_joint_packet(payload)
    assert packet.sequence == 42
    assert packet.positions == tuple(float(policy[name]) for name in JOINT_NAMES)


def test_hardware_joint_packet_rejects_missing_joint():
    import json
    import pytest

    payload = json.dumps(
        {
            "schema_version": 1,
            "sequence": 1,
            "source": "so100_plus_feetech_read_only",
            "policy": {name: 0.0 for name in JOINT_NAMES[:-1]},
        }
    ).encode("ascii")
    with pytest.raises(ValueError, match="exactly the seven"):
        decode_hardware_joint_packet(payload)


def test_grasp_state_machine_tracks_position_only():
    plan = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    sm = GraspStateMachine(GraspThresholds(track_max_delta=0.02, track_gain=1.0), ctrl_dt=0.02)
    sm.reset(plan)
    sm.phase = GraspPhase.FINAL_APPROACH
    intent = sm.step(
        GraspObservation(
            tcp_pos=np.array([0.33, 0.0, 0.07]),
            dist_to_control=0.02,
            final_err=0.02,
            tracking=TrackingObservation(valid=True, delta_world=np.array([0.01, -0.002, 0.0]), source="wrist"),
        )
    )
    assert intent.phase == GraspPhase.FINAL_APPROACH
    assert np.allclose(intent.target_pos, np.array([0.35, -0.002, 0.07]))
    assert np.allclose(intent.target_quat_wxyz, plan.grasp_quat_wxyz)


def test_final_approach_timeout_uses_independent_seconds():
    plan = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    # A near pose may commit on the soft timeout, but a far pose must not close.
    sm = GraspStateMachine(
        GraspThresholds(
            final_approach_timeout=0.10,
            final_total_timeout=0.20,
            final_stable_time=0.10,
            final_grasp_dist=0.01,
            final_timeout_close_dist=0.03,
        ),
        ctrl_dt=0.02,
    )
    sm.reset(plan)
    sm.phase = GraspPhase.FINAL_APPROACH
    last = None
    for _ in range(5):
        last = sm.step(
            GraspObservation(
                tcp_pos=np.array([0.30, 0.0, 0.12]),
                dist_to_control=0.06,
                final_err=0.06,
            )
        )
    assert last is not None
    assert last.phase == GraspPhase.FINAL_APPROACH
    assert sm.last_reason != "close_gate_timeout_near"


def test_close_gate_freezes_tracking_until_replan():
    plan = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    sm = GraspStateMachine(
        GraspThresholds(
            final_grasp_dist=0.015,
            final_stable_time=0.04,
            close_tracking_confidence=0.45,
            close_target_speed=0.005,
        ),
        ctrl_dt=0.02,
    )
    sm.reset(plan)
    sm.phase = GraspPhase.FINAL_APPROACH
    tracking = TrackingObservation(
        valid=True,
        confidence=0.9,
        delta_world=np.array([0.005, 0.0, 0.0]),
        source="wrist",
    )
    obs = GraspObservation(
        tcp_pos=plan.grasp_pos.copy(),
        dist_to_control=0.01,
        final_err=0.01,
        target_speed=0.0,
        tracking=tracking,
    )
    sm.step(obs)
    intent = sm.step(obs)
    assert intent.phase == GraspPhase.COMMIT_GRASP
    committed = sm.plan.grasp_pos.copy()

    intent = sm.step(
        GraspObservation(
            tcp_pos=committed.copy(),
            dist_to_control=0.0,
            final_err=0.0,
            target_speed=0.0,
            tracking=TrackingObservation(
                valid=True,
                confidence=1.0,
                delta_world=np.array([-0.02, 0.02, 0.0]),
                source="wrist",
            ),
        )
    )
    assert intent.phase == GraspPhase.CLOSE
    assert intent.should_freeze_arm
    assert np.allclose(sm.plan.grasp_pos, committed)


def test_default_close_gate_accepts_observed_policy_error():
    plan = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    sm = GraspStateMachine(GraspThresholds(final_stable_time=0.04), ctrl_dt=0.02)
    sm.reset(plan)
    sm.phase = GraspPhase.FINAL_APPROACH
    obs = GraspObservation(
        tcp_pos=plan.grasp_pos.copy(),
        dist_to_control=0.032,
        final_err=0.032,
        target_speed=0.0,
        tracking=TrackingObservation(valid=True, confidence=0.9, source="wrist"),
    )
    sm.step(obs)
    intent = sm.step(obs)
    assert intent.phase == GraspPhase.COMMIT_GRASP
    assert intent.reason == "close_gate_stable"


def test_tracking_loss_before_close_does_not_trigger_replan():
    plan = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    sm = GraspStateMachine(
        GraspThresholds(final_approach_timeout=0.10, final_total_timeout=0.20),
        ctrl_dt=0.02,
    )
    sm.reset(plan)
    sm.phase = GraspPhase.FINAL_APPROACH
    for _ in range(6):
        intent = sm.step(
            GraspObservation(
                tcp_pos=plan.grasp_pos.copy(),
                dist_to_control=0.01,
                final_err=0.01,
                tracking=TrackingObservation(
                    valid=False,
                    confidence=0.0,
                    replan_required=True,
                    source="wrist",
                ),
            )
        )
    assert intent.phase == GraspPhase.FINAL_APPROACH
    assert not intent.should_plan_grasp


def test_dynamic_target_starts_at_anchor_and_dwells_at_endpoints():
    runner = MujocoInProcessRunner(
        MujocoRunnerConfig(
            repo_root=Path("."),
            target_motion="line",
            target_motion_amplitude=0.03,
            target_motion_travel_time=2.0,
            target_motion_dwell_time=1.0,
            target_motion_delay=2.0,
            ctrl_dt=0.02,
        )
    )
    anchor = np.array([0.42, 0.08, 0.021])
    at_start, speed_start, phase_start = runner._target_motion_state(2.0, anchor)
    at_positive, speed_positive, phase_positive = runner._target_motion_state(
        3.0, anchor
    )
    at_negative, speed_negative, phase_negative = runner._target_motion_state(
        6.0, anchor
    )
    at_cycle, speed_cycle, _ = runner._target_motion_state(8.0, anchor)

    assert np.allclose(at_start, anchor)
    assert np.allclose(speed_start, 0.0)
    assert phase_start == "move_positive_y"
    assert np.isclose(at_positive[1], anchor[1] + 0.03)
    assert np.allclose(speed_positive, 0.0, atol=1.0e-12)
    assert phase_positive == "dwell_positive_y"
    assert np.isclose(at_negative[1], anchor[1] - 0.03)
    assert np.allclose(speed_negative, 0.0, atol=1.0e-12)
    assert phase_negative == "dwell_negative_y"
    assert np.allclose(at_cycle, anchor)
    assert np.allclose(speed_cycle, 0.0, atol=1.0e-12)


def test_configurable_color_mask_selects_only_target_color():
    rgb = np.zeros((80, 100, 3), dtype=np.uint8)
    rgb[20:50, 30:70] = np.array([245, 15, 12], dtype=np.uint8)
    rgb[5:15, 5:15] = np.array([20, 230, 20], dtype=np.uint8)
    mask = hsv_color_mask(
        rgb,
        target_rgb=parse_rgb("255,0,0"),
        hue_tolerance_deg=18.0,
        saturation_min=0.45,
        value_min=0.30,
    )
    components = color_components(mask, min_area=20)
    assert len(components) == 1
    assert components[0]["bbox"] == (30, 20, 70, 50)
    assert int(components[0]["area"]) == 1200


def test_replan_accept_replaces_plan_and_counts_attempt():
    initial = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    updated = GraspPlan(
        pregrasp_pos=np.array([0.32, 0.03, 0.11]),
        grasp_pos=np.array([0.36, 0.03, 0.08]),
        grasp_quat_wxyz=np.array([0.7, 0.0, 0.7, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    sm = GraspStateMachine(GraspThresholds(replan_max_attempts=2), ctrl_dt=0.02)
    sm.reset(initial)
    sm.phase = GraspPhase.REPLAN_GRASP
    sm.accept_replan(updated)
    assert sm.phase == GraspPhase.MOVE_TO_PREGRASP
    assert sm.replan_attempts == 1
    assert np.allclose(sm.plan.grasp_pos, updated.grasp_pos)


def test_replan_rejection_exhausts_attempt_budget():
    plan = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    sm = GraspStateMachine(GraspThresholds(replan_max_attempts=1), ctrl_dt=0.02)
    sm.reset(plan)
    sm.phase = GraspPhase.REPLAN_GRASP
    sm.reject_replan("no_points")
    intent = sm.step(
        GraspObservation(
            tcp_pos=plan.pregrasp_pos.copy(),
            dist_to_control=0.0,
            final_err=0.0,
        )
    )
    assert intent.done
    assert not intent.success
    assert "replan_attempts_exhausted" in intent.reason


def test_second_lift_failure_does_not_exceed_replan_budget():
    plan = GraspPlan(
        pregrasp_pos=np.array([0.30, 0.00, 0.10]),
        grasp_pos=np.array([0.34, 0.00, 0.07]),
        grasp_quat_wxyz=np.array([1.0, 0.0, 0.0, 0.0]),
        approach_axis_world=np.array([1.0, 0.0, 0.0]),
    )
    sm = GraspStateMachine(
        GraspThresholds(replan_max_attempts=1, lift_time=0.02),
        ctrl_dt=0.02,
    )
    sm.reset(plan)
    sm.accept_replan(plan)
    sm.phase = GraspPhase.LIFT
    intent = sm.step(
        GraspObservation(
            tcp_pos=plan.grasp_pos.copy(),
            dist_to_control=0.0,
            final_err=0.0,
            target_lift=0.0,
        )
    )
    assert intent.done
    assert not intent.should_plan_grasp
    assert "lift_failed_replan_exhausted" in intent.reason


def test_workspace_table_persistence_pipeline():
    points = np.array(
        [
            [0.0, 0.0, 0.04],
            [0.0, 0.0, 0.10],
            [0.40, 0.0, 0.10],
        ],
        dtype=np.float32,
    )
    cropped = WorkspaceCrop(x_min=-0.1, x_max=0.1, y_min=-0.1, y_max=0.1, z_min=0.0, z_max=0.2).apply(points)
    filtered, n_table = TableFilter(enabled=True, z_max=0.055).apply(cropped)
    persistence = VoxelPersistence(voxel_size=0.01, min_hits=2, forget_frames=4)
    assert cropped.shape[0] == 2
    assert n_table == 1
    assert persistence.update(filtered).shape[0] == 0
    assert persistence.update(filtered).shape[0] == 1


def test_mujoco_external_command_builder_tracking_switch():
    cfg = MujocoExternalGraspConfig(
        repo_root=Path("."),
        python_executable="python",
        enable_internal_tracking=False,
        enable_avoidance=True,
    )
    grasp = PlannedGraspCommand(
        pregrasp=PoseWxyz(np.array([0.1, 0.2, 0.3]), np.array([1.0, 0.0, 0.0, 0.0])),
        grasp=PoseWxyz(np.array([0.2, 0.2, 0.3]), np.array([1.0, 0.0, 0.0, 0.0])),
        gripper_width=0.05,
    )
    cmd = build_mujoco_external_grasp_cmd(cfg, grasp)
    assert "--no-grasp-track-object" in cmd
    assert "--enable-sdf-cbf-qp" in cmd
    assert "0.100000,0.200000,0.300000" in cmd
