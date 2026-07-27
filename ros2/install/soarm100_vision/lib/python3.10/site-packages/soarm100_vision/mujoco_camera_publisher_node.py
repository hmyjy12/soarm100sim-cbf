from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import Bool


def _rgb_msg(rgb: np.ndarray, *, stamp, frame_id: str) -> Image:
    arr = np.asarray(rgb, dtype=np.uint8)
    msg = Image()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.height = int(arr.shape[0])
    msg.width = int(arr.shape[1])
    msg.encoding = "rgb8"
    msg.is_bigendian = False
    msg.step = int(arr.shape[1]) * 3
    msg.data = np.ascontiguousarray(arr).tobytes()
    return msg


def _depth_msg(depth: np.ndarray, *, stamp, frame_id: str) -> Image:
    arr = np.asarray(depth, dtype=np.float32)
    msg = Image()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.height = int(arr.shape[0])
    msg.width = int(arr.shape[1])
    msg.encoding = "32FC1"
    msg.is_bigendian = False
    msg.step = int(arr.shape[1]) * 4
    msg.data = np.ascontiguousarray(arr).tobytes()
    return msg


def _mask_msg(mask: np.ndarray, *, stamp, frame_id: str) -> Image:
    arr = np.asarray(mask, dtype=np.uint8)
    msg = Image()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.height = int(arr.shape[0])
    msg.width = int(arr.shape[1])
    msg.encoding = "mono8"
    msg.is_bigendian = False
    msg.step = int(arr.shape[1])
    msg.data = np.ascontiguousarray(arr).tobytes()
    return msg


def _body_descendants(model, root_body_id: int) -> set[int]:
    descendants = {int(root_body_id)}
    changed = True
    while changed:
        changed = False
        for body_id in range(int(model.nbody)):
            if body_id not in descendants and int(model.body_parentid[body_id]) in descendants:
                descendants.add(body_id)
                changed = True
    return descendants


def _robot_geom_ids(mujoco, model, root_body: str = "base") -> set[int]:
    root = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, root_body)
    if root < 0:
        return set()
    bodies = _body_descendants(model, int(root))
    return {
        int(geom_id)
        for geom_id in range(int(model.ngeom))
        if int(model.geom_bodyid[geom_id]) in bodies
    }


def _robot_mask_from_segmentation(segmentation: np.ndarray, robot_geom_ids: set[int]) -> np.ndarray:
    seg = np.asarray(segmentation)
    if seg.ndim != 3 or seg.shape[2] < 1 or not robot_geom_ids:
        return np.zeros(seg.shape[:2], dtype=np.uint8)
    geom_ids = seg[:, :, 0].astype(np.int32)
    return (np.isin(geom_ids, np.fromiter(robot_geom_ids, dtype=np.int32)) * 255).astype(
        np.uint8
    )


def _camera_info(*, stamp, frame_id: str, width: int, height: int, fovy_deg: float) -> CameraInfo:
    fy = height / (2.0 * np.tan(np.deg2rad(float(fovy_deg)) / 2.0))
    fx = fy
    cx = (width - 1) / 2.0
    cy = (height - 1) / 2.0
    msg = CameraInfo()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.width = int(width)
    msg.height = int(height)
    msg.k = [float(fx), 0.0, float(cx), 0.0, float(fy), float(cy), 0.0, 0.0, 1.0]
    msg.p = [float(fx), 0.0, float(cx), 0.0, 0.0, float(fy), float(cy), 0.0, 0.0, 0.0, 1.0, 0.0]
    msg.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    msg.distortion_model = "plumb_bob"
    msg.d = [0.0, 0.0, 0.0, 0.0, 0.0]
    return msg


