"""EMBODISTEER 式全身 CBF-QP：在 PPO 名义增量上做最小安全修正。

v2：在当前 q 评估 h；约束作用于 dq_total=dq_nom+dq_cbf；不可行时投影 dq_nom。
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


def _dq_cbf_bounds(dq_nom: np.ndarray, dq_max: float) -> tuple[np.ndarray, np.ndarray]:
    """dq_total=dq_nom+dq_cbf ∈ [-dq_max,dq_max] 时 dq_cbf 的逐关节上下界。"""
    dq_nom = np.asarray(dq_nom, dtype=np.float64).reshape(-1)
    m = float(dq_max)
    return -m - dq_nom, m - dq_nom


def _find_feasible_point(
    a_ineq: np.ndarray,
    b_ineq: np.ndarray,
    lb: np.ndarray,
    ub: np.ndarray,
    x0: np.ndarray | None = None,
    max_iter: int = 200,
) -> tuple[np.ndarray | None, bool]:
    n = lb.shape[0]
    x = _project_box(np.zeros(n, dtype=np.float64) if x0 is None else x0.copy(), lb, ub)
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
    x0: np.ndarray | None = None,
    max_iter: int = 300,
) -> tuple[np.ndarray | None, bool]:
    """min ½ xᵀ H x  s.t. A x >= b, box。"""
    n = lb.shape[0]
    if a_ineq.shape[0] == 0:
        return np.zeros(n, dtype=np.float64), True

    x0_use = np.zeros(n, dtype=np.float64) if x0 is None else _project_box(x0, lb, ub)
    x, ok = _find_feasible_point(a_ineq, b_ineq, lb, ub, x0=x0_use)
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


def _project_dq_total(
    dq_nom: np.ndarray,
    a_ineq: np.ndarray,
    b_total: np.ndarray,
    dq_max: float,
    max_iter: int = 120,
) -> tuple[np.ndarray, bool]:
    """不可行时：将 dq_nom 投影到 CBF+box 可行集，min 改动（迭代投影）。"""
    m = float(dq_max)
    dq = np.clip(np.asarray(dq_nom, dtype=np.float64).reshape(-1), -m, m)
    if a_ineq.shape[0] == 0:
        return dq, True
    for _ in range(max_iter):
        viol = b_total - a_ineq @ dq
        worst = float(np.max(viol))
        if worst <= 1e-7:
            return dq, True
        i = int(np.argmax(viol))
        ai = a_ineq[i]
        denom = float(ai @ ai) + 1e-12
        dq = dq + ((worst + 1e-5) / denom) * ai
        dq = np.clip(dq, -m, m)
    return dq, False

try:
    from .constants import ACTION_DIM, ACTION_SCALE
except ImportError:
    from constants import ACTION_DIM, ACTION_SCALE  # type: ignore


DEFAULT_MONITOR_SPECS: tuple[tuple[str, float], ...] = (
    ("shoulder_pitch", 0.02),
    ("ellbow", 0.035),
    ("wrist_pitch", 0.035),
    ("wrist_roll", 0.025),
    ("gripper", 0.025),
    ("tcp", 0.015),
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
    activate_margin: float = 0.04
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


def _build_constraints(
    records: list[dict],
    cfg: CbfConfig,
    dq_nom: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """返回 A, b_total（约束 dq_total）, b_cbf（约束 dq_cbf）。"""
    rows: list[np.ndarray] = []
    rhs_total: list[float] = []
    rhs_cbf: list[float] = []
    dq_nom = np.asarray(dq_nom, dtype=np.float64).reshape(ACTION_DIM)
    for rec in records:
        h = float(rec["h"])
        if h >= cfg.activate_margin:
            continue
        grad_q = np.asarray(rec["grad_q"], dtype=np.float64)
        b_tot = -cfg.gamma * h
        rows.append(grad_q)
        rhs_total.append(b_tot)
        rhs_cbf.append(b_tot - float(grad_q @ dq_nom))
    if not rows:
        z = np.zeros(0, dtype=np.float64)
        empty = np.zeros((0, ACTION_DIM), dtype=np.float64)
        return empty, z, z
    a = np.stack(rows, axis=0)
    return a, np.asarray(rhs_total, dtype=np.float64), np.asarray(rhs_cbf, dtype=np.float64)


def _solve_qp_min_correction(
    a_ineq: np.ndarray,
    b_ineq: np.ndarray,
    lb: np.ndarray,
    ub: np.ndarray,
) -> tuple[np.ndarray | None, bool]:
    """min ½‖dq_cbf‖²  s.t. A·dq_cbf ≥ b, box（贴近 dq_nom 的最小修正）。"""
    n = ACTION_DIM
    h_mat = np.eye(n, dtype=np.float64)

    if a_ineq.shape[0] == 0:
        return np.zeros(n, dtype=np.float64), True

    if _HAS_SCIPY:
        def objective(x: np.ndarray) -> float:
            return 0.5 * float(x @ x)

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
    """在当前 q 处求 Δq_cbf，使 dq_total=dq_nom+Δq_cbf 满足 CBF。"""
    dq_nom = np.asarray(dq_nom, dtype=np.float64).reshape(ACTION_DIM)
    info: dict = {
        "cbf_active": False,
        "cbf_feasible": True,
        "cbf_projected": False,
        "h_min": float("inf"),
        "cbf_worst_monitor": "",
        "cbf_worst_obstacle": "",
        "dq_cbf_norm": 0.0,
        "dq_nom_norm": float(np.linalg.norm(dq_nom)),
        "nom_violation": 0.0,
        "n_constraints": 0,
    }
    if not obstacles:
        return np.zeros(ACTION_DIM, dtype=np.float64), info

    records, h_min, worst = _worst_barrier(
        model, data, ids, monitors, obstacles, cfg, tcp_pose_fn
    )
    info["h_min"] = float(h_min)
    if worst is not None:
        info["cbf_worst_monitor"] = str(worst["monitor"])
        info["cbf_worst_obstacle"] = str(worst["obstacle"])
        info["nom_violation"] = float(-(float(worst["grad_q"] @ dq_nom) + cfg.gamma * float(worst["h"])))

    need_active = h_min < cfg.activate_margin
    if not need_active:
        for rec in records:
            if float(rec["h"]) >= cfg.activate_margin:
                continue
            g = np.asarray(rec["grad_q"], dtype=np.float64)
            if float(g @ dq_nom) < -cfg.gamma * float(rec["h"]) - 1e-9:
                need_active = True
                break

    if not need_active:
        return np.zeros(ACTION_DIM, dtype=np.float64), info

    info["cbf_active"] = True
    a_ineq, b_total, b_cbf = _build_constraints(records, cfg, dq_nom)
    info["n_constraints"] = int(a_ineq.shape[0])

    lb_cbf, ub_cbf = _dq_cbf_bounds(dq_nom, cfg.dq_max)
    dq_cbf, ok = _solve_qp_min_correction(a_ineq, b_cbf, lb_cbf, ub_cbf)

    if not ok or dq_cbf is None:
        dq_total, proj_ok = _project_dq_total(dq_nom, a_ineq, b_total, cfg.dq_max)
        dq_cbf = dq_total - dq_nom
        info["cbf_feasible"] = bool(proj_ok)
        info["cbf_projected"] = True
    else:
        dq_total = dq_nom + dq_cbf
        if not np.all(a_ineq @ dq_total >= b_total - 1e-5):
            dq_total, proj_ok = _project_dq_total(dq_nom, a_ineq, b_total, cfg.dq_max)
            dq_cbf = dq_total - dq_nom
            info["cbf_feasible"] = bool(proj_ok)
            info["cbf_projected"] = True

    dq_cbf = np.clip(dq_cbf, lb_cbf, ub_cbf)
    dq_total = np.clip(dq_nom + dq_cbf, -cfg.dq_max, cfg.dq_max)
    dq_cbf = dq_total - dq_nom
    info["dq_cbf_norm"] = float(np.linalg.norm(dq_cbf))
    info["dq_total_norm"] = float(np.linalg.norm(dq_total))
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
        "cbf_projected": bool(info.get("cbf_projected", False)),
        "nom_violation": float(info.get("nom_violation", 0.0)),
    }
