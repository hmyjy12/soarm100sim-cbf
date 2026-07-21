from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import CameraInfo, Image, PointCloud2, PointField


def stamp_s(msg: Any) -> float:
    stamp = msg.header.stamp
    return float(stamp.sec) + float(stamp.nanosec) * 1e-9


def image_to_numpy(msg: Image) -> np.ndarray:
    if msg.encoding == "rgb8":
        return np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3).copy()
    if msg.encoding == "bgr8":
        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        return arr[..., ::-1].copy()
    if msg.encoding == "rgba8":
        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 4)
        return arr[..., :3].copy()
    if msg.encoding == "mono8":
        return np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width).copy()
    if msg.encoding == "16UC1":
        return np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width).astype(np.float32) * 1e-3
    if msg.encoding == "32FC1":
        return np.frombuffer(msg.data, dtype=np.float32).reshape(msg.height, msg.width).copy()
    raise ValueError(f"unsupported image encoding: {msg.encoding}")


def numpy_to_mask_msg(mask: np.ndarray, *, stamp, frame_id: str) -> Image:
    img = np.asarray(mask, dtype=bool).astype(np.uint8) * 255
    msg = Image()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.height = int(img.shape[0])
    msg.width = int(img.shape[1])
    msg.encoding = "mono8"
    msg.is_bigendian = False
    msg.step = int(img.shape[1])
    msg.data = np.ascontiguousarray(img).tobytes()
    return msg


def numpy_rgb_to_msg(rgb: np.ndarray, *, stamp, frame_id: str) -> Image:
    img = np.asarray(rgb, dtype=np.uint8)
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError(f"expected HxWx3 rgb image, got {img.shape}")
    msg = Image()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.height = int(img.shape[0])
    msg.width = int(img.shape[1])
    msg.encoding = "rgb8"
    msg.is_bigendian = False
    msg.step = int(img.shape[1]) * 3
    msg.data = np.ascontiguousarray(img).tobytes()
    return msg


def camera_intrinsics(info: CameraInfo) -> tuple[float, float, float, float]:
    k = info.k
    return float(k[0]), float(k[4]), float(k[2]), float(k[5])


def masked_depth_to_points(depth_m: np.ndarray, mask: np.ndarray, info: CameraInfo) -> np.ndarray:
    d = np.asarray(depth_m, dtype=np.float32)
    m = np.asarray(mask, dtype=bool)
    valid = m & np.isfinite(d) & (d > 1e-4)
    if not np.any(valid):
        return np.zeros((0, 3), dtype=np.float32)
    v, u = np.nonzero(valid)
    z = d[v, u].astype(np.float32)
    fx, fy, cx, cy = camera_intrinsics(info)
    x = (u.astype(np.float32) - cx) * z / fx
    y = (v.astype(np.float32) - cy) * z / fy
    return np.stack([x, y, z], axis=1).astype(np.float32)


def pointcloud2_xyz(points: np.ndarray, *, stamp, frame_id: str) -> PointCloud2:
    pts = np.asarray(points, dtype=np.float32).reshape(-1, 3)
    msg = PointCloud2()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.height = 1
    msg.width = int(pts.shape[0])
    msg.fields = [
        PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
    ]
    msg.is_bigendian = False
    msg.point_step = 12
    msg.row_step = msg.point_step * msg.width
    msg.is_dense = False
    msg.data = pts.tobytes()
    return msg


def pose_from_xyz(xyz: np.ndarray, *, stamp, frame_id: str) -> PoseStamped:
    p = np.asarray(xyz, dtype=np.float64).reshape(3)
    msg = PoseStamped()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.pose.position.x = float(p[0])
    msg.pose.position.y = float(p[1])
    msg.pose.position.z = float(p[2])
    msg.pose.orientation.w = 1.0
    return msg


def bbox_from_mask(mask: np.ndarray, expand_px: int = 0) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(np.asarray(mask, dtype=bool))
    if xs.size == 0:
        return None
    h, w = mask.shape[:2]
    x1 = max(0, int(xs.min()) - int(expand_px))
    y1 = max(0, int(ys.min()) - int(expand_px))
    x2 = min(w, int(xs.max()) + int(expand_px) + 1)
    y2 = min(h, int(ys.max()) + int(expand_px) + 1)
    return x1, y1, x2, y2


def dump_json(path: str | Path, data: dict[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)
