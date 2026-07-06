"""夹爪捏合中心 TCP 位姿（位置 + 姿态），采样与训练共用。"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import numpy as np

from sample.constants import (
    TCP_APPROACH_LOCAL_WRIST_ROLL,
    TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL,
    TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER,
)

if TYPE_CHECKING:
    import torch


def _as_vec3(values: tuple[float, float, float] | np.ndarray) -> np.ndarray:
    return np.asarray(values, dtype=np.float64).reshape(3)


def quat_rotate_wxyz_single(quat_wxyz: np.ndarray, vec_xyz: np.ndarray) -> np.ndarray:
    quat = np.asarray(quat_wxyz, dtype=np.float64).reshape(4)
    vec = np.asarray(vec_xyz, dtype=np.float64).reshape(3)
    qw = quat[0]
    qxyz = quat[1:]
    t = 2.0 * np.cross(qxyz, vec)
    return vec + qw * t + np.cross(qxyz, t)


def normalize_quat_wxyz_single(quat_wxyz: np.ndarray) -> np.ndarray:
    quat = np.asarray(quat_wxyz, dtype=np.float64).reshape(4)
    norm = float(np.linalg.norm(quat))
    if norm < 1e-12:
        return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
    return quat / norm


def rotmat_to_quat_wxyz(rot: np.ndarray) -> np.ndarray:
    """3x3 旋转矩阵 -> wxyz 四元数。"""
    m = np.asarray(rot, dtype=np.float64).reshape(3, 3)
    trace = float(np.trace(m))
    if trace > 0.0:
        s = math.sqrt(trace + 1.0) * 2.0
        w = 0.25 * s
        x = (m[2, 1] - m[1, 2]) / s
        y = (m[0, 2] - m[2, 0]) / s
        z = (m[1, 0] - m[0, 1]) / s
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
        w = (m[2, 1] - m[1, 2]) / s
        x = 0.25 * s
        y = (m[0, 1] + m[1, 0]) / s
        z = (m[0, 2] + m[2, 0]) / s
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
        w = (m[0, 2] - m[2, 0]) / s
        x = (m[0, 1] + m[1, 0]) / s
        y = 0.25 * s
        z = (m[1, 2] + m[2, 1]) / s
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
        w = (m[1, 0] - m[0, 1]) / s
        x = (m[0, 2] + m[2, 0]) / s
        y = (m[1, 2] + m[2, 1]) / s
        z = 0.25 * s
    return normalize_quat_wxyz_single(np.array([w, x, y, z], dtype=np.float64))


def compute_pinch_tcp_pose_numpy(
    wrist_roll_pos_w: np.ndarray,
    wrist_roll_quat_wxyz: np.ndarray,
    gripper_pos_w: np.ndarray,
    gripper_quat_wxyz: np.ndarray,
    *,
    fixed_tip_local_wrist_roll: tuple[float, float, float] = TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL,
    moving_tip_local_gripper: tuple[float, float, float] = TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER,
    approach_local_wrist_roll: tuple[float, float, float] = TCP_APPROACH_LOCAL_WRIST_ROLL,
) -> tuple[np.ndarray, np.ndarray]:
    """由 wrist_roll（定爪）与 gripper（动爪）body 位姿计算捏合中心 TCP。"""
    wr_q = normalize_quat_wxyz_single(wrist_roll_quat_wxyz)
    gr_q = normalize_quat_wxyz_single(gripper_quat_wxyz)

    fixed_tip_w = np.asarray(wrist_roll_pos_w, dtype=np.float64).reshape(3) + quat_rotate_wxyz_single(
        wr_q, _as_vec3(fixed_tip_local_wrist_roll)
    )
    moving_tip_w = np.asarray(gripper_pos_w, dtype=np.float64).reshape(3) + quat_rotate_wxyz_single(
        gr_q, _as_vec3(moving_tip_local_gripper)
    )
    tcp_pos_w = 0.5 * (fixed_tip_w + moving_tip_w)

    close_axis = moving_tip_w - fixed_tip_w
    close_norm = float(np.linalg.norm(close_axis))
    if close_norm < 1e-8:
        return tcp_pos_w.astype(np.float64), wr_q.astype(np.float64)

    x_axis = close_axis / close_norm
    z_axis = quat_rotate_wxyz_single(wr_q, _as_vec3(approach_local_wrist_roll))
    z_norm = float(np.linalg.norm(z_axis))
    if z_norm < 1e-8:
        return tcp_pos_w.astype(np.float64), wr_q.astype(np.float64)
    z_axis = z_axis / z_norm

    y_axis = np.cross(z_axis, x_axis)
    y_norm = float(np.linalg.norm(y_axis))
    if y_norm < 1e-8:
        return tcp_pos_w.astype(np.float64), wr_q.astype(np.float64)
    y_axis = y_axis / y_norm
    z_axis = np.cross(x_axis, y_axis)
    z_axis = z_axis / max(float(np.linalg.norm(z_axis)), 1e-12)

    rot = np.column_stack([x_axis, y_axis, z_axis])
    tcp_quat_w = rotmat_to_quat_wxyz(rot)
    return tcp_pos_w.astype(np.float64), tcp_quat_w.astype(np.float64)


def compute_pinch_tcp_pose_torch(
    wrist_roll_pos_w: torch.Tensor,
    wrist_roll_quat_wxyz: torch.Tensor,
    gripper_pos_w: torch.Tensor,
    gripper_quat_wxyz: torch.Tensor,
    *,
    fixed_tip_local_wrist_roll: tuple[float, float, float] = TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL,
    moving_tip_local_gripper: tuple[float, float, float] = TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER,
    approach_local_wrist_roll: tuple[float, float, float] = TCP_APPROACH_LOCAL_WRIST_ROLL,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Batched torch 版，与 numpy 版语义一致。"""
    import torch

    fixed_local = torch.tensor(fixed_tip_local_wrist_roll, device=wrist_roll_pos_w.device, dtype=wrist_roll_pos_w.dtype)
    moving_local = torch.tensor(moving_tip_local_gripper, device=gripper_pos_w.device, dtype=gripper_pos_w.dtype)
    approach_local = torch.tensor(
        approach_local_wrist_roll, device=wrist_roll_pos_w.device, dtype=wrist_roll_pos_w.dtype
    )

    wr_q = wrist_roll_quat_wxyz / torch.norm(wrist_roll_quat_wxyz, dim=-1, keepdim=True).clamp_min(1e-8)
    gr_q = gripper_quat_wxyz / torch.norm(gripper_quat_wxyz, dim=-1, keepdim=True).clamp_min(1e-8)

    fixed_tip_w = wrist_roll_pos_w + _quat_rotate_torch(wr_q, fixed_local.unsqueeze(0).expand_as(wrist_roll_pos_w))
    moving_tip_w = gripper_pos_w + _quat_rotate_torch(gr_q, moving_local.unsqueeze(0).expand_as(gripper_pos_w))
    tcp_pos_w = 0.5 * (fixed_tip_w + moving_tip_w)

    close_axis = moving_tip_w - fixed_tip_w
    close_norm = torch.norm(close_axis, dim=-1, keepdim=True).clamp_min(1e-8)
    x_axis = close_axis / close_norm

    approach = approach_local.unsqueeze(0).expand(wr_q.shape[0], -1)
    z_axis = _quat_rotate_torch(wr_q, approach)
    z_axis = z_axis / torch.norm(z_axis, dim=-1, keepdim=True).clamp_min(1e-8)

    y_axis = torch.cross(z_axis, x_axis, dim=-1)
    y_norm = torch.norm(y_axis, dim=-1, keepdim=True)
    fallback = y_norm.squeeze(-1) < 1e-8

    y_axis = y_axis / y_norm.clamp_min(1e-8)
    z_axis = torch.cross(x_axis, y_axis, dim=-1)
    z_axis = z_axis / torch.norm(z_axis, dim=-1, keepdim=True).clamp_min(1e-8)

    rot = torch.stack([x_axis, y_axis, z_axis], dim=-1)
    tcp_quat_w = _rotmat_to_quat_wxyz_torch(rot)
    if torch.any(fallback):
        tcp_quat_w = torch.where(fallback.unsqueeze(-1), wr_q, tcp_quat_w)
    return tcp_pos_w, tcp_quat_w


