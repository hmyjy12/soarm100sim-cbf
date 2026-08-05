from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    description_share = Path(
        get_package_share_directory("so100_plus_description")
    )
    robot_description = (description_share / "urdf/so100_plus.urdf").read_text()
    rviz_config = str(description_share / "rviz/so100_plus.rviz")

    udp_port = LaunchConfiguration("udp_port")
    stale_timeout = LaunchConfiguration("stale_timeout")
    use_rviz = LaunchConfiguration("use_rviz")

    return LaunchDescription(
        [
            DeclareLaunchArgument("udp_port", default_value="15001"),
            DeclareLaunchArgument("stale_timeout", default_value="0.5"),
            DeclareLaunchArgument("use_rviz", default_value="true"),
            Node(
                package="soarm100_vision",
                executable="hardware_joint_state_node",
                name="hardware_joint_state",
                output="screen",
                parameters=[
                    {
                        "udp_port": ParameterValue(udp_port, value_type=int),
                        "stale_timeout": ParameterValue(
                            stale_timeout, value_type=float
                        ),
                    }
                ],
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="hardware_robot_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="hardware_state_rviz",
                output="screen",
                arguments=["-d", rviz_config],
                condition=IfCondition(use_rviz),
            ),
        ]
    )
