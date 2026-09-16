from __future__ import annotations

import json
from pathlib import Path
import time

import numpy as np
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import CameraInfo, Image, PointCloud2

from soarm100_vision.vision_utils import (
    image_to_numpy,
    numpy_rgb_to_msg,
    pointcloud2_to_xyz,
)


def project_base_points(
    points_base: np.ndarray,
    T_parent_cam: np.ndarray,
    camera_matrix: np.ndarray,
    width: int,
    height: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Project base-frame points into the registered ROS optical image."""
    points = np.asarray(points_base, dtype=np.float64).reshape(-1, 3)
    if points.shape[0] == 0:
        return np.zeros((0, 2), dtype=np.int32), np.zeros(0, dtype=np.float64)
    transform = np.asarray(T_parent_cam, dtype=np.float64).reshape(4, 4)
    # T_parent_cam uses MuJoCo camera axes. ROS optical axes differ in Y/Z.
    points_mj = (transform[:3, :3].T @ (points - transform[:3, 3]).T).T
    points_optical = points_mj * np.array([1.0, -1.0, -1.0])
    z = points_optical[:, 2]
    valid = np.isfinite(points_optical).all(axis=1) & (z > 1.0e-4)
    fx, fy = float(camera_matrix[0, 0]), float(camera_matrix[1, 1])
    cx, cy = float(camera_matrix[0, 2]), float(camera_matrix[1, 2])
    u = fx * points_optical[:, 0] / np.maximum(z, 1.0e-4) + cx
    v = fy * points_optical[:, 1] / np.maximum(z, 1.0e-4) + cy
    valid &= (u >= 0.0) & (u < width) & (v >= 0.0) & (v < height)
    pixels = np.column_stack((np.rint(u[valid]), np.rint(v[valid]))).astype(np.int32)
    return pixels, z[valid]


class ObstacleOverlayViewerNode(Node):
    def __init__(self) -> None:
        super().__init__("soarm100_obstacle_overlay_viewer")
        self.declare_parameter("repo_root", str(Path(__file__).resolve().parents[3]))
        self.declare_parameter(
            "calib_json", "hardware/calibration/camera/real_camera_calib.json"
        )
        self.declare_parameter("input_camera_name", "scene_depth")
        self.declare_parameter("rgb_topic", "/camera/color/image_raw")
        self.declare_parameter("camera_info_topic", "/camera/color/camera_info")
        self.declare_parameter("obstacle_cloud_topic", "/obstacle/cloud")
        self.declare_parameter("ignored_thin_topic", "/obstacle/ignored_thin")
        self.declare_parameter("worst_point_topic", "/obstacle/worst_point")
        self.declare_parameter("overlay_topic", "/debug/obstacle_overlay")
        self.declare_parameter("show_window", True)
        self.declare_parameter("window_name", "SO-ARM100 CBF obstacles")
        self.declare_parameter("max_fps", 10.0)
        self.declare_parameter("mask_radius_px", 6)
        self.declare_parameter("mask_close_px", 13)
        self.declare_parameter("min_component_area_px", 20)
        self.declare_parameter("cloud_stale_s", 1.5)

        repo = Path(str(self.get_parameter("repo_root").value)).expanduser().resolve()
        calib = Path(str(self.get_parameter("calib_json").value))
        if not calib.is_absolute():
            calib = repo / calib
        payload = json.loads(calib.read_text(encoding="utf-8"))
        camera_name = str(self.get_parameter("input_camera_name").value)
        self._T_parent_cam = np.asarray(
            payload["mounts"][camera_name]["T_parent_cam"], dtype=np.float64
        ).reshape(4, 4)

        self._rgb: Image | None = None
        self._info: CameraInfo | None = None
        self._points = np.zeros((0, 3), dtype=np.float32)
        self._ignored_thin_points = np.zeros((0, 3), dtype=np.float32)
        self._cloud_received_at: float | None = None
        self._worst_point: np.ndarray | None = None
        self._last_draw_at = 0.0
        self._warned_info_size_mismatch = False
        self._cv2 = None
        self._window_ok = False
        if bool(self.get_parameter("show_window").value):
            self._init_window()

        self._overlay_pub = self.create_publisher(
            Image, str(self.get_parameter("overlay_topic").value), 1
        )
        self.create_subscription(
            Image,
            str(self.get_parameter("rgb_topic").value),
            self._on_rgb,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            CameraInfo,
            str(self.get_parameter("camera_info_topic").value),
            self._on_info,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            PointCloud2,
            str(self.get_parameter("obstacle_cloud_topic").value),
            self._on_cloud,
            1,
        )
        self.create_subscription(
            PointCloud2,
            str(self.get_parameter("ignored_thin_topic").value),
            self._on_ignored_thin,
            1,
        )
        self.create_subscription(
            PointStamped,
            str(self.get_parameter("worst_point_topic").value),
            self._on_worst_point,
            1,
        )
        rate = max(float(self.get_parameter("max_fps").value), 1.0)
        self.create_timer(1.0 / rate, self._tick)
        self.get_logger().info(
            "obstacle overlay ready: green=CBF mask blue=ignored thin yellow=components "
            f"overlay={self.get_parameter('overlay_topic').value}"
        )

    def _init_window(self) -> None:
        try:
            import cv2

            self._cv2 = cv2
            cv2.namedWindow(
                str(self.get_parameter("window_name").value), cv2.WINDOW_NORMAL
            )
            self._window_ok = True
        except Exception as exc:
            self.get_logger().warning(f"OpenCV window unavailable: {exc}")

    def _on_rgb(self, msg: Image) -> None:
        self._rgb = msg

    def _on_info(self, msg: CameraInfo) -> None:
        self._info = msg

    def _on_cloud(self, msg: PointCloud2) -> None:
        if msg.header.frame_id not in ("", "base"):
            self.get_logger().warning(
                f"ignoring obstacle cloud frame={msg.header.frame_id!r}; expected 'base'",
                throttle_duration_sec=2.0,
            )
            return
        self._points = pointcloud2_to_xyz(msg)
        self._cloud_received_at = time.monotonic()

    def _on_worst_point(self, msg: PointStamped) -> None:
        if msg.header.frame_id in ("", "base"):
            self._worst_point = np.array(
                [msg.point.x, msg.point.y, msg.point.z], dtype=np.float64
            )

    def _on_ignored_thin(self, msg: PointCloud2) -> None:
        if msg.header.frame_id in ("", "base"):
            self._ignored_thin_points = pointcloud2_to_xyz(msg)

    def _tick(self) -> None:
        if self._rgb is None or self._info is None or self._cv2 is None:
            return
        now = time.monotonic()
        min_dt = 1.0 / max(float(self.get_parameter("max_fps").value), 1.0)
        if now - self._last_draw_at < min_dt:
            return
        self._last_draw_at = now
        rgb = np.asarray(image_to_numpy(self._rgb), dtype=np.uint8)
        if rgb.ndim != 3 or rgb.shape[2] != 3:
            return
        out = rgb.copy()
        height, width = out.shape[:2]
        if (
            (int(self._info.width), int(self._info.height)) != (width, height)
            and not self._warned_info_size_mismatch
        ):
            self._warned_info_size_mismatch = True
            self.get_logger().warning(
                "obstacle overlay RGB/CameraInfo size mismatch: "
                f"RGB={width}x{height}, "
                f"CameraInfo={int(self._info.width)}x{int(self._info.height)}; "
                "projection overlay may be shifted"
            )
        K = np.asarray(self._info.k, dtype=np.float64).reshape(3, 3)
        pixels, _ = project_base_points(
            self._points, self._T_parent_cam, K, width, height
        )
        ignored_pixels, _ = project_base_points(
            self._ignored_thin_points, self._T_parent_cam, K, width, height
        )
        mask = np.zeros((height, width), dtype=np.uint8)
        radius = max(int(self.get_parameter("mask_radius_px").value), 1)
        for u, v in pixels:
            self._cv2.circle(mask, (int(u), int(v)), radius, 255, -1)
        close_px = max(int(self.get_parameter("mask_close_px").value), 1)
        if close_px > 1 and np.any(mask):
            kernel = self._cv2.getStructuringElement(
                self._cv2.MORPH_ELLIPSE, (close_px, close_px)
            )
            mask = self._cv2.morphologyEx(mask, self._cv2.MORPH_CLOSE, kernel)

        green = np.zeros_like(out)
        green[..., 1] = 255
        selected = mask > 0
        out[selected] = (0.55 * out[selected] + 0.45 * green[selected]).astype(np.uint8)
        for u, v in ignored_pixels:
            self._cv2.circle(out, (int(u), int(v)), radius, (0, 120, 255), -1)
        components = 0
        min_area = int(self.get_parameter("min_component_area_px").value)
        count, _, stats, _ = self._cv2.connectedComponentsWithStats(mask, 8)
        for index in range(1, count):
            x, y, w, h, area = (int(v) for v in stats[index])
            if area < min_area:
                continue
            components += 1
            self._cv2.rectangle(out, (x, y), (x + w - 1, y + h - 1), (255, 255, 0), 2)
            self._cv2.putText(
                out,
                f"obstacle {components}",
                (x, max(20, y - 5)),
                self._cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                3,
            )
            self._cv2.putText(
                out,
                f"obstacle {components}",
                (x, max(20, y - 5)),
                self._cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                1,
            )

        if self._worst_point is not None:
            worst_pixels, _ = project_base_points(
                self._worst_point.reshape(1, 3), self._T_parent_cam, K, width, height
            )
            if worst_pixels.shape[0] == 1:
                u, v = (int(value) for value in worst_pixels[0])
                self._cv2.circle(out, (u, v), 11, (255, 0, 0), 3)
                self._cv2.putText(
                    out,
                    "CBF WORST",
                    (min(u + 14, width - 120), max(v - 10, 20)),
                    self._cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 0, 0),
                    2,
                )

        age = float("inf") if self._cloud_received_at is None else now - self._cloud_received_at
        stale = age > float(self.get_parameter("cloud_stale_s").value)
        status = (
            f"CBF points={self._points.shape[0]} projected={pixels.shape[0]} "
            f"ignored_thin={self._ignored_thin_points.shape[0]} "
            f"boxes={components} age={age:.2f}s{' STALE' if stale else ''}"
        )
        color = (255, 0, 0) if stale else (0, 255, 0)
        self._cv2.putText(out, status, (10, 25), self._cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        self._cv2.putText(out, status, (10, 25), self._cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        self._overlay_pub.publish(
            numpy_rgb_to_msg(
                out, stamp=self._rgb.header.stamp, frame_id=self._rgb.header.frame_id
            )
        )
        if self._window_ok:
            self._cv2.imshow(
                str(self.get_parameter("window_name").value), out[..., ::-1]
            )
            self._cv2.waitKey(1)


def main() -> None:
    rclpy.init()
    node = ObstacleOverlayViewerNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
