from __future__ import annotations

import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node

from soarm100_interfaces.action import ExecuteGrasp
from soarm100_interfaces.srv import SetAvoidance


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
        self._avoidance_enabled = bool(self.get_parameter("default_enable_avoidance").value)
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
        stages = (
            "SEGMENTING",
            "PLANNING_GRASP",
            "MOVE_TO_PREGRASP",
            "FINAL_APPROACH",
            "CLOSE",
            "LIFT",
        )
        for stage in stages:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                result.reason = f"cancelled_at_{stage}"
                return result
            feedback.stage = stage
            feedback.reason = "interface_skeleton"
            feedback.target_visible_score = 0.0
            feedback.grasp_score = 0.0
            feedback.tcp_pos_err = 0.0
            feedback.tcp_ori_err = 0.0
            feedback.sdf_min_dist = float("inf")
            feedback.cbf_active = self._avoidance_enabled
            feedback.tracking_valid = False
            feedback.replan_running = stage in ("SEGMENTING", "PLANNING_GRASP")
            goal_handle.publish_feedback(feedback)
            time.sleep(0.05)
        goal_handle.succeed()
        result.success = False
        result.reason = "skeleton_only_policy_anygrasp_not_connected"
        result.final_grasp_pose = goal.approximate_target_pose
        result.lift_height = 0.0
        result.attempts = 0
        return result


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
