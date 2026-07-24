from __future__ import annotations

from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image, PointCloud2
from std_msgs.msg import String

from soarm100_vision.sdf_cbf_core import TableFilter, VoxelPersistence, WorkspaceCrop
from soarm100_vision.policy_backend_core import (
    points_to_base_from_calib,
    points_to_base_from_mujoco_camera,
)
from soarm100_vision.vision_utils import (
    depth_to_points,
    image_to_numpy,
    pointcloud2_xyz,
)


class ObstacleCloudNode(Node):
    """Build a workspace obstacle cloud from main RGB-D depth.

    This mirrors the MuJoCo ``workspace_sdf`` front-end: remove robot/self pixels
    when a mask is available, crop to reachable workspace, remove table/floor,
    then keep only short-window persistent voxels. The published cloud is the
    obstacle input for an SDF-CBF-QP node.
    """

    def __init__(self) -> None:
        super().__init__("soarm100_obstacle_cloud")
        self.declare_parameter("depth_topic", "/camera/depth/image_rect_raw")
        self.declare_parameter("camera_info_topic", "/camera/depth/camera_info")
        self.declare_parameter("robot_mask_topic", "/robot/mask")
        self.declare_parameter("obstacle_cloud_topic", "/obstacle/cloud")
        self.declare_parameter("status_topic", "/obstacle/status")
        self.declare_parameter("use_robot_mask", True)
        self.declare_parameter("repo_root", str(Path(__file__).resolve().parents[3]))
        self.declare_parameter(
            "mjcf", "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"
        )
        self.declare_parameter("calib_json", "logs/calib/camera_calib.json")
        self.declare_parameter("use_sim_camera_extrinsics", True)
        self.declare_parameter("input_camera_name", "scene_depth")
        self.declare_parameter("base_frame", "base")
        self.declare_parameter("workspace_x", [0.02, 0.36])
        self.declare_parameter("workspace_y", [-0.08, 0.26])
        self.declare_parameter("workspace_z", [0.055, 0.42])
        self.declare_parameter("remove_table_plane", True)
        self.declare_parameter("table_z_max", 0.055)
        self.declare_parameter("persistence_voxel_size", 0.012)
        self.declare_parameter("persistence_hits", 2)
        self.declare_parameter("persistence_forget_frames", 4)
        self.declare_parameter("min_points", 30)
        self.declare_parameter("publish_rate_hz", 10.0)
        self.declare_parameter("obstacle_mode", "static")
        self.declare_parameter("static_frames", 5)

        self._depth: Image | None = None
        self._info: CameraInfo | None = None
        self._robot_mask: np.ndarray | None = None
        self._last_depth_stamp: tuple[int, int] | None = None
        self._processed_frames = 0
        self._frozen_cloud = np.zeros((0, 3), dtype=np.float32)
        self._persistence = VoxelPersistence(
            voxel_size=float(self._param("persistence_voxel_size")),
            min_hits=int(self._param("persistence_hits")),
            forget_frames=int(self._param("persistence_forget_frames")),
        )

        self._cloud_pub = self.create_publisher(PointCloud2, self._param("obstacle_cloud_topic"), 1)
        self._status_pub = self.create_publisher(String, self._param("status_topic"), 1)
        self.create_subscription(Image, self._param("depth_topic"), self._on_depth, 1)
        self.create_subscription(CameraInfo, self._param("camera_info_topic"), self._on_info, 10)
        self.create_subscription(Image, self._param("robot_mask_topic"), self._on_robot_mask, 1)
        period = 1.0 / max(float(self._param("publish_rate_hz")), 1e-3)
        self.create_timer(period, self._tick)
        self.get_logger().info(
            "obstacle cloud ready: "
            f"depth={self._param('depth_topic')} robot_mask={self._param('robot_mask_topic')} "
            f"cloud={self._param('obstacle_cloud_topic')}"
        )

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _on_depth(self, msg: Image) -> None:
        self._depth = msg

    def _on_info(self, msg: CameraInfo) -> None:
        self._info = msg

    def _on_robot_mask(self, msg: Image) -> None:
        self._robot_mask = image_to_numpy(msg) > 0

    def _tick(self) -> None:
        if self._depth is None or self._info is None:
            return
        mode = str(self._param("obstacle_mode")).strip().lower()
        if mode == "static" and self._processed_frames >= int(
            self._param("static_frames")
        ):
            return
        stamp_key = (
            int(self._depth.header.stamp.sec),
            int(self._depth.header.stamp.nanosec),
        )
        if stamp_key == self._last_depth_stamp:
            return
        self._last_depth_stamp = stamp_key
        self._processed_frames += 1
        depth = image_to_numpy(self._depth).astype(np.float32)
        n_self = 0
        if bool(self._param("use_robot_mask")) and self._robot_mask is not None:
            if self._robot_mask.shape[:2] == depth.shape[:2]:
                valid_self = self._robot_mask & np.isfinite(depth) & (depth > 1e-4)
                n_self = int(np.count_nonzero(valid_self))
                depth = depth.copy()
                depth[self._robot_mask] = np.nan
        pts_all = depth_to_points(depth, self._info)
        repo = Path(str(self._param("repo_root"))).expanduser().resolve()
        if bool(self._param("use_sim_camera_extrinsics")):
            pts_all = points_to_base_from_mujoco_camera(
                pts_all,
                repo_root=repo,
                mjcf=str(self._param("mjcf")),
                input_camera_name=str(self._param("input_camera_name")),
            )
        else:
            pts_all = points_to_base_from_calib(
                pts_all,
                repo_root=repo,
                calib_json=str(self._param("calib_json")),
                input_camera_name=str(self._param("input_camera_name")),
            )
        wx = [float(x) for x in self._param("workspace_x")]
        wy = [float(x) for x in self._param("workspace_y")]
        wz = [float(x) for x in self._param("workspace_z")]
        pts_workspace = WorkspaceCrop(
            x_min=wx[0],
            x_max=wx[1],
            y_min=wy[0],
            y_max=wy[1],
            z_min=wz[0],
            z_max=wz[1],
        ).apply(pts_all)
        pts, n_table = TableFilter(
            enabled=bool(self._param("remove_table_plane")),
            z_max=float(self._param("table_z_max")),
        ).apply(pts_workspace)
        self._persistence.voxel_size = float(self._param("persistence_voxel_size"))
        self._persistence.min_hits = int(self._param("persistence_hits"))
        self._persistence.forget_frames = int(self._param("persistence_forget_frames"))
        persistent = self._persistence.update(pts)
        if mode == "static" and persistent.shape[0] >= int(self._param("min_points")):
            self._frozen_cloud = persistent.copy()
        stamp = self._depth.header.stamp
        frame_id = str(self._param("base_frame"))
        if persistent.shape[0] >= int(self._param("min_points")):
            self._cloud_pub.publish(pointcloud2_xyz(persistent, stamp=stamp, frame_id=frame_id))
        bbox_text = "bbox=empty"
        if persistent.shape[0] > 0:
            bbox_min = persistent.min(axis=0)
            bbox_max = persistent.max(axis=0)
            bbox_text = (
                f"bbox_min=({bbox_min[0]:+.3f},{bbox_min[1]:+.3f},{bbox_min[2]:+.3f}) "
                f"bbox_max=({bbox_max[0]:+.3f},{bbox_max[1]:+.3f},{bbox_max[2]:+.3f})"
            )
        status = (
            f"stamp={stamp_key[0]}.{stamp_key[1]:09d} "
            f"depth={pts_all.shape[0]} robot_mask_received={self._robot_mask is not None} "
            f"self_rm={n_self} workspace={pts_workspace.shape[0]} "
            f"table_rm={n_table} raw_obstacle={pts.shape[0]} persistent={persistent.shape[0]} "
            f"voxels={len(self._persistence.records)} mode={mode} "
            f"frame={self._processed_frames}/{self._param('static_frames')} {bbox_text}"
        )
        self._status_pub.publish(String(data=status))
        self.get_logger().info(status)


def main() -> None:
    rclpy.init()
    node = ObstacleCloudNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
