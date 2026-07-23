from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node

from soarm100_interfaces.action import PlanGrasp
from soarm100_vision.vision_utils import pointcloud2_to_xyz


def _quat_wxyz_from_rot(R: np.ndarray) -> tuple[float, float, float, float]:
    m = np.asarray(R, dtype=np.float64).reshape(3, 3)
    tr = float(np.trace(m))
    if tr > 0.0:
        s = np.sqrt(tr + 1.0) * 2.0
        w = 0.25 * s
        x = (m[2, 1] - m[1, 2]) / s
        y = (m[0, 2] - m[2, 0]) / s
        z = (m[1, 0] - m[0, 1]) / s
    else:
        i = int(np.argmax(np.diag(m)))
        if i == 0:
            s = np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
            w = (m[2, 1] - m[1, 2]) / s
            x = 0.25 * s
            y = (m[0, 1] + m[1, 0]) / s
            z = (m[0, 2] + m[2, 0]) / s
        elif i == 1:
            s = np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
            w = (m[0, 2] - m[2, 0]) / s
            x = (m[0, 1] + m[1, 0]) / s
            y = 0.25 * s
            z = (m[1, 2] + m[2, 1]) / s
        else:
            s = np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
            w = (m[1, 0] - m[0, 1]) / s
            x = (m[0, 2] + m[2, 0]) / s
            y = (m[1, 2] + m[2, 1]) / s
            z = 0.25 * s
    q = np.array([w, x, y, z], dtype=np.float64)
    q /= max(float(np.linalg.norm(q)), 1e-12)
    return float(q[0]), float(q[1]), float(q[2]), float(q[3])


def _pose_from_grasp(position: np.ndarray, rotation: np.ndarray, *, stamp, frame_id: str) -> PoseStamped:
    p = np.asarray(position, dtype=np.float64).reshape(3)
    qw, qx, qy, qz = _quat_wxyz_from_rot(rotation)
    msg = PoseStamped()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.pose.position.x = float(p[0])
    msg.pose.position.y = float(p[1])
    msg.pose.position.z = float(p[2])
    msg.pose.orientation.w = qw
    msg.pose.orientation.x = qx
    msg.pose.orientation.y = qy
    msg.pose.orientation.z = qz
    return msg


