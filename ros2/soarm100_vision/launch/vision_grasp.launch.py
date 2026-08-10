from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    target_prompt = LaunchConfiguration("target_prompt")
    target_segmentation_mode = LaunchConfiguration("target_segmentation_mode")
    target_color_rgb = LaunchConfiguration("target_color_rgb")
    color_hue_tolerance_deg = LaunchConfiguration("color_hue_tolerance_deg")
    enable_avoidance = LaunchConfiguration("enable_avoidance")
    rgb_topic = LaunchConfiguration("rgb_topic")
    depth_topic = LaunchConfiguration("depth_topic")
    camera_info_topic = LaunchConfiguration("camera_info_topic")
    wrist_rgb_topic = LaunchConfiguration("wrist_rgb_topic")
    yolo_model = LaunchConfiguration("yolo_model")
    fixed_yolo_model = LaunchConfiguration("fixed_yolo_model")
    fixed_yolo_target_class = LaunchConfiguration("fixed_yolo_target_class")
    fixed_yolo_conf = LaunchConfiguration("fixed_yolo_conf")
    fixed_yolo_iou = LaunchConfiguration("fixed_yolo_iou")
    fixed_yolo_device = LaunchConfiguration("fixed_yolo_device")
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
    mujoco_target_motion = LaunchConfiguration("mujoco_target_motion")
    mujoco_target_motion_amplitude = LaunchConfiguration(
        "mujoco_target_motion_amplitude"
    )
    mujoco_target_motion_travel_time = LaunchConfiguration(
        "mujoco_target_motion_travel_time"
    )
    mujoco_target_motion_dwell_time = LaunchConfiguration(
        "mujoco_target_motion_dwell_time"
    )
    mujoco_target_motion_delay = LaunchConfiguration("mujoco_target_motion_delay")
    mujoco_enable_obstacle = LaunchConfiguration("mujoco_enable_obstacle")
    mujoco_obstacle_body = LaunchConfiguration("mujoco_obstacle_body")
    mujoco_obstacle_pos = LaunchConfiguration("mujoco_obstacle_pos")
    mujoco_obstacle_motion = LaunchConfiguration("mujoco_obstacle_motion")
    mujoco_obstacle_motion_amp = LaunchConfiguration("mujoco_obstacle_motion_amp")
    mujoco_obstacle_motion_period = LaunchConfiguration(
        "mujoco_obstacle_motion_period"
    )
    mujoco_traj_log = LaunchConfiguration("mujoco_traj_log")
    mujoco_python = LaunchConfiguration("mujoco_python")
    mujoco_speed = LaunchConfiguration("mujoco_speed")
    mujoco_backend_mode = LaunchConfiguration("mujoco_backend_mode")
    mujoco_inprocess_viewer = LaunchConfiguration("mujoco_inprocess_viewer")
    use_sim_camera_extrinsics = LaunchConfiguration("use_sim_camera_extrinsics")
    calib_json = LaunchConfiguration("calib_json")
    mujoco_internal_tracking = LaunchConfiguration("mujoco_internal_tracking")
    mujoco_track_source = LaunchConfiguration("mujoco_track_source")
    mujoco_replan_attempts = LaunchConfiguration("mujoco_replan_attempts")
    mujoco_final_approach_timeout = LaunchConfiguration(
        "mujoco_final_approach_timeout"
    )
    grasp_final_dist = LaunchConfiguration("grasp_final_dist")
    grasp_final_timeout_close_dist = LaunchConfiguration(
        "grasp_final_timeout_close_dist"
    )
    grasp_final_stable_time = LaunchConfiguration("grasp_final_stable_time")
    grasp_close_tracking_confidence = LaunchConfiguration(
        "grasp_close_tracking_confidence"
    )
    grasp_close_target_speed = LaunchConfiguration("grasp_close_target_speed")
    tracking_topic = LaunchConfiguration("tracking_topic")
    obstacle_cloud_topic = LaunchConfiguration("obstacle_cloud_topic")
    obstacle_mode = LaunchConfiguration("obstacle_mode")
    enable_visualizer = LaunchConfiguration("enable_visualizer")
    show_window = LaunchConfiguration("show_window")

    return LaunchDescription(
        [
            DeclareLaunchArgument("target_prompt", default_value="red cube"),
            DeclareLaunchArgument("target_segmentation_mode", default_value="color"),
            DeclareLaunchArgument("target_color_rgb", default_value="255,0,0"),
            DeclareLaunchArgument("color_hue_tolerance_deg", default_value="18.0"),
            DeclareLaunchArgument("enable_avoidance", default_value="false"),
            DeclareLaunchArgument("rgb_topic", default_value="/camera/color/image_raw"),
            DeclareLaunchArgument("depth_topic", default_value="/camera/depth/image_rect_raw"),
            DeclareLaunchArgument("camera_info_topic", default_value="/camera/color/camera_info"),
            DeclareLaunchArgument("wrist_rgb_topic", default_value="/wrist/color/image_raw"),
            DeclareLaunchArgument("yolo_model", default_value="models/vision/yolov8s-world.pt"),
            DeclareLaunchArgument(
                "fixed_yolo_model", default_value="models/vision/yolowork_fixed_best.pt"
            ),
            DeclareLaunchArgument("fixed_yolo_target_class", default_value=""),
            DeclareLaunchArgument("fixed_yolo_conf", default_value="0.01"),
            DeclareLaunchArgument("fixed_yolo_iou", default_value="0.70"),
            DeclareLaunchArgument("fixed_yolo_device", default_value="auto"),
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
            DeclareLaunchArgument("mujoco_target_motion", default_value="none"),
            DeclareLaunchArgument(
                "mujoco_target_motion_amplitude", default_value="0.05"
            ),
            DeclareLaunchArgument(
                "mujoco_target_motion_travel_time", default_value="2.0"
            ),
            DeclareLaunchArgument(
                "mujoco_target_motion_dwell_time", default_value="1.0"
            ),
            DeclareLaunchArgument("mujoco_target_motion_delay", default_value="0.5"),
            DeclareLaunchArgument("mujoco_enable_obstacle", default_value="false"),
            DeclareLaunchArgument("mujoco_obstacle_body", default_value="obstacle_rod_mount"),
            DeclareLaunchArgument("mujoco_obstacle_pos", default_value="0.16,0.09,0.02"),
            DeclareLaunchArgument("mujoco_obstacle_motion", default_value="none"),
            DeclareLaunchArgument(
                "mujoco_obstacle_motion_amp", default_value="0.03,0.00,0.00"
            ),
            DeclareLaunchArgument("mujoco_obstacle_motion_period", default_value="5.0"),
            DeclareLaunchArgument("mujoco_traj_log", default_value="logs/ros2_execute_grasp.jsonl"),
            DeclareLaunchArgument("mujoco_python", default_value="python"),
            DeclareLaunchArgument("mujoco_speed", default_value="1.0"),
            DeclareLaunchArgument("mujoco_backend_mode", default_value="subprocess"),
            DeclareLaunchArgument("mujoco_inprocess_viewer", default_value="false"),
            DeclareLaunchArgument("use_sim_camera_extrinsics", default_value="true"),
            DeclareLaunchArgument(
                "calib_json",
                default_value="hardware/calibration/camera/real_camera_calib.json",
            ),
            DeclareLaunchArgument("mujoco_internal_tracking", default_value="true"),
            DeclareLaunchArgument("mujoco_track_source", default_value="wrist"),
            DeclareLaunchArgument("mujoco_replan_attempts", default_value="2"),
            DeclareLaunchArgument(
                "mujoco_final_approach_timeout", default_value="10.0"
            ),
            DeclareLaunchArgument("grasp_final_dist", default_value="0.035"),
            DeclareLaunchArgument(
                "grasp_final_timeout_close_dist", default_value="0.040"
            ),
            DeclareLaunchArgument("grasp_final_stable_time", default_value="0.20"),
            DeclareLaunchArgument(
                "grasp_close_tracking_confidence", default_value="0.45"
            ),
            DeclareLaunchArgument(
                "grasp_close_target_speed", default_value="0.005"
            ),
            DeclareLaunchArgument("tracking_topic", default_value="/target/tracked_2d"),
            DeclareLaunchArgument("obstacle_cloud_topic", default_value="/obstacle/cloud"),
            DeclareLaunchArgument("obstacle_mode", default_value="static"),
            DeclareLaunchArgument("enable_visualizer", default_value="false"),
            DeclareLaunchArgument("show_window", default_value="false"),
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
                        "fixed_yolo_model": fixed_yolo_model,
                        "fixed_yolo_target_class": fixed_yolo_target_class,
                        "fixed_yolo_conf": ParameterValue(
                            fixed_yolo_conf, value_type=float
                        ),
                        "fixed_yolo_iou": ParameterValue(
                            fixed_yolo_iou, value_type=float
                        ),
                        "fixed_yolo_device": ParameterValue(
                            fixed_yolo_device, value_type=str
                        ),
                        "sam_model": sam_model,
                        "segmentation_mode": target_segmentation_mode,
                        "target_color_rgb": target_color_rgb,
                        "color_hue_tolerance_deg": ParameterValue(
                            color_hue_tolerance_deg, value_type=float
                        ),
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
                        "obstacle_mode": obstacle_mode,
                        "repo_root": repo_root,
                        "mjcf": mujoco_mjcf,
                        "use_sim_camera_extrinsics": use_sim_camera_extrinsics,
                        "calib_json": calib_json,
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
                        "publish_wrist_rgb": False,
                        "scene_burst_frames": 5,
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
                        "repo_root": repo_root,
                        "mjcf": mujoco_mjcf,
                        "use_sim_camera_extrinsics": use_sim_camera_extrinsics,
                        "calib_json": calib_json,
                        "enable_ik_filter": True,
                        "ik_position_tolerance_m": 0.005,
                        "ik_rotation_tolerance_deg": 3.0,
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
                        "rgb_topic": wrist_rgb_topic,
                        "tracking_mode": target_segmentation_mode,
                        "target_color_rgb": target_color_rgb,
                        "color_hue_tolerance_deg": ParameterValue(
                            color_hue_tolerance_deg, value_type=float
                        ),
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
                        "inprocess_viewer": False,
                        "use_sim_camera_extrinsics": use_sim_camera_extrinsics,
                        "calib_json": calib_json,
                        "default_target_object": mujoco_target_object,
                        "default_target_pos": mujoco_target_pos,
                        "target_motion": mujoco_target_motion,
                        "target_motion_amplitude": ParameterValue(
                            mujoco_target_motion_amplitude, value_type=float
                        ),
                        "target_motion_travel_time": ParameterValue(
                            mujoco_target_motion_travel_time, value_type=float
                        ),
                        "target_motion_dwell_time": ParameterValue(
                            mujoco_target_motion_dwell_time, value_type=float
                        ),
                        "target_motion_delay": ParameterValue(
                            mujoco_target_motion_delay, value_type=float
                        ),
                        "default_traj_log": mujoco_traj_log,
                        "enable_obstacle": mujoco_enable_obstacle,
                        "obstacle_body": mujoco_obstacle_body,
                        "obstacle_pos": mujoco_obstacle_pos,
                        "obstacle_motion": mujoco_obstacle_motion,
                        "obstacle_motion_amp": mujoco_obstacle_motion_amp,
                        "obstacle_motion_period": ParameterValue(
                            mujoco_obstacle_motion_period, value_type=float
                        ),
                        "obstacle_mode": obstacle_mode,
                        "enable_internal_tracking": mujoco_internal_tracking,
                        "grasp_track_source": mujoco_track_source,
                        "grasp_replan_max_attempts": mujoco_replan_attempts,
                        "grasp_final_approach_timeout": mujoco_final_approach_timeout,
                        "grasp_final_dist": ParameterValue(
                            grasp_final_dist, value_type=float
                        ),
                        "grasp_final_timeout_close_dist": ParameterValue(
                            grasp_final_timeout_close_dist, value_type=float
                        ),
                        "grasp_final_stable_time": ParameterValue(
                            grasp_final_stable_time, value_type=float
                        ),
                        "grasp_close_tracking_confidence": ParameterValue(
                            grasp_close_tracking_confidence, value_type=float
                        ),
                        "grasp_close_target_speed": ParameterValue(
                            grasp_close_target_speed, value_type=float
                        ),
                        "tracking_topic": tracking_topic,
                        "obstacle_cloud_topic": obstacle_cloud_topic,
                    }
                ],
            ),
            Node(
                package="soarm100_vision",
                executable="mujoco_mirror_viewer_node",
                name="mujoco_mirror_viewer",
                output="screen",
                condition=IfCondition(mujoco_inprocess_viewer),
                parameters=[
                    {
                        "repo_root": repo_root,
                        "mjcf": mujoco_mjcf,
                        "sim_state_topic": "/mujoco/sim_state",
                        "obstacle_body": mujoco_obstacle_body,
                        "obstacle_pos": mujoco_obstacle_pos,
                        "obstacle_motion": mujoco_obstacle_motion,
                        "obstacle_motion_amp": mujoco_obstacle_motion_amp,
                        "obstacle_motion_period": ParameterValue(
                            mujoco_obstacle_motion_period, value_type=float
                        ),
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
