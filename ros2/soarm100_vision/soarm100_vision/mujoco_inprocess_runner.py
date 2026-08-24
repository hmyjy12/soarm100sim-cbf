from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

import numpy as np

from soarm100_vision.grasp_core import (
    GraspObservation,
    GraspPhase,
    GraspPlan,
    GraspStateMachine,
    GraspThresholds,
    TrackingObservation,
)
from soarm100_vision.policy_backend_core import PlannedGraspCommand


@dataclass
class MujocoRunnerConfig:
    repo_root: Path
    mjcf: str = "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"
    checkpoint: str = "rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt"
    target_object: str = "cube"
    target_body: str = "target_object"
    target_pos: str = "0.42,0.08,0.021"
    object_settle_s: float = 0.75
    target_motion: str = "none"
    target_motion_amplitude: float = 0.050
    target_motion_travel_time: float = 2.0
    target_motion_dwell_time: float = 1.0
    target_motion_delay: float = 0.5
    enable_tracking: bool = True
    enable_obstacle: bool = False
    obstacle_mode: str = "static"
    obstacle_body: str = "obstacle_rod_mount"
    obstacle_pos: str = "0.16,0.09,0.02"
    obstacle_motion: str = "none"
    obstacle_motion_amp: str = "0.03,0.00,0.00"
    obstacle_motion_period: float = 5.0
    enable_cbf: bool = False
    cbf_d_safe: float = 0.020
    cbf_gamma: float = 0.8
    cbf_lambda: float = 0.5
    cbf_activate_margin: float = 0.040
    sdf_voxel_size: float = 0.010
    sdf_inflate: float = 0.015
    replan_max_attempts: int = 2
    final_approach_timeout: float = 10.0
    final_grasp_dist: float = 0.035
    final_timeout_close_dist: float = 0.040
    final_stable_time: float = 0.20
    track_max_delta: float = 0.080
    close_tracking_confidence: float = 0.45
    close_target_speed: float = 0.005
    return_home_on_failure: bool = True
    return_home_timeout: float = 8.0
    return_home_tolerance: float = 0.020
    return_home_stable_time: float = 0.20
    camera_publish_interval_steps: int = 5
    replan_camera_settle_s: float = 0.15
    max_steps: int = 900
    open_q: float = 1.2
    close_q: float = 0.4
    ctrl_dt: float = 0.02
    speed: float = 1.0
    show_viewer: bool = False
    viewer_sync_interval: int = 1
    viewer_hold_s: float = 8.0
    traj_log: str = "log/runtime/ros2_inprocess_grasp.jsonl"


@dataclass
class MujocoRunResult:
    success: bool
    reason: str
    lift_height: float
    final_phase: str
    steps: int


