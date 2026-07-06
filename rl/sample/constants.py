"""Shared constants for SO-100 Plus sampling (no Isaac Lab dependency)."""

REACH_JOINT_NAMES: tuple[str, ...] = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)

GRIPPER_JOINT_NAME = "gripper_joint"
BASE_LINK_NAME = "base"

# 捏合中心 TCP：定爪在 wrist_roll mesh，动爪在 gripper link。
WRIST_ROLL_BODY_NAME = "wrist_roll"
GRIPPER_BODY_NAME = "gripper"
# FK 雅可比链末端（最后一个可控 link body）。
TCP_BODY_NAME = GRIPPER_BODY_NAME

# 指尖参考点（各 link 局部坐标，单位 m）。可按 CAD/实机标定后修改。
TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL: tuple[float, float, float] = (0.0, -0.031, 0.030)
TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER: tuple[float, float, float] = (0.0, 0.031, 0.004)
# 工具系 z 轴（approach）在 wrist_roll 局部系中的方向。
TCP_APPROACH_LOCAL_WRIST_ROLL: tuple[float, float, float] = (0.0, 0.0, 1.0)

HOME_JOINT_POS: dict[str, float] = {
    "shoulder_rotation_joint": 0.0,
    "shoulder_pitch_joint": -1.57079,
    "ellbow_joint": 1.57079,
    "wrist_pitch_joint": 0.0,
    "wrist_jaw_joint": 0.0,
    "wrist_roll_joint": 0.0,
    "gripper_joint": 0.0,
}
