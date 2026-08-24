from __future__ import annotations

from collections import deque
import threading
import time
from pathlib import Path

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image, PointCloud2
from std_msgs.msg import String

from soarm100_interfaces.srv import SegmentTarget
from soarm100_vision.vision_utils import (
    color_components,
    dump_json,
    expand_mask_bbox,
    image_to_numpy,
    masked_depth_to_points,
    numpy_to_mask_msg,
    pointcloud2_xyz,
    pose_from_xyz,
    hsv_color_mask,
    parse_rgb,
)


def normalize_model_names(names) -> dict[int, str]:
    if isinstance(names, dict):
        return {int(class_id): str(name) for class_id, name in names.items()}
    return {class_id: str(name) for class_id, name in enumerate(names)}


def resolve_fixed_class_id(names, requested_class: str) -> tuple[int, str]:
    model_names = normalize_model_names(names)
    requested = str(requested_class).strip()
    if not requested:
        raise RuntimeError(
            "fixed_yolo_target_class_empty available="
            + ",".join(model_names.values())
        )
    matches = [
        (class_id, name)
        for class_id, name in model_names.items()
        if name.casefold() == requested.casefold()
    ]
    if not matches:
        raise RuntimeError(
            f"fixed_yolo_unknown_class:{requested} available="
            + ",".join(model_names.values())
        )
    return matches[0]


