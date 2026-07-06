#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


JOINT_NAMES = [
    'shoulder_rotation_joint',
    'shoulder_pitch_joint',
    'ellbow_joint',
    'wrist_pitch_joint',
    'wrist_jaw_joint',
    'wrist_roll_joint',
    'gripper_joint',
]

# Home pose from so100_plus.xml keyframe.
HOME_POSITIONS = [0.0, -1.57079, 1.57079, 0.0, 0.0, 0.0, 0.0]


class StaticJointPublisher(Node):
    def __init__(self):
        super().__init__('static_joint_publisher')
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(0.1, self.publish_joint_states)

    def publish_joint_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = JOINT_NAMES
        msg.position = HOME_POSITIONS
        self.publisher.publish(msg)


def main():
    rclpy.init()
    node = StaticJointPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
