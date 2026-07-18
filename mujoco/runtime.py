"""MuJoCo Reach 运行时：TCP、obs、动作滤波与位置控制。"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np

try:
    from .constants import (
        ACTION_DIM,
        ACTION_FILTER_TAU,
        ACTION_SCALE,
        BASE_BODY,
        CBF_FILTER_TAU,
        DECIMATION,
        GRIPPER_BODY,
        HOME_QPOS,
        REACH_JOINT_NAMES,
        SIM_DT,
        WRIST_ROLL_BODY,
    )
except ImportError:
    from constants import (  # type: ignore
        ACTION_DIM,
        ACTION_FILTER_TAU,
        ACTION_SCALE,
        BASE_BODY,
        CBF_FILTER_TAU,
        DECIMATION,
        GRIPPER_BODY,
        HOME_QPOS,
        REACH_JOINT_NAMES,
        SIM_DT,
        WRIST_ROLL_BODY,
    )

_RL_ROOT = Path(__file__).resolve().parent.parent / "rl"
if str(_RL_ROOT) not in sys.path:
    sys.path.insert(0, str(_RL_ROOT))

from sample.tcp_pose import compute_pinch_tcp_pose_numpy  # noqa: E402


def _body_id(model: mujoco.MjModel, name: str) -> int:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
    if bid < 0:
        raise ValueError(f"body not found: {name}")
    return bid


def _joint_id(model: mujoco.MjModel, name: str) -> int:
    jid = int(mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name))
    if jid < 0:
        raise ValueError(f"joint not found: {name}")
    return jid


def quat_conjugate(q: np.ndarray) -> np.ndarray:
    return np.asarray([q[0], -q[1], -q[2], -q[3]], dtype=np.float64)


def quat_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.asarray(
        [
            aw * bw - ax * bx - ay * by - az * bz,
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
        ],
        dtype=np.float64,
    )


@dataclass
class RobotIds:
    joint_ids: list
    qpos_adr: list
    dof_adr: list
    act_ids: list
    base_body: int
    wrist_roll_body: int
    gripper_body: int
    q_low: np.ndarray
    q_high: np.ndarray
    tcp_offset_local: np.ndarray = field(
        default_factory=lambda: np.zeros(3, dtype=np.float64)
    )


def resolve_robot_ids(model: mujoco.MjModel) -> RobotIds:
    joint_ids = [_joint_id(model, n) for n in REACH_JOINT_NAMES]
    qpos_adr = [int(model.jnt_qposadr[j]) for j in joint_ids]
    dof_adr = [int(model.jnt_dofadr[j]) for j in joint_ids]
    act_ids = list(range(min(ACTION_DIM, model.nu)))
    jlow = np.zeros(ACTION_DIM, dtype=np.float64)
    jhigh = np.zeros(ACTION_DIM, dtype=np.float64)
    for i, jid in enumerate(joint_ids):
        lo, hi = model.jnt_range[jid]
        if abs(float(hi) - float(lo)) < 1e-12:
            lo, hi = -np.pi, np.pi
        jlow[i] = float(lo)
        jhigh[i] = float(hi)
    return RobotIds(
        joint_ids=joint_ids,
        qpos_adr=qpos_adr,
        dof_adr=dof_adr,
        act_ids=act_ids,
        base_body=_body_id(model, BASE_BODY),
        wrist_roll_body=_body_id(model, WRIST_ROLL_BODY),
        gripper_body=_body_id(model, GRIPPER_BODY),
        q_low=jlow,
        q_high=jhigh,
    )


def joint_pos(data: mujoco.MjData, ids: RobotIds) -> np.ndarray:
    return np.asarray([data.qpos[a] for a in ids.qpos_adr], dtype=np.float64)


def joint_vel(data: mujoco.MjData, ids: RobotIds) -> np.ndarray:
    return np.asarray([data.qvel[a] for a in ids.dof_adr], dtype=np.float64)


def tcp_pose_w(data: mujoco.MjData, ids: RobotIds):
    wr_pos = np.asarray(data.xpos[ids.wrist_roll_body], dtype=np.float64).copy()
    wr_quat = np.asarray(data.xquat[ids.wrist_roll_body], dtype=np.float64).copy()
    gr_pos = np.asarray(data.xpos[ids.gripper_body], dtype=np.float64).copy()
    gr_quat = np.asarray(data.xquat[ids.gripper_body], dtype=np.float64).copy()
    tcp_pos, tcp_quat = compute_pinch_tcp_pose_numpy(wr_pos, wr_quat, gr_pos, gr_quat)
    offset = np.asarray(getattr(ids, "tcp_offset_local", np.zeros(3)), dtype=np.float64).reshape(3)
    if float(np.linalg.norm(offset)) > 1e-12:
        rot = np.zeros(9, dtype=np.float64)
        mujoco.mju_quat2Mat(rot, np.asarray(tcp_quat, dtype=np.float64))
        tcp_pos = np.asarray(tcp_pos, dtype=np.float64).reshape(3) + rot.reshape(3, 3) @ offset
    return tcp_pos, tcp_quat


def make_obs(data: mujoco.MjData, ids: RobotIds, target_pos_w, target_quat_wxyz):
    q = joint_pos(data, ids)
    qd = joint_vel(data, ids)
    root = np.asarray(data.xpos[ids.base_body], dtype=np.float64)
    tcp_w, ee_quat = tcp_pose_w(data, ids)
    tcp_rel = tcp_w - root
    target = np.asarray(target_pos_w, dtype=np.float64).reshape(3)
    target_rel = target - root
    pos_err = target - tcp_w

    ee_u = ee_quat / max(float(np.linalg.norm(ee_quat)), 1e-12)
    dq = np.asarray(target_quat_wxyz, dtype=np.float64).reshape(4)
    dq = dq / max(float(np.linalg.norm(dq)), 1e-12)
    quat_err = quat_multiply(dq, quat_conjugate(ee_u))
    quat_err = quat_err / max(float(np.linalg.norm(quat_err)), 1e-12)
    if quat_err[0] < 0.0:
        quat_err = -quat_err

    obs = np.concatenate([q, qd, tcp_rel, target_rel, pos_err, quat_err]).astype(np.float32)
    info = {
        "distance": float(np.linalg.norm(pos_err)),
        "quat_dot": float(abs(np.dot(ee_u, dq))),
    }
    return obs, info


@dataclass
class ReachStepper:
    policy: object
    ids: RobotIds
    model: mujoco.MjModel | None = None
    action_scale: float = ACTION_SCALE
    filter_tau: float = ACTION_FILTER_TAU
    sim_dt: float = SIM_DT
    decimation: int = DECIMATION
    enable_cbf: bool = False
    cbf_cfg: object | None = None
    cbf_monitors: list | None = None
    cbf_obstacles: list | None = None
    cbf_obstacle_source: object | None = None
    cbf_filter_tau: float = CBF_FILTER_TAU
    filtered_action: np.ndarray = field(
        default_factory=lambda: np.zeros(ACTION_DIM, dtype=np.float64)
    )
    filtered_dq_cbf: np.ndarray = field(
        default_factory=lambda: np.zeros(ACTION_DIM, dtype=np.float64)
    )

    def __post_init__(self) -> None:
        dt_ctrl = self.sim_dt * self.decimation
        tau = max(float(self.filter_tau), 1e-6)
        self.beta = float(dt_ctrl / (tau + dt_ctrl))
        cbf_tau = max(float(self.cbf_filter_tau), 1e-6)
        self.cbf_beta = float(dt_ctrl / (cbf_tau + dt_ctrl))
        if self.enable_cbf and self.cbf_cfg is not None:
            try:
                from .cbf import resolve_monitors
            except ImportError:
                from cbf import resolve_monitors  # type: ignore
            if self.model is None:
                raise ValueError("enable_cbf=True 需要传入 model")
            if self.cbf_monitors is None:
                self.cbf_monitors = resolve_monitors(
                    self.model,
                    self.cbf_cfg.monitor_specs,
                    self.cbf_cfg.capsule_specs,
                )

    def reset_filter(self) -> None:
        self.filtered_action[:] = 0.0
        self.filtered_dq_cbf[:] = 0.0
        if self.cbf_obstacle_source is not None:
            self.cbf_obstacle_source.reset()

    def refresh_cbf_obstacles(self, data: mujoco.MjData) -> None:
        if not self.enable_cbf or self.cbf_cfg is None or self.model is None:
            return
        if self.cbf_obstacle_source is not None:
            self.cbf_obstacle_source.update(self.model, data)
            self.cbf_obstacles = self.cbf_obstacle_source.get_obstacles()
            return
        try:
            from .cbf import load_obstacles
        except ImportError:
            from cbf import load_obstacles  # type: ignore
        self.cbf_obstacles = load_obstacles(
            self.model, data, self.cbf_cfg.obstacle_geom_names
        )

    def compute_targets(self, model: mujoco.MjModel, data: mujoco.MjData, target_pos_w, target_quat_w):
        obs, info = make_obs(data, self.ids, target_pos_w, target_quat_w)
        raw = np.clip(self.policy.act_mean(obs).astype(np.float64), -1.0, 1.0)
        self.filtered_action += self.beta * (raw - self.filtered_action)
        curr_q = joint_pos(data, self.ids)
        dq_nom = self.action_scale * self.filtered_action
        dq_cbf = np.zeros(ACTION_DIM, dtype=np.float64)
        cbf_info: dict = {}
        if self.enable_cbf and self.cbf_cfg is not None and self.cbf_monitors is not None:
            if (
                self.cbf_obstacle_source is not None
                and getattr(self.cbf_obstacle_source, "refresh_every_step", False)
            ):
                self.refresh_cbf_obstacles(data)
            elif self.cbf_obstacles is None:
                self.refresh_cbf_obstacles(data)
            try:
                from .cbf import solve_cbf_correction
            except ImportError:
                from cbf import solve_cbf_correction  # type: ignore
            dq_cbf_raw, cbf_info = solve_cbf_correction(
                model,
                data,
                self.ids,
                dq_nom,
                self.cbf_cfg,
                self.cbf_monitors,
                self.cbf_obstacles or [],
                tcp_pose_w,
            )
            self.filtered_dq_cbf += self.cbf_beta * (dq_cbf_raw - self.filtered_dq_cbf)
            dq_cbf = self.filtered_dq_cbf.copy()
            cbf_info["dq_cbf_raw_norm"] = float(np.linalg.norm(dq_cbf_raw))
            cbf_info["dq_cbf_norm"] = float(np.linalg.norm(dq_cbf))
        dq_total = dq_nom + dq_cbf
        dq_total = np.clip(dq_total, -self.action_scale, self.action_scale)
        tgt = curr_q + dq_total
        tgt = np.clip(tgt, self.ids.q_low, self.ids.q_high)
        if not cbf_info:
            cbf_info = {}
        cbf_info.setdefault("dq_nom_norm", float(np.linalg.norm(dq_nom)))
        cbf_info.setdefault("dq_total_norm", float(np.linalg.norm(dq_total)))
        return tgt, {
            "obs": obs,
            "raw_action": raw,
            "dq_nom": dq_nom,
            "dq_cbf": dq_cbf,
            **cbf_info,
            **info,
        }


def set_ctrl(data: mujoco.MjData, ids: RobotIds, q_tgt: np.ndarray) -> None:
    for i, aid in enumerate(ids.act_ids):
        data.ctrl[aid] = float(q_tgt[i])


def cartesian_position_servo_target(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids: RobotIds,
    target_pos_w: np.ndarray,
    *,
    max_step: float,
    damping: float = 1e-3,
) -> tuple[np.ndarray, dict]:
    """One-step damped least-squares TCP position servo.

    This intentionally controls only position. Orientation is held indirectly by
    the current joint posture, which is enough for the first static sphere
    pregrasp/final-approach smoke test.
    """
    curr_q = joint_pos(data, ids)
    tcp_w, ee_quat = tcp_pose_w(data, ids)
    err = np.asarray(target_pos_w, dtype=np.float64).reshape(3) - tcp_w
    dist = float(np.linalg.norm(err))
    if dist <= 1e-9:
        return curr_q.copy(), {
            "distance": 0.0,
            "quat_dot": 1.0,
            "dq_nom": np.zeros(ACTION_DIM, dtype=np.float64),
            "dq_cbf": np.zeros(ACTION_DIM, dtype=np.float64),
            "raw_action": np.zeros(ACTION_DIM, dtype=np.float64),
            "h_min": float("inf"),
            "cbf_active": False,
            "cbf_feasible": True,
            "cbf_projected": False,
            "n_constraints": 0,
            "dq_nom_norm": 0.0,
            "dq_total_norm": 0.0,
            "dq_cbf_norm": 0.0,
        }

    step = err
    max_step = max(float(max_step), 1e-6)
    if dist > max_step:
        step = err * (max_step / dist)

    n_arm = max(ACTION_DIM - 1, 1)
    j_arm = np.zeros((3, n_arm), dtype=np.float64)
    eps = 1e-5
    q_saved = data.qpos.copy()
    qvel_saved = data.qvel.copy()
    for i, qadr in enumerate(ids.qpos_adr[:n_arm]):
        data.qpos[qadr] = q_saved[qadr] + eps
        mujoco.mj_forward(model, data)
        tcp_plus, _ = tcp_pose_w(data, ids)
        data.qpos[qadr] = q_saved[qadr] - eps
        mujoco.mj_forward(model, data)
        tcp_minus, _ = tcp_pose_w(data, ids)
        j_arm[:, i] = (tcp_plus - tcp_minus) / (2.0 * eps)
        data.qpos[qadr] = q_saved[qadr]
    data.qpos[:] = q_saved
    data.qvel[:] = qvel_saved
    mujoco.mj_forward(model, data)
    lhs = j_arm @ j_arm.T + float(damping) * np.eye(3, dtype=np.float64)
    dq_arm = j_arm.T @ np.linalg.solve(lhs, step)
    dq_arm = np.clip(dq_arm, -max_step, max_step)
    dq = np.zeros(ACTION_DIM, dtype=np.float64)
    dq[:n_arm] = dq_arm
    tgt = np.clip(curr_q + dq, ids.q_low, ids.q_high)
    return tgt, {
        "distance": dist,
        "quat_dot": 1.0,
        "dq_nom": dq.copy(),
        "dq_cbf": np.zeros(ACTION_DIM, dtype=np.float64),
        "raw_action": np.zeros(ACTION_DIM, dtype=np.float64),
        "h_min": float("inf"),
        "cbf_active": False,
        "cbf_feasible": True,
        "cbf_projected": False,
        "n_constraints": 0,
        "dq_nom_norm": float(np.linalg.norm(dq)),
        "dq_total_norm": float(np.linalg.norm(tgt - curr_q)),
        "dq_cbf_norm": 0.0,
    }


def _quat_to_rotvec(q_wxyz: np.ndarray) -> np.ndarray:
    q = np.asarray(q_wxyz, dtype=np.float64).reshape(4)
    q = q / max(float(np.linalg.norm(q)), 1e-12)
    if q[0] < 0.0:
        q = -q
    v = q[1:]
    s = float(np.linalg.norm(v))
    if s < 1e-10:
        return 2.0 * v
    angle = 2.0 * np.arctan2(s, float(q[0]))
    return v * (angle / s)


def cartesian_pose_servo_target(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids: RobotIds,
    target_pos_w: np.ndarray,
    target_quat_wxyz: np.ndarray,
    *,
    max_pos_step: float,
    max_rot_step: float = 0.02,
    rot_weight: float = 0.35,
    damping: float = 2e-3,
) -> tuple[np.ndarray, dict]:
    """One-step damped least-squares TCP pose servo for arm joints.

    The gripper joint is intentionally excluded from the Jacobian because grasp
    phases command it separately as open/close.
    """
    curr_q = joint_pos(data, ids)
    tcp_w, ee_quat = tcp_pose_w(data, ids)
    pos_err = np.asarray(target_pos_w, dtype=np.float64).reshape(3) - tcp_w
    pos_dist = float(np.linalg.norm(pos_err))
    pos_step = pos_err.copy()
    max_pos_step = max(float(max_pos_step), 1e-6)
    if pos_dist > max_pos_step:
        pos_step = pos_err * (max_pos_step / pos_dist)

    target_q = np.asarray(target_quat_wxyz, dtype=np.float64).reshape(4)
    target_q = target_q / max(float(np.linalg.norm(target_q)), 1e-12)
    ee_q = np.asarray(ee_quat, dtype=np.float64).reshape(4)
    ee_q = ee_q / max(float(np.linalg.norm(ee_q)), 1e-12)
    q_err = quat_multiply(target_q, quat_conjugate(ee_q))
    rot_err = _quat_to_rotvec(q_err)
    rot_norm = float(np.linalg.norm(rot_err))
    rot_step = rot_err.copy()
    max_rot_step = max(float(max_rot_step), 1e-6)
    if rot_norm > max_rot_step:
        rot_step = rot_err * (max_rot_step / rot_norm)

    n_arm = max(ACTION_DIM - 1, 1)
    j = np.zeros((6, n_arm), dtype=np.float64)
    eps = 1e-5
    q_saved = data.qpos.copy()
    qvel_saved = data.qvel.copy()
    for i, qadr in enumerate(ids.qpos_adr[:n_arm]):
        data.qpos[qadr] = q_saved[qadr] + eps
        mujoco.mj_forward(model, data)
        tcp_plus, quat_plus = tcp_pose_w(data, ids)

        data.qpos[qadr] = q_saved[qadr] - eps
        mujoco.mj_forward(model, data)
        tcp_minus, quat_minus = tcp_pose_w(data, ids)

        j[:3, i] = (tcp_plus - tcp_minus) / (2.0 * eps)
        q_delta = quat_multiply(quat_plus, quat_conjugate(quat_minus))
        j[3:, i] = _quat_to_rotvec(q_delta) / (2.0 * eps)
        data.qpos[qadr] = q_saved[qadr]

    data.qpos[:] = q_saved
    data.qvel[:] = qvel_saved
    mujoco.mj_forward(model, data)

    err6 = np.concatenate([pos_step, float(rot_weight) * rot_step])
    j6 = j.copy()
    j6[3:, :] *= float(rot_weight)
    lhs = j6 @ j6.T + float(damping) * np.eye(6, dtype=np.float64)
    dq_arm = j6.T @ np.linalg.solve(lhs, err6)
    max_joint_step = max(float(max_pos_step), float(max_rot_step) * 0.5)
    dq_arm = np.clip(dq_arm, -max_joint_step, max_joint_step)
    dq = np.zeros(ACTION_DIM, dtype=np.float64)
    dq[:n_arm] = dq_arm
    tgt = np.clip(curr_q + dq, ids.q_low, ids.q_high)
    return tgt, {
        "distance": pos_dist,
        "quat_dot": float(abs(np.dot(ee_q, target_q))),
        "dq_nom": dq.copy(),
        "dq_cbf": np.zeros(ACTION_DIM, dtype=np.float64),
        "raw_action": np.zeros(ACTION_DIM, dtype=np.float64),
        "h_min": float("inf"),
        "cbf_active": False,
        "cbf_feasible": True,
        "cbf_projected": False,
        "n_constraints": 0,
        "dq_nom_norm": float(np.linalg.norm(dq)),
        "dq_total_norm": float(np.linalg.norm(tgt - curr_q)),
        "dq_cbf_norm": 0.0,
        "rot_err_norm": rot_norm,
    }


def reset_obstacle_rod(model: mujoco.MjModel, data: mujoco.MjData) -> None:
    """每局将可碰倒细杆复位为直立（无该关节时静默跳过）。"""
    try:
        from .constants import OBSTACLE_ROD_JOINT, OBSTACLE_ROD_MOUNT_POS_M
    except ImportError:
        from constants import OBSTACLE_ROD_JOINT, OBSTACLE_ROD_MOUNT_POS_M  # type: ignore

    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, OBSTACLE_ROD_JOINT)
    if jid < 0:
        return
    qadr = int(model.jnt_qposadr[jid])
    vadr = int(model.jnt_dofadr[jid])
    jtype = int(model.jnt_type[jid])
    if jtype == int(mujoco.mjtJoint.mjJNT_BALL):
        data.qpos[qadr : qadr + 4] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        data.qvel[vadr : vadr + 3] = 0.0
    elif jtype == int(mujoco.mjtJoint.mjJNT_FREE):
        mount = np.asarray(OBSTACLE_ROD_MOUNT_POS_M, dtype=np.float64)
        data.qpos[qadr : qadr + 3] = mount
        data.qpos[qadr + 3 : qadr + 7] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        data.qvel[vadr : vadr + 6] = 0.0


def reset_home(model: mujoco.MjModel, data: mujoco.MjData, ids: RobotIds) -> None:
    home = np.asarray(HOME_QPOS, dtype=np.float64)
    for i, adr in enumerate(ids.qpos_adr):
        data.qpos[adr] = home[i]
    reset_obstacle_rod(model, data)
    data.qvel[:] = 0.0
    set_ctrl(data, ids, home)
    mujoco.mj_forward(model, data)


def load_target_bank(npz_path):
    z = np.load(str(npz_path))
    if "tcp_pos" in z.files:
        pos = np.asarray(z["tcp_pos"], dtype=np.float64)
    else:
        pos = np.asarray(z["tcp"], dtype=np.float64)
    if "tcp_quat_wxyz" in z.files:
        quat = np.asarray(z["tcp_quat_wxyz"], dtype=np.float64)
    else:
        quat = np.tile(np.array([1.0, 0.0, 0.0, 0.0]), (pos.shape[0], 1))
    return pos, quat
