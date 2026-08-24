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


def expand_mask_bbox(mask: np.ndarray, ratio: float) -> np.ndarray:
    """Return a bbox-expanded mask.

    The original mask is kept exactly; the expanded result fills the enlarged
    bounding box. This is useful as a permissive ROI for grasp planning while
    keeping the raw SAM mask available for target-only point clouds.
    """
    m = np.asarray(mask, dtype=bool)
    if m.size == 0 or not np.any(m):
        return m.copy()
    r = max(float(ratio), 0.0)
    if r <= 0.0:
        return m.copy()
    ys, xs = np.nonzero(m)
    h, w = m.shape[:2]
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    pad_y = max(1, int(round((y1 - y0 + 1) * r)))
    pad_x = max(1, int(round((x1 - x0 + 1) * r)))
    out = np.zeros_like(m, dtype=bool)
    out[
        max(0, y0 - pad_y) : min(h, y1 + pad_y + 1),
        max(0, x0 - pad_x) : min(w, x1 + pad_x + 1),
    ] = True
    return out


def dilate_mask(mask: np.ndarray, radius_px: int) -> np.ndarray:
    m = np.asarray(mask, dtype=bool)
    r = max(int(radius_px), 0)
    if r == 0 or m.size == 0:
        return m.copy()
    out = m.copy()
    h, w = m.shape[:2]
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


def depth_to_points(
    depth_m: np.ndarray, info: CameraInfo, *, pixel_stride: int = 1
) -> np.ndarray:
    d = np.asarray(depth_m, dtype=np.float32)
    valid = np.isfinite(d) & (d > 1e-4)
    stride = max(int(pixel_stride), 1)
    if stride > 1:
        sampled = np.zeros_like(valid)
        sampled[::stride, ::stride] = valid[::stride, ::stride]
        valid = sampled
    return masked_depth_to_points(d, valid, info)


def crop_points_xyz(
    points: np.ndarray,
    *,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    zlim: tuple[float, float],
) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float32).reshape(-1, 3)
    if pts.shape[0] == 0:
        return pts
    m = (
        (pts[:, 0] >= float(xlim[0]))
        & (pts[:, 0] <= float(xlim[1]))
        & (pts[:, 1] >= float(ylim[0]))
        & (pts[:, 1] <= float(ylim[1]))
        & (pts[:, 2] >= float(zlim[0]))
        & (pts[:, 2] <= float(zlim[1]))
    )
    return pts[m]


def filter_table_plane(points: np.ndarray, table_z_max: float, *, enabled: bool = True) -> tuple[np.ndarray, int]:
    pts = np.asarray(points, dtype=np.float32).reshape(-1, 3)
    if pts.shape[0] == 0 or not bool(enabled):
        return pts, 0
    keep = pts[:, 2] > float(table_z_max)
    return pts[keep], int(np.count_nonzero(~keep))


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


def pointcloud2_to_xyz(msg: PointCloud2) -> np.ndarray:
    if msg.point_step < 12:
        raise ValueError(f"PointCloud2 point_step too small: {msg.point_step}")
    offsets = {field.name: int(field.offset) for field in msg.fields}
    if not {"x", "y", "z"}.issubset(offsets):
        raise ValueError("PointCloud2 requires x/y/z fields")
    n = int(msg.width) * int(msg.height)
    if n <= 0:
        return np.zeros((0, 3), dtype=np.float32)
    raw = np.frombuffer(msg.data, dtype=np.uint8)
    pts = np.empty((n, 3), dtype=np.float32)
    for i, name in enumerate(("x", "y", "z")):
        off = offsets[name]
        vals = np.ndarray(
            shape=(n,),
            dtype="<f4" if not msg.is_bigendian else ">f4",
            buffer=raw,
            offset=off,
            strides=(int(msg.point_step),),
        )
        pts[:, i] = vals
    return pts[np.all(np.isfinite(pts), axis=1)]


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


def hsv_color_mask(
    rgb: np.ndarray,
    *,
    target_rgb: tuple[int, int, int],
    hue_tolerance_deg: float = 18.0,
    saturation_min: float = 0.45,
    value_min: float = 0.30,
) -> np.ndarray:
    """Segment pixels near a configurable RGB color in circular HSV space."""
    import cv2

    image = np.asarray(rgb, dtype=np.uint8)
    if image.ndim != 3 or image.shape[2] < 3:
        raise ValueError(f"expected HxWx3 RGB image, got {image.shape}")
    target = np.asarray(target_rgb, dtype=np.uint8).reshape(1, 1, 3)
    hsv = cv2.cvtColor(image[..., :3], cv2.COLOR_RGB2HSV)
    target_hsv = cv2.cvtColor(target, cv2.COLOR_RGB2HSV)[0, 0]
    hue = hsv[..., 0].astype(np.float32) * 2.0
    target_hue = float(target_hsv[0]) * 2.0
    hue_delta = np.abs(hue - target_hue)
    hue_delta = np.minimum(hue_delta, 360.0 - hue_delta)
    saturation = hsv[..., 1].astype(np.float32) / 255.0
    value = hsv[..., 2].astype(np.float32) / 255.0
    return (
        (hue_delta <= max(float(hue_tolerance_deg), 0.0))
        & (saturation >= float(saturation_min))
        & (value >= float(value_min))
    )


def color_components(
    mask: np.ndarray,
    *,
    min_area: int,
) -> list[dict[str, float | tuple[int, int, int, int]]]:
    """Return connected color regions sorted from largest to smallest."""
    import cv2

    binary = np.asarray(mask, dtype=bool).astype(np.uint8)
    count, _labels, stats, centroids = cv2.connectedComponentsWithStats(
        binary, connectivity=8
    )
    components = []
    for index in range(1, int(count)):
        area = int(stats[index, cv2.CC_STAT_AREA])
        if area < max(int(min_area), 1):
            continue
        x = int(stats[index, cv2.CC_STAT_LEFT])
        y = int(stats[index, cv2.CC_STAT_TOP])
        w = int(stats[index, cv2.CC_STAT_WIDTH])
        h = int(stats[index, cv2.CC_STAT_HEIGHT])
        components.append(
            {
                "area": float(area),
                "bbox": (x, y, x + w, y + h),
                "u": float(centroids[index, 0]),
                "v": float(centroids[index, 1]),
            }
        )
    components.sort(key=lambda item: float(item["area"]), reverse=True)
    return components


def parse_rgb(value: str) -> tuple[int, int, int]:
    parts = [int(x) for x in str(value).replace(",", " ").split()]
    if len(parts) != 3 or any(x < 0 or x > 255 for x in parts):
        raise ValueError(f"expected RGB values in [0,255], got {value!r}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def dump_json(path: str | Path, data: dict[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)
