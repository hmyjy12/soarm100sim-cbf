"""EMBODISTEER 式全身 CBF-QP：在 PPO 名义增量上做最小安全修正。

v2：在当前 q 评估 h；约束作用于 dq_total=dq_nom+dq_cbf；不可行时投影 dq_nom。
共享默认保持 legacy/real-safe 行为：每段 capsule 采样 9 点，QP 使用 identity
metric。仿真入口可通过 ``CbfConfig`` 显式选择更密的采样和 task-preserving metric。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import mujoco
import numpy as np

try:
    from scipy.optimize import minimize
    from scipy.spatial import cKDTree

    _HAS_SCIPY = True
except ImportError:
    cKDTree = None  # type: ignore[assignment]
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
    # wrist_pitch 由前臂胶囊覆盖（见 DEFAULT_CAPSULE_SPECS）
    ("wrist_roll", 0.025),
    ("gripper", 0.025),
    ("tcp", 0.015),
)

# 全臂胶囊链：CBF 约束仍用线段采样近似，但避免只监测 body 原点导致漏杆。
DEFAULT_CAPSULE_SPECS: tuple[tuple[str, str, float], ...] = (
    ("base", "shoulder_rotation", 0.035),
    ("shoulder_rotation", "shoulder_pitch", 0.035),
    ("shoulder_pitch", "ellbow", 0.038),
    ("ellbow", "wrist_pitch", 0.04),
    ("wrist_pitch", "wrist_jaw", 0.035),
    ("wrist_jaw", "wrist_roll", 0.032),
    ("wrist_roll", "gripper", 0.030),
)

# 对外兼容常量保持 legacy 值；增强采样必须由每个 CbfConfig 显式选择，不能改共享全局默认。
CAPSULE_SEGMENT_SAMPLES = 9

DEFAULT_OBSTACLE_GEOM_NAMES: tuple[str, ...] = ("obstacle_rod",)


@dataclass
class AxisAlignedBoxObstacle:
    """世界系轴对齐方盒障碍。"""

    name: str
    center: np.ndarray
    half_extents: np.ndarray
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))


@dataclass
class CylinderObstacle:
    """有限圆柱（细杆）：中心、单位轴向、半径、半长。"""

    name: str
    center: np.ndarray
    axis: np.ndarray
    radius: float
    half_length: float
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))


@dataclass
class PointCloudSdfObstacle:
    """由障碍物表面点云构造的 unsigned SDF 查询对象。"""

    name: str
    points: np.ndarray
    truncation_distance: float = 0.12
    voxel_size: float = 0.01
    inflate: float = 0.0
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    _tree: object | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        pts = np.asarray(self.points, dtype=np.float64).reshape(-1, 3)
        finite = np.all(np.isfinite(pts), axis=1)
        pts = pts[finite]
        if pts.shape[0] > 0 and float(self.voxel_size) > 1e-6:
            pts = _voxel_downsample_points(pts, float(self.voxel_size))
        self.points = pts
        self.velocity = np.asarray(self.velocity, dtype=np.float64).reshape(3)
        if cKDTree is not None and pts.shape[0] > 0:
            self._tree = cKDTree(pts)


Obstacle = AxisAlignedBoxObstacle | CylinderObstacle | PointCloudSdfObstacle


@dataclass
class CbfConstraint:
    """OSCBF 风格的约束行：先把安全约束收集起来，再统一交给 QP。"""

    name: str
    source: str
    a: np.ndarray
    b_total: float
    b_delta: float
    h: float
    active: bool = True
    debug: dict = field(default_factory=dict)


@dataclass
class CapsulePairBarrier:
    """两段 capsule 之间的 self/inter-arm 距离约束信息。"""

    left_name: str
    right_name: str
    h: float
    distance: float
    normal: np.ndarray
    s_left: float
    t_right: float
    p_left: np.ndarray
    p_right: np.ndarray
    grad_left: np.ndarray
    grad_right: np.ndarray


@dataclass
class CbfConfig:
    d_safe: float = 0.02
    gamma: float = 0.8
    lambda_cbf: float = 0.5
    dq_max: float = ACTION_SCALE
    activate_margin: float = 0.04
    task_weight: np.ndarray = field(default_factory=lambda: np.ones(3, dtype=np.float64))
    frozen_joint_mask: np.ndarray = field(
        default_factory=lambda: np.zeros(ACTION_DIM, dtype=bool)
    )
    monitor_specs: tuple[tuple[str, float], ...] = DEFAULT_MONITOR_SPECS
    capsule_specs: tuple[tuple[str, str, float], ...] = DEFAULT_CAPSULE_SPECS
    obstacle_geom_names: tuple[str, ...] = DEFAULT_OBSTACLE_GEOM_NAMES
    # 共享默认刻意保持已验证的真机路径；增强能力必须由入口显式开启。
    capsule_sample_count: int = CAPSULE_SEGMENT_SAMPLES
    qp_metric: str = "identity"
    task_preserve_weight: float = 1.0
    target_guidance: bool = False
    target_guidance_clearance: float = 0.07
    target_guidance_reach: float = 0.04
    target_guidance_forward: float = 0.0
    target_guidance_dynamic_clearance: float = 0.14
    target_guidance_dynamic_forward: float = 0.04
    target_guidance_dynamic_speed_thresh: float = 1e-4
    target_guidance_dynamic_closing_speed_thresh: float = 1e-4
    target_guidance_release_steps: int = 32
    target_guidance_switch_slack: float = 0.05
    target_guidance_dynamic_lookahead_steps: float = 2.0
    dynamic_obstacle_lookahead_steps: float = 0.0


@dataclass
class DualArmCbfConfig:
    """实验性双臂 safety filter 配置：环境沿用单臂，左右臂互避单独调参。

    当前仅覆盖纯数学和 QP 测试；双臂 MuJoCo 模型级回归尚未完成。
    """

    env: CbfConfig = field(default_factory=CbfConfig)
    d_safe_inter_arm: float = 0.03
    gamma_inter_arm: float = 0.8
    activate_margin_inter_arm: float = 0.06
    top_k_inter_arm: int = 3
    dq_max: float = ACTION_SCALE
    frozen_joint_mask: np.ndarray | None = None


@dataclass
class MonitorPoint:
    name: str
    r_link: float
    body_id: int | None = None  # None 表示 pinch TCP


@dataclass
class CapsuleMonitor:
    """连杆胶囊：父子 body 原点连线 + 半径 r_link（CBF 用线段采样近似）。"""

    name: str
    body_a_id: int
    body_b_id: int
    r_link: float


Monitor = MonitorPoint | CapsuleMonitor
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


def _voxel_downsample_points(points: np.ndarray, voxel_size: float) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return pts
    v = max(float(voxel_size), 1e-9)
    keys = np.floor(pts / v).astype(np.int64)
    _, first = np.unique(keys, axis=0, return_index=True)
    return pts[np.sort(first)]


def pointcloud_sdf_h_and_grad_p(
    p: np.ndarray,
    obs: PointCloudSdfObstacle,
    d_safe: float,
    r_link: float,
) -> tuple[float, np.ndarray]:
    """点到表面点云 unsigned SDF 的 h 与 ∇_p h。"""
    p = np.asarray(p, dtype=np.float64).reshape(3)
    pts = np.asarray(obs.points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return float("inf"), np.zeros(3, dtype=np.float64)

    if obs._tree is not None:
        dist, idx = obs._tree.query(p, k=1, distance_upper_bound=float(obs.truncation_distance))
        if not np.isfinite(dist) or int(idx) >= pts.shape[0]:
            return float(obs.truncation_distance), np.zeros(3, dtype=np.float64)
        nearest = pts[int(idx)]
    else:
        delta_all = pts - p.reshape(1, 3)
        d2 = np.einsum("ij,ij->i", delta_all, delta_all)
        idx = int(np.argmin(d2))
        dist = float(np.sqrt(d2[idx]))
        if dist > float(obs.truncation_distance):
            return float(obs.truncation_distance), np.zeros(3, dtype=np.float64)
        nearest = pts[idx]

    delta = p - nearest
    dist = float(np.linalg.norm(delta))
    if dist > 1e-9:
        grad_p = delta / dist
    else:
        grad_p = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    h = dist - float(obs.inflate) - float(d_safe) - float(r_link)
    return h, grad_p


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
    if isinstance(obs, PointCloudSdfObstacle):
        return pointcloud_sdf_h_and_grad_p(p, obs, d_safe, r_link)
    if isinstance(obs, CylinderObstacle):
        return cylinder_h_and_grad_p(
            p, obs.center, obs.axis, obs.radius, obs.half_length, d_safe, r_link
        )
    return box_h_and_grad_p(p, obs.center, obs.half_extents, d_safe, r_link)


def obstacle_step_velocity(obs: Obstacle) -> np.ndarray:
    return np.asarray(getattr(obs, "velocity", np.zeros(3, dtype=np.float64)), dtype=np.float64).reshape(3)


def segment_obstacle_h_and_grad(
    p0: np.ndarray,
    p1: np.ndarray,
    j0: np.ndarray,
    j1: np.ndarray,
    obs: Obstacle,
    d_safe: float,
    r_link: float,
    n_samples: int = CAPSULE_SEGMENT_SAMPLES,
) -> tuple[float, np.ndarray, np.ndarray, float]:
    """线段胶囊到障碍的最紧 h 与 ∇_q h（采样最近点 + Jacobian 线性插值）。"""
    p0 = np.asarray(p0, dtype=np.float64).reshape(3)
    p1 = np.asarray(p1, dtype=np.float64).reshape(3)
    j0 = np.asarray(j0, dtype=np.float64)
    j1 = np.asarray(j1, dtype=np.float64)
    n = max(2, int(n_samples))
    ts = np.linspace(0.0, 1.0, n, dtype=np.float64)

    h_min = float("inf")
    grad_q_best = np.zeros(ACTION_DIM, dtype=np.float64)
    grad_p_best = np.zeros(3, dtype=np.float64)
    t_best = 0.0
    for t in ts:
        p = p0 + t * (p1 - p0)
        h, grad_p = obstacle_h_and_grad_p(p, obs, d_safe, r_link)
        if float(h) < h_min:
            h_min = float(h)
            t_best = float(t)
            grad_p_best = np.asarray(grad_p, dtype=np.float64).reshape(3)
            j_interp = (1.0 - t) * j0 + t * j1
            grad_q_best = j_interp.T @ grad_p
    return h_min, grad_q_best, grad_p_best, t_best


def closest_points_on_segments(
    a0: np.ndarray,
    a1: np.ndarray,
    b0: np.ndarray,
    b1: np.ndarray,
    eps: float = 1e-12,
) -> tuple[float, float, np.ndarray, np.ndarray]:
    """两条有限线段的最近点；self-collision / inter-arm capsule 距离会用到。"""
    a0 = np.asarray(a0, dtype=np.float64).reshape(3)
    a1 = np.asarray(a1, dtype=np.float64).reshape(3)
    b0 = np.asarray(b0, dtype=np.float64).reshape(3)
    b1 = np.asarray(b1, dtype=np.float64).reshape(3)

    u = a1 - a0
    v = b1 - b0
    w0 = a0 - b0
    aa = float(u @ u)
    bb = float(u @ v)
    cc = float(v @ v)
    dd = float(u @ w0)
    ee = float(v @ w0)
    denom = aa * cc - bb * bb

    if aa < eps and cc < eps:
        s = 0.0
        t = 0.0
    elif aa < eps:
        s = 0.0
        t = float(np.clip(ee / max(cc, eps), 0.0, 1.0))
    elif cc < eps:
        t = 0.0
        s = float(np.clip(-dd / max(aa, eps), 0.0, 1.0))
    else:
        if abs(denom) > eps:
            s = float(np.clip((bb * ee - cc * dd) / denom, 0.0, 1.0))
        else:
            s = 0.0
        t = float(np.clip((bb * s + ee) / max(cc, eps), 0.0, 1.0))
        s = float(np.clip((bb * t - dd) / max(aa, eps), 0.0, 1.0))
        t = float(np.clip((bb * s + ee) / max(cc, eps), 0.0, 1.0))

    p_a = a0 + s * u
    p_b = b0 + t * v
    return s, t, p_a, p_b


def capsule_pair_h_and_grads(
    left_name: str,
    right_name: str,
    left_a: np.ndarray,
    left_b: np.ndarray,
    left_j_a: np.ndarray,
    left_j_b: np.ndarray,
    left_radius: float,
    right_a: np.ndarray,
    right_b: np.ndarray,
    right_j_a: np.ndarray,
    right_j_b: np.ndarray,
    right_radius: float,
    d_safe: float,
) -> CapsulePairBarrier:
    """左右两段 capsule 的 h 与两边关节梯度，用于 inter-arm CBF。"""
    s, t, p_left, p_right = closest_points_on_segments(
        left_a, left_b, right_a, right_b
    )
    delta = p_left - p_right
    distance = float(np.linalg.norm(delta))
    normal = delta / distance if distance > 1e-9 else np.array([0.0, 0.0, 1.0])

    j_left = (1.0 - s) * np.asarray(
        left_j_a, dtype=np.float64
    ) + s * np.asarray(left_j_b, dtype=np.float64)
    j_right = (1.0 - t) * np.asarray(
        right_j_a, dtype=np.float64
    ) + t * np.asarray(right_j_b, dtype=np.float64)
    grad_left = j_left.T @ normal
    grad_right = -(j_right.T @ normal)
    h = distance - float(left_radius) - float(right_radius) - float(d_safe)

    return CapsulePairBarrier(
        left_name=left_name,
        right_name=right_name,
        h=float(h),
        distance=distance,
        normal=normal,
        s_left=float(s),
        t_right=float(t),
        p_left=p_left,
        p_right=p_right,
        grad_left=np.asarray(grad_left, dtype=np.float64),
        grad_right=np.asarray(grad_right, dtype=np.float64),
    )


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


def resolve_capsule_monitors(
    model: mujoco.MjModel, specs: tuple[tuple[str, str, float], ...]
) -> list[CapsuleMonitor]:
    capsules: list[CapsuleMonitor] = []
    for body_a, body_b, r_link in specs:
        bid_a = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_a)
        bid_b = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_b)
        if bid_a < 0:
            raise ValueError(f"capsule body_a not found: {body_a}")
        if bid_b < 0:
            raise ValueError(f"capsule body_b not found: {body_b}")
        name = f"{body_a}->{body_b}"
        capsules.append(
            CapsuleMonitor(
                name=name,
                body_a_id=int(bid_a),
                body_b_id=int(bid_b),
                r_link=float(r_link),
            )
        )
    return capsules


def resolve_monitors(
    model: mujoco.MjModel,
    point_specs: tuple[tuple[str, float], ...],
    capsule_specs: tuple[tuple[str, str, float], ...] = DEFAULT_CAPSULE_SPECS,
) -> list[Monitor]:
    monitors: list[Monitor] = list(resolve_monitor_points(model, point_specs))
    monitors.extend(resolve_capsule_monitors(model, capsule_specs))
    return monitors


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
    monitors: list[Monitor],
    obstacles: list[Obstacle],
    cfg: CbfConfig,
    tcp_pose_fn,
) -> tuple[list[dict], float, dict | None]:
    records: list[dict] = []
    h_min = float("inf")
    worst: dict | None = None
    for mon in monitors:
        if isinstance(mon, CapsuleMonitor):
            p0, j0 = body_pos_and_jacobian(model, data, ids, mon.body_a_id)
            p1, j1 = body_pos_and_jacobian(model, data, ids, mon.body_b_id)
            for obs in obstacles:
                h, grad_q, grad_p, t_seg = segment_obstacle_h_and_grad(
                    p0,
                    p1,
                    j0,
                    j1,
                    obs,
                    cfg.d_safe,
                    mon.r_link,
                    n_samples=cfg.capsule_sample_count,
                )
                obs_vel = obstacle_step_velocity(obs)
                obs_step = float(grad_p @ obs_vel)
                rec = {
                    "monitor": mon.name,
                    "obstacle": obs.name,
                    "h": float(h),
                    "grad_q": grad_q,
                    "obs_step": obs_step,
                    "obs_speed": float(np.linalg.norm(obs_vel)),
                    "capsule_t": float(t_seg),
                }
                records.append(rec)
                if float(h) < h_min:
                    h_min = float(h)
                    worst = rec
            continue

        if mon.body_id is None:
            pos, j_pos = tcp_pos_and_jacobian(model, data, ids, tcp_pose_fn)
        else:
            pos, j_pos = body_pos_and_jacobian(model, data, ids, mon.body_id)
        for obs in obstacles:
            h, grad_p = obstacle_h_and_grad_p(pos, obs, cfg.d_safe, mon.r_link)
            grad_q = j_pos.T @ grad_p
            obs_vel = obstacle_step_velocity(obs)
            obs_step = float(grad_p @ obs_vel)
            rec = {
                "monitor": mon.name,
                "obstacle": obs.name,
                "h": float(h),
                "grad_q": grad_q,
                "obs_step": obs_step,
                "obs_speed": float(np.linalg.norm(obs_vel)),
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
    constraints = build_cbf_constraints_from_records(records, cfg, dq_nom)
    return stack_cbf_constraints(constraints, action_dim=ACTION_DIM)


def build_cbf_constraints_from_records(
    records: list[dict],
    cfg: CbfConfig,
    dq_nom: np.ndarray,
) -> list[CbfConstraint]:
    """把距离记录转成 OSCBF 风格的约束对象。"""
    constraints: list[CbfConstraint] = []
    dq_nom = np.asarray(dq_nom, dtype=np.float64).reshape(ACTION_DIM)
    for rec in records:
        h = float(rec["h"])
        if h >= cfg.activate_margin:
            continue
        grad_q = np.asarray(rec["grad_q"], dtype=np.float64).copy()
        frozen = np.asarray(cfg.frozen_joint_mask, dtype=bool).reshape(ACTION_DIM)
        grad_q[frozen] = 0.0
        obs_step = float(rec.get("obs_step", 0.0))
        obs_speed = float(rec.get("obs_speed", 0.0))
        h_eff = h - max(0.0, float(cfg.dynamic_obstacle_lookahead_steps)) * obs_speed
        b_tot = obs_step - cfg.gamma * h_eff
        monitor = str(rec.get("monitor", ""))
        obstacle = str(rec.get("obstacle", ""))
        constraints.append(
            CbfConstraint(
                name=f"{monitor}->{obstacle}",
                source="environment",
                a=grad_q,
                b_total=float(b_tot),
                b_delta=float(b_tot - float(grad_q @ dq_nom)),
                h=h,
                active=True,
                debug={
                    **{k: v for k, v in rec.items() if k != "grad_q"},
                    "h_eff": float(h_eff),
                    "dynamic_padding": float(h - h_eff),
                },
            )
        )
    return constraints


def stack_cbf_constraints(
    constraints: list[CbfConstraint],
    action_dim: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """把约束对象打包成 QP 使用的 A、b_total、b_delta。"""
    active = [c for c in constraints if c.active]
    if not active:
        z = np.zeros(0, dtype=np.float64)
        empty = np.zeros((0, int(action_dim)), dtype=np.float64)
        return empty, z, z
    a = np.stack(
        [np.asarray(c.a, dtype=np.float64).reshape(action_dim) for c in active],
        axis=0,
    )
    b_total = np.asarray([float(c.b_total) for c in active], dtype=np.float64)
    b_delta = np.asarray([float(c.b_delta) for c in active], dtype=np.float64)
    return a, b_total, b_delta


def inter_arm_constraint_from_capsule_pair(
    pair: CapsulePairBarrier,
    dq_nom_dual: np.ndarray,
    gamma: float,
    activate_margin: float,
) -> CbfConstraint:
    """把 left-capsule/right-capsule 距离结果转成双臂 QP 约束。"""
    grad_left = np.asarray(pair.grad_left, dtype=np.float64).reshape(-1)
    grad_right = np.asarray(pair.grad_right, dtype=np.float64).reshape(-1)
    a = np.concatenate([grad_left, grad_right])
    dq_nom_dual = np.asarray(dq_nom_dual, dtype=np.float64).reshape(a.shape[0])
    b_total = -float(gamma) * float(pair.h)
    return CbfConstraint(
        name=f"{pair.left_name}<->{pair.right_name}",
        source="inter_arm",
        a=a,
        b_total=b_total,
        b_delta=b_total - float(a @ dq_nom_dual),
        h=float(pair.h),
        active=bool(pair.h < float(activate_margin)),
        debug={
            "distance": float(pair.distance),
            "normal": pair.normal,
            "s_left": float(pair.s_left),
            "t_right": float(pair.t_right),
            "p_left": pair.p_left,
            "p_right": pair.p_right,
        },
    )


def make_task_preserving_hessian(
    action_dim: int,
    task_jacobians: list[tuple[np.ndarray, float]] | None = None,
    base_weight: float = 1.0,
) -> np.ndarray:
    """采用 OSCBF 任务一致性思想，使 QP 修正在满足安全约束时尽量少扰动指定任务。"""
    h_mat = float(base_weight) * np.eye(int(action_dim), dtype=np.float64)
    if not task_jacobians:
        return h_mat
    for jac, weight in task_jacobians:
        j = np.asarray(jac, dtype=np.float64)
        if j.ndim == 1:
            j = j.reshape(1, -1)
        h_mat += float(weight) * (j.T @ j)
    return h_mat


def make_qp_metric_hessian(
    cfg: CbfConfig,
    action_dim: int,
    tcp_jacobian: np.ndarray | None = None,
) -> np.ndarray:
    """按 ``cfg.qp_metric`` 显式构造 CBF 修正的 QP metric。

    ``identity`` 是 legacy/真机安全默认；``task_preserving`` 才会增加
    ``task_preserve_weight * J_tcp.T @ J_tcp``，供仿真实验显式启用。
    ``gamma`` 是离散 CBF 屏障增益；``lambda_cbf`` 仅为兼容已有调用保留，不能暗中
    变成 QP 目标权重。
    """
    metric = str(cfg.qp_metric).strip().lower()
    if metric == "identity":
        return np.eye(int(action_dim), dtype=np.float64)
    if metric == "task_preserving":
        if tcp_jacobian is None:
            raise ValueError("task_preserving QP metric requires tcp_jacobian")
        return make_task_preserving_hessian(
            action_dim=int(action_dim),
            task_jacobians=[(tcp_jacobian, float(cfg.task_preserve_weight))],
        )
    raise ValueError(
        f"unknown qp_metric {cfg.qp_metric!r}; expected 'identity' or 'task_preserving'"
    )


def lift_arm_constraint_to_dual(
    constraint: CbfConstraint,
    side: str,
    arm_dim: int,
) -> CbfConstraint:
    """单臂环境约束升维到双臂 QP：[A_L,0] 或 [0,A_R]。"""
    arm_dim = int(arm_dim)
    a_arm = np.asarray(constraint.a, dtype=np.float64).reshape(arm_dim)
    a_dual = np.zeros(2 * arm_dim, dtype=np.float64)
    side_norm = str(side).strip().lower()
    if side_norm in ("left", "l"):
        a_dual[:arm_dim] = a_arm
        source = "left_env"
    elif side_norm in ("right", "r"):
        a_dual[arm_dim:] = a_arm
        source = "right_env"
    else:
        raise ValueError(f"unknown dual-arm side: {side}")
    return CbfConstraint(
        name=constraint.name,
        source=source,
        a=a_dual,
        b_total=float(constraint.b_total),
        b_delta=float(constraint.b_delta),
        h=float(constraint.h),
        active=bool(constraint.active),
        debug=dict(constraint.debug),
    )


def build_environment_constraints_for_arm(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    dq_nom: np.ndarray,
    cfg: CbfConfig,
    monitors: list[Monitor],
    obstacles: list[Obstacle],
    tcp_pose_fn,
) -> tuple[list[CbfConstraint], dict]:
    """只构造单臂环境 CBF 约束，不求解 QP。"""
    dq_nom = np.asarray(dq_nom, dtype=np.float64).reshape(ACTION_DIM)
    info: dict = {
        "h_min": float("inf"),
        "worst_monitor": "",
        "worst_obstacle": "",
        "n_constraints": 0,
    }
    if not obstacles:
        return [], info
    records, h_min, worst = _worst_barrier(
        model, data, ids, monitors, obstacles, cfg, tcp_pose_fn
    )
    constraints = build_cbf_constraints_from_records(records, cfg, dq_nom)
    info["h_min"] = float(h_min)
    info["n_constraints"] = int(len(constraints))
    if worst is not None:
        info["worst_monitor"] = str(worst.get("monitor", ""))
        info["worst_obstacle"] = str(worst.get("obstacle", ""))
        info["worst_obs_step"] = float(worst.get("obs_step", 0.0))
        info["worst_capsule_t"] = float(worst.get("capsule_t", 0.0))
    return constraints, info


def _capsule_endpoint_states(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    capsule: CapsuleMonitor,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p0, j0 = body_pos_and_jacobian(model, data, ids, capsule.body_a_id)
    p1, j1 = body_pos_and_jacobian(model, data, ids, capsule.body_b_id)
    return p0, j0, p1, j1


def build_inter_arm_constraints_from_capsules(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    left_ids,
    right_ids,
    left_capsules: list[CapsuleMonitor],
    right_capsules: list[CapsuleMonitor],
    dq_nom_dual: np.ndarray,
    cfg: DualArmCbfConfig,
    pair_allowlist: set[tuple[str, str]] | None = None,
) -> tuple[list[CbfConstraint], dict]:
    """双臂扩展：以 OSCBF/VFI 思路将左右 capsule 的自碰距离转为 QP 约束。"""
    barriers: list[CapsulePairBarrier] = []
    for left_cap in left_capsules:
        left_key = str(left_cap.name)
        if pair_allowlist is not None:
            allowed_right = {
                right_name for left_name, right_name in pair_allowlist
                if left_name == left_key
            }
            if not allowed_right:
                continue
        l0, jl0, l1, jl1 = _capsule_endpoint_states(model, data, left_ids, left_cap)
        for right_cap in right_capsules:
            right_key = str(right_cap.name)
            if pair_allowlist is not None and right_key not in allowed_right:
                continue
            r0, jr0, r1, jr1 = _capsule_endpoint_states(
                model, data, right_ids, right_cap
            )
            barriers.append(
                capsule_pair_h_and_grads(
                    left_name=left_key,
                    right_name=right_key,
                    left_a=l0,
                    left_b=l1,
                    left_j_a=jl0,
                    left_j_b=jl1,
                    left_radius=left_cap.r_link,
                    right_a=r0,
                    right_b=r1,
                    right_j_a=jr0,
                    right_j_b=jr1,
                    right_radius=right_cap.r_link,
                    d_safe=cfg.d_safe_inter_arm,
                )
            )

    barriers.sort(key=lambda item: item.h)
    # 只将 h 最小的危险 pair 送入 QP；top_k=0 表示不截断、保留全部候选。
    top_k = max(0, int(cfg.top_k_inter_arm))
    selected = barriers[:top_k] if top_k > 0 else barriers
    constraints = [
        inter_arm_constraint_from_capsule_pair(
            pair,
            dq_nom_dual=dq_nom_dual,
            gamma=cfg.gamma_inter_arm,
            activate_margin=cfg.activate_margin_inter_arm,
        )
        for pair in selected
    ]

    worst = barriers[0] if barriers else None
    info: dict = {
        "h_LR_min": float(worst.h) if worst is not None else float("inf"),
        "distance_LR_min": float(worst.distance) if worst is not None else float("inf"),
        "worst_left_link": str(worst.left_name) if worst is not None else "",
        "worst_right_link": str(worst.right_name) if worst is not None else "",
        "n_interarm_candidates": int(len(barriers)),
        "n_interarm_selected": int(len(selected)),
        "n_interarm_constraints": int(sum(1 for c in constraints if c.active)),
    }
    return constraints, info


def solve_dual_arm_cbf_correction(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    left_ids,
    right_ids,
    dq_left_nom: np.ndarray,
    dq_right_nom: np.ndarray,
    cfg: DualArmCbfConfig,
    left_monitors: list[Monitor],
    right_monitors: list[Monitor],
    obstacles: list[Obstacle],
    left_tcp_pose_fn,
    right_tcp_pose_fn,
    pair_allowlist: set[tuple[str, str]] | None = None,
    task_jacobians: list[tuple[np.ndarray, float]] | None = None,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """实验性双臂 OSCBF safety filter：环境和 inter-arm 约束统一求解。

    联合空间维度始终由 ``2 * ACTION_DIM`` 推导，不能假设固定关节数。
    """
    arm_dim = ACTION_DIM
    dq_left_nom = np.asarray(dq_left_nom, dtype=np.float64).reshape(arm_dim)
    dq_right_nom = np.asarray(dq_right_nom, dtype=np.float64).reshape(arm_dim)
    dq_nom_dual = np.concatenate([dq_left_nom, dq_right_nom])

    info: dict = {
        "dual_cbf_active": False,
        "dual_cbf_feasible": True,
        "dual_cbf_projected": False,
        "h_L_env_min": float("inf"),
        "h_R_env_min": float("inf"),
        "h_LR_min": float("inf"),
        "dq_left_cbf_norm": 0.0,
        "dq_right_cbf_norm": 0.0,
        "dq_dual_nom_norm": float(np.linalg.norm(dq_nom_dual)),
        "n_constraints": 0,
        "n_left_env_constraints": 0,
        "n_right_env_constraints": 0,
        "n_interarm_constraints": 0,
    }

    left_env, left_info = build_environment_constraints_for_arm(
        model,
        data,
        left_ids,
        dq_left_nom,
        cfg.env,
        left_monitors,
        obstacles,
        left_tcp_pose_fn,
    )
    right_env, right_info = build_environment_constraints_for_arm(
        model,
        data,
        right_ids,
        dq_right_nom,
        cfg.env,
        right_monitors,
        obstacles,
        right_tcp_pose_fn,
    )

    dual_constraints: list[CbfConstraint] = []
    dual_constraints.extend(
        lift_arm_constraint_to_dual(c, side="left", arm_dim=arm_dim)
        for c in left_env
    )
    dual_constraints.extend(
        lift_arm_constraint_to_dual(c, side="right", arm_dim=arm_dim)
        for c in right_env
    )

    left_capsules = [m for m in left_monitors if isinstance(m, CapsuleMonitor)]
    right_capsules = [m for m in right_monitors if isinstance(m, CapsuleMonitor)]
    inter_arm, inter_info = build_inter_arm_constraints_from_capsules(
        model,
        data,
        left_ids,
        right_ids,
        left_capsules,
        right_capsules,
        dq_nom_dual,
        cfg,
        pair_allowlist=pair_allowlist,
    )
    dual_constraints.extend(inter_arm)

    a_ineq, b_total, b_delta = stack_cbf_constraints(
        dual_constraints,
        action_dim=2 * arm_dim,
    )
    info["h_L_env_min"] = float(left_info.get("h_min", float("inf")))
    info["h_R_env_min"] = float(right_info.get("h_min", float("inf")))
    info["h_LR_min"] = float(inter_info.get("h_LR_min", float("inf")))
    info["distance_LR_min"] = float(inter_info.get("distance_LR_min", float("inf")))
    info["worst_left_env_monitor"] = str(left_info.get("worst_monitor", ""))
    info["worst_left_env_obstacle"] = str(left_info.get("worst_obstacle", ""))
    info["worst_right_env_monitor"] = str(right_info.get("worst_monitor", ""))
    info["worst_right_env_obstacle"] = str(right_info.get("worst_obstacle", ""))
    info["worst_left_link"] = str(inter_info.get("worst_left_link", ""))
    info["worst_right_link"] = str(inter_info.get("worst_right_link", ""))
    info["n_left_env_constraints"] = int(left_info.get("n_constraints", 0))
    info["n_right_env_constraints"] = int(right_info.get("n_constraints", 0))
    info["n_interarm_constraints"] = int(
        inter_info.get("n_interarm_constraints", 0)
    )
    info["n_constraints"] = int(a_ineq.shape[0])

    if a_ineq.shape[0] == 0:
        z = np.zeros(arm_dim, dtype=np.float64)
        return z, z, info

    info["dual_cbf_active"] = True
    lb_cbf, ub_cbf = _dq_cbf_bounds(dq_nom_dual, cfg.dq_max)
    if cfg.frozen_joint_mask is not None:
        frozen = np.asarray(cfg.frozen_joint_mask, dtype=bool).reshape(2 * arm_dim)
        lb_cbf[frozen] = -dq_nom_dual[frozen]
        ub_cbf[frozen] = -dq_nom_dual[frozen]

    h_mat = make_task_preserving_hessian(
        action_dim=2 * arm_dim,
        task_jacobians=task_jacobians,
    )
    dq_cbf_dual, ok = _solve_qp_min_correction(
        a_ineq,
        b_delta,
        lb_cbf,
        ub_cbf,
        h_mat=h_mat,
    )

    if not ok or dq_cbf_dual is None:
        dq_total, proj_ok = _project_dq_total(
            dq_nom_dual,
            a_ineq,
            b_total,
            cfg.dq_max,
        )
        dq_cbf_dual = dq_total - dq_nom_dual
        info["dual_cbf_feasible"] = bool(proj_ok)
        info["dual_cbf_projected"] = True
    else:
        dq_total = dq_nom_dual + dq_cbf_dual
        if not np.all(a_ineq @ dq_total >= b_total - 1e-5):
            dq_total, proj_ok = _project_dq_total(
                dq_nom_dual,
                a_ineq,
                b_total,
                cfg.dq_max,
            )
            dq_cbf_dual = dq_total - dq_nom_dual
            info["dual_cbf_feasible"] = bool(proj_ok)
            info["dual_cbf_projected"] = True

    dq_cbf_dual = np.clip(dq_cbf_dual, lb_cbf, ub_cbf)
    dq_total = np.clip(dq_nom_dual + dq_cbf_dual, -cfg.dq_max, cfg.dq_max)
    dq_cbf_dual = dq_total - dq_nom_dual
    dq_left_cbf = dq_cbf_dual[:arm_dim]
    dq_right_cbf = dq_cbf_dual[arm_dim:]
    info["dq_left_cbf_norm"] = float(np.linalg.norm(dq_left_cbf))
    info["dq_right_cbf_norm"] = float(np.linalg.norm(dq_right_cbf))
    info["dq_dual_cbf_norm"] = float(np.linalg.norm(dq_cbf_dual))
    info["dq_dual_total_norm"] = float(np.linalg.norm(dq_total))
    return dq_left_cbf, dq_right_cbf, info


def _solve_qp_min_correction(
    a_ineq: np.ndarray,
    b_ineq: np.ndarray,
    lb: np.ndarray,
    ub: np.ndarray,
    h_mat: np.ndarray | None = None,
) -> tuple[np.ndarray | None, bool]:
    """min ½‖dq_cbf‖²  s.t. A·dq_cbf ≥ b, box（贴近 dq_nom 的最小修正）。"""
    n = int(lb.shape[0])
    if h_mat is None:
        h_mat = np.eye(n, dtype=np.float64)
    else:
        h_mat = np.asarray(h_mat, dtype=np.float64).reshape(n, n)

    if a_ineq.shape[0] == 0:
        return np.zeros(n, dtype=np.float64), True

    if _HAS_SCIPY:
        def objective(x: np.ndarray) -> float:
            return 0.5 * float(x @ h_mat @ x)

        constraints = []
        for i in range(a_ineq.shape[0]):
            ai = a_ineq[i]
            bi = float(b_ineq[i])
            constraints.append(
                {"type": "ineq", "fun": lambda x, ai=ai, bi=bi: float(ai @ x - bi)}
            )

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
    monitors: list[Monitor],
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
        info["cbf_worst_obs_step"] = float(worst.get("obs_step", 0.0))
        info["cbf_worst_obs_speed"] = float(worst.get("obs_speed", 0.0))
        info["cbf_worst_capsule_t"] = float(worst.get("capsule_t", 0.0))
        rhs_worst = float(worst.get("obs_step", 0.0)) - cfg.gamma * float(worst["h"])
        info["nom_violation"] = float(rhs_worst - float(worst["grad_q"] @ dq_nom))

    need_active = h_min < cfg.activate_margin
    if not need_active:
        for rec in records:
            if float(rec["h"]) >= cfg.activate_margin:
                continue
            g = np.asarray(rec["grad_q"], dtype=np.float64)
            rhs = float(rec.get("obs_step", 0.0)) - cfg.gamma * float(rec["h"])
            if float(g @ dq_nom) < rhs - 1e-9:
                need_active = True
                break

    if not need_active:
        return np.zeros(ACTION_DIM, dtype=np.float64), info

    info["cbf_active"] = True
    a_ineq, b_total, b_cbf = _build_constraints(records, cfg, dq_nom)
    info["n_constraints"] = int(a_ineq.shape[0])

    lb_cbf, ub_cbf = _dq_cbf_bounds(dq_nom, cfg.dq_max)
    frozen = np.asarray(cfg.frozen_joint_mask, dtype=bool).reshape(ACTION_DIM)
    lb_cbf[frozen] = -dq_nom[frozen]
    ub_cbf[frozen] = -dq_nom[frozen]
    j_tcp = None
    if str(cfg.qp_metric).strip().lower() == "task_preserving":
        _, j_tcp = tcp_pos_and_jacobian(model, data, ids, tcp_pose_fn)
    h_mat = make_qp_metric_hessian(cfg, ACTION_DIM, tcp_jacobian=j_tcp)
    dq_cbf, ok = _solve_qp_min_correction(
        a_ineq,
        b_cbf,
        lb_cbf,
        ub_cbf,
        h_mat=h_mat,
    )

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
        "worst_obs_step": float(info.get("cbf_worst_obs_step", 0.0)),
        "worst_obs_speed": float(info.get("cbf_worst_obs_speed", 0.0)),
        "guided_target_active": bool(info.get("guided_target_active", False)),
        "guided_target_dynamic": bool(info.get("guided_target_dynamic", False)),
        "guided_target_dynamic_params": bool(info.get("guided_target_dynamic_params", False)),
        "guided_target_side": float(info.get("guided_target_side", 0.0)),
        "guided_target_memory_side": float(info.get("guided_target_memory_side", 0.0)),
        "guided_target_miss_count": int(info.get("guided_target_miss_count", 0)),
        "guided_target_closing_speed": float(info.get("guided_target_closing_speed", 0.0)),
        "guided_target_clearance": float(info.get("guided_target_clearance", 0.0)),
        "guided_target_forward": float(info.get("guided_target_forward", 0.0)),
    }
