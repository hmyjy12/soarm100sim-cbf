from __future__ import annotations

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

from soarm100_vision.sdf_cbf_core import SdfCloudState
from soarm100_vision.vision_utils import pointcloud2_to_xyz


class SdfCbfBackendNode(Node):
    """SDF-CBF backend boundary for ROS2 obstacle clouds.

    This node currently owns the ROS2-facing SDF state: it consumes obstacle
    clouds, keeps the latest point set, and publishes diagnostics. The next
    control step is to colocate this state with the policy backend so CBF-QP can
    correct policy actions every control tick.
    """

    def __init__(self) -> None:
        super().__init__("soarm100_sdf_cbf_backend")
        self.declare_parameter("obstacle_cloud_topic", "/obstacle/cloud")
        self.declare_parameter("status_topic", "/sdf/status")
        self.declare_parameter("inflate_m", 0.015)
        self.declare_parameter("min_points", 30)
        self._state = SdfCloudState(
            inflate_m=float(self.get_parameter("inflate_m").value),
            min_points=int(self.get_parameter("min_points").value),
        )
        self._status_pub = self.create_publisher(String, str(self.get_parameter("status_topic").value), 1)
        self.create_subscription(PointCloud2, str(self.get_parameter("obstacle_cloud_topic").value), self._on_cloud, 1)
        self.create_timer(0.5, self._tick)
        self.get_logger().info(
            f"SDF-CBF backend ready: obstacle_cloud={self.get_parameter('obstacle_cloud_topic').value}"
        )

    def _on_cloud(self, msg: PointCloud2) -> None:
        self._state.points = pointcloud2_to_xyz(msg)
        self._state.frame_id = str(msg.header.frame_id)
        self._state.stamp_s = float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1e-9

    def _tick(self) -> None:
        self._state.inflate_m = float(self.get_parameter("inflate_m").value)
        self._state.min_points = int(self.get_parameter("min_points").value)
        self._status_pub.publish(String(data=self._state.status_text()))


def main() -> None:
    rclpy.init()
    node = SdfCbfBackendNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