class MujocoInProcessRunner:
    """Minimal in-process MuJoCo grasp runner.

    The runner is a deployment-shape bridge: ROS2 owns planning/tracking/SDF
    topics, while this class owns only MuJoCo I/O for simulation validation. It
    intentionally accepts an already planned grasp and uses GraspStateMachine
    instead of embedding grasp transitions in the ROS node.
    """

    def __init__(self, cfg: MujocoRunnerConfig) -> None:
        self.cfg = cfg
        self.repo = Path(cfg.repo_root).expanduser().resolve()
        self._log_stream = None

    def run(
        self,
        cmd: PlannedGraspCommand,
        *,
        feedback_cb=None,
        tracking_provider=None,
        obstacle_provider=None,
        replan_provider=None,
        camera_frame_cb=None,
        sim_state_cb=None,
    ) -> MujocoRunResult:
        modules = self._load_mujoco_modules()
        mujoco = modules["mujoco"]
        runtime = modules["runtime"]
        policy_mod = modules["policy"]
        constants = modules["constants"]
        cbf_mod = modules["cbf"]
        camera_mod = modules["camera"]

        mjcf = Path(self.cfg.mjcf)
        if not mjcf.is_absolute():
            mjcf = self.repo / mjcf
        ckpt = Path(self.cfg.checkpoint)
        if not ckpt.is_absolute():
            ckpt = self.repo / ckpt

        model = mujoco.MjModel.from_xml_path(str(mjcf))
        data = mujoco.MjData(model)
        viewer = None
        camera_rig = None
        # Create the offscreen GLFW context before the passive viewer context.
        # Creating it after launch_passive() makes the first camera render race
        # with the viewer context and has caused intermittent native crashes.
        if camera_frame_cb is not None:
            camera_rig = camera_mod.MujocoCameraRig(
                model, width=640, height=480
            )
        if bool(self.cfg.show_viewer):
            import mujoco.viewer  # type: ignore

            viewer = mujoco.viewer.launch_passive(model, data)
        ids = runtime.resolve_robot_ids(model)
        policy = policy_mod.SkrlGaussianPolicy(ckpt)
        cbf_cfg = None
        cbf_monitors = None
        if bool(self.cfg.enable_cbf):
            cbf_cfg = cbf_mod.CbfConfig(
                d_safe=float(self.cfg.cbf_d_safe),
                gamma=float(self.cfg.cbf_gamma),
                lambda_cbf=float(self.cfg.cbf_lambda),
                activate_margin=float(self.cfg.cbf_activate_margin),
            )
            cbf_monitors = cbf_mod.resolve_monitors(model, cbf_cfg.monitor_specs, cbf_cfg.capsule_specs)
        stepper = runtime.ReachStepper(
            policy=policy,
            ids=ids,
            model=model,
            enable_cbf=bool(self.cfg.enable_cbf),
            cbf_cfg=cbf_cfg,
            cbf_monitors=cbf_monitors,
        )
        runtime.reset_home(model, data, ids)
        self._configure_grasp_targets(mujoco, model, data)
        self._set_target_body(mujoco, model, data, str(self.cfg.target_body), self._parse_vec3(self.cfg.target_pos))
        self._configure_obstacle(mujoco, model, data)
        mujoco.mj_forward(model, data)
        self._settle_object(mujoco, model, data)
        mujoco.mj_forward(model, data)
        home_tcp_pos, home_tcp_quat = runtime.tcp_pose_w(data, ids)
        home_tcp_pos = np.asarray(home_tcp_pos, dtype=np.float64).copy()
        home_tcp_quat = np.asarray(home_tcp_quat, dtype=np.float64).copy()
        if sim_state_cb is not None:
            sim_state_cb(
                float(data.time), np.asarray(data.qpos, dtype=np.float64).copy()
            )
        if camera_frame_cb is not None:
            assert camera_rig is not None
            self._publish_camera_frame(camera_rig, data, model, constants, camera_frame_cb)

        plan = GraspPlan(
            pregrasp_pos=np.asarray(cmd.pregrasp.pos, dtype=np.float64).reshape(3),
            grasp_pos=np.asarray(cmd.grasp.pos, dtype=np.float64).reshape(3),
            grasp_quat_wxyz=np.asarray(cmd.grasp.quat_wxyz, dtype=np.float64).reshape(4),
            approach_axis_world=np.array([1.0, 0.0, 0.0], dtype=np.float64),
            gripper_width=float(cmd.gripper_width),
        )
        thresholds = GraspThresholds(
            replan_max_attempts=max(int(self.cfg.replan_max_attempts), 0),
            final_approach_timeout=max(
                float(self.cfg.final_approach_timeout), float(self.cfg.ctrl_dt)
            ),
            final_grasp_dist=max(float(self.cfg.final_grasp_dist), 0.0),
            final_timeout_close_dist=max(
                float(self.cfg.final_timeout_close_dist), 0.0
            ),
            final_stable_time=max(float(self.cfg.final_stable_time), 0.0),
            track_max_delta=max(float(self.cfg.track_max_delta), 0.0),
            close_tracking_confidence=max(
                float(self.cfg.close_tracking_confidence), 0.0
            ),
            close_target_speed=max(float(self.cfg.close_target_speed), 0.0),
        )
        sm = GraspStateMachine(thresholds, ctrl_dt=float(self.cfg.ctrl_dt))
        sm.reset(plan)
        # MuJoCo provides the exact object center only to bootstrap the wrist
        # template. Subsequent motion is estimated from wrist RGB tracking.
        tracking_reference_world = self._target_pos(mujoco, model, data)

        target_initial_z = self._target_z(mujoco, model, data)
        frozen_q = None
        close_start_q = None
        last_intent = None
        best_lift = 0.0
        obstacle_points = np.zeros((0, 3), dtype=np.float64)
        obstacle_seq = -1
        obstacle_base_pos = self._parse_vec3(self.cfg.obstacle_pos)
        obstacle_motion_amp = self._parse_vec3(self.cfg.obstacle_motion_amp)
        current_obstacle_pos = obstacle_base_pos.copy()
        obstacle_step_velocity = np.zeros(3, dtype=np.float64)
        target_motion_anchor = self._target_pos(mujoco, model, data)
        target_motion_epoch = 0.0
        target_motion_frozen = False
        target_motion_armed = not bool(self.cfg.enable_tracking)
        target_motion_phase = "disabled"
        target_commanded_pos = target_motion_anchor.copy()
        target_velocity = np.zeros(3, dtype=np.float64)
        self._target_motion_anchor = target_motion_anchor.copy()
        log_path = self._log_path()
        native_log_stream = None
        if log_path is not None:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            self._log_stream = log_path.open("w", encoding="utf-8", buffering=65536)
            native_path = log_path.with_suffix(log_path.suffix + ".native.log")
            native_log_stream = native_path.open("w", encoding="utf-8", buffering=1)
            print(f"[mujoco_runner] native stage log -> {native_path}", flush=True)

        def native_stage(step_index: int, stage: str) -> None:
            if native_log_stream is None:
                return
            native_log_stream.write(
                f"{time.time():.9f} step={int(step_index)} stage={stage}\n"
            )
            native_log_stream.flush()
            if int(step_index) < 3:
                os.fsync(native_log_stream.fileno())

        try:
            total_step_budget = int(self.cfg.max_steps) * (1 + max(int(self.cfg.replan_max_attempts), 0))
            for step in range(total_step_budget):
                native_stage(step, "loop_begin")
                step_started = time.perf_counter()
                control_time = float(step) * float(self.cfg.ctrl_dt)
                if viewer is not None and not viewer.is_running():
                    return MujocoRunResult(
                        success=False,
                        reason="viewer_closed",
                        lift_height=float(best_lift),
                        final_phase=sm.phase.value,
                        steps=step,
                    )
                target_motion_allowed = sm.phase in (
                    GraspPhase.MOVE_TO_PREGRASP,
                    GraspPhase.FINAL_APPROACH,
                )
                target_motion_enabled = (
                    str(self.cfg.target_motion).strip().lower() == "line"
                )
                if target_motion_enabled and target_motion_allowed:
                    if not target_motion_armed:
                        target_motion_phase = "waiting_for_tracking"
                        target_commanded_pos = target_motion_anchor.copy()
                        target_velocity = np.zeros(3, dtype=np.float64)
                        self._set_target_body(
                            mujoco,
                            model,
                            data,
                            str(self.cfg.target_body),
                            target_commanded_pos,
                            reset_velocity=False,
                        )
                        target_motion_frozen = False
                    else:
                        if target_motion_frozen:
                            target_motion_anchor = self._target_pos(
                                mujoco, model, data
                            )
                            target_motion_epoch = control_time
                            self._target_motion_anchor = target_motion_anchor.copy()
                        target_motion_frozen = False
                        (
                            target_commanded_pos,
                            target_velocity,
                            target_motion_phase,
                        ) = self._target_motion_state(
                            control_time - target_motion_epoch,
                            target_motion_anchor,
                        )
                        self._set_target_body(
                            mujoco,
                            model,
                            data,
                            str(self.cfg.target_body),
                            target_commanded_pos,
                            reset_velocity=False,
                        )
                else:
                    if target_motion_enabled:
                        target_motion_phase = f"frozen_{sm.phase.value.lower()}"
                        target_motion_frozen = True
                    else:
                        target_motion_phase = "disabled"
                    target_commanded_pos = self._target_pos(mujoco, model, data)
                    target_velocity = np.zeros(3, dtype=np.float64)
                if (
                    bool(self.cfg.enable_obstacle)
                    and str(self.cfg.obstacle_motion).strip().lower() != "none"
                ):
                    current_obstacle_pos, obstacle_step_velocity = self._obstacle_motion_state(
                        float(data.time),
                        obstacle_base_pos,
                        obstacle_motion_amp,
                    )
                    self._set_target_body(
                        mujoco,
                        model,
                        data,
                        str(self.cfg.obstacle_body),
                        current_obstacle_pos,
                        reset_velocity=False,
                    )
                if bool(self.cfg.enable_cbf) and obstacle_provider is not None and cbf_cfg is not None:
                    payload = obstacle_provider()
                    next_seq = (
                        int(payload.get("seq", 0))
                        if isinstance(payload, dict)
                        else obstacle_seq + 1
                    )
                    if next_seq != obstacle_seq:
                        raw_points = (
                            payload.get("points", np.zeros((0, 3)))
                            if isinstance(payload, dict)
                            else payload
                        )
                        obstacle_points = np.asarray(
                            raw_points, dtype=np.float64
                        ).reshape(-1, 3)
                        obstacle_seq = next_seq
                        if obstacle_points.shape[0] > 0:
                            stepper.cbf_obstacles = [
                                cbf_mod.PointCloudSdfObstacle(
                                    name="ros2_obstacle_cloud",
                                    points=obstacle_points,
                                    voxel_size=float(self.cfg.sdf_voxel_size),
                                    inflate=float(self.cfg.sdf_inflate),
                                    velocity=obstacle_step_velocity,
                                )
                            ]
                        else:
                            stepper.cbf_obstacles = []

                if (
                    camera_rig is not None
                    and step % max(int(self.cfg.camera_publish_interval_steps), 1) == 0
                ):
                    native_stage(step, "before_camera_render")
                    self._publish_camera_frame(
                        camera_rig,
                        data,
                        model,
                        constants,
                        camera_frame_cb,
                        include_scene=bool(
                            self.cfg.enable_cbf
                            and str(self.cfg.obstacle_mode).strip().lower() == "dynamic"
                        ),
                        include_scene_rgb=False,
                        include_wrist=True,
                        tracking_reference_world=tracking_reference_world,
                    )
                    native_stage(step, "after_camera_render")

                if sm.plan is not None:
                    plan = sm.plan
                tcp_pos, _tcp_quat = runtime.tcp_pose_w(data, ids)
                current_target = plan.pregrasp_pos if sm.phase == GraspPhase.MOVE_TO_PREGRASP else plan.grasp_pos
                target_object_pos = self._target_pos(mujoco, model, data)
                target_lift = float(target_object_pos[2]) - target_initial_z
                best_lift = max(best_lift, float(target_lift))
                tracking_obs = None
                if bool(self.cfg.enable_tracking) and tracking_provider is not None:
                    tracked = tracking_provider()
                    if tracked is not None:
                        tracking_obs = self._rgb_tracking_observation(
                            tracked,
                            model,
                            data,
                            constants,
                            tracking_reference_world,
                        )
                    else:
                        tracking_obs = TrackingObservation(
                            valid=False,
                            source="ros2_wrist_rgb",
                            reason="tracking_sample_unavailable",
                        )
                if (
                    target_motion_enabled
                    and not target_motion_armed
                    and tracking_obs is not None
                    and tracking_obs.valid
                ):
                    target_motion_armed = True
                    target_motion_anchor = self._target_pos(mujoco, model, data)
                    target_motion_epoch = control_time
                    self._target_motion_anchor = target_motion_anchor.copy()
                    target_motion_phase = "tracking_acquired"
                obs = GraspObservation(
                    tcp_pos=np.asarray(tcp_pos, dtype=np.float64),
                    dist_to_control=float(np.linalg.norm(np.asarray(tcp_pos) - current_target)),
                    approach_error_deg=0.0,
                    final_err=float(np.linalg.norm(np.asarray(tcp_pos) - plan.grasp_pos)),
                    target_lift=float(target_lift),
                    target_gripper_contacts=0,
                    target_speed=float(np.linalg.norm(target_velocity)),
                    tracking=tracking_obs,
                )
                intent = sm.step(obs)
                last_intent = intent
                if intent.should_plan_grasp and replan_provider is not None:
                    attempt = int(sm.replan_attempts) + 1
                    if feedback_cb is not None:
                        feedback_cb(
                            GraspPhase.REPLAN_GRASP.value,
                            f"replan_request attempt={attempt}",
                            best_lift,
                        )
                    if camera_rig is not None:
                        self._publish_camera_frame(
                            camera_rig,
                            data,
                            model,
                            constants,
                            camera_frame_cb,
                            include_scene=True,
                            include_scene_rgb=True,
                            include_wrist=True,
                            tracking_reference_world=tracking_reference_world,
                        )
                        time.sleep(max(float(self.cfg.replan_camera_settle_s), 0.0))
                    try:
                        new_cmd, replan_reason = replan_provider(attempt)
                    except Exception as exc:
                        new_cmd, replan_reason = None, f"provider_exception:{exc}"
                    if new_cmd is None:
                        sm.reject_replan(str(replan_reason))
                        self._append_event_log(
                            log_path,
                            step=step,
                            event="replan_reject",
                            attempt=attempt,
                            reason=str(replan_reason),
                        )
                        if feedback_cb is not None:
                            feedback_cb(
                                GraspPhase.REPLAN_GRASP.value,
                                sm.last_reason,
                                best_lift,
                            )
                        continue
                    plan = GraspPlan(
                        pregrasp_pos=np.asarray(new_cmd.pregrasp.pos, dtype=np.float64).reshape(3),
                        grasp_pos=np.asarray(new_cmd.grasp.pos, dtype=np.float64).reshape(3),
                        grasp_quat_wxyz=np.asarray(new_cmd.grasp.quat_wxyz, dtype=np.float64).reshape(4),
                        approach_axis_world=np.array([1.0, 0.0, 0.0], dtype=np.float64),
                        gripper_width=float(new_cmd.gripper_width),
                    )
                    sm.accept_replan(plan)
                    tracking_reference_world = self._target_pos(
                        mujoco, model, data
                    )
                    target_motion_armed = False
                    frozen_q = None
                    close_start_q = None
                    self._append_event_log(
                        log_path,
                        step=step,
                        event="replan_accept",
                        attempt=attempt,
                        reason=str(replan_reason),
                        pregrasp=plan.pregrasp_pos,
                        grasp=plan.grasp_pos,
                        grasp_quat=plan.grasp_quat_wxyz,
                        gripper_width=plan.gripper_width,
                    )
                    if feedback_cb is not None:
                        feedback_cb(
                            sm.phase.value,
                            f"{sm.last_reason} {replan_reason}",
                            best_lift,
                        )
                    continue
                if feedback_cb is not None and step % max(int(round(0.5 / self.cfg.ctrl_dt)), 1) == 0:
                    feedback_cb(intent.phase.value, intent.reason, best_lift)
                if intent.done:
                    return_suffix = ""
                    if (
                        not intent.success
                        and bool(self.cfg.return_home_on_failure)
                        and "replan" in str(intent.reason)
                    ):
                        if feedback_cb is not None:
                            feedback_cb(
                                "RETURN_HOME",
                                f"grasp_failed:{intent.reason}; "
                                f"returning cbf={bool(self.cfg.enable_cbf)}",
                                best_lift,
                            )
                        returned, return_err = self._return_home(
                            mujoco=mujoco,
                            model=model,
                            data=data,
                            runtime=runtime,
                            constants=constants,
                            cbf_mod=cbf_mod,
                            stepper=stepper,
                            ids=ids,
                            target_pos=home_tcp_pos,
                            target_quat=home_tcp_quat,
                            obstacle_provider=obstacle_provider,
                            camera_rig=camera_rig,
                            camera_frame_cb=camera_frame_cb,
                            sim_state_cb=sim_state_cb,
                        )
                        return_suffix = (
                            f"; return_home={'reached' if returned else 'timeout'}"
                            f" err={return_err * 1000.0:.1f}mm"
                            f" cbf={bool(self.cfg.enable_cbf)}"
                        )
                        self._append_event_log(
                            log_path,
                            step=step,
                            event="return_home",
                            attempt=int(sm.replan_attempts),
                            success=returned,
                            error_m=return_err,
                            cbf_enabled=bool(self.cfg.enable_cbf),
                            reason=intent.reason,
                        )
                        if feedback_cb is not None:
                            feedback_cb(
                                "RETURN_HOME",
                                return_suffix.lstrip("; "),
                                best_lift,
                            )
                    return MujocoRunResult(
                        success=bool(intent.success),
                        reason=f"{intent.reason}{return_suffix}",
                        lift_height=float(best_lift),
                        final_phase=sm.phase.value,
                        steps=step,
                    )

                q_before = runtime.joint_pos(data, ids)
                step_info = {}
                if intent.phase == GraspPhase.CLOSE:
                    if frozen_q is None:
                        frozen_q = q_before.copy()
                    if close_start_q is None:
                        close_start_q = q_before.copy()
                    q_tgt = frozen_q.copy()
                    start_grip = float(close_start_q[-1])
                    q_tgt[-1] = (1.0 - intent.gripper_alpha) * start_grip + intent.gripper_alpha * float(self.cfg.close_q)
                else:
                    q_tgt, step_info = stepper.compute_targets(model, data, intent.target_pos, intent.target_quat_wxyz)
                    if intent.gripper_mode == "open":
                        q_tgt[-1] = float(self.cfg.open_q)
                    elif intent.gripper_mode == "close":
                        q_tgt[-1] = float(self.cfg.close_q)

                runtime.set_ctrl(data, ids, q_tgt)
                native_stage(step, "after_set_ctrl")
                self._append_step_log(
                    log_path,
                    step=step,
                    phase=intent.phase.value,
                    reason=intent.reason,
                    q_before=q_before,
                    q_target=q_tgt,
                    tcp_pos=tcp_pos,
                    control_target=intent.target_pos,
                    pregrasp=sm.plan.pregrasp_pos if sm.plan is not None else plan.pregrasp_pos,
                    grasp=sm.plan.grasp_pos if sm.plan is not None else plan.grasp_pos,
                    target_object_pos=target_object_pos,
                    dist_to_control=obs.dist_to_control,
                    final_err=obs.final_err,
                    target_lift=target_lift,
                    best_lift=best_lift,
                    gripper_mode=intent.gripper_mode,
                    tracking_obs=tracking_obs,
                    tracking_frozen=bool(sm.tracking_frozen),
                    close_gate=sm.close_gate,
                    target_commanded_pos=target_commanded_pos,
                    target_velocity=target_velocity,
                    target_motion_phase=target_motion_phase,
                    obstacle_points=obstacle_points,
                    obstacle_pos=current_obstacle_pos,
                    obstacle_velocity=obstacle_step_velocity,
                    info=step_info,
                    enable_cbf=bool(self.cfg.enable_cbf),
                )
                native_stage(step, "after_step_log")
                native_stage(step, "before_mj_step")
                for _ in range(int(constants.DECIMATION)):
                    mujoco.mj_step(model, data)
                native_stage(step, "after_mj_step")
                if sim_state_cb is not None:
                    sim_state_cb(
                        float(data.time),
                        np.asarray(data.qpos, dtype=np.float64).copy(),
                    )
                if step + 1 >= total_step_budget:
                    returned, return_err = self._return_home(
                        mujoco=mujoco,
                        model=model,
                        data=data,
                        runtime=runtime,
                        constants=constants,
                        cbf_mod=cbf_mod,
                        stepper=stepper,
                        ids=ids,
                        target_pos=home_tcp_pos,
                        target_quat=home_tcp_quat,
                        obstacle_provider=obstacle_provider,
                        camera_rig=camera_rig,
                        camera_frame_cb=camera_frame_cb,
                        sim_state_cb=sim_state_cb,
                    )
                    reason = (
                        f"runner_step_budget_exhausted steps={total_step_budget}; "
                        f"return_home={'reached' if returned else 'timeout'} "
                        f"err={return_err * 1000.0:.1f}mm "
                        f"cbf={bool(self.cfg.enable_cbf)}"
                    )
                    self._append_event_log(
                        log_path,
                        step=step,
                        event="return_home",
                        attempt=int(sm.replan_attempts),
                        success=returned,
                        error_m=return_err,
                        cbf_enabled=bool(self.cfg.enable_cbf),
                        reason="runner_step_budget_exhausted",
                    )
                    if feedback_cb is not None:
                        feedback_cb("RETURN_HOME", reason, best_lift)
                    return MujocoRunResult(
                        success=False,
                        reason=reason,
                        lift_height=float(best_lift),
                        final_phase=sm.phase.value,
                        steps=step + 1,
                    )
                if viewer is not None and step % max(int(self.cfg.viewer_sync_interval), 1) == 0:
                    native_stage(step, "before_overlay")
                    self._draw_grasp_overlay(
                        mujoco, viewer, model, data, runtime, ids, sm.plan or plan
                    )
                    native_stage(step, "after_overlay")
                    native_stage(step, "before_viewer_sync")
                    viewer.sync()
                    native_stage(step, "after_viewer_sync")
                    target_wall_dt = float(self.cfg.ctrl_dt) / max(float(self.cfg.speed), 1.0e-6)
                    remaining = target_wall_dt - (time.perf_counter() - step_started)
                    if remaining > 0.0:
                        time.sleep(remaining)
        finally:
            if self._log_stream is not None:
                self._log_stream.flush()
                self._log_stream.close()
                self._log_stream = None
            if native_log_stream is not None:
                native_log_stream.flush()
                native_log_stream.close()
            if camera_rig is not None:
                camera_rig.close()
            if viewer is not None and float(self.cfg.viewer_hold_s) > 0.0:
                hold_until = time.time() + float(self.cfg.viewer_hold_s)
                while viewer.is_running() and time.time() < hold_until:
                    viewer.sync()
                    time.sleep(0.05)
            if viewer is not None:
                viewer.close()

        reason = last_intent.reason if last_intent is not None else "max_steps"
        return MujocoRunResult(
            success=False,
            reason=f"timeout:{reason}",
            lift_height=float(best_lift),
            final_phase=sm.phase.value,
            steps=int(total_step_budget),
        )

    def _target_motion_state(
        self,
        elapsed: float,
        anchor: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, str]:
        """Periodic Y motion with smooth travel and a dwell at each endpoint."""
        base = np.asarray(anchor, dtype=np.float64).reshape(3)
        delay = max(float(self.cfg.target_motion_delay), 0.0)
        if elapsed < delay:
            return base.copy(), np.zeros(3, dtype=np.float64), "initial_delay"

        amplitude = max(float(self.cfg.target_motion_amplitude), 0.0)
        travel = max(float(self.cfg.target_motion_travel_time), self.cfg.ctrl_dt)
        dwell = max(float(self.cfg.target_motion_dwell_time), 0.0)
        half_travel = 0.5 * travel
        cycle = 2.0 * (travel + dwell)
        tau = (float(elapsed) - delay) % max(cycle, self.cfg.ctrl_dt)

        if tau < half_travel:
            u = tau / half_travel
            y_offset = 0.5 * amplitude * (1.0 - np.cos(np.pi * u))
            y_speed = 0.5 * amplitude * np.pi / half_travel * np.sin(np.pi * u)
            phase = "move_positive_y"
        elif tau < half_travel + dwell:
            y_offset = amplitude
            y_speed = 0.0
            phase = "dwell_positive_y"
        elif tau < half_travel + dwell + travel:
            u = (tau - half_travel - dwell) / travel
            y_offset = amplitude * np.cos(np.pi * u)
            y_speed = -amplitude * np.pi / travel * np.sin(np.pi * u)
            phase = "move_negative_y"
        elif tau < half_travel + 2.0 * dwell + travel:
            y_offset = -amplitude
            y_speed = 0.0
            phase = "dwell_negative_y"
        else:
            u = (
                tau - half_travel - 2.0 * dwell - travel
            ) / half_travel
            y_offset = -0.5 * amplitude * (1.0 + np.cos(np.pi * u))
            y_speed = 0.5 * amplitude * np.pi / half_travel * np.sin(np.pi * u)
            phase = "return_center"

        pos = base.copy()
        velocity = np.zeros(3, dtype=np.float64)
        pos[1] += y_offset
        velocity[1] = y_speed
        return pos, velocity, phase

    def _obstacle_motion_state(
        self,
        sim_time: float,
        base_pos: np.ndarray,
        amplitude: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        kind = str(self.cfg.obstacle_motion).strip().lower()
        period = max(float(self.cfg.obstacle_motion_period), 1.0e-6)
        omega = 2.0 * np.pi / period
        theta = omega * float(sim_time)
        amp = np.asarray(amplitude, dtype=np.float64).reshape(3)
        base = np.asarray(base_pos, dtype=np.float64).reshape(3)
        if kind == "line":
            pos = base + amp * np.sin(theta)
            velocity = amp * omega * np.cos(theta) * float(self.cfg.ctrl_dt)
        elif kind == "circle":
            pos = base + np.array(
                [amp[0] * np.cos(theta), amp[1] * np.sin(theta), amp[2] * np.sin(theta)],
                dtype=np.float64,
            )
            velocity = np.array(
                [
                    -amp[0] * omega * np.sin(theta),
                    amp[1] * omega * np.cos(theta),
                    amp[2] * omega * np.cos(theta),
                ],
                dtype=np.float64,
            ) * float(self.cfg.ctrl_dt)
        else:
            return base.copy(), np.zeros(3, dtype=np.float64)
        return pos, velocity

    def _return_home(
        self,
        *,
        mujoco,
        model,
        data,
        runtime,
        constants,
        cbf_mod,
        stepper,
        ids,
        target_pos,
        target_quat,
        obstacle_provider,
        camera_rig,
        camera_frame_cb,
        sim_state_cb,
    ) -> tuple[bool, float]:
        max_steps = max(
            int(np.ceil(float(self.cfg.return_home_timeout) / self.cfg.ctrl_dt)), 1
        )
        stable_required = max(
            int(np.ceil(float(self.cfg.return_home_stable_time) / self.cfg.ctrl_dt)), 1
        )
        stable = 0
        error = float("inf")
        obstacle_seq = -1
        dynamic = (
            bool(self.cfg.enable_cbf)
            and str(self.cfg.obstacle_mode).strip().lower() == "dynamic"
        )
        obstacle_base_pos = self._parse_vec3(self.cfg.obstacle_pos)
        obstacle_amp = self._parse_vec3(self.cfg.obstacle_motion_amp)

        for step in range(max_steps):
            obstacle_velocity = np.zeros(3, dtype=np.float64)
            if (
                bool(self.cfg.enable_obstacle)
                and str(self.cfg.obstacle_motion).strip().lower() != "none"
            ):
                obstacle_pos, obstacle_velocity = self._obstacle_motion_state(
                    float(data.time), obstacle_base_pos, obstacle_amp
                )
                self._set_target_body(
                    mujoco,
                    model,
                    data,
                    str(self.cfg.obstacle_body),
                    obstacle_pos,
                    reset_velocity=False,
                )
            if (
                dynamic
                and camera_rig is not None
                and camera_frame_cb is not None
                and step % max(int(self.cfg.camera_publish_interval_steps), 1) == 0
            ):
                self._publish_camera_frame(
                    camera_rig,
                    data,
                    model,
                    constants,
                    camera_frame_cb,
                    include_scene=True,
                    include_scene_rgb=False,
                    include_wrist=False,
                )
            if bool(self.cfg.enable_cbf) and obstacle_provider is not None:
                payload = obstacle_provider()
                seq = int(payload.get("seq", 0)) if isinstance(payload, dict) else step
                if seq != obstacle_seq:
                    points = np.asarray(
                        payload.get("points", np.zeros((0, 3)))
                        if isinstance(payload, dict)
                        else payload,
                        dtype=np.float64,
                    ).reshape(-1, 3)
                    obstacle_seq = seq
                    stepper.cbf_obstacles = (
                        [
                            cbf_mod.PointCloudSdfObstacle(
                                name="ros2_return_home_obstacle_cloud",
                                points=points,
                                voxel_size=float(self.cfg.sdf_voxel_size),
                                inflate=float(self.cfg.sdf_inflate),
                                velocity=obstacle_velocity,
                            )
                        ]
                        if points.shape[0] > 0
                        else []
                    )

            tcp_pos, _ = runtime.tcp_pose_w(data, ids)
            error = float(
                np.linalg.norm(
                    np.asarray(tcp_pos, dtype=np.float64)
                    - np.asarray(target_pos, dtype=np.float64)
                )
            )
            stable = stable + 1 if error <= float(self.cfg.return_home_tolerance) else 0
            if stable >= stable_required:
                return True, error

            q_target, _ = stepper.compute_targets(
                model, data, target_pos, target_quat
            )
            q_target[-1] = float(self.cfg.open_q)
            runtime.set_ctrl(data, ids, q_target)
            for _ in range(int(constants.DECIMATION)):
                mujoco.mj_step(model, data)
            if sim_state_cb is not None:
                sim_state_cb(
                    float(data.time),
                    np.asarray(data.qpos, dtype=np.float64).copy(),
                )
        return False, error

    def _load_mujoco_modules(self) -> dict:
        old_path = list(sys.path)
        sys.path = [p for p in sys.path if Path(p or ".").resolve() != self.repo]
        import mujoco  # type: ignore

        sys.path = old_path
        mujoco_dir = str(self.repo / "mujoco")

        def load_local(name: str):
            module_name = f"_soarm100_mujoco_{name}"
            cached = sys.modules.get(module_name)
            if cached is not None:
                return cached
            spec = importlib.util.spec_from_file_location(
                module_name, str(Path(mujoco_dir) / f"{name}.py")
            )
            if spec is None or spec.loader is None:
                raise ImportError(f"cannot load MuJoCo module: {name}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            # Local modules retain fallback imports such as ``from constants``.
            sys.modules.setdefault(name, module)
            spec.loader.exec_module(module)
            return module

        constants = load_local("constants")
        policy = load_local("policy")
        runtime = load_local("runtime")
        cbf = load_local("cbf")
        camera = load_local("camera")

        return {
            "mujoco": mujoco,
            "constants": constants,
            "policy": policy,
            "runtime": runtime,
            "cbf": cbf,
            "camera": camera,
        }

    def _publish_camera_frame(
        self,
        rig,
        data,
        model,
        constants,
        callback,
        *,
        include_scene: bool = False,
        include_scene_rgb: bool = False,
        include_wrist: bool = True,
        tracking_reference_world=None,
    ) -> None:
        if callback is None:
            return
        scene_name = str(constants.SCENE_DEPTH_CAM)
        wrist_name = str(constants.WRIST_RGB_CAM)
        scene_id = model.camera(scene_name).id
        wrist_id = model.camera(wrist_name).id
        frame = {}
        if include_scene:
            if include_scene_rgb:
                frame["scene_rgb"] = rig.capture_rgb(data, scene_name)
            frame["scene_depth"] = rig.capture_depth_m(data, scene_name)
            scene_seg = rig.capture_segmentation(data, scene_name)
            robot_geom_ids = self._robot_geom_ids_for_model(model, constants)
            frame["scene_robot_mask"] = self._robot_mask_from_segmentation(
                scene_seg, robot_geom_ids
            )
            frame["scene_sim_time"] = float(data.time)
            frame["scene_fovy"] = float(model.cam_fovy[scene_id])
        if include_wrist:
            frame["wrist_rgb"] = rig.capture_rgb(data, wrist_name)
            frame["wrist_fovy"] = float(model.cam_fovy[wrist_id])
            frame["wrist_camera_pos_world"] = np.asarray(
                data.cam_xpos[wrist_id], dtype=np.float64
            ).copy()
            frame["wrist_camera_rot_world"] = np.asarray(
                data.cam_xmat[wrist_id], dtype=np.float64
            ).reshape(3, 3).copy()
            if tracking_reference_world is not None:
                frame["tracking_reference_world"] = np.asarray(
                    tracking_reference_world, dtype=np.float64
                ).reshape(3).copy()
        if frame:
            callback(frame)

    @staticmethod
    def _robot_geom_ids_for_model(model, constants) -> set[int]:
        import mujoco

        root_name = str(getattr(constants, "ROBOT_ROOT_BODY", "base"))
        root = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, root_name)
        if root < 0:
            root = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "base")
        if root < 0:
            return set()
        bodies = {int(root)}
        changed = True
        while changed:
            changed = False
            for body_id in range(int(model.nbody)):
                if body_id not in bodies and int(model.body_parentid[body_id]) in bodies:
                    bodies.add(body_id)
                    changed = True
        return {
            int(geom_id)
            for geom_id in range(int(model.ngeom))
            if int(model.geom_bodyid[geom_id]) in bodies
        }

    @staticmethod
    def _robot_mask_from_segmentation(
        segmentation: np.ndarray, robot_geom_ids: set[int]
    ) -> np.ndarray:
        seg = np.asarray(segmentation)
        if seg.ndim != 3 or seg.shape[2] < 1 or not robot_geom_ids:
            return np.zeros(seg.shape[:2], dtype=np.uint8)
        geom_ids = seg[:, :, 0].astype(np.int32)
        return (
            np.isin(geom_ids, np.fromiter(robot_geom_ids, dtype=np.int32)) * 255
        ).astype(np.uint8)

    @staticmethod
    def _rgb_tracking_observation(
        tracked, model, data, constants, tracking_reference_world
    ):
        if not isinstance(tracked, dict):
            return TrackingObservation(
                valid=False, source="ros2_wrist_rgb", reason="invalid_tracking_payload"
            )
        if not bool(tracked.get("valid", False)):
            return TrackingObservation(
                valid=False,
                source="ros2_wrist_rgb",
                reason=str(tracked.get("reason", "track_invalid")),
                confidence=float(tracked.get("confidence", 0.0)),
                replan_required=bool(tracked.get("replan_required", False)),
            )
        wrist_id = model.camera(str(constants.WRIST_RGB_CAM)).id
        cam_pos = np.asarray(data.cam_xpos[wrist_id], dtype=np.float64)
        cam_rot = np.asarray(data.cam_xmat[wrist_id], dtype=np.float64).reshape(3, 3)
        reference = np.asarray(tracking_reference_world, dtype=np.float64).reshape(3)
        p_mj = cam_rot.T @ (reference - cam_pos)
        p_opt = np.array([p_mj[0], -p_mj[1], -p_mj[2]], dtype=np.float64)
        if p_opt[2] <= 1.0e-4:
            return TrackingObservation(
                valid=False,
                source="ros2_wrist_rgb",
                reason="reference_behind_wrist_camera",
            )
        width = float(tracked.get("image_width", 640.0))
        height = float(tracked.get("image_height", 480.0))
        fy = height / (2.0 * np.tan(np.deg2rad(float(model.cam_fovy[wrist_id])) / 2.0))
        fx = fy
        du = float(tracked.get("delta_u", 0.0))
        dv = float(tracked.get("delta_v", 0.0))
        delta_opt = np.array(
            [du * p_opt[2] / fx, dv * p_opt[2] / fy, 0.0], dtype=np.float64
        )
        delta_mj = np.array(
            [delta_opt[0], -delta_opt[1], -delta_opt[2]], dtype=np.float64
        )
        return TrackingObservation(
            valid=True,
            delta_world=cam_rot @ delta_mj,
            source="ros2_wrist_rgb",
            reason=(
                f"{tracked.get('reason', 'track_ok')} "
                f"du={du:+.1f}px dv={dv:+.1f}px depth={p_opt[2]:.3f}m"
            ),
            confidence=float(tracked.get("confidence", 0.0)),
            n_points=1,
            replan_required=bool(tracked.get("replan_required", False)),
        )

    @staticmethod
    def _grasp_target_objects() -> dict[str, tuple[str, str]]:
        return {
            "cube": ("target_object", "target_object_geom"),
            "bottle": ("target_bottle", "target_bottle_geom"),
            "sphere": ("target_sphere", "target_sphere_geom"),
        }

    @staticmethod
    def _parse_vec3(raw) -> np.ndarray:
        vals = [float(x) for x in str(raw).replace(",", " ").split()]
        if len(vals) != 3:
            raise ValueError(f"expected x,y,z, got {raw!r}")
        return np.asarray(vals, dtype=np.float64)

    def _configure_grasp_targets(self, mujoco, model, data) -> None:
        objects = self._grasp_target_objects()
        obj = str(self.cfg.target_object).strip().lower()
        if obj in objects:
            self.cfg.target_body = objects[obj][0]
            selected_geom = objects[obj][1]
        else:
            selected_geom = ""
        for body_name, geom_name in objects.values():
            gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, str(geom_name))
            is_selected = body_name == str(self.cfg.target_body) or geom_name == selected_geom
            if gid >= 0:
                model.geom_contype[int(gid)] = 1 if is_selected else 0
                model.geom_conaffinity[int(gid)] = 1 if is_selected else 0
                if is_selected:
                    model.geom_rgba[int(gid)] = np.array([1.0, 0.05, 0.05, 1.0], dtype=np.float32)
                else:
                    model.geom_rgba[int(gid)] = np.array([1.0, 0.05, 0.05, 0.0], dtype=np.float32)
                    self._set_target_body(mujoco, model, data, body_name, np.array([0.0, 0.0, -1.0], dtype=np.float64))

    def _configure_obstacle(self, mujoco, model, data) -> None:
        body_name = str(self.cfg.obstacle_body).strip()
        if not body_name:
            return
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name)
        if bid < 0:
            if bool(self.cfg.enable_obstacle):
                raise RuntimeError(f"enabled obstacle body not found in mjcf: {body_name}")
            return
        if bool(self.cfg.enable_obstacle):
            self._set_target_body(mujoco, model, data, body_name, self._parse_vec3(self.cfg.obstacle_pos))
        else:
            # If an obstacle scene is loaded with avoidance off, keep the body out
            # of camera/control range so no stray contacts affect the baseline.
            self._set_target_body(mujoco, model, data, body_name, np.array([0.0, 0.0, -1.0], dtype=np.float64))

    def _set_target_body(
        self,
        mujoco,
        model,
        data,
        body_name: str,
        pos: np.ndarray,
        *,
        reset_velocity: bool = True,
    ) -> None:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(body_name))
        if bid < 0:
            return
        target = np.asarray(pos, dtype=np.float64).reshape(3)
        free_jid = -1
        for jid in range(int(model.njnt)):
            if int(model.jnt_bodyid[jid]) == int(bid) and int(model.jnt_type[jid]) == int(mujoco.mjtJoint.mjJNT_FREE):
                free_jid = int(jid)
                break
        if free_jid >= 0:
            qadr = int(model.jnt_qposadr[free_jid])
            dadr = int(model.jnt_dofadr[free_jid])
            data.qpos[qadr : qadr + 3] = target
            data.qpos[qadr + 3 : qadr + 7] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
            if reset_velocity:
                data.qvel[dadr : dadr + 6] = 0.0
        else:
            model.body_pos[int(bid)] = target
        if reset_velocity:
            data.qvel[:] = 0.0
        mujoco.mj_forward(model, data)

    def _settle_object(self, mujoco, model, data) -> None:
        steps = max(0, int(round(float(self.cfg.object_settle_s) / float(model.opt.timestep))))
        for _ in range(steps):
            mujoco.mj_step(model, data)
        data.qvel[:] = 0.0
        mujoco.mj_forward(model, data)

    def _target_z(self, mujoco, model, data) -> float:
        return float(self._target_pos(mujoco, model, data)[2])

    def _target_pos(self, mujoco, model, data) -> np.ndarray:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(self.cfg.target_body))
        if bid < 0:
            return self._parse_vec3(self.cfg.target_pos)
        return np.asarray(data.xpos[int(bid)], dtype=np.float64).copy()

    @staticmethod
    def _scene_add_sphere(mujoco, scene, pos, radius, rgba) -> None:
        if scene.ngeom >= len(scene.geoms):
            return
        mujoco.mjv_initGeom(
            scene.geoms[scene.ngeom],
            mujoco.mjtGeom.mjGEOM_SPHERE,
            np.array([float(radius), 0.0, 0.0], dtype=np.float64),
            np.asarray(pos, dtype=np.float64).reshape(3),
            np.eye(3, dtype=np.float64).reshape(9),
            np.asarray(rgba, dtype=np.float32),
        )
        scene.ngeom += 1

    @staticmethod
    def _scene_add_connector(mujoco, scene, geom_type, start, end, width, rgba) -> None:
        if scene.ngeom >= len(scene.geoms):
            return
        geom = scene.geoms[scene.ngeom]
        mujoco.mjv_connector(
            geom,
            geom_type,
            float(width),
            np.asarray(start, dtype=np.float64).reshape(3),
            np.asarray(end, dtype=np.float64).reshape(3),
        )
        geom.rgba[:] = np.asarray(rgba, dtype=np.float32)
        scene.ngeom += 1

    @staticmethod
    def _rot_from_quat_wxyz(quat) -> np.ndarray:
        w, x, y, z = np.asarray(quat, dtype=np.float64).reshape(4)
        norm = max(float(np.linalg.norm([w, x, y, z])), 1.0e-12)
        w, x, y, z = w / norm, x / norm, y / norm, z / norm
        return np.array(
            [
                [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
            ],
            dtype=np.float64,
        )

    def _draw_grasp_overlay(self, mujoco, viewer, model, data, runtime, ids, plan) -> None:
        try:
            tcp_pos, _ = runtime.tcp_pose_w(data, ids)
            target_bid = mujoco.mj_name2id(
                model, mujoco.mjtObj.mjOBJ_BODY, str(self.cfg.target_body)
            )
            target_pos = (
                np.asarray(data.xpos[int(target_bid)], dtype=np.float64)
                if target_bid >= 0
                else np.asarray(self._parse_vec3(self.cfg.target_pos), dtype=np.float64)
            )
            grasp = np.asarray(plan.grasp_pos, dtype=np.float64).reshape(3)
            pregrasp = np.asarray(plan.pregrasp_pos, dtype=np.float64).reshape(3)
            rotation = self._rot_from_quat_wxyz(plan.grasp_quat_wxyz)
            with viewer.lock():
                scene = viewer.user_scn
                scene.ngeom = 0
                self._scene_add_sphere(
                    mujoco, scene, pregrasp, 0.007, [0.0, 0.75, 1.0, 0.95]
                )
                self._scene_add_sphere(
                    mujoco, scene, grasp, 0.008, [0.0, 1.0, 0.1, 1.0]
                )
                self._scene_add_sphere(
                    mujoco, scene, tcp_pos, 0.006, [1.0, 0.0, 1.0, 0.95]
                )
                self._scene_add_connector(
                    mujoco,
                    scene,
                    mujoco.mjtGeom.mjGEOM_CAPSULE,
                    grasp,
                    target_pos,
                    0.0015,
                    [1.0, 1.0, 1.0, 0.75],
                )
                axis_colors = (
                    [1.0, 0.1, 0.1, 0.95],
                    [0.1, 1.0, 0.1, 0.95],
                    [0.1, 0.35, 1.0, 0.95],
                )
                for axis, color in zip(rotation.T, axis_colors):
                    self._scene_add_connector(
                        mujoco,
                        scene,
                        mujoco.mjtGeom.mjGEOM_ARROW,
                        grasp,
                        grasp + 0.05 * axis,
                        0.003,
                        color,
                    )
        except Exception:
            # Overlay diagnostics must never interrupt the control loop.
            return

    def _log_path(self) -> Path | None:
        raw = str(self.cfg.traj_log).strip()
        if not raw:
            return None
        path = Path(raw)
        if not path.is_absolute():
            path = self.repo / path
        return path

    @staticmethod
    def _arr(x) -> list[float]:
        return [float(v) for v in np.asarray(x, dtype=np.float64).reshape(-1).tolist()]

    def _append_step_log(
        self,
        path: Path | None,
        *,
        step: int,
        phase: str,
        reason: str,
        q_before: np.ndarray,
        q_target: np.ndarray,
        tcp_pos: np.ndarray,
        control_target: np.ndarray,
        pregrasp: np.ndarray,
        grasp: np.ndarray,
        target_object_pos: np.ndarray,
        dist_to_control: float,
        final_err: float,
        target_lift: float,
        best_lift: float,
        gripper_mode: str,
        tracking_obs: TrackingObservation | None,
        tracking_frozen: bool,
        close_gate: dict,
        target_commanded_pos: np.ndarray,
        target_velocity: np.ndarray,
        target_motion_phase: str,
        obstacle_points: np.ndarray,
        obstacle_pos: np.ndarray,
        obstacle_velocity: np.ndarray,
        info: dict,
        enable_cbf: bool,
    ) -> None:
        if path is None:
            return
        obs_pts = np.asarray(obstacle_points, dtype=np.float64).reshape(-1, 3)
        grasp_target_offset = np.asarray(grasp, dtype=np.float64).reshape(3) - np.asarray(
            target_object_pos, dtype=np.float64
        ).reshape(3)
        rec = {
            "time_wall": time.time(),
            "step": int(step),
            "t": float(step) * float(self.cfg.ctrl_dt),
            "phase": str(phase),
            "reason": str(reason),
            "q_before": self._arr(q_before),
            "q_target": self._arr(q_target),
            "tcp_pos": self._arr(tcp_pos),
            "control_target": self._arr(control_target),
            "pregrasp": self._arr(pregrasp),
            "grasp": self._arr(grasp),
            "target_object_pos": self._arr(target_object_pos),
            "grasp_target_offset": self._arr(grasp_target_offset),
            "grasp_target_dist": float(np.linalg.norm(grasp_target_offset)),
            "dist_to_control": float(dist_to_control),
            "final_err": float(final_err),
            "target_lift": float(target_lift),
            "best_lift": float(best_lift),
            "gripper_mode": str(gripper_mode),
            "tracking_valid": bool(tracking_obs.valid) if tracking_obs is not None else False,
            "tracking_delta": self._arr(tracking_obs.delta_world) if tracking_obs is not None else [0.0, 0.0, 0.0],
            "tracking_source": str(tracking_obs.source) if tracking_obs is not None else "",
            "tracking_confidence": float(tracking_obs.confidence) if tracking_obs is not None else 0.0,
            "tracking_reason": str(tracking_obs.reason) if tracking_obs is not None else "",
            "tracking_frozen": bool(tracking_frozen),
            "target_motion_phase": str(target_motion_phase),
            "target_commanded_pos": self._arr(target_commanded_pos),
            "target_velocity": self._arr(target_velocity),
            "target_speed": float(
                np.linalg.norm(np.asarray(target_velocity, dtype=np.float64))
            ),
            "close_gate": dict(close_gate),
            "obstacle_points": int(obs_pts.shape[0]),
            "obstacle_pos": self._arr(obstacle_pos),
            "obstacle_step_velocity": self._arr(obstacle_velocity),
            "cbf_enabled": bool(enable_cbf),
            "cbf_active": bool(info.get("cbf_active", False)),
            "h_min": float(info.get("h_min", float("inf"))),
            "dq_nom_norm": float(info.get("dq_nom_norm", 0.0)),
            "dq_cbf_norm": float(info.get("dq_cbf_norm", 0.0)),
            "dq_total_norm": float(info.get("dq_total_norm", 0.0)),
        }
        line = json.dumps(rec, ensure_ascii=False) + "\n"
        if self._log_stream is not None:
            self._log_stream.write(line)
            if int(step) % 25 == 0:
                self._log_stream.flush()
        else:
            with path.open("a", encoding="utf-8") as f:
                f.write(line)

    def _append_event_log(self, path: Path | None, *, step: int, event: str, attempt: int, reason: str, **values) -> None:
        if path is None:
            return
        rec = {
            "time_wall": time.time(),
            "step": int(step),
            "t": float(step) * float(self.cfg.ctrl_dt),
            "event": str(event),
            "phase": GraspPhase.REPLAN_GRASP.value,
            "attempt": int(attempt),
            "reason": str(reason),
        }
        for key, value in values.items():
            if isinstance(value, np.ndarray):
                rec[key] = self._arr(value)
            else:
                rec[key] = float(value) if isinstance(value, (np.floating, float)) else value
        line = json.dumps(rec, ensure_ascii=False) + "\n"
        if self._log_stream is not None:
            self._log_stream.write(line)
            self._log_stream.flush()
        else:
            with path.open("a", encoding="utf-8") as f:
                f.write(line)
