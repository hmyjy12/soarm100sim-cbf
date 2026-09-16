#!/usr/bin/env python3
"""Verify live Orbbec RGB, depth and depth CameraInfo before arm power-on."""

from __future__ import annotations

import argparse
import time
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image


def stamp_s(message) -> float:
    return float(message.header.stamp.sec) + float(message.header.stamp.nanosec) * 1.0e-9


class RgbdSyncCheck(Node):
    def __init__(self, rgb_topic: str, depth_topic: str, info_topic: str) -> None:
        super().__init__("check_orbbec_rgbd_sync")
        self.rgb_stamps: deque[float] = deque(maxlen=120)
        self.depth_stamps: deque[float] = deque(maxlen=120)
        self.info_count = 0
        self.rgb_shape: tuple[int, int] | None = None
        self.depth_shape: tuple[int, int] | None = None
        self.info_shape: tuple[int, int] | None = None
        self.create_subscription(Image, rgb_topic, self._on_rgb, qos_profile_sensor_data)
        self.create_subscription(Image, depth_topic, self._on_depth, qos_profile_sensor_data)
        self.create_subscription(CameraInfo, info_topic, self._on_info, qos_profile_sensor_data)

    def _on_rgb(self, message: Image) -> None:
        self.rgb_stamps.append(stamp_s(message))
        self.rgb_shape = (int(message.width), int(message.height))

    def _on_depth(self, message: Image) -> None:
        self.depth_stamps.append(stamp_s(message))
        self.depth_shape = (int(message.width), int(message.height))

    def _on_info(self, message: CameraInfo) -> None:
        self.info_count += 1
        self.info_shape = (int(message.width), int(message.height))

    def best_delta_s(self) -> float | None:
        if not self.rgb_stamps or not self.depth_stamps:
            return None
        return min(abs(rgb - depth) for rgb in self.rgb_stamps for depth in self.depth_stamps)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rgb-topic", default="/camera/color/image_raw")
    parser.add_argument("--depth-topic", default="/camera/depth/image_raw")
    parser.add_argument("--camera-info-topic", default="/camera/depth/camera_info")
    parser.add_argument("--timeout-s", type=float, default=10.0)
    parser.add_argument("--tolerance-s", type=float, default=0.10)
    parser.add_argument("--min-frames", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rclpy.init()
    node = RgbdSyncCheck(args.rgb_topic, args.depth_topic, args.camera_info_topic)
    deadline = time.monotonic() + float(args.timeout_s)
    try:
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
            best = node.best_delta_s()
            enough = (
                len(node.rgb_stamps) >= int(args.min_frames)
                and len(node.depth_stamps) >= int(args.min_frames)
                and node.info_count > 0
            )
            depth_info_shape_ok = (
                node.depth_shape is not None and node.depth_shape == node.info_shape
            )
            if enough and depth_info_shape_ok and best is not None and best <= float(args.tolerance_s):
                print(
                    "[rgbd_sync] PASS "
                    f"rgb={len(node.rgb_stamps)} depth={len(node.depth_stamps)} "
                    f"info={node.info_count} rgb_shape={node.rgb_shape} "
                    f"depth_shape={node.depth_shape} info_shape={node.info_shape} "
                    f"rgb_depth_shape_match={node.rgb_shape == node.depth_shape} "
                    f"best_dt={best:.6f}s tolerance={float(args.tolerance_s):.6f}s"
                )
                return 0

        best = node.best_delta_s()
        if not node.rgb_stamps and not node.depth_stamps and node.info_count == 0:
            diagnosis = "no_camera_messages:start_orbbec_driver_and_check_ros_domain"
        elif not node.rgb_stamps:
            diagnosis = "missing_rgb"
        elif not node.depth_stamps:
            diagnosis = "missing_depth"
        elif node.info_count == 0:
            diagnosis = "missing_camera_info"
        elif node.depth_shape != node.info_shape:
            diagnosis = "depth_camera_info_shape_mismatch"
        else:
            diagnosis = "rgb_depth_timestamp_mismatch"
        print(
            "[rgbd_sync] FAIL "
            f"reason={diagnosis} "
            f"rgb={len(node.rgb_stamps)} depth={len(node.depth_stamps)} "
            f"info={node.info_count} rgb_shape={node.rgb_shape} "
            f"depth_shape={node.depth_shape} info_shape={node.info_shape} "
            f"best_dt={'none' if best is None else f'{best:.6f}s'} "
            f"tolerance={float(args.tolerance_s):.6f}s"
        )
        return 1
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
