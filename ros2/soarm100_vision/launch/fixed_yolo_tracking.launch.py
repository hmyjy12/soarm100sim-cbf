from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, Shutdown
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "rgb_topic", default_value="/camera/color/image_raw"
            ),
            DeclareLaunchArgument(
                "model", default_value="models/vision/yolowork_fixed_best.pt"
            ),
            DeclareLaunchArgument("target_class", default_value="all"),
            DeclareLaunchArgument("conf", default_value="0.01"),
            DeclareLaunchArgument("iou", default_value="0.70"),
            DeclareLaunchArgument("imgsz", default_value="640"),
            DeclareLaunchArgument("device", default_value="auto"),
            DeclareLaunchArgument("tracker", default_value="botsort.yaml"),
            DeclareLaunchArgument("max_fps", default_value="30.0"),
            DeclareLaunchArgument("show_window", default_value="true"),
            Node(
                package="soarm100_vision",
                executable="fixed_yolo_tracker_node",
                name="fixed_yolo_tracker",
                output="screen",
                on_exit=Shutdown(reason="fixed YOLO tracker exited"),
                parameters=[
                    {
                        "rgb_topic": LaunchConfiguration("rgb_topic"),
                        "model": LaunchConfiguration("model"),
                        "target_class": LaunchConfiguration("target_class"),
                        "conf": ParameterValue(
                            LaunchConfiguration("conf"), value_type=float
                        ),
                        "iou": ParameterValue(
                            LaunchConfiguration("iou"), value_type=float
                        ),
                        "imgsz": ParameterValue(
                            LaunchConfiguration("imgsz"), value_type=int
                        ),
                        "device": ParameterValue(
                            LaunchConfiguration("device"), value_type=str
                        ),
                        "tracker": LaunchConfiguration("tracker"),
                        "max_fps": ParameterValue(
                            LaunchConfiguration("max_fps"), value_type=float
                        ),
                        "show_window": ParameterValue(
                            LaunchConfiguration("show_window"), value_type=bool
                        ),
                    }
                ],
            ),
        ]
    )