class TargetSegmenterNode(Node):
    """On-demand color, YOLO-World + SAM, or fixed YOLO + SAM segmentation.

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
        self.declare_parameter("expanded_mask_topic", "/target/mask_expanded")
        self.declare_parameter("synchronized_depth_topic", "")
        self.declare_parameter("target_cloud_topic", "/target/cloud")
        self.declare_parameter("target_roi_cloud_topic", "/target/cloud_roi")
        self.declare_parameter("target_center_topic", "/target/center")
        self.declare_parameter("status_topic", "/target/segmentation_status")
        self.declare_parameter("segment_service", "/segment_target")
        self.declare_parameter("yolo_model", "models/vision/yolov8s-world.pt")
        self.declare_parameter("fixed_yolo_model", "models/vision/yolowork_fixed_best.pt")
        self.declare_parameter("fixed_yolo_target_class", "")
        self.declare_parameter("fixed_yolo_conf", 0.01)
        self.declare_parameter("fixed_yolo_iou", 0.70)
        self.declare_parameter("fixed_yolo_imgsz", 640)
        self.declare_parameter("fixed_yolo_device", "auto")
        self.declare_parameter("sam_model", "models/vision/mobile_sam.pt")
        self.declare_parameter("debug_dir", "log/runtime/ros2_vision")
        self.declare_parameter("min_points", 30)
        self.declare_parameter("mask_expand_ratio", 0.05)
        self.declare_parameter("use_expanded_mask_for_target_cloud", False)
        self.declare_parameter("fallback_red_mask", True)
        self.declare_parameter("segmentation_mode", "color")
        self.declare_parameter("target_color_rgb", "255,0,0")
        self.declare_parameter("color_hue_tolerance_deg", 18.0)
        self.declare_parameter("color_saturation_min", 0.45)
        self.declare_parameter("color_value_min", 0.30)
        self.declare_parameter("color_min_area_px", 40)
        self.declare_parameter("auto_segment_hz", 0.0)
        self.declare_parameter("auto_target_prompt", "")
        self.declare_parameter("rgb_depth_sync_tolerance_s", 0.10)
        self.declare_parameter("rgb_depth_buffer_size", 60)

        self._rgb: Image | None = None
        self._depth: Image | None = None
        self._info: CameraInfo | None = None
        buffer_size = max(int(self._param("rgb_depth_buffer_size")), 2)
        self._rgb_buffer: deque[Image] = deque(maxlen=buffer_size)
        self._depth_buffer: deque[Image] = deque(maxlen=buffer_size)
        self._synced_bundle: tuple[Image, Image, CameraInfo, float] | None = None
        self._frame_lock = threading.Lock()
        self._detector = None
        self._sam = None
        self._detector_prompt = ""
        self._model_error = ""
        if str(self._param("segmentation_mode")).strip().lower() in (
            "yolo_sam",
            "fixed_yolo_sam",
        ):
            self._load_models()
            if self._model_error:
                self.get_logger().error(self._model_error)

        self._mask_pub = self.create_publisher(Image, self._param("mask_topic"), 1)
        self._expanded_mask_pub = self.create_publisher(Image, self._param("expanded_mask_topic"), 1)
        synced_depth_topic = str(self._param("synchronized_depth_topic")).strip()
        self._synced_depth_pub = (
            self.create_publisher(Image, synced_depth_topic, 1)
            if synced_depth_topic
            else None
        )
        self._cloud_pub = self.create_publisher(PointCloud2, self._param("target_cloud_topic"), 1)
        self._roi_cloud_pub = self.create_publisher(PointCloud2, self._param("target_roi_cloud_topic"), 1)
        self._center_pub = self.create_publisher(PoseStamped, self._param("target_center_topic"), 1)
        self._status_pub = self.create_publisher(String, self._param("status_topic"), 1)
        sensor_group = ReentrantCallbackGroup()
        inference_group = MutuallyExclusiveCallbackGroup()
        self.create_subscription(
            Image, self._param("rgb_topic"), self._on_rgb, qos_profile_sensor_data,
            callback_group=sensor_group,
        )
        self.create_subscription(
            Image, self._param("depth_topic"), self._on_depth, qos_profile_sensor_data,
            callback_group=sensor_group,
        )
        self.create_subscription(
            CameraInfo,
            self._param("camera_info_topic"),
            self._on_info,
            qos_profile_sensor_data,
            callback_group=sensor_group,
        )
        self.create_service(
            SegmentTarget, str(self._param("segment_service")), self._on_segment,
            callback_group=inference_group,
        )
        auto_hz = float(self._param("auto_segment_hz"))
        if auto_hz > 0.0:
            self.create_timer(
                1.0 / auto_hz, self._auto_segment, callback_group=inference_group
            )
        self.get_logger().info(
            "target segmenter ready: "
            f"mode={self._param('segmentation_mode')} "
            f"color={self._param('target_color_rgb')} "
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
            mode = str(self._param("segmentation_mode")).strip().lower()
            detector_path = (
                self._param("fixed_yolo_model")
                if mode == "fixed_yolo_sam"
                else self._param("yolo_model")
            )
            self._detector = YOLO(str(detector_path))
            self._sam = SAM(str(self._param("sam_model")))
            if mode == "fixed_yolo_sam":
                names = normalize_model_names(self._detector.names)
                self.get_logger().info(
                    "fixed_yolo classes=" + ",".join(names.values())
                )
        except Exception as exc:
            self._model_error = f"model load failed: {exc}"

    def _on_rgb(self, msg: Image) -> None:
        with self._frame_lock:
            self._rgb = msg
            self._rgb_buffer.append(msg)
            self._update_synced_bundle_locked()

    def _on_depth(self, msg: Image) -> None:
        with self._frame_lock:
            self._depth = msg
            self._depth_buffer.append(msg)
            self._update_synced_bundle_locked()

    def _on_info(self, msg: CameraInfo) -> None:
        with self._frame_lock:
            self._info = msg
            self._update_synced_bundle_locked()

    @staticmethod
    def _stamp_s(msg) -> float:
        return float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1.0e-9

    def _update_synced_bundle_locked(self) -> None:
        if not self._rgb_buffer or not self._depth_buffer or self._info is None:
            return
        depth = self._depth_buffer[-1]
        depth_stamp = self._stamp_s(depth)
        rgb = min(
            self._rgb_buffer,
            key=lambda candidate: abs(self._stamp_s(candidate) - depth_stamp),
        )
        sync_delta = abs(self._stamp_s(rgb) - depth_stamp)
        if sync_delta <= float(self._param("rgb_depth_sync_tolerance_s")):
            self._synced_bundle = (rgb, depth, self._info, sync_delta)

    def _auto_segment(self) -> None:
        request = SegmentTarget.Request()
        request.target_prompt = str(self._param("auto_target_prompt"))
        request.force_yolo = True
        response = self._on_segment(request, SegmentTarget.Response())
        if not response.success:
            self._status_pub.publish(String(data=f"failed reason={response.reason}"))
            self.get_logger().warning(
                f"automatic target segmentation failed: {response.reason}",
                throttle_duration_sec=1.0,
            )

    def _on_segment(self, request: SegmentTarget.Request, response: SegmentTarget.Response):
        with self._frame_lock:
            bundle = self._synced_bundle
        if bundle is None:
            response.success = False
            response.reason = "waiting_for_synchronized_rgb_depth_camera_info"
            return response
        rgb_msg, depth_msg, info_msg, sync_delta_s = bundle
        mode = str(self._param("segmentation_mode")).strip().lower()
        if mode in ("yolo_sam", "fixed_yolo_sam") and (
            self._detector is None or self._sam is None
        ):
            response.success = False
            response.reason = self._model_error or "models_not_loaded"
            return response

        try:
            inference_started = time.perf_counter()
            rgb = image_to_numpy(rgb_msg)
            depth = image_to_numpy(depth_msg)
            used_fallback = False
            selected_class = ""
            if mode == "color":
                mask, bbox, score = self._color_mask(rgb)
            elif mode == "yolo_sam":
                try:
                    bbox, score = self._detect_bbox(rgb, request.target_prompt)
                    mask = self._segment_mask(rgb, bbox)
                except RuntimeError as exc:
                    if (
                        not bool(self._param("fallback_red_mask"))
                        or "no_yolo_detection" not in str(exc)
                    ):
                        raise
                    mask, bbox, score = self._fallback_red_mask(rgb)
                    used_fallback = True
            elif mode == "fixed_yolo_sam":
                requested_class = str(self._param("fixed_yolo_target_class")).strip()
                if not requested_class:
                    requested_class = request.target_prompt
                bbox, score, selected_class = self._detect_fixed_bbox(
                    rgb, requested_class
                )
                mask = self._segment_mask(rgb, bbox)
            else:
                raise RuntimeError(f"unsupported_segmentation_mode:{mode}")
            expanded_mask = expand_mask_bbox(mask, float(self._param("mask_expand_ratio")))
            cloud_mask = expanded_mask if bool(self._param("use_expanded_mask_for_target_cloud")) else mask
            points = masked_depth_to_points(depth, cloud_mask, info_msg)
            roi_points = masked_depth_to_points(depth, expanded_mask, info_msg)
            if points.shape[0] < int(self._param("min_points")):
                response.success = False
                response.reason = f"target_points_too_few:{points.shape[0]}"
                return response
            center = np.nanmedian(points, axis=0)
            # The mask is consumed together with depth, so bind it to the
            # synchronized depth frame rather than the inference finish time.
            stamp = depth_msg.header.stamp
            frame_id = rgb_msg.header.frame_id
            mask_msg = numpy_to_mask_msg(mask, stamp=stamp, frame_id=frame_id)
            expanded_mask_msg = numpy_to_mask_msg(expanded_mask, stamp=stamp, frame_id=frame_id)
            cloud_msg = pointcloud2_xyz(points, stamp=stamp, frame_id=frame_id)
            roi_cloud_msg = pointcloud2_xyz(roi_points, stamp=stamp, frame_id=frame_id)
            center_msg = pose_from_xyz(center, stamp=stamp, frame_id=frame_id)
            self._mask_pub.publish(mask_msg)
            if self._synced_depth_pub is not None:
                self._synced_depth_pub.publish(depth_msg)
            self._expanded_mask_pub.publish(expanded_mask_msg)
            self._cloud_pub.publish(cloud_msg)
            self._roi_cloud_pub.publish(roi_cloud_msg)
            self._center_pub.publish(center_msg)

            debug_path = Path(str(self._param("debug_dir"))) / "segment_target_latest.json"
            debug_json = dump_json(
                debug_path,
                {
                    "ok": True,
                    "target_prompt": request.target_prompt,
                    "segmentation_mode": mode,
                    "target_color_rgb": str(self._param("target_color_rgb")),
                    "selected_class": selected_class,
                    "bbox_xyxy": [float(x) for x in bbox],
                    "score": float(score),
                    "fallback_red_mask": bool(used_fallback),
                    "mask_pixels": int(np.count_nonzero(mask)),
                    "expanded_mask_pixels": int(np.count_nonzero(expanded_mask)),
                    "mask_expand_ratio": float(self._param("mask_expand_ratio")),
                    "use_expanded_mask_for_target_cloud": bool(self._param("use_expanded_mask_for_target_cloud")),
                    "n_points": int(points.shape[0]),
                    "n_roi_points": int(roi_points.shape[0]),
                    "center_camera": [float(x) for x in center],
                    "rgb_depth_sync_delta_s": float(sync_delta_s),
                    "inference_latency_s": float(time.perf_counter() - inference_started),
                    "stamp_s": float(time.time()),
                },
            )
            response.success = True
            response.reason = f"ok mode={mode}"
            response.target_center = center_msg
            response.score = float(score)
            response.bbox_xyxy = [float(x) for x in bbox]
            response.mask_topic = str(self._param("mask_topic"))
            response.debug_json = debug_json
            self._status_pub.publish(
                String(
                    data=(
                        f"ok mode={mode} prompt={request.target_prompt} points={points.shape[0]} "
                        f"class={selected_class or '-'} "
                        f"bbox={','.join(f'{float(x):.1f}' for x in bbox)} "
                        f"roi_points={roi_points.shape[0]} mask_px={int(np.count_nonzero(mask))} "
                        f"expanded_px={int(np.count_nonzero(expanded_mask))} score={score:.3f} "
                        f"fallback_red={used_fallback} sync_dt={sync_delta_s:.4f}s "
                        f"inference_s={time.perf_counter() - inference_started:.3f}"
                    )
                )
            )
        except Exception as exc:
            response.success = False
            response.reason = f"segment_failed:{exc}"
        return response

    def _detect_bbox(self, rgb: np.ndarray, prompt: str) -> tuple[np.ndarray, float]:
        normalized_prompt = str(prompt).strip()
        if hasattr(self._detector, "set_classes") and normalized_prompt != self._detector_prompt:
            self._detector.set_classes([normalized_prompt])
            self._detector_prompt = normalized_prompt
        result = self._detector.predict(self._ultralytics_image(rgb), verbose=False)[0]
        boxes = getattr(result, "boxes", None)
        if boxes is None or len(boxes) == 0:
            raise RuntimeError("no_yolo_detection")
        xyxy = boxes.xyxy.detach().cpu().numpy()
        conf = boxes.conf.detach().cpu().numpy() if getattr(boxes, "conf", None) is not None else np.ones(len(xyxy))
        idx = int(np.argmax(conf))
        return xyxy[idx].astype(np.float32), float(conf[idx])

    def _detect_fixed_bbox(
        self, rgb: np.ndarray, requested_class: str
    ) -> tuple[np.ndarray, float, str]:
        class_id, class_name = resolve_fixed_class_id(
            self._detector.names, requested_class
        )
        kwargs = {
            "conf": float(self._param("fixed_yolo_conf")),
            "iou": float(self._param("fixed_yolo_iou")),
            "imgsz": int(self._param("fixed_yolo_imgsz")),
            "classes": [class_id],
            "verbose": False,
        }
        device = str(self._param("fixed_yolo_device")).strip()
        if device and device.lower() != "auto":
            kwargs["device"] = device
        result = self._detector.predict(self._ultralytics_image(rgb), **kwargs)[0]
        boxes = getattr(result, "boxes", None)
        if boxes is None or len(boxes) == 0:
            raise RuntimeError(f"no_fixed_yolo_detection:{class_name}")
        xyxy = boxes.xyxy.detach().cpu().numpy()
        conf = (
            boxes.conf.detach().cpu().numpy()
            if getattr(boxes, "conf", None) is not None
            else np.ones(len(xyxy), dtype=np.float32)
        )
        index = int(np.argmax(conf))
        return xyxy[index].astype(np.float32), float(conf[index]), class_name

    def _segment_mask(self, rgb: np.ndarray, bbox: np.ndarray) -> np.ndarray:
        result = self._sam.predict(
            self._ultralytics_image(rgb),
            bboxes=np.asarray([bbox], dtype=np.float32),
            verbose=False,
        )[0]
        masks = getattr(result, "masks", None)
        if masks is None or masks.data is None or len(masks.data) == 0:
            raise RuntimeError("no_sam_mask")
        mask = masks.data[0].detach().cpu().numpy() > 0.5
        return np.asarray(mask, dtype=bool)

    @staticmethod
    def _ultralytics_image(rgb: np.ndarray) -> np.ndarray:
        # Ultralytics treats NumPy inputs as OpenCV BGR images.
        return np.ascontiguousarray(np.asarray(rgb, dtype=np.uint8)[..., ::-1])

    def _fallback_red_mask(self, rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
        arr = np.asarray(rgb, dtype=np.uint8)
        r = arr[..., 0].astype(np.int16)
        g = arr[..., 1].astype(np.int16)
        b = arr[..., 2].astype(np.int16)
        mask = (r > 120) & (r > g + 45) & (r > b + 45)
        ys, xs = np.nonzero(mask)
        if xs.size == 0:
            raise RuntimeError("no_yolo_detection_and_no_red_mask")
        x0 = int(xs.min())
        x1 = int(xs.max())
        y0 = int(ys.min())
        y1 = int(ys.max())
        if (x1 - x0 + 1) * (y1 - y0 + 1) < int(self._param("min_points")):
            raise RuntimeError(f"red_mask_too_small:{xs.size}")
        bbox = np.array([x0, y0, x1, y1], dtype=np.float32)
        return np.asarray(mask, dtype=bool), bbox, 0.50

    def _color_mask(self, rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
        mask = hsv_color_mask(
            rgb,
            target_rgb=parse_rgb(str(self._param("target_color_rgb"))),
            hue_tolerance_deg=float(self._param("color_hue_tolerance_deg")),
            saturation_min=float(self._param("color_saturation_min")),
            value_min=float(self._param("color_value_min")),
        )
        components = color_components(
            mask, min_area=int(self._param("color_min_area_px"))
        )
        if not components:
            raise RuntimeError("no_target_color_component")
        selected = components[0]
        x1, y1, x2, y2 = selected["bbox"]
        selected_mask = np.zeros_like(mask, dtype=bool)
        selected_mask[y1:y2, x1:x2] = mask[y1:y2, x1:x2]
        bbox = np.asarray([x1, y1, x2 - 1, y2 - 1], dtype=np.float32)
        score = min(1.0, float(selected["area"]) / max((x2 - x1) * (y2 - y1), 1))
        return selected_mask, bbox, score


def main() -> None:
    rclpy.init()
    node = TargetSegmenterNode()
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
