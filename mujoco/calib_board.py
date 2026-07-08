"""仿真棋盘格：纹理生成、3D 角点、OpenCV ↔ MuJoCo 外参转换。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np

try:
    import cv2
except ImportError as exc:
    raise ImportError("calib_board 需要 opencv-python: pip install opencv-python") from exc


@dataclass(frozen=True)
class ChessboardSpec:
    """OpenCV 内角点数量 (cols, rows)，即 findChessboardCorners 的 patternSize。"""

    inner_cols: int = 9
    inner_rows: int = 6
    square_size_m: float = 0.025

    @property
    def pattern_size(self) -> tuple[int, int]:
        return self.inner_cols, self.inner_rows

    @property
    def num_inner_corners(self) -> int:
        return self.inner_cols * self.inner_rows

    @property
    def board_width_m(self) -> float:
        return self.inner_cols * self.square_size_m

    @property
    def board_height_m(self) -> float:
        return self.inner_rows * self.square_size_m

    @property
    def geom_half_size(self) -> tuple[float, float, float]:
        """MuJoCo box half-size；板面在 body 的 XY 平面，+Z 为法向。"""
        sx = 0.5 * (self.inner_cols + 1) * self.square_size_m
        sy = 0.5 * (self.inner_rows + 1) * self.square_size_m
        return sx, sy, 0.002

    def object_points(self) -> np.ndarray:
        """N×3 角点，板坐标系 Z=0，原点在第 0 个内角点（OpenCV 惯例）。"""
        cols, rows = self.pattern_size
        grid = np.zeros((cols * rows, 3), dtype=np.float64)
        grid[:, :2] = (
            np.mgrid[0:cols, 0:rows].T.reshape(-1, 2).astype(np.float64)
            * self.square_size_m
        )
        return grid

    def body_origin_to_board_center_offset(self) -> np.ndarray:
        """body 原点在第一个内角点；几何中心偏移。"""
        return np.array(
            [
                0.5 * (self.inner_cols - 1) * self.square_size_m,
                0.5 * (self.inner_rows - 1) * self.square_size_m,
                0.0,
            ],
            dtype=np.float64,
        )


# OpenCV 相机系 (X右 Y下 Z前) → MuJoCo 相机系 (X右 Y上 -Z前)
_R_OPENCV_TO_MUJOCO = np.diag([1.0, -1.0, -1.0])


def generate_checker_texture(
    spec: ChessboardSpec,
    path: Path,
    *,
    tex_square_px: int = 64,
) -> Path:
    """生成与 object_points 对齐的棋盘 PNG（外圈各多 1 格）。"""
    path = Path(path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    cols, rows = spec.inner_cols + 1, spec.inner_rows + 1
    w, h = cols * tex_square_px, rows * tex_square_px
    img = np.zeros((h, w), dtype=np.uint8)
    for j in range(rows):
        for i in range(cols):
            val = 255 if (i + j) % 2 == 0 else 0
            y0, y1 = j * tex_square_px, (j + 1) * tex_square_px
            x0, x1 = i * tex_square_px, (i + 1) * tex_square_px
            img[y0:y1, x0:x1] = val
    if not cv2.imwrite(str(path), img):
        raise RuntimeError(f"cannot write checker texture {path}")
    return path


def set_free_body_pose(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    body_name: str,
    pos: np.ndarray,
    quat_wxyz: np.ndarray,
) -> None:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name)
    if bid < 0:
        raise ValueError(f"body not found: {body_name}")
    jnt = int(model.body_jntnum[bid])
    if jnt != 1:
        raise ValueError(f"{body_name} 需要单个 free joint")
    jid = int(model.body_jntadr[bid])
    if int(model.jnt_type[jid]) != int(mujoco.mjtJoint.mjJNT_FREE):
        raise ValueError(f"{body_name} joint 不是 free")
    adr = int(model.jnt_qposadr[jid])
    data.qpos[adr : adr + 3] = np.asarray(pos, dtype=np.float64).reshape(3)
    q = np.asarray(quat_wxyz, dtype=np.float64).reshape(4)
    q /= max(float(np.linalg.norm(q)), 1e-12)
    data.qpos[adr + 3 : adr + 7] = q
    vadr = int(model.jnt_dofadr[jid])
    data.qvel[vadr : vadr + 6] = 0.0
    mujoco.mj_forward(model, data)


def board_T_world(model: mujoco.MjModel, data: mujoco.MjData, body_name: str = "calib_board") -> np.ndarray:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name)
    R = np.asarray(data.xmat[bid], dtype=np.float64).reshape(3, 3)
    t = np.asarray(data.xpos[bid], dtype=np.float64)
    T = np.eye(4, dtype=np.float64)
    T[:3, :3] = R
    T[:3, 3] = t
    return T


def object_points_world(
    spec: ChessboardSpec,
    T_world_board: np.ndarray,
) -> np.ndarray:
    pts = spec.object_points()
    R, t = T_world_board[:3, :3], T_world_board[:3, 3]
    return (R @ pts.T).T + t


def quat_wxyz_from_R(R: np.ndarray) -> np.ndarray:
    q = np.zeros(4, dtype=np.float64)
    mujoco.mju_mat2Quat(q, np.asarray(R, dtype=np.float64).reshape(-1))
    return q


def quat_board_facing_point(
    board_pos: np.ndarray,
    target: np.ndarray,
    *,
    up_world: np.ndarray | None = None,
) -> np.ndarray:
    """板面 +Z_body 指向 target（相机），便于正对棋盘拍摄。"""
    up = np.array([0.0, 0.0, 1.0] if up_world is None else up_world, dtype=np.float64)
    z = np.asarray(target, dtype=np.float64) - np.asarray(board_pos, dtype=np.float64)
    zn = float(np.linalg.norm(z))
    if zn < 1e-8:
        z = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    else:
        z = z / zn
    x = np.cross(up, z)
    xn = float(np.linalg.norm(x))
    if xn < 1e-6:
        x = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    else:
        x = x / xn
    y = np.cross(z, x)
    R = np.column_stack([x, y, z])
    return quat_wxyz_from_R(R)


def detect_corners(gray: np.ndarray, spec: ChessboardSpec) -> np.ndarray | None:
    flags = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE
    pattern = spec.pattern_size
    corners = None
    if hasattr(cv2, "findChessboardCornersSB"):
        ok, corners = cv2.findChessboardCornersSB(gray, pattern, flags)
        if ok:
            return corners.reshape(-1, 2).astype(np.float64)
    ok, corners = cv2.findChessboardCorners(gray, pattern, flags)
    if not ok:
        return None
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 1e-4)
    corners = cv2.cornerSubPix(
        gray,
        corners,
        winSize=(5, 5),
        zeroZone=(-1, -1),
        criteria=crit,
    )
    return corners.reshape(-1, 2).astype(np.float64)


def T_world_cam_from_opencv_rvec_tvec(
    rvec: np.ndarray,
    tvec: np.ndarray,
    T_world_board: np.ndarray,
) -> np.ndarray:
    """由 OpenCV solvePnP（board 系 obj 点）恢复 MuJoCo ``T_world_cam``。"""
    R_cv, _ = cv2.Rodrigues(np.asarray(rvec, dtype=np.float64).reshape(3, 1))
    t_cv = np.asarray(tvec, dtype=np.float64).reshape(3)
    R_cam_board = _R_OPENCV_TO_MUJOCO @ R_cv
    t_cam_board = _R_OPENCV_TO_MUJOCO @ t_cv
    T_cam_board = np.eye(4, dtype=np.float64)
    T_cam_board[:3, :3] = R_cam_board
    T_cam_board[:3, 3] = t_cam_board
    T_board_cam = np.linalg.inv(T_cam_board)
    return T_world_board @ T_board_cam


def T_world_cam_from_world_points_pnp(
    object_points_world: np.ndarray,
    image_uv: np.ndarray,
    K: np.ndarray,
) -> np.ndarray | None:
    """已知世界系 3D 角点时的 PnP（仿真 GT 模式推荐）。"""
    obj = np.asarray(object_points_world, dtype=np.float32).reshape(-1, 3)
    uv = np.asarray(image_uv, dtype=np.float32).reshape(-1, 2)
    ok, rvec, tvec = cv2.solvePnP(obj, uv, K, None, flags=cv2.SOLVEPNP_ITERATIVE)
    if not ok:
        return None
    R_cv, _ = cv2.Rodrigues(rvec)
    t_cv = tvec.reshape(3)
    T_cw = np.eye(4, dtype=np.float64)
    T_cw[:3, :3] = _R_OPENCV_TO_MUJOCO @ R_cv
    T_cw[:3, 3] = _R_OPENCV_TO_MUJOCO @ t_cv
    return np.linalg.inv(T_cw)


def T_parent_cam_from_world_cam(T_world_cam: np.ndarray, T_world_parent: np.ndarray) -> np.ndarray:
    return np.linalg.inv(T_world_parent) @ T_world_cam
