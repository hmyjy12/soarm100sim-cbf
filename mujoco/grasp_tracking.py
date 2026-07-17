"""Near-field grasp target tracking backends.

The grasp state machine consumes a small world-frame delta from this module.
Backends may use MuJoCo ground truth, wrist camera observations, or a future
real camera pipeline. Invalid estimates are explicit and must not be applied.
"""

from __future__ import annotations

from dataclasses import dataclass

import mujoco
import numpy as np

try:
    from .camera import MujocoCameraRig
    from .constants import WRIST_RGB_CAM
except ImportError:
    from camera import MujocoCameraRig  # type: ignore
    from constants import WRIST_RGB_CAM  # type: ignore


@dataclass
class GraspTrackResult:
    valid: bool
    delta_world: np.ndarray
    confidence: float
    reason: str
    source: str
    n_points: int = 0
    pos_world: np.ndarray | None = None
    pos_err_world: np.ndarray | None = None
    pos_err_norm: float = float("nan")


@dataclass
class TargetObservation:
    valid: bool
    pos_world: np.ndarray
    confidence: float
    reason: str
    source: str
    n_points: int = 0


class GraspTracker:
    def reset(self) -> None:
        return

    def update(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        *,
        target_pos: np.ndarray,
        target_plan_pos: np.ndarray,
    ) -> GraspTrackResult:
        raise NotImplementedError

    def observe_target(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        *,
        fallback_pos: np.ndarray,
    ) -> TargetObservation:
        return TargetObservation(
            valid=False,
            pos_world=np.asarray(fallback_pos, dtype=np.float64).reshape(3),
            confidence=0.0,
            reason="observe_target_not_supported",
            source="none",
            n_points=0,
        )


class GroundTruthGraspTracker(GraspTracker):
    def observe_target(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        *,
        fallback_pos: np.ndarray,
    ) -> TargetObservation:
        return TargetObservation(
            valid=True,
            pos_world=np.asarray(fallback_pos, dtype=np.float64).reshape(3),
            confidence=1.0,
            reason="gt_target_pose",
            source="gt",
            n_points=1,
        )

    def update(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        *,
        target_pos: np.ndarray,
        target_plan_pos: np.ndarray,
    ) -> GraspTrackResult:
        delta = np.asarray(target_pos, dtype=np.float64).reshape(3) - np.asarray(target_plan_pos, dtype=np.float64).reshape(3)
        return GraspTrackResult(
            valid=True,
            delta_world=delta,
            confidence=1.0,
            reason="gt_target_pose",
            source="gt",
            n_points=1,
        )


