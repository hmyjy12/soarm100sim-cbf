#!/usr/bin/env python3
"""Compare end-effector FK between MuJoCo XML and URDF for SO-ARM100 Plus."""

from __future__ import annotations

import argparse
import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import mujoco
import numpy as np

# Repo-relative defaults.
PKG_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PKG_ROOT.parents[1]
DEFAULT_MJCF = REPO_ROOT / "SO-ARM100/Simulation/SO100/mujoco/so100_plus.xml"
DEFAULT_URDF = PKG_ROOT / "urdf/so100_plus.urdf"

JOINT_NAMES = [
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
]

TEST_POSES = {
    "zeros": [0.0] * 7,
    "home": [0.0, -1.57079, 1.57079, 0.0, 0.0, 0.0, 0.0],
    "mid": [0.5, -1.0, 1.2, 0.3, 0.2, 0.4, 0.5],
    "limits_low": [-2.2, -3.14158, 0.0, -2.0, -1.45, -3.14158, -0.2],
    "limits_high": [2.2, 0.2, 3.14158, 1.8, 1.45, 3.14158, 2.0],
}


@dataclass
class Pose:
  position: np.ndarray
  rotation: np.ndarray

  @classmethod
  def from_matrix(cls, transform: np.ndarray) -> "Pose":
    return cls(transform[:3, 3].copy(), transform[:3, :3].copy())

  def as_matrix(self) -> np.ndarray:
    transform = np.eye(4)
    transform[:3, :3] = self.rotation
    transform[:3, 3] = self.position
    return transform


def parse_xyz(text: str) -> np.ndarray:
  return np.array([float(v) for v in text.split()], dtype=float)


