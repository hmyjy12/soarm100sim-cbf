from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    target_prompt = LaunchConfiguration("target_prompt")
    enable_avoidance = LaunchConfiguration("enable_avoidance")
    rgb_topic = LaunchConfiguration("rgb_topic")
    depth_topic = LaunchConfiguration("depth_topic")
    camera_info_topic = LaunchConfiguration("camera_info_topic")
    wrist_depth_topic = LaunchConfiguration("wrist_depth_topic")
    wrist_camera_info_topic = LaunchConfiguration("wrist_camera_info_topic")
    yolo_model = LaunchConfiguration("yolo_model")
    sam_model = LaunchConfiguration("sam_model")
    enable_visualizer = LaunchConfiguration("enable_visualizer")
    show_window = LaunchConfiguration("show_window")

    return LaunchDescription(
        [
            DeclareLaunchArgument("target_prompt", default_value="red cube"),
            DeclareLaunchArgument("enable_avoidance", default_value="false"),
            DeclareLaunchArgument("rgb_topic", default_value="/camera/color/image_raw"),
            DeclareLaunchArgument("depth_topic", default_value="/camera/depth/image_rect_raw"),
            DeclareLaunchArgument("camera_info_topic", default_value="/camera/color/camera_info"),
            DeclareLaunchArgument("wrist_depth_topic", default_value="/wrist/depth/image_rect_raw"),
            DeclareLaunchArgument("wrist_camera_info_topic", default_value="/wrist/depth/camera_info"),
            DeclareLaunchArgument("yolo_model", default_value="models/vision/yolov8s-world.pt"),
            DeclareLaunchArgument("sam_model", default_value="models/vision/mobile_sam.pt"),
            DeclareLaunchArgument("enable_visualizer", default_value="true"),
            DeclareLaunchArgument("show_window", default_value="true"),
            Node(
                package="soarm100_vision",
                executable="target_segmenter_node",
                name="target_segmenter",
                output="screen",
                parameters=[
                    {
                        "rgb_topic": rgb_topic,
                        "depth_topic": depth_topic,
                        "camera_info_topic": camera_info_topic,
                        "yolo_model": yolo_model,
                        "sam_model": sam_model,
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="wrist_tracker_node",
                name="wrist_tracker",
                output="screen",
                parameters=[
                    {
                        "depth_topic": wrist_depth_topic,
                        "camera_info_topic": wrist_camera_info_topic,
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="grasp_orchestrator_node",
                name="grasp_orchestrator",
                output="screen",
                parameters=[{"default_enable_avoidance": enable_avoidance}],
            ),
            Node(
                package="soarm100_vision",
                executable="debug_viewer_node",
                name="debug_viewer",
                output="screen",
                condition=IfCondition(enable_visualizer),
                parameters=[
                    {
                        "rgb_topic": rgb_topic,
                        "mask_topic": "/target/mask",
                        "show_window": show_window,
                    }
                ],
            ),
        ]
    )
