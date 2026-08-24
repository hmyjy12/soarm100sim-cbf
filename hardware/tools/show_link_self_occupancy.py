#!/usr/bin/env python3
"""Show learned per-link occupancy voxels in the MuJoCo viewer."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import time

import mujoco
import mujoco.viewer
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
JOINT_NAMES = (
    "shoulder_rotation_joint", "shoulder_pitch_joint", "ellbow_joint",
    "wrist_pitch_joint", "wrist_jaw_joint", "wrist_roll_joint", "gripper_joint",
)
HOME_QPOS = (0.0, -math.pi / 2, math.pi / 2, 0.0, 0.0, 0.0, 0.0)
LINK_COLORS = {
    "ellbow": (1.0, 0.55, 0.0, 0.45),
    "wrist_pitch": (0.0, 0.8, 1.0, 0.45),
    "wrist_jaw": (1.0, 0.0, 0.75, 0.45),
    "wrist_roll": (0.3, 1.0, 0.2, 0.45),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "model",
        type=Path,
        nargs="?",
        default=Path("hardware/calibration/link_self_occupancy.npz"),
    )
    parser.add_argument(
        "--mjcf",
        type=Path,
        default=Path("SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"),
    )
    parser.add_argument("--min-probability", type=float, default=0.10)
    parser.add_argument("--max-voxels-per-link", type=int, default=400)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return (path if path.is_absolute() else PROJECT_ROOT / path).resolve()


def set_home(model, data) -> None:
    for name, value in zip(JOINT_NAMES, HOME_QPOS, strict=True):
        joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
        data.qpos[int(model.jnt_qposadr[joint_id])] = value
    mujoco.mj_forward(model, data)


def main() -> int:
    args = parse_args()
    occupancy = np.load(resolve(args.model))
    voxel_size = float(occupancy["voxel_size_m"])
    model = mujoco.MjModel.from_xml_path(str(resolve(args.mjcf)))
    data = mujoco.MjData(model)
    set_home(model, data)
    print("[occupancy_viewer] colors: " + ", ".join(LINK_COLORS))
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            with viewer.lock():
                scene = viewer.user_scn
                scene.ngeom = 0
                for name, color in LINK_COLORS.items():
                    keys = occupancy[f"{name}_keys"]
                    probability = occupancy[f"{name}_probability"]
                    selected = np.flatnonzero(probability >= args.min_probability)
                    if selected.size > args.max_voxels_per_link:
                        order = np.argsort(probability[selected])[-args.max_voxels_per_link :]
                        selected = selected[order]
                    body_id = mujoco.mj_name2id(
                        model, mujoco.mjtObj.mjOBJ_BODY, name
                    )
                    position = np.asarray(data.xpos[body_id])
                    rotation = np.asarray(data.xmat[body_id]).reshape(3, 3)
                    local = (keys[selected].astype(np.float64) + 0.5) * voxel_size
                    world = position + local @ rotation.T
                    for point in world:
                        if scene.ngeom >= len(scene.geoms):
                            break
                        mujoco.mjv_initGeom(
                            scene.geoms[scene.ngeom],
                            mujoco.mjtGeom.mjGEOM_BOX,
                            np.full(3, voxel_size * 0.48, dtype=np.float64),
                            point,
                            rotation.reshape(9),
                            np.asarray(color, dtype=np.float32),
                        )
                        scene.ngeom += 1
            viewer.sync()
            time.sleep(1.0 / 30.0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
