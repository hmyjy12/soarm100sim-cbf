#!/usr/bin/env python3
"""Closed-gripper hold smoke test.

This script bypasses policy, AnyGrasp, tracking, and CBF. It places the red
sphere directly at the current pinch TCP with the gripper already closed, then
holds joint position to check whether the current MuJoCo contact parameters can
keep the object in the gripper.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

import mujoco
import numpy as np

try:
    import mujoco.viewer
except Exception:  # pragma: no cover - optional GUI backend
    mujoco_viewer = None
else:
    mujoco_viewer = mujoco.viewer

_THIS = Path(__file__).resolve().parent


def _load_local(mod_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


_c = _load_local("so100_hold_constants", _THIS / "constants.py")
_rt = _load_local("so100_hold_runtime", _THIS / "runtime.py")

DEFAULT_MJCF_NOROD = _c.DEFAULT_MJCF_NOROD
SIM_DT = _c.SIM_DT
REACH_JOINT_NAMES = _c.REACH_JOINT_NAMES

TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL = np.asarray([0.0, -0.031, 0.030], dtype=np.float64)
TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER = np.asarray([0.0, 0.031, 0.004], dtype=np.float64)

resolve_robot_ids = _rt.resolve_robot_ids
reset_home = _rt.reset_home
set_ctrl = _rt.set_ctrl
tcp_pose_w = _rt.tcp_pose_w
joint_pos = _rt.joint_pos


def _joint_qpos_addr(model: mujoco.MjModel, name: str) -> int:
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
    if jid < 0:
        raise ValueError(f"joint not found: {name}")
    return int(model.jnt_qposadr[int(jid)])


def _body_id(model: mujoco.MjModel, name: str) -> int:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
    if bid < 0:
        raise ValueError(f"body not found: {name}")
    return int(bid)


def _geom_id(model: mujoco.MjModel, name: str) -> int:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, name)
    if gid < 0:
        raise ValueError(f"geom not found: {name}")
    return int(gid)


def _site_id(model: mujoco.MjModel, name: str) -> int:
    return int(mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, name))


def _actuator_id(model: mujoco.MjModel, name: str) -> int:
    aid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)
    if aid < 0:
        raise ValueError(f"actuator not found: {name}")
    return int(aid)


def _target_names(object_name: str) -> tuple[str, str, str]:
    if object_name == "sphere":
        return "target_sphere", "target_sphere_freejoint", "target_sphere_geom"
    if object_name == "cube":
        return "target_object", "target_object_freejoint", "target_object_geom"
    raise ValueError(f"unsupported --object: {object_name}")


def _disable_unused_targets(model: mujoco.MjModel, active_geom: str) -> None:
    for geom_name in ("target_sphere_geom", "target_object_geom", "target_bottle_geom"):
        gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, geom_name)
        if gid < 0 or geom_name == active_geom:
            continue
        model.geom_contype[gid] = 0
        model.geom_conaffinity[gid] = 0
        model.geom_rgba[gid, 3] = 0.0


def _set_free_body_pose(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    *,
    joint_name: str,
    pos: np.ndarray,
    quat_wxyz: np.ndarray | None = None,
) -> None:
    adr = _joint_qpos_addr(model, joint_name)
    data.qpos[adr : adr + 3] = np.asarray(pos, dtype=np.float64).reshape(3)
    quat = np.asarray(quat_wxyz if quat_wxyz is not None else [1.0, 0.0, 0.0, 0.0], dtype=np.float64)
    quat /= max(float(np.linalg.norm(quat)), 1e-12)
    data.qpos[adr + 3 : adr + 7] = quat
    vadr = int(model.jnt_dofadr[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)])
    data.qvel[vadr : vadr + 6] = 0.0


def _set_robot_q(model: mujoco.MjModel, data: mujoco.MjData, ids, q: np.ndarray) -> None:
    q = np.asarray(q, dtype=np.float64).reshape(len(ids.qpos_adr))
    for i, adr in enumerate(ids.qpos_adr):
        data.qpos[int(adr)] = float(q[i])
    mujoco.mj_forward(model, data)


def _parse_q(text: str, n: int) -> np.ndarray | None:
    if not text.strip():
        return None
    vals = [float(x) for x in text.split(",")]
    if len(vals) != n:
        raise ValueError(f"--init-q expects {n} comma-separated values, got {len(vals)}")
    return np.asarray(vals, dtype=np.float64)


def _count_geom_contacts(model: mujoco.MjModel, data: mujoco.MjData, geom_name: str) -> tuple[int, list[tuple[str, str]]]:
    gid = _geom_id(model, geom_name)
    pairs: list[tuple[str, str]] = []
    for i in range(int(data.ncon)):
        c = data.contact[i]
        if int(c.geom1) != gid and int(c.geom2) != gid:
            continue
        other = int(c.geom2) if int(c.geom1) == gid else int(c.geom1)
        other_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, other) or ""
        body_id = int(model.geom_bodyid[other])
        body_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, body_id) or ""
        pairs.append((other_name, body_name))
    return len(pairs), pairs


def _count_geom_body_contacts(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    *,
    geom_name: str,
    body_name: str,
) -> int:
    gid = _geom_id(model, geom_name)
    bid = _body_id(model, body_name)
    count = 0
    for i in range(int(data.ncon)):
        c = data.contact[i]
        if int(c.geom1) != gid and int(c.geom2) != gid:
            continue
        other = int(c.geom2) if int(c.geom1) == gid else int(c.geom1)
        if int(model.geom_bodyid[other]) == bid:
            count += 1
    return count


def _body_point_w(data: mujoco.MjData, body_id: int, point_local: np.ndarray) -> np.ndarray:
    rot = np.asarray(data.xmat[body_id], dtype=np.float64).reshape(3, 3)
    pos = np.asarray(data.xpos[body_id], dtype=np.float64)
    return pos + rot @ np.asarray(point_local, dtype=np.float64).reshape(3)


def _gripper_points_w(data: mujoco.MjData, ids) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fixed = _body_point_w(data, ids.wrist_roll_body, TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL)
    moving = _body_point_w(data, ids.gripper_body, TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER)
    center = 0.5 * (fixed + moving)
    return fixed, moving, center


def _finger_site_points_w(model: mujoco.MjModel, data: mujoco.MjData) -> tuple[np.ndarray | None, np.ndarray | None]:
    fixed_sid = _site_id(model, "fixed_finger_inner_site")
    moving_sid = _site_id(model, "moving_finger_inner_site")
    fixed = np.asarray(data.site_xpos[fixed_sid], dtype=np.float64).copy() if fixed_sid >= 0 else None
    moving = np.asarray(data.site_xpos[moving_sid], dtype=np.float64).copy() if moving_sid >= 0 else None
    return fixed, moving


def _quat_to_mat(quat_wxyz: np.ndarray) -> np.ndarray:
    rot = np.zeros(9, dtype=np.float64)
    mujoco.mju_quat2Mat(rot, np.asarray(quat_wxyz, dtype=np.float64).reshape(4))
    return rot.reshape(3, 3)


def _sphere_radius(model: mujoco.MjModel) -> float:
    gid = _geom_id(model, "target_sphere_geom")
    return float(model.geom_size[gid, 0])


def _object_contact_radius(model: mujoco.MjModel, geom_name: str) -> float:
    gid = _geom_id(model, geom_name)
    gtype = int(model.geom_type[gid])
    if gtype == int(mujoco.mjtGeom.mjGEOM_SPHERE):
        return float(model.geom_size[gid, 0])
    if gtype == int(mujoco.mjtGeom.mjGEOM_BOX):
        return float(np.max(model.geom_size[gid, :3]))
    return float(np.max(model.geom_size[gid]))


def _find_fixed_finger_surface_center(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    *,
    fixed_tip: np.ndarray,
    moving_tip: np.ndarray,
    radius: float,
    clearance: float,
    joint_name: str = "target_sphere_freejoint",
    geom_name: str = "target_sphere_geom",
) -> tuple[np.ndarray, dict]:
    direction = np.asarray(moving_tip - fixed_tip, dtype=np.float64)
    direction /= max(float(np.linalg.norm(direction)), 1e-12)
    max_s = max(float(np.linalg.norm(moving_tip - fixed_tip)) + radius, radius * 3.0)
    samples = np.linspace(0.0, max_s, 81)
    seen_fixed_contact = False
    chosen_s: float | None = None
    trace: list[dict] = []
    for s in samples:
        pos = fixed_tip + direction * float(s)
        _set_free_body_pose(model, data, joint_name=joint_name, pos=pos)
        mujoco.mj_forward(model, data)
        fixed_contacts = _count_geom_body_contacts(
            model, data, geom_name=geom_name, body_name="wrist_roll"
        )
        moving_contacts = _count_geom_body_contacts(
            model, data, geom_name=geom_name, body_name="gripper"
        )
        trace.append({"s": float(s), "fixed_contacts": int(fixed_contacts), "moving_contacts": int(moving_contacts)})
        if fixed_contacts > 0:
            seen_fixed_contact = True
            continue
        if seen_fixed_contact and moving_contacts == 0:
            chosen_s = float(s) + float(clearance)
            break
    if chosen_s is None:
        chosen_s = radius + float(clearance)
    return fixed_tip + direction * chosen_s, {
        "chosen_s": float(chosen_s),
        "seen_fixed_contact": bool(seen_fixed_contact),
        "max_s": float(max_s),
        "trace_head": trace[:8],
        "trace_tail": trace[-8:],
    }


def _apply_target_overrides(model: mujoco.MjModel, args: argparse.Namespace, target_body: str, target_geom: str) -> None:
    gid = _geom_id(model, target_geom)
    bid = _body_id(model, target_body)
    if str(args.object) == "cube" and float(args.cube_half_size) > 0.0:
        model.geom_size[gid, :3] = float(args.cube_half_size)
    if float(args.target_mass) > 0.0:
        model.body_mass[bid] = float(args.target_mass)


def _apply_soft_target(model: mujoco.MjModel, args: argparse.Namespace, target_geom: str) -> None:
    if not (bool(args.soft_sphere) or bool(args.soft_target)):
        return
    gid = _geom_id(model, target_geom)
    solref = np.asarray([float(x) for x in str(args.soft_solref).split(",")], dtype=np.float64)
    solimp = np.asarray([float(x) for x in str(args.soft_solimp).split(",")], dtype=np.float64)
    friction = np.asarray([float(x) for x in str(args.soft_friction).split(",")], dtype=np.float64)
    if solref.size != 2:
        raise ValueError("--soft-solref expects 2 values")
    if solimp.size == 3:
        solimp = np.asarray([solimp[0], solimp[1], solimp[2], 0.5, 2.0], dtype=np.float64)
    if solimp.size != 5:
        raise ValueError("--soft-solimp expects 3 or 5 values")
    if friction.size != 3:
        raise ValueError("--soft-friction expects 3 values")
    model.geom_solref[gid, :] = solref
    model.geom_solimp[gid, :] = solimp
    model.geom_friction[gid, :] = friction
    model.geom_condim[gid] = int(args.soft_condim)


def _apply_jaw_actuator_overrides(model: mujoco.MjModel, args: argparse.Namespace) -> dict:
    aid = _actuator_id(model, "Jaw")
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, "gripper_joint")
    if jid < 0:
        raise ValueError("joint not found: gripper_joint")
    dof = int(model.jnt_dofadr[int(jid)])
    before = {
        "forcerange": model.actuator_forcerange[aid].copy().tolist(),
        "gainprm": model.actuator_gainprm[aid].copy().tolist(),
        "biasprm": model.actuator_biasprm[aid].copy().tolist(),
        "dof_damping": float(model.dof_damping[dof]),
    }

    if float(args.jaw_force_range) > 0.0:
        lim = float(args.jaw_force_range)
        model.actuator_forcerange[aid, :] = np.asarray([-lim, lim], dtype=np.float64)

    if float(args.jaw_kp) > 0.0:
        kp = float(args.jaw_kp)
        old_kp = max(abs(float(before["gainprm"][0])), 1e-9)
        old_kv = abs(float(before["biasprm"][2]))
        old_ratio = old_kv / max(2.0 * np.sqrt(old_kp * max(float(model.dof_armature[dof]), 1e-9)), 1e-9)
        ratio = float(args.jaw_dampratio) if float(args.jaw_dampratio) > 0.0 else old_ratio
        kv = 2.0 * ratio * np.sqrt(kp * max(float(model.dof_armature[dof]), 1e-9))
        model.actuator_gainprm[aid, 0] = kp
        model.actuator_biasprm[aid, 1] = -kp
        model.actuator_biasprm[aid, 2] = -kv
    elif float(args.jaw_dampratio) > 0.0:
        kp = max(abs(float(model.actuator_gainprm[aid, 0])), 1e-9)
        kv = 2.0 * float(args.jaw_dampratio) * np.sqrt(kp * max(float(model.dof_armature[dof]), 1e-9))
        model.actuator_biasprm[aid, 2] = -kv

    if float(args.jaw_dof_damping) >= 0.0:
        model.dof_damping[dof] = float(args.jaw_dof_damping)

    return {
        "before": before,
        "after": {
            "forcerange": model.actuator_forcerange[aid].copy().tolist(),
            "gainprm": model.actuator_gainprm[aid].copy().tolist(),
            "biasprm": model.actuator_biasprm[aid].copy().tolist(),
            "dof_damping": float(model.dof_damping[dof]),
        },
    }


def _gripper_force(data: mujoco.MjData, ids) -> float:
    if not ids.act_ids:
        return 0.0
    return float(data.actuator_force[int(ids.act_ids[-1])])


def _phase_ctrl_q(
    args: argparse.Namespace,
    hold_q: np.ndarray,
    k: int,
    settle_steps: int,
    ramp_steps: int,
    rotate_steps: int,
) -> tuple[str, float]:
    if not bool(args.ramp_close):
        return "hold_closed", float(args.close_q)
    if k < settle_steps:
        return "settle_open", float(args.open_q)
    if k >= settle_steps + ramp_steps:
        return ("post_rotate" if rotate_steps > 0 else "hold_after_ramp"), float(hold_q[-1])
    if ramp_steps <= 1:
        return "ramp_close", float(args.close_q)
    alpha = min(1.0, max(0.0, (k - settle_steps) / float(ramp_steps - 1)))
    q = (1.0 - alpha) * float(args.open_q) + alpha * float(args.close_q)
    phase = "ramp_close" if alpha < 1.0 else "hold_after_ramp"
    return phase, float(q)


def run(args: argparse.Namespace) -> int:
    mjcf = Path(args.mjcf).expanduser().resolve()
    model = mujoco.MjModel.from_xml_path(str(mjcf))
    model.opt.timestep = float(SIM_DT)
    if bool(args.no_gravity):
        model.opt.gravity[:] = 0.0
    target_body, target_joint, target_geom = _target_names(str(args.object))
    _disable_unused_targets(model, target_geom)
    _apply_target_overrides(model, args, target_body, target_geom)
    _apply_soft_target(model, args, target_geom)
    jaw_params = _apply_jaw_actuator_overrides(model, args)
    data = mujoco.MjData(model)
    ids = resolve_robot_ids(model)

    reset_home(model, data, ids)
    q = joint_pos(data, ids)
    q_init = _parse_q(str(args.init_q), len(q))
    if q_init is not None:
        q = q_init
    q[-1] = float(args.open_q if bool(args.ramp_close) else args.close_q)
    _set_robot_q(model, data, ids, q)

    tcp_pos, tcp_quat = tcp_pose_w(data, ids)
    fixed_tip, moving_tip, pinch_center = _gripper_points_w(data, ids)
    fixed_site, moving_site = _finger_site_points_w(model, data)
    fixed_ref = fixed_site if fixed_site is not None else fixed_tip
    moving_ref = moving_site if moving_site is not None else moving_tip
    radius = _object_contact_radius(model, target_geom)
    placement_debug = {}
    place_mode = str(args.place_mode)
    if place_mode == "tcp":
        base_pos = tcp_pos
    elif place_mode == "pinch_center":
        base_pos = pinch_center
    elif place_mode == "fixed_tip":
        base_pos = fixed_tip
    elif place_mode == "moving_tip":
        base_pos = moving_tip
    elif place_mode == "fixed_finger_surface":
        fixed_to_moving = moving_ref - fixed_ref
        fixed_to_moving /= max(float(np.linalg.norm(fixed_to_moving)), 1e-12)
        base_pos = fixed_ref + fixed_to_moving * (radius + float(args.surface_clearance))
    elif place_mode == "fixed_finger_scan":
        base_pos, placement_debug = _find_fixed_finger_surface_center(
            model,
            data,
            fixed_tip=fixed_ref,
            moving_tip=moving_ref,
            radius=radius,
            clearance=float(args.surface_clearance),
            joint_name=target_joint,
            geom_name=target_geom,
        )
    else:
        raise ValueError(f"unknown --place-mode: {place_mode}")
    offset = np.asarray([float(x) for x in str(args.object_offset).split(",")], dtype=np.float64)
    if str(args.object_offset_frame) == "tcp":
        offset_w = _quat_to_mat(tcp_quat) @ offset
    elif str(args.object_offset_frame) == "world":
        offset_w = offset
    else:
        raise ValueError(f"unknown --object-offset-frame: {args.object_offset_frame}")
    sphere_pos = base_pos + offset_w
    _set_free_body_pose(model, data, joint_name=target_joint, pos=sphere_pos)
    if target_joint != "target_sphere_freejoint":
        _set_free_body_pose(model, data, joint_name="target_sphere_freejoint", pos=np.asarray([0.2, 0.0, -1.0]))
    if target_joint != "target_object_freejoint":
        _set_free_body_pose(model, data, joint_name="target_object_freejoint", pos=np.asarray([0.2, 0.0, -1.0]))
    _set_free_body_pose(model, data, joint_name="target_bottle_freejoint", pos=np.asarray([0.2, 0.0, -1.0]))
    mujoco.mj_forward(model, data)

    hold_q = q.copy()
    set_ctrl(data, ids, hold_q)
    start_pos = np.asarray(data.xpos[_body_id(model, target_body)], dtype=np.float64).copy()
    start_tcp = tcp_pos.copy()
    initial_tip_gap = float(np.linalg.norm(fixed_tip - moving_tip))

    viewer = None
    if bool(args.view):
        if mujoco_viewer is None:
            raise RuntimeError("mujoco.viewer is unavailable")
        viewer = mujoco_viewer.launch_passive(model, data)

    settle_steps = max(0, int(args.settle_steps if int(args.settle_steps) >= 0 else round(float(args.settle_s) / float(SIM_DT))))
    ramp_steps = max(1, int(round(float(args.close_time) / float(SIM_DT))))
    rotate_steps = max(0, int(round(float(args.rotate_time) / float(SIM_DT))))
    hold_steps = max(1, int(round(float(args.duration) / float(SIM_DT))))
    steps = settle_steps + ramp_steps + rotate_steps + hold_steps if bool(args.ramp_close) else hold_steps
    max_drop = 0.0
    max_sep = 0.0
    min_contacts = 10**9
    max_abs_gripper_force = 0.0
    force_stop_step = -1
    force_stop_ctrl = float("nan")
    wrist_roll_start = float(hold_q[5]) if len(hold_q) > 5 else 0.0
    last_pairs: list[tuple[str, str]] = []
    log_rows = []
    for k in range(steps):
        phase, desired_gripper_q = _phase_ctrl_q(args, hold_q, k, settle_steps, ramp_steps, rotate_steps)
        if force_stop_step < 0:
            hold_q[-1] = desired_gripper_q
        if bool(args.ramp_close) and rotate_steps > 0 and k >= settle_steps + ramp_steps:
            rotate_k = min(rotate_steps, k - settle_steps - ramp_steps + 1)
            alpha_rot = rotate_k / float(max(rotate_steps, 1))
            hold_q[5] = wrist_roll_start + alpha_rot * float(args.rotate_angle)
        set_ctrl(data, ids, hold_q)
        freeze_now = bool(args.freeze_object) or (bool(args.freeze_during_settle) and k < settle_steps)
        if freeze_now:
            _set_free_body_pose(model, data, joint_name=target_joint, pos=start_pos)
            mujoco.mj_forward(model, data)
        mujoco.mj_step(model, data)
        gripper_force = _gripper_force(data, ids)
        max_abs_gripper_force = max(max_abs_gripper_force, abs(gripper_force))
        if (
            bool(args.ramp_close)
            and force_stop_step < 0
            and float(args.force_stop) > 0.0
            and abs(gripper_force) >= float(args.force_stop)
        ):
            force_stop_step = int(k)
            force_stop_ctrl = float(hold_q[-1])
        obj_pos = np.asarray(data.xpos[_body_id(model, target_body)], dtype=np.float64).copy()
        tcp_now, _ = tcp_pose_w(data, ids)
        fixed_now, moving_now, pinch_now = _gripper_points_w(data, ids)
        contacts, pairs = _count_geom_contacts(model, data, target_geom)
        last_pairs = pairs
        drop = float(start_pos[2] - obj_pos[2])
        sep = float(np.linalg.norm(obj_pos - tcp_now))
        max_drop = max(max_drop, drop)
        max_sep = max(max_sep, sep)
        min_contacts = min(min_contacts, contacts)
        if args.log:
            log_rows.append(
                {
                    "step": int(k),
                    "t_s": float(k * SIM_DT),
                    "phase": phase,
                    "freeze_object": bool(freeze_now),
                    "gripper_ctrl": float(hold_q[-1]),
                    "gripper_q": float(joint_pos(data, ids)[-1]),
                    "wrist_roll_ctrl": float(hold_q[5]),
                    "wrist_roll_q": float(joint_pos(data, ids)[5]),
                    "gripper_force": gripper_force,
                    "object_pos": obj_pos.tolist(),
                    "tcp_pos": tcp_now.tolist(),
                    "pinch_center": pinch_now.tolist(),
                    "tip_gap_m": float(np.linalg.norm(fixed_now - moving_now)),
                    "drop_m": drop,
                    "sep_m": sep,
                    "contacts": int(contacts),
                    "pairs": pairs[:8],
                }
            )
        if viewer is not None:
            viewer.sync()
            time.sleep(float(SIM_DT) / max(float(args.speed), 1e-3))
            if not viewer.is_running():
                break

    end_pos = np.asarray(data.xpos[_body_id(model, target_body)], dtype=np.float64).copy()
    end_tcp, _ = tcp_pose_w(data, ids)
    end_fixed, end_moving, end_pinch = _gripper_points_w(data, ids)
    end_sep = float(np.linalg.norm(end_pos - end_tcp))
    end_drop = float(start_pos[2] - end_pos[2])
    contacts, pairs = _count_geom_contacts(model, data, target_geom)
    held = bool(end_drop <= float(args.max_drop) and end_sep <= float(args.max_sep) and contacts > 0)

    result = {
        "held": held,
        "duration_s": float(args.duration),
        "close_q": float(args.close_q),
        "open_q": float(args.open_q),
        "ramp_close": bool(args.ramp_close),
        "settle_steps": int(settle_steps),
        "close_time_s": float(args.close_time),
        "rotate_angle_rad": float(args.rotate_angle),
        "rotate_time_s": float(args.rotate_time),
        "force_stop": float(args.force_stop),
        "jaw_actuator": jaw_params,
        "force_stop_step": int(force_stop_step),
        "force_stop_ctrl": force_stop_ctrl,
        "max_abs_gripper_force": max_abs_gripper_force,
        "end_gripper_q": float(joint_pos(data, ids)[-1]),
        "end_gripper_ctrl": float(hold_q[-1]),
        "end_wrist_roll_q": float(joint_pos(data, ids)[5]),
        "end_wrist_roll_ctrl": float(hold_q[5]),
        "no_gravity": bool(args.no_gravity),
        "freeze_object": bool(args.freeze_object),
        "freeze_during_settle": bool(args.freeze_during_settle),
        "place_mode": place_mode,
        "placement_debug": placement_debug,
        "object": str(args.object),
        "target_body": target_body,
        "target_geom": target_geom,
        "object_offset": offset.tolist(),
        "object_offset_frame": str(args.object_offset_frame),
        "object_offset_world": offset_w.tolist(),
        "object_contact_radius_m": radius,
        "object_contact_diameter_m": 2.0 * radius,
        "target_mass": float(model.body_mass[_body_id(model, target_body)]),
        "target_geom_size": model.geom_size[_geom_id(model, target_geom)].tolist(),
        "fixed_finger_inner_site_pos": fixed_site.tolist() if fixed_site is not None else None,
        "moving_finger_inner_site_pos": moving_site.tolist() if moving_site is not None else None,
        "soft_target": bool(args.soft_target or args.soft_sphere),
        "target_solref": model.geom_solref[_geom_id(model, target_geom)].tolist(),
        "target_solimp": model.geom_solimp[_geom_id(model, target_geom)].tolist(),
        "target_friction": model.geom_friction[_geom_id(model, target_geom)].tolist(),
        "target_condim": int(model.geom_condim[_geom_id(model, target_geom)]),
        "initial_tip_gap_m": initial_tip_gap,
        "end_tip_gap_m": float(np.linalg.norm(end_fixed - end_moving)),
        "start_fixed_tip_pos": fixed_tip.tolist(),
        "start_moving_tip_pos": moving_tip.tolist(),
        "start_pinch_center": pinch_center.tolist(),
        "end_pinch_center": end_pinch.tolist(),
        "start_object_pos": start_pos.tolist(),
        "end_object_pos": end_pos.tolist(),
        "start_tcp_pos": start_tcp.tolist(),
        "end_tcp_pos": end_tcp.tolist(),
        "end_drop_m": end_drop,
        "max_drop_m": max_drop,
        "end_sep_m": end_sep,
        "max_sep_m": max_sep,
        "min_contacts": int(min_contacts if min_contacts < 10**9 else 0),
        "end_contacts": int(contacts),
        "end_pairs": pairs[:8],
        "last_pairs": last_pairs[:8],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.log:
        out = Path(args.log).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            for row in log_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"[grasp_hold_smoke] log -> {out.resolve()}")

    if viewer is not None:
        viewer.close()
    return 0 if held else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF_NOROD))
    p.add_argument("--duration", type=float, default=3.0)
    p.add_argument("--close-q", type=float, default=-0.2)
    p.add_argument("--open-q", type=float, default=1.2)
    p.add_argument("--ramp-close", action="store_true", help="Start open, settle object, then close gripper slowly.")
    p.add_argument("--settle-s", type=float, default=1.0, help="Open-gripper settling time before ramp close.")
    p.add_argument("--settle-steps", type=int, default=-1, help="Override --settle-s with an exact simulation-step count.")
    p.add_argument("--close-time", type=float, default=0.6, help="Seconds used to ramp from --open-q to --close-q.")
    p.add_argument("--force-stop", type=float, default=12.0, help="Stop increasing close command when |gripper actuator force| reaches this; <=0 disables.")
    p.add_argument("--jaw-force-range", type=float, default=-1.0, help="Runtime Jaw actuator force limit; <=0 keeps MJCF default.")
    p.add_argument("--jaw-kp", type=float, default=-1.0, help="Runtime Jaw position actuator kp; <=0 keeps MJCF default.")
    p.add_argument("--jaw-dampratio", type=float, default=-1.0, help="Runtime Jaw dampratio approximation; <=0 keeps current compiled value.")
    p.add_argument("--jaw-dof-damping", type=float, default=-1.0, help="Runtime gripper dof damping; <0 keeps MJCF default.")
    p.add_argument("--rotate-angle", type=float, default=0.0, help="Post-close wrist_roll rotation angle in radians.")
    p.add_argument("--rotate-time", type=float, default=0.0, help="Seconds used for post-close wrist_roll rotation.")
    p.add_argument("--init-q", type=str, default="", help=f"Optional {len(REACH_JOINT_NAMES)}-DoF robot q, comma separated.")
    p.add_argument("--object", choices=("sphere", "cube"), default="sphere", help="Object used for the hold smoke test.")
    p.add_argument("--cube-half-size", type=float, default=0.014, help="Runtime cube half size in meters; <=0 keeps MJCF size.")
    p.add_argument("--target-mass", type=float, default=0.030, help="Runtime target body mass in kg; <=0 keeps MJCF mass.")
    p.add_argument("--object-offset", type=str, default="0,0,0", help="Offset added before placing sphere.")
    p.add_argument("--object-offset-frame", choices=("world", "tcp"), default="world")
    p.add_argument(
        "--place-mode",
        choices=("tcp", "pinch_center", "fixed_tip", "moving_tip", "fixed_finger_surface", "fixed_finger_scan"),
        default="pinch_center",
        help="Reference point used before --object-offset is applied.",
    )
    p.add_argument("--surface-clearance", type=float, default=0.001, help="Extra clearance for fixed_finger_surface placement.")
    p.add_argument("--max-drop", type=float, default=0.010, help="Held if final z drop is below this value.")
    p.add_argument("--max-sep", type=float, default=0.050, help="Held if final object-TCP distance is below this value.")
    p.add_argument("--log", type=str, default="")
    p.add_argument("--view", action="store_true")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--no-gravity", action="store_true", help="Set global gravity to zero for visual/contact inspection.")
    p.add_argument("--freeze-object", action="store_true", help="Keep the sphere at its initial pose every sim step.")
    p.add_argument("--freeze-during-settle", action="store_true", help="Keep sphere fixed only before ramp closing starts.")
    p.add_argument("--soft-target", action="store_true", help="Runtime-only softer/high-friction contact for selected target.")
    p.add_argument("--soft-sphere", action="store_true", help="Backward-compatible alias for --soft-target.")
    p.add_argument("--soft-solref", type=str, default="0.08,1", help="solref for --soft-target, format: timeconst,damping.")
    p.add_argument("--soft-solimp", type=str, default="0.75,0.95,0.02", help="solimp for --soft-target, format: d0,dwidth,width.")
    p.add_argument("--soft-friction", type=str, default="3.0,0.05,0.005", help="friction for --soft-target.")
    p.add_argument("--soft-condim", type=int, default=4, help="condim for --soft-target.")
    return p


if __name__ == "__main__":
    raise SystemExit(run(build_parser().parse_args()))