class AnyGraspPlannerNode(Node):
    """PlanGrasp action server backed by AnyGrasp SDK subprocess."""

    def __init__(self) -> None:
        super().__init__("soarm100_anygrasp_planner")
        self.declare_parameter("sdk_root", "anygrasp_sdk")
        self.declare_parameter("checkpoint_path", "anygrasp_sdk/grasp_detection/log/checkpoint_detection.tar")
        self.declare_parameter("conda_env", "graspnet_gpu")
        self.declare_parameter("min_points", 50)
        self.declare_parameter("top_k", 45)
        self.declare_parameter("min_score", 0.01)
        self.declare_parameter("max_width", 0.10)
        self.declare_parameter("pregrasp_distance", 0.07)
        self.declare_parameter("timeout_s", 60.0)
        self._server = ActionServer(
            self,
            PlanGrasp,
            "plan_grasp",
            execute_callback=self._execute,
            goal_callback=self._goal,
            cancel_callback=self._cancel,
        )
        self.get_logger().info("AnyGrasp planner ready: action=plan_grasp")

    def _param(self, name: str):
        return self.get_parameter(name).value

    def _goal(self, goal_request: PlanGrasp.Goal) -> GoalResponse:
        if goal_request.target_cloud.width * goal_request.target_cloud.height <= 0:
            self.get_logger().warn("rejecting plan goal: empty target_cloud")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _cancel(self, _goal_handle) -> CancelResponse:
        return CancelResponse.ACCEPT

    async def _execute(self, goal_handle):
        result = PlanGrasp.Result()
        feedback = PlanGrasp.Feedback()
        try:
            pts = pointcloud2_to_xyz(goal_handle.request.target_cloud)
            feedback.stage = "INPUT_CLOUD"
            feedback.candidate_count = 0
            feedback.best_score = 0.0
            feedback.reason = f"points={pts.shape[0]}"
            goal_handle.publish_feedback(feedback)
            if pts.shape[0] < int(self._param("min_points")):
                raise RuntimeError(f"not_enough_points:{pts.shape[0]}")
            raw = self._predict(pts, int(goal_handle.request.top_k or int(self._param("top_k"))))
            candidates = list(raw.get("candidates", []))
            feedback.stage = "ANYGRASP_DONE"
            feedback.candidate_count = len(candidates)
            feedback.best_score = float(candidates[0].get("score", 0.0)) if candidates else 0.0
            feedback.reason = str(raw.get("message", "ok"))
            goal_handle.publish_feedback(feedback)
            if not candidates:
                raise RuntimeError(str(raw.get("message", "no_candidates")))
            selected = candidates[0]
            for i, cand in enumerate(candidates[: min(8, len(candidates))]):
                cpos = np.asarray(cand.get("translation", [0.0, 0.0, 0.0]), dtype=np.float64).reshape(3)
                crot = np.asarray(cand.get("rotation_matrix", np.eye(3)), dtype=np.float64).reshape(3, 3)
                capp = crot[:, 0]
                capp /= max(float(np.linalg.norm(capp)), 1e-12)
                self.get_logger().info(
                    f"AnyGrasp candidate[{i:02d}] frame={goal_handle.request.target_cloud.header.frame_id or '<empty>'} "
                    f"score={float(cand.get('score', 0.0)):.3f} width={float(cand.get('width', 0.0))*1000.0:.1f}mm "
                    f"pos=({cpos[0]:+.3f},{cpos[1]:+.3f},{cpos[2]:+.3f}) "
                    f"approach=({capp[0]:+.2f},{capp[1]:+.2f},{capp[2]:+.2f})"
                )
            pos = np.asarray(selected["translation"], dtype=np.float64).reshape(3)
            rot = np.asarray(selected["rotation_matrix"], dtype=np.float64).reshape(3, 3)
            approach = rot[:, 0]
            approach /= max(float(np.linalg.norm(approach)), 1e-12)
            pre = pos - float(self._param("pregrasp_distance")) * approach
            stamp = goal_handle.request.target_cloud.header.stamp
            frame_id = goal_handle.request.target_cloud.header.frame_id
            result.success = True
            result.reason = "ok"
            result.selected_grasp_pose = _pose_from_grasp(pos, rot, stamp=stamp, frame_id=frame_id)
            result.selected_pregrasp_pose = _pose_from_grasp(pre, rot, stamp=stamp, frame_id=frame_id)
            result.grasp_score = float(selected.get("score", 0.0))
            result.gripper_width = float(selected.get("width", 0.0))
            result.candidate_count = len(candidates)
            goal_handle.succeed()
        except Exception as exc:
            result.success = False
            result.reason = f"plan_failed:{exc}"
            goal_handle.abort()
        return result

    def _predict(self, points: np.ndarray, top_k: int) -> dict:
        sdk_root = Path(str(self._param("sdk_root"))).expanduser().resolve()
        worker = sdk_root / "grasp_detection" / "predict_npz.py"
        if not worker.is_file():
            raise FileNotFoundError(f"AnyGrasp worker not found: {worker}")
        with tempfile.TemporaryDirectory(prefix="ros2_anygrasp_") as td:
            tmp = Path(td)
            pts_path = tmp / "points.npz"
            out_path = tmp / "candidates.json"
            np.savez_compressed(pts_path, points=np.ascontiguousarray(points, dtype=np.float32))
            py = Path(sys.executable).expanduser().resolve()
            conda_root = py.parents[3] if len(py.parents) > 3 and py.parents[2].name == "envs" else py.parents[1]
            worker_python = conda_root / "envs" / str(self._param("conda_env")) / "bin" / "python"
            py_cmd = str(worker_python) if worker_python.is_file() else "python"
            cmd = [
                py_cmd,
                str(worker),
                "--points-npz",
                str(pts_path),
                "--out-json",
                str(out_path),
                "--checkpoint-path",
                str(Path(str(self._param("checkpoint_path"))).expanduser().resolve()),
                "--sdk-root",
                str(sdk_root),
                "--top-k",
                str(int(top_k)),
                "--min-score",
                str(float(self._param("min_score"))),
                "--max-width",
                str(float(self._param("max_width"))),
            ]
            env = os.environ.copy()
            env["PATH"] = f"{sdk_root / 'tools'}:{env.get('PATH', '')}"
            env.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-anygrasp")
            proc = subprocess.run(
                cmd,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                timeout=float(self._param("timeout_s")),
            )
            if proc.returncode != 0:
                details = ""
                if out_path.is_file():
                    try:
                        failed = json.loads(out_path.read_text(encoding="utf-8"))
                        details = f" message={failed.get('message', '')} traceback={str(failed.get('traceback', ''))[-3000:]}"
                    except Exception:
                        details = f" output_json={out_path.read_text(encoding='utf-8', errors='replace')[-3000:]}"
                raise RuntimeError(
                    f"worker_failed:{proc.returncode}:{details} "
                    f"stdout={proc.stdout[-2000:]} stderr={proc.stderr[-3000:]}"
                )
            if not out_path.is_file():
                raise RuntimeError(f"worker_no_output stdout={proc.stdout[-1000:]}")
            return json.loads(out_path.read_text(encoding="utf-8"))


def main() -> None:
    rclpy.init()
    node = AnyGraspPlannerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
