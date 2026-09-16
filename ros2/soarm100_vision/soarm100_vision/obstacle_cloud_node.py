from __future__ import annotations

from collections import deque
import json
import os
from pathlib import Path
import sys
import threading
import time

import numpy as np
import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
    qos_profile_sensor_data,
)
from sensor_msgs.msg import CameraInfo, Image, JointState, PointCloud2
from std_msgs.msg import String

from soarm100_vision.sdf_cbf_core import (
    AttachedThinComponentFilter,
    AttachedThinFilterConfig,
    DEFAULT_SELF_FILTER_CAPSULES,
    TableFilter,
    VoxelPersistence,
    WorkspaceCrop,
    filter_capsule_self_points,
    filter_oriented_box_self_points,
    nearest_joint_sample,
)
from soarm100_vision.policy_backend_core import (
    points_to_base_from_calib,
    points_to_base_from_mujoco_camera,
)
from soarm100_vision.vision_utils import (
    depth_to_points,
    image_to_numpy,
    pointcloud2_xyz,
)


JOINT_NAMES = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
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
        self.declare_parameter("target_mask_topic", "/obstacle/selected_mask")
        self.declare_parameter("obstacle_cloud_topic", "/obstacle/cloud")
        self.declare_parameter("status_topic", "/obstacle/status")
        self.declare_parameter("use_robot_mask", True)
        self.declare_parameter("obstacle_selection_mode", "all_except_target")
        self.declare_parameter("target_mask_sync_tolerance_s", 1.0)
        self.declare_parameter("use_joint_state_self_filter", False)
        self.declare_parameter("joint_state_topic", "/joint_states")
        self.declare_parameter("joint_sync_tolerance_s", 0.075)
        self.declare_parameter("joint_buffer_s", 2.0)
        # Includes the real arm's attached cable bundle, which extends beyond
        # the link meshes represented by the nominal capsule radii.
        self.declare_parameter("self_filter_margin_m", 0.035)
        self.declare_parameter("enable_wrist_attachment_box", False)
        # wrist_jaw-local tight box around the raised white wrist housing.
        # Values come from wrist_jaw.STL bounds, not from a symmetric capsule.
        self.declare_parameter("wrist_attachment_box_body", "wrist_jaw")
        self.declare_parameter(
            "wrist_attachment_box_center_m", [0.020100, 0.0, 0.021400]
        )
        self.declare_parameter(
            "wrist_attachment_box_half_size_m", [0.037100, 0.020613, 0.045200]
        )
        self.declare_parameter("wrist_attachment_box_margin_m", 0.004)
        self.declare_parameter("enable_attached_thin_filter", False)
        self.declare_parameter("ignored_thin_topic", "/obstacle/ignored_thin")
        self.declare_parameter("thin_voxel_size_m", 0.010)
        self.declare_parameter("thin_connectivity_m", 0.018)
        self.declare_parameter("thin_min_points", 5)
        self.declare_parameter("thin_min_length_m", 0.060)
        self.declare_parameter("thin_max_width_m", 0.022)
        self.declare_parameter("thin_min_aspect_ratio", 4.0)
        self.declare_parameter("thin_attachment_distance_m", 0.025)
        self.declare_parameter("thin_max_robot_distance_m", 0.100)
        self.declare_parameter("thin_min_near_robot_fraction", 0.80)
        self.declare_parameter("repo_root", str(Path(__file__).resolve().parents[3]))
        self.declare_parameter(
            "mjcf", "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"
        )
        self.declare_parameter("calib_json", "log/runtime/calib/camera_calib.json")
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
        self.declare_parameter("depth_pixel_stride", 4)
        self.declare_parameter("publish_rate_hz", 10.0)
        self.declare_parameter("obstacle_mode", "static")
        self.declare_parameter("static_frames", 5)
        self.declare_parameter("lock_static_target_cloud", False)

        self._depth: Image | None = None
        self._info: CameraInfo | None = None
        self._robot_mask: np.ndarray | None = None
        self._target_mask: np.ndarray | None = None
        self._target_mask_stamp_s = 0.0
        self._target_mask_frame_id = ""
        self._target_mask_encoding = ""
        self._target_mask_width = 0
        self._target_mask_height = 0
        self._target_mask_pixels = 0
        self._target_mask_callback_count = 0
        self._depth_callback_count = 0
        self._target_mask_lock = threading.Lock()
        self._target_mask_was_valid = False
        self._joint_samples: deque[tuple[float, np.ndarray]] = deque(maxlen=240)
        self._last_depth_stamp: tuple[int, int] | None = None
        self._last_published_depth_stamp: tuple[int, int] | None = None
        self._processed_frames = 0
        self._locked_cloud: np.ndarray | None = None
        self._locked_ignored_thin = np.zeros((0, 3), dtype=np.float64)
        self._locked_source_stamp_s = 0.0
        self._static_lock_candidate_frames = 0
        self._mujoco = None
        self._model = None
        self._data = None
        self._ids = None
        self._capsule_body_ids: list[tuple[int, int, float]] = []
        self._wrist_attachment_body_id: int | None = None
        if bool(self._param("use_joint_state_self_filter")):
            self._init_robot_self_filter()
        self._persistence = VoxelPersistence(
            voxel_size=float(self._param("persistence_voxel_size")),
            min_hits=int(self._param("persistence_hits")),
            forget_frames=int(self._param("persistence_forget_frames")),
        )

        self._cloud_pub = self.create_publisher(PointCloud2, self._param("obstacle_cloud_topic"), 1)
        self._ignored_thin_pub = self.create_publisher(
            PointCloud2, self._param("ignored_thin_topic"), 1
        )
        self._status_pub = self.create_publisher(String, self._param("status_topic"), 1)
        sensor_group = ReentrantCallbackGroup()
        timer_group = MutuallyExclusiveCallbackGroup()
        selected_mask_qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.VOLATILE,
        )
        self.create_subscription(
            Image,
            self._param("depth_topic"),
            self._on_depth,
            qos_profile_sensor_data,
            callback_group=sensor_group,
        )
        self.create_subscription(
            CameraInfo,
            self._param("camera_info_topic"),
            self._on_info,
            qos_profile_sensor_data,
            callback_group=sensor_group,
        )
        self.create_subscription(
            Image,
            self._param("robot_mask_topic"),
            self._on_robot_mask,
            qos_profile_sensor_data,
            callback_group=sensor_group,
        )
        self.create_subscription(
            Image,
            self._param("target_mask_topic"),
            self._on_target_mask,
            selected_mask_qos,
            callback_group=sensor_group,
        )
        self.create_subscription(
            JointState,
            self._param("joint_state_topic"),
            self._on_joint_state,
            qos_profile_sensor_data,
            callback_group=sensor_group,
        )
        period = 1.0 / max(float(self._param("publish_rate_hz")), 1e-3)
        self.create_timer(period, self._tick, callback_group=timer_group)
        self.get_logger().info(
            "obstacle cloud ready: "
            f"depth={self._param('depth_topic')} robot_mask={self._param('robot_mask_topic')} "
            f"cloud={self._param('obstacle_cloud_topic')}"
        )

    def _init_robot_self_filter(self) -> None:
        repo = Path(str(self._param("repo_root"))).expanduser().resolve()
        repo_resolved = repo.resolve()
        os.chdir(repo / "ros2")
        sys.path[:] = [
            entry
            for entry in sys.path
            if entry and Path(entry).resolve() != repo_resolved
        ]
        import mujoco  # type: ignore

        source_dir = str(repo / "mujoco")
        if source_dir not in sys.path:
            sys.path.insert(0, source_dir)
        import runtime as reach_runtime  # type: ignore

        model = mujoco.MjModel.from_xml_path(str(repo / str(self._param("mjcf"))))
        data = mujoco.MjData(model)
        ids = reach_runtime.resolve_robot_ids(model)
        capsule_ids: list[tuple[int, int, float]] = []
        for body_a, body_b, radius in DEFAULT_SELF_FILTER_CAPSULES:
            a_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_a)
            b_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_b)
            if a_id < 0 or b_id < 0:
                raise ValueError(f"self-filter body missing: {body_a}->{body_b}")
            capsule_ids.append((int(a_id), int(b_id), float(radius)))
        self._mujoco = mujoco
        self._model = model
        self._data = data
        self._ids = ids
        self._capsule_body_ids = capsule_ids
        body_name = str(self._param("wrist_attachment_box_body"))
        body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name)
        if body_id < 0:
            raise ValueError(f"self-filter body missing: {body_name}")
        self._wrist_attachment_body_id = int(body_id)

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _on_depth(self, msg: Image) -> None:
        self._depth_callback_count += 1
        self._depth = msg

    def _on_info(self, msg: CameraInfo) -> None:
        self._info = msg

    def _on_robot_mask(self, msg: Image) -> None:
        self._robot_mask = image_to_numpy(msg) > 0

    def _on_target_mask(self, msg: Image) -> None:
        with self._target_mask_lock:
            self._on_target_mask_locked(msg)

    def _on_target_mask_locked(self, msg: Image) -> None:
        self._target_mask_callback_count += 1
        callback_wall_s = time.time()
        self.get_logger().info(
            "selected_mask callback received: "
            f"callback_count={self._target_mask_callback_count} "
            f"stamp={(float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1.0e-9):.9f} "
            f"frame_id={msg.header.frame_id!r} width={msg.width} height={msg.height} "
            f"encoding={msg.encoding!r} receive_wall={callback_wall_s:.6f}",
        )
        try:
            mask = image_to_numpy(msg) > 0
        except Exception as exc:
            self.get_logger().error(
                "selected_mask callback rejected image: "
                f"callback_count={self._target_mask_callback_count} "
                f"stamp={(float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1.0e-9):.9f} "
                f"frame_id={msg.header.frame_id!r} width={msg.width} height={msg.height} "
                f"encoding={msg.encoding!r} error={exc}"
            )
            return
        self._target_mask = mask
        self._target_mask_stamp_s = (
            float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1.0e-9
        )
        self._target_mask_frame_id = str(msg.header.frame_id)
        self._target_mask_encoding = str(msg.encoding)
        self._target_mask_width = int(msg.width)
        self._target_mask_height = int(msg.height)
        self._target_mask_pixels = int(np.count_nonzero(mask))
        # Mask and synchronized depth use separate ROS topics. Re-evaluate the
        # current depth regardless of DDS delivery order once its mask arrives.
        self._last_depth_stamp = None

    def _on_joint_state(self, msg: JointState) -> None:
        if tuple(msg.name) != JOINT_NAMES or len(msg.position) != len(JOINT_NAMES):
            return
        q = np.asarray(msg.position, dtype=np.float64)
        if not np.all(np.isfinite(q)):
            return
        stamp = float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1.0e-9
        if stamp <= 0.0:
            stamp = self.get_clock().now().nanoseconds * 1.0e-9
        self._joint_samples.append((stamp, q.copy()))
        cutoff = stamp - max(float(self._param("joint_buffer_s")), 0.1)
        while self._joint_samples and self._joint_samples[0][0] < cutoff:
            self._joint_samples.popleft()

    def _filter_robot_from_base_cloud(
        self, points: np.ndarray, depth_stamp_s: float
    ) -> tuple[
        np.ndarray | None,
        int,
        float,
        list[tuple[np.ndarray, np.ndarray, float]],
        int,
    ]:
        if not bool(self._param("use_joint_state_self_filter")):
            return points, 0, 0.0, [], 0
        q, sync_delta = nearest_joint_sample(
            list(self._joint_samples),
            depth_stamp_s,
            float(self._param("joint_sync_tolerance_s")),
        )
        if q is None:
            return None, 0, sync_delta, [], 0
        assert self._mujoco is not None
        assert self._model is not None and self._data is not None and self._ids is not None
        for address, value in zip(self._ids.qpos_adr, q):
            self._data.qpos[address] = float(value)
        self._mujoco.mj_forward(self._model, self._data)
        capsules = [
            (
                np.asarray(self._data.xpos[a_id], dtype=np.float64).copy(),
                np.asarray(self._data.xpos[b_id], dtype=np.float64).copy(),
                radius,
            )
            for a_id, b_id, radius in self._capsule_body_ids
        ]
        filtered, removed = filter_capsule_self_points(
            points, capsules, float(self._param("self_filter_margin_m"))
        )
        box_removed = 0
        if bool(self._param("enable_wrist_attachment_box")):
            assert self._wrist_attachment_body_id is not None
            body_id = self._wrist_attachment_body_id
            body_position = np.asarray(self._data.xpos[body_id], dtype=np.float64)
            body_rotation = np.asarray(self._data.xmat[body_id], dtype=np.float64).reshape(3, 3)
            local_center = np.asarray(
                self._param("wrist_attachment_box_center_m"), dtype=np.float64
            ).reshape(3)
            center_world = body_position + body_rotation @ local_center
            filtered, box_removed = filter_oriented_box_self_points(
                filtered,
                center_world=center_world,
                rotation_world_from_local=body_rotation,
                half_size_m=np.asarray(
                    self._param("wrist_attachment_box_half_size_m"), dtype=np.float64
                ),
                margin_m=float(self._param("wrist_attachment_box_margin_m")),
            )
        return filtered, removed, sync_delta, capsules, box_removed

    def _filter_attached_thin_components(
        self,
        points: np.ndarray,
        capsules: list[tuple[np.ndarray, np.ndarray, float]],
    ):
        if not bool(self._param("enable_attached_thin_filter")):
            return points, np.zeros((0, 3), dtype=np.float64), 0, 0, 0.0
        config = AttachedThinFilterConfig(
            voxel_size_m=float(self._param("thin_voxel_size_m")),
            connectivity_m=float(self._param("thin_connectivity_m")),
            min_points=int(self._param("thin_min_points")),
            min_length_m=float(self._param("thin_min_length_m")),
            max_width_m=float(self._param("thin_max_width_m")),
            min_aspect_ratio=float(self._param("thin_min_aspect_ratio")),
            attachment_distance_m=float(self._param("thin_attachment_distance_m")),
            max_robot_distance_m=float(self._param("thin_max_robot_distance_m")),
            min_near_robot_fraction=float(self._param("thin_min_near_robot_fraction")),
        )
        started = time.perf_counter()
        result = AttachedThinComponentFilter(config).apply(points, capsules[-4:])
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        return (
            result.kept_points,
            result.removed_points,
            result.components_checked,
            result.components_removed,
            elapsed_ms,
        )

    def _tick(self) -> None:
        if self._depth is None or self._info is None:
            return
        mode = str(self._param("obstacle_mode")).strip().lower()
        if mode not in ("static", "dynamic"):
            self.get_logger().error(f"unsupported obstacle_mode={mode}", throttle_duration_sec=2.0)
            return
        if mode == "static" and self._locked_cloud is not None:
            stamp = self.get_clock().now().to_msg()
            frame_id = str(self._param("base_frame"))
            self._cloud_pub.publish(
                pointcloud2_xyz(self._locked_cloud, stamp=stamp, frame_id=frame_id)
            )
            self._ignored_thin_pub.publish(
                pointcloud2_xyz(
                    self._locked_ignored_thin, stamp=stamp, frame_id=frame_id
                )
            )
            self.get_logger().info(
                "static target cloud heartbeat: "
                f"points={self._locked_cloud.shape[0]} "
                f"source_stamp={self._locked_source_stamp_s:.9f}",
                throttle_duration_sec=2.0,
            )
            return
        stamp_key = (
            int(self._depth.header.stamp.sec),
            int(self._depth.header.stamp.nanosec),
        )
        if stamp_key in (self._last_depth_stamp, self._last_published_depth_stamp):
            return
        self._last_depth_stamp = stamp_key
        self._processed_frames += 1
        depth_stamp_s = float(stamp_key[0]) + float(stamp_key[1]) * 1.0e-9
        depth = image_to_numpy(self._depth).astype(np.float32)
        selection_mode = str(self._param("obstacle_selection_mode")).strip().lower()
        if selection_mode not in ("all_except_target", "target_only"):
            self.get_logger().error(
                f"unsupported obstacle_selection_mode={selection_mode}",
                throttle_duration_sec=2.0,
            )
            return
        with self._target_mask_lock:
            target_mask = self._target_mask
            target_mask_stamp_s = self._target_mask_stamp_s
            target_mask_was_valid = self._target_mask_was_valid
        target_mask_valid = (
            target_mask is not None
            and target_mask.shape[:2] == depth.shape[:2]
            and abs(depth_stamp_s - target_mask_stamp_s)
            <= float(self._param("target_mask_sync_tolerance_s"))
        )
        mask_dt_s = (
            abs(depth_stamp_s - target_mask_stamp_s)
            if target_mask is not None
            else float("inf")
        )
        target_mask_pixels = 0
        if target_mask_valid:
            assert target_mask is not None
            if not target_mask_was_valid:
                self._persistence.records.clear()
            target_mask_pixels = int(np.count_nonzero(target_mask))
            depth = depth.copy()
            if selection_mode == "all_except_target":
                depth[target_mask] = np.nan
            else:
                depth[~target_mask] = np.nan
        elif selection_mode == "target_only":
            with self._target_mask_lock:
                self._target_mask_was_valid = False
            status = (
                f"stamp={stamp_key[0]}.{stamp_key[1]:09d} valid=false "
                "reason=target_mask_missing_or_stale "
                f"latest_mask_stamp={target_mask_stamp_s:.9f} "
                f"current_depth_stamp={depth_stamp_s:.9f} "
                f"mask_dt={mask_dt_s:.6f}s "
                f"tolerance={float(self._param('target_mask_sync_tolerance_s')):.6f}s "
                f"mask_callback_count={self._target_mask_callback_count} "
                f"depth_callback_count={self._depth_callback_count} "
                f"mask_shape={None if self._target_mask is None else self._target_mask.shape} "
                f"latest_mask_frame={self._target_mask_frame_id!r} "
                f"latest_mask_encoding={self._target_mask_encoding!r} "
                f"latest_mask_pixels={self._target_mask_pixels} "
                f"depth_shape={depth.shape}"
            )
            self._status_pub.publish(String(data=status))
            self.get_logger().warning(status, throttle_duration_sec=1.0)
            return
        with self._target_mask_lock:
            self._target_mask_was_valid = target_mask_valid
        n_self = 0
        if bool(self._param("use_robot_mask")) and self._robot_mask is not None:
            if self._robot_mask.shape[:2] == depth.shape[:2]:
                valid_self = self._robot_mask & np.isfinite(depth) & (depth > 1e-4)
                n_self = int(np.count_nonzero(valid_self))
                depth = depth.copy()
                depth[self._robot_mask] = np.nan
        pixel_stride = max(int(self._param("depth_pixel_stride")), 1)
        pts_all = depth_to_points(depth, self._info, pixel_stride=pixel_stride)
        optical_stats = cloud_stats(pts_all)
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
        base_stats = cloud_stats(pts_all)
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
        before_self = pts.copy()
        (
            pts,
            n_capsule_self,
            joint_sync_delta,
            capsules,
            n_wrist_box,
        ) = self._filter_robot_from_base_cloud(pts, depth_stamp_s)
        if pts is None:
            status = (
                f"stamp={stamp_key[0]}.{stamp_key[1]:09d} valid=false "
                f"reason=joint_sync_missing nearest_dt={joint_sync_delta:.4f}s"
            )
            self._status_pub.publish(String(data=status))
            self.get_logger().warning(status, throttle_duration_sec=1.0)
            return
        pts, ignored_thin, thin_components, thin_removed_components, thin_ms = (
            self._filter_attached_thin_components(pts, capsules)
        )
        self._persistence.voxel_size = float(self._param("persistence_voxel_size"))
        if mode == "dynamic":
            # A moving obstacle must not leave a union of historical occupied
            # voxels behind it. Keep only the current frame; CBF receives the
            # obstacle velocity separately from the simulation backend.
            self._persistence.min_hits = 1
            self._persistence.forget_frames = 0
            # Also discard within-voxel averaging with older frames.
            self._persistence.records.clear()
        else:
            self._persistence.min_hits = int(self._param("persistence_hits"))
            self._persistence.forget_frames = int(self._param("persistence_forget_frames"))
        persistent = self._persistence.update(pts)
        ready_to_lock_static = (
            mode == "static"
            and bool(self._param("lock_static_target_cloud"))
            and selection_mode == "target_only"
            and persistent.shape[0] >= int(self._param("min_points"))
        )
        if ready_to_lock_static:
            self._static_lock_candidate_frames += 1
        else:
            self._static_lock_candidate_frames = 0
        if ready_to_lock_static and self._static_lock_candidate_frames >= max(
            int(self._param("static_frames")), 1
        ):
            self._locked_cloud = persistent.copy()
            self._locked_ignored_thin = ignored_thin.copy()
            self._locked_source_stamp_s = depth_stamp_s
            self.get_logger().info(
                "locked static target cloud in base frame: "
                f"points={persistent.shape[0]} source_stamp={depth_stamp_s:.9f} "
                f"frames={self._static_lock_candidate_frames}"
            )
        stamp = self._depth.header.stamp
        frame_id = str(self._param("base_frame"))
        self._cloud_pub.publish(pointcloud2_xyz(persistent, stamp=stamp, frame_id=frame_id))
        self._last_published_depth_stamp = stamp_key
        self._ignored_thin_pub.publish(
            pointcloud2_xyz(ignored_thin, stamp=stamp, frame_id=frame_id)
        )
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
            f"depth={pts_all.shape[0]} pixel_stride={pixel_stride} "
            f"selection={selection_mode} target_mask_valid={target_mask_valid} "
            f"target_mask_px={target_mask_pixels} "
            f"robot_mask_received={self._robot_mask is not None} "
            f"self_rm={n_self + n_capsule_self + n_wrist_box} "
            f"capsule_self_rm={n_capsule_self} "
            f"wrist_box_rm={n_wrist_box} "
            f"joint_sync_dt={joint_sync_delta:.4f}s workspace={pts_workspace.shape[0]} "
            f"table_rm={n_table} raw_obstacle={pts.shape[0]} persistent={persistent.shape[0]} "
            f"thin_components={thin_components} "
            f"thin_removed_components={thin_removed_components} "
            f"thin_removed_points={ignored_thin.shape[0]} thin_filter_ms={thin_ms:.2f} "
            f"voxels={len(self._persistence.records)} mode={mode} "
            f"frame={self._processed_frames}/{self._param('static_frames')} {bbox_text}"
        )
        self._status_pub.publish(String(data=status))
        self.get_logger().info(status)
        self.get_logger().info("geometry=" + json.dumps({
            "source_stamp_s": depth_stamp_s, "mode": mode,
            "locked": self._locked_cloud is not None,
            "optical_selected": optical_stats, "base_before_filters": base_stats,
            "base_output": cloud_stats(persistent),
            "before_self_clearance_m": capsule_clearance(before_self, capsules),
            "output_clearance_m": capsule_clearance(persistent, capsules),
            "self_filter_margin_m": float(self._param("self_filter_margin_m")),
            "self_filter_capsules": [
                {"a": a.tolist(), "b": b.tolist(), "radius_m": r}
                for a, b, r in capsules
            ],
        }))


def cloud_stats(points: np.ndarray) -> dict:
    if len(points) == 0:
        return {"points": 0}
    return {"points": len(points), "centroid_m": points.mean(axis=0).tolist(),
            "bbox_min_m": points.min(axis=0).tolist(),
            "bbox_max_m": points.max(axis=0).tolist()}


def capsule_clearance(points: np.ndarray, capsules: list) -> float | None:
    if not len(points) or not capsules:
        return None
    best = float("inf")
    for a, b, radius in capsules:
        ab = b - a
        t = np.clip((points - a) @ ab / max(float(ab @ ab), 1e-20), 0, 1)
        best = min(best, float(np.linalg.norm(points - (a + t[:, None] * ab), axis=1).min()) - radius)
    return best


def main() -> None:
    rclpy.init()
    node = ObstacleCloudNode()
    try:
        executor = MultiThreadedExecutor(num_threads=2)
        executor.add_node(node)
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    except Exception:
        if rclpy.ok():
            raise
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
