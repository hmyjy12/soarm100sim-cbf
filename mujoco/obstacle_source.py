"""CBF 障碍物来源：仿真 geom GT 或 scene_depth 视觉估计。

视觉模式默认使用 ``camera_calib.json`` 的内参 K 与外参 T_parent_cam（真机同路径）。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np

try:
    from .cbf import AxisAlignedBoxObstacle, CylinderObstacle, Obstacle, PointCloudSdfObstacle, load_obstacles
    from .calib import (
        CameraCalibration,
        CameraIntrinsics,
        DEFAULT_CALIB_JSON,
        T_world_cam,
        T_world_cam_calibrated,
        camera_intrinsics,
        load_json,
    )
    from .camera import MujocoCameraRig
    from .constants import SCENE_DEPTH_CAM
    from .vision_obstacle import RodDetectConfig, RodDetectDebug, RodObstacleTracker, unproject_depth_map
except ImportError:
    from cbf import AxisAlignedBoxObstacle, CylinderObstacle, Obstacle, PointCloudSdfObstacle, load_obstacles  # type: ignore
    from calib import (  # type: ignore
        CameraCalibration,
        CameraIntrinsics,
        DEFAULT_CALIB_JSON,
        T_world_cam,
        T_world_cam_calibrated,
        camera_intrinsics,
        load_json,
    )
    from camera import MujocoCameraRig  # type: ignore
    from constants import SCENE_DEPTH_CAM  # type: ignore
    from vision_obstacle import RodDetectConfig, RodDetectDebug, RodObstacleTracker, unproject_depth_map  # type: ignore


class ObstacleSource(ABC):
    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        ...

    @abstractmethod
    def get_obstacles(self) -> list[Obstacle]:
        ...

    @property
    def refresh_every_step(self) -> bool:
        return False


class MujocoGeomObstacleSource(ObstacleSource):
    """从 MuJoCo named geom 读取 GT（现有默认路径）。"""

    def __init__(self, geom_names: tuple[str, ...]) -> None:
        self.geom_names = tuple(geom_names)
        self._obstacles: list[Obstacle] = []

    def reset(self) -> None:
        self._obstacles = []

    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        self._obstacles = load_obstacles(model, data, self.geom_names)

    def get_obstacles(self) -> list[Obstacle]:
        return list(self._obstacles)


@dataclass
class IdealPointCloudSdfConfig:
    sample_spacing_m: float = 0.006
    voxel_size_m: float = 0.004
    truncation_distance_m: float = 0.12
    inflate_m: float = 0.0
    name_prefix: str = "ideal_sdf"


@dataclass
class IdealPointCloudSdfDebug:
    n_geoms: int = 0
    n_surface_points: int = 0
    n_sdf_points: int = 0
    detected: bool = False


def _orthonormal_basis(axis: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    z = np.asarray(axis, dtype=np.float64).reshape(3)
    z /= max(float(np.linalg.norm(z)), 1e-12)
    tmp = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    if abs(float(np.dot(tmp, z))) > 0.9:
        tmp = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    u = np.cross(z, tmp)
    u /= max(float(np.linalg.norm(u)), 1e-12)
    v = np.cross(z, u)
    v /= max(float(np.linalg.norm(v)), 1e-12)
    return u, v


def _sample_cylinder_surface(obs: CylinderObstacle, spacing: float) -> np.ndarray:
    center = np.asarray(obs.center, dtype=np.float64).reshape(3)
    axis = np.asarray(obs.axis, dtype=np.float64).reshape(3)
    axis /= max(float(np.linalg.norm(axis)), 1e-12)
    radius = max(float(obs.radius), 1e-6)
    half_length = max(float(obs.half_length), 1e-6)
    spacing = max(float(spacing), 1e-4)
    u, v = _orthonormal_basis(axis)

    n_theta = max(12, int(np.ceil(2.0 * np.pi * radius / spacing)))
    n_z = max(2, int(np.ceil(2.0 * half_length / spacing)) + 1)
    theta = np.linspace(0.0, 2.0 * np.pi, n_theta, endpoint=False, dtype=np.float64)
    zs = np.linspace(-half_length, half_length, n_z, dtype=np.float64)
    circle = np.cos(theta).reshape(-1, 1) * u.reshape(1, 3) + np.sin(theta).reshape(-1, 1) * v.reshape(1, 3)

    side = []
    for z in zs:
        side.append(center.reshape(1, 3) + axis.reshape(1, 3) * z + radius * circle)

    n_r = max(2, int(np.ceil(radius / spacing)) + 1)
    rs = np.linspace(0.0, radius, n_r, dtype=np.float64)
    caps = []
    for z in (-half_length, half_length):
        cap_center = center + axis * z
        for r in rs:
            caps.append(cap_center.reshape(1, 3) + r * circle)
    return np.vstack(side + caps)


def _sample_box_surface(obs: AxisAlignedBoxObstacle, spacing: float) -> np.ndarray:
    center = np.asarray(obs.center, dtype=np.float64).reshape(3)
    half = np.asarray(obs.half_extents, dtype=np.float64).reshape(3)
    spacing = max(float(spacing), 1e-4)
    axes = [
        np.linspace(-half[i], half[i], max(2, int(np.ceil(2.0 * half[i] / spacing)) + 1), dtype=np.float64)
        for i in range(3)
    ]
    pts = []
    for fixed_axis in range(3):
        other = [i for i in range(3) if i != fixed_axis]
        grid0, grid1 = np.meshgrid(axes[other[0]], axes[other[1]], indexing="ij")
        for sign in (-1.0, 1.0):
            p = np.zeros((grid0.size, 3), dtype=np.float64)
            p[:, fixed_axis] = sign * half[fixed_axis]
            p[:, other[0]] = grid0.reshape(-1)
            p[:, other[1]] = grid1.reshape(-1)
            pts.append(center.reshape(1, 3) + p)
    return np.vstack(pts)


def _sample_obstacle_surface(obs: Obstacle, spacing: float) -> np.ndarray:
    if isinstance(obs, CylinderObstacle):
        return _sample_cylinder_surface(obs, spacing)
    if isinstance(obs, AxisAlignedBoxObstacle):
        return _sample_box_surface(obs, spacing)
    if isinstance(obs, PointCloudSdfObstacle):
        return np.asarray(obs.points, dtype=np.float64).reshape(-1, 3)
    return np.zeros((0, 3), dtype=np.float64)


@dataclass
class MujocoGeomPointCloudSdfObstacleSource(ObstacleSource):
    """明确障碍物 geom → 理想表面点云 → SDF（不走视觉链路）。"""

    geom_names: tuple[str, ...]
    cfg: IdealPointCloudSdfConfig = field(default_factory=IdealPointCloudSdfConfig)
    _obstacles: list[Obstacle] = field(default_factory=list)
    last_debug: IdealPointCloudSdfDebug = field(default_factory=IdealPointCloudSdfDebug)

    @property
    def refresh_every_step(self) -> bool:
        return True

    def reset(self) -> None:
        self._obstacles = []
        self.last_debug = IdealPointCloudSdfDebug()

    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        geoms = load_obstacles(model, data, self.geom_names)
        clouds = [_sample_obstacle_surface(obs, self.cfg.sample_spacing_m) for obs in geoms]
        clouds = [pts for pts in clouds if pts.shape[0] > 0]
        if clouds:
            points = np.vstack(clouds)
            obs = PointCloudSdfObstacle(
                name=self.cfg.name_prefix,
                points=points,
                truncation_distance=float(self.cfg.truncation_distance_m),
                voxel_size=float(self.cfg.voxel_size_m),
                inflate=float(self.cfg.inflate_m),
            )
            self._obstacles = [obs]
            n_sdf = int(obs.points.shape[0])
            n_surface = int(points.shape[0])
        else:
            self._obstacles = []
            n_sdf = 0
            n_surface = 0
        self.last_debug = IdealPointCloudSdfDebug(
            n_geoms=int(len(geoms)),
            n_surface_points=n_surface,
            n_sdf_points=n_sdf,
            detected=bool(self._obstacles),
        )

    def get_obstacles(self) -> list[Obstacle]:
        return list(self._obstacles)


@dataclass
class SceneDepthVisionObstacleSource(ObstacleSource):
    """scene_depth 深度 → 圆柱拟合 → CylinderObstacle。"""

    camera_rig: MujocoCameraRig
    cam_name: str = SCENE_DEPTH_CAM
    calibration: CameraCalibration | None = None
    use_sim_cam: bool = False
    rod_cfg: RodDetectConfig = field(default_factory=RodDetectConfig)
    _tracker: RodObstacleTracker = field(default_factory=RodObstacleTracker)
    _obstacles: list[Obstacle] = field(default_factory=list)
    compare_gt_geom: str | None = "obstacle_rod"

    def __post_init__(self) -> None:
        self._tracker = RodObstacleTracker(cfg=self.rod_cfg)

    @property
    def refresh_every_step(self) -> bool:
        return True

    @property
    def last_debug(self) -> RodDetectDebug:
        return self._tracker.last_debug

    def reset(self) -> None:
        self._tracker.reset()
        self._obstacles = []

    def _camera_intrinsics(self, model: mujoco.MjModel) -> CameraIntrinsics:
        if self.use_sim_cam or self.calibration is None:
            return camera_intrinsics(model, self.cam_name)
        return self.calibration.intrinsics_for(self.cam_name)

    def _camera_T_world_cam(self, model: mujoco.MjModel, data: mujoco.MjData) -> np.ndarray:
        if self.use_sim_cam or self.calibration is None:
            return T_world_cam(model, data, self.cam_name)
        return T_world_cam_calibrated(model, data, self.calibration, self.cam_name)

    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        intr = self._camera_intrinsics(model)
        depth_m = self.camera_rig.capture_depth_m(data, self.cam_name)
        T_wc = self._camera_T_world_cam(model, data)

        gt = None
        if self.compare_gt_geom:
            gt_list = load_obstacles(model, data, (self.compare_gt_geom,))
            if gt_list:
                gt = gt_list[0]

        self._obstacles = self._tracker.update(depth_m, intr, T_wc, gt=gt)

    def get_obstacles(self) -> list[Obstacle]:
        return list(self._obstacles)

    def close(self) -> None:
        self.camera_rig.close()


@dataclass
class SceneDepthSdfConfig:
    min_depth_m: float = 0.12
    max_depth_m: float = 1.1
    roi_x: tuple[float, float] = (0.02, 0.36)
    roi_y: tuple[float, float] = (-0.08, 0.26)
    roi_z: tuple[float, float] = (0.02, 0.42)
    voxel_size_m: float = 0.01
    min_points: int = 20
    inflate_m: float = 0.01
    truncation_distance_m: float = 0.12
    self_filter_margin_m: float = 0.008
    self_filter_capsules: tuple[tuple[str, str, float], ...] = (
        ("base", "shoulder_rotation", 0.035),
        ("shoulder_rotation", "shoulder_pitch", 0.035),
        ("shoulder_pitch", "ellbow", 0.038),
        ("ellbow", "wrist_pitch", 0.040),
        ("wrist_pitch", "wrist_jaw", 0.035),
        ("wrist_jaw", "wrist_roll", 0.032),
        ("wrist_roll", "gripper", 0.030),
    )
    name: str = "scene_depth_sdf"


@dataclass
class SceneDepthSdfDebug:
    n_depth_valid: int = 0
    n_roi: int = 0
    n_self_filtered: int = 0
    n_sdf_points: int = 0
    detected: bool = False


def _filter_sdf_roi(points: np.ndarray, cfg: SceneDepthSdfConfig) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return pts
    finite = np.all(np.isfinite(pts), axis=1)
    x0, x1 = cfg.roi_x
    y0, y1 = cfg.roi_y
    z0, z1 = cfg.roi_z
    keep = (
        finite
        & (pts[:, 0] >= x0)
        & (pts[:, 0] <= x1)
        & (pts[:, 1] >= y0)
        & (pts[:, 1] <= y1)
        & (pts[:, 2] >= z0)
        & (pts[:, 2] <= z1)
    )
    return pts[keep]


def _points_near_segment(points: np.ndarray, a: np.ndarray, b: np.ndarray, radius: float) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return np.zeros(0, dtype=bool)
    a = np.asarray(a, dtype=np.float64).reshape(3)
    b = np.asarray(b, dtype=np.float64).reshape(3)
    ab = b - a
    denom = float(ab @ ab)
    if denom < 1e-12:
        d = np.linalg.norm(pts - a.reshape(1, 3), axis=1)
    else:
        t = np.clip(((pts - a.reshape(1, 3)) @ ab) / denom, 0.0, 1.0)
        closest = a.reshape(1, 3) + t.reshape(-1, 1) * ab.reshape(1, 3)
        d = np.linalg.norm(pts - closest, axis=1)
    return d <= float(radius)


def _filter_robot_self_points(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    points: np.ndarray,
    cfg: SceneDepthSdfConfig,
) -> tuple[np.ndarray, int]:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return pts, 0
    near_self = np.zeros(pts.shape[0], dtype=bool)
    margin = max(float(cfg.self_filter_margin_m), 0.0)
    for body_a, body_b, radius in cfg.self_filter_capsules:
        bid_a = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_a)
        bid_b = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_b)
        if bid_a < 0 or bid_b < 0:
            continue
        a = np.asarray(data.xpos[int(bid_a)], dtype=np.float64)
        b = np.asarray(data.xpos[int(bid_b)], dtype=np.float64)
        near_self |= _points_near_segment(pts, a, b, float(radius) + margin)
    return pts[~near_self], int(np.count_nonzero(near_self))


@dataclass
class SceneDepthSdfObstacleSource(ObstacleSource):
    """scene_depth 深度 → 表面点云 unsigned SDF。"""

    camera_rig: MujocoCameraRig
    cam_name: str = SCENE_DEPTH_CAM
    calibration: CameraCalibration | None = None
    use_sim_cam: bool = False
    cfg: SceneDepthSdfConfig = field(default_factory=SceneDepthSdfConfig)
    _obstacles: list[Obstacle] = field(default_factory=list)
    last_debug: SceneDepthSdfDebug = field(default_factory=SceneDepthSdfDebug)

    @property
    def refresh_every_step(self) -> bool:
        return True

    def reset(self) -> None:
        self._obstacles = []
        self.last_debug = SceneDepthSdfDebug()

    def _camera_intrinsics(self, model: mujoco.MjModel) -> CameraIntrinsics:
        if self.use_sim_cam or self.calibration is None:
            return camera_intrinsics(model, self.cam_name)
        return self.calibration.intrinsics_for(self.cam_name)

    def _camera_T_world_cam(self, model: mujoco.MjModel, data: mujoco.MjData) -> np.ndarray:
        if self.use_sim_cam or self.calibration is None:
            return T_world_cam(model, data, self.cam_name)
        return T_world_cam_calibrated(model, data, self.calibration, self.cam_name)

    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        intr = self._camera_intrinsics(model)
        depth_m = self.camera_rig.capture_depth_m(data, self.cam_name)
        T_wc = self._camera_T_world_cam(model, data)
        pts_all = unproject_depth_map(
            intr,
            T_wc,
            depth_m,
            min_depth_m=self.cfg.min_depth_m,
            max_depth_m=self.cfg.max_depth_m,
        )
        pts = _filter_sdf_roi(pts_all, self.cfg)
        pts, n_self_filtered = _filter_robot_self_points(model, data, pts, self.cfg)
        if pts.shape[0] >= int(self.cfg.min_points):
            obs = PointCloudSdfObstacle(
                name=self.cfg.name,
                points=pts,
                truncation_distance=float(self.cfg.truncation_distance_m),
                voxel_size=float(self.cfg.voxel_size_m),
                inflate=float(self.cfg.inflate_m),
            )
            self._obstacles = [obs]
            n_sdf = int(obs.points.shape[0])
        else:
            self._obstacles = []
            n_sdf = 0
        self.last_debug = SceneDepthSdfDebug(
            n_depth_valid=int(pts_all.shape[0]),
            n_roi=int(pts.shape[0] + n_self_filtered),
            n_self_filtered=n_self_filtered,
            n_sdf_points=n_sdf,
            detected=bool(self._obstacles),
        )

    def get_obstacles(self) -> list[Obstacle]:
        return list(self._obstacles)

    def close(self) -> None:
        self.camera_rig.close()


class WristRgbObstacleSource(ObstacleSource):
    """占位：近场 RGB/深度补盲（v1 未实现）。"""

    def reset(self) -> None:
        pass

    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        raise NotImplementedError(
            "wrist_rgb 视觉障碍检测尚未实现；v1 请用 --obstacle-source vision（scene_depth）"
        )

    def get_obstacles(self) -> list[Obstacle]:
        return []


def make_obstacle_source(
    kind: str,
    model: mujoco.MjModel,
    *,
    geom_names: tuple[str, ...] = ("obstacle_rod",),
    calib_json: Path | str | None = None,
    use_sim_cam: bool = False,
) -> ObstacleSource:
    k = str(kind).lower().strip()
    if k in ("geom", "mujoco", "gt"):
        return MujocoGeomObstacleSource(geom_names)
    if k in ("geom_sdf", "ideal_sdf", "pointcloud", "ideal_pointcloud"):
        return MujocoGeomPointCloudSdfObstacleSource(geom_names=tuple(geom_names))
    if k in ("vision", "scene_depth", "depth"):
        rig = MujocoCameraRig(model)
        cal: CameraCalibration | None = None
        if not use_sim_cam:
            cal = load_json(calib_json or DEFAULT_CALIB_JSON)
        return SceneDepthVisionObstacleSource(
            camera_rig=rig,
            calibration=cal,
            use_sim_cam=use_sim_cam,
        )
    if k in ("sdf", "scene_depth_sdf", "depth_sdf", "vision_sdf"):
        rig = MujocoCameraRig(model)
        cal = None if use_sim_cam else load_json(calib_json or DEFAULT_CALIB_JSON)
        return SceneDepthSdfObstacleSource(
            camera_rig=rig,
            calibration=cal,
            use_sim_cam=use_sim_cam,
        )
    if k in ("wrist", "wrist_rgb"):
        return WristRgbObstacleSource()
    raise ValueError(f"unknown obstacle source: {kind!r} (use geom|geom_sdf|vision|sdf)")
