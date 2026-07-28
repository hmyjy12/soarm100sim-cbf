from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re
import sys

import numpy as np


@dataclass
class PoseWxyz:
    pos: np.ndarray
    quat_wxyz: np.ndarray
    frame_id: str = "base"

    @classmethod
    def from_ros_pose(cls, msg) -> "PoseWxyz":
        return cls(
            pos=np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z], dtype=np.float64),
            quat_wxyz=np.array(
                [msg.pose.orientation.w, msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z],
                dtype=np.float64,
            ),
            frame_id=str(msg.header.frame_id),
        )

    def xyz_csv(self) -> str:
        return f"{self.pos[0]:.6f},{self.pos[1]:.6f},{self.pos[2]:.6f}"

    def quat_csv(self) -> str:
        q = self.quat_wxyz / max(float(np.linalg.norm(self.quat_wxyz)), 1e-12)
        return f"{q[0]:.8f},{q[1]:.8f},{q[2]:.8f},{q[3]:.8f}"


@dataclass
class MujocoExternalGraspConfig:
    repo_root: Path
    python_executable: str = "python"
    target_object: str = "cube"
    target_pos: str = "0.42,0.08,0.021"
    traj_log: str = "logs/ros2_policy_backend_grasp.jsonl"
    speed: float = 1.0
    headless: bool = False
    enable_avoidance: bool = False
    enable_internal_tracking: bool = True
    grasp_track_source: str = "wrist"
    grasp_track_max_delta: float = 0.020
    grasp_replan_max_attempts: int = 0
    extra_args: str = ""


@dataclass
class PlannedGraspCommand:
    pregrasp: PoseWxyz
    grasp: PoseWxyz
    tracking_reference: PoseWxyz | None = None
    gripper_width: float = 0.0


@dataclass
class ExecutionParseState:
    lines: list[str] = field(default_factory=list)
    lift_height: float = 0.0
    success_hint: bool = False
    stage: str = "STARTING"
    reason: str = ""

    def feed(self, line: str) -> None:
        self.lines.append(str(line))
        if "[grasp]" in line or "state=" in line:
            self.stage = stage_from_line(line)
            self.reason = line[-240:]
        m = re.search(r"target_lift=([-+0-9.]+)mm", line)
        if m:
            self.lift_height = float(m.group(1)) / 1000.0
        if "lift success" in line or "state=VERIFY" in line:
            self.success_hint = True

    def tail(self, n: int = 12) -> str:
        return "\n".join(self.lines[-int(n):])


def build_mujoco_external_grasp_cmd(cfg: MujocoExternalGraspConfig, grasp: PlannedGraspCommand) -> list[str]:
    cmd = [
        str(cfg.python_executable),
        "mujoco/play.py",
        "--episodes",
        "1",
        "--target-idx",
        "123",
        "--enable-grasp-chain",
        "--grasp-source",
        "external",
        "--external-pregrasp-pos",
        grasp.pregrasp.xyz_csv(),
        "--external-grasp-pos",
        grasp.grasp.xyz_csv(),
        "--external-grasp-quat",
        grasp.grasp.quat_csv(),
        "--external-gripper-width",
        f"{float(grasp.gripper_width):.6f}",
        "--grasp-target-object",
        str(cfg.target_object),
        "--grasp-target-pos",
        str(cfg.target_pos),
        "--traj-log",
        str(cfg.traj_log),
        "--stop-on-success",
        "--verbose",
        "--grasp-track-max-delta",
        f"{float(cfg.grasp_track_max_delta):.6f}",
        "--grasp-replan-max-attempts",
        str(int(cfg.grasp_replan_max_attempts)),
        "--speed",
        str(float(cfg.speed)),
    ]
    if cfg.enable_internal_tracking:
        cmd.extend(["--grasp-track-object", "--grasp-track-source", str(cfg.grasp_track_source)])
    else:
        cmd.append("--no-grasp-track-object")
    if cfg.headless:
        cmd.append("--headless")
    if cfg.enable_avoidance:
        cmd.extend(["--enable-obstacle", "--enable-sdf-cbf-qp"])
    extra = str(cfg.extra_args).strip()
    if extra:
        cmd.extend(extra.split())
    return cmd


