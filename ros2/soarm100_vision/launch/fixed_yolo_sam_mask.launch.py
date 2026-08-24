from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    repo_root = LaunchConfiguration("repo_root")
    target_class = LaunchConfiguration("target_class")
    detector_model = LaunchConfiguration("detector_model")
    sam_model = LaunchConfiguration("sam_model")
    detector_conf = LaunchConfiguration("detector_conf")
    detector_iou = LaunchConfiguration("detector_iou")
    detector_imgsz = LaunchConfiguration("detector_imgsz")
    detector_device = LaunchConfiguration("detector_device")
    rgb_topic = LaunchConfiguration("rgb_topic")
    depth_topic = LaunchConfiguration("depth_topic")
    camera_info_topic = LaunchConfiguration("camera_info_topic")
    enable_visualizer = LaunchConfiguration("enable_visualizer")
    show_window = LaunchConfiguration("show_window")
    python_executable = LaunchConfiguration("python_executable")
    auto_segment_hz = LaunchConfiguration("auto_segment_hz")

    return LaunchDescription(
        [
            DeclareLaunchArgument("repo_root", default_value="."),
            DeclareLaunchArgument(
                "python_executable",
                default_value="/home/sophie/miniconda3/envs/vision_seg/bin/python",
            ),
            DeclareLaunchArgument("target_class", default_value="jpgCat"),
            DeclareLaunchArgument(
                "detector_model",
                default_value="models/vision/yolowork_fixed_best.pt",
            ),
            DeclareLaunchArgument(
                "sam_model", default_value="models/vision/mobile_sam.pt"
            ),
            DeclareLaunchArgument("detector_conf", default_value="0.01"),
            DeclareLaunchArgument("detector_iou", default_value="0.70"),
            DeclareLaunchArgument("detector_imgsz", default_value="640"),
            DeclareLaunchArgument("detector_device", default_value="auto"),
            DeclareLaunchArgument("auto_segment_hz", default_value="2.0"),
            DeclareLaunchArgument(
                "rgb_topic", default_value="/camera/color/image_raw"
            ),
            DeclareLaunchArgument(
                "depth_topic", default_value="/camera/depth/image_raw"
            ),
            DeclareLaunchArgument(
                "camera_info_topic", default_value="/camera/color/camera_info"
            ),
            DeclareLaunchArgument("enable_visualizer", default_value="true"),
            DeclareLaunchArgument("show_window", default_value="true"),
            Node(
                package="soarm100_vision",
                executable="target_segmenter_node",
                name="fixed_yolo_sam_segmenter",
                output="screen",
                prefix=[python_executable],
                parameters=[
                    {
                        "repo_root": repo_root,
                        "segmentation_mode": "fixed_yolo_sam",
                        "fixed_yolo_model": detector_model,
                        "fixed_yolo_target_class": target_class,
                        "fixed_yolo_conf": ParameterValue(
                            detector_conf, value_type=float
                        ),
                        "fixed_yolo_iou": ParameterValue(
                            detector_iou, value_type=float
                        ),
                        "fixed_yolo_imgsz": ParameterValue(
                            detector_imgsz, value_type=int
                        ),
                        "fixed_yolo_device": ParameterValue(
                            detector_device, value_type=str
                        ),
                        "sam_model": sam_model,
                        "rgb_topic": rgb_topic,
                        "depth_topic": depth_topic,
                        "camera_info_topic": camera_info_topic,
                        "auto_segment_hz": ParameterValue(
                            auto_segment_hz, value_type=float
                        ),
                        "auto_target_prompt": target_class,
                        "debug_dir": "log/runtime/ros2_vision/fixed_yolo_sam",
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="debug_viewer_node",
                name="fixed_yolo_sam_viewer",
                output="screen",
                prefix=[python_executable],
                condition=IfCondition(enable_visualizer),
                parameters=[
                    {
                        "rgb_topic": rgb_topic,
                        "mask_topic": "/target/mask",
                        "show_window": ParameterValue(
                            show_window, value_type=bool
                        ),
                        "window_name": "Fixed YOLO + SAM target mask",
                    }
                ],
            ),
        ]
    )
