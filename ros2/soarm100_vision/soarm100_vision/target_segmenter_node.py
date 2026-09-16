from __future__ import annotations

from collections import deque
import threading
import time
from pathlib import Path

import cv2
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

        self._rgb: tuple[Image, float] | None = None
        self._depth: tuple[Image, float] | None = None
        self._info: CameraInfo | None = None
        buffer_size = max(int(self._param("rgb_depth_buffer_size")), 2)
        self._rgb_buffer: deque[tuple[Image, float]] = deque(maxlen=buffer_size)
        self._depth_buffer: deque[tuple[Image, float]] = deque(maxlen=buffer_size)
        self._rgb_count = 0
        self._depth_count = 0
        self._info_count = 0
        self._selected_mask_publish_count = 0
        self._synced_bundle: tuple[
            Image, Image, CameraInfo, float, float, float, int, int
        ] | None = None
        self._frame_lock = threading.Lock()
        self._inference_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._auto_thread: threading.Thread | None = None
        self._last_auto_segment_depth_stamp_s = -1.0
        self._last_successful_segment_depth_stamp_s = -1.0
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
            self._auto_thread = threading.Thread(
                target=self._auto_loop,
                args=(auto_hz,),
                daemon=True,
            )
            self._auto_thread.start()
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
        received_wall_s = time.time()
        with self._frame_lock:
            self._rgb_count += 1
            self._rgb = (msg, received_wall_s)
            self._rgb_buffer.append((msg, received_wall_s))
            self._update_synced_bundle_locked()

    def _on_depth(self, msg: Image) -> None:
        received_wall_s = time.time()
        with self._frame_lock:
            self._depth_count += 1
            self._depth = (msg, received_wall_s)
            self._depth_buffer.append((msg, received_wall_s))
            self._update_synced_bundle_locked()

    def _on_info(self, msg: CameraInfo) -> None:
        with self._frame_lock:
            self._info_count += 1
            self._info = msg
            self._update_synced_bundle_locked()

    @staticmethod
    def _stamp_s(msg) -> float:
        return float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1.0e-9

    def _sync_debug_locked(self) -> dict[str, float | int]:
        now = time.time()
        latest_rgb_stamp_s = self._stamp_s(self._rgb[0]) if self._rgb else -1.0
        latest_depth_stamp_s = self._stamp_s(self._depth[0]) if self._depth else -1.0
        latest_rgb_age_s = now - self._rgb[1] if self._rgb else -1.0
        latest_depth_age_s = now - self._depth[1] if self._depth else -1.0
        best_delta_s = -1.0
        if self._rgb_buffer and self._depth_buffer:
            best_delta_s = min(
                abs(self._stamp_s(rgb[0]) - self._stamp_s(depth[0]))
                for rgb in self._rgb_buffer
                for depth in self._depth_buffer
            )
        return {
            "rgb_count": int(self._rgb_count),
            "depth_count": int(self._depth_count),
            "info_count": int(self._info_count),
            "rgb_queue_size": int(len(self._rgb_buffer)),
            "depth_queue_size": int(len(self._depth_buffer)),
            "latest_rgb_stamp_s": float(latest_rgb_stamp_s),
            "latest_depth_stamp_s": float(latest_depth_stamp_s),
            "latest_rgb_age_s": float(latest_rgb_age_s),
            "latest_depth_age_s": float(latest_depth_age_s),
            "best_delta_s": float(best_delta_s),
        }

    @staticmethod
    def _format_sync_debug(debug: dict[str, float | int]) -> str:
        return (
            f"counts={debug['rgb_count']},{debug['depth_count']},{debug['info_count']} "
            f"queues={debug['rgb_queue_size']},{debug['depth_queue_size']} "
            f"latest_rgb_stamp={debug['latest_rgb_stamp_s']:.6f} "
            f"latest_depth_stamp={debug['latest_depth_stamp_s']:.6f} "
            f"latest_rgb_age={debug['latest_rgb_age_s']:.3f}s "
            f"latest_depth_age={debug['latest_depth_age_s']:.3f}s "
            f"best_dt={debug['best_delta_s']:.6f}s"
        )

    def _update_synced_bundle_locked(self) -> None:
        if not self._rgb_buffer or not self._depth_buffer or self._info is None:
            return
        tolerance_s = float(self._param("rgb_depth_sync_tolerance_s"))
        for depth, depth_received_wall_s in reversed(self._depth_buffer):
            depth_stamp = self._stamp_s(depth)
            rgb, rgb_received_wall_s = min(
                self._rgb_buffer,
                key=lambda candidate: abs(self._stamp_s(candidate[0]) - depth_stamp),
            )
            sync_delta = abs(self._stamp_s(rgb) - depth_stamp)
            if sync_delta > tolerance_s:
                continue
            self._synced_bundle = (
                rgb,
                depth,
                self._info,
                sync_delta,
                rgb_received_wall_s,
                depth_received_wall_s,
                len(self._rgb_buffer),
                len(self._depth_buffer),
            )
            return
        self._synced_bundle = None

    def _auto_loop(self, auto_hz: float) -> None:
        period = 1.0 / max(float(auto_hz), 1.0e-3)
        next_start = time.monotonic()
        while not self._stop_event.is_set():
            now = time.monotonic()
            if now < next_start:
                self._stop_event.wait(next_start - now)
                continue
            self._auto_segment()
            # Heavy YOLO/SAM inference can overrun the requested period. Do
            # not catch up with back-to-back inference; leave executor threads
            # time to run image subscription callbacks and refresh snapshots.
            next_start = time.monotonic() + period

    def _auto_segment(self) -> None:
        depth_stamp_s = -1.0
        with self._frame_lock:
            bundle = self._synced_bundle
            if bundle is not None:
                depth_stamp_s = self._stamp_s(bundle[1])
                if depth_stamp_s <= self._last_auto_segment_depth_stamp_s:
                    debug = self._sync_debug_locked()
                    reason = (
                        "waiting_for_new_rgb_depth_pair:"
                        f"last_depth_stamp={depth_stamp_s:.6f} "
                        f"last_processed_depth_stamp="
                        f"{self._last_auto_segment_depth_stamp_s:.6f} "
                        + self._format_sync_debug(debug)
                    )
                    self._status_pub.publish(String(data=f"failed reason={reason}"))
                    self.get_logger().warning(
                        f"automatic target segmentation failed: {reason}",
                        throttle_duration_sec=1.0,
                    )
                    return
        request = SegmentTarget.Request()
        request.target_prompt = str(self._param("auto_target_prompt"))
        request.force_yolo = True
        response = self._on_segment(request, SegmentTarget.Response())
        if response.success:
            self._last_auto_segment_depth_stamp_s = (
                self._last_successful_segment_depth_stamp_s
            )
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
                if not self._rgb_buffer:
                    wait_reason = "waiting_for_rgb"
                elif not self._depth_buffer:
                    wait_reason = "waiting_for_depth"
                elif self._info is None:
                    wait_reason = "waiting_for_camera_info"
                else:
                    debug = self._sync_debug_locked()
                    wait_reason = (
                        "waiting_for_rgb_depth_sync:"
                        f"tolerance={float(self._param('rgb_depth_sync_tolerance_s')):.6f}s:"
                        + self._format_sync_debug(debug)
                    )
        if bundle is None:
            response.success = False
            response.reason = wait_reason
            return response
        (
            rgb_msg,
            depth_msg,
            info_msg,
            sync_delta_s,
            rgb_received_wall_s,
            depth_received_wall_s,
            rgb_queue_size,
            depth_queue_size,
        ) = bundle
        mode = str(self._param("segmentation_mode")).strip().lower()
        if mode in ("yolo_sam", "fixed_yolo_sam") and (
            self._detector is None or self._sam is None
        ):
            response.success = False
            response.reason = self._model_error or "models_not_loaded"
            return response

        try:
            inference_start_wall_s = time.time()
            inference_started = time.perf_counter()
            yolo_latency_s = 0.0
            sam_latency_s = 0.0
            with self._inference_lock:
                rgb = image_to_numpy(rgb_msg)
                depth = image_to_numpy(depth_msg)
                used_fallback = False
                selected_class = ""
                if mode == "color":
                    mask, bbox, score = self._color_mask(rgb)
                elif mode == "yolo_sam":
                    try:
                        yolo_start = time.perf_counter()
                        bbox, score = self._detect_bbox(rgb, request.target_prompt)
                        yolo_latency_s = time.perf_counter() - yolo_start
                        sam_start = time.perf_counter()
                        mask = self._segment_mask(rgb, bbox)
                        sam_latency_s = time.perf_counter() - sam_start
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
                    yolo_start = time.perf_counter()
                    bbox, score, selected_class = self._detect_fixed_bbox(
                        rgb, requested_class
                    )
                    yolo_latency_s = time.perf_counter() - yolo_start
                    sam_start = time.perf_counter()
                    mask = self._segment_mask(rgb, bbox)
                    sam_latency_s = time.perf_counter() - sam_start
                else:
                    raise RuntimeError(f"unsupported_segmentation_mode:{mode}")
            expanded_mask = expand_mask_bbox(mask, float(self._param("mask_expand_ratio")))

            depth_h, depth_w = depth.shape[:2]

            if mask.shape[:2] != (depth_h, depth_w):
                mask = cv2.resize(
                    mask.astype(np.uint8),
                    (depth_w, depth_h),
                    interpolation=cv2.INTER_NEAREST,
                ).astype(bool)

            if expanded_mask.shape[:2] != (depth_h, depth_w):
                expanded_mask = cv2.resize(
                    expanded_mask.astype(np.uint8),
                    (depth_w, depth_h),
                    interpolation=cv2.INTER_NEAREST,
                ).astype(bool)

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
            selected_mask_publish_stamp_s = self._stamp_s(depth_msg)
            frame_id = rgb_msg.header.frame_id
            mask_msg = numpy_to_mask_msg(mask, stamp=stamp, frame_id=frame_id)
            expanded_mask_msg = numpy_to_mask_msg(expanded_mask, stamp=stamp, frame_id=frame_id)
            cloud_msg = pointcloud2_xyz(points, stamp=stamp, frame_id=frame_id)
            roi_cloud_msg = pointcloud2_xyz(roi_points, stamp=stamp, frame_id=frame_id)
            center_msg = pose_from_xyz(center, stamp=stamp, frame_id=frame_id)
            self._mask_pub.publish(mask_msg)
            self._selected_mask_publish_count += 1
            publish_wall_s = time.time()
            self.get_logger().info(
                "selected_mask publish invoked: "
                f"publish_count={self._selected_mask_publish_count} "
                f"stamp={self._stamp_s(mask_msg):.9f} "
                f"frame_id={mask_msg.header.frame_id!r} "
                f"width={mask_msg.width} height={mask_msg.height} "
                f"encoding={mask_msg.encoding!r} "
                f"mask_pixels={int(np.count_nonzero(mask))} "
                f"publish_wall={publish_wall_s:.6f}",
            )
            if self._synced_depth_pub is not None:
                self._synced_depth_pub.publish(depth_msg)
            self._expanded_mask_pub.publish(expanded_mask_msg)
            self._cloud_pub.publish(cloud_msg)
            self._roi_cloud_pub.publish(roi_cloud_msg)
            self._center_pub.publish(center_msg)

            debug_path = Path(str(self._param("debug_dir"))) / "segment_target_latest.json"
            inference_end_wall_s = time.time()
            inference_latency_s = time.perf_counter() - inference_started
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
                    "rgb_msg_stamp_s": float(self._stamp_s(rgb_msg)),
                    "depth_msg_stamp_s": float(self._stamp_s(depth_msg)),
                    "rgb_depth_sync_delta_s": float(sync_delta_s),
                    "rgb_wall_receive_age_s": float(
                        inference_start_wall_s - rgb_received_wall_s
                    ),
                    "depth_wall_receive_age_s": float(
                        inference_start_wall_s - depth_received_wall_s
                    ),
                    "rgb_queue_size": int(rgb_queue_size),
                    "depth_queue_size": int(depth_queue_size),
                    "inference_start_wall_s": float(inference_start_wall_s),
                    "inference_end_wall_s": float(inference_end_wall_s),
                    "yolo_latency_s": float(yolo_latency_s),
                    "sam_latency_s": float(sam_latency_s),
                    "inference_latency_s": float(inference_latency_s),
                    "selected_mask_publish_stamp_s": float(
                        selected_mask_publish_stamp_s
                    ),
                    "selected_mask_publish_count": int(
                        self._selected_mask_publish_count
                    ),
                    "stamp_s": float(time.time()),
                },
            )
            self._last_successful_segment_depth_stamp_s = float(
                selected_mask_publish_stamp_s
            )
            response.success = True
            response.reason = f"ok mode={mode}"
            response.target_center = center_msg
            response.score = float(score)
            response.bbox_xyxy = [float(x) for x in bbox]
            response.mask_topic = str(self._param("mask_topic"))
            response.debug_json = debug_json
            status_text = (
                f"ok mode={mode} prompt={request.target_prompt} points={points.shape[0]} "
                f"class={selected_class or '-'} "
                f"bbox={','.join(f'{float(x):.1f}' for x in bbox)} "
                f"roi_points={roi_points.shape[0]} mask_px={int(np.count_nonzero(mask))} "
                f"expanded_px={int(np.count_nonzero(expanded_mask))} score={score:.3f} "
                f"fallback_red={used_fallback} sync_dt={sync_delta_s:.4f}s "
                f"rgb_stamp={self._stamp_s(rgb_msg):.6f} "
                f"depth_stamp={self._stamp_s(depth_msg):.6f} "
                f"rgb_age={inference_start_wall_s - rgb_received_wall_s:.3f}s "
                f"depth_age={inference_start_wall_s - depth_received_wall_s:.3f}s "
                f"queues={rgb_queue_size},{depth_queue_size} "
                f"yolo_s={yolo_latency_s:.3f} sam_s={sam_latency_s:.3f} "
                f"inference_s={inference_latency_s:.3f} "
                f"mask_stamp={selected_mask_publish_stamp_s:.6f}"
            )
            self._status_pub.publish(String(data=status_text))
            self.get_logger().info(
                "automatic target segmentation succeeded: " + status_text,
                throttle_duration_sec=0.2,
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

    def destroy_node(self) -> bool:
        self._stop_event.set()
        if self._auto_thread is not None:
            self._auto_thread.join(timeout=2.0)
        return super().destroy_node()


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
