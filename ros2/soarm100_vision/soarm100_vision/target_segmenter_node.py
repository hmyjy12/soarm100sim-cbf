from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image, PointCloud2
from std_msgs.msg import String

from soarm100_interfaces.srv import SegmentTarget
from soarm100_vision.vision_utils import (
    dump_json,
    image_to_numpy,
    masked_depth_to_points,
    numpy_to_mask_msg,
    pointcloud2_xyz,
    pose_from_xyz,
)


class TargetSegmenterNode(Node):
    """On-demand YOLO-World + SAM target segmentation.

    This node is intentionally service-triggered. Heavy open-vocabulary
    detection and SAM segmentation should run at task start or replan time,
    while wrist tracking handles high-frequency local motion.
    """

    def __init__(self) -> None:
        super().__init__("soarm100_target_segmenter")
        self.declare_parameter("rgb_topic", "/camera/color/image_raw")
        self.declare_parameter("depth_topic", "/camera/depth/image_rect_raw")
        self.declare_parameter("camera_info_topic", "/camera/color/camera_info")
        self.declare_parameter("mask_topic", "/target/mask")
        self.declare_parameter("target_cloud_topic", "/target/cloud")
        self.declare_parameter("target_center_topic", "/target/center")
        self.declare_parameter("status_topic", "/target/segmentation_status")
        self.declare_parameter("yolo_model", "models/vision/yolov8s-world.pt")
        self.declare_parameter("sam_model", "models/vision/mobile_sam.pt")
        self.declare_parameter("debug_dir", "logs/ros2_vision")
        self.declare_parameter("min_points", 30)
        self.declare_parameter("bbox_expand_ratio", 0.10)

        self._rgb: Image | None = None
        self._depth: Image | None = None
        self._info: CameraInfo | None = None
        self._detector = None
        self._sam = None
        self._model_error = ""
        self._load_models()

        self._mask_pub = self.create_publisher(Image, self._param("mask_topic"), 1)
        self._cloud_pub = self.create_publisher(PointCloud2, self._param("target_cloud_topic"), 1)
        self._center_pub = self.create_publisher(PoseStamped, self._param("target_center_topic"), 1)
        self._status_pub = self.create_publisher(String, self._param("status_topic"), 1)
        self.create_subscription(Image, self._param("rgb_topic"), self._on_rgb, 1)
        self.create_subscription(Image, self._param("depth_topic"), self._on_depth, 1)
        self.create_subscription(CameraInfo, self._param("camera_info_topic"), self._on_info, 10)
        self.create_service(SegmentTarget, "segment_target", self._on_segment)
        self.get_logger().info(
            "target segmenter ready: "
            f"rgb={self._param('rgb_topic')} depth={self._param('depth_topic')} "
            f"mask={self._param('mask_topic')} cloud={self._param('target_cloud_topic')}"
        )

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _load_models(self) -> None:
        try:
            from ultralytics import SAM, YOLO
        except Exception as exc:
            self._model_error = f"ultralytics unavailable: {exc}"
            return
        try:
            self._detector = YOLO(str(self._param("yolo_model")))
            self._sam = SAM(str(self._param("sam_model")))
        except Exception as exc:
            self._model_error = f"model load failed: {exc}"

    def _on_rgb(self, msg: Image) -> None:
        self._rgb = msg

    def _on_depth(self, msg: Image) -> None:
        self._depth = msg

    def _on_info(self, msg: CameraInfo) -> None:
        self._info = msg

    def _on_segment(self, request: SegmentTarget.Request, response: SegmentTarget.Response):
        if self._rgb is None or self._depth is None or self._info is None:
            response.success = False
            response.reason = "waiting_for_rgb_depth_camera_info"
            return response
        if self._detector is None or self._sam is None:
            response.success = False
            response.reason = self._model_error or "models_not_loaded"
            return response

        try:
            rgb = image_to_numpy(self._rgb)
            depth = image_to_numpy(self._depth)
            bbox, score = self._detect_bbox(rgb, request.target_prompt)
            mask = self._segment_mask(rgb, bbox)
            points = masked_depth_to_points(depth, mask, self._info)
            if points.shape[0] < int(self._param("min_points")):
                response.success = False
                response.reason = f"target_points_too_few:{points.shape[0]}"
                return response
            center = np.nanmedian(points, axis=0)
            stamp = self._rgb.header.stamp
            frame_id = self._rgb.header.frame_id
            mask_msg = numpy_to_mask_msg(mask, stamp=stamp, frame_id=frame_id)
            cloud_msg = pointcloud2_xyz(points, stamp=stamp, frame_id=frame_id)
            center_msg = pose_from_xyz(center, stamp=stamp, frame_id=frame_id)
            self._mask_pub.publish(mask_msg)
            self._cloud_pub.publish(cloud_msg)
            self._center_pub.publish(center_msg)

            debug_path = Path(str(self._param("debug_dir"))) / "segment_target_latest.json"
            debug_json = dump_json(
                debug_path,
                {
                    "ok": True,
                    "target_prompt": request.target_prompt,
                    "bbox_xyxy": [float(x) for x in bbox],
                    "score": float(score),
                    "n_points": int(points.shape[0]),
                    "center_camera": [float(x) for x in center],
                    "stamp_s": float(time.time()),
                },
            )
            response.success = True
            response.reason = "ok"
            response.target_center = center_msg
            response.score = float(score)
            response.bbox_xyxy = [float(x) for x in bbox]
            response.mask_topic = str(self._param("mask_topic"))
            response.debug_json = debug_json
            self._status_pub.publish(String(data=f"ok prompt={request.target_prompt} points={points.shape[0]} score={score:.3f}"))
        except Exception as exc:
            response.success = False
            response.reason = f"segment_failed:{exc}"
        return response

    def _detect_bbox(self, rgb: np.ndarray, prompt: str) -> tuple[np.ndarray, float]:
        if hasattr(self._detector, "set_classes"):
            self._detector.set_classes([str(prompt)])
        result = self._detector.predict(rgb, verbose=False)[0]
        boxes = getattr(result, "boxes", None)
        if boxes is None or len(boxes) == 0:
            raise RuntimeError("no_yolo_detection")
        xyxy = boxes.xyxy.detach().cpu().numpy()
        conf = boxes.conf.detach().cpu().numpy() if getattr(boxes, "conf", None) is not None else np.ones(len(xyxy))
        idx = int(np.argmax(conf))
        return xyxy[idx].astype(np.float32), float(conf[idx])

    def _segment_mask(self, rgb: np.ndarray, bbox: np.ndarray) -> np.ndarray:
        result = self._sam.predict(rgb, bboxes=np.asarray([bbox], dtype=np.float32), verbose=False)[0]
        masks = getattr(result, "masks", None)
        if masks is None or masks.data is None or len(masks.data) == 0:
            raise RuntimeError("no_sam_mask")
        mask = masks.data[0].detach().cpu().numpy() > 0.5
        return np.asarray(mask, dtype=bool)


def main() -> None:
    rclpy.init()
    node = TargetSegmenterNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
