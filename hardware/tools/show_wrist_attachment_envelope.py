#!/usr/bin/env python3
"""Visualize the real obstacle self-filter box on the MuJoCo wrist."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import time

import mujoco
import mujoco.viewer
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MJCF = (
    PROJECT_ROOT
    / "SO-ARM100"
    / "Simulation"
    / "SO100"
    / "mujoco"
    / "scene_plus_norod.xml"
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

# These wrist_jaw.STL bounds mirror obstacle_cloud_node.py exactly.
FILTER_BODY = "wrist_jaw"
MESH_CENTER_LOCAL = np.array([0.020100, 0.0, 0.021400], dtype=np.float64)
MESH_HALF_SIZE = np.array([0.037100, 0.020613, 0.045200], dtype=np.float64)
FILTER_MARGIN = 0.004


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mjcf", type=Path, default=DEFAULT_MJCF)
    parser.add_argument(
        "--oscillate",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Oscillate wrist_jaw to verify that both boxes follow the link",
    )
    parser.add_argument("--delta-deg", type=float, default=25.0)
    parser.add_argument("--period-s", type=float, default=2.0)
    parser.add_argument("--check-only", action="store_true", help="Validate geometry without GUI")
    args = parser.parse_args()
    if not 0.0 < args.delta_deg <= 45.0:
        parser.error("--delta-deg must be within (0, 45]")
    if args.period_s < 1.0:
        parser.error("--period-s must be at least 1.0")
    return args


def set_pose(model: mujoco.MjModel, data: mujoco.MjData, pose: list[float]) -> None:
    for name, value in zip(JOINT_NAMES, pose, strict=True):
        joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
        if joint_id < 0:
            raise ValueError(f"joint not found: {name}")
        data.qpos[int(model.jnt_qposadr[joint_id])] = float(value)
    mujoco.mj_forward(model, data)


def add_link_box(
    scene,
    body_position: np.ndarray,
    body_rotation: np.ndarray,
    center_local: np.ndarray,
    half_size: np.ndarray,
    rgba: tuple[float, float, float, float],
) -> None:
    if scene.ngeom >= len(scene.geoms):
        return
    center_world = body_position + body_rotation @ center_local
    mujoco.mjv_initGeom(
        scene.geoms[scene.ngeom],
        mujoco.mjtGeom.mjGEOM_BOX,
        np.asarray(half_size, dtype=np.float64),
        center_world,
        body_rotation.reshape(9),
        np.asarray(rgba, dtype=np.float32),
    )
    scene.ngeom += 1


def draw_overlay(viewer, model: mujoco.MjModel, data: mujoco.MjData) -> None:
    body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, FILTER_BODY)
    if body_id < 0:
        raise ValueError(f"body not found: {FILTER_BODY}")
    position = np.asarray(data.xpos[body_id], dtype=np.float64)
    rotation = np.asarray(data.xmat[body_id], dtype=np.float64).reshape(3, 3)
    with viewer.lock():
        scene = viewer.user_scn
        scene.ngeom = 0
        add_link_box(
            scene,
            position,
            rotation,
            MESH_CENTER_LOCAL,
            MESH_HALF_SIZE + FILTER_MARGIN,
            (1.0, 0.0, 0.75, 0.28),
        )
        add_link_box(
            scene,
            position,
            rotation,
            MESH_CENTER_LOCAL,
            MESH_HALF_SIZE,
            (0.0, 0.9, 1.0, 0.22),
        )


def main() -> int:
    args = parse_args()
    model = mujoco.MjModel.from_xml_path(str(args.mjcf.expanduser().resolve()))
    data = mujoco.MjData(model)
    pose = list(HOME_QPOS)
    set_pose(model, data, pose)

    full_size_mm = 2.0 * (MESH_HALF_SIZE + FILTER_MARGIN) * 1000.0
    print("[wrist_envelope] magenta = active self-filter box")
    print("[wrist_envelope] cyan = tight wrist_jaw.STL bounds (inside magenta)")
    print(
        "[wrist_envelope] filter center local mm="
        f"{MESH_CENTER_LOCAL * 1000.0}; size mm={full_size_mm}"
    )
    print("[wrist_envelope] close the viewer to exit")

    if args.check_only:
        body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, FILTER_BODY)
        rotation = np.asarray(data.xmat[body_id], dtype=np.float64).reshape(3, 3)
        center_world = np.asarray(data.xpos[body_id]) + rotation @ MESH_CENTER_LOCAL
        print(f"[wrist_envelope] home world center m={center_world}")
        return 0

    started = time.monotonic()
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            if args.oscillate:
                phase = math.sin(2.0 * math.pi * (time.monotonic() - started) / args.period_s)
                pose[JOINT_NAMES.index("wrist_jaw_joint")] = math.radians(args.delta_deg) * phase
                set_pose(model, data, pose)
            draw_overlay(viewer, model, data)
            viewer.sync()
            time.sleep(1.0 / 30.0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
