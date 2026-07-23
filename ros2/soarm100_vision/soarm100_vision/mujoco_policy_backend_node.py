from __future__ import annotations

import asyncio
import os
from pathlib import Path
import threading

import numpy as np

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import PointCloud2

from soarm100_interfaces.action import ExecutePlannedGrasp
from soarm100_vision.vision_utils import pointcloud2_to_xyz
from soarm100_vision.policy_backend_core import (
    ExecutionParseState,
    MujocoExternalGraspConfig,
    PlannedGraspCommand,
    PoseWxyz,
    build_mujoco_external_grasp_cmd,
    points_to_base_from_calib,
    points_to_base_from_mujoco_camera,
    pose_to_base_from_calib,
    pose_to_base_from_mujoco_camera,
)
from soarm100_vision.mujoco_inprocess_runner import MujocoInProcessRunner, MujocoRunnerConfig


def _pose_summary(label: str, pose: PoseStamped) -> str:
    p = pose.pose.position
    q = pose.pose.orientation
    return (
        f"{label}[frame={pose.header.frame_id or '<empty>'} "
        f"pos=({p.x:+.3f},{p.y:+.3f},{p.z:+.3f}) "
        f"quat=({q.w:+.3f},{q.x:+.3f},{q.y:+.3f},{q.z:+.3f})]"
    )


