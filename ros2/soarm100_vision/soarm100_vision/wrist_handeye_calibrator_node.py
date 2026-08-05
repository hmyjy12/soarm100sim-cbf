"""Interactive real-hardware wrist-camera hand-eye calibration.

The checkerboard stays fixed in the workspace while the wrist camera moves.
This node never commands the robot; it only consumes an image, CameraInfo and
the base-to-wrist TF. Press SPACE to capture, S to solve with Tsai, Q to quit.

A Trigger service at /wrist_handeye/capture is also provided so an external
manual orchestrator can power the arm and request one capture.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.duration import Duration
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo, Image
from std_srvs.srv import Trigger
from tf2_ros import Buffer, TransformException, TransformListener

from .vision_utils import image_to_numpy


@dataclass
class Sample:
    stamp_ns: int
    T_base_gripper: np.ndarray
    T_camera_board: np.ndarray
    reprojection_rms_px: float
    image_path: str


def _transform_matrix(msg: TransformStamped) -> np.ndarray:
    t = msg.transform.translation
    q = msg.transform.rotation
    quat = np.array([q.x, q.y, q.z, q.w], dtype=np.float64)
    n = float(np.linalg.norm(quat))
    if n < 1.0e-12:
        raise ValueError("TF contains a zero quaternion")
    x, y, z, w = quat / n
    R = np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float64,
    )
    T = np.eye(4, dtype=np.float64)
    T[:3, :3] = R
    T[:3, 3] = (t.x, t.y, t.z)
    return T


def _rotation_angle_deg(R: np.ndarray) -> float:
    c = float(np.clip((np.trace(R) - 1.0) * 0.5, -1.0, 1.0))
    return math.degrees(math.acos(c))


def _matrix_dict(T: np.ndarray) -> dict:
    return {
        "matrix": np.asarray(T, dtype=float).tolist(),
        "translation_m": np.asarray(T[:3, 3], dtype=float).tolist(),
        "rotation_matrix": np.asarray(T[:3, :3], dtype=float).tolist(),
    }


class WristHandeyeCalibrator(Node):
    def __init__(self) -> None:
        super().__init__("wrist_handeye_calibrator")
        self.declare_parameter("image_topic", "/wrist/color/image_raw")
        self.declare_parameter("camera_info_topic", "/wrist/color/camera_info")
        self.declare_parameter("base_frame", "base")
        self.declare_parameter("gripper_frame", "wrist_roll")
        self.declare_parameter("inner_cols", 9)
        self.declare_parameter("inner_rows", 6)
        self.declare_parameter("square_size_m", 0.02428)
        self.declare_parameter("output_dir", "logs/hardware/wrist_handeye")
        self.declare_parameter("min_samples", 12)
        self.declare_parameter("max_reprojection_rms_px", 1.5)
        self.declare_parameter("reject_duplicate_samples", True)
        self.declare_parameter("min_translation_delta_m", 0.015)
        self.declare_parameter("min_rotation_delta_deg", 8.0)
        self.declare_parameter("tf_timeout_sec", 0.2)
        self.declare_parameter("show_window", True)

        self._pattern = (
            int(self.get_parameter("inner_cols").value),
            int(self.get_parameter("inner_rows").value),
        )
        square = float(self.get_parameter("square_size_m").value)
        self._object_points = np.zeros((self._pattern[0] * self._pattern[1], 3), np.float64)
        self._object_points[:, :2] = (
            np.mgrid[0 : self._pattern[0], 0 : self._pattern[1]].T.reshape(-1, 2) * square
        )

        root = Path(str(self.get_parameter("output_dir").value)).expanduser()
        if not root.is_absolute():
            root = Path.cwd() / root
        session = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._session_dir = (root / session).resolve()
        self._image_dir = self._session_dir / "images"
        self._image_dir.mkdir(parents=True, exist_ok=True)

        self._tf_buffer = Buffer(cache_time=Duration(seconds=10.0))
        self._tf_listener = TransformListener(self._tf_buffer, self)
        self._camera_info: CameraInfo | None = None
        self._image_msg: Image | None = None
        self._display: np.ndarray | None = None
        self._detection: tuple[np.ndarray, np.ndarray, float] | None = None
        self._samples: list[Sample] = []
        self._last_status = "ready"
        self._window = "SO-ARM100 wrist hand-eye (SPACE capture, S solve, Q quit)"
        self._show_window = bool(self.get_parameter("show_window").value)

        self.create_subscription(
            CameraInfo, str(self.get_parameter("camera_info_topic").value), self._on_info, 1
        )
        self.create_subscription(
            Image, str(self.get_parameter("image_topic").value), self._on_image, 1
        )
        self.create_service(Trigger, "/wrist_handeye/capture", self._handle_capture)
        self.create_timer(1.0 / 15.0, self._tick)
        if self._show_window:
            cv2.namedWindow(self._window, cv2.WINDOW_NORMAL)

        reject_dup = bool(self.get_parameter("reject_duplicate_samples").value)
        self.get_logger().info(
            "real wrist hand-eye ready; "
            f"pattern={self._pattern[0]}x{self._pattern[1]} square={square*1000:.2f}mm "
            f"TF={self.get_parameter('base_frame').value}<-{self.get_parameter('gripper_frame').value} "
            f"reject_duplicates={reject_dup} "
            f"capture_srv=/wrist_handeye/capture "
            f"output={self._session_dir}"
        )

    def _on_info(self, msg: CameraInfo) -> None:
        self._camera_info = msg

    def _on_image(self, msg: Image) -> None:
        self._image_msg = msg

    def _intrinsics(self) -> tuple[np.ndarray, np.ndarray] | None:
        if self._camera_info is None:
            return None
        K = np.asarray(self._camera_info.k, dtype=np.float64).reshape(3, 3)
        if K[0, 0] <= 0.0 or K[1, 1] <= 0.0:
            return None
        dist = np.asarray(self._camera_info.d, dtype=np.float64).reshape(-1, 1)
        return K, dist

    def _detect(self, rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, float] | None:
        intr = self._intrinsics()
        if intr is None:
            return None
        K, dist = intr
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        flags = cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_EXHAUSTIVE | cv2.CALIB_CB_ACCURACY
        ok, corners = cv2.findChessboardCornersSB(gray, self._pattern, flags)
        if not ok:
            return None
        corners = corners.reshape(-1, 2).astype(np.float64)
        ok, rvec, tvec = cv2.solvePnP(
            self._object_points, corners, K, dist, flags=cv2.SOLVEPNP_ITERATIVE
        )
        if not ok or float(tvec[2]) <= 0.0:
            return None
        projected, _ = cv2.projectPoints(self._object_points, rvec, tvec, K, dist)
        residual = projected.reshape(-1, 2) - corners
        rms = float(np.sqrt(np.mean(np.sum(residual * residual, axis=1))))
        R, _ = cv2.Rodrigues(rvec)
        T_camera_board = np.eye(4, dtype=np.float64)
        T_camera_board[:3, :3] = R
        T_camera_board[:3, 3] = tvec.reshape(3)
        return corners, T_camera_board, rms

    def _tick(self) -> None:
        if self._image_msg is None:
            if self._show_window:
                waiting = np.zeros((540, 960, 3), dtype=np.uint8)
                cv2.putText(
                    waiting,
                    "WAITING FOR WRIST IMAGE",
                    (90, 235),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.25,
                    (0, 180, 255),
                    3,
                )
                cv2.putText(
                    waiting,
                    str(self.get_parameter("image_topic").value),
                    (90, 290),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (220, 220, 220),
                    2,
                )
                cv2.putText(
                    waiting,
                    "Start ./ros2/run_wrist_camera.sh in another terminal",
                    (90, 345),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (220, 220, 220),
                    2,
                )
                cv2.imshow(self._window, waiting)
                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), ord("Q"), 27):
                    rclpy.shutdown()
            return
        try:
            rgb = np.asarray(image_to_numpy(self._image_msg), dtype=np.uint8)
            self._detection = self._detect(rgb)
            display = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            if self._detection is not None:
                corners, _, rms = self._detection
                cv2.drawChessboardCorners(
                    display, self._pattern, corners.reshape(-1, 1, 2).astype(np.float32), True
                )
                status = f"DETECTED rms={rms:.3f}px samples={len(self._samples)}"
                color = (0, 220, 0)
            elif self._intrinsics() is None:
                status = f"NO CAMERA_INFO samples={len(self._samples)}"
                color = (0, 0, 255)
            else:
                status = f"NO COMPLETE 9x6 BOARD samples={len(self._samples)}"
                color = (0, 0, 255)
            cv2.putText(display, status, (18, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
            cv2.putText(
                display,
                "SPACE capture   S solve Tsai   Q quit",
                (18, 66),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                display,
                self._last_status[:90],
                (18, 98),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 220, 255),
                2,
            )
            self._display = display
            if self._show_window:
                cv2.imshow(self._window, display)
                key = cv2.waitKey(1) & 0xFF
                if key == ord(" "):
                    self._capture()
                elif key in (ord("s"), ord("S")):
                    self._solve()
                elif key in (ord("q"), ord("Q"), 27):
                    rclpy.shutdown()
        except Exception as exc:
            self.get_logger().warning(f"preview/detection failed: {exc}", throttle_duration_sec=2.0)

    def _lookup_pose(self) -> np.ndarray:
        assert self._image_msg is not None
        base = str(self.get_parameter("base_frame").value)
        gripper = str(self.get_parameter("gripper_frame").value)
        stamp = Time.from_msg(self._image_msg.header.stamp)
        timeout = Duration(seconds=float(self.get_parameter("tf_timeout_sec").value))
        try:
            msg = self._tf_buffer.lookup_transform(base, gripper, stamp, timeout=timeout)
        except TransformException as stamped_exc:
            try:
                msg = self._tf_buffer.lookup_transform(base, gripper, Time(), timeout=timeout)
                self.get_logger().warning(
                    f"timestamped TF unavailable; using latest TF: {stamped_exc}",
                    throttle_duration_sec=3.0,
                )
            except TransformException as latest_exc:
                raise RuntimeError(f"TF {base}<-{gripper} unavailable: {latest_exc}") from latest_exc
        return _transform_matrix(msg)

    def _handle_capture(
        self, _request: Trigger.Request, response: Trigger.Response
    ) -> Trigger.Response:
        ok, message = self._capture()
        response.success = ok
        response.message = message
        return response

    def _capture(self) -> tuple[bool, str]:
        if self._detection is None or self._display is None or self._image_msg is None:
            message = "sample rejected: checkerboard or camera intrinsics unavailable"
            self._last_status = message
            self.get_logger().warning(message)
            return False, message
        corners, T_camera_board, rms = self._detection
        max_rms = float(self.get_parameter("max_reprojection_rms_px").value)
        if rms > max_rms:
            message = f"sample rejected: reprojection RMS {rms:.3f}px > {max_rms:.3f}px"
            self._last_status = message
            self.get_logger().warning(message)
            return False, message
        try:
            T_base_gripper = self._lookup_pose()
        except RuntimeError as exc:
            message = str(exc)
            self._last_status = message
            self.get_logger().error(message)
            return False, message

        if bool(self.get_parameter("reject_duplicate_samples").value) and self._samples:
            last = self._samples[-1].T_base_gripper
            dt = float(np.linalg.norm(T_base_gripper[:3, 3] - last[:3, 3]))
            da = _rotation_angle_deg(last[:3, :3].T @ T_base_gripper[:3, :3])
            min_dt = float(self.get_parameter("min_translation_delta_m").value)
            min_da = float(self.get_parameter("min_rotation_delta_deg").value)
            if dt < min_dt and da < min_da:
                message = (
                    f"sample rejected as duplicate: delta={dt*1000:.1f}mm/{da:.1f}deg; "
                    f"need either {min_dt*1000:.1f}mm or {min_da:.1f}deg"
                )
                self._last_status = message
                self.get_logger().warning(message)
                return False, message

        index = len(self._samples)
        image_path = self._image_dir / f"sample_{index:03d}.png"
        cv2.imwrite(str(image_path), self._display)
        stamp_ns = Time.from_msg(self._image_msg.header.stamp).nanoseconds
        self._samples.append(
            Sample(stamp_ns, T_base_gripper.copy(), T_camera_board.copy(), rms, str(image_path))
        )
        self._write_dataset()
        message = (
            f"CAPTURED sample={index:03d} rms={rms:.3f}px "
            f"board_distance={np.linalg.norm(T_camera_board[:3, 3])*1000:.1f}mm "
            f"total={len(self._samples)}"
        )
        self._last_status = message
        self.get_logger().info(message)
        return True, message

    def _dataset_payload(self) -> dict:
        return {
            "schema": "soarm100_real_wrist_handeye_samples_v1",
            "method": "Tsai",
            "base_frame": str(self.get_parameter("base_frame").value),
            "gripper_frame": str(self.get_parameter("gripper_frame").value),
            "camera_frame": self._image_msg.header.frame_id if self._image_msg else "",
            "pattern_inner_corners": list(self._pattern),
            "square_size_m": float(self.get_parameter("square_size_m").value),
            "samples": [
                {
                    "stamp_ns": s.stamp_ns,
                    "T_base_gripper": s.T_base_gripper.tolist(),
                    "T_camera_board": s.T_camera_board.tolist(),
                    "reprojection_rms_px": s.reprojection_rms_px,
                    "image_path": s.image_path,
                }
                for s in self._samples
            ],
        }

    def _write_dataset(self) -> None:
        (self._session_dir / "samples.json").write_text(
            json.dumps(self._dataset_payload(), indent=2), encoding="utf-8"
        )

    def _solve(self) -> None:
        minimum = int(self.get_parameter("min_samples").value)
        if len(self._samples) < minimum:
            message = f"cannot solve: {len(self._samples)} samples, need at least {minimum}"
            self._last_status = message
            self.get_logger().error(message)
            return
        R_g2b = [s.T_base_gripper[:3, :3] for s in self._samples]
        t_g2b = [s.T_base_gripper[:3, 3].reshape(3, 1) for s in self._samples]
        R_t2c = [s.T_camera_board[:3, :3] for s in self._samples]
        t_t2c = [s.T_camera_board[:3, 3].reshape(3, 1) for s in self._samples]
        R_c2g, t_c2g = cv2.calibrateHandEye(
            R_g2b, t_g2b, R_t2c, t_t2c, method=cv2.CALIB_HAND_EYE_TSAI
        )
        T_gripper_camera = np.eye(4, dtype=np.float64)
        T_gripper_camera[:3, :3] = R_c2g
        T_gripper_camera[:3, 3] = np.asarray(t_c2g).reshape(3)

        board_poses = [
            s.T_base_gripper @ T_gripper_camera @ s.T_camera_board for s in self._samples
        ]
        translations = np.stack([T[:3, 3] for T in board_poses])
        center = np.mean(translations, axis=0)
        trans_errors = np.linalg.norm(translations - center, axis=1)
        R_ref = board_poses[0][:3, :3]
        rot_errors = np.array([_rotation_angle_deg(R_ref.T @ T[:3, :3]) for T in board_poses])
        result = {
            "schema": "soarm100_real_wrist_handeye_result_v1",
            "method": "Tsai (cv2.CALIB_HAND_EYE_TSAI)",
            "transform_semantics": "T_gripper_camera maps wrist camera optical coordinates into gripper coordinates",
            "base_frame": str(self.get_parameter("base_frame").value),
            "gripper_frame": str(self.get_parameter("gripper_frame").value),
            "camera_frame": self._image_msg.header.frame_id if self._image_msg else "",
            "sample_count": len(self._samples),
            "T_gripper_camera": _matrix_dict(T_gripper_camera),
            "validation": {
                "fixed_board_translation_rms_mm": float(np.sqrt(np.mean(trans_errors**2)) * 1000.0),
                "fixed_board_translation_max_mm": float(np.max(trans_errors) * 1000.0),
                "fixed_board_rotation_rms_deg_vs_first": float(np.sqrt(np.mean(rot_errors**2))),
                "fixed_board_rotation_max_deg_vs_first": float(np.max(rot_errors)),
                "mean_pnp_reprojection_rms_px": float(
                    np.mean([s.reprojection_rms_px for s in self._samples])
                ),
            },
        }
        output = self._session_dir / "wrist_handeye_tsai.json"
        output.write_text(json.dumps(result, indent=2), encoding="utf-8")
        v = result["validation"]
        yaml_output = self._session_dir / "wrist_handeye_tsai.yaml"
        storage = cv2.FileStorage(str(yaml_output), cv2.FILE_STORAGE_WRITE)
        if not storage.isOpened():
            raise RuntimeError(f"cannot open hand-eye YAML for writing: {yaml_output}")
        storage.write("method", "Tsai")
        storage.write("base_frame", result["base_frame"])
        storage.write("gripper_frame", result["gripper_frame"])
        storage.write("camera_frame", result["camera_frame"])
        storage.write("T_gripper_camera", T_gripper_camera)
        storage.write("sample_count", len(self._samples))
        storage.write(
            "fixed_board_translation_rms_mm",
            v["fixed_board_translation_rms_mm"],
        )
        storage.write(
            "fixed_board_rotation_rms_deg",
            v["fixed_board_rotation_rms_deg_vs_first"],
        )
        storage.release()
        message = (
            "SOLVED Tsai: "
            f"samples={len(self._samples)} board_spread={v['fixed_board_translation_rms_mm']:.2f}mm RMS, "
            f"rotation={v['fixed_board_rotation_rms_deg_vs_first']:.2f}deg RMS; result={output}"
        )
        self._last_status = message
        self.get_logger().info(message)

    def destroy_node(self) -> bool:
        if self._show_window:
            cv2.destroyWindow(self._window)
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = WristHandeyeCalibrator()
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
