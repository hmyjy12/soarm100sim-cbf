"""scene_depth 深度图 → 世界系圆柱障碍（视觉避障 v1）。

v1 仅使用固定俯视相机 scene_depth；腕部 wrist_rgb 暂不参与检测
（朝指缝前方，多数姿态看不到侧方杆；后续可在 reach 近场作补盲）。
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

try:
    from .cbf import CylinderObstacle
    from .calib import CameraIntrinsics, camera_to_world
    from .constants import OBSTACLE_ROD_CENTER_POS_M
except ImportError:
    from cbf import CylinderObstacle  # type: ignore
    from calib import CameraIntrinsics, camera_to_world  # type: ignore
    from constants import OBSTACLE_ROD_CENTER_POS_M  # type: ignore


@dataclass
class RodDetectConfig:
    rod_radius: float = 0.012
    rod_half_length: float = 0.15
    min_depth_m: float = 0.12
    max_depth_m: float = 1.1
    roi_x: tuple[float, float] = (0.08, 0.24)
    roi_y: tuple[float, float] = (0.02, 0.18)
    roi_z: tuple[float, float] = (0.08, 0.34)
    # 工作区先验：仿真/真机杆大致位置；无先验时可设 use_prior_xy=False
    use_prior_xy: bool = True
    prior_xy: tuple[float, float] = (
        float(OBSTACLE_ROD_CENTER_POS_M[0]),
        float(OBSTACLE_ROD_CENTER_POS_M[1]),
    )
    prior_xy_radius_m: float = 0.045
    min_points: int = 30
    ema_alpha: float = 0.35
    min_half_length: float = 0.04
    inlier_dist_m: float = 0.018
    name: str = "vision_rod"


@dataclass
class RodDetectDebug:
    n_depth_valid: int = 0
    n_roi: int = 0
    detected: bool = False
    using_tracker: bool = False
    center_err_mm: float | None = None
    axis_angle_deg: float | None = None


def unproject_depth_map(
    intr: CameraIntrinsics,
    T_wc: np.ndarray,
    depth_m: np.ndarray,
    *,
    min_depth_m: float,
    max_depth_m: float,
) -> np.ndarray:
    """有效深度像素 → N×3 世界系点云。"""
    d = np.asarray(depth_m, dtype=np.float64)
    valid = np.isfinite(d) & (d >= min_depth_m) & (d <= max_depth_m)
    if not np.any(valid):
        return np.zeros((0, 3), dtype=np.float64)

    v_idx, u_idx = np.nonzero(valid)
    depths = d[valid]
    u = u_idx.astype(np.float64)
    v = v_idx.astype(np.float64)

    x = (u - intr.cx) / intr.fx
    y = -(v - intr.cy) / intr.fy
    # MuJoCo's depth renderer returns camera z-depth in meters, not Euclidean
    # range along a normalized ray.
    p_cam = np.stack([x * depths, y * depths, -depths], axis=1)
    return camera_to_world(T_wc, p_cam)


def _filter_roi(points: np.ndarray, cfg: RodDetectConfig) -> np.ndarray:
    if points.shape[0] == 0:
        return points
    x0, x1 = cfg.roi_x
    y0, y1 = cfg.roi_y
    z0, z1 = cfg.roi_z
    m = (
        (points[:, 0] >= x0)
        & (points[:, 0] <= x1)
        & (points[:, 1] >= y0)
        & (points[:, 1] <= y1)
        & (points[:, 2] >= z0)
        & (points[:, 2] <= z1)
    )
    pts = points[m]
    if pts.shape[0] == 0 or not cfg.use_prior_xy:
        return pts
    prior = np.asarray(cfg.prior_xy, dtype=np.float64)
    dxy = np.linalg.norm(pts[:, :2] - prior.reshape(1, 2), axis=1)
    return pts[dxy <= cfg.prior_xy_radius_m]


def _refine_inliers(points: np.ndarray, cfg: RodDetectConfig) -> np.ndarray:
    """PCA 粗轴 → 距轴 inlier 精炼（去掉臂/桌面离群点）。"""
    if points.shape[0] < cfg.min_points:
        return points
    center = points.mean(axis=0)
    centered = points - center
    cov = (centered.T @ centered) / max(points.shape[0], 1)
    _, eigvecs = np.linalg.eigh(cov)
    axis = eigvecs[:, 2]
    axis = axis / max(float(np.linalg.norm(axis)), 1e-12)
    # 到轴线距离
    cross = np.cross(axis.reshape(1, 3), centered)
    dist = np.linalg.norm(cross, axis=1)
    inliers = dist <= cfg.inlier_dist_m
    if int(inliers.sum()) >= cfg.min_points:
        return points[inliers]
    return points


def fit_rod_cylinder(points: np.ndarray, cfg: RodDetectConfig) -> CylinderObstacle | None:
    """PCA 拟合有限圆柱（半径固定为 cfg.rod_radius）。"""
    if points.shape[0] < cfg.min_points:
        return None

    centroid = points.mean(axis=0)
    centered = points - centroid
    cov = (centered.T @ centered) / max(points.shape[0], 1)
    eigvals, eigvecs = np.linalg.eigh(cov)
    axis = eigvecs[:, int(np.argmax(eigvals))]
    axis = axis / max(float(np.linalg.norm(axis)), 1e-12)
    if axis[2] < 0.0:
        axis = -axis

    proj = centered @ axis
    half_length = float(max((proj.max() - proj.min()) * 0.5, cfg.min_half_length))
    t_mid = 0.5 * (float(proj.min()) + float(proj.max()))
    center = centroid + axis * t_mid

    # 已知杆长时：用标称半长，沿轴补全可能被遮挡的下半段
    if cfg.rod_half_length > half_length * 1.15 and float(np.abs(axis[2])) > 0.85:
        center = center - axis * (cfg.rod_half_length - half_length)
        half_length = float(cfg.rod_half_length)

    return CylinderObstacle(
        name=cfg.name,
        center=center,
        axis=axis,
        radius=float(cfg.rod_radius),
        half_length=half_length,
    )


@dataclass
class RodObstacleTracker:
    cfg: RodDetectConfig = field(default_factory=RodDetectConfig)
    _tracked: CylinderObstacle | None = None
    last_debug: RodDetectDebug = field(default_factory=RodDetectDebug)

    def reset(self) -> None:
        self._tracked = None
        self.last_debug = RodDetectDebug()

    def update(
        self,
        depth_m: np.ndarray,
        intr: CameraIntrinsics,
        T_wc: np.ndarray,
        *,
        gt: CylinderObstacle | None = None,
    ) -> list[CylinderObstacle]:
        pts_all = unproject_depth_map(
            intr,
            T_wc,
            depth_m,
            min_depth_m=self.cfg.min_depth_m,
            max_depth_m=self.cfg.max_depth_m,
        )
        pts = _filter_roi(pts_all, self.cfg)
        pts = _refine_inliers(pts, self.cfg)
        obs = fit_rod_cylinder(pts, self.cfg)

        dbg = RodDetectDebug(
            n_depth_valid=int(pts_all.shape[0]),
            n_roi=int(pts.shape[0]),
            detected=obs is not None,
        )

        if obs is not None:
            if self._tracked is None:
                self._tracked = obs
            else:
                a = float(self.cfg.ema_alpha)
                center = (1.0 - a) * self._tracked.center + a * obs.center
                axis = (1.0 - a) * self._tracked.axis + a * obs.axis
                axis = axis / max(float(np.linalg.norm(axis)), 1e-12)
                half_length = (1.0 - a) * self._tracked.half_length + a * obs.half_length
                self._tracked = CylinderObstacle(
                    name=self.cfg.name,
                    center=center,
                    axis=axis,
                    radius=self.cfg.rod_radius,
                    half_length=float(half_length),
                )
        elif self._tracked is not None:
            dbg.using_tracker = True

        if gt is not None and self._tracked is not None:
            dbg.center_err_mm = float(np.linalg.norm(self._tracked.center - gt.center) * 1000.0)
            dot = float(np.clip(abs(np.dot(self._tracked.axis, gt.axis)), -1.0, 1.0))
            dbg.axis_angle_deg = float(np.degrees(np.arccos(dot)))

        self.last_debug = dbg
        if self._tracked is None:
            return []
        return [self._tracked]