class WristSegmentationGraspTracker(GraspTracker):
    """MuJoCo-only wrist tracker using target geom segmentation and depth.

    This is a simulation bridge toward the real wrist-camera tracker: it uses
    the same validity semantics but relies on MuJoCo segmentation to isolate
    the target. It estimates target centroid motion in world coordinates.
    """

    def __init__(
        self,
        model: mujoco.MjModel,
        *,
        target_geom_name: str,
        cam_name: str = WRIST_RGB_CAM,
        min_points: int = 24,
        flip_image_y: bool = True,
    ) -> None:
        self._rig = MujocoCameraRig(model)
        self._cam_name = str(cam_name)
        self._target_geom_name = str(target_geom_name)
        self._target_geom_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, self._target_geom_name)
        self._min_points = int(min_points)
        self._flip_image_y = bool(flip_image_y)
        self._ref_centroid: np.ndarray | None = None

    def close(self) -> None:
        self._rig.close()

    def reset(self) -> None:
        self._ref_centroid = None

    def _centroid_world(self, model: mujoco.MjModel, data: mujoco.MjData) -> tuple[np.ndarray | None, int, str]:
        if self._target_geom_id < 0:
            return None, 0, f"missing target geom {self._target_geom_name}"
        seg = self._rig.capture_segmentation(data, self._cam_name)
        depth = self._rig.capture_depth_m(data, self._cam_name)
        # Keep this consistent with AnyGraspBridge's target_geom_seg mask.
        mask = seg[..., 0].astype(np.int32) == int(self._target_geom_id)
        valid = mask & np.isfinite(depth) & (depth > 1e-4)
        vs, us = np.nonzero(valid)
        n = int(us.size)
        if n < self._min_points:
            return None, n, f"target_points_too_few:{n}"
        h, w = depth.shape
        cid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, self._cam_name)
        fovy = np.deg2rad(float(model.cam_fovy[int(cid)]))
        fy = 0.5 * h / max(np.tan(0.5 * fovy), 1e-12)
        fx = fy
        cx = 0.5 * (w - 1)
        cy = 0.5 * (h - 1)
        z = depth[valid]
        x = (us.astype(np.float64) - cx) * z / fx
        y = (vs.astype(np.float64) - cy) * z / fy
        # MuJoCo camera looks down local -Z; renderer depth is positive along view.
        pts_cam_y = -y if self._flip_image_y else y
        pts_cam = np.column_stack([x, pts_cam_y, -z])
        cam_pos = np.asarray(data.cam_xpos[int(cid)], dtype=np.float64).reshape(3)
        cam_R = np.asarray(data.cam_xmat[int(cid)], dtype=np.float64).reshape(3, 3)
        pts_world = cam_pos.reshape(1, 3) + pts_cam @ cam_R.T
        return np.mean(pts_world, axis=0), n, "ok"

    def update(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        *,
        target_pos: np.ndarray,
        target_plan_pos: np.ndarray,
    ) -> GraspTrackResult:
        centroid, n, reason = self._centroid_world(model, data)
        if centroid is None:
            return GraspTrackResult(
                valid=False,
                delta_world=np.zeros(3, dtype=np.float64),
                confidence=0.0,
                reason=reason,
                source="wrist",
                n_points=n,
                pos_world=None,
                pos_err_world=None,
            )
        if self._ref_centroid is None:
            self._ref_centroid = np.asarray(centroid, dtype=np.float64).reshape(3).copy()
        delta = np.asarray(centroid, dtype=np.float64).reshape(3) - self._ref_centroid
        target = np.asarray(target_pos, dtype=np.float64).reshape(3)
        pos_err = np.asarray(centroid, dtype=np.float64).reshape(3) - target
        confidence = min(1.0, float(n) / max(float(self._min_points * 4), 1.0))
        return GraspTrackResult(
            valid=True,
            delta_world=delta,
            confidence=confidence,
            reason=reason,
            source="wrist",
            n_points=n,
            pos_world=np.asarray(centroid, dtype=np.float64).reshape(3),
            pos_err_world=pos_err,
            pos_err_norm=float(np.linalg.norm(pos_err)),
        )

    def observe_target(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        *,
        fallback_pos: np.ndarray,
    ) -> TargetObservation:
        centroid, n, reason = self._centroid_world(model, data)
        if centroid is None:
            return TargetObservation(
                valid=False,
                pos_world=np.asarray(fallback_pos, dtype=np.float64).reshape(3),
                confidence=0.0,
                reason=reason,
                source="wrist",
                n_points=n,
            )
        confidence = min(1.0, float(n) / max(float(self._min_points * 4), 1.0))
        return TargetObservation(
            valid=True,
            pos_world=np.asarray(centroid, dtype=np.float64).reshape(3),
            confidence=confidence,
            reason=reason,
            source="wrist",
            n_points=n,
        )


def make_grasp_tracker(
    source: str,
    model: mujoco.MjModel,
    *,
    target_geom_name: str,
    wrist_flip_image_y: bool = True,
) -> GraspTracker | None:
    s = str(source).strip().lower()
    if s in ("none", "off", "false", "0"):
        return None
    if s in ("gt", "truth", "mujoco"):
        return GroundTruthGraspTracker()
    if s in ("wrist", "wrist_rgb", "wrist_seg"):
        return WristSegmentationGraspTracker(
            model,
            target_geom_name=target_geom_name,
            flip_image_y=bool(wrist_flip_image_y),
        )
    raise ValueError(f"unknown grasp tracking source: {source!r}")
