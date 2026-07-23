"""相机标定：内参、世界系↔相机系变换、腕部相机随动外参。

约定（与 MuJoCo / camera.py 一致）：
  - 相机光轴沿相机系 **-Z**（``view = -R[:,2]``）
  - ``data.cam_xmat`` 为 3×3，相机系 → 世界系：``p_world = R @ p_cam + t``
  - 深度图（Renderer）为沿像素射线、从相机中心到表面的距离（米）

固定相机（scene_depth）：
  - 仿真：每步可读 ``data.cam_xpos/xmat``；标定文件存 ``T_base_cam``（home 时 base≈world）
  - 真机：棋盘格/Charuco 标一次 ``T_base_cam``，之后不变

腕部相机（wrist_rgb）：
  - 仿真/真机共用：手眼标定存 **静态** ``T_wrist_roll_cam``
  - 每控制步：``T_world_cam(q) = T_world_wrist_roll(q) @ T_wrist_roll_cam``
  - 不可只存一张 ``T_world_cam``（会随臂动而变）
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

try:
    from .camera import camera_extrinsics, camera_id
    from .constants import (
        BASE_BODY,
        CAM_HEIGHT,
        CAM_WIDTH,
        SCENE_DEPTH_CAM,
        WRIST_RGB_CAM,
        WRIST_RGB_CAM_PARENT,
        WRIST_RGB_CAM_POS_LOCAL_WRIST_ROLL,
        WRIST_RGB_CAM_QUAT_LOCAL_WRIST_ROLL,
    )
except ImportError:
    from camera import camera_extrinsics, camera_id  # type: ignore
    from constants import (  # type: ignore
        BASE_BODY,
        CAM_HEIGHT,
        CAM_WIDTH,
        SCENE_DEPTH_CAM,
        WRIST_RGB_CAM,
        WRIST_RGB_CAM_PARENT,
        WRIST_RGB_CAM_POS_LOCAL_WRIST_ROLL,
        WRIST_RGB_CAM_QUAT_LOCAL_WRIST_ROLL,
    )


@dataclass
class CameraIntrinsics:
    name: str
    width: int
    height: int
    fovy_deg: float
    fx: float
    fy: float
    cx: float
    cy: float

    @property
    def K(self) -> np.ndarray:
        return np.array(
            [[self.fx, 0.0, self.cx], [0.0, self.fy, self.cy], [0.0, 0.0, 1.0]],
            dtype=np.float64,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "fovy_deg": self.fovy_deg,
            "fx": self.fx,
            "fy": self.fy,
            "cx": self.cx,
            "cy": self.cy,
            "K": self.K.tolist(),
        }


@dataclass
class MountExtrinsics:
    """相机相对父 body 的静态外参（手眼 / 固定支架）。"""

    camera: str
    parent_body: str
    T_parent_cam: np.ndarray  # 4×4, p_parent = T @ p_cam (齐次)

    def to_dict(self) -> dict[str, Any]:
        return {
            "camera": self.camera,
            "parent_body": self.parent_body,
            "T_parent_cam": self.T_parent_cam.tolist(),
        }


@dataclass
class CameraCalibration:
    world_frame: str
    intrinsics: dict[str, CameraIntrinsics]
    mounts: dict[str, MountExtrinsics]
    fixed_cameras: tuple[str, ...]
    moving_cameras: dict[str, str]  # cam -> parent_body for FK 更新

    def to_dict(self) -> dict[str, Any]:
        return {
            "world_frame": self.world_frame,
            "convention": {
                "optical_axis": "-Z_cam",
                "cam_xmat": "camera_to_world_rotation",
                "depth": "distance_along_ray_from_camera_center_m",
            },
            "intrinsics": {k: v.to_dict() for k, v in self.intrinsics.items()},
            "mounts": {k: v.to_dict() for k, v in self.mounts.items()},
            "fixed_cameras": list(self.fixed_cameras),
            "moving_cameras": dict(self.moving_cameras),
        }

    def save_json(self, path: Path | str) -> None:
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> CameraCalibration:
        intr: dict[str, CameraIntrinsics] = {}
        for name, raw in d["intrinsics"].items():
            intr[name] = CameraIntrinsics(
                name=str(raw.get("name", name)),
                width=int(raw["width"]),
                height=int(raw["height"]),
                fovy_deg=float(raw.get("fovy_deg", 0.0)),
                fx=float(raw["fx"]),
                fy=float(raw["fy"]),
                cx=float(raw["cx"]),
                cy=float(raw["cy"]),
            )
        mounts: dict[str, MountExtrinsics] = {}
        for name, raw in d["mounts"].items():
            mounts[name] = MountExtrinsics(
                camera=str(raw.get("camera", name)),
                parent_body=str(raw["parent_body"]),
                T_parent_cam=np.asarray(raw["T_parent_cam"], dtype=np.float64),
            )
        fixed = tuple(str(x) for x in d.get("fixed_cameras", ()))
        moving = {str(k): str(v) for k, v in d.get("moving_cameras", {}).items()}
        return cls(
            world_frame=str(d.get("world_frame", BASE_BODY)),
            intrinsics=intr,
            mounts=mounts,
            fixed_cameras=fixed,
            moving_cameras=moving,
        )

    def intrinsics_for(self, cam_name: str) -> CameraIntrinsics:
        if cam_name not in self.intrinsics:
            raise KeyError(f"camera not in calibration: {cam_name}")
        return self.intrinsics[cam_name]

    def mount_for(self, cam_name: str) -> MountExtrinsics:
        if cam_name not in self.mounts:
            raise KeyError(f"camera mount not in calibration: {cam_name}")
        return self.mounts[cam_name]


DEFAULT_CALIB_JSON = (
    Path(__file__).resolve().parent.parent / "logs" / "calib" / "camera_calib.json"
)


def load_json(path: Path | str | None = None) -> CameraCalibration:
    """加载 ``camera_calib.json``（真机 / 仿真共用）。"""
    p = Path(path if path is not None else DEFAULT_CALIB_JSON).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(
            f"标定文件不存在: {p}\n"
            "  仿真请先运行: python mujoco/calib_verify.py\n"
            "  真机请写入 Charuco/棋盘格标定结果"
        )
    data = json.loads(p.read_text(encoding="utf-8"))
    return CameraCalibration.from_dict(data)


def T_world_cam_calibrated(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    cal: CameraCalibration,
    cam_name: str,
) -> np.ndarray:
    """由标定 JSON 的 ``T_parent_cam`` + 当前父 link 位姿得到 ``T_world_cam``。"""
    mount = cal.mount_for(cam_name)
    return T_world_cam_from_mount(model, data, mount.parent_body, mount.T_parent_cam)


def T_target_cam_source_cam(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    cal: CameraCalibration,
    source_cam: str,
    target_cam: str,
) -> np.ndarray:
    """相机间实时外参：``p_target_cam = T @ p_source_cam``。

    固定相机使用标定 JSON 中的静态 ``T_parent_cam``；腕部相机使用当前
    FK 的父 link 位姿乘静态手眼 ``T_wrist_roll_cam``，因此该矩阵会随关节角变化。
    """
    T_world_source = T_world_cam_calibrated(model, data, cal, source_cam)
    T_world_target = T_world_cam_calibrated(model, data, cal, target_cam)
    return invert_T(T_world_target) @ T_world_source


def transform_points_between_cameras(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    cal: CameraCalibration,
    points_source_cam: np.ndarray,
    source_cam: str,
    target_cam: str,
) -> np.ndarray:
    """N×3 点从 ``source_cam`` 相机系转换到 ``target_cam`` 相机系。"""
    pts = np.asarray(points_source_cam, dtype=np.float64).reshape(-1, 3)
    T_target_source = T_target_cam_source_cam(model, data, cal, source_cam, target_cam)
    return camera_to_world(T_target_source, pts)


def make_T(R: np.ndarray, t: np.ndarray) -> np.ndarray:
    T = np.eye(4, dtype=np.float64)
    T[:3, :3] = np.asarray(R, dtype=np.float64).reshape(3, 3)
    T[:3, 3] = np.asarray(t, dtype=np.float64).reshape(3)
    return T


def invert_T(T: np.ndarray) -> np.ndarray:
    R = T[:3, :3]
    t = T[:3, 3]
    Ti = np.eye(4, dtype=np.float64)
    Ti[:3, :3] = R.T
    Ti[:3, 3] = -R.T @ t
    return Ti


def body_T_world(model: mujoco.MjModel, data: mujoco.MjData, body_name: str) -> np.ndarray:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name)
    if bid < 0:
        raise ValueError(f"body not found: {body_name}")
    R = np.asarray(data.xmat[bid], dtype=np.float64).reshape(3, 3)
    t = np.asarray(data.xpos[bid], dtype=np.float64)
    return make_T(R, t)


def T_world_cam(model: mujoco.MjModel, data: mujoco.MjData, cam_name: str) -> np.ndarray:
    ext = camera_extrinsics(model, data, cam_name)
    return make_T(ext.rot_world, ext.pos_world)


def T_cam_world(model: mujoco.MjModel, data: mujoco.MjData, cam_name: str) -> np.ndarray:
    return invert_T(T_world_cam(model, data, cam_name))


def T_parent_cam_static(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    cam_name: str,
    parent_body: str,
) -> np.ndarray:
    """``T_parent_cam``：p_parent = R @ p_cam + t（与 MuJoCo 链一致）。"""
    T_w_cam = T_world_cam(model, data, cam_name)
    T_w_parent = body_T_world(model, data, parent_body)
    return invert_T(T_w_parent) @ T_w_cam


def T_world_cam_from_mount(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    parent_body: str,
    T_parent_cam: np.ndarray,
) -> np.ndarray:
    """真机/回放：由父 link 位姿 + 静态手眼外参得到当前 ``T_world_cam``。"""
    return body_T_world(model, data, parent_body) @ T_parent_cam


def camera_intrinsics(
    model: mujoco.MjModel,
    cam_name: str,
    *,
    width: int = CAM_WIDTH,
    height: int = CAM_HEIGHT,
) -> CameraIntrinsics:
    cid = camera_id(model, cam_name)
    fovy = float(model.cam_fovy[cid])
    h, w = int(height), int(width)
    fy = h / (2.0 * np.tan(np.deg2rad(fovy) / 2.0))
    fx = fy  # MuJoCo 方形像素、零 skew
    return CameraIntrinsics(
        name=cam_name,
        width=w,
        height=h,
        fovy_deg=fovy,
        fx=float(fx),
        fy=float(fy),
        cx=(w - 1) / 2.0,
        cy=(h - 1) / 2.0,
    )


def world_to_camera(T_world_cam_mat: np.ndarray, points_world: np.ndarray) -> np.ndarray:
    """N×3 世界点 → N×3 相机系（MuJoCo -Z 朝前）。"""
    pts = np.asarray(points_world, dtype=np.float64).reshape(-1, 3)
    R = T_world_cam_mat[:3, :3]
    t = T_world_cam_mat[:3, 3]
    return (R.T @ (pts - t).T).T


def camera_to_world(T_world_cam_mat: np.ndarray, points_cam: np.ndarray) -> np.ndarray:
    pts = np.asarray(points_cam, dtype=np.float64).reshape(-1, 3)
    R = T_world_cam_mat[:3, :3]
    t = T_world_cam_mat[:3, 3]
    return (R @ pts.T).T + t


def pixel_ray_cam(intr: CameraIntrinsics, u: float, v: float) -> np.ndarray:
    """单位射线，相机系，指向场景（-Z 为光轴）。"""
    x = (u - intr.cx) / intr.fx
    y = (v - intr.cy) / intr.fy
    ray = np.array([x, y, -1.0], dtype=np.float64)
    return ray / max(float(np.linalg.norm(ray)), 1e-12)


def project_world(
    intr: CameraIntrinsics,
    T_wc: np.ndarray,
    points_world: np.ndarray,
    *,
    min_depth: float = 1e-4,
) -> tuple[np.ndarray, np.ndarray]:
    """世界点 → 像素 (N×2) 与 valid (N,) bool。在相机后方或太近则 invalid。"""
    p_cam = world_to_camera(T_wc, points_world)
    z = -p_cam[:, 2]
    valid = z > min_depth
    uv = np.full((p_cam.shape[0], 2), np.nan, dtype=np.float64)
    if np.any(valid):
        uv[valid, 0] = intr.fx * p_cam[valid, 0] / z[valid] + intr.cx
        uv[valid, 1] = intr.fy * p_cam[valid, 1] / z[valid] + intr.cy
    return uv, valid


def unproject_depth(
    intr: CameraIntrinsics,
    u: float,
    v: float,
    depth_m: float,
) -> np.ndarray:
    """深度图像素 → 相机系 3D（深度为沿射线距离）。"""
    ray = pixel_ray_cam(intr, u, v)
    return ray * float(depth_m)


def unproject_depth_to_world(
    intr: CameraIntrinsics,
    T_wc: np.ndarray,
    u: float,
    v: float,
    depth_m: float,
) -> np.ndarray:
    p_cam = unproject_depth(intr, u, v, depth_m)
    return camera_to_world(T_wc, p_cam.reshape(1, 3))[0]


def export_sim_calibration(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    *,
    world_frame: str = BASE_BODY,
) -> CameraCalibration:
    """从当前 MuJoCo 状态导出仿真 ground-truth 标定（建议在 home 调用）。"""
    intr = {
        SCENE_DEPTH_CAM: camera_intrinsics(model, SCENE_DEPTH_CAM),
        WRIST_RGB_CAM: camera_intrinsics(model, WRIST_RGB_CAM),
    }
    T_base_cam_scene = T_parent_cam_static(model, data, SCENE_DEPTH_CAM, world_frame)
    T_wr_cam = T_parent_cam_static(model, data, WRIST_RGB_CAM, WRIST_RGB_CAM_PARENT)
    mounts = {
        SCENE_DEPTH_CAM: MountExtrinsics(SCENE_DEPTH_CAM, world_frame, T_base_cam_scene),
        WRIST_RGB_CAM: MountExtrinsics(WRIST_RGB_CAM, WRIST_RGB_CAM_PARENT, T_wr_cam),
    }
    return CameraCalibration(
        world_frame=world_frame,
        intrinsics=intr,
        mounts=mounts,
        fixed_cameras=(SCENE_DEPTH_CAM,),
        moving_cameras={WRIST_RGB_CAM: WRIST_RGB_CAM_PARENT},
    )


def wrist_mount_from_mjcf_constants() -> np.ndarray:
    """MJCF 中 wrist_rgb 相对 wrist_roll 的标称位姿（与 XML pos/quat 一致）。"""
    w, x, y, z = WRIST_RGB_CAM_QUAT_LOCAL_WRIST_ROLL
    # MuJoCo body quat: w,x,y,z → rotation matrix
    R = np.zeros((3, 3), dtype=np.float64)
    mujoco.mju_quat2Mat(R.ravel(), np.array([w, x, y, z], dtype=np.float64))
    return make_T(R.reshape(3, 3), np.asarray(WRIST_RGB_CAM_POS_LOCAL_WRIST_ROLL, dtype=np.float64))