def pose_to_base_from_calib(
    pose,
    *,
    repo_root: Path,
    calib_json: str | Path,
    input_camera_name: str,
    base_frame: str,
):
    frame = str(pose.header.frame_id).strip()
    if frame in ("", str(base_frame), "world", "map"):
        return pose
    calib_path = Path(calib_json)
    if not calib_path.is_absolute():
        calib_path = Path(repo_root) / calib_path
    data = json.loads(calib_path.read_text(encoding="utf-8"))
    cam_name = str(input_camera_name)
    T_mj = np.asarray(data["mounts"][cam_name]["T_parent_cam"], dtype=np.float64).reshape(4, 4)
    D = np.diag([1.0, -1.0, -1.0]).astype(np.float64)
    p_ros = np.array([pose.pose.position.x, pose.pose.position.y, pose.pose.position.z], dtype=np.float64)
    q_ros = [pose.pose.orientation.w, pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z]
    R_ros = rot_from_quat_wxyz(q_ros)
    p_mj = D @ p_ros
    R_mj = D @ R_ros
    p_base = T_mj[:3, :3] @ p_mj + T_mj[:3, 3]
    R_base = T_mj[:3, :3] @ R_mj
    return set_pose_like(pose, p_base, quat_from_rot_wxyz(R_base), str(base_frame))


def pose_to_base_from_mujoco_camera(
    pose,
    *,
    repo_root: Path,
    mjcf: str | Path,
    input_camera_name: str,
    base_frame: str,
):
    frame = str(pose.header.frame_id).strip()
    if frame in ("", str(base_frame), "world", "map"):
        return pose
    T_mj = mujoco_camera_transform(repo_root=repo_root, mjcf=mjcf, camera_name=input_camera_name)
    D = np.diag([1.0, -1.0, -1.0]).astype(np.float64)
    p_ros = np.array([pose.pose.position.x, pose.pose.position.y, pose.pose.position.z], dtype=np.float64)
    q_ros = [pose.pose.orientation.w, pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z]
    R_ros = rot_from_quat_wxyz(q_ros)
    p_mj = D @ p_ros
    R_mj = D @ R_ros
    p_base = T_mj[:3, :3] @ p_mj + T_mj[:3, 3]
    R_base = T_mj[:3, :3] @ R_mj
    return set_pose_like(pose, p_base, quat_from_rot_wxyz(R_base), str(base_frame))


def mujoco_camera_transform(*, repo_root: Path, mjcf: str | Path, camera_name: str) -> np.ndarray:
    repo = Path(repo_root).expanduser().resolve()
    mjcf_path = Path(mjcf)
    if not mjcf_path.is_absolute():
        mjcf_path = repo / mjcf_path
    old_path = list(sys.path)
    sys.path = [p for p in sys.path if Path(p or ".").resolve() != repo]
    try:
        import mujoco  # type: ignore
    finally:
        sys.path = old_path
    sys.path.insert(0, str(repo / "mujoco"))
    try:
        from calib import T_world_cam  # type: ignore

        model = mujoco.MjModel.from_xml_path(str(mjcf_path))
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        return np.asarray(T_world_cam(model, data, str(camera_name)), dtype=np.float64).reshape(4, 4)
    finally:
        try:
            sys.path.remove(str(repo / "mujoco"))
        except ValueError:
            pass


