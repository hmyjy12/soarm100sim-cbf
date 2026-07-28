from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class GraspPhase(str, Enum):
    MOVE_TO_PREGRASP = "MOVE_TO_PREGRASP"
    FINAL_APPROACH = "FINAL_APPROACH"
    COMMIT_GRASP = "COMMIT_GRASP"
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
    final_grasp_dist: float = 0.035
    final_stable_time: float = 0.20
    # FINAL_APPROACH 最长等待时间（秒）；与 final_stable_time 解耦，不再用倍率相乘。
    final_approach_timeout: float = 10.0
    final_total_timeout: float = 20.0
    final_timeout_close_dist: float = 0.040
    close_tracking_confidence: float = 0.45
    close_target_speed: float = 0.005
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
    replan_required: bool = False


@dataclass
class GraspObservation:
    tcp_pos: np.ndarray
    dist_to_control: float
    approach_error_deg: float = 0.0
    final_err: float = 0.0
    target_lift: float = 0.0
    target_gripper_contacts: int = 0
    target_speed: float = 0.0
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
        self.tracking_frozen = False
        self.close_gate: dict[str, float | bool | str | int] = {}
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
        self.tracking_frozen = False
        self.close_gate = {}
        self.last_reason = "reset"

    def accept_replan(self, plan: GraspPlan) -> None:
        next_attempt = self.replan_attempts + 1
        self.reset(plan)
        self.replan_attempts = next_attempt
        self.last_reason = f"replan_accept attempt={self.replan_attempts}"

    def reject_replan(self, reason: str) -> None:
        self.replan_attempts += 1
        self.replan_wait_counter = 0
        self.last_reason = f"replan_reject attempt={self.replan_attempts} reason={reason}"

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
            timeout_steps = max(stable_steps, self._steps(th.final_approach_timeout, min_steps=1))
            total_timeout_steps = max(
                timeout_steps,
                self._steps(th.final_total_timeout, min_steps=1),
            )
            tracking_ok = (
                obs.tracking is None
                or (
                    obs.tracking.valid
                    and obs.tracking.confidence >= th.close_tracking_confidence
                )
            )
            target_stable = obs.target_speed <= th.close_target_speed
            position_ok = obs.final_err <= th.final_grasp_dist
            if position_ok and tracking_ok and target_stable:
                self.success_counter += 1
            else:
                self.success_counter = 0
            reached = self.success_counter >= stable_steps
            timed_out = self.final_counter >= timeout_steps
            timeout_close = (
                timed_out
                and tracking_ok
                and target_stable
                and obs.final_err <= th.final_timeout_close_dist
            )
            self.close_gate = {
                "position_ok": bool(position_ok),
                "tracking_ok": bool(tracking_ok),
                "target_stable": bool(target_stable),
                "final_err_m": float(obs.final_err),
                "target_speed_mps": float(obs.target_speed),
                "tracking_confidence": (
                    float(obs.tracking.confidence) if obs.tracking is not None else 1.0
                ),
                "stable_counter": int(self.success_counter),
                "stable_required": int(stable_steps),
                "timed_out": bool(timed_out),
            }
            if reached or timeout_close:
                self.phase = GraspPhase.COMMIT_GRASP
                self.tracking_frozen = True
                self.last_reason = (
                    "close_gate_stable" if reached else "close_gate_timeout_near"
                )
                self.success_counter = 0
                self.close_counter = 0
            elif self.final_counter >= total_timeout_steps:
                self.phase = GraspPhase.FAILED
                self.last_reason = "final_total_timeout"
                return self._intent(
                    plan.grasp_pos,
                    plan.grasp_quat_wxyz,
                    "open",
                    done=True,
                    success=False,
                    reason=self.last_reason,
                )
            return self._intent(plan.grasp_pos, plan.grasp_quat_wxyz, "open", reason=self.last_reason)

        if self.phase == GraspPhase.COMMIT_GRASP:
            self.phase = GraspPhase.CLOSE
            self.close_counter = 0
            self.tracking_frozen = True
            self.last_reason = "grasp_pose_committed"
            return self._intent(
                plan.grasp_pos,
                plan.grasp_quat_wxyz,
                "open",
                should_freeze_arm=True,
                reason=self.last_reason,
            )

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
                if self.replan_attempts >= th.replan_max_attempts:
                    self.phase = GraspPhase.FAILED
                    self.last_reason = f"lift_failed_replan_exhausted attempts={self.replan_attempts}"
                    return self._intent(
                        lift_target,
                        plan.grasp_quat_wxyz,
                        "close",
                        done=True,
                        success=False,
                        reason=self.last_reason,
                    )
                self.phase = GraspPhase.REPLAN_GRASP
                self.replan_wait_counter = 0
                self.last_reason = "lift_failed"
                return self._intent(plan.pregrasp_pos, plan.grasp_quat_wxyz, "open", should_plan_grasp=True, reason=self.last_reason)
            return self._intent(lift_target, plan.grasp_quat_wxyz, "close", reason=self.last_reason)

        if self.phase == GraspPhase.REPLAN_GRASP:
            self.replan_wait_counter += 1
            if self.replan_attempts >= th.replan_max_attempts:
                self.phase = GraspPhase.FAILED
                self.last_reason = f"replan_attempts_exhausted attempts={self.replan_attempts}"
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
        if self.tracking_frozen:
            return
        if self.phase == GraspPhase.MOVE_TO_PREGRASP:
            if obs.dist_to_control > self.thresholds.track_activate_dist:
                return
        elif self.phase != GraspPhase.FINAL_APPROACH:
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