def rpy_to_matrix(roll: float, pitch: float, yaw: float) -> np.ndarray:
  cr, sr = math.cos(roll), math.sin(roll)
  cp, sp = math.cos(pitch), math.sin(pitch)
  cy, sy = math.cos(yaw), math.sin(yaw)
  return np.array(
      [
          [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
          [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
          [-sp, cp * sr, cp * cr],
      ],
      dtype=float,
  )


def make_transform(xyz: Sequence[float], rpy: Sequence[float]) -> np.ndarray:
  transform = np.eye(4)
  transform[:3, :3] = rpy_to_matrix(rpy[0], rpy[1], rpy[2])
  transform[:3, 3] = np.asarray(xyz, dtype=float)
  return transform


def rotation_about_axis(axis: Sequence[float], angle: float) -> np.ndarray:
  axis = np.asarray(axis, dtype=float)
  norm = np.linalg.norm(axis)
  if norm < 1e-12:
    raise ValueError("Joint axis has zero length")
  axis = axis / norm
  x, y, z = axis
  c = math.cos(angle)
  s = math.sin(angle)
  t = 1.0 - c
  return np.array(
      [
          [t * x * x + c, t * x * y - s * z, t * x * z + s * y],
          [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
          [t * x * z - s * y, t * y * z + s * x, t * z * z + c],
      ],
      dtype=float,
  )


def matrix_to_rpy(rotation: np.ndarray) -> np.ndarray:
  sy = -rotation[2, 0]
  if abs(sy) < 1.0 - 1e-8:
    pitch = math.asin(sy)
    roll = math.atan2(rotation[2, 1], rotation[2, 2])
    yaw = math.atan2(rotation[1, 0], rotation[0, 0])
  else:
    pitch = math.copysign(math.pi / 2.0, sy)
    roll = math.atan2(-rotation[0, 1], rotation[1, 1])
    yaw = 0.0
  return np.array([roll, pitch, yaw], dtype=float)


def rotation_error_deg(reference: np.ndarray, estimate: np.ndarray) -> float:
  delta = reference.T @ estimate
  trace = np.clip((np.trace(delta) - 1.0) * 0.5, -1.0, 1.0)
  return math.degrees(math.acos(trace))


@dataclass
class UrdfJoint:
  name: str
  parent: str
  child: str
  origin_xyz: np.ndarray
  origin_rpy: np.ndarray
  axis: np.ndarray
  joint_type: str


def load_urdf_joints(urdf_path: Path) -> Dict[str, UrdfJoint]:
  root = ET.parse(urdf_path).getroot()
  joints: Dict[str, UrdfJoint] = {}
  for joint_elem in root.findall("joint"):
    origin = joint_elem.find("origin")
    axis = joint_elem.find("axis")
    joints[joint_elem.attrib["name"]] = UrdfJoint(
        name=joint_elem.attrib["name"],
        parent=joint_elem.find("parent").attrib["link"],
        child=joint_elem.find("child").attrib["link"],
        origin_xyz=parse_xyz(origin.attrib.get("xyz", "0 0 0")) if origin is not None else np.zeros(3),
        origin_rpy=parse_xyz(origin.attrib.get("rpy", "0 0 0")) if origin is not None else np.zeros(3),
        axis=parse_xyz(axis.attrib.get("xyz", "0 0 1")) if axis is not None else np.array([0.0, 0.0, 1.0]),
        joint_type=joint_elem.attrib.get("type", "fixed"),
    )
  return joints


def build_joint_chain(joints: Dict[str, UrdfJoint], base_link: str, tip_link: str) -> List[str]:
  child_to_joint = {joint.child: name for name, joint in joints.items()}
  chain: List[str] = []
  current = tip_link
  while current != base_link:
    if current not in child_to_joint:
      raise ValueError(f"No joint found with child link '{current}'")
    joint_name = child_to_joint[current]
    chain.append(joint_name)
    current = joints[joint_name].parent
  chain.reverse()
  return chain


def urdf_fk(
    urdf_path: Path,
    joint_angles: Sequence[float],
    base_link: str = "base",
    tip_link: str = "gripper",
) -> Pose:
  joints = load_urdf_joints(urdf_path)
  joint_chain = build_joint_chain(joints, base_link, tip_link)
  if len(joint_chain) != len(joint_angles):
    raise ValueError(
        f"Expected {len(joint_chain)} joint angles, got {len(joint_angles)}"
    )

  transform = np.eye(4)
  for joint_name, angle in zip(joint_chain, joint_angles):
    joint = joints[joint_name]
    if joint.joint_type not in {"revolute", "continuous"}:
      raise ValueError(f"Unsupported joint type '{joint.joint_type}' for {joint_name}")

    joint_origin = make_transform(joint.origin_xyz, joint.origin_rpy)
    joint_motion = np.eye(4)
    joint_motion[:3, :3] = rotation_about_axis(joint.axis, angle)
    transform = transform @ joint_origin @ joint_motion

  return Pose.from_matrix(transform)


def mujoco_fk(
    mjcf_path: Path,
    joint_angles: Sequence[float],
    base_body: str = "base",
    tip_body: str = "gripper",
) -> Pose:
  model = mujoco.MjModel.from_xml_path(str(mjcf_path))
  data = mujoco.MjData(model)
  if len(joint_angles) != model.nq:
    raise ValueError(f"Expected {model.nq} joint angles, got {len(joint_angles)}")

  data.qpos[:] = joint_angles
  mujoco.mj_forward(model, data)

  base_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, base_body)
  tip_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, tip_body)

  base_pos = data.xpos[base_id].copy()
  base_mat = data.xmat[base_id].reshape(3, 3).copy()
  tip_pos = data.xpos[tip_id].copy()
  tip_mat = data.xmat[tip_id].reshape(3, 3).copy()

  base_inv = np.eye(4)
  base_inv[:3, :3] = base_mat.T
  base_inv[:3, 3] = -base_mat.T @ base_pos

  tip = np.eye(4)
  tip[:3, :3] = tip_mat
  tip[:3, 3] = tip_pos

  relative = base_inv @ tip
  return Pose.from_matrix(relative)


def compare_pose(pose_a: Pose, pose_b: Pose) -> Tuple[float, float, np.ndarray, np.ndarray]:
  position_error = float(np.linalg.norm(pose_a.position - pose_b.position))
  orientation_error = rotation_error_deg(pose_a.rotation, pose_b.rotation)
  return position_error, orientation_error, pose_a.position, pose_b.position


def format_pose(name: str, pose: Pose) -> str:
  rpy = matrix_to_rpy(pose.rotation)
  return (
      f"{name}:\n"
      f"  pos [m]  = [{pose.position[0]: .6f}, {pose.position[1]: .6f}, {pose.position[2]: .6f}]\n"
      f"  rpy [rad]= [{rpy[0]: .6f}, {rpy[1]: .6f}, {rpy[2]: .6f}]"
  )


def run_comparison(
    mjcf_path: Path,
    urdf_path: Path,
    poses: Dict[str, Sequence[float]],
    pos_tol_mm: float,
    rot_tol_deg: float,
) -> int:
  print("SO-ARM100 Plus FK comparison: MuJoCo XML vs URDF")
  print(f"  MJCF : {mjcf_path}")
  print(f"  URDF : {urdf_path}")
  print(f"  Tip  : gripper in base frame")
  print()

  failed = 0
  for pose_name, joint_angles in poses.items():
    mj_pose = mujoco_fk(mjcf_path, joint_angles)
    urdf_pose = urdf_fk(urdf_path, joint_angles)
    pos_err_m, rot_err_deg, mj_pos, urdf_pos = compare_pose(mj_pose, urdf_pose)
    pos_err_mm = pos_err_m * 1000.0
    ok = pos_err_mm <= pos_tol_mm and rot_err_deg <= rot_tol_deg
    failed += int(not ok)

    status = "PASS" if ok else "FAIL"
    print(f"[{status}] pose = {pose_name}")
    print(f"  joints = {np.array2string(np.asarray(joint_angles), precision=5, separator=', ')}")
    print(format_pose("  MuJoCo", mj_pose))
    print(format_pose("  URDF  ", urdf_pose))
    print(
        f"  error  : position = {pos_err_mm:.4f} mm, orientation = {rot_err_deg:.4f} deg"
    )
    print(f"  delta  : dpos = [{urdf_pos[0]-mj_pos[0]: .6f}, "
          f"{urdf_pos[1]-mj_pos[1]: .6f}, {urdf_pos[2]-mj_pos[2]: .6f}] m")
    print()

  if failed == 0:
    print("All poses match within tolerance.")
  else:
    print(f"{failed} pose(s) exceeded tolerance.")
  return failed


def parse_joint_list(text: str) -> List[float]:
  return [float(v) for v in text.split(",") if v.strip()]


def build_arg_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
      description="Compare MuJoCo and URDF forward kinematics for so100_plus."
  )
  parser.add_argument("--mjcf", type=Path, default=DEFAULT_MJCF, help="Path to MuJoCo XML")
  parser.add_argument("--urdf", type=Path, default=DEFAULT_URDF, help="Path to URDF")
  parser.add_argument(
      "--joints",
      type=str,
      default="",
      help="Comma-separated joint angles (rad). If set, only this pose is checked.",
  )
  parser.add_argument(
      "--pos-tol-mm",
      type=float,
      default=1.0,
      help="Position tolerance in millimeters",
  )
  parser.add_argument(
      "--rot-tol-deg",
      type=float,
      default=1.0,
      help="Orientation tolerance in degrees",
  )
  return parser


def main(argv: Iterable[str] | None = None) -> int:
  parser = build_arg_parser()
  args = parser.parse_args(argv)

  if not args.mjcf.is_file():
    raise FileNotFoundError(f"MJCF not found: {args.mjcf}")
  if not args.urdf.is_file():
    raise FileNotFoundError(f"URDF not found: {args.urdf}")

  if args.joints:
    poses = {"custom": parse_joint_list(args.joints)}
  else:
    poses = TEST_POSES

  return run_comparison(
      args.mjcf,
      args.urdf,
      poses,
      pos_tol_mm=args.pos_tol_mm,
      rot_tol_deg=args.rot_tol_deg,
  )


if __name__ == "__main__":
  raise SystemExit(main())