class MujocoPolicyBackendNode(Node):
    """Execute planned pregrasp/final poses through the existing MuJoCo policy loop."""

    def __init__(self) -> None:
        super().__init__("soarm100_mujoco_policy_backend")
        self.declare_parameter("repo_root", str(Path(__file__).resolve().parents[3]))
        self.declare_parameter("python_executable", "python")
        self.declare_parameter("default_target_object", "cube")
        self.declare_parameter("default_target_pos", "0.42,0.08,0.021")
        self.declare_parameter("default_traj_log", "logs/ros2_policy_backend_grasp.jsonl")
        self.declare_parameter("enable_obstacle", False)
        self.declare_parameter("obstacle_body", "obstacle_rod_mount")
        self.declare_parameter("obstacle_pos", "0.16,0.09,0.02")
        self.declare_parameter("backend_mode", "subprocess")
        self.declare_parameter("inprocess_viewer", False)
        self.declare_parameter("mjcf", "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml")
        self.declare_parameter("checkpoint", "rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt")
        self.declare_parameter("calib_json", "logs/calib/camera_calib.json")
        self.declare_parameter("use_sim_camera_extrinsics", True)
        self.declare_parameter("input_camera_name", "scene_depth")
        self.declare_parameter("tracking_topic", "/target/tracked_center")
        self.declare_parameter("tracking_camera_name", "wrist_rgb")
        self.declare_parameter("obstacle_cloud_topic", "/obstacle/cloud")
        self.declare_parameter("obstacle_camera_name", "scene_depth")
        self.declare_parameter("base_frame", "base")
        self.declare_parameter("speed", 0.5)
        self.declare_parameter("headless", False)
        self.declare_parameter("timeout_s", 90.0)
        self.declare_parameter("enable_internal_tracking", True)
        self.declare_parameter("grasp_track_source", "wrist")
        self.declare_parameter("grasp_track_max_delta", 0.020)
        self.declare_parameter("grasp_replan_max_attempts", 0)
        self.declare_parameter("extra_args", "")
        self._lock = threading.Lock()
        self._tracked_pos_base: np.ndarray | None = None
        self._obstacle_points_base = np.zeros((0, 3), dtype=np.float32)
        self.create_subscription(PoseStamped, str(self.get_parameter("tracking_topic").value), self._on_tracking, 1)
        self.create_subscription(PointCloud2, str(self.get_parameter("obstacle_cloud_topic").value), self._on_obstacle_cloud, 1)
        self._server = ActionServer(
            self,
            ExecutePlannedGrasp,
            "execute_planned_grasp",
            execute_callback=self._execute,
            goal_callback=self._goal,
            cancel_callback=self._cancel,
        )
        self.get_logger().info("MuJoCo policy backend ready: action=execute_planned_grasp")

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _goal(self, _goal_request: ExecutePlannedGrasp.Goal) -> GoalResponse:
        return GoalResponse.ACCEPT

    def _cancel(self, _goal_handle) -> CancelResponse:
        return CancelResponse.ACCEPT

    def _on_tracking(self, msg: PoseStamped) -> None:
        repo = Path(str(self._param("repo_root"))).expanduser().resolve()
        try:
            converted = pose_to_base_from_calib(
                msg,
                repo_root=repo,
                calib_json=str(self._param("calib_json")),
                input_camera_name=str(self._param("tracking_camera_name")),
                base_frame=str(self._param("base_frame")),
            )
            p = converted.pose.position
            with self._lock:
                self._tracked_pos_base = np.array([p.x, p.y, p.z], dtype=np.float64)
        except Exception as exc:
            self.get_logger().warn(f"tracking pose conversion failed: {exc}")

    def _on_obstacle_cloud(self, msg: PointCloud2) -> None:
        repo = Path(str(self._param("repo_root"))).expanduser().resolve()
        try:
            pts = pointcloud2_to_xyz(msg)
            frame = str(msg.header.frame_id).strip()
            if frame not in ("", str(self._param("base_frame")), "world", "map"):
                if bool(self._param("use_sim_camera_extrinsics")):
                    pts = points_to_base_from_mujoco_camera(
                        pts,
                        repo_root=repo,
                        mjcf=str(self._param("mjcf")),
                        input_camera_name=str(self._param("obstacle_camera_name")),
                    )
                else:
                    pts = points_to_base_from_calib(
                        pts,
                        repo_root=repo,
                        calib_json=str(self._param("calib_json")),
                        input_camera_name=str(self._param("obstacle_camera_name")),
                    )
            with self._lock:
                self._obstacle_points_base = np.asarray(pts, dtype=np.float32).reshape(-1, 3).copy()
        except Exception as exc:
            self.get_logger().warn(f"obstacle cloud conversion failed: {exc}")

    async def _execute(self, goal_handle):
        goal = goal_handle.request
        result = ExecutePlannedGrasp.Result()
        feedback = ExecutePlannedGrasp.Feedback()
        repo = Path(str(self._param("repo_root"))).expanduser().resolve()
        raw_pregrasp_pose = goal.pregrasp_pose
        raw_grasp_pose = goal.grasp_pose
        pregrasp_pose = self._pose_to_base(goal.pregrasp_pose, repo)
        grasp_pose = self._pose_to_base(goal.grasp_pose, repo)
        target_object = str(goal.target_object).strip() or str(self._param("default_target_object"))
        target_pos = str(goal.target_pos).strip() or str(self._param("default_target_pos"))
        traj_log = str(goal.traj_log).strip() or str(self._param("default_traj_log"))
        self.get_logger().info(
            "planned grasp pose conversion: "
            f"source={'sim_mjcf' if bool(self._param('use_sim_camera_extrinsics')) else 'calib_json'} "
            f"{_pose_summary('raw_pregrasp', raw_pregrasp_pose)} "
            f"{_pose_summary('raw_grasp', raw_grasp_pose)} "
            f"{_pose_summary('base_pregrasp', pregrasp_pose)} "
            f"{_pose_summary('base_grasp', grasp_pose)} "
            f"width={float(goal.gripper_width)*1000.0:.1f}mm "
            f"target={target_object}@{target_pos} traj_log={traj_log}"
        )
        cfg = MujocoExternalGraspConfig(
            repo_root=repo,
            python_executable=str(self._param("python_executable")),
            target_object=target_object,
            target_pos=target_pos,
            traj_log=traj_log,
            speed=float(self._param("speed")),
            headless=bool(self._param("headless")),
            enable_avoidance=bool(goal.enable_avoidance),
            enable_internal_tracking=bool(self._param("enable_internal_tracking")),
            grasp_track_source=str(self._param("grasp_track_source")),
            grasp_track_max_delta=float(self._param("grasp_track_max_delta")),
            grasp_replan_max_attempts=int(self._param("grasp_replan_max_attempts")),
            extra_args=str(self._param("extra_args")),
        )
        planned = PlannedGraspCommand(
            pregrasp=PoseWxyz.from_ros_pose(pregrasp_pose),
            grasp=PoseWxyz.from_ros_pose(grasp_pose),
            gripper_width=float(goal.gripper_width),
        )
        mode = str(self._param("backend_mode")).strip().lower()
        if mode == "inprocess":
            return self._execute_inprocess(goal_handle, planned, cfg)
        cmd = build_mujoco_external_grasp_cmd(cfg, planned)

        feedback.stage = "STARTING_MUJOCO"
        feedback.reason = (
            f"using converted AnyGrasp pose; {_pose_summary('base_pregrasp', pregrasp_pose)} "
            f"{_pose_summary('base_grasp', grasp_pose)} traj_log={traj_log}"
        )
        feedback.lift_height = 0.0
        goal_handle.publish_feedback(feedback)

        env = os.environ.copy()
        if bool(self._param("headless")):
            env.setdefault("MUJOCO_GL", "egl")
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(repo),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=env,
            )
            parsed = ExecutionParseState()
            assert proc.stdout is not None
            while True:
                if goal_handle.is_cancel_requested:
                    proc.terminate()
                    goal_handle.canceled()
                    result.success = False
                    result.reason = "cancelled"
                    result.return_code = 130
                    result.lift_height = parsed.lift_height
                    return result
                try:
                    raw = await asyncio.wait_for(proc.stdout.readline(), timeout=0.2)
                except asyncio.TimeoutError:
                    if proc.returncode is not None:
                        break
                    continue
                if not raw:
                    break
                line = raw.decode(errors="replace").rstrip()
                parsed.feed(line)
                if parsed.reason:
                    feedback.stage = parsed.stage
                    feedback.reason = parsed.reason
                    feedback.lift_height = parsed.lift_height
                    goal_handle.publish_feedback(feedback)
            rc = await asyncio.wait_for(proc.wait(), timeout=float(self._param("timeout_s")))
            result.return_code = int(rc)
            result.lift_height = float(parsed.lift_height)
            result.success = bool(rc == 0 and parsed.success_hint)
            result.reason = "ok" if result.success else f"mujoco_finished rc={rc} success_hint={parsed.success_hint}\n{parsed.tail()}"
            if result.success:
                goal_handle.succeed()
            else:
                goal_handle.abort()
        except Exception as exc:
            result.success = False
            result.reason = f"backend_failed:{exc}"
            result.return_code = 1
            result.lift_height = 0.0
            goal_handle.abort()
        return result

    def _execute_inprocess(self, goal_handle, planned: PlannedGraspCommand, cfg: MujocoExternalGraspConfig):
        result = ExecutePlannedGrasp.Result()
        feedback = ExecutePlannedGrasp.Feedback()
        feedback.stage = "STARTING_MUJOCO_INPROCESS"
        feedback.reason = (
            "using converted AnyGrasp pose in GraspStateMachine + MuJoCo runner; "
            f"pre={planned.pregrasp.xyz_csv()} grasp={planned.grasp.xyz_csv()} "
            f"quat={planned.grasp.quat_csv()} traj_log={cfg.traj_log}"
        )
        feedback.lift_height = 0.0
        goal_handle.publish_feedback(feedback)

        def publish(stage: str, reason: str, lift: float) -> None:
            feedback.stage = stage
            feedback.reason = reason
            feedback.lift_height = float(lift)
            goal_handle.publish_feedback(feedback)

        try:
            runner = MujocoInProcessRunner(
                MujocoRunnerConfig(
                    repo_root=cfg.repo_root,
                    mjcf=str(self._param("mjcf")),
                    checkpoint=str(self._param("checkpoint")),
                    target_object=str(cfg.target_object),
                    target_pos=str(cfg.target_pos),
                    enable_obstacle=bool(self._param("enable_obstacle")),
                    obstacle_body=str(self._param("obstacle_body")),
                    obstacle_pos=str(self._param("obstacle_pos")),
                    enable_cbf=bool(cfg.enable_avoidance),
                    replan_max_attempts=int(cfg.grasp_replan_max_attempts),
                    speed=float(cfg.speed),
                    show_viewer=bool(self._param("inprocess_viewer")),
                    traj_log=str(cfg.traj_log),
                )
            )
            run_res = runner.run(
                planned,
                feedback_cb=publish,
                tracking_provider=self._latest_tracking_pos,
                obstacle_provider=self._latest_obstacle_points,
            )
            result.success = bool(run_res.success)
            result.reason = str(run_res.reason)
            result.lift_height = float(run_res.lift_height)
            result.return_code = 0 if result.success else 1
            if result.success:
                goal_handle.succeed()
            else:
                goal_handle.abort()
        except Exception as exc:
            result.success = False
            result.reason = f"inprocess_backend_failed:{exc}"
            result.lift_height = 0.0
            result.return_code = 1
            goal_handle.abort()
        return result

    def _latest_tracking_pos(self):
        with self._lock:
            return None if self._tracked_pos_base is None else self._tracked_pos_base.copy()

    def _latest_obstacle_points(self):
        with self._lock:
            return self._obstacle_points_base.copy()

    def _pose_to_base(self, pose, repo: Path):
        if bool(self._param("use_sim_camera_extrinsics")):
            return pose_to_base_from_mujoco_camera(
                pose,
                repo_root=repo,
                mjcf=str(self._param("mjcf")),
                input_camera_name=str(self._param("input_camera_name")),
                base_frame=str(self._param("base_frame")),
            )
        return pose_to_base_from_calib(
            pose,
            repo_root=repo,
            calib_json=str(self._param("calib_json")),
            input_camera_name=str(self._param("input_camera_name")),
            base_frame=str(self._param("base_frame")),
        )


def main() -> None:
    rclpy.init()
    node = MujocoPolicyBackendNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
