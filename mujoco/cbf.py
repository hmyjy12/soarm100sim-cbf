"""EMBODISTEER 式全身 CBF-QP：在名义关节增量上求最小安全修正。

不可行时策略 A：Δq_cbf = 0，仍执行 PPO 名义 Δq_nom。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import mujoco
import numpy as np

try:
    from scipy.optimize import minimize

    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False


def _project_box(x: np.ndarray, lb: np.ndarray, ub: np.ndarray) -> np.ndarray:
    return np.clip(x, lb, ub)


def _find_feasible_point(
    a_ineq: np.ndarray,
    b_ineq: np.ndarray,
    lb: np.ndarray,
    ub: np.ndarray,
    max_iter: int = 200,
) -> tuple[np.ndarray | None, bool]:
    """找满足 A x >= b 且 box 内的可行点。"""
    n = lb.shape[0]
    x = _project_box(np.zeros(n, dtype=np.float64), lb, ub)
    if a_ineq.shape[0] == 0:
        return x, True
    for _ in range(max_iter):
        viol = b_ineq - a_ineq @ x
        worst = float(np.max(viol))
        if worst <= 1e-7:
            return x, True
        i = int(np.argmax(viol))
        ai = a_ineq[i]
        denom = float(ai @ ai) + 1e-12
        x = x + ((worst + 1e-5) / denom) * ai
        x = _project_box(x, lb, ub)
    return None, False


def _solve_qp_projected_gradient(
    h_mat: np.ndarray,
    a_ineq: np.ndarray,
    b_ineq: np.ndarray,
    lb: np.ndarray,
    ub: np.ndarray,
    max_iter: int = 300,
) -> tuple[np.ndarray | None, bool]:
    """min ½ xᵀ H x  s.t. A x >= b, box。纯 numpy，无 scipy 依赖。"""
    n = lb.shape[0]
    if a_ineq.shape[0] == 0:
        return np.zeros(n, dtype=np.float64), True

    x, ok = _find_feasible_point(a_ineq, b_ineq, lb, ub)
    if not ok or x is None:
        return None, False

    for _ in range(max_iter):
        grad = h_mat @ x
        if float(np.linalg.norm(grad)) < 1e-7 and np.all(a_ineq @ x >= b_ineq - 1e-7):
            return x, True
        alpha = 1.0
        improved = False
        for _ls in range(24):
            x_try = _project_box(x - alpha * grad, lb, ub)
            if np.all(a_ineq @ x_try >= b_ineq - 1e-7):
                if float(x_try @ h_mat @ x_try) <= float(x @ h_mat @ x) + 1e-10:
                    x = x_try
                    improved = True
                    break
            alpha *= 0.5
        if not improved:
            break

    if np.all(a_ineq @ x >= b_ineq - 1e-6):
        return x, True
    return None, False

try:
    from .constants import ACTION_DIM, ACTION_SCALE
except ImportError:
    from constants import ACTION_DIM, ACTION_SCALE  # type: ignore


DEFAULT_MONITOR_SPECS: tuple[tuple[str, float], ...] = (
    ("shoulder_pitch", 0.02),
    ("ellbow", 0.03),
    ("wrist_pitch", 0.02),
    ("wrist_roll", 0.02),
    ("gripper", 0.02),
    ("tcp", 0.01),
)

DEFAULT_OBSTACLE_GEOM_NAMES: tuple[str, ...] = ("obstacle_rod",)


@dataclass
class AxisAlignedBoxObstacle:
    """世界系轴对齐方盒障碍。"""

    name: str
    center: np.ndarray
    half_extents: np.ndarray


@dataclass
class CylinderObstacle:
    """有限圆柱（细杆）：中心、单位轴向、半径、半长。"""

    name: str
    center: np.ndarray
    axis: np.ndarray
    radius: float
    half_length: float


Obstacle = AxisAlignedBoxObstacle | CylinderObstacle


@dataclass
class CbfConfig:
    d_safe: float = 0.02
    gamma: float = 0.8
    lambda_cbf: float = 0.5
    dq_max: float = ACTION_SCALE
    activate_margin: float = 0.10
    task_weight: np.ndarray = field(default_factory=lambda: np.ones(3, dtype=np.float64))
    monitor_specs: tuple[tuple[str, float], ...] = DEFAULT_MONITOR_SPECS
    obstacle_geom_names: tuple[str, ...] = DEFAULT_OBSTACLE_GEOM_NAMES


@dataclass
class MonitorPoint:
    name: str
    r_link: float
    body_id: int | None = None  # None 表示 pinch TCP


def box_h_and_grad_p(
    p: np.ndarray,
    center: np.ndarray,
    half_extents: np.ndarray,
    d_safe: float,
    r_link: float,
) -> tuple[float, np.ndarray]:
    """点到轴对齐盒的符号距离 h 与 ∇_p h（世界系）。"""
    p = np.asarray(p, dtype=np.float64).reshape(3)
    center = np.asarray(center, dtype=np.float64).reshape(3)
    half_extents = np.asarray(half_extents, dtype=np.float64).reshape(3)
    d = p - center
    d_clamp = np.clip(d, -half_extents, half_extents)
    p_close = center + d_clamp
    delta = p - p_close
    dist = float(np.linalg.norm(delta))
    margin = float(d_safe + r_link)
    if dist > 1e-8:
        grad_p = delta / dist
        h = dist - margin
        return h, grad_p
    slack = half_extents - np.abs(d)
    axis = int(np.argmin(slack))
    sign = 1.0 if d[axis] >= 0.0 else -1.0
    grad_p = np.zeros(3, dtype=np.float64)
    grad_p[axis] = sign
    h = float(slack[axis] - margin)
    return h, grad_p


def _unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n < 1e-12:
        return np.array([0.0, 0.0, 1.0], dtype=np.float64)
    return v / n


def cylinder_h_and_grad_p(
    p: np.ndarray,
    center: np.ndarray,
    axis: np.ndarray,
    radius: float,
    half_length: float,
    d_safe: float,
    r_link: float,
) -> tuple[float, np.ndarray]:
    """点到有限圆柱（侧面+端盖）的符号距离 h 与 ∇_p h。"""
    p = np.asarray(p, dtype=np.float64).reshape(3)
    center = np.asarray(center, dtype=np.float64).reshape(3)
    axis = _unit(np.asarray(axis, dtype=np.float64).reshape(3))
    v = p - center
    t_ax = float(np.dot(v, axis))
    r_vec = v - t_ax * axis
    r_dist = float(np.linalg.norm(r_vec))
    margin = float(d_safe + r_link)

    if abs(t_ax) <= half_length:
        if r_dist > 1e-8:
            grad_p = r_vec / r_dist
            h = r_dist - float(radius) - margin
            return h, grad_p
        sign = 1.0 if abs(axis[0]) < 0.9 else 1.0
        grad_p = np.array([sign, 0.0, 0.0], dtype=np.float64)
        if abs(axis[0]) > 0.9:
            grad_p = np.array([0.0, sign, 0.0], dtype=np.float64)
        h = -float(radius) - margin
        return h, grad_p

    t_cap = half_length if t_ax > 0.0 else -half_length
    cap_center = center + t_cap * axis
    v_cap = p - cap_center
    r_cap = v_cap - np.dot(v_cap, axis) * axis
    r_cap_dist = float(np.linalg.norm(r_cap))
    axial = abs(t_ax) - half_length
    if r_cap_dist <= float(radius):
        grad_p = axis if t_ax > 0.0 else -axis
        h = axial - margin
        return h, grad_p
    if r_cap_dist > 1e-8:
        radial_dir = r_cap / r_cap_dist
        closest = cap_center + radial_dir * float(radius)
    else:
        closest = cap_center
        radial_dir = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    delta = p - closest
    dist = float(np.linalg.norm(delta))
    if dist > 1e-8:
        return dist - margin, delta / dist
    return -margin, radial_dir


def obstacle_h_and_grad_p(
    p: np.ndarray,
    obs: Obstacle,
    d_safe: float,
    r_link: float,
) -> tuple[float, np.ndarray]:
    if isinstance(obs, CylinderObstacle):
        return cylinder_h_and_grad_p(
            p, obs.center, obs.axis, obs.radius, obs.half_length, d_safe, r_link
        )
    return box_h_and_grad_p(p, obs.center, obs.half_extents, d_safe, r_link)


def _geom_world_pose(model: mujoco.MjModel, data: mujoco.MjData, gid: int):
    bid = int(model.geom_bodyid[gid])
    gpos = np.asarray(model.geom_pos[gid], dtype=np.float64)
    gquat = np.asarray(model.geom_quat[gid], dtype=np.float64)
    if float(np.linalg.norm(gquat)) < 1e-12:
        gquat = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
    body_pos = np.asarray(data.xpos[bid], dtype=np.float64)
    body_mat = np.asarray(data.xmat[bid], dtype=np.float64).reshape(3, 3)
    # geom_quat 相对 body 的旋转（MuJoCo 4-tuple wxyz）
    w, x, y, z = gquat
    rot_g = np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float64,
    )
    center = body_pos + body_mat @ gpos
    world_rot = body_mat @ rot_g
    return center, world_rot


def load_obstacles(model: mujoco.MjModel, data: mujoco.MjData, geom_names: tuple[str, ...]):
    obstacles: list[Obstacle] = []
    for gname in geom_names:
        gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, gname)
        if gid < 0:
            continue
        center, world_rot = _geom_world_pose(model, data, gid)
        gtype = int(model.geom_type[gid])
        if gtype == int(mujoco.mjtGeom.mjGEOM_BOX):
            half_extents = np.asarray(model.geom_size[gid][:3], dtype=np.float64)
            obstacles.append(AxisAlignedBoxObstacle(name=gname, center=center, half_extents=half_extents))
        elif gtype == int(mujoco.mjtGeom.mjGEOM_CYLINDER):
            radius = float(model.geom_size[gid][0])
            half_length = float(model.geom_size[gid][1])
            axis = _unit(world_rot[:, 2])
            obstacles.append(
                CylinderObstacle(
                    name=gname,
                    center=center,
                    axis=axis,
                    radius=radius,
                    half_length=half_length,
                )
            )
    return obstacles


def load_box_obstacles(model: mujoco.MjModel, data: mujoco.MjData, geom_names: tuple[str, ...]):
    """兼容旧名。"""
    return [o for o in load_obstacles(model, data, geom_names) if isinstance(o, AxisAlignedBoxObstacle)]


def resolve_monitor_points(model: mujoco.MjModel, specs: tuple[tuple[str, float], ...]) -> list[MonitorPoint]:
    points: list[MonitorPoint] = []
    for name, r_link in specs:
        if name == "tcp":
            points.append(MonitorPoint(name=name, r_link=float(r_link), body_id=None))
            continue
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        if bid < 0:
            raise ValueError(f"monitor body not found: {name}")
        points.append(MonitorPoint(name=name, r_link=float(r_link), body_id=int(bid)))
    return points


def _backup_arm_qpos(data: mujoco.MjData, ids) -> np.ndarray:
    return np.asarray([data.qpos[a] for a in ids.qpos_adr], dtype=np.float64)


def _restore_arm_qpos(data: mujoco.MjData, ids, q_arm: np.ndarray) -> None:
    for i, adr in enumerate(ids.qpos_adr):
        data.qpos[adr] = float(q_arm[i])


def _with_arm_qpos(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    q_arm: np.ndarray,
    fn: Callable[[], object],
):
    saved = _backup_arm_qpos(data, ids)
    _restore_arm_qpos(data, ids, q_arm)
    mujoco.mj_forward(model, data)
    try:
        return fn()
    finally:
        _restore_arm_qpos(data, ids, saved)
        mujoco.mj_forward(model, data)


def body_pos_and_jacobian(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    body_id: int,
) -> tuple[np.ndarray, np.ndarray]:
    pos = np.asarray(data.xpos[body_id], dtype=np.float64).copy()
    jacp = np.zeros((3, model.nv), dtype=np.float64)
    jacr = np.zeros((3, model.nv), dtype=np.float64)
    mujoco.mj_jac(model, data, jacp, jacr, pos, body_id)
    j_arm = jacp[:, ids.dof_adr]
    return pos, np.asarray(j_arm, dtype=np.float64)


def tcp_pos_and_jacobian(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    tcp_pose_fn,
    eps: float = 1e-6,
) -> tuple[np.ndarray, np.ndarray]:
    q0 = _backup_arm_qpos(data, ids)
    p0, _ = tcp_pose_fn(data, ids)
    j = np.zeros((3, ACTION_DIM), dtype=np.float64)
    for i in range(ACTION_DIM):
        q_try = q0.copy()
        q_try[i] += eps
        _restore_arm_qpos(data, ids, q_try)
        mujoco.mj_forward(model, data)
        p1, _ = tcp_pose_fn(data, ids)
        j[:, i] = (p1 - p0) / eps
    _restore_arm_qpos(data, ids, q0)
    mujoco.mj_forward(model, data)
    return np.asarray(p0, dtype=np.float64), j


def _worst_barrier(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    monitors: list[MonitorPoint],
    obstacles: list[Obstacle],
    cfg: CbfConfig,
    tcp_pose_fn,
) -> tuple[list[dict], float, dict | None]:
    records: list[dict] = []
    h_min = float("inf")
    worst: dict | None = None
    for mon in monitors:
        if mon.body_id is None:
            pos, j_pos = tcp_pos_and_jacobian(model, data, ids, tcp_pose_fn)
        else:
            pos, j_pos = body_pos_and_jacobian(model, data, ids, mon.body_id)
        for obs in obstacles:
            h, grad_p = obstacle_h_and_grad_p(pos, obs, cfg.d_safe, mon.r_link)
            grad_q = j_pos.T @ grad_p
            rec = {
                "monitor": mon.name,
                "obstacle": obs.name,
                "h": float(h),
                "grad_q": grad_q,
            }
            records.append(rec)
            if float(h) < h_min:
                h_min = float(h)
                worst = rec
    return records, h_min, worst


def _build_constraints(records: list[dict], cfg: CbfConfig) -> tuple[np.ndarray, np.ndarray]:
    rows: list[np.ndarray] = []
    rhs: list[float] = []
    for rec in records:
        h = float(rec["h"])
        if h >= cfg.activate_margin:
            continue
        grad_q = np.asarray(rec["grad_q"], dtype=np.float64)
        rows.append(grad_q)
        rhs.append(-cfg.gamma * h)
    if not rows:
        return np.zeros((0, ACTION_DIM)), np.zeros(0, dtype=np.float64)
    return np.stack(rows, axis=0), np.asarray(rhs, dtype=np.float64)


def _solve_qp_embodisteer(
    j_task: np.ndarray,
    a_ineq: np.ndarray,
    b_ineq: np.ndarray,
    cfg: CbfConfig,
) -> tuple[np.ndarray | None, bool]:
    """min ½‖W^{1/2} J Δq‖² + ½λ‖Δq‖²  s.t. AΔq ≥ b, box."""
    n = ACTION_DIM
    w = np.asarray(cfg.task_weight, dtype=np.float64).reshape(3)
    w_sqrt = np.sqrt(np.clip(w, 1e-12, None))
    j_w = w_sqrt[:, None] * j_task
    h_mat = j_w.T @ j_w + float(cfg.lambda_cbf) * np.eye(n, dtype=np.float64)

    lb = -float(cfg.dq_max) * np.ones(n, dtype=np.float64)
    ub = float(cfg.dq_max) * np.ones(n, dtype=np.float64)

    if a_ineq.shape[0] == 0:
        return np.zeros(n, dtype=np.float64), True

    if _HAS_SCIPY:
        def objective(x: np.ndarray) -> float:
            return 0.5 * float(x @ h_mat @ x)

        constraints = []
        for i in range(a_ineq.shape[0]):
            ai = a_ineq[i]
            bi = float(b_ineq[i])
            constraints.append({"type": "ineq", "fun": lambda x, ai=ai, bi=bi: float(ai @ x - bi)})

        bounds = [(float(lb[i]), float(ub[i])) for i in range(n)]
        res = minimize(
            objective,
            np.zeros(n, dtype=np.float64),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"ftol": 1e-9, "maxiter": 200},
        )
        if res.success and np.all(a_ineq @ res.x >= b_ineq - 1e-6):
            return np.asarray(res.x, dtype=np.float64), True

    return _solve_qp_projected_gradient(h_mat, a_ineq, b_ineq, lb, ub)


def solve_cbf_correction(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    dq_nom: np.ndarray,
    cfg: CbfConfig,
    monitors: list[MonitorPoint],
    obstacles: list[Obstacle],
    tcp_pose_fn,
) -> tuple[np.ndarray, dict]:
    """在 q_diff = q + dq_nom 处求 Δq_cbf。"""
    dq_nom = np.asarray(dq_nom, dtype=np.float64).reshape(ACTION_DIM)
    info: dict = {
        "cbf_active": False,
        "cbf_feasible": True,
        "h_min": float("inf"),
        "cbf_worst_monitor": "",
        "cbf_worst_obstacle": "",
        "dq_cbf_norm": 0.0,
        "dq_nom_norm": float(np.linalg.norm(dq_nom)),
        "n_constraints": 0,
    }
    if not obstacles:
        return np.zeros(ACTION_DIM, dtype=np.float64), info

    q_now = _backup_arm_qpos(data, ids)
    q_diff = q_now + dq_nom

    def _eval():
        return _worst_barrier(model, data, ids, monitors, obstacles, cfg, tcp_pose_fn)

    records, h_min, worst = _with_arm_qpos(model, data, ids, q_diff, _eval)
    info["h_min"] = float(h_min)
    if worst is not None:
        info["cbf_worst_monitor"] = str(worst["monitor"])
        info["cbf_worst_obstacle"] = str(worst["obstacle"])

    if h_min >= cfg.activate_margin:
        return np.zeros(ACTION_DIM, dtype=np.float64), info

    info["cbf_active"] = True
    a_ineq, b_ineq = _build_constraints(records, cfg)
    info["n_constraints"] = int(a_ineq.shape[0])

    def _task_jac():
        _, j_task = tcp_pos_and_jacobian(model, data, ids, tcp_pose_fn)
        return j_task

    j_task = _with_arm_qpos(model, data, ids, q_diff, _task_jac)

    dq_cbf, ok = _solve_qp_embodisteer(j_task, a_ineq, b_ineq, cfg)
    if not ok or dq_cbf is None:
        info["cbf_feasible"] = False
        return np.zeros(ACTION_DIM, dtype=np.float64), info

    dq_cbf = np.clip(dq_cbf, -cfg.dq_max, cfg.dq_max)
    info["dq_cbf_norm"] = float(np.linalg.norm(dq_cbf))
    info["dq_total_norm"] = float(np.linalg.norm(dq_nom + dq_cbf))
    return dq_cbf, info


def cbf_step_log_record(ep: int, step: int, t: float, info: dict) -> dict:
    """单步 CBF 日志（可 JSON 序列化）。"""
    return {
        "ep": int(ep),
        "step": int(step),
        "t_s": float(t),
        "h_min_m": float(info.get("h_min", float("nan"))),
        "cbf_active": bool(info.get("cbf_active", False)),
        "cbf_feasible": bool(info.get("cbf_feasible", True)),
        "n_constraints": int(info.get("n_constraints", 0)),
        "worst_monitor": str(info.get("cbf_worst_monitor", "")),
        "worst_obstacle": str(info.get("cbf_worst_obstacle", "")),
        "dq_nom_norm": float(info.get("dq_nom_norm", 0.0)),
        "dq_cbf_norm": float(info.get("dq_cbf_norm", 0.0)),
        "dq_total_norm": float(info.get("dq_total_norm", info.get("dq_nom_norm", 0.0))),
    }