class MujocoCameraPublisherNode(Node):
    """Publish MuJoCo scene/wrist cameras as ROS2 RGB-D topics."""

    def __init__(self) -> None:
        super().__init__("soarm100_mujoco_camera_publisher")
        self.declare_parameter("repo_root", str(Path(__file__).resolve().parents[3]))
        self.declare_parameter("mjcf", "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml")
        self.declare_parameter("target_object", "cube")
        self.declare_parameter("target_pos", "0.42,0.08,0.022")
        self.declare_parameter("enable_obstacle", False)
        self.declare_parameter("obstacle_body", "obstacle_rod_mount")
        self.declare_parameter("obstacle_pos", "0.16,0.09,0.02")
        self.declare_parameter("width", 640)
        self.declare_parameter("height", 480)
        self.declare_parameter("publish_rate_hz", 10.0)
        self.declare_parameter("scene_burst_frames", 5)
        self.declare_parameter("publish_wrist_rgb", False)
        self.declare_parameter("step_sim", True)
        self.declare_parameter("scene_rgb_topic", "/camera/color/image_raw")
        self.declare_parameter("scene_depth_topic", "/camera/depth/image_rect_raw")
        self.declare_parameter("scene_info_topic", "/camera/color/camera_info")
        self.declare_parameter("robot_mask_topic", "/robot/mask")
        self.declare_parameter("wrist_rgb_topic", "/wrist/color/image_raw")
        self.declare_parameter("wrist_info_topic", "/wrist/color/camera_info")
        self.declare_parameter("backend_camera_active_topic", "/mujoco/backend_camera_active")
        self.declare_parameter(
            "camera_paused_topic", "/mujoco/standalone_camera_paused"
        )
        self._backend_camera_active = False
        self._published_scene_frames = 0

        repo = Path(str(self.get_parameter("repo_root").value)).expanduser().resolve()
        old_path = list(sys.path)
        sys.path = [p for p in sys.path if Path(p or ".").resolve() != repo]
        import mujoco  # type: ignore

        sys.path = old_path
        sys.path.insert(0, str(repo / "mujoco"))
        from camera import MujocoCameraRig  # type: ignore
        from constants import SCENE_DEPTH_CAM, WRIST_RGB_CAM  # type: ignore

        mjcf = Path(str(self.get_parameter("mjcf").value))
        if not mjcf.is_absolute():
            mjcf = repo / mjcf
        self._mujoco = mujoco
        self._model = self._mujoco.MjModel.from_xml_path(str(mjcf))
        self._data = self._mujoco.MjData(self._model)
        self._configure_grasp_targets()
        self._set_body_pos(self._selected_target_body, self._parse_vec3(str(self.get_parameter("target_pos").value)))
        self._configure_obstacle()
        self._settle_object(0.75)
        self._mujoco.mj_forward(self._model, self._data)
        self._scene_cam = SCENE_DEPTH_CAM
        self._wrist_cam = WRIST_RGB_CAM
        self._rig_cls = MujocoCameraRig
        self._rig = MujocoCameraRig(
            self._model,
            width=int(self.get_parameter("width").value),
            height=int(self.get_parameter("height").value),
        )
        self._robot_geom_ids = _robot_geom_ids(self._mujoco, self._model)
        self._scene_rgb_pub = self.create_publisher(Image, str(self.get_parameter("scene_rgb_topic").value), 1)
        self._scene_depth_pub = self.create_publisher(Image, str(self.get_parameter("scene_depth_topic").value), 1)
        self._scene_info_pub = self.create_publisher(CameraInfo, str(self.get_parameter("scene_info_topic").value), 1)
        self._robot_mask_pub = self.create_publisher(
            Image, str(self.get_parameter("robot_mask_topic").value), 1
        )
        self._wrist_rgb_pub = self.create_publisher(Image, str(self.get_parameter("wrist_rgb_topic").value), 1)
        self._wrist_info_pub = self.create_publisher(CameraInfo, str(self.get_parameter("wrist_info_topic").value), 1)
        self._paused_pub = self.create_publisher(
            Bool, str(self.get_parameter("camera_paused_topic").value), 1
        )
        self.create_subscription(
            Bool,
            str(self.get_parameter("backend_camera_active_topic").value),
            self._on_backend_camera_active,
            1,
        )
        period = 1.0 / max(float(self.get_parameter("publish_rate_hz").value), 1e-3)
        self.create_timer(period, self._tick)
        self.get_logger().info(
            f"MuJoCo camera publisher ready: mjcf={mjcf} scene={self._scene_cam} wrist={self._wrist_cam} "
            f"target={self._selected_target_body} pos={self.get_parameter('target_pos').value} "
            f"obstacle={self.get_parameter('enable_obstacle').value} "
            f"{self.get_parameter('obstacle_body').value}@{self.get_parameter('obstacle_pos').value}"
        )

    def _tick(self) -> None:
        if self._backend_camera_active:
            return
        if self._rig is None:
            self._rig = self._rig_cls(
                self._model,
                width=int(self.get_parameter("width").value),
                height=int(self.get_parameter("height").value),
            )
        burst_frames = max(int(self.get_parameter("scene_burst_frames").value), 1)
        if self._published_scene_frames >= burst_frames:
            return
        if (
            self._scene_rgb_pub.get_subscription_count() == 0
            or self._scene_depth_pub.get_subscription_count() == 0
        ):
            return
        if bool(self.get_parameter("step_sim").value):
            self._mujoco.mj_step(self._model, self._data)
        stamp = self.get_clock().now().to_msg()
        w = int(self.get_parameter("width").value)
        h = int(self.get_parameter("height").value)
        scene_frame = "scene_depth_optical"
        wrist_frame = "wrist_rgb_optical"

        scene_rgb = self._rig.capture_rgb(self._data, self._scene_cam)
        scene_depth = self._rig.capture_depth_m(self._data, self._scene_cam)
        scene_seg = self._rig.capture_segmentation(self._data, self._scene_cam)
        robot_mask = _robot_mask_from_segmentation(scene_seg, self._robot_geom_ids)

        scene_id = self._mujoco.mj_name2id(self._model, self._mujoco.mjtObj.mjOBJ_CAMERA, self._scene_cam)
        self._scene_rgb_pub.publish(_rgb_msg(scene_rgb, stamp=stamp, frame_id=scene_frame))
        self._robot_mask_pub.publish(
            _mask_msg(robot_mask, stamp=stamp, frame_id=scene_frame)
        )
        self._scene_depth_pub.publish(_depth_msg(scene_depth, stamp=stamp, frame_id=scene_frame))
        self._scene_info_pub.publish(
            _camera_info(stamp=stamp, frame_id=scene_frame, width=w, height=h, fovy_deg=float(self._model.cam_fovy[scene_id]))
        )
        if bool(self.get_parameter("publish_wrist_rgb").value):
            wrist_rgb = self._rig.capture_rgb(self._data, self._wrist_cam)
            wrist_id = self._mujoco.mj_name2id(
                self._model, self._mujoco.mjtObj.mjOBJ_CAMERA, self._wrist_cam
            )
            self._wrist_rgb_pub.publish(
                _rgb_msg(wrist_rgb, stamp=stamp, frame_id=wrist_frame)
            )
            self._wrist_info_pub.publish(
                _camera_info(
                    stamp=stamp,
                    frame_id=wrist_frame,
                    width=w,
                    height=h,
                    fovy_deg=float(self._model.cam_fovy[wrist_id]),
                )
            )
        self._published_scene_frames += 1
        self.get_logger().info(
            f"scene initialization frame={self._published_scene_frames}/{burst_frames} "
            f"sim_time={float(self._data.time):.3f}s "
            f"robot_mask_pixels={int(np.count_nonzero(robot_mask))}"
        )

    def _on_backend_camera_active(self, msg: Bool) -> None:
        active = bool(msg.data)
        if active != self._backend_camera_active:
            self._backend_camera_active = active
            if active:
                if self._rig is not None:
                    self._rig.close()
                    self._rig = None
            else:
                self._published_scene_frames = 0
                if self._rig is None:
                    self._rig = self._rig_cls(
                        self._model,
                        width=int(self.get_parameter("width").value),
                        height=int(self.get_parameter("height").value),
                    )
            self.get_logger().info(f"standalone camera publishing {'paused' if active else 'resumed'}")
        self._paused_pub.publish(Bool(data=active))

    def destroy_node(self) -> bool:
        if self._rig is not None:
            self._rig.close()
            self._rig = None
        return super().destroy_node()

    @staticmethod
    def _targets() -> dict[str, tuple[str, str]]:
        return {
            "cube": ("target_object", "target_object_geom"),
            "bottle": ("target_bottle", "target_bottle_geom"),
            "sphere": ("target_sphere", "target_sphere_geom"),
        }

    @staticmethod
    def _parse_vec3(raw: str) -> np.ndarray:
        vals = [float(x) for x in str(raw).replace(",", " ").split()]
        if len(vals) != 3:
            raise ValueError(f"expected x,y,z, got {raw!r}")
        return np.asarray(vals, dtype=np.float64)

    def _configure_grasp_targets(self) -> None:
        obj = str(self.get_parameter("target_object").value).strip().lower()
        body, selected_geom = self._targets().get(obj, self._targets()["cube"])
        self._selected_target_body = body
        for body_name, geom_name in self._targets().values():
            gid = self._mujoco.mj_name2id(self._model, self._mujoco.mjtObj.mjOBJ_GEOM, geom_name)
            selected = geom_name == selected_geom
            if gid >= 0:
                self._model.geom_contype[int(gid)] = 1 if selected else 0
                self._model.geom_conaffinity[int(gid)] = 1 if selected else 0
                self._model.geom_rgba[int(gid)] = np.array(
                    [1.0, 0.05, 0.05, 1.0 if selected else 0.0],
                    dtype=np.float32,
                )
            if not selected:
                self._set_body_pos(body_name, np.array([0.0, 0.0, -1.0], dtype=np.float64))

    def _configure_obstacle(self) -> None:
        body_name = str(self.get_parameter("obstacle_body").value).strip()
        if not body_name:
            return
        bid = self._mujoco.mj_name2id(self._model, self._mujoco.mjtObj.mjOBJ_BODY, body_name)
        if bid < 0:
            if bool(self.get_parameter("enable_obstacle").value):
                raise RuntimeError(f"enabled obstacle body not found in mjcf: {body_name}")
            return
        if bool(self.get_parameter("enable_obstacle").value):
            self._set_body_pos(body_name, self._parse_vec3(str(self.get_parameter("obstacle_pos").value)))
        else:
            self._set_body_pos(body_name, np.array([0.0, 0.0, -1.0], dtype=np.float64))

    def _set_body_pos(self, body_name: str, pos: np.ndarray) -> None:
        bid = self._mujoco.mj_name2id(self._model, self._mujoco.mjtObj.mjOBJ_BODY, str(body_name))
        if bid < 0:
            return
        target = np.asarray(pos, dtype=np.float64).reshape(3)
        free_jid = -1
        for jid in range(int(self._model.njnt)):
            if int(self._model.jnt_bodyid[jid]) == int(bid) and int(self._model.jnt_type[jid]) == int(self._mujoco.mjtJoint.mjJNT_FREE):
                free_jid = int(jid)
                break
        if free_jid >= 0:
            qadr = int(self._model.jnt_qposadr[free_jid])
            dadr = int(self._model.jnt_dofadr[free_jid])
            self._data.qpos[qadr : qadr + 3] = target
            self._data.qpos[qadr + 3 : qadr + 7] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
            self._data.qvel[dadr : dadr + 6] = 0.0
        else:
            self._model.body_pos[int(bid)] = target
        self._mujoco.mj_forward(self._model, self._data)

    def _settle_object(self, seconds: float) -> None:
        for _ in range(max(0, int(round(float(seconds) / float(self._model.opt.timestep))))):
            self._mujoco.mj_step(self._model, self._data)
        self._data.qvel[:] = 0.0
        self._mujoco.mj_forward(self._model, self._data)


def main() -> None:
    rclpy.init()
    node = MujocoCameraPublisherNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
