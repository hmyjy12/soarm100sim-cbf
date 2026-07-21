from __future__ import annotations

import time

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from soarm100_vision.vision_utils import image_to_numpy, numpy_rgb_to_msg


class DebugViewerNode(Node):
    """OpenCV preview for segmentation/tracking debug.

    The node publishes an overlay image even when the local OpenCV window is
    disabled or unavailable. Use rqt_image_view on /debug/target_overlay when
    running headless.
    """

    def __init__(self) -> None:
        super().__init__("soarm100_debug_viewer")
        self.declare_parameter("rgb_topic", "/camera/color/image_raw")
        self.declare_parameter("mask_topic", "/target/mask")
        self.declare_parameter("segmentation_status_topic", "/target/segmentation_status")
        self.declare_parameter("tracking_status_topic", "/target/tracking_status")
        self.declare_parameter("overlay_topic", "/debug/target_overlay")
        self.declare_parameter("show_window", True)
        self.declare_parameter("window_name", "SO-ARM100 vision")
        self.declare_parameter("max_fps", 15.0)

        self._rgb_msg: Image | None = None
        self._mask_msg: Image | None = None
        self._seg_status = ""
        self._track_status = ""
        self._last_draw_t = 0.0
        self._cv2 = None
        self._window_ok = False
        self._show_window = bool(self.get_parameter("show_window").value)
        if self._show_window:
            self._init_window()

        self._overlay_pub = self.create_publisher(Image, self.get_parameter("overlay_topic").value, 1)
        self.create_subscription(Image, self.get_parameter("rgb_topic").value, self._on_rgb, 1)
        self.create_subscription(Image, self.get_parameter("mask_topic").value, self._on_mask, 1)
        self.create_subscription(String, self.get_parameter("segmentation_status_topic").value, self._on_seg_status, 10)
        self.create_subscription(String, self.get_parameter("tracking_status_topic").value, self._on_track_status, 10)
        self.create_timer(1.0 / max(1.0, float(self.get_parameter("max_fps").value)), self._tick)
        self.get_logger().info(
            "debug viewer ready: "
            f"rgb={self.get_parameter('rgb_topic').value} mask={self.get_parameter('mask_topic').value} "
            f"overlay={self.get_parameter('overlay_topic').value} show_window={self._show_window}"
        )

    def _init_window(self) -> None:
        try:
            import cv2

            self._cv2 = cv2
            cv2.namedWindow(str(self.get_parameter("window_name").value), cv2.WINDOW_NORMAL)
            self._window_ok = True
        except Exception as exc:
            self._window_ok = False
            self.get_logger().warn(f"OpenCV window unavailable; overlay topic still active: {exc}")

    def _on_rgb(self, msg: Image) -> None:
        self._rgb_msg = msg

    def _on_mask(self, msg: Image) -> None:
        self._mask_msg = msg

    def _on_seg_status(self, msg: String) -> None:
        self._seg_status = msg.data

    def _on_track_status(self, msg: String) -> None:
        self._track_status = msg.data

    def _tick(self) -> None:
        if self._rgb_msg is None:
            return
        now = time.time()
        min_dt = 1.0 / max(1.0, float(self.get_parameter("max_fps").value))
        if now - self._last_draw_t < min_dt:
            return
        self._last_draw_t = now
        try:
            overlay = self._make_overlay()
            self._overlay_pub.publish(
                numpy_rgb_to_msg(overlay, stamp=self._rgb_msg.header.stamp, frame_id=self._rgb_msg.header.frame_id)
            )
            if self._window_ok and self._cv2 is not None:
                bgr = overlay[..., ::-1]
                self._cv2.imshow(str(self.get_parameter("window_name").value), bgr)
                self._cv2.waitKey(1)
        except Exception as exc:
            self.get_logger().warn(f"debug overlay failed: {exc}")

    def _make_overlay(self) -> np.ndarray:
        rgb = image_to_numpy(self._rgb_msg)
        out = np.asarray(rgb, dtype=np.uint8).copy()
        if self._mask_msg is not None:
            mask = image_to_numpy(self._mask_msg) > 0
            if mask.shape[:2] == out.shape[:2]:
                color = np.zeros_like(out)
                color[..., 0] = 255
                out = np.where(mask[..., None], (0.55 * out + 0.45 * color).astype(np.uint8), out)
                ys, xs = np.nonzero(mask)
                if xs.size > 0:
                    x1, x2 = int(xs.min()), int(xs.max())
                    y1, y2 = int(ys.min()), int(ys.max())
                    out[y1 : y1 + 2, x1:x2 + 1] = (255, 255, 0)
                    out[y2 : y2 + 2, x1:x2 + 1] = (255, 255, 0)
                    out[y1:y2 + 1, x1 : x1 + 2] = (255, 255, 0)
                    out[y1:y2 + 1, x2 : x2 + 2] = (255, 255, 0)
        if self._cv2 is not None:
            lines = [
                f"seg: {self._seg_status[:90]}",
                f"track: {self._track_status[:90]}",
            ]
            y = 24
            for line in lines:
                self._cv2.putText(out, line, (10, y), self._cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 3)
                self._cv2.putText(out, line, (10, y), self._cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1)
                y += 24
        return out


def main() -> None:
    rclpy.init()
    node = DebugViewerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
