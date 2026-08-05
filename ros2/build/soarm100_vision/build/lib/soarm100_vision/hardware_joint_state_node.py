"""Publish calibrated, read-only hardware feedback as ROS2 JointState."""

from __future__ import annotations

import socket
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool

from .hardware_joint_bridge import JOINT_NAMES, decode_hardware_joint_packet


class HardwareJointStateNode(Node):
    def __init__(self) -> None:
        super().__init__("so100_plus_hardware_joint_state")
        self.declare_parameter("bind_host", "127.0.0.1")
        self.declare_parameter("udp_port", 15001)
        self.declare_parameter("joint_state_topic", "/joint_states")
        self.declare_parameter("stale_topic", "/hardware/joint_state_stale")
        self.declare_parameter("stale_timeout", 0.5)
        self.declare_parameter("poll_rate", 100.0)
        self.declare_parameter("status_period", 3.0)

        host = str(self.get_parameter("bind_host").value)
        port = int(self.get_parameter("udp_port").value)
        poll_rate = float(self.get_parameter("poll_rate").value)
        if poll_rate <= 0.0:
            raise ValueError("poll_rate must be positive")

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((host, port))
        self._socket.setblocking(False)
        self._joint_pub = self.create_publisher(
            JointState, str(self.get_parameter("joint_state_topic").value), 10
        )
        self._stale_pub = self.create_publisher(
            Bool, str(self.get_parameter("stale_topic").value), 1
        )
        self._last_receive_time: float | None = None
        self._last_sequence: int | None = None
        self._last_stale: bool | None = None
        self._last_status_time = 0.0
        self._invalid_packets = 0
        self._dropped_packets = 0
        self.create_timer(1.0 / poll_rate, self._poll)
        self.create_timer(0.1, self._publish_status)
        self.get_logger().info(
            f"read-only hardware joint bridge listening on udp://{host}:{port}; "
            f"publishing {self.get_parameter('joint_state_topic').value}"
        )

    def _poll(self) -> None:
        latest = None
        while True:
            try:
                payload, _address = self._socket.recvfrom(65535)
            except BlockingIOError:
                break
            try:
                packet = decode_hardware_joint_packet(payload)
            except ValueError as exc:
                self._invalid_packets += 1
                self.get_logger().warning(
                    f"discarding invalid hardware packet: {exc}",
                    throttle_duration_sec=3.0,
                )
                continue
            if self._last_sequence is not None:
                if packet.sequence <= self._last_sequence:
                    continue
                self._dropped_packets += max(
                    0, packet.sequence - self._last_sequence - 1
                )
            latest = packet

        if latest is None:
            return

        self._last_sequence = latest.sequence
        self._last_receive_time = time.monotonic()
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(JOINT_NAMES)
        msg.position = list(latest.positions)
        self._joint_pub.publish(msg)

    def _publish_status(self) -> None:
        now = time.monotonic()
        timeout = float(self.get_parameter("stale_timeout").value)
        stale = (
            self._last_receive_time is None
            or now - self._last_receive_time > timeout
        )
        self._stale_pub.publish(Bool(data=stale))

        status_period = float(self.get_parameter("status_period").value)
        if stale != self._last_stale or now - self._last_status_time >= status_period:
            age = (
                float("inf")
                if self._last_receive_time is None
                else now - self._last_receive_time
            )
            state = "STALE" if stale else "LIVE"
            self.get_logger().info(
                f"hardware_joint_state={state} seq={self._last_sequence} "
                f"age={age:.3f}s dropped={self._dropped_packets} "
                f"invalid={self._invalid_packets}"
            )
            self._last_stale = stale
            self._last_status_time = now

    def destroy_node(self) -> bool:
        self._socket.close()
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = HardwareJointStateNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
