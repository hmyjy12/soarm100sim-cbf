from __future__ import annotations

import time

import rclpy
from rclpy.action import ActionClient
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import PointCloud2

from soarm100_interfaces.action import ExecuteGrasp, ExecutePlannedGrasp, PlanGrasp
from soarm100_interfaces.srv import SegmentTarget, SetAvoidance


def _pose_summary(label: str, pose: PoseStamped) -> str:
    p = pose.pose.position
    q = pose.pose.orientation
    return (
        f"{label}[frame={pose.header.frame_id or '<empty>'} "
        f"pos=({p.x:+.3f},{p.y:+.3f},{p.z:+.3f}) "
        f"quat=({q.w:+.3f},{q.x:+.3f},{q.y:+.3f},{q.z:+.3f})]"
    )


class GraspOrchestratorNode(Node):
    """Action-level grasp coordinator.

    This is the ROS2 boundary for the full task. The first implementation keeps
    the interfaces stable and reports stages; concrete policy, AnyGrasp, and
    CBF-QP clients should be connected behind this node.
    """

    def __init__(self) -> None:
        super().__init__("soarm100_grasp_orchestrator")
        self.declare_parameter("default_enable_avoidance", False)
        self.declare_parameter("max_attempts", 2)
        self.declare_parameter("segment_service", "segment_target")
        self.declare_parameter("plan_action", "plan_grasp")
        self.declare_parameter("policy_action", "execute_planned_grasp")
        self.declare_parameter("target_cloud_topic", "/target/cloud")
        self.declare_parameter("target_object", "cube")
        self.declare_parameter("target_pos", "0.42,0.08,0.021")
        self.declare_parameter("traj_log", "logs/ros2_execute_grasp.jsonl")
        self.declare_parameter("wait_timeout_s", 10.0)
        self._avoidance_enabled = bool(self.get_parameter("default_enable_avoidance").value)
        self._target_cloud: PointCloud2 | None = None
        self._segment_client = self.create_client(SegmentTarget, str(self.get_parameter("segment_service").value))
        self._plan_client = ActionClient(self, PlanGrasp, str(self.get_parameter("plan_action").value))
        self._policy_client = ActionClient(self, ExecutePlannedGrasp, str(self.get_parameter("policy_action").value))
        self.create_subscription(PointCloud2, str(self.get_parameter("target_cloud_topic").value), self._on_target_cloud, 1)
        self.create_service(SetAvoidance, "set_avoidance", self._on_set_avoidance)
        self._action_server = ActionServer(
            self,
            ExecuteGrasp,
            "execute_grasp",
            execute_callback=self._execute,
            goal_callback=self._goal,
            cancel_callback=self._cancel,
        )
        self.get_logger().info("grasp orchestrator ready: action=execute_grasp service=set_avoidance")

    def _on_target_cloud(self, msg: PointCloud2) -> None:
        self._target_cloud = msg

    def _goal(self, goal_request: ExecuteGrasp.Goal) -> GoalResponse:
        if not str(goal_request.target_prompt).strip():
            self.get_logger().warn("rejecting grasp goal: empty target_prompt")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _cancel(self, _goal_handle) -> CancelResponse:
        return CancelResponse.ACCEPT

    def _on_set_avoidance(self, request: SetAvoidance.Request, response: SetAvoidance.Response):
        self._avoidance_enabled = bool(request.enabled)
        response.success = True
        response.reason = f"avoidance_enabled={self._avoidance_enabled}"
        return response

    async def _execute(self, goal_handle):
        goal = goal_handle.request
        self._avoidance_enabled = bool(goal.enable_avoidance)
        feedback = ExecuteGrasp.Feedback()
        result = ExecuteGrasp.Result()
        attempts = 0

        def publish(stage: str, reason: str, *, replan: bool = False, grasp_score: float = 0.0) -> None:
            feedback.stage = stage
            feedback.reason = reason
            feedback.target_visible_score = 0.0
            feedback.grasp_score = float(grasp_score)
            feedback.tcp_pos_err = 0.0
            feedback.tcp_ori_err = 0.0
            feedback.sdf_min_dist = float("inf")
            feedback.cbf_active = self._avoidance_enabled
            feedback.tracking_valid = False
            feedback.replan_running = bool(replan)
            goal_handle.publish_feedback(feedback)

        max_attempts = max(int(self.get_parameter("max_attempts").value), 1)
        timeout_s = float(self.get_parameter("wait_timeout_s").value)
        last_reason = ""
        final_grasp = goal.approximate_target_pose

        for attempt in range(max_attempts):
            attempts = attempt + 1
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                result.reason = f"cancelled_at_attempt_{attempts}"
                return result

            publish("SEGMENTING", f"attempt={attempts}", replan=attempt > 0)
            seg = await self._call_segment(goal.target_prompt, timeout_s)
            if not seg.success:
                last_reason = f"segment_failed:{seg.reason}"
                publish("SEGMENT_FAILED", last_reason, replan=attempt > 0)
                continue
            feedback.target_visible_score = float(seg.score)
            goal_handle.publish_feedback(feedback)

            cloud = self._target_cloud
            if cloud is None or cloud.width * cloud.height <= 0:
                last_reason = "segment_success_but_no_target_cloud"
                publish("PLANNING_FAILED", last_reason, replan=attempt > 0)
                continue

            publish("PLANNING_GRASP", f"attempt={attempts} cloud_points={cloud.width * cloud.height}", replan=attempt > 0)
            plan = await self._call_plan(goal.target_prompt, cloud, timeout_s)
            if not plan.success:
                last_reason = f"plan_failed:{plan.reason}"
                publish("PLANNING_FAILED", last_reason, replan=attempt > 0)
                continue

            final_grasp = plan.selected_grasp_pose
            self.get_logger().info(
                "AnyGrasp selected pose forwarded to policy: "
                f"{_pose_summary('pregrasp', plan.selected_pregrasp_pose)} "
                f"{_pose_summary('grasp', plan.selected_grasp_pose)} "
                f"score={float(plan.grasp_score):.3f} width={float(plan.gripper_width)*1000.0:.1f}mm "
                f"candidates={int(plan.candidate_count)}"
            )
            publish(
                "READY_TO_EXECUTE_POLICY",
                (
                    f"planned score={float(plan.grasp_score):.3f} "
                    f"width={float(plan.gripper_width)*1000.0:.1f}mm candidates={int(plan.candidate_count)} "
                    f"{_pose_summary('grasp', plan.selected_grasp_pose)}"
                ),
                grasp_score=float(plan.grasp_score),
            )
            publish("EXECUTING_POLICY", "sending planned grasp to MuJoCo/policy backend", grasp_score=float(plan.grasp_score))
            exec_res = await self._call_policy(plan, goal.enable_avoidance, max(timeout_s, 90.0))
            result.success = bool(exec_res.success)
            result.reason = str(exec_res.reason)
            result.final_grasp_pose = final_grasp
            result.lift_height = float(exec_res.lift_height)
            result.attempts = attempts
            if result.success:
                goal_handle.succeed()
            else:
                goal_handle.abort()
            return result

        goal_handle.abort()
        result.success = False
        result.reason = last_reason or "all_attempts_failed"
        result.final_grasp_pose = final_grasp
        result.lift_height = 0.0
        result.attempts = attempts
        return result

    async def _call_segment(self, prompt: str, timeout_s: float):
        if not self._segment_client.wait_for_service(timeout_sec=timeout_s):
            res = SegmentTarget.Response()
            res.success = False
            res.reason = "segment_service_unavailable"
            return res
        req = SegmentTarget.Request()
        req.target_prompt = str(prompt)
        req.force_yolo = True
        fut = self._segment_client.call_async(req)
        return await fut

    async def _call_plan(self, prompt: str, cloud: PointCloud2, timeout_s: float):
        if not self._plan_client.wait_for_server(timeout_sec=timeout_s):
            res = PlanGrasp.Result()
            res.success = False
            res.reason = "plan_action_unavailable"
            return res
        goal = PlanGrasp.Goal()
        goal.target_prompt = str(prompt)
        goal.approximate_target_pose = _pose_default()
        goal.target_cloud = cloud
        goal.top_k = 45
        send_future = self._plan_client.send_goal_async(goal)
        plan_handle = await send_future
        if not plan_handle.accepted:
            res = PlanGrasp.Result()
            res.success = False
            res.reason = "plan_goal_rejected"
            return res
        result_future = plan_handle.get_result_async()
        wrapped = await result_future
        return wrapped.result

    async def _call_policy(self, plan: PlanGrasp.Result, enable_avoidance: bool, timeout_s: float):
        if not self._policy_client.wait_for_server(timeout_sec=timeout_s):
            res = ExecutePlannedGrasp.Result()
            res.success = False
            res.reason = "policy_action_unavailable"
            return res
        goal = ExecutePlannedGrasp.Goal()
        goal.pregrasp_pose = plan.selected_pregrasp_pose
        goal.grasp_pose = plan.selected_grasp_pose
        goal.gripper_width = float(plan.gripper_width)
        goal.enable_avoidance = bool(enable_avoidance)
        goal.target_object = str(self.get_parameter("target_object").value)
        goal.target_pos = str(self.get_parameter("target_pos").value)
        goal.traj_log = str(self.get_parameter("traj_log").value)
        send_future = self._policy_client.send_goal_async(goal)
        policy_handle = await send_future
        if not policy_handle.accepted:
            res = ExecutePlannedGrasp.Result()
            res.success = False
            res.reason = "policy_goal_rejected"
            return res
        result_future = policy_handle.get_result_async()
        wrapped = await result_future
        return wrapped.result


def _pose_default():
    msg = PoseStamped()
    msg.pose.orientation.w = 1.0
    return msg


def main() -> None:
    rclpy.init()
    node = GraspOrchestratorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
