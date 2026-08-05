#!/usr/bin/env python3
"""Display a fixed MuJoCo reference pose for hardware alignment."""

from __future__ import annotations

import argparse
import math
import time
from pathlib import Path

import mujoco
import mujoco.viewer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MJCF = (
    PROJECT_ROOT
    / "SO-ARM100"
    / "Simulation"
    / "SO100"
    / "mujoco"
    / "so100_plus.xml"
)
JOINT_NAMES = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)
HOME_QPOS = (0.0, -math.pi / 2, math.pi / 2, 0.0, 0.0, 0.0, 0.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mjcf", type=Path, default=DEFAULT_MJCF)
    parser.add_argument(
        "--oscillate-joint",
        choices=JOINT_NAMES,
        help="Optionally alternate this joint between home and a positive delta",
    )
    parser.add_argument("--delta-deg", type=float, default=10.0)
    parser.add_argument("--period", type=float, default=2.0)
    args = parser.parse_args()
    if args.delta_deg <= 0 or args.delta_deg > 20:
        parser.error("--delta-deg must be within (0, 20]")
    if args.period < 1:
        parser.error("--period must be at least 1 second")
    return args


def set_pose(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    values: tuple[float, ...] | list[float],
) -> None:
    for name, value in zip(JOINT_NAMES, values, strict=True):
        joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
        if joint_id < 0:
            raise ValueError(f"joint not found in MJCF: {name}")
        data.qpos[model.jnt_qposadr[joint_id]] = value
    mujoco.mj_forward(model, data)


def main() -> int:
    args = parse_args()
    model = mujoco.MjModel.from_xml_path(str(args.mjcf.resolve()))
    data = mujoco.MjData(model)
    pose = list(HOME_QPOS)
    set_pose(model, data, pose)

    print("[mujoco_reference] policy home q(rad):")
    for name, value in zip(JOINT_NAMES, HOME_QPOS, strict=True):
        print(f"  {name:28s} {value:+.6f}")
    if args.oscillate_joint:
        print(
            f"[mujoco_reference] oscillating {args.oscillate_joint} "
            f"between home and +{args.delta_deg:.1f}deg"
        )
    else:
        print("[mujoco_reference] fixed pose; close the viewer to exit")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        phase_positive = False
        next_switch = time.monotonic() + args.period
        while viewer.is_running():
            if args.oscillate_joint and time.monotonic() >= next_switch:
                phase_positive = not phase_positive
                pose = list(HOME_QPOS)
                if phase_positive:
                    index = JOINT_NAMES.index(args.oscillate_joint)
                    pose[index] += math.radians(args.delta_deg)
                set_pose(model, data, pose)
                state = "positive" if phase_positive else "home"
                print(f"[mujoco_reference] state={state}")
                next_switch = time.monotonic() + args.period
            viewer.sync()
            time.sleep(1 / 30)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
