"""SO-100 Plus 工作空间采样（关节随机 + FK 预筛 + Isaac 验证）。

流程与 tar&ori/sample.py 一致：
  1) 在 URDF 关节限位内随机 joint_pos，用解析 FK 雅可比做奇异性/可操作性预筛；
  2) 将候选写入 Isaac 仿真，步进稳定后做接触力碰撞过滤；
  3) 读取仿真中的关节状态与捏合中心 TCP 位姿落盘（字段 `tcp`）。
"""

from __future__ import annotations

import math
import os
import random
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import torch

import isaaclab.sim as sim_utils
from isaaclab.scene import InteractiveScene
from isaaclab.sim import SimulationContext
from pxr import Usd

from sample.constants import (
    GRIPPER_BODY_NAME,
    HOME_JOINT_POS,
    REACH_JOINT_NAMES,
    TCP_BODY_NAME,
    WRIST_ROLL_BODY_NAME,
)
from sample.pipeline import ChunkedDataSink, PipelinePaths
from sample.robot_cfg import SampleSceneCfg, build_so100_plus_cfg
from sample.tcp_pose import (
    compute_pinch_tcp_pose_numpy,
    pose_dict_from_arrays,
    rotmat_to_quat_wxyz,
)


@dataclass
class JointInfo:
    name: str
    parent: str
    child: str
    axis: np.ndarray
    origin_xyz: np.ndarray
    origin_rpy: np.ndarray
    lower: float
    upper: float
    joint_type: str


def _parse_xyz(value: str | None, default: tuple[float, float, float]) -> np.ndarray:
    if value is None:
        return np.array(default, dtype=np.float64)
    return np.array([float(item) for item in value.split()], dtype=np.float64)


def _rpy_to_rot(rpy: np.ndarray) -> np.ndarray:
    roll, pitch, yaw = rpy
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]], dtype=np.float64)
    ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]], dtype=np.float64)
    rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]], dtype=np.float64)
    return rz @ ry @ rx


def _axis_angle_to_rot(axis: np.ndarray, angle: float) -> np.ndarray:
    axis = axis / (np.linalg.norm(axis) + 1e-12)
    x, y, z = axis
    c = math.cos(angle)
    s = math.sin(angle)
    v = 1.0 - c
    return np.array(
        [
            [x * x * v + c, x * y * v - z * s, x * z * v + y * s],
            [y * x * v + z * s, y * y * v + c, y * z * v - x * s],
            [z * x * v - y * s, z * y * v + x * s, z * z * v + c],
        ],
        dtype=np.float64,
    )


def _parse_urdf(urdf_path: str) -> tuple[Dict[str, JointInfo], Dict[str, str]]:
    root = ET.parse(urdf_path).getroot()
    joints: Dict[str, JointInfo] = {}
    child_to_joint: Dict[str, str] = {}
    for joint_elem in root.findall("joint"):
        parent_elem = joint_elem.find("parent")
        child_elem = joint_elem.find("child")
        if parent_elem is None or child_elem is None:
            continue
        origin_elem = joint_elem.find("origin")
        axis_elem = joint_elem.find("axis")
        limit_elem = joint_elem.find("limit")
        axis = _parse_xyz(axis_elem.attrib.get("xyz") if axis_elem is not None else None, (0.0, 0.0, 1.0))
        axis = axis / max(np.linalg.norm(axis), 1e-12)
        lower = float(limit_elem.attrib.get("lower", -math.pi)) if limit_elem is not None else -math.pi
        upper = float(limit_elem.attrib.get("upper", math.pi)) if limit_elem is not None else math.pi
        info = JointInfo(
            name=joint_elem.attrib["name"],
            parent=parent_elem.attrib["link"],
            child=child_elem.attrib["link"],
            axis=axis,
            origin_xyz=_parse_xyz(origin_elem.attrib.get("xyz") if origin_elem is not None else None, (0.0, 0.0, 0.0)),
            origin_rpy=_parse_xyz(origin_elem.attrib.get("rpy") if origin_elem is not None else None, (0.0, 0.0, 0.0)),
            lower=lower,
            upper=upper,
            joint_type=joint_elem.attrib.get("type", "fixed"),
        )
        joints[info.name] = info
        child_to_joint[info.child] = info.name
    return joints, child_to_joint


def _chain(child_to_joint: Dict[str, str], joints: Dict[str, JointInfo], base_link: str, ee_link: str) -> List[str]:
    chain: List[str] = []
    current = ee_link
    while current != base_link:
        joint_name = child_to_joint.get(current)
        if joint_name is None:
            raise RuntimeError(f"无法回溯链路: {base_link} -> {ee_link}")
        chain.append(joint_name)
        current = joints[joint_name].parent
    chain.reverse()
    return chain


