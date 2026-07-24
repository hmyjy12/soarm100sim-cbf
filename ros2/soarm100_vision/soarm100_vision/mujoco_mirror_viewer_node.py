from __future__ import annotations

from pathlib import Path
import sys
import threading

import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class MujocoMirrorViewerNode(Node):
    """Display the backend model state in an isolated GLFW process."""

    def __init__(self) -> None:
        super().__init__("soarm100_mujoco_mirror_viewer")
        self.declare_parameter("repo_root", str(Path(__file__).resolve().parents[3]))
        self.declare_parameter(
            "mjcf", "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"
        )
        self.declare_parameter("sim_state_topic", "/mujoco/sim_state")
        self.declare_parameter("obstacle_body", "obstacle_rod_mount")
        self.declare_parameter("obstacle_pos", "0.16,0.09,0.02")
        self.declare_parameter("obstacle_motion", "none")
        self.declare_parameter("obstacle_motion_amp", "0.03,0.00,0.00")
        self.declare_parameter("obstacle_motion_period", 5.0)

        repo = Path(str(self.get_parameter("repo_root").value)).expanduser().resolve()
        mjcf = Path(str(self.get_parameter("mjcf").value))
        if not mjcf.is_absolute():
            mjcf = repo / mjcf

        old_path = list(sys.path)
        sys.path = [p for p in sys.path if Path(p or ".").resolve() != repo]
        import mujoco  # type: ignore
        import mujoco.viewer  # type: ignore

        sys.path = old_path
        self._mujoco = mujoco
        self._model = mujoco.MjModel.from_xml_path(str(mjcf))
        self._data = mujoco.MjData(self._model)
        self._obstacle_body_id = mujoco.mj_name2id(
            self._model,
            mujoco.mjtObj.mjOBJ_BODY,
            str(self.get_parameter("obstacle_body").value),
        )
        self._obstacle_pos = self._vec3(
            str(self.get_parameter("obstacle_pos").value)
        )
        self._obstacle_amp = self._vec3(
            str(self.get_parameter("obstacle_motion_amp").value)
        )
        self._pending: np.ndarray | None = None
        self._pending_time = 0.0
        self._lock = threading.Lock()
        self._viewer = mujoco.viewer.launch_passive(self._model, self._data)
        self.create_subscription(
            Float64MultiArray,
            str(self.get_parameter("sim_state_topic").value),
            self._on_state,
            1,
        )
        self.create_timer(1.0 / 60.0, self._sync)
        self.get_logger().info(
            f"MuJoCo mirror viewer ready: "
            f"state={self.get_parameter('sim_state_topic').value}"
        )

    def _on_state(self, msg: Float64MultiArray) -> None:
        values = np.asarray(msg.data, dtype=np.float64)
        if values.size != self._model.nq + 1:
            self.get_logger().error(
                f"state size mismatch: got={values.size - 1} "
                f"expected={self._model.nq}"
            )
            return
        with self._lock:
            self._pending_time = float(values[0])
            self._pending = values[1:].copy()

    def _sync(self) -> None:
        if not self._viewer.is_running():
            return
        with self._lock:
            qpos = self._pending
            sim_time = self._pending_time
            self._pending = None
        if qpos is not None:
            self._data.qpos[:] = qpos
            self._data.time = sim_time
            self._update_obstacle(sim_time)
            self._mujoco.mj_forward(self._model, self._data)
        self._viewer.sync()

    @staticmethod
    def _vec3(value: str) -> np.ndarray:
        values = [float(item) for item in value.replace(",", " ").split()]
        if len(values) != 3:
            raise ValueError(f"expected x,y,z, got {value!r}")
        return np.asarray(values, dtype=np.float64)

    def _update_obstacle(self, sim_time: float) -> None:
        if self._obstacle_body_id < 0:
            return
        kind = str(self.get_parameter("obstacle_motion").value).strip().lower()
        period = max(float(self.get_parameter("obstacle_motion_period").value), 1.0e-6)
        theta = 2.0 * np.pi * float(sim_time) / period
        if kind == "line":
            pos = self._obstacle_pos + self._obstacle_amp * np.sin(theta)
        elif kind == "circle":
            pos = self._obstacle_pos + np.array(
                [
                    self._obstacle_amp[0] * np.cos(theta),
                    self._obstacle_amp[1] * np.sin(theta),
                    self._obstacle_amp[2] * np.sin(theta),
                ],
                dtype=np.float64,
            )
        else:
            pos = self._obstacle_pos
        self._model.body_pos[self._obstacle_body_id] = pos

    def close(self) -> None:
        self._viewer.close()


def main() -> None:
    rclpy.init()
    node = MujocoMirrorViewerNode()
    try:
        rclpy.spin(node)
    finally:
        node.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
