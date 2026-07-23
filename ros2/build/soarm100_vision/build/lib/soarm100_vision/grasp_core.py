from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class GraspPhase(str, Enum):
    MOVE_TO_PREGRASP = "MOVE_TO_PREGRASP"
    FINAL_APPROACH = "FINAL_APPROACH"
    CLOSE = "CLOSE"
    LIFT = "LIFT"
    VERIFY = "VERIFY"
    REPLAN_GRASP = "REPLAN_GRASP"
    FAILED = "FAILED"


@dataclass
class GraspThresholds:
    pregrasp_success_dist: float = 0.035
    pregrasp_approach_success_deg: float = 60.0
    pregrasp_stable_time: float = 0.05
    final_grasp_dist: float = 0.010
    final_stable_time: float = 0.10
    final_timeout_scale: float = 2.0
    close_time: float = 0.80
    lift_time: float = 0.80
    lift_height: float = 0.035
    lift_success_height: float = 0.015
    track_activate_dist: float = 0.080
    track_max_delta: float = 0.020
    track_gain: float = 1.0
    track_close_time: float = 0.40
    replan_delta: float = 0.030
    replan_max_attempts: int = 1
    replan_ready_dist: float = 0.018
    replan_settle_time: float = 0.75


@dataclass
class GraspPlan:
    pregrasp_pos: np.ndarray
    grasp_pos: np.ndarray
    grasp_quat_wxyz: np.ndarray
    approach_axis_world: np.ndarray
    gripper_width: float = 0.0
    score: float = 0.0

    def copy(self) -> "GraspPlan":
        return GraspPlan(
            pregrasp_pos=np.asarray(self.pregrasp_pos, dtype=np.float64).copy(),
            grasp_pos=np.asarray(self.grasp_pos, dtype=np.float64).copy(),
            grasp_quat_wxyz=np.asarray(self.grasp_quat_wxyz, dtype=np.float64).copy(),
            approach_axis_world=np.asarray(self.approach_axis_world, dtype=np.float64).copy(),
            gripper_width=float(self.gripper_width),
            score=float(self.score),
        )


@dataclass
class TrackingObservation:
    valid: bool
    delta_world: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    source: str = ""
    reason: str = ""
    confidence: float = 0.0
    n_points: int = 0


@dataclass
class GraspObservation:
    tcp_pos: np.ndarray
    dist_to_control: float
    approach_error_deg: float = 0.0
    final_err: float = 0.0
    target_lift: float = 0.0
    target_gripper_contacts: int = 0
    tracking: TrackingObservation | None = None


@dataclass
class ControlIntent:
    phase: GraspPhase
    target_pos: np.ndarray
    target_quat_wxyz: np.ndarray
    gripper_mode: str
    gripper_alpha: float = 0.0
    should_freeze_arm: bool = False
    should_plan_grasp: bool = False
    done: bool = False
    success: bool = False
    reason: str = ""


