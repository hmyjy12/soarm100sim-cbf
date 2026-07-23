from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


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
        self.declare_parameter("step_sim", True)
        self.declare_parameter("scene_rgb_topic", "/camera/color/image_raw")
        self.declare_parameter("scene_depth_topic", "/camera/depth/image_rect_raw")
        self.declare_parameter("scene_info_topic", "/camera/color/camera_info")
        self.declare_parameter("wrist_rgb_topic", "/wrist/color/image_raw")
        self.declare_parameter("wrist_depth_topic", "/wrist/depth/image_rect_raw")
        self.declare_parameter("wrist_info_topic", "/wrist/depth/camera_info")

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
        self._rig = MujocoCameraRig(
            self._model,
            width=int(self.get_parameter("width").value),
            height=int(self.get_parameter("height").value),
        )
        self._scene_rgb_pub = self.create_publisher(Image, str(self.get_parameter("scene_rgb_topic").value), 1)
        self._scene_depth_pub = self.create_publisher(Image, str(self.get_parameter("scene_depth_topic").value), 1)
        self._scene_info_pub = self.create_publisher(CameraInfo, str(self.get_parameter("scene_info_topic").value), 1)
        self._wrist_rgb_pub = self.create_publisher(Image, str(self.get_parameter("wrist_rgb_topic").value), 1)
        self._wrist_depth_pub = self.create_publisher(Image, str(self.get_parameter("wrist_depth_topic").value), 1)
        self._wrist_info_pub = self.create_publisher(CameraInfo, str(self.get_parameter("wrist_info_topic").value), 1)
        period = 1.0 / max(float(self.get_parameter("publish_rate_hz").value), 1e-3)
        self.create_timer(period, self._tick)
        self.get_logger().info(
            f"MuJoCo camera publisher ready: mjcf={mjcf} scene={self._scene_cam} wrist={self._wrist_cam} "
            f"target={self._selected_target_body} pos={self.get_parameter('target_pos').value} "
            f"obstacle={self.get_parameter('enable_obstacle').value} "
            f"{self.get_parameter('obstacle_body').value}@{self.get_parameter('obstacle_pos').value}"
        )

    def _tick(self) -> None:
        if bool(self.get_parameter("step_sim").value):
            self._mujoco.mj_step(self._model, self._data)
        stamp = self.get_clock().now().to_msg()
        w = int(self.get_parameter("width").value)
        h = int(self.get_parameter("height").value)
        scene_frame = "scene_depth_optical"
        wrist_frame = "wrist_rgb_optical"

        scene_rgb = self._rig.capture_rgb(self._data, self._scene_cam)
        scene_depth = self._rig.capture_depth_m(self._data, self._scene_cam)
        wrist_rgb = self._rig.capture_rgb(self._data, self._wrist_cam)
        wrist_depth = self._rig.capture_depth_m(self._data, self._wrist_cam)

        scene_id = self._mujoco.mj_name2id(self._model, self._mujoco.mjtObj.mjOBJ_CAMERA, self._scene_cam)
        wrist_id = self._mujoco.mj_name2id(self._model, self._mujoco.mjtObj.mjOBJ_CAMERA, self._wrist_cam)
        self._scene_rgb_pub.publish(_rgb_msg(scene_rgb, stamp=stamp, frame_id=scene_frame))
        self._scene_depth_pub.publish(_depth_msg(scene_depth, stamp=stamp, frame_id=scene_frame))
        self._scene_info_pub.publish(
            _camera_info(stamp=stamp, frame_id=scene_frame, width=w, height=h, fovy_deg=float(self._model.cam_fovy[scene_id]))
        )
        self._wrist_rgb_pub.publish(_rgb_msg(wrist_rgb, stamp=stamp, frame_id=wrist_frame))
        self._wrist_depth_pub.publish(_depth_msg(wrist_depth, stamp=stamp, frame_id=wrist_frame))
        self._wrist_info_pub.publish(
            _camera_info(stamp=stamp, frame_id=wrist_frame, width=w, height=h, fovy_deg=float(self._model.cam_fovy[wrist_id]))
        )

    def destroy_node(self) -> bool:
        self._rig.close()
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
        rclpy.shutdown()


if __name__ == "__main__":
    main()
