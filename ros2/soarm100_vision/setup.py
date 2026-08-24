from setuptools import find_packages, setup

package_name = "soarm100_vision"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (
            f"share/{package_name}/launch",
            [
                "launch/vision_grasp.launch.py",
                "launch/fixed_yolo_sam_mask.launch.py",
                "launch/fixed_yolo_tracking.launch.py",
                "launch/real_single_grasp.launch.py",
                "launch/hardware_state.launch.py",
                "launch/hardware_single_joint.launch.py",
                "launch/hardware_controller.launch.py",
            ],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="sophie",
    maintainer_email="todo@example.com",
    description="SO-ARM100 vision segmentation and wrist target tracking.",
    license="Proprietary",
    entry_points={
        "console_scripts": [
            "target_segmenter_node = soarm100_vision.target_segmenter_node:main",
            "fixed_yolo_tracker_node = soarm100_vision.fixed_yolo_tracker_node:main",
            "wrist_tracker_node = soarm100_vision.wrist_tracker_node:main",
            "obstacle_cloud_node = soarm100_vision.obstacle_cloud_node:main",
            "obstacle_overlay_viewer_node = soarm100_vision.obstacle_overlay_viewer_node:main",
            "link_self_occupancy_collector_node = soarm100_vision.link_self_occupancy_collector_node:main",
            "anygrasp_planner_node = soarm100_vision.anygrasp_planner_node:main",
            "mujoco_policy_backend_node = soarm100_vision.mujoco_policy_backend_node:main",
            "mujoco_mirror_viewer_node = soarm100_vision.mujoco_mirror_viewer_node:main",
            "mujoco_camera_publisher_node = soarm100_vision.mujoco_camera_publisher_node:main",
            "hardware_joint_state_node = soarm100_vision.hardware_joint_state_node:main",
            "hardware_single_joint_service_node = soarm100_vision.hardware_single_joint_service_node:main",
            "hardware_controller_node = soarm100_vision.hardware_controller_node:main",
            "policy_reach_node = soarm100_vision.policy_reach_node:main",
            "real_policy_grasp_backend_node = soarm100_vision.real_policy_grasp_backend_node:main",
            "wrist_handeye_calibrator_node = soarm100_vision.wrist_handeye_calibrator_node:main",
            "wrist_handeye_pose_sequence_node = soarm100_vision.wrist_handeye_pose_sequence_node:main",
            "orbbec_eye_to_hand_calibrator_node = soarm100_vision.orbbec_eye_to_hand_calibrator_node:main",
            "sdf_cbf_backend_node = soarm100_vision.sdf_cbf_backend_node:main",
            "debug_viewer_node = soarm100_vision.debug_viewer_node:main",
            "grasp_orchestrator_node = soarm100_vision.grasp_orchestrator_node:main",
            "send_planned_grasp = soarm100_vision.send_planned_grasp_node:main",
            "send_execute_grasp = soarm100_vision.send_execute_grasp_node:main",
        ],
    },
)
