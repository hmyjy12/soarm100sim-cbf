"""Automatically scan safe wrist poses and record RGB-D self-occupancy data."""

from __future__ import annotations

from collections import deque
from datetime import datetime
import json
import math
from pathlib import Path
import time

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image, JointState

from soarm100_interfaces.srv import MoveJointTarget
from soarm100_vision.hardware_joint_limit_filter import HardwareJointLimitFilter
from soarm100_vision.vision_utils import image_to_numpy


JOINT_NAMES = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)
MODEL_LIMITS = np.array(
    [
        [-2.2, 2.2],
        [-math.pi, 0.2],
        [0.0, math.pi],
        [-2.0, 1.8],
        [-1.45, 1.45],
        [-math.pi, math.pi],
        [-0.2, 2.0],
    ],
    dtype=np.float64,
)


class LinkSelfOccupancyCollector(Node):
    def __init__(self) -> None:
        super().__init__("link_self_occupancy_collector")
        repo_default = str(Path(__file__).resolve().parents[3])
        self.declare_parameter("repo_root", repo_default)
        self.declare_parameter(
            "scan_config", "hardware/calibration/link_self_occupancy_scan.json"
        )
        self.declare_parameter("output_root", "log/runtime/hardware/link_self_occupancy")
        self.declare_parameter("depth_topic", "/camera/depth/image_raw")
        self.declare_parameter("camera_info_topic", "/camera/depth/camera_info")
        self.declare_parameter("joint_state_topic", "/joint_states")
        self.declare_parameter("frames_per_pose", 8)
        self.declare_parameter("settle_s", 0.75)
        self.declare_parameter("move_duration_s", 7.0)
        self.declare_parameter("max_move_delta_rad", 0.33)
        self.declare_parameter("joint_sync_tolerance_s", 0.075)
        self.declare_parameter("stationary_tolerance_rad", 0.005)
        self.declare_parameter("confirmation", "")
        self.declare_parameter(
            "hardware_calibration_json",
            "hardware/calibration/lerobot/so100_plus_new_arm.json",
        )
        self.declare_parameter(
            "hardware_mapping_json", "hardware/calibration/policy_joint_mapping.json"
        )

        self.repo = Path(str(self.get_parameter("repo_root").value)).resolve()
        self.scan_path = self._resolve(str(self.get_parameter("scan_config").value))
        self.scan = json.loads(self.scan_path.read_text(encoding="utf-8"))
        if tuple(self.scan["joint_order"]) != JOINT_NAMES:
            raise ValueError("scan joint_order does not match hardware joint order")
        self.output_dir = self._make_output_dir()
        self._joint_samples: deque[tuple[float, np.ndarray]] = deque(maxlen=300)
        self._depth: Image | None = None
        self._info: CameraInfo | None = None
        self._last_saved_stamp: tuple[int, int] | None = None
        self._manifest_frames: list[dict] = []
        self._move_client = self.create_client(
            MoveJointTarget, "/hardware/move_joint_target"
        )
        self.create_subscription(
            JointState,
            str(self.get_parameter("joint_state_topic").value),
            self._on_joint_state,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            Image,
            str(self.get_parameter("depth_topic").value),
            self._on_depth,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            CameraInfo,
            str(self.get_parameter("camera_info_topic").value),
            self._on_info,
            qos_profile_sensor_data,
        )
        limit_filter = HardwareJointLimitFilter(
            repo_root=self.repo,
            calibration_json=str(self.get_parameter("hardware_calibration_json").value),
            mapping_json=str(self.get_parameter("hardware_mapping_json").value),
            margin_counts=100,
        )
        self.hardware_low, self.hardware_high = limit_filter.policy_safe_bounds()

    def _resolve(self, value: str) -> Path:
        path = Path(value).expanduser()
        return (path if path.is_absolute() else self.repo / path).resolve()

    def _make_output_dir(self) -> Path:
        root = self._resolve(str(self.get_parameter("output_root").value))
        output = root / datetime.now().strftime("%Y%m%d_%H%M%S")
        output.mkdir(parents=True, exist_ok=False)
        return output

    @staticmethod
    def _stamp_s(msg) -> float:
        return float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1e-9

    def _on_joint_state(self, msg: JointState) -> None:
        values = dict(zip(msg.name, msg.position))
        if not all(name in values for name in JOINT_NAMES):
            return
        q = np.asarray([values[name] for name in JOINT_NAMES], dtype=np.float64)
        if np.all(np.isfinite(q)):
            stamp = self._stamp_s(msg)
            self._joint_samples.append((stamp, q))

    def _on_depth(self, msg: Image) -> None:
        self._depth = msg

    def _on_info(self, msg: CameraInfo) -> None:
        self._info = msg

    def _spin_until(self, predicate, timeout_s: float, reason: str) -> None:
        deadline = time.monotonic() + timeout_s
        while rclpy.ok() and not predicate():
            if time.monotonic() >= deadline:
                raise RuntimeError(reason)
            rclpy.spin_once(self, timeout_sec=0.05)

    def _current_q(self) -> np.ndarray:
        if not self._joint_samples:
            raise RuntimeError("joint state unavailable")
        return self._joint_samples[-1][1].copy()

    def _valid_target(self, target: np.ndarray) -> tuple[bool, str]:
        low = np.maximum(MODEL_LIMITS[:, 0], self.hardware_low)
        high = np.minimum(MODEL_LIMITS[:, 1], self.hardware_high)
        bad = np.flatnonzero((target < low) | (target > high))
        if bad.size:
            details = ", ".join(
                f"{JOINT_NAMES[i]}={target[i]:+.3f} notin[{low[i]:+.3f},{high[i]:+.3f}]"
                for i in bad
            )
            return False, details
        return True, "ok"

    def _move(self, target: np.ndarray, name: str) -> np.ndarray:
        current = self._current_q()
        max_delta = float(self.get_parameter("max_move_delta_rad").value)
        commanded = current + np.clip(target - current, -max_delta, max_delta)
        if not np.allclose(commanded, target, atol=1.0e-9):
            limited = np.flatnonzero(np.abs(commanded - target) > 1.0e-9)
            details = ", ".join(
                f"{JOINT_NAMES[i]} {target[i] - current[i]:+.3f}->{commanded[i] - current[i]:+.3f}rad"
                for i in limited
            )
            print(f"[collector] LIMIT {name}: {details}")
        valid, reason = self._valid_target(commanded)
        if not valid:
            raise RuntimeError(f"limited move {name} is unsafe: {reason}")
        request = MoveJointTarget.Request()
        request.position_rad = commanded.tolist()
        request.duration = float(self.get_parameter("move_duration_s").value)
        request.confirmation = "MOVE_JOINT_TARGET"
        future = self._move_client.call_async(request)
        rclpy.spin_until_future_complete(
            self, future, timeout_sec=request.duration + 15.0
        )
        response = future.result()
        if response is None or not response.success:
            reason = "no response" if response is None else response.reason
            raise RuntimeError(f"move {name} failed: {reason}")
        return commanded

    def _settle(self) -> None:
        settle_s = float(self.get_parameter("settle_s").value)
        tolerance = float(self.get_parameter("stationary_tolerance_rad").value)
        deadline = time.monotonic() + max(3.0, settle_s + 2.0)
        stable_since: float | None = None
        previous_q: np.ndarray | None = None
        previous_stamp: float | None = None
        while rclpy.ok() and time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
            if not self._joint_samples:
                continue
            stamp, current_q = self._joint_samples[-1]
            if stamp == previous_stamp:
                continue
            if previous_q is not None and float(np.max(np.abs(current_q - previous_q))) <= tolerance:
                stable_since = stable_since or time.monotonic()
                if time.monotonic() - stable_since >= settle_s:
                    return
            else:
                stable_since = None
            previous_q = current_q.copy()
            previous_stamp = stamp
        raise RuntimeError("arm did not become encoder-stationary before capture")

    def _nearest_q(self, stamp_s: float) -> tuple[np.ndarray, float]:
        if not self._joint_samples:
            raise RuntimeError("joint state unavailable during capture")
        joint_stamp, q = min(
            self._joint_samples, key=lambda item: abs(item[0] - stamp_s)
        )
        return q.copy(), abs(joint_stamp - stamp_s)

    def _capture_pose(self, pose_index: int, pose_name: str, target: np.ndarray) -> None:
        count = int(self.get_parameter("frames_per_pose").value)
        saved = 0
        while rclpy.ok() and saved < count:
            rclpy.spin_once(self, timeout_sec=0.2)
            if self._depth is None or self._info is None:
                continue
            stamp_key = (
                int(self._depth.header.stamp.sec),
                int(self._depth.header.stamp.nanosec),
            )
            if stamp_key == self._last_saved_stamp:
                continue
            stamp_s = stamp_key[0] + stamp_key[1] * 1e-9
            q, sync_delta = self._nearest_q(stamp_s)
            if sync_delta > float(self.get_parameter("joint_sync_tolerance_s").value):
                continue
            depth = np.asarray(image_to_numpy(self._depth)).copy()
            frame_name = f"pose_{pose_index:02d}_frame_{saved:02d}.npz"
            np.savez_compressed(
                self.output_dir / frame_name,
                depth=depth,
                q=q,
                target_q=target,
                camera_k=np.asarray(self._info.k, dtype=np.float64),
                stamp_s=np.array(stamp_s),
                sync_delta_s=np.array(sync_delta),
            )
            self._manifest_frames.append(
                {
                    "file": frame_name,
                    "pose_index": pose_index,
                    "pose_name": pose_name,
                    "stamp_s": stamp_s,
                    "joint_sync_delta_s": sync_delta,
                }
            )
            self._last_saved_stamp = stamp_key
            saved += 1
            print(f"[collector] {pose_name}: frame {saved}/{count} dt={sync_delta:.4f}s")

    def _write_manifest(
        self, observed_start_q: np.ndarray, scan_start_q: np.ndarray, status: str
    ) -> None:
        payload = {
            "schema_version": 1,
            "status": status,
            "scan_config": str(self.scan_path),
            "joint_order": list(JOINT_NAMES),
            "observed_start_q": observed_start_q.tolist(),
            "scan_start_q": scan_start_q.tolist(),
            "depth_topic": str(self.get_parameter("depth_topic").value),
            "camera_info_topic": str(self.get_parameter("camera_info_topic").value),
            "frames": self._manifest_frames,
        }
        (self.output_dir / "manifest.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )

    def run(self) -> None:
        if str(self.get_parameter("confirmation").value) != "COLLECT_LINK_SELF_OCCUPANCY":
            raise RuntimeError("confirmation must be COLLECT_LINK_SELF_OCCUPANCY")
        self._spin_until(
            lambda: self._move_client.wait_for_service(timeout_sec=0.1),
            10.0,
            "/hardware/move_joint_target unavailable",
        )
        self._spin_until(
            lambda: bool(self._joint_samples) and self._depth is not None and self._info is not None,
            10.0,
            "RGB-D or joint state unavailable",
        )
        observed_start_q = self._current_q()
        print(f"[collector] output={self.output_dir}")
        print(f"[collector] observed_start_q={observed_start_q.tolist()}")
        scan_start_q = observed_start_q.copy()
        arm_low = np.maximum(MODEL_LIMITS[:6, 0], self.hardware_low[:6])
        arm_high = np.minimum(MODEL_LIMITS[:6, 1], self.hardware_high[:6])
        bad_arm = np.flatnonzero(
            (scan_start_q[:6] < arm_low) | (scan_start_q[:6] > arm_high)
        )
        if bad_arm.size:
            details = ", ".join(
                f"{JOINT_NAMES[i]}={scan_start_q[i]:+.3f} "
                f"notin[{arm_low[i]:+.3f},{arm_high[i]:+.3f}]"
                for i in bad_arm
            )
            raise RuntimeError(f"startup arm pose outside safe intersection: {details}")
        gripper_low = max(MODEL_LIMITS[6, 0], self.hardware_low[6])
        gripper_high = min(MODEL_LIMITS[6, 1], self.hardware_high[6])
        if not gripper_low <= scan_start_q[6] <= gripper_high:
            safe_gripper = float(np.clip(scan_start_q[6], gripper_low + 0.03, gripper_high - 0.03))
            print(
                f"[collector] gripper={scan_start_q[6]:+.3f} is not a legal motion target; "
                f"opening to {safe_gripper:+.3f} rad before scanning"
            )
            scan_start_q[6] = safe_gripper
            scan_start_q = self._move(scan_start_q, "prepare_safe_gripper")
            self._settle()
        status = "failed"
        failure: Exception | None = None
        try:
            for index, pose in enumerate(self.scan["poses"]):
                offset = np.asarray(pose["offset_rad"], dtype=np.float64)
                target = scan_start_q + offset
                valid, reason = self._valid_target(target)
                if not valid:
                    print(f"[collector] SKIP {pose['name']}: {reason}")
                    continue
                print(f"[collector] MOVE {index + 1}/{len(self.scan['poses'])}: {pose['name']}")
                target = self._move(target, str(pose["name"]))
                self._settle()
                self._capture_pose(index, str(pose["name"]), target)
            status = "complete"
        except Exception as exc:
            failure = exc
        try:
            self._move(scan_start_q, "return_scan_start")
        except Exception as return_exc:
            if failure is None:
                failure = return_exc
            else:
                print(f"[collector] WARNING: return_scan_start also failed: {return_exc}")
        finally:
            self._write_manifest(observed_start_q, scan_start_q, status)
        if failure is not None:
            raise failure
        print(f"[collector] complete: {len(self._manifest_frames)} frames")


def main() -> None:
    rclpy.init()
    node = LinkSelfOccupancyCollector()
    try:
        node.run()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
