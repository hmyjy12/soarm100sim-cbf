from __future__ import annotations

from dataclasses import dataclass
import json
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
    enable_obstacle: bool = False
    obstacle_body: str = "obstacle_rod_mount"
    obstacle_pos: str = "0.16,0.09,0.02"
    enable_cbf: bool = False
    cbf_d_safe: float = 0.020
    cbf_gamma: float = 0.8
    cbf_lambda: float = 0.5
    cbf_activate_margin: float = 0.040
    sdf_voxel_size: float = 0.010
    sdf_inflate: float = 0.015
    replan_max_attempts: int = 0
    max_steps: int = 450
    open_q: float = 1.2
    close_q: float = 0.4
    ctrl_dt: float = 0.02
    speed: float = 1.0
    show_viewer: bool = False
    viewer_sync_interval: int = 1
    viewer_hold_s: float = 8.0
    traj_log: str = "logs/ros2_inprocess_grasp.jsonl"


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

    def run(self, cmd: PlannedGraspCommand, *, feedback_cb=None, tracking_provider=None, obstacle_provider=None) -> MujocoRunResult:
        modules = self._load_mujoco_modules()
        mujoco = modules["mujoco"]
        runtime = modules["runtime"]
        policy_mod = modules["policy"]
        constants = modules["constants"]
        cbf_mod = modules["cbf"]

        mjcf = Path(self.cfg.mjcf)
        if not mjcf.is_absolute():
            mjcf = self.repo / mjcf
        ckpt = Path(self.cfg.checkpoint)
        if not ckpt.is_absolute():
            ckpt = self.repo / ckpt

        model = mujoco.MjModel.from_xml_path(str(mjcf))
        data = mujoco.MjData(model)
        viewer = None
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

        plan = GraspPlan(
            pregrasp_pos=np.asarray(cmd.pregrasp.pos, dtype=np.float64).reshape(3),
            grasp_pos=np.asarray(cmd.grasp.pos, dtype=np.float64).reshape(3),
            grasp_quat_wxyz=np.asarray(cmd.grasp.quat_wxyz, dtype=np.float64).reshape(4),
            approach_axis_world=np.array([1.0, 0.0, 0.0], dtype=np.float64),
            gripper_width=float(cmd.gripper_width),
        )
        thresholds = GraspThresholds(replan_max_attempts=max(int(self.cfg.replan_max_attempts), 0))
        sm = GraspStateMachine(thresholds, ctrl_dt=float(self.cfg.ctrl_dt))
        sm.reset(plan)

        target_initial_z = self._target_z(mujoco, model, data)
        frozen_q = None
        close_start_q = None
        last_intent = None
        best_lift = 0.0
        tracking_ref = None
        log_path = self._log_path()
        if log_path is not None:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text("", encoding="utf-8")

        try:
            for step in range(int(self.cfg.max_steps)):
                if viewer is not None and not viewer.is_running():
                    return MujocoRunResult(
                        success=False,
                        reason="viewer_closed",
                        lift_height=float(best_lift),
                        final_phase=sm.phase.value,
                        steps=step,
                    )
                if bool(self.cfg.enable_cbf) and obstacle_provider is not None and cbf_cfg is not None:
                    obstacle_points = np.asarray(obstacle_provider(), dtype=np.float64).reshape(-1, 3)
                    if obstacle_points.shape[0] > 0:
                        stepper.cbf_obstacles = [
                            cbf_mod.PointCloudSdfObstacle(
                                name="ros2_obstacle_cloud",
                                points=obstacle_points,
                                voxel_size=float(self.cfg.sdf_voxel_size),
                                inflate=float(self.cfg.sdf_inflate),
                            )
                        ]
                    else:
                        stepper.cbf_obstacles = []

                tcp_pos, _tcp_quat = runtime.tcp_pose_w(data, ids)
                current_target = plan.pregrasp_pos if sm.phase == GraspPhase.MOVE_TO_PREGRASP else plan.grasp_pos
                target_lift = self._target_z(mujoco, model, data) - target_initial_z
                best_lift = max(best_lift, float(target_lift))
                tracking_obs = None
                if tracking_provider is not None:
                    tracked = tracking_provider()
                    if tracked is not None:
                        tracked = np.asarray(tracked, dtype=np.float64).reshape(3)
                        if tracking_ref is None:
                            tracking_ref = tracked.copy()
                        tracking_obs = TrackingObservation(
                            valid=True,
                            delta_world=tracked - tracking_ref,
                            source="ros2_wrist",
                            confidence=1.0,
                            n_points=1,
                        )
                obs = GraspObservation(
                    tcp_pos=np.asarray(tcp_pos, dtype=np.float64),
                    dist_to_control=float(np.linalg.norm(np.asarray(tcp_pos) - current_target)),
                    approach_error_deg=0.0,
                    final_err=float(np.linalg.norm(np.asarray(tcp_pos) - plan.grasp_pos)),
                    target_lift=float(target_lift),
                    target_gripper_contacts=0,
                    tracking=tracking_obs,
                )
                intent = sm.step(obs)
                last_intent = intent
                if feedback_cb is not None and step % max(int(round(0.5 / self.cfg.ctrl_dt)), 1) == 0:
                    feedback_cb(intent.phase.value, intent.reason, best_lift)
                if intent.done:
                    return MujocoRunResult(
                        success=bool(intent.success),
                        reason=str(intent.reason),
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
                    dist_to_control=obs.dist_to_control,
                    final_err=obs.final_err,
                    target_lift=target_lift,
                    best_lift=best_lift,
                    gripper_mode=intent.gripper_mode,
                    tracking_obs=tracking_obs,
                    obstacle_points=obstacle_points if "obstacle_points" in locals() else np.zeros((0, 3)),
                    info=step_info,
                    enable_cbf=bool(self.cfg.enable_cbf),
                )
                for _ in range(int(constants.DECIMATION)):
                    mujoco.mj_step(model, data)
                if viewer is not None and step % max(int(self.cfg.viewer_sync_interval), 1) == 0:
                    viewer.sync()
                    time.sleep(float(self.cfg.ctrl_dt) / max(float(self.cfg.speed), 1.0e-6))
        finally:
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
            steps=int(self.cfg.max_steps),
        )

    def _load_mujoco_modules(self) -> dict:
        old_path = list(sys.path)
        sys.path = [p for p in sys.path if Path(p or ".").resolve() != self.repo]
        import mujoco  # type: ignore

        sys.path = old_path
        mujoco_dir = str(self.repo / "mujoco")
        if mujoco_dir not in sys.path:
            sys.path.insert(0, mujoco_dir)
        import constants  # type: ignore
        import policy  # type: ignore
        import runtime  # type: ignore
        import cbf  # type: ignore

        return {"mujoco": mujoco, "constants": constants, "policy": policy, "runtime": runtime, "cbf": cbf}

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

    def _set_target_body(self, mujoco, model, data, body_name: str, pos: np.ndarray) -> None:
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
            data.qvel[dadr : dadr + 6] = 0.0
        else:
            model.body_pos[int(bid)] = target
        data.qvel[:] = 0.0
        mujoco.mj_forward(model, data)

    def _settle_object(self, mujoco, model, data) -> None:
        steps = max(0, int(round(float(self.cfg.object_settle_s) / float(model.opt.timestep))))
        for _ in range(steps):
            mujoco.mj_step(model, data)
        data.qvel[:] = 0.0
        mujoco.mj_forward(model, data)

    def _target_z(self, mujoco, model, data) -> float:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(self.cfg.target_body))
        if bid < 0:
            return 0.0
        return float(data.xpos[int(bid)][2])

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
        dist_to_control: float,
        final_err: float,
        target_lift: float,
        best_lift: float,
        gripper_mode: str,
        tracking_obs: TrackingObservation | None,
        obstacle_points: np.ndarray,
        info: dict,
        enable_cbf: bool,
    ) -> None:
        if path is None:
            return
        obs_pts = np.asarray(obstacle_points, dtype=np.float64).reshape(-1, 3)
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
            "dist_to_control": float(dist_to_control),
            "final_err": float(final_err),
            "target_lift": float(target_lift),
            "best_lift": float(best_lift),
            "gripper_mode": str(gripper_mode),
            "tracking_valid": bool(tracking_obs.valid) if tracking_obs is not None else False,
            "tracking_delta": self._arr(tracking_obs.delta_world) if tracking_obs is not None else [0.0, 0.0, 0.0],
            "tracking_source": str(tracking_obs.source) if tracking_obs is not None else "",
            "obstacle_points": int(obs_pts.shape[0]),
            "cbf_enabled": bool(enable_cbf),
            "cbf_active": bool(info.get("cbf_active", False)),
            "h_min": float(info.get("h_min", float("inf"))),
            "dq_nom_norm": float(info.get("dq_nom_norm", 0.0)),
            "dq_cbf_norm": float(info.get("dq_cbf_norm", 0.0)),
            "dq_total_norm": float(info.get("dq_total_norm", 0.0)),
        }
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
