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
from soarm100_vision.sdf_cbf_core import TableFilter, VoxelPersistence, WorkspaceCrop


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
    # 0.10s @ 50Hz => 5 steps; still far from grasp so must time out, not final_stable.
    sm = GraspStateMachine(
        GraspThresholds(final_approach_timeout=0.10, final_stable_time=0.10, final_grasp_dist=0.01),
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
    assert last.phase == GraspPhase.CLOSE
    assert sm.last_reason == "final_timeout"


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
