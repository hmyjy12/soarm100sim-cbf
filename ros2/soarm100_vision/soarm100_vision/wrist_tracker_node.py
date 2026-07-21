from __future__ import annotations

import math

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import String

from soarm100_vision.vision_utils import bbox_from_mask, image_to_numpy, masked_depth_to_points, pose_from_xyz


class WristTrackerNode(Node):
    """Lightweight target-center tracking for the wrist camera.

    The tracker consumes the initial segmentation mask, then keeps a local ROI
    around the previous mask/center. It estimates only target translation. The
    grasp orientation, approach axis, and gripper width remain owned by the
    grasp planner until a replan is explicitly requested.
    """

    def __init__(self) -> None:
        super().__init__("soarm100_wrist_tracker")
        self.declare_parameter("depth_topic", "/wrist/depth/image_rect_raw")
        self.declare_parameter("camera_info_topic", "/wrist/depth/camera_info")
        self.declare_parameter("initial_mask_topic", "/target/mask")
        self.declare_parameter("tracked_pose_topic", "/target/tracked_center")
        self.declare_parameter("status_topic", "/target/tracking_status")
        self.declare_parameter("roi_expand_px", 24)
        self.declare_parameter("min_points", 20)
        self.declare_parameter("max_step_m", 0.035)
        self.declare_parameter("warn_delta_m", 0.020)
        self.declare_parameter("replan_delta_m", 0.050)

        self._depth: Image | None = None
        self._info: CameraInfo | None = None
        self._mask: np.ndarray | None = None
        self._initial_center: np.ndarray | None = None
        self._last_center: np.ndarray | None = None
        self._invalid_count = 0

        self._pose_pub = self.create_publisher(PoseStamped, self._param("tracked_pose_topic"), 1)
        self._status_pub = self.create_publisher(String, self._param("status_topic"), 1)
        self.create_subscription(Image, self._param("depth_topic"), self._on_depth, 1)
        self.create_subscription(CameraInfo, self._param("camera_info_topic"), self._on_info, 10)
        self.create_subscription(Image, self._param("initial_mask_topic"), self._on_mask, 1)
        self.create_timer(1.0 / 20.0, self._tick)
        self.get_logger().info(
            "wrist tracker ready: "
            f"depth={self._param('depth_topic')} mask={self._param('initial_mask_topic')} "
            f"tracked={self._param('tracked_pose_topic')}"
        )

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _on_depth(self, msg: Image) -> None:
        self._depth = msg

    def _on_info(self, msg: CameraInfo) -> None:
        self._info = msg

    def _on_mask(self, msg: Image) -> None:
        mask = image_to_numpy(msg) > 0
        self._mask = mask
        self._initial_center = None
        self._last_center = None
        self._invalid_count = 0
        self._status_pub.publish(String(data=f"TRACK_INIT mask_pixels={int(np.count_nonzero(mask))}"))

    def _tick(self) -> None:
        if self._depth is None or self._info is None or self._mask is None:
            return
        try:
            depth = image_to_numpy(self._depth)
            roi_mask = self._roi_mask(self._mask, depth.shape)
            points = masked_depth_to_points(depth, roi_mask, self._info)
            if points.shape[0] < int(self._param("min_points")):
                self._invalid_count += 1
                self._status_pub.publish(String(data=f"TRACK_LOST_SHORT reason=target_points_too_few:{points.shape[0]} invalid_count={self._invalid_count}"))
                return
            center = np.nanmedian(points, axis=0)
            if self._last_center is not None:
                step = float(np.linalg.norm(center - self._last_center))
                if step > float(self._param("max_step_m")):
                    self._invalid_count += 1
                    self._status_pub.publish(String(data=f"TRACK_WARN reason=jump step={step:.4f} invalid_count={self._invalid_count}"))
                    return
            if self._initial_center is None:
                self._initial_center = center.copy()
            self._last_center = center.copy()
            self._invalid_count = 0
            delta = float(np.linalg.norm(center - self._initial_center))
            if delta >= float(self._param("replan_delta_m")):
                stage = "REPLAN_REQUIRED"
            elif delta >= float(self._param("warn_delta_m")):
                stage = "TRACK_WARN"
            else:
                stage = "TRACK_OK"
            msg = pose_from_xyz(center, stamp=self._depth.header.stamp, frame_id=self._depth.header.frame_id)
            self._pose_pub.publish(msg)
            self._status_pub.publish(String(data=f"{stage} n_points={points.shape[0]} delta={delta:.4f} center=({center[0]:.4f},{center[1]:.4f},{center[2]:.4f})"))
        except Exception as exc:
            self._invalid_count += 1
            self._status_pub.publish(String(data=f"TRACK_ERROR reason={exc} invalid_count={self._invalid_count}"))

    def _roi_mask(self, mask: np.ndarray, depth_shape: tuple[int, ...]) -> np.ndarray:
        h, w = depth_shape[:2]
        if mask.shape[:2] != (h, w):
            return np.zeros((h, w), dtype=bool)
        bbox = bbox_from_mask(mask, expand_px=int(self._param("roi_expand_px")))
        if bbox is None:
            return np.zeros((h, w), dtype=bool)
        x1, y1, x2, y2 = bbox
        roi = np.zeros((h, w), dtype=bool)
        roi[y1:y2, x1:x2] = True
        return roi


def main() -> None:
    rclpy.init()
    node = WristTrackerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
