from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node


def generate_launch_description():
    root = LaunchConfiguration("repo_root")
    calib = LaunchConfiguration("calib_json")
    return LaunchDescription([
        DeclareLaunchArgument("repo_root", default_value="."),
        DeclareLaunchArgument(
            "calib_json",
            default_value="hardware/calibration/camera/real_camera_calib.json",
        ),
        Node(
            package="soarm100_vision",
            executable="anygrasp_planner_node",
            name="real_anygrasp_planner",
            output="screen",
            parameters=[{
                "repo_root": root,
                "use_sim_camera_extrinsics": False,
                "calib_json": calib,
                "input_camera_name": "scene_depth",
                "top_k": 45,
                "grasp_approach_offset_m": -0.040,
                "pregrasp_distance": 0.040,
                "enable_ik_filter": True,
                "ik_position_tolerance_m": 0.005,
                "ik_rotation_tolerance_deg": 3.0,
                "enable_hardware_limit_filter": True,
                "hardware_calibration_json": "hardware/calibration/lerobot/so100_plus_new_arm.json",
                "hardware_mapping_json": "hardware/calibration/policy_joint_mapping.json",
                "hardware_limit_margin_counts": 0,
            }],
        ),
        Node(
            package="soarm100_vision",
            executable="real_policy_grasp_backend_node",
            name="real_policy_grasp_backend",
            output="screen",
            parameters=[{
                "repo_root": root,
                "calib_json": calib,
            }],
        ),
        Node(
            package="soarm100_vision",
            executable="grasp_orchestrator_node",
            name="real_grasp_orchestrator",
            output="screen",
            parameters=[{
                "max_attempts": 1,
                "default_enable_avoidance": False,
                "wait_timeout_s": 90.0,
            }],
        ),
    ])