def _quat_rotate_torch(quat_wxyz: torch.Tensor, vec_xyz: torch.Tensor) -> torch.Tensor:
    import torch

    qw = quat_wxyz[:, :1]
    qxyz = quat_wxyz[:, 1:]
    t = 2.0 * torch.cross(qxyz, vec_xyz, dim=-1)
    return vec_xyz + qw * t + torch.cross(qxyz, t, dim=-1)


def _rotmat_to_quat_wxyz_torch(rot: torch.Tensor) -> torch.Tensor:
    """Batched 3x3 -> wxyz。"""
    import torch

    m00 = rot[:, 0, 0]
    m11 = rot[:, 1, 1]
    m22 = rot[:, 2, 2]
    trace = m00 + m11 + m22

    quat = torch.zeros(rot.shape[0], 4, device=rot.device, dtype=rot.dtype)
    cond0 = trace > 0.0

    s0 = torch.sqrt(trace[cond0] + 1.0) * 2.0
    quat[cond0, 0] = 0.25 * s0
    quat[cond0, 1] = (rot[cond0, 2, 1] - rot[cond0, 1, 2]) / s0
    quat[cond0, 2] = (rot[cond0, 0, 2] - rot[cond0, 2, 0]) / s0
    quat[cond0, 3] = (rot[cond0, 1, 0] - rot[cond0, 0, 1]) / s0

    cond1 = (~cond0) & (m00 >= m11) & (m00 >= m22)
    s1 = torch.sqrt(1.0 + m00[cond1] - m11[cond1] - m22[cond1]) * 2.0
    quat[cond1, 0] = (rot[cond1, 2, 1] - rot[cond1, 1, 2]) / s1
    quat[cond1, 1] = 0.25 * s1
    quat[cond1, 2] = (rot[cond1, 0, 1] + rot[cond1, 1, 0]) / s1
    quat[cond1, 3] = (rot[cond1, 0, 2] + rot[cond1, 2, 0]) / s1

    cond2 = (~cond0) & (~cond1) & (m11 >= m22)
    s2 = torch.sqrt(1.0 + m11[cond2] - m00[cond2] - m22[cond2]) * 2.0
    quat[cond2, 0] = (rot[cond2, 0, 2] - rot[cond2, 2, 0]) / s2
    quat[cond2, 1] = (rot[cond2, 0, 1] + rot[cond2, 1, 0]) / s2
    quat[cond2, 2] = 0.25 * s2
    quat[cond2, 3] = (rot[cond2, 1, 2] + rot[cond2, 2, 1]) / s2

    cond3 = (~cond0) & (~cond1) & (~cond2)
    s3 = torch.sqrt(1.0 + m22[cond3] - m00[cond3] - m11[cond3]) * 2.0
    quat[cond3, 0] = (rot[cond3, 1, 0] - rot[cond3, 0, 1]) / s3
    quat[cond3, 1] = (rot[cond3, 0, 2] + rot[cond3, 2, 0]) / s3
    quat[cond3, 2] = (rot[cond3, 1, 2] + rot[cond3, 2, 1]) / s3
    quat[cond3, 3] = 0.25 * s3

    return quat / torch.norm(quat, dim=-1, keepdim=True).clamp_min(1e-8)


def quat_to_rpy_wxyz(quat_wxyz: np.ndarray) -> np.ndarray:
    w, x, y, z = np.asarray(quat_wxyz, dtype=np.float64).reshape(4)
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    sinp = 2.0 * (w * y - z * x)
    sinp = max(-1.0, min(1.0, sinp))
    pitch = math.asin(sinp)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    return np.array([roll, pitch, yaw], dtype=np.float64)


def pose_dict_from_arrays(
    pos_rel: np.ndarray,
    quat_wxyz: np.ndarray,
    *,
    orientation_format: str = "quat",
) -> dict:
    block = {
        "pos": {
            "x": float(pos_rel[0]),
            "y": float(pos_rel[1]),
            "z": float(pos_rel[2]),
        },
        "quat": {
            "w": float(quat_wxyz[0]),
            "x": float(quat_wxyz[1]),
            "y": float(quat_wxyz[2]),
            "z": float(quat_wxyz[3]),
        },
    }
    if orientation_format in ("rpy", "both"):
        rpy = quat_to_rpy_wxyz(quat_wxyz)
        block["rpy"] = {
            "roll": float(rpy[0]),
            "pitch": float(rpy[1]),
            "yaw": float(rpy[2]),
        }
    return block
