from __future__ import annotations

import argparse
import sys

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from rclpy.node import Node

from soarm100_interfaces.action import ExecuteGrasp


def _pose(pos_csv: str, frame_id: str) -> PoseStamped:
    pos = [float(x) for x in str(pos_csv).replace(",", " ").split()]
    if len(pos) != 3:
        raise ValueError("--approx-target-pos must be x,y,z")
    msg = PoseStamped()
    msg.header.frame_id = str(frame_id)
    msg.pose.position.x = float(pos[0])
    msg.pose.position.y = float(pos[1])
    msg.pose.position.z = float(pos[2])
    msg.pose.orientation.w = 1.0
    return msg


class ExecuteGraspClient(Node):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__("soarm100_send_execute_grasp")
        self.args = args
        self.client = ActionClient(self, ExecuteGrasp, str(args.action))

    def send(self) -> int:
        if not self.client.wait_for_server(timeout_sec=float(self.args.wait_timeout)):
            self.get_logger().error(f"action server unavailable: {self.args.action}")
            return 2
        goal = ExecuteGrasp.Goal()
        goal.target_prompt = str(self.args.target)
        goal.enable_avoidance = bool(self.args.enable_avoidance)
        goal.approximate_target_pose = _pose(self.args.approx_target_pos, self.args.frame)
        fut = self.client.send_goal_async(goal, feedback_callback=self._feedback)
        rclpy.spin_until_future_complete(self, fut)
        handle = fut.result()
        if handle is None or not handle.accepted:
            self.get_logger().error("execute grasp goal rejected")
            return 3
        self.get_logger().info("execute grasp goal accepted")
        res_fut = handle.get_result_async()
        rclpy.spin_until_future_complete(self, res_fut)
        wrapped = res_fut.result()
        res = wrapped.result
        p = res.final_grasp_pose.pose.position
        q = res.final_grasp_pose.pose.orientation
        self.get_logger().info(
            f"result success={res.success} attempts={res.attempts} lift={res.lift_height:.4f} "
            f"reason={res.reason} final=({p.x:+.3f},{p.y:+.3f},{p.z:+.3f}) "
            f"quat=({q.w:+.3f},{q.x:+.3f},{q.y:+.3f},{q.z:+.3f})"
        )
        return 0 if res.success else 1

    def _feedback(self, msg) -> None:
        fb = msg.feedback
        self.get_logger().info(
            f"feedback stage={fb.stage} grasp={fb.grasp_score:.3f} "
            f"replan={fb.replan_running} cbf={fb.cbf_active} reason={fb.reason}"
        )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", default="execute_grasp")
    parser.add_argument("--target", default="red cube")
    parser.add_argument("--frame", default="base")
    parser.add_argument("--approx-target-pos", default="0.42,0.08,0.022")
    parser.add_argument("--enable-avoidance", action="store_true")
    parser.add_argument("--wait-timeout", type=float, default=30.0)
    args = parser.parse_args(argv)
    rclpy.init()
    node = ExecuteGraspClient(args)
    try:
        code = node.send()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    raise SystemExit(code)


if __name__ == "__main__":
    main(sys.argv[1:])