class GraspStateMachine:
    """MuJoCo-free grasp-chain state machine.

    This class decides state transitions and target pose intent only. Robot I/O,
    policy inference, CBF-QP, contact acquisition, and camera acquisition are
    backend responsibilities.
    """

    def __init__(self, thresholds: GraspThresholds, ctrl_dt: float) -> None:
        self.thresholds = thresholds
        self.ctrl_dt = float(ctrl_dt)
        self.phase = GraspPhase.MOVE_TO_PREGRASP
        self.plan: GraspPlan | None = None
        self.plan0: GraspPlan | None = None
        self.success_counter = 0
        self.final_counter = 0
        self.close_counter = 0
        self.lift_counter = 0
        self.replan_attempts = 0
        self.replan_wait_counter = 0
        self.tracking_invalid_counter = 0
        self.tracking_ever_valid = False
        self.last_reason = ""

    def reset(self, plan: GraspPlan) -> None:
        self.phase = GraspPhase.MOVE_TO_PREGRASP
        self.plan = plan.copy()
        self.plan0 = plan.copy()
        self.success_counter = 0
        self.final_counter = 0
        self.close_counter = 0
        self.lift_counter = 0
        self.replan_wait_counter = 0
        self.tracking_invalid_counter = 0
        self.tracking_ever_valid = False
        self.last_reason = "reset"

    def accept_replan(self, plan: GraspPlan) -> None:
        self.replan_attempts += 1
        self.reset(plan)
        self.last_reason = f"replan_accept attempt={self.replan_attempts}"

    def step(self, obs: GraspObservation) -> ControlIntent:
        if self.plan is None or self.plan0 is None:
            self.phase = GraspPhase.FAILED
            return self._intent(np.zeros(3), np.array([1.0, 0.0, 0.0, 0.0]), "hold", done=True, reason="missing_plan")

        self._apply_tracking(obs)
        plan = self.plan
        th = self.thresholds

        if self.phase == GraspPhase.MOVE_TO_PREGRASP:
            stable_steps = self._steps(th.pregrasp_stable_time, min_steps=1)
            if obs.dist_to_control <= th.pregrasp_success_dist and obs.approach_error_deg <= th.pregrasp_approach_success_deg:
                self.success_counter += 1
            else:
                self.success_counter = 0
            if self.success_counter >= stable_steps:
                self.phase = GraspPhase.FINAL_APPROACH
                self.success_counter = 0
                self.final_counter = 0
                self.last_reason = "pregrasp_reached"
            return self._intent(plan.pregrasp_pos, plan.grasp_quat_wxyz, "open", reason=self.last_reason)

        if self.phase == GraspPhase.FINAL_APPROACH:
            self.final_counter += 1
            stable_steps = self._steps(th.final_stable_time, min_steps=1)
            timeout_steps = max(stable_steps, int(np.ceil(stable_steps * max(th.final_timeout_scale, 1.0))))
            if obs.final_err <= th.final_grasp_dist:
                self.success_counter += 1
            else:
                self.success_counter = 0
            if self._should_replan(obs):
                self.phase = GraspPhase.REPLAN_GRASP
                self.replan_wait_counter = 0
                self.last_reason = "tracking_replan"
                return self._intent(plan.pregrasp_pos, plan.grasp_quat_wxyz, "open", should_plan_grasp=True, reason=self.last_reason)
            if self.success_counter >= stable_steps or self.final_counter >= timeout_steps:
                self.phase = GraspPhase.CLOSE
                self.success_counter = 0
                self.close_counter = 0
                self.last_reason = "final_stable" if self.success_counter >= stable_steps else "final_timeout"
            return self._intent(plan.grasp_pos, plan.grasp_quat_wxyz, "open", reason=self.last_reason)

        if self.phase == GraspPhase.CLOSE:
            self.close_counter += 1
            close_steps = self._steps(th.close_time, min_steps=1)
            alpha = min(1.0, self.close_counter / max(close_steps, 1))
            if self.close_counter >= close_steps:
                self.phase = GraspPhase.LIFT
                self.lift_counter = 0
                self.last_reason = "close_complete"
            return self._intent(plan.grasp_pos, plan.grasp_quat_wxyz, "close", gripper_alpha=alpha, should_freeze_arm=True, reason=self.last_reason)

        if self.phase == GraspPhase.LIFT:
            self.lift_counter += 1
            lift_target = plan.grasp_pos + np.array([0.0, 0.0, th.lift_height], dtype=np.float64)
            if obs.target_lift >= th.lift_success_height:
                self.phase = GraspPhase.VERIFY
                self.last_reason = "lift_success"
                return self._intent(lift_target, plan.grasp_quat_wxyz, "close", done=True, success=True, reason=self.last_reason)
            if self.lift_counter >= self._steps(th.lift_time, min_steps=1):
                self.phase = GraspPhase.REPLAN_GRASP
                self.replan_wait_counter = 0
                self.last_reason = "lift_failed"
                return self._intent(plan.pregrasp_pos, plan.grasp_quat_wxyz, "open", should_plan_grasp=True, reason=self.last_reason)
            return self._intent(lift_target, plan.grasp_quat_wxyz, "close", reason=self.last_reason)

        if self.phase == GraspPhase.REPLAN_GRASP:
            self.replan_wait_counter += 1
            if self.replan_attempts >= th.replan_max_attempts:
                self.phase = GraspPhase.FAILED
                self.last_reason = "replan_attempts_exhausted"
                return self._intent(plan.grasp_pos, plan.grasp_quat_wxyz, "close", done=True, success=False, reason=self.last_reason)
            ready = obs.dist_to_control <= th.replan_ready_dist
            settled = self.replan_wait_counter >= self._steps(th.replan_settle_time, min_steps=1)
            return self._intent(
                plan.pregrasp_pos,
                plan.grasp_quat_wxyz,
                "open",
                should_plan_grasp=bool(ready or settled),
                reason="replan_wait",
            )

        done = self.phase in (GraspPhase.VERIFY, GraspPhase.FAILED)
        return self._intent(plan.grasp_pos, plan.grasp_quat_wxyz, "close", done=done, success=self.phase == GraspPhase.VERIFY, reason=self.last_reason)

    def _apply_tracking(self, obs: GraspObservation) -> None:
        if self.plan is None or self.plan0 is None or obs.tracking is None:
            return
        if self.phase not in (GraspPhase.FINAL_APPROACH, GraspPhase.CLOSE):
            return
        track = obs.tracking
        if track.valid:
            self.tracking_invalid_counter = 0
            self.tracking_ever_valid = True
        else:
            if self.tracking_ever_valid:
                self.tracking_invalid_counter += 1
            return
        delta = np.asarray(track.delta_world, dtype=np.float64).reshape(3)
        if float(np.linalg.norm(delta)) <= self.thresholds.track_max_delta:
            gain = float(self.thresholds.track_gain)
            self.plan.pregrasp_pos = self.plan0.pregrasp_pos + gain * delta
            self.plan.grasp_pos = self.plan0.grasp_pos + gain * delta
            self.last_reason = f"track_update source={track.source}"

    def _should_replan(self, obs: GraspObservation) -> bool:
        if obs.tracking is None or self.replan_attempts >= self.thresholds.replan_max_attempts:
            return False
        if self.phase != GraspPhase.FINAL_APPROACH:
            return False
        if obs.tracking.valid:
            delta_norm = float(np.linalg.norm(obs.tracking.delta_world))
            return delta_norm >= self.thresholds.replan_delta
        return self.tracking_ever_valid and self.tracking_invalid_counter >= 3

    def _steps(self, duration: float, *, min_steps: int) -> int:
        return max(int(np.ceil(max(float(duration), 0.0) / max(self.ctrl_dt, 1e-6))), int(min_steps))

    def _intent(
        self,
        pos: np.ndarray,
        quat: np.ndarray,
        gripper_mode: str,
        *,
        gripper_alpha: float = 0.0,
        should_freeze_arm: bool = False,
        should_plan_grasp: bool = False,
        done: bool = False,
        success: bool = False,
        reason: str = "",
    ) -> ControlIntent:
        return ControlIntent(
            phase=self.phase,
            target_pos=np.asarray(pos, dtype=np.float64).reshape(3).copy(),
            target_quat_wxyz=np.asarray(quat, dtype=np.float64).reshape(4).copy(),
            gripper_mode=str(gripper_mode),
            gripper_alpha=float(gripper_alpha),
            should_freeze_arm=bool(should_freeze_arm),
            should_plan_grasp=bool(should_plan_grasp),
            done=bool(done),
            success=bool(success),
            reason=str(reason),
        )
