"""Project main-camera target center into a wrist-image ROI seed.

Used for 2real wrist template tracking. Simulation already publishes
`/wrist/tracking_roi` from the MuJoCo backend; enable this node only when that
backend is off and hand-eye calibrations plus base->wrist_roll TF are available.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo, RegionOfInterest
from std_msgs.msg import String
from tf2_ros import Buffer, TransformException, TransformListener

from soarm100_vision.vision_utils import camera_intrinsics


def _load_matrix(path: Path, key: str) -> np.ndarray:
    payload = json.loads(path.read_text(encoding="utf-8"))
    block = payload.get(key)
    if not isinstance(block, dict) or "matrix" not in block:
        raise ValueError(f"{path} missing {key}.matrix")
    matrix = np.asarray(block["matrix"], dtype=np.float64)
    if matrix.shape != (4, 4):
        raise ValueError(f"{path} {key}.matrix must be 4x4, got {matrix.shape}")
    return matrix


def _invert_rigid(T: np.ndarray) -> np.ndarray:
    out = np.eye(4, dtype=np.float64)
    r = T[:3, :3]
    out[:3, :3] = r.T
    out[:3, 3] = -r.T @ T[:3, 3]
    return out


def _transform_to_matrix(transform) -> np.ndarray:
    t = transform.transform.translation
    q = transform.transform.rotation
    x, y, z, w = float(q.x), float(q.y), float(q.z), float(q.w)
    rot = np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float64,
    )
    matrix = np.eye(4, dtype=np.float64)
    matrix[:3, :3] = rot
    matrix[:3, 3] = [float(t.x), float(t.y), float(t.z)]
    return matrix


class WristTrackingRoiNode(Node):
    """Seed `/wrist/tracking_roi` from `/target/center` via hand-eye calibrations."""

    def __init__(self) -> None:
        super().__init__("soarm100_wrist_tracking_roi")
        repo_default = str(Path(__file__).resolve().parents[3])
        self.declare_parameter("repo_root", repo_default)
        self.declare_parameter("target_center_topic", "/target/center")
        self.declare_parameter("wrist_camera_info_topic", "/wrist/color/camera_info")
        self.declare_parameter("roi_topic", "/wrist/tracking_roi")
        self.declare_parameter("status_topic", "/wrist/tracking_roi_status")
        self.declare_parameter("base_frame", "base")
        self.declare_parameter("gripper_frame", "wrist_roll")
        self.declare_parameter("wrist_camera_frame", "wrist_camera_optical_frame")
        self.declare_parameter(
            "orbbec_calibration",
            "logs/hardware/orbbec_handeye/20260805_143740/orbbec_eye_to_hand_tsai.json",
        )
        self.declare_parameter(
            "wrist_calibration",
            "logs/hardware/wrist_handeye/20260805_110442/wrist_handeye_tsai.json",
        )
        self.declare_parameter("roi_half_size_px", 28)
        self.declare_parameter("min_roi_size_px", 12)
        self.declare_parameter("publish_rate_hz", 15.0)
        self.declare_parameter("tf_timeout_s", 0.05)

        self._center: PoseStamped | None = None
        self._wrist_info: CameraInfo | None = None
        self._status = "waiting_for_target_center"
        repo = Path(str(self.get_parameter("repo_root").value)).expanduser().resolve()
        orbbec_path = self._resolve(repo, str(self.get_parameter("orbbec_calibration").value))
        wrist_path = self._resolve(repo, str(self.get_parameter("wrist_calibration").value))
        self._T_base_camera = _load_matrix(orbbec_path, "T_base_camera")
        self._T_gripper_camera = _load_matrix(wrist_path, "T_gripper_camera")
        self._T_camera_gripper = _invert_rigid(self._T_gripper_camera)

        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)
        self._roi_pub = self.create_publisher(
            RegionOfInterest, str(self.get_parameter("roi_topic").value), 1
        )
        self._status_pub = self.create_publisher(
            String, str(self.get_parameter("status_topic").value), 1
        )
        self.create_subscription(
            PoseStamped,
            str(self.get_parameter("target_center_topic").value),
            self._on_center,
            1,
        )
        self.create_subscription(
            CameraInfo,
            str(self.get_parameter("wrist_camera_info_topic").value),
            self._on_info,
            1,
        )
        rate = float(self.get_parameter("publish_rate_hz").value)
        self.create_timer(1.0 / max(rate, 1.0), self._tick)
        self.get_logger().info(
            "wrist tracking ROI seeder ready: "
            f"orbbec={orbbec_path.name} wrist={wrist_path.name} "
            f"center={self.get_parameter('target_center_topic').value} "
            f"roi={self.get_parameter('roi_topic').value}"
        )

    @staticmethod
    def _resolve(repo: Path, value: str) -> Path:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = repo / path
        path = path.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"calibration file not found: {path}")
        return path

    def _on_center(self, msg: PoseStamped) -> None:
        self._center = msg

    def _on_info(self, msg: CameraInfo) -> None:
        self._wrist_info = msg

    def _tick(self) -> None:
        try:
            roi, detail = self._compute_roi()
        except Exception as exc:
            self._status = f"roi_error:{exc}"
            self._status_pub.publish(String(data=self._status))
            return
        if roi is None:
            self._status_pub.publish(String(data=self._status))
            return
        self._roi_pub.publish(roi)
        self._status = detail
        self._status_pub.publish(String(data=detail))

    def _compute_roi(self) -> tuple[RegionOfInterest | None, str]:
        if self._center is None:
            self._status = "waiting_for_target_center"
            return None, self._status
        if self._wrist_info is None:
            self._status = "waiting_for_wrist_camera_info"
            return None, self._status

        p_cam = np.array(
            [
                float(self._center.pose.position.x),
                float(self._center.pose.position.y),
                float(self._center.pose.position.z),
                1.0,
            ],
            dtype=np.float64,
        )
        p_base = self._T_base_camera @ p_cam

        base = str(self.get_parameter("base_frame").value)
        gripper = str(self.get_parameter("gripper_frame").value)
        timeout = Duration(seconds=float(self.get_parameter("tf_timeout_s").value))
        try:
            tf_msg = self._tf_buffer.lookup_transform(
                base, gripper, Time(), timeout=timeout
            )
        except TransformException as exc:
            self._status = f"waiting_for_tf:{base}->{gripper}:{exc}"
            return None, self._status

        T_base_gripper = _transform_to_matrix(tf_msg)
        T_base_wrist_cam = T_base_gripper @ self._T_gripper_camera
        p_wrist = _invert_rigid(T_base_wrist_cam) @ p_base
        if p_wrist[2] <= 1.0e-4:
            self._status = f"target_behind_wrist_camera z={p_wrist[2]:.4f}"
            return None, self._status

        fx, fy, cx, cy = camera_intrinsics(self._wrist_info)
        u = fx * (p_wrist[0] / p_wrist[2]) + cx
        v = fy * (p_wrist[1] / p_wrist[2]) + cy
        width = int(self._wrist_info.width)
        height = int(self._wrist_info.height)
        half = int(self.get_parameter("roi_half_size_px").value)
        x1 = max(0, int(round(u)) - half)
        y1 = max(0, int(round(v)) - half)
        x2 = min(width, int(round(u)) + half)
        y2 = min(height, int(round(v)) + half)
        min_size = int(self.get_parameter("min_roi_size_px").value)
        if x2 - x1 < min_size or y2 - y1 < min_size:
            self._status = (
                f"roi_too_small uv=({u:.1f},{v:.1f}) size={x2 - x1}x{y2 - y1}"
            )
            return None, self._status

        roi = RegionOfInterest()
        roi.x_offset = x1
        roi.y_offset = y1
        roi.width = x2 - x1
        roi.height = y2 - y1
        roi.do_rectify = False
        detail = (
            f"ok uv=({u:.1f},{v:.1f}) depth={p_wrist[2]:.3f}m "
            f"roi=[{x1},{y1},{x2},{y2}]"
        )
        return roi, detail


def main() -> None:
    rclpy.init()
    node = WristTrackingRoiNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
