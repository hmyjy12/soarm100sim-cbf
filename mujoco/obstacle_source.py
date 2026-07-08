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
    from .cbf import Obstacle, load_obstacles
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
    from .vision_obstacle import RodDetectConfig, RodDetectDebug, RodObstacleTracker
except ImportError:
    from cbf import Obstacle, load_obstacles  # type: ignore
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
    from vision_obstacle import RodDetectConfig, RodDetectDebug, RodObstacleTracker  # type: ignore


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
    if k in ("wrist", "wrist_rgb"):
        return WristRgbObstacleSource()
    raise ValueError(f"unknown obstacle source: {kind!r} (use geom|vision)")