def _fk_jac(
    chain: List[str],
    joints: Dict[str, JointInfo],
    q_map: Dict[str, float],
    active_set: set[str],
) -> tuple[np.ndarray, np.ndarray]:
    transform = np.eye(4, dtype=np.float64)
    axes_w: List[np.ndarray] = []
    pos_w: List[np.ndarray] = []
    for joint_name in chain:
        joint = joints[joint_name]
        joint_transform = transform.copy()
        joint_transform[:3, :3] = transform[:3, :3] @ _rpy_to_rot(joint.origin_rpy)
        joint_transform[:3, 3] = transform[:3, :3] @ joint.origin_xyz + transform[:3, 3]
        angle = float(q_map.get(joint_name, 0.0))
        rot_active = _axis_angle_to_rot(joint.axis, angle) if joint.joint_type == "revolute" else np.eye(3)
        if joint_name in active_set:
            axes_w.append(joint_transform[:3, :3] @ joint.axis)
            pos_w.append(joint_transform[:3, 3].copy())
        transform = joint_transform.copy()
        transform[:3, :3] = joint_transform[:3, :3] @ rot_active
    position = transform[:3, 3]
    jacobian = np.zeros((6, len(axes_w)), dtype=np.float64)
    for index, (axis_w, origin_w) in enumerate(zip(axes_w, pos_w)):
        jacobian[:3, index] = np.cross(axis_w, position - origin_w)
        jacobian[3:, index] = axis_w
    return transform, jacobian


def _fk_link_transforms(
    chain: List[str],
    joints: Dict[str, JointInfo],
    q_map: Dict[str, float],
) -> Dict[str, np.ndarray]:
    transform = np.eye(4, dtype=np.float64)
    out: Dict[str, np.ndarray] = {"base": transform.copy()}
    for joint_name in chain:
        joint = joints[joint_name]
        joint_transform = transform.copy()
        joint_transform[:3, :3] = transform[:3, :3] @ _rpy_to_rot(joint.origin_rpy)
        joint_transform[:3, 3] = transform[:3, :3] @ joint.origin_xyz + transform[:3, 3]
        angle = float(q_map.get(joint_name, 0.0))
        rot_active = _axis_angle_to_rot(joint.axis, angle) if joint.joint_type == "revolute" else np.eye(3)
        transform = joint_transform.copy()
        transform[:3, :3] = joint_transform[:3, :3] @ rot_active
        out[joint.child] = transform.copy()
    return out


