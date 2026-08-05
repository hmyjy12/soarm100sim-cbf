from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument("repo_root", default_value="."),
            DeclareLaunchArgument("port", default_value="/dev/ttyACM0"),
            DeclareLaunchArgument("lerobot_env", default_value="lerobot"),
            DeclareLaunchArgument("max_delta_deg", default_value="2.0"),
            Node(
                package="soarm100_vision",
                executable="hardware_single_joint_service_node",
                name="hardware_single_joint_service",
                output="screen",
                parameters=[
                    {
                        "repo_root": LaunchConfiguration("repo_root"),
                        "port": LaunchConfiguration("port"),
                        "lerobot_env": LaunchConfiguration("lerobot_env"),
                        "max_delta_deg": ParameterValue(
                            LaunchConfiguration("max_delta_deg"),
                            value_type=float,
                        ),
                    }
                ],
            )
        ]
    )
