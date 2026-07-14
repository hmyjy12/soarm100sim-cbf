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
    from .constants import BASE_BODY, SCENE_DEPTH_CAM
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
    from constants import BASE_BODY, SCENE_DEPTH_CAM  # type: ignore
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
        self._prev_centers: dict[str, np.ndarray] = {}

    def reset(self) -> None:
        self._obstacles = []
        self._prev_centers.clear()

    @property
    def refresh_every_step(self) -> bool:
        return True

    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        obstacles = load_obstacles(model, data, self.geom_names)
        for obs in obstacles:
            center = np.asarray(getattr(obs, "center", np.zeros(3)), dtype=np.float64).reshape(3)
            prev = self._prev_centers.get(str(obs.name))
            if prev is not None:
                obs.velocity = center - prev
            self._prev_centers[str(obs.name)] = center.copy()
        self._obstacles = obstacles

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
    _prev_centroid: np.ndarray | None = None

    @property
    def refresh_every_step(self) -> bool:
        return True

    def reset(self) -> None:
        self._obstacles = []
        self.last_debug = IdealPointCloudSdfDebug()
        self._prev_centroid = None

    def update(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        geoms = load_obstacles(model, data, self.geom_names)
        clouds = [_sample_obstacle_surface(obs, self.cfg.sample_spacing_m) for obs in geoms]
        clouds = [pts for pts in clouds if pts.shape[0] > 0]
        if clouds:
            points = np.vstack(clouds)
            centroid = np.mean(points, axis=0)
            velocity = np.zeros(3, dtype=np.float64)
            if self._prev_centroid is not None:
                velocity = centroid - self._prev_centroid
            self._prev_centroid = centroid.copy()
            obs = PointCloudSdfObstacle(
                name=self.cfg.name_prefix,
                points=points,
                truncation_distance=float(self.cfg.truncation_distance_m),
                voxel_size=float(self.cfg.voxel_size_m),
                inflate=float(self.cfg.inflate_m),
                velocity=velocity,
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
    _prev_centers: dict[str, np.ndarray] = field(default_factory=dict)

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
        self._prev_centers.clear()

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

        obstacles = self._tracker.update(depth_m, intr, T_wc, gt=gt)
        for obs in obstacles:
            center = np.asarray(getattr(obs, "center", np.zeros(3)), dtype=np.float64).reshape(3)
            prev = self._prev_centers.get(str(obs.name))
            if prev is not None:
                obs.velocity = center - prev
            self._prev_centers[str(obs.name)] = center.copy()
        self._obstacles = obstacles

    def get_obstacles(self) -> list[Obstacle]:
        return list(self._obstacles)

    def close(self) -> None:
        self.camera_rig.close()


@dataclass
class SceneDepthSdfConfig:
    min_depth_m: float = 0.12
    max_depth_m: float = 1.1
    # Reachable workspace crop. Points outside this volume cannot be hit by the
    # arm in this task, so they should not enter the safety field.
    roi_x: tuple[float, float] = (0.02, 0.36)
    roi_y: tuple[float, float] = (-0.08, 0.26)
    roi_z: tuple[float, float] = (0.055, 0.42)
    remove_table_plane: bool = True
    table_z_max_m: float = 0.055
    voxel_size_m: float = 0.01
    min_points: int = 20
    inflate_m: float = 0.01
    truncation_distance_m: float = 0.12
    use_segmentation_self_mask: bool = True
    robot_root_body: str = BASE_BODY
    segmentation_dilate_px: int = 2
    persistence_voxel_size_m: float = 0.012
    persistence_hits: int = 2
    persistence_forget_frames: int = 6
    # Remove the robot's own perceived surface plus the CBF safety shell.
    # Otherwise residual self points just outside the physical capsule are still
    # inside h = dist - d_safe - r_link - inflate, causing constant corrections.
    self_filter_margin_m: float = 0.035
    use_capsule_self_filter_fallback: bool = False
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
    n_robot_masked: int = 0
    n_workspace: int = 0
    n_table_filtered: int = 0
    n_roi: int = 0
    n_self_filtered: int = 0
    n_fused_points: int = 0
    n_persistent_voxels: int = 0
    n_voxel_memory: int = 0
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


def _filter_table_plane(points: np.ndarray, cfg: SceneDepthSdfConfig) -> tuple[np.ndarray, int]:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0 or not bool(cfg.remove_table_plane):
        return pts, 0
    keep = pts[:, 2] > float(cfg.table_z_max_m)
    return pts[keep], int(np.count_nonzero(~keep))


def _body_descendants(model: mujoco.MjModel, root_bid: int) -> set[int]:
    out = {int(root_bid)}
    changed = True
    while changed:
        changed = False
        for bid in range(int(model.nbody)):
            parent = int(model.body_parentid[bid])
            if bid not in out and parent in out:
                out.add(int(bid))
                changed = True
    return out


def _robot_geom_ids(model: mujoco.MjModel, cfg: SceneDepthSdfConfig) -> set[int]:
    root = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(cfg.robot_root_body))
    if root < 0:
        return set()
    bodies = _body_descendants(model, int(root))
    return {int(gid) for gid in range(int(model.ngeom)) if int(model.geom_bodyid[gid]) in bodies}


def _dilate_mask(mask: np.ndarray, radius_px: int) -> np.ndarray:
    m = np.asarray(mask, dtype=bool)
    r = max(int(radius_px), 0)
    if r == 0 or m.size == 0:
        return m
    out = m.copy()
    h, w = m.shape
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx == 0 and dy == 0:
                continue
            y0 = max(0, dy)
            y1 = min(h, h + dy)
            x0 = max(0, dx)
            x1 = min(w, w + dx)
            sy0 = max(0, -dy)
            sy1 = min(h, h - dy)
            sx0 = max(0, -dx)
            sx1 = min(w, w - dx)
            out[y0:y1, x0:x1] |= m[sy0:sy1, sx0:sx1]
    return out


def _robot_segmentation_mask(seg: np.ndarray, robot_geom_ids: set[int], cfg: SceneDepthSdfConfig) -> np.ndarray:
    s = np.asarray(seg)
    if s.ndim != 3 or s.shape[2] < 1 or not robot_geom_ids:
        return np.zeros(s.shape[:2], dtype=bool)
    geom_ids = s[:, :, 0].astype(np.int32)
    mask = np.isin(geom_ids, np.fromiter(robot_geom_ids, dtype=np.int32))
    return _dilate_mask(mask, int(cfg.segmentation_dilate_px))


def _voxel_observations(points: np.ndarray, voxel_size: float) -> dict[tuple[int, int, int], tuple[np.ndarray, int]]:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return {}
    v = max(float(voxel_size), 1e-6)
    keys = np.floor(pts / v).astype(np.int64)
    sums: dict[tuple[int, int, int], np.ndarray] = {}
    counts: dict[tuple[int, int, int], int] = {}
    for key_arr, p in zip(keys, pts):
        key = (int(key_arr[0]), int(key_arr[1]), int(key_arr[2]))
        if key in sums:
            sums[key] += p
            counts[key] += 1
        else:
            sums[key] = p.copy()
            counts[key] = 1
    return {key: (sums[key] / float(counts[key]), counts[key]) for key in sums}


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
    _voxel_memory: dict[tuple[int, int, int], dict[str, object]] = field(default_factory=dict)
    _frame_idx: int = 0
    _robot_geom_ids: set[int] | None = None
    _prev_centroid: np.ndarray | None = None

    @property
    def refresh_every_step(self) -> bool:
        return True

    def reset(self) -> None:
        self._obstacles = []
        self.last_debug = SceneDepthSdfDebug()
        self._voxel_memory.clear()
        self._frame_idx = 0
        self._prev_centroid = None

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
        n_robot_masked = 0
        if bool(self.cfg.use_segmentation_self_mask):
            if self._robot_geom_ids is None:
                self._robot_geom_ids = _robot_geom_ids(model, self.cfg)
            seg = self.camera_rig.capture_segmentation(data, self.cam_name)
            robot_mask = _robot_segmentation_mask(seg, self._robot_geom_ids, self.cfg)
            valid_robot = robot_mask & np.isfinite(depth_m) & (depth_m >= self.cfg.min_depth_m) & (depth_m <= self.cfg.max_depth_m)
            n_robot_masked = int(np.count_nonzero(valid_robot))
            depth_m = np.asarray(depth_m, dtype=np.float64).copy()
            depth_m[robot_mask] = np.nan
        T_wc = self._camera_T_world_cam(model, data)
        pts_all = unproject_depth_map(
            intr,
            T_wc,
            depth_m,
            min_depth_m=self.cfg.min_depth_m,
            max_depth_m=self.cfg.max_depth_m,
        )
        pts_workspace = _filter_sdf_roi(pts_all, self.cfg)
        pts, n_table_filtered = _filter_table_plane(pts_workspace, self.cfg)
        if bool(self.cfg.use_capsule_self_filter_fallback) or not bool(self.cfg.use_segmentation_self_mask):
            pts, n_capsule_filtered = _filter_robot_self_points(model, data, pts, self.cfg)
        else:
            n_capsule_filtered = 0
        self._frame_idx += 1
        observations = _voxel_observations(pts, self.cfg.persistence_voxel_size_m)
        for key, (center, count) in observations.items():
            rec = self._voxel_memory.get(key)
            if rec is None:
                self._voxel_memory[key] = {
                    "hits": 1,
                    "last_seen": int(self._frame_idx),
                    "center": center,
                    "count": int(count),
                }
            else:
                prev_count = int(rec.get("count", 1))
                total_count = prev_count + int(count)
                prev_center = np.asarray(rec.get("center", center), dtype=np.float64)
                rec["center"] = (prev_center * float(prev_count) + center * float(count)) / float(total_count)
                rec["count"] = total_count
                rec["hits"] = int(rec.get("hits", 0)) + 1
                rec["last_seen"] = int(self._frame_idx)
        forget = max(int(self.cfg.persistence_forget_frames), 1)
        stale = [
            key for key, rec in self._voxel_memory.items()
            if int(self._frame_idx) - int(rec.get("last_seen", -10**9)) > forget
        ]
        for key in stale:
            del self._voxel_memory[key]
        hit_thresh = max(int(self.cfg.persistence_hits), 1)
        persistent = [
            np.asarray(rec["center"], dtype=np.float64)
            for rec in self._voxel_memory.values()
            if int(rec.get("hits", 0)) >= hit_thresh
        ]
        pts_persistent = np.vstack(persistent) if persistent else np.zeros((0, 3), dtype=np.float64)
        if pts_persistent.shape[0] >= int(self.cfg.min_points):
            centroid = np.mean(pts_persistent, axis=0)
            velocity = np.zeros(3, dtype=np.float64)
            if self._prev_centroid is not None:
                velocity = centroid - self._prev_centroid
            self._prev_centroid = centroid.copy()
            obs = PointCloudSdfObstacle(
                name=self.cfg.name,
                points=pts_persistent,
                truncation_distance=float(self.cfg.truncation_distance_m),
                voxel_size=float(self.cfg.voxel_size_m),
                inflate=float(self.cfg.inflate_m),
                velocity=velocity,
            )
            self._obstacles = [obs]
            n_sdf = int(obs.points.shape[0])
        else:
            self._obstacles = []
            n_sdf = 0
            self._prev_centroid = None
        self.last_debug = SceneDepthSdfDebug(
            n_depth_valid=int(pts_all.shape[0]),
            n_robot_masked=n_robot_masked,
            n_workspace=int(pts_workspace.shape[0]),
            n_table_filtered=n_table_filtered,
            n_roi=int(pts.shape[0] + n_capsule_filtered),
            n_self_filtered=int(n_robot_masked + n_capsule_filtered),
            n_fused_points=int(pts_persistent.shape[0]),
            n_persistent_voxels=int(pts_persistent.shape[0]),
            n_voxel_memory=int(len(self._voxel_memory)),
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
    if k in ("sdf", "scene_depth_sdf", "depth_sdf", "vision_sdf", "workspace_sdf", "unknown_sdf"):
        rig = MujocoCameraRig(model)
        cal = None if use_sim_cam else load_json(calib_json or DEFAULT_CALIB_JSON)
        return SceneDepthSdfObstacleSource(
            camera_rig=rig,
            calibration=cal,
            use_sim_cam=use_sim_cam,
        )
    if k in ("wrist", "wrist_rgb"):
        return WristRgbObstacleSource()
    raise ValueError(f"unknown obstacle source: {kind!r} (use geom|geom_sdf|vision|workspace_sdf)")