def points_to_base_from_calib(
    points: np.ndarray,
    *,
    repo_root: Path,
    calib_json: str | Path,
    input_camera_name: str,
) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return np.zeros((0, 3), dtype=np.float32)
    calib_path = Path(calib_json)
    if not calib_path.is_absolute():
        calib_path = Path(repo_root) / calib_path
    data = json.loads(calib_path.read_text(encoding="utf-8"))
    T_mj = np.asarray(data["mounts"][str(input_camera_name)]["T_parent_cam"], dtype=np.float64).reshape(4, 4)
    D = np.diag([1.0, -1.0, -1.0]).astype(np.float64)
    pts_mj = (D @ pts.T).T
    pts_base = (T_mj[:3, :3] @ pts_mj.T).T + T_mj[:3, 3]
    return pts_base.astype(np.float32)


def points_to_base_from_mujoco_camera(
    points: np.ndarray,
    *,
    repo_root: Path,
    mjcf: str | Path,
    input_camera_name: str,
) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return np.zeros((0, 3), dtype=np.float32)
    T_mj = mujoco_camera_transform(repo_root=repo_root, mjcf=mjcf, camera_name=input_camera_name)
    D = np.diag([1.0, -1.0, -1.0]).astype(np.float64)
    pts_mj = (D @ pts.T).T
    pts_base = (T_mj[:3, :3] @ pts_mj.T).T + T_mj[:3, 3]
    return pts_base.astype(np.float32)


def rot_from_quat_wxyz(q) -> np.ndarray:
    w, x, y, z = [float(v) for v in q]
    n = max(float(np.sqrt(w * w + x * x + y * y + z * z)), 1e-12)
    w, x, y, z = w / n, x / n, y / n, z / n
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float64,
    )


def quat_from_rot_wxyz(R: np.ndarray) -> tuple[float, float, float, float]:
    m = np.asarray(R, dtype=np.float64).reshape(3, 3)
    tr = float(np.trace(m))
    if tr > 0.0:
        s = np.sqrt(tr + 1.0) * 2.0
        q = np.array([0.25 * s, (m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s])
    else:
        i = int(np.argmax(np.diag(m)))
        if i == 0:
            s = np.sqrt(max(1.0 + m[0, 0] - m[1, 1] - m[2, 2], 1e-12)) * 2.0
            q = np.array([(m[2, 1] - m[1, 2]) / s, 0.25 * s, (m[0, 1] + m[1, 0]) / s, (m[0, 2] + m[2, 0]) / s])
        elif i == 1:
            s = np.sqrt(max(1.0 + m[1, 1] - m[0, 0] - m[2, 2], 1e-12)) * 2.0
            q = np.array([(m[0, 2] - m[2, 0]) / s, (m[0, 1] + m[1, 0]) / s, 0.25 * s, (m[1, 2] + m[2, 1]) / s])
        else:
            s = np.sqrt(max(1.0 + m[2, 2] - m[0, 0] - m[1, 1], 1e-12)) * 2.0
            q = np.array([(m[1, 0] - m[0, 1]) / s, (m[0, 2] + m[2, 0]) / s, (m[1, 2] + m[2, 1]) / s, 0.25 * s])
    q = q / max(float(np.linalg.norm(q)), 1e-12)
    return float(q[0]), float(q[1]), float(q[2]), float(q[3])


def set_pose_like(msg, pos: np.ndarray, quat_wxyz: tuple[float, float, float, float], frame_id: str):
    out = type(msg)()
    out.header.stamp = msg.header.stamp
    out.header.frame_id = frame_id
    out.pose.position.x = float(pos[0])
    out.pose.position.y = float(pos[1])
    out.pose.position.z = float(pos[2])
    out.pose.orientation.w = float(quat_wxyz[0])
    out.pose.orientation.x = float(quat_wxyz[1])
    out.pose.orientation.y = float(quat_wxyz[2])
    out.pose.orientation.z = float(quat_wxyz[3])
    return out


def stage_from_line(line: str) -> str:
    m = re.search(r"state=([A-Z_]+)", line)
    if m:
        return m.group(1)
    for stage in ("pregrasp", "final", "close", "lift", "replan"):
        if stage in line.lower():
            return stage.upper()
    return "MUJOCO"
