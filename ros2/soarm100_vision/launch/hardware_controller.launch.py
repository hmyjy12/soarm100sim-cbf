from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from pathlib import Path


def generate_launch_description():
    description_share = Path(get_package_share_directory("so100_plus_description"))
    robot_description = (description_share / "urdf/so100_plus.urdf").read_text()
    return LaunchDescription(
        [
            DeclareLaunchArgument("repo_root", default_value="."),
            DeclareLaunchArgument("port", default_value="/dev/ttyACM0"),
            DeclareLaunchArgument("lerobot_env", default_value="lerobot"),
            DeclareLaunchArgument(
                "calibration_file",
                default_value="hardware/calibration/lerobot/so100_plus_new_arm.json",
            ),
            DeclareLaunchArgument("shoulder_lift_p", default_value="16"),
            DeclareLaunchArgument("feedback_rate_hz", default_value="20.0"),
            DeclareLaunchArgument("driver_rate_hz", default_value="20.0"),
            DeclareLaunchArgument("max_stream_command_delta_rad", default_value="0.25"),
            Node(
                package="soarm100_vision",
                executable="hardware_controller_node",
                name="hardware_controller",
                output="screen",
                parameters=[
                    {
                        "repo_root": LaunchConfiguration("repo_root"),
                        "port": LaunchConfiguration("port"),
                        "lerobot_env": LaunchConfiguration("lerobot_env"),
                        "calibration_file": LaunchConfiguration("calibration_file"),
                        "shoulder_lift_p": ParameterValue(
                            LaunchConfiguration("shoulder_lift_p"),
                            value_type=int,
                        ),
                        "feedback_rate_hz": ParameterValue(
                            LaunchConfiguration("feedback_rate_hz"),
                            value_type=float,
                        ),
                        "driver_rate_hz": ParameterValue(
                            LaunchConfiguration("driver_rate_hz"),
                            value_type=float,
                        ),
                        "max_stream_command_delta_rad": ParameterValue(
                            LaunchConfiguration("max_stream_command_delta_rad"),
                            value_type=float,
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
        ]
    )
