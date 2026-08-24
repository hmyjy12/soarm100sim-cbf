#!/usr/bin/env python3
"""Build per-link residual self-occupancy from an empty-scene scan."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

import mujoco
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = PROJECT_ROOT / "ros2" / "soarm100_vision"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from soarm100_vision.policy_backend_core import points_to_base_from_calib
from soarm100_vision.sdf_cbf_core import (
    DEFAULT_SELF_FILTER_CAPSULES,
    TableFilter,
    WorkspaceCrop,
    filter_capsule_self_points,
    filter_oriented_box_self_points,
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
LEARNED_LINKS = ("ellbow", "wrist_pitch", "wrist_jaw", "wrist_roll")
WRIST_BOX_CENTER = np.array([0.020100, 0.0, 0.021400], dtype=np.float64)
WRIST_BOX_HALF_SIZE = np.array([0.037100, 0.020613, 0.045200], dtype=np.float64)
WRIST_BOX_MARGIN = 0.004


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, help="Scan directory containing manifest.json")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("hardware/calibration/link_self_occupancy.npz"),
    )
    parser.add_argument(
        "--mjcf",
        type=Path,
        default=Path("SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"),
    )
    parser.add_argument(
        "--calib-json",
        default="hardware/calibration/camera/real_camera_calib.json",
    )
    parser.add_argument("--camera-name", default="scene_depth")
    parser.add_argument("--voxel-size-m", type=float, default=0.008)
    parser.add_argument("--association-radius-m", type=float, default=0.120)
    parser.add_argument("--min-hit-frames", type=int, default=3)
    parser.add_argument("--pixel-stride", type=int, default=4)
    args = parser.parse_args()
    if not 0.004 <= args.voxel_size_m <= 0.020:
        parser.error("--voxel-size-m must be within [0.004, 0.020]")
    if not 0.05 <= args.association_radius_m <= 0.20:
        parser.error("--association-radius-m must be within [0.05, 0.20]")
    if args.min_hit_frames < 2:
        parser.error("--min-hit-frames must be at least 2")
    return args


def resolve(path: Path) -> Path:
    return (path if path.is_absolute() else PROJECT_ROOT / path).expanduser().resolve()


def depth_to_camera_points(depth: np.ndarray, k: np.ndarray, stride: int) -> np.ndarray:
    image = np.asarray(depth)
    z = image.astype(np.float64)
    if np.issubdtype(image.dtype, np.integer):
        z *= 0.001
    rows, cols = np.mgrid[0 : image.shape[0] : stride, 0 : image.shape[1] : stride]
    z = z[::stride, ::stride]
    valid = np.isfinite(z) & (z > 0.05) & (z < 2.0)
    fx, fy, cx, cy = float(k[0]), float(k[4]), float(k[2]), float(k[5])
    x = (cols[valid] - cx) * z[valid] / fx
    y = (rows[valid] - cy) * z[valid] / fy
    return np.column_stack((x, y, z[valid]))


class RobotGeometry:
    def __init__(self, mjcf: Path) -> None:
        self.model = mujoco.MjModel.from_xml_path(str(mjcf))
        self.data = mujoco.MjData(self.model)
        self.joint_qpos = []
        for name in JOINT_NAMES:
            joint_id = mujoco.mj_name2id(
                self.model, mujoco.mjtObj.mjOBJ_JOINT, name
            )
            if joint_id < 0:
                raise ValueError(f"joint missing from MJCF: {name}")
            self.joint_qpos.append(int(self.model.jnt_qposadr[joint_id]))
        self.body_ids = {
            name: int(mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, name))
            for name in LEARNED_LINKS
        }
        self.capsule_ids = []
        for start, end, radius in DEFAULT_SELF_FILTER_CAPSULES:
            a = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, start)
            b = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, end)
            self.capsule_ids.append((int(a), int(b), float(radius)))

    def forward(self, q: np.ndarray) -> None:
        for address, value in zip(self.joint_qpos, q, strict=True):
            self.data.qpos[address] = float(value)
        mujoco.mj_forward(self.model, self.data)

    def remove_rigid(self, points: np.ndarray) -> tuple[np.ndarray, int]:
        capsules = [
            (
                np.asarray(self.data.xpos[a]).copy(),
                np.asarray(self.data.xpos[b]).copy(),
                radius,
            )
            for a, b, radius in self.capsule_ids
        ]
        filtered, capsule_removed = filter_capsule_self_points(
            points, capsules, margin_m=0.020
        )
        body_id = self.body_ids["wrist_jaw"]
        rotation = np.asarray(self.data.xmat[body_id]).reshape(3, 3)
        center = np.asarray(self.data.xpos[body_id]) + rotation @ WRIST_BOX_CENTER
        filtered, box_removed = filter_oriented_box_self_points(
            filtered,
            center,
            rotation,
            WRIST_BOX_HALF_SIZE,
            WRIST_BOX_MARGIN,
        )
        return filtered, capsule_removed + box_removed

    def assign_local(self, points: np.ndarray, max_distance: float):
        if points.shape[0] == 0:
            return {}
        local_by_link = {}
        distances = []
        for name in LEARNED_LINKS:
            body_id = self.body_ids[name]
            position = np.asarray(self.data.xpos[body_id])
            rotation = np.asarray(self.data.xmat[body_id]).reshape(3, 3)
            local = (points - position.reshape(1, 3)) @ rotation
            local_by_link[name] = local
            distances.append(np.linalg.norm(local, axis=1))
        distance_matrix = np.column_stack(distances)
        nearest = np.argmin(distance_matrix, axis=1)
        nearest_distance = distance_matrix[np.arange(points.shape[0]), nearest]
        assigned = {}
        for index, name in enumerate(LEARNED_LINKS):
            mask = (nearest == index) & (nearest_distance <= max_distance)
            assigned[name] = local_by_link[name][mask]
        return assigned


def main() -> int:
    args = parse_args()
    dataset = resolve(args.dataset)
    manifest = json.loads((dataset / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "complete":
        raise RuntimeError(f"dataset is not complete: {manifest.get('status')}")
    robot = RobotGeometry(resolve(args.mjcf))
    frame_hits = {name: defaultdict(int) for name in LEARNED_LINKS}
    processed_frames = 0
    total_residual = 0
    total_rigid = 0

    workspace = WorkspaceCrop(0.02, 0.45, -0.30, 0.30, 0.01, 0.45)
    table = TableFilter(True, 0.055)
    for frame_index, entry in enumerate(manifest["frames"]):
        payload = np.load(dataset / entry["file"])
        q = np.asarray(payload["q"], dtype=np.float64)
        camera_points = depth_to_camera_points(
            payload["depth"], payload["camera_k"], int(args.pixel_stride)
        )
        points = points_to_base_from_calib(
            camera_points,
            repo_root=PROJECT_ROOT,
            calib_json=str(args.calib_json),
            input_camera_name=str(args.camera_name),
        )
        points = workspace.apply(points)
        points, _ = table.apply(points)
        robot.forward(q)
        residual, rigid_removed = robot.remove_rigid(points)
        assigned = robot.assign_local(residual, float(args.association_radius_m))
        for name, local_points in assigned.items():
            if local_points.shape[0] == 0:
                continue
            keys = np.unique(
                np.floor(local_points / float(args.voxel_size_m)).astype(np.int32),
                axis=0,
            )
            for key in map(tuple, keys.tolist()):
                frame_hits[name][key] += 1
        processed_frames += 1
        total_residual += int(residual.shape[0])
        total_rigid += int(rigid_removed)
        print(
            f"[build] frame {frame_index + 1}/{len(manifest['frames'])} "
            f"rigid_rm={rigid_removed} residual={residual.shape[0]}"
        )

    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    arrays = {}
    summary = {}
    for name in LEARNED_LINKS:
        selected = [
            (key, hits)
            for key, hits in frame_hits[name].items()
            if hits >= int(args.min_hit_frames)
        ]
        keys = np.asarray([item[0] for item in selected], dtype=np.int32).reshape(-1, 3)
        hits = np.asarray([item[1] for item in selected], dtype=np.int32)
        probability = hits.astype(np.float32) / max(processed_frames, 1)
        arrays[f"{name}_keys"] = keys
        arrays[f"{name}_hit_frames"] = hits
        arrays[f"{name}_probability"] = probability
        summary[name] = {
            "voxels": int(keys.shape[0]),
            "max_probability": float(probability.max()) if probability.size else 0.0,
        }
    arrays["voxel_size_m"] = np.array(float(args.voxel_size_m), dtype=np.float64)
    arrays["processed_frames"] = np.array(processed_frames, dtype=np.int32)
    np.savez_compressed(output, **arrays)
    metadata = {
        "schema_version": 1,
        "source_dataset": str(dataset),
        "processed_frames": processed_frames,
        "voxel_size_m": float(args.voxel_size_m),
        "association_radius_m": float(args.association_radius_m),
        "min_hit_frames": int(args.min_hit_frames),
        "mean_rigid_removed_points": total_rigid / max(processed_frames, 1),
        "mean_residual_points": total_residual / max(processed_frames, 1),
        "links": summary,
        "runtime_enabled": False,
    }
    output.with_suffix(".json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    print(f"[build] wrote {output}")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
