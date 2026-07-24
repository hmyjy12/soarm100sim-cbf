from __future__ import annotations

from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, RegionOfInterest
from std_msgs.msg import String

from soarm100_interfaces.msg import TrackedTarget2D
from soarm100_vision.vision_utils import image_to_numpy


class WristTrackerNode(Node):
    """RGB-only local appearance tracker for the wrist camera."""

    def __init__(self) -> None:
        super().__init__("soarm100_wrist_tracker")
        self.declare_parameter("rgb_topic", "/wrist/color/image_raw")
        self.declare_parameter("roi_hint_topic", "/wrist/tracking_roi")
        self.declare_parameter("tracked_topic", "/target/tracked_2d")
        self.declare_parameter("status_topic", "/target/tracking_status")
        self.declare_parameter("search_expand_px", 48)
        self.declare_parameter("min_template_px", 12)
        self.declare_parameter("match_threshold", 0.45)
        self.declare_parameter("replan_lost_frames", 5)
        self.declare_parameter("template_update_alpha", 0.04)
        self.declare_parameter("repo_root", str(Path(__file__).resolve().parents[3]))
        self.declare_parameter("save_failure_frames", True)
        self.declare_parameter(
            "failure_frame_dir", "logs/ros2_tracking_failures"
        )

        self._rgb: Image | None = None
        self._rgb_seq = 0
        self._processed_seq = -1
        self._hint: RegionOfInterest | None = None
        self._template: np.ndarray | None = None
        self._bbox: tuple[int, int, int, int] | None = None
        self._lost_frames = 0

        self._track_pub = self.create_publisher(
            TrackedTarget2D, str(self._param("tracked_topic")), 1
        )
        self._status_pub = self.create_publisher(
            String, str(self._param("status_topic")), 1
        )
        self.create_subscription(
            Image, str(self._param("rgb_topic")), self._on_rgb, 1
        )
        self.create_subscription(
            RegionOfInterest, str(self._param("roi_hint_topic")), self._on_hint, 1
        )
        self.create_timer(1.0 / 30.0, self._tick)
        self.get_logger().info(
            "RGB wrist tracker ready: "
            f"rgb={self._param('rgb_topic')} hint={self._param('roi_hint_topic')} "
            f"tracked={self._param('tracked_topic')}"
        )

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _on_rgb(self, msg: Image) -> None:
        self._rgb = msg
        self._rgb_seq += 1

    def _on_hint(self, msg: RegionOfInterest) -> None:
        self._hint = msg

    @staticmethod
    def _gray(image: np.ndarray) -> np.ndarray:
        arr = np.asarray(image)
        if arr.ndim == 2:
            return np.ascontiguousarray(arr.astype(np.uint8))
        rgb = arr[..., :3].astype(np.float32)
        gray = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
        return np.ascontiguousarray(np.clip(gray, 0, 255).astype(np.uint8))

    @staticmethod
    def _clip_bbox(
        bbox: tuple[int, int, int, int], shape: tuple[int, int]
    ) -> tuple[int, int, int, int] | None:
        h, w = shape
        x1, y1, x2, y2 = bbox
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        if x2 <= x1 or y2 <= y1:
            return None
        return x1, y1, x2, y2

    def _initialize(self, gray: np.ndarray) -> bool:
        hint = self._hint
        if hint is None:
            return False
        bbox = self._clip_bbox(
            (
                int(hint.x_offset),
                int(hint.y_offset),
                int(hint.x_offset + hint.width),
                int(hint.y_offset + hint.height),
            ),
            gray.shape,
        )
        if bbox is None:
            return False
        x1, y1, x2, y2 = bbox
        minimum = int(self._param("min_template_px"))
        if x2 - x1 < minimum or y2 - y1 < minimum:
            return False
        self._template = gray[y1:y2, x1:x2].copy()
        self._bbox = bbox
        self._lost_frames = 0
        return True

    def _tick(self) -> None:
        if self._rgb is None or self._processed_seq == self._rgb_seq:
            return
        self._processed_seq = self._rgb_seq
        msg = self._rgb
        try:
            import cv2

            gray = self._gray(image_to_numpy(msg))
            if self._template is None or self._bbox is None:
                if not self._initialize(gray):
                    self._publish(msg, valid=False, reason="waiting_for_visible_roi")
                    return
            assert self._template is not None and self._bbox is not None
            hint = self._hint
            if hint is None:
                self._lost(msg, "tracking_hint_missing")
                return
            x1 = int(hint.x_offset)
            y1 = int(hint.y_offset)
            x2 = int(hint.x_offset + hint.width)
            y2 = int(hint.y_offset + hint.height)
            expand = int(self._param("search_expand_px"))
            search_bbox = self._clip_bbox(
                (x1 - expand, y1 - expand, x2 + expand, y2 + expand), gray.shape
            )
            if search_bbox is None:
                self._lost(msg, "search_roi_outside_image")
                return
            sx1, sy1, sx2, sy2 = search_bbox
            search = gray[sy1:sy2, sx1:sx2]
            best = None
            for scale in (0.70, 0.85, 1.0, 1.20, 1.40):
                tw = max(int(round(self._template.shape[1] * scale)), 8)
                th = max(int(round(self._template.shape[0] * scale)), 8)
                if search.shape[0] < th or search.shape[1] < tw:
                    continue
                candidate = cv2.resize(
                    self._template, (tw, th), interpolation=cv2.INTER_LINEAR
                )
                scores = cv2.matchTemplate(
                    search, candidate, cv2.TM_CCOEFF_NORMED
                )
                _, score, _, location = cv2.minMaxLoc(scores)
                if best is None or float(score) > best[0]:
                    best = (float(score), location, candidate)
            if best is None:
                self._lost(msg, "search_roi_smaller_than_template")
                return
            confidence, max_loc, matched_template = best
            if not np.isfinite(confidence) or confidence < float(
                self._param("match_threshold")
            ):
                self._save_failure_frame(
                    cv2,
                    image_to_numpy(msg),
                    search_bbox,
                    max_loc,
                    matched_template,
                    float(confidence),
                )
                self._lost(msg, f"low_confidence:{confidence:.3f}")
                return
            nx1 = int(sx1 + max_loc[0])
            ny1 = int(sy1 + max_loc[1])
            th, tw = matched_template.shape[:2]
            nx2, ny2 = nx1 + tw, ny1 + th
            self._bbox = (nx1, ny1, nx2, ny2)
            self._lost_frames = 0
            alpha = float(self._param("template_update_alpha"))
            patch = gray[ny1:ny2, nx1:nx2].astype(np.float32)
            canonical_h, canonical_w = self._template.shape[:2]
            patch = cv2.resize(
                patch, (canonical_w, canonical_h), interpolation=cv2.INTER_LINEAR
            )
            updated = (
                (1.0 - alpha) * self._template.astype(np.float32) + alpha * patch
            )
            self._template = np.clip(updated, 0, 255).astype(np.uint8)
            self._publish(
                msg,
                valid=True,
                confidence=float(confidence),
                bbox=self._bbox,
                reason="track_ok",
            )
        except Exception as exc:
            self._lost(msg, f"tracker_error:{exc}")

    def _save_failure_frame(
        self,
        cv2,
        rgb: np.ndarray,
        search_bbox: tuple[int, int, int, int],
        max_loc: tuple[int, int],
        matched_template: np.ndarray,
        confidence: float,
    ) -> None:
        if not bool(self._param("save_failure_frames")):
            return
        out_dir = Path(str(self._param("failure_frame_dir"))).expanduser()
        if not out_dir.is_absolute():
            out_dir = (
                Path(str(self._param("repo_root"))).expanduser().resolve() / out_dir
            )
        out_dir.mkdir(parents=True, exist_ok=True)
        index = int(self._rgb_seq)
        sx1, sy1, sx2, sy2 = search_bbox
        th, tw = matched_template.shape[:2]
        mx1 = int(sx1 + max_loc[0])
        my1 = int(sy1 + max_loc[1])
        annotated = np.asarray(rgb).copy()
        cv2.rectangle(annotated, (sx1, sy1), (sx2, sy2), (255, 255, 0), 2)
        cv2.rectangle(
            annotated, (mx1, my1), (mx1 + tw, my1 + th), (255, 0, 0), 2
        )
        cv2.putText(
            annotated,
            f"confidence={confidence:.3f}",
            (10, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.imwrite(
            str(out_dir / f"frame_{index:06d}_annotated.png"),
            cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR),
        )
        cv2.imwrite(
            str(out_dir / f"frame_{index:06d}_template.png"), matched_template
        )
        self.get_logger().warn(
            f"saved low-confidence wrist diagnostics: frame={index} "
            f"confidence={confidence:.3f} dir={out_dir}"
        )

    def _lost(self, image_msg: Image, reason: str) -> None:
        self._lost_frames += 1
        replan = self._lost_frames >= int(self._param("replan_lost_frames"))
        if replan:
            self._template = None
            self._bbox = None
        self._publish(
            image_msg, valid=False, replan=replan, reason=reason
        )

    def _publish(
        self,
        image_msg: Image,
        *,
        valid: bool,
        confidence: float = 0.0,
        bbox: tuple[int, int, int, int] | None = None,
        replan: bool = False,
        reason: str,
    ) -> None:
        out = TrackedTarget2D()
        out.header = image_msg.header
        out.valid = bool(valid)
        out.image_width = int(image_msg.width)
        out.image_height = int(image_msg.height)
        if self._hint is not None:
            out.reference_u = float(
                self._hint.x_offset + 0.5 * self._hint.width
            )
            out.reference_v = float(
                self._hint.y_offset + 0.5 * self._hint.height
            )
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            out.u = float(0.5 * (x1 + x2))
            out.v = float(0.5 * (y1 + y2))
            out.width = float(x2 - x1)
            out.height = float(y2 - y1)
            out.delta_u = float(out.u - out.reference_u)
            out.delta_v = float(out.v - out.reference_v)
        out.confidence = float(confidence)
        out.lost_frames = int(self._lost_frames)
        out.replan_required = bool(replan)
        out.reason = str(reason)
        self._track_pub.publish(out)
        self._status_pub.publish(
            String(
                data=(
                    f"{'TRACK_OK' if valid else 'TRACK_LOST'} "
                    f"uv=({out.u:.1f},{out.v:.1f}) confidence={out.confidence:.3f} "
                    f"lost={out.lost_frames} replan={out.replan_required} reason={out.reason}"
                )
            )
        )


def main() -> None:
    rclpy.init()
    node = WristTrackerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
