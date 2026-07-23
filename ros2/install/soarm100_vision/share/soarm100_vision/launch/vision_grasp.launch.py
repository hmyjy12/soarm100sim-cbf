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
    anygrasp_sdk_root = LaunchConfiguration("anygrasp_sdk_root")
    anygrasp_checkpoint = LaunchConfiguration("anygrasp_checkpoint")
    anygrasp_conda_env = LaunchConfiguration("anygrasp_conda_env")
    enable_anygrasp_planner = LaunchConfiguration("enable_anygrasp_planner")
    enable_obstacle_cloud = LaunchConfiguration("enable_obstacle_cloud")
    enable_mujoco_backend = LaunchConfiguration("enable_mujoco_backend")
    enable_mujoco_camera = LaunchConfiguration("enable_mujoco_camera")
    enable_sdf_backend = LaunchConfiguration("enable_sdf_backend")
    repo_root = LaunchConfiguration("repo_root")
    mujoco_mjcf = LaunchConfiguration("mujoco_mjcf")
    mujoco_target_object = LaunchConfiguration("mujoco_target_object")
    mujoco_target_pos = LaunchConfiguration("mujoco_target_pos")
    mujoco_enable_obstacle = LaunchConfiguration("mujoco_enable_obstacle")
    mujoco_obstacle_body = LaunchConfiguration("mujoco_obstacle_body")
    mujoco_obstacle_pos = LaunchConfiguration("mujoco_obstacle_pos")
    mujoco_traj_log = LaunchConfiguration("mujoco_traj_log")
    mujoco_python = LaunchConfiguration("mujoco_python")
    mujoco_speed = LaunchConfiguration("mujoco_speed")
    mujoco_backend_mode = LaunchConfiguration("mujoco_backend_mode")
    mujoco_inprocess_viewer = LaunchConfiguration("mujoco_inprocess_viewer")
    use_sim_camera_extrinsics = LaunchConfiguration("use_sim_camera_extrinsics")
    mujoco_internal_tracking = LaunchConfiguration("mujoco_internal_tracking")
    mujoco_track_source = LaunchConfiguration("mujoco_track_source")
    tracking_topic = LaunchConfiguration("tracking_topic")
    obstacle_cloud_topic = LaunchConfiguration("obstacle_cloud_topic")
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
            DeclareLaunchArgument("anygrasp_sdk_root", default_value="anygrasp_sdk"),
            DeclareLaunchArgument("anygrasp_checkpoint", default_value="anygrasp_sdk/grasp_detection/log/checkpoint_detection.tar"),
            DeclareLaunchArgument("anygrasp_conda_env", default_value="graspnet_gpu"),
            DeclareLaunchArgument("enable_anygrasp_planner", default_value="false"),
            DeclareLaunchArgument("enable_obstacle_cloud", default_value="true"),
            DeclareLaunchArgument("enable_mujoco_backend", default_value="false"),
            DeclareLaunchArgument("enable_mujoco_camera", default_value="false"),
            DeclareLaunchArgument("enable_sdf_backend", default_value="false"),
            DeclareLaunchArgument("repo_root", default_value="."),
            DeclareLaunchArgument("mujoco_mjcf", default_value="SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"),
            DeclareLaunchArgument("mujoco_target_object", default_value="cube"),
            DeclareLaunchArgument("mujoco_target_pos", default_value="0.42,0.08,0.021"),
            DeclareLaunchArgument("mujoco_enable_obstacle", default_value="false"),
            DeclareLaunchArgument("mujoco_obstacle_body", default_value="obstacle_rod_mount"),
            DeclareLaunchArgument("mujoco_obstacle_pos", default_value="0.16,0.09,0.02"),
            DeclareLaunchArgument("mujoco_traj_log", default_value="logs/ros2_execute_grasp.jsonl"),
            DeclareLaunchArgument("mujoco_python", default_value="python"),
            DeclareLaunchArgument("mujoco_speed", default_value="0.5"),
            DeclareLaunchArgument("mujoco_backend_mode", default_value="subprocess"),
            DeclareLaunchArgument("mujoco_inprocess_viewer", default_value="false"),
            DeclareLaunchArgument("use_sim_camera_extrinsics", default_value="true"),
            DeclareLaunchArgument("mujoco_internal_tracking", default_value="true"),
            DeclareLaunchArgument("mujoco_track_source", default_value="wrist"),
            DeclareLaunchArgument("tracking_topic", default_value="/target/tracked_center"),
            DeclareLaunchArgument("obstacle_cloud_topic", default_value="/obstacle/cloud"),
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
                        "mask_expand_ratio": 0.05,
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="obstacle_cloud_node",
                name="obstacle_cloud",
                output="screen",
                condition=IfCondition(enable_obstacle_cloud),
                parameters=[
                    {
                        "depth_topic": depth_topic,
                        "camera_info_topic": camera_info_topic,
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="sdf_cbf_backend_node",
                name="sdf_cbf_backend",
                output="screen",
                condition=IfCondition(enable_sdf_backend),
            ),
            Node(
                package="soarm100_vision",
                executable="mujoco_camera_publisher_node",
                name="mujoco_camera_publisher",
                output="screen",
                condition=IfCondition(enable_mujoco_camera),
                parameters=[
                    {
                        "repo_root": repo_root,
                        "mjcf": mujoco_mjcf,
                        "target_object": mujoco_target_object,
                        "target_pos": mujoco_target_pos,
                        "enable_obstacle": mujoco_enable_obstacle,
                        "obstacle_body": mujoco_obstacle_body,
                        "obstacle_pos": mujoco_obstacle_pos,
                        "traj_log": mujoco_traj_log,
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="anygrasp_planner_node",
                name="anygrasp_planner",
                output="screen",
                condition=IfCondition(enable_anygrasp_planner),
                parameters=[
                    {
                        "sdk_root": anygrasp_sdk_root,
                        "checkpoint_path": anygrasp_checkpoint,
                        "conda_env": anygrasp_conda_env,
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
                executable="mujoco_policy_backend_node",
                name="mujoco_policy_backend",
                output="screen",
                condition=IfCondition(enable_mujoco_backend),
                parameters=[
                    {
                        "repo_root": repo_root,
                        "mjcf": mujoco_mjcf,
                        "python_executable": mujoco_python,
                        "speed": mujoco_speed,
                        "backend_mode": mujoco_backend_mode,
                        "inprocess_viewer": mujoco_inprocess_viewer,
                        "use_sim_camera_extrinsics": use_sim_camera_extrinsics,
                        "default_target_object": mujoco_target_object,
                        "default_target_pos": mujoco_target_pos,
                        "default_traj_log": mujoco_traj_log,
                        "enable_obstacle": mujoco_enable_obstacle,
                        "obstacle_body": mujoco_obstacle_body,
                        "obstacle_pos": mujoco_obstacle_pos,
                        "enable_internal_tracking": mujoco_internal_tracking,
                        "grasp_track_source": mujoco_track_source,
                        "tracking_topic": tracking_topic,
                        "obstacle_cloud_topic": obstacle_cloud_topic,
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="grasp_orchestrator_node",
                name="grasp_orchestrator",
                output="screen",
                parameters=[
                    {
                        "default_enable_avoidance": enable_avoidance,
                        "target_object": mujoco_target_object,
                        "target_pos": mujoco_target_pos,
                        "traj_log": mujoco_traj_log,
                    }
                ],
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
