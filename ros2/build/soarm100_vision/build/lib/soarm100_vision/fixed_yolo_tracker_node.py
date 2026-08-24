from __future__ import annotations

import json
import time

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.executors import ExternalShutdownException
from sensor_msgs.msg import Image
from std_msgs.msg import String

from soarm100_vision.target_segmenter_node import (
    normalize_model_names,
    resolve_fixed_class_id,
)
from soarm100_vision.vision_utils import image_to_numpy, numpy_rgb_to_msg


class FixedYoloTrackerNode(Node):
    """Continuously track fixed model classes on the main camera RGB stream."""

    def __init__(self) -> None:
        super().__init__("fixed_yolo_tracker")
        self.declare_parameter("rgb_topic", "/camera/color/image_raw")
        self.declare_parameter("annotated_topic", "/debug/fixed_yolo_tracking")
        self.declare_parameter("detections_topic", "/target/detections")
        self.declare_parameter("model", "models/vision/yolowork_fixed_best.pt")
        self.declare_parameter("target_class", "all")
        self.declare_parameter("conf", 0.01)
        self.declare_parameter("iou", 0.70)
        self.declare_parameter("imgsz", 640)
        self.declare_parameter("device", "auto")
        self.declare_parameter("tracker", "botsort.yaml")
        self.declare_parameter("max_fps", 30.0)
        self.declare_parameter("show_window", True)
        self.declare_parameter("window_name", "Orbbec fixed YOLO tracking")

        from ultralytics import YOLO

        self._model = YOLO(str(self._param("model")))
        self._names = normalize_model_names(self._model.names)
        target_class = str(self._param("target_class")).strip()
        if not target_class or target_class.casefold() == "all":
            self._class_ids = sorted(self._names)
            self._target_class = "all"
        else:
            class_id, class_name = resolve_fixed_class_id(
                self._names, target_class
            )
            self._class_ids = [class_id]
            self._target_class = class_name

        self._latest: Image | None = None
        self._latest_sequence = 0
        self._processed_sequence = -1
        self._last_inference = 0.0
        self._smoothed_fps = 0.0
        self._last_status_log = 0.0
        self._first_inference_started = False
        self._cv2 = None
        self._window_ok = False
        if bool(self._param("show_window")):
            self._init_window()

        self._annotated_pub = self.create_publisher(
            Image,
            str(self._param("annotated_topic")),
            qos_profile_sensor_data,
        )
        self._detections_pub = self.create_publisher(
            String, str(self._param("detections_topic")), 10
        )
        self.create_subscription(
            Image,
            str(self._param("rgb_topic")),
            self._on_rgb,
            qos_profile_sensor_data,
        )
        self.create_timer(
            1.0 / max(float(self._param("max_fps")), 1.0), self._tick
        )
        self.get_logger().info(
            "fixed YOLO tracking ready: "
            f"rgb={self._param('rgb_topic')} model={self._param('model')} "
            f"classes={self._names} selected={self._target_class} "
            f"tracker={self._param('tracker')} device={self._param('device')}"
        )

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _init_window(self) -> None:
        try:
            import cv2

            self._cv2 = cv2
            cv2.namedWindow(str(self._param("window_name")), cv2.WINDOW_NORMAL)
            self._window_ok = True
        except Exception as exc:
            self.get_logger().warn(
                f"OpenCV window unavailable; annotated topic remains active: {exc}"
            )

    def _on_rgb(self, msg: Image) -> None:
        self._latest = msg
        self._latest_sequence += 1

    def _tick(self) -> None:
        if self._latest is None or self._processed_sequence == self._latest_sequence:
            return
        msg = self._latest
        sequence = self._latest_sequence
        started = time.perf_counter()
        try:
            if not self._first_inference_started:
                self._first_inference_started = True
                self.get_logger().info(
                    "first RGB frame received; CUDA/tracker warm-up may take a while"
                )
            rgb = image_to_numpy(msg)
            bgr = np.ascontiguousarray(rgb[..., ::-1])
            kwargs = {
                "source": bgr,
                "persist": True,
                "tracker": str(self._param("tracker")),
                "conf": float(self._param("conf")),
                "iou": float(self._param("iou")),
                "imgsz": int(self._param("imgsz")),
                "classes": self._class_ids,
                "verbose": False,
            }
            device = str(self._param("device")).strip()
            if device and device.casefold() != "auto":
                kwargs["device"] = device
            result = self._model.track(**kwargs)[0]
            annotated_bgr, detections = self._draw_detections(bgr, result)
            elapsed = max(time.perf_counter() - started, 1.0e-6)
            instant_fps = 1.0 / elapsed
            self._smoothed_fps = (
                instant_fps
                if self._smoothed_fps <= 0.0
                else 0.85 * self._smoothed_fps + 0.15 * instant_fps
            )
            self._draw_status(annotated_bgr, len(detections))
            annotated_rgb = np.ascontiguousarray(annotated_bgr[..., ::-1])
            self._annotated_pub.publish(
                numpy_rgb_to_msg(
                    annotated_rgb,
                    stamp=msg.header.stamp,
                    frame_id=msg.header.frame_id,
                )
            )
            payload = {
                "frame_id": msg.header.frame_id,
                "stamp": {
                    "sec": int(msg.header.stamp.sec),
                    "nanosec": int(msg.header.stamp.nanosec),
                },
                "inference_ms": elapsed * 1000.0,
                "fps": self._smoothed_fps,
                "detections": detections,
            }
            self._detections_pub.publish(
                String(data=json.dumps(payload, ensure_ascii=True))
            )
            now = time.monotonic()
            if now - self._last_status_log >= 3.0:
                self._last_status_log = now
                summary = ", ".join(
                    f"{item['class_name']}:{item['confidence']:.2f}"
                    for item in detections
                ) or "none"
                self.get_logger().info(
                    f"tracking fps={self._smoothed_fps:.1f} "
                    f"inference={elapsed * 1000.0:.1f}ms "
                    f"objects={len(detections)} [{summary}]"
                )
            if self._window_ok and self._cv2 is not None:
                self._cv2.imshow(str(self._param("window_name")), annotated_bgr)
                key = self._cv2.waitKey(1) & 0xFF
                if key in (ord("q"), 27):
                    self.get_logger().info("viewer requested shutdown")
                    rclpy.shutdown()
        except Exception as exc:
            self.get_logger().error(f"fixed YOLO tracking failed: {exc}")
        finally:
            self._processed_sequence = sequence
            self._last_inference = time.perf_counter()

    def _draw_detections(self, frame: np.ndarray, result) -> tuple[np.ndarray, list[dict]]:
        import cv2

        annotated = frame.copy()
        detections: list[dict] = []
        boxes = getattr(result, "boxes", None)
        if boxes is None:
            return annotated, detections
        for box in boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())
            track_id = (
                int(box.id.item())
                if getattr(box, "id", None) is not None
                else None
            )
            xyxy = [float(value) for value in box.xyxy[0].tolist()]
            x1, y1, x2, y2 = [int(round(value)) for value in xyxy]
            class_name = self._names[class_id]
            label = f"{class_name} {confidence:.2f}"
            if track_id is not None:
                label += f" id={track_id}"
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (255, 255, 0), 3)
            (width, height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2
            )
            top = max(0, y1 - height - baseline - 8)
            cv2.rectangle(
                annotated,
                (x1, top),
                (x1 + width + 10, top + height + baseline + 8),
                (255, 255, 0),
                -1,
            )
            cv2.putText(
                annotated,
                label,
                (x1 + 5, top + height + 3),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (40, 30, 90),
                2,
                cv2.LINE_AA,
            )
            detections.append(
                {
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "track_id": track_id,
                    "bbox_xyxy": xyxy,
                }
            )
        return annotated, detections

    def _draw_status(self, frame: np.ndarray, count: int) -> None:
        import cv2

        status = (
            f"FPS: {self._smoothed_fps:.1f} | Objects: {count} | "
            f"Device: {self._param('device')}"
        )
        cv2.putText(
            frame,
            status,
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    def destroy_node(self):
        if self._cv2 is not None:
            try:
                self._cv2.destroyAllWindows()
            except Exception:
                pass
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = FixedYoloTrackerNode()
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