def _transform_pos_quat(transform: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pos = transform[:3, 3].copy()
    quat = rotmat_to_quat_wxyz(transform[:3, :3])
    return pos, quat


def _fk_pinch_tcp_rel(
    chain: List[str],
    joints: Dict[str, JointInfo],
    q_map: Dict[str, float],
) -> np.ndarray:
    transforms = _fk_link_transforms(chain, joints, q_map)
    wr_pos, wr_quat = _transform_pos_quat(transforms[WRIST_ROLL_BODY_NAME])
    gr_pos, gr_quat = _transform_pos_quat(transforms[GRIPPER_BODY_NAME])
    tcp_pos, _ = compute_pinch_tcp_pose_numpy(wr_pos, wr_quat, gr_pos, gr_quat)
    return tcp_pos


def _clip_with_margin(lower: float, upper: float, ratio: float) -> tuple[float, float]:
    span = upper - lower
    margin = max(1e-4, span * ratio)
    lo, hi = lower + margin, upper - margin
    if lo >= hi:
        mid = 0.5 * (lower + upper)
        lo, hi = mid - 1e-4, mid + 1e-4
    return lo, hi


def _resolve_spawnable_usd_path(src_usd_path: str, preferred_prim_path: str) -> str:
    stage = Usd.Stage.Open(src_usd_path)
    if stage is None:
        raise RuntimeError(f"无法打开 USD: {src_usd_path}")

    preferred = preferred_prim_path.strip()
    default_prim = stage.GetDefaultPrim()
    default_path = default_prim.GetPath().pathString if default_prim and default_prim.IsValid() else ""
    root_prims = [prim for prim in stage.GetPseudoRoot().GetChildren() if prim.IsValid()]
    root_paths = [prim.GetPath().pathString for prim in root_prims]

    candidate_paths: List[str] = []
    if preferred:
        candidate_paths.append(preferred)
    for path in ("/World/Robot", "/Robot", "/so100_plus"):
        if path not in candidate_paths:
            candidate_paths.append(path)
    if default_path:
        candidate_paths.append(default_path)
    for path in root_paths:
        if path not in candidate_paths:
            candidate_paths.append(path)

    chosen = ""
    for path in candidate_paths:
        prim = stage.GetPrimAtPath(path)
        if prim and prim.IsValid():
            chosen = path
            break
    if not chosen:
        raise RuntimeError(
            f"USD 中未找到可引用机器人 prim。defaultPrim={default_path!r}, root_prims={root_paths}"
        )
    if chosen == default_path and default_path:
        print(f"[INFO] USD defaultPrim 有效，直接使用: {default_path}")
        return src_usd_path
    return src_usd_path


def run_isaac_sampling(args, paths: PipelinePaths, sink: ChunkedDataSink) -> None:
    if not os.path.isfile(args.urdf_path):
        raise FileNotFoundError(f"URDF 不存在: {args.urdf_path}")
    if not os.path.isfile(args.usd_path):
        raise FileNotFoundError(
            f"USD 不存在: {args.usd_path}\n"
            "请先使用 Isaac Lab convert_urdf.py 从 so100_plus.urdf 转换生成 USD。"
        )

    joints, child_to_joint = _parse_urdf(args.urdf_path)
    chain = _chain(child_to_joint, joints, "base", TCP_BODY_NAME)
    active_names = list(REACH_JOINT_NAMES)
    all_joint_names = list(REACH_JOINT_NAMES)
    active_set = set(active_names)
    xyz_min = np.array([args.x_min, args.y_min, args.z_min], dtype=np.float64)
    xyz_max = np.array([args.x_max, args.y_max, args.z_max], dtype=np.float64)

    sim_cfg = sim_utils.SimulationCfg(dt=args.dt, device=args.device)
    sim = SimulationContext(sim_cfg)
    spawnable_usd = _resolve_spawnable_usd_path(args.usd_path, args.usd_robot_prim_path)
    robot_cfg = build_so100_plus_cfg(
        spawnable_usd,
        enable_self_collisions=not args.disable_self_collision,
    ).replace(prim_path="{ENV_REGEX_NS}/Robot")

    scene_cfg = SampleSceneCfg(
        num_envs=max(1, int(args.num_envs)),
        env_spacing=1.5,
    )
    scene_cfg.robot = robot_cfg
    scene = InteractiveScene(scene_cfg)
    sim.reset()
    scene.reset()
    robot = scene["robot"]

    joint_ids = {name: int(robot.find_joints(name)[0][0]) for name in all_joint_names}
    wrist_roll_ids, _ = robot.find_bodies(WRIST_ROLL_BODY_NAME)
    gripper_ids, _ = robot.find_bodies(GRIPPER_BODY_NAME)
    if len(wrist_roll_ids) == 0:
        raise RuntimeError(f"未在仿真中找到 body: {WRIST_ROLL_BODY_NAME}")
    if len(gripper_ids) == 0:
        raise RuntimeError(f"未在仿真中找到 body: {GRIPPER_BODY_NAME}")
    wrist_roll_body_id = int(wrist_roll_ids[0])
    gripper_body_id = int(gripper_ids[0])

    num_envs = int(args.num_envs)
    env_ids = torch.arange(num_envs, device=sim.device)
    default_pos = robot.data.default_joint_pos[0].clone()
    zero_vel = torch.zeros_like(robot.data.joint_vel[:num_envs])
    rng = random.Random(args.seed)
    bounds = {
        name: _clip_with_margin(joints[name].lower, joints[name].upper, args.joint_margin_ratio)
        for name in active_names
    }

    global_record_idx = sink.total_records
    accepted = sink.total_records
    attempts = 0
    max_attempts = max(1, int(args.max_attempt_factor) * int(args.num_samples))
    phase_start = time.time()
    last_progress = 0.0

    def _print_progress(force: bool = False) -> None:
        nonlocal last_progress
        if not args.show_progress:
            return
        now = time.time()
        if (not force) and (now - last_progress < max(float(args.progress_refresh_sec), 0.05)):
            return
        last_progress = now
        ratio = min(1.0, accepted / max(1, int(args.num_samples)))
        bar_len = 28
        filled = int(ratio * bar_len)
        bar = "#" * filled + "-" * (bar_len - filled)
        elapsed = now - phase_start
        speed = accepted / max(elapsed, 1e-6)
        msg = (
            f"[sample] |{bar}| {accepted}/{args.num_samples} "
            f"({ratio * 100:5.1f}%) attempts={attempts} speed={speed:.2f}/s elapsed={elapsed:6.1f}s"
        )
        if sys.stdout.isatty():
            print("\r" + msg, end="", flush=True)
            if force:
                print(flush=True)
        else:
            print(msg, flush=True)

    while accepted < int(args.num_samples) and attempts < max_attempts:
        _print_progress()
        attempts += num_envs
        joint_pos_batch = default_pos.unsqueeze(0).repeat(num_envs, 1)
        pre_ok = [False] * num_envs
        q_maps: list[dict[str, float]] = []

        for env_i in range(num_envs):
            q_map = {name: float(HOME_JOINT_POS.get(name, 0.0)) for name in all_joint_names}
            for name in active_names:
                lo, hi = bounds[name]
                q_map[name] = rng.uniform(lo, hi)
            q_maps.append(q_map)
            _, jacobian = _fk_jac(chain, joints, q_map, active_set)
            linear_jac = jacobian[:3, :]
            singular_values = np.linalg.svd(linear_jac, compute_uv=False)
            sigma_min = float(np.min(singular_values))
            sigma_max = float(np.max(singular_values))
            cond = sigma_max / max(1e-12, sigma_min)
            manip = float(math.sqrt(max(np.linalg.det(linear_jac @ linear_jac.T), 0.0)))
            if (
                sigma_min < args.sigma_min_threshold
                or cond > args.cond_max_threshold
                or manip < args.manipulability_threshold
            ):
                continue
            try:
                tcp_rel_pre = _fk_pinch_tcp_rel(chain, joints, q_map)
            except KeyError:
                continue
            if not np.all((tcp_rel_pre > xyz_min) & (tcp_rel_pre < xyz_max)):
                continue
            pre_ok[env_i] = True
            for name in active_names:
                joint_pos_batch[env_i, joint_ids[name]] = float(q_map[name])

        robot.write_joint_state_to_sim(joint_pos_batch[:num_envs], zero_vel, None, env_ids)
        scene.write_data_to_sim()
        for _ in range(max(1, int(args.settle_steps))):
            sim.step()
            scene.update(args.dt)

        for env_i in range(num_envs):
            if accepted >= int(args.num_samples):
                break
            if not pre_ok[env_i]:
                continue

            contact_force = 0.0
            contact_forces = getattr(robot.data, "contact_sensor_forces_w", None)
            if contact_forces is not None and contact_forces.numel() > 0:
                contact_force = float(torch.norm(contact_forces[env_i], dim=-1).max().item())
            if contact_force > args.collision_force_threshold:
                continue

            root_pos = robot.data.root_pos_w[env_i, :3].detach().cpu().numpy()
            wr_pos_w = robot.data.body_pos_w[env_i, wrist_roll_body_id, :].detach().cpu().numpy()
            wr_quat_w = robot.data.body_quat_w[env_i, wrist_roll_body_id, :].detach().cpu().numpy()
            gr_pos_w = robot.data.body_pos_w[env_i, gripper_body_id, :].detach().cpu().numpy()
            gr_quat_w = robot.data.body_quat_w[env_i, gripper_body_id, :].detach().cpu().numpy()
            tcp_pos_w, tcp_quat_w = compute_pinch_tcp_pose_numpy(wr_pos_w, wr_quat_w, gr_pos_w, gr_quat_w)
            tcp_rel = tcp_pos_w - root_pos
            if not np.all((tcp_rel > xyz_min) & (tcp_rel < xyz_max)):
                continue

            tcp_block = pose_dict_from_arrays(
                tcp_rel,
                tcp_quat_w,
                orientation_format=args.orientation_format,
            )
            gripper_link_block = pose_dict_from_arrays(
                gr_pos_w - root_pos,
                gr_quat_w,
                orientation_format="quat",
            )

            arm_state = {}
            for name in all_joint_names:
                joint_id = joint_ids[name]
                arm_state[name] = {
                    "pos": float(robot.data.joint_pos[env_i, joint_id].item()),
                    "vel": float(robot.data.joint_vel[env_i, joint_id].item()),
                }

            global_record_idx += 1
            sink.add(
                {
                    "time": float(round(global_record_idx * args.dt, 6)),
                    "arm": arm_state,
                    "tcp": tcp_block,
                    "gripper_link": gripper_link_block,
                    "collision_force": float(contact_force),
                }
            )
            accepted += 1

    _print_progress(force=True)
    print(
        f"[sample] 请求={args.num_samples}, 成功={accepted}, 尝试={attempts}, "
        f"成功率={accepted / max(1, attempts):.3f}"
    )
    if accepted < int(args.num_samples):
        print("[WARN] 未达到目标采样数，可增大 max_attempt_factor 或放宽阈值/工作空间范围。")
