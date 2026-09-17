#!/usr/bin/env python3
"""SO-100 Plus Reach：MuJoCo 推理（默认 C：bank-start best_agent）。

注意：本目录名为 mujoco，与官方库同名，因此本脚本用 importlib 加载本地模块。

  cd soarm100sim && python mujoco/play.py
  python mujoco/play.py --headless --episodes 20
  python mujoco/play.py --episodes 5 --speed 0.5   # 半速看过程
  python mujoco/play.py --episodes 1 --hold-home 30   # 先停 30s 看 3D 里相机装位
  python mujoco/play.py --enable-cbf --verbose     # 开启全身 CBF-QP 避障
  python mujoco/play.py --enable-cbf --obstacle-source vision --vision-debug  # 视觉障碍
  python mujoco/play.py --enable-cbf --cbf-log log/runtime/mujoco_cbf.jsonl
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np

_THIS = Path(__file__).resolve().parent
_RL_ROOT = _THIS.parent / "rl"
if str(_RL_ROOT) not in sys.path:
    sys.path.insert(0, str(_RL_ROOT))


def _load_local(mod_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


_c = _load_local("so100_mj_constants", _THIS / "constants.py")
_pol = _load_local("so100_mj_policy", _THIS / "policy.py")
_rt = _load_local("so100_mj_runtime", _THIS / "runtime.py")
_cbf = _load_local("so100_mj_cbf", _THIS / "cbf.py")
_dyn = _load_local("so100_mj_dynamic", _THIS / "dynamic.py")
_ag = _load_local("so100_mj_anygrasp_bridge", _THIS / "anygrasp_bridge.py")
_track = _load_local("so100_mj_grasp_tracking", _THIS / "grasp_tracking.py")

DEFAULT_CHECKPOINT = _c.DEFAULT_CHECKPOINT
DEFAULT_MJCF = _c.DEFAULT_MJCF
DEFAULT_MJCF_NOROD = _c.DEFAULT_MJCF_NOROD
DEFAULT_MJCF_GRASP_OBSTACLE = DEFAULT_MJCF_NOROD.with_name("scene_plus_grasp_obstacle.xml")
DEFAULT_NPZ_TEST = _c.DEFAULT_NPZ_TEST
DEFAULT_NPZ_TRAIN = _c.DEFAULT_NPZ_TRAIN
SIM_DT = _c.SIM_DT
DECIMATION = _c.DECIMATION
ACTION_SCALE = _c.ACTION_SCALE
ACTION_FILTER_TAU = _c.ACTION_FILTER_TAU
ACTION_DIM = _c.ACTION_DIM
EPISODE_LENGTH_S = _c.EPISODE_LENGTH_S
CBF_D_SAFE = _c.CBF_D_SAFE
CBF_GAMMA = _c.CBF_GAMMA
CBF_LAMBDA = _c.CBF_LAMBDA
CBF_ACTIVATE_MARGIN = _c.CBF_ACTIVATE_MARGIN
CBF_FILTER_TAU = _c.CBF_FILTER_TAU
SCENE_DEPTH_CAM = _c.SCENE_DEPTH_CAM
WRIST_RGB_CAM = _c.WRIST_RGB_CAM
GRIPPER_BODY = _c.GRIPPER_BODY
BASE_BODY = _c.BASE_BODY
CbfConfig = _cbf.CbfConfig
cbf_step_log_record = _cbf.cbf_step_log_record
MotionSpec = _dyn.MotionSpec
AnyGraspBridge = _ag.AnyGraspBridge
AnyGraspConfig = _ag.AnyGraspConfig
make_grasp_tracker = _track.make_grasp_tracker


@dataclass
class CbfEpisodeStats:
    steps: int = 0
    active_steps: int = 0
    infeasible_steps: int = 0
    correction_steps: int = 0
    h_min_ep: float = float("inf")
    max_dq_cbf: float = 0.0

    def update(self, info: dict) -> None:
        self.steps += 1
        h = float(info.get("h_min", float("inf")))
        self.h_min_ep = min(self.h_min_ep, h)
        if info.get("cbf_active"):
            self.active_steps += 1
        if info.get("cbf_active") and not info.get("cbf_feasible", True):
            self.infeasible_steps += 1
        dq_cbf = float(info.get("dq_cbf_norm", 0.0))
        if dq_cbf > 1e-6:
            self.correction_steps += 1
            self.max_dq_cbf = max(self.max_dq_cbf, dq_cbf)

    def summary_line(self, ep: int) -> str:
        h_mm = self.h_min_ep * 1000.0 if math.isfinite(self.h_min_ep) else float("nan")
        return (
            f"[ep {ep:03d}][cbf] steps={self.steps}  active={self.active_steps}  "
            f"infeas={self.infeasible_steps}  corrected={self.correction_steps}  "
            f"h_min_ep={h_mm:.1f}mm  max|dq_cbf|={self.max_dq_cbf:.4f}"
        )
SkrlGaussianPolicy = _pol.SkrlGaussianPolicy
ReachStepper = _rt.ReachStepper
load_target_bank = _rt.load_target_bank
reset_home = _rt.reset_home
resolve_robot_ids = _rt.resolve_robot_ids
set_ctrl = _rt.set_ctrl
tcp_pose_w = _rt.tcp_pose_w
joint_pos = _rt.joint_pos
cartesian_pose_servo_target = _rt.cartesian_pose_servo_target


def _ori_deg(quat_dot: float) -> float:
    d = min(1.0, max(0.0, abs(quat_dot)))
    return float(2.0 * math.degrees(math.acos(d)))


def _quat_angle_deg(q_a: np.ndarray, q_b: np.ndarray) -> float:
    a = np.asarray(q_a, dtype=np.float64).reshape(4)
    b = np.asarray(q_b, dtype=np.float64).reshape(4)
    a /= max(float(np.linalg.norm(a)), 1e-12)
    b /= max(float(np.linalg.norm(b)), 1e-12)
    return _ori_deg(float(np.dot(a, b)))


def _quat_conjugate_wxyz(q: np.ndarray) -> np.ndarray:
    quat = np.asarray(q, dtype=np.float64).reshape(4)
    return np.array([quat[0], -quat[1], -quat[2], -quat[3]], dtype=np.float64)


def _quat_multiply_wxyz(q_a: np.ndarray, q_b: np.ndarray) -> np.ndarray:
    a = np.asarray(q_a, dtype=np.float64).reshape(4)
    b = np.asarray(q_b, dtype=np.float64).reshape(4)
    out = np.zeros(4, dtype=np.float64)
    mujoco.mju_mulQuat(out, a, b)
    out /= max(float(np.linalg.norm(out)), 1e-12)
    return out


def _quat_to_rotvec_wxyz(q: np.ndarray) -> np.ndarray:
    quat = np.asarray(q, dtype=np.float64).reshape(4)
    quat /= max(float(np.linalg.norm(quat)), 1e-12)
    if quat[0] < 0.0:
        quat = -quat
    v = quat[1:]
    s = float(np.linalg.norm(v))
    if s < 1e-10:
        return 2.0 * v
    angle = 2.0 * math.atan2(s, float(quat[0]))
    return v * (angle / s)


def _quat_to_rotmat_wxyz(q: np.ndarray) -> np.ndarray:
    quat = np.asarray(q, dtype=np.float64).reshape(4)
    quat /= max(float(np.linalg.norm(quat)), 1e-12)
    mat = np.zeros(9, dtype=np.float64)
    mujoco.mju_quat2Mat(mat, quat)
    return mat.reshape(3, 3)


def _axis_angle_deg(a: np.ndarray, b: np.ndarray) -> float:
    va = np.asarray(a, dtype=np.float64).reshape(3)
    vb = np.asarray(b, dtype=np.float64).reshape(3)
    va /= max(float(np.linalg.norm(va)), 1e-12)
    vb /= max(float(np.linalg.norm(vb)), 1e-12)
    d = min(1.0, max(-1.0, float(np.dot(va, vb))))
    return float(math.degrees(math.acos(d)))


def _axis_alignment_errors_deg(tcp_quat: np.ndarray, desired_axis: np.ndarray) -> dict[str, float]:
    if not np.all(np.isfinite(tcp_quat)) or not np.all(np.isfinite(desired_axis)):
        return {name: float("nan") for name in ("+x", "-x", "+y", "-y", "+z", "-z")}
    R = _quat_to_rotmat_wxyz(tcp_quat)
    axes = {
        "+x": R[:, 0],
        "-x": -R[:, 0],
        "+y": R[:, 1],
        "-y": -R[:, 1],
        "+z": R[:, 2],
        "-z": -R[:, 2],
    }
    return {name: _axis_angle_deg(axis, desired_axis) for name, axis in axes.items()}


def _format_axis_alignment(errors: dict[str, float]) -> str:
    parts = []
    for name in ("+x", "-x", "+y", "-y", "+z", "-z"):
        val = float(errors.get(name, float("nan")))
        parts.append(f"{name}:{val:.1f}")
    best_name, best_val = min(
        errors.items(),
        key=lambda kv: float(kv[1]) if math.isfinite(float(kv[1])) else float("inf"),
    )
    return " ".join(parts) + f" best={best_name}:{float(best_val):.1f}"


def _axis_text(v: np.ndarray) -> str:
    a = np.asarray(v, dtype=np.float64).reshape(3)
    return f"({a[0]:+.2f},{a[1]:+.2f},{a[2]:+.2f})"


def _grasp_pose_axis_debug(
    tcp_quat: np.ndarray,
    desired_quat: np.ndarray,
    desired_approach: np.ndarray,
    approach_local_axis: np.ndarray,
    *,
    model: mujoco.MjModel | None = None,
    ids=None,
    q: np.ndarray | None = None,
) -> dict:
    local_app = np.asarray(approach_local_axis, dtype=np.float64).reshape(3)
    local_app /= max(float(np.linalg.norm(local_app)), 1e-12)
    desired_app = np.asarray(desired_approach, dtype=np.float64).reshape(3)
    if np.all(np.isfinite(desired_app)):
        desired_app /= max(float(np.linalg.norm(desired_app)), 1e-12)

    tcp_q = np.asarray(tcp_quat, dtype=np.float64).reshape(4)
    des_q = np.asarray(desired_quat, dtype=np.float64).reshape(4)
    R_tcp = _quat_to_rotmat_wxyz(tcp_q) if np.all(np.isfinite(tcp_q)) else np.full((3, 3), np.nan)
    R_des = _quat_to_rotmat_wxyz(des_q) if np.all(np.isfinite(des_q)) else np.full((3, 3), np.nan)

    tcp_app = R_tcp @ local_app if np.all(np.isfinite(R_tcp)) else np.full(3, np.nan)
    desired_closing = R_des[:, 0] if np.all(np.isfinite(R_des)) else np.full(3, np.nan)
    tcp_closing = R_tcp[:, 0] if np.all(np.isfinite(R_tcp)) else np.full(3, np.nan)
    desired_palm = R_des[:, 1] if np.all(np.isfinite(R_des)) else np.full(3, np.nan)
    tcp_palm = R_tcp[:, 1] if np.all(np.isfinite(R_tcp)) else np.full(3, np.nan)

    gripper_closing = np.full(3, np.nan)
    gripper_palm = np.full(3, np.nan)
    gripper_closing_axes_deg = {
        "+x": float("nan"),
        "-x": float("nan"),
        "+y": float("nan"),
        "-y": float("nan"),
        "+z": float("nan"),
        "-z": float("nan"),
    }
    gripper_closing_best_axis = ""
    gripper_closing_best_deg = float("nan")
    if model is not None and ids is not None and q is not None:
        tmp = mujoco.MjData(model)
        _set_robot_qpos(model, tmp, ids, q)
        R_gripper = np.asarray(tmp.xmat[int(ids.gripper_body)], dtype=np.float64).reshape(3, 3)
        gripper_closing = R_gripper[:, 0]
        gripper_palm = R_gripper[:, 1]
        gripper_axis_vecs = {
            "+x": R_gripper[:, 0],
            "-x": -R_gripper[:, 0],
            "+y": R_gripper[:, 1],
            "-y": -R_gripper[:, 1],
            "+z": R_gripper[:, 2],
            "-z": -R_gripper[:, 2],
        }
        if np.all(np.isfinite(desired_closing)):
            gripper_closing_axes_deg = {
                k: float(_axis_angle_deg(v, desired_closing)) for k, v in gripper_axis_vecs.items()
            }
            gripper_closing_best_axis, gripper_closing_best_deg = min(
                gripper_closing_axes_deg.items(),
                key=lambda kv: float(kv[1]) if math.isfinite(float(kv[1])) else float("inf"),
            )

    return {
        "desired_approach_axis": _arr(desired_app),
        "actual_approach_axis": _arr(tcp_app),
        "approach_err_deg": float(_axis_angle_deg(tcp_app, desired_app))
        if np.all(np.isfinite(tcp_app)) and np.all(np.isfinite(desired_app))
        else float("nan"),
        "desired_closing_axis": _arr(desired_closing),
        "tcp_closing_axis": _arr(tcp_closing),
        "closing_axis_err_deg": float(_axis_angle_deg(tcp_closing, desired_closing))
        if np.all(np.isfinite(tcp_closing)) and np.all(np.isfinite(desired_closing))
        else float("nan"),
        "desired_palm_axis": _arr(desired_palm),
        "tcp_palm_axis": _arr(tcp_palm),
        "palm_axis_err_deg": float(_axis_angle_deg(tcp_palm, desired_palm))
        if np.all(np.isfinite(tcp_palm)) and np.all(np.isfinite(desired_palm))
        else float("nan"),
        "gripper_body_closing_axis": _arr(gripper_closing),
        "gripper_body_closing_err_deg": float(_axis_angle_deg(gripper_closing, desired_closing))
        if np.all(np.isfinite(gripper_closing)) and np.all(np.isfinite(desired_closing))
        else float("nan"),
        "gripper_body_closing_axis_alignment_deg": {k: float(v) for k, v in gripper_closing_axes_deg.items()},
        "gripper_body_closing_axis_best": str(gripper_closing_best_axis),
        "gripper_body_closing_axis_best_deg": float(gripper_closing_best_deg),
        "gripper_body_palm_axis": _arr(gripper_palm),
        "gripper_body_palm_err_deg": float(_axis_angle_deg(gripper_palm, desired_palm))
        if np.all(np.isfinite(gripper_palm)) and np.all(np.isfinite(desired_palm))
        else float("nan"),
    }


def _format_grasp_axis_debug(dbg: dict) -> str:
    return (
        f"closing_err={float(dbg.get('closing_axis_err_deg', float('nan'))):.1f}deg "
        f"palm_err={float(dbg.get('palm_axis_err_deg', float('nan'))):.1f}deg "
        f"tcp_close={_axis_text(np.asarray(dbg.get('tcp_closing_axis', [float('nan')] * 3), dtype=np.float64))} "
        f"desired_close={_axis_text(np.asarray(dbg.get('desired_closing_axis', [float('nan')] * 3), dtype=np.float64))} "
        f"gripper_close_err={float(dbg.get('gripper_body_closing_err_deg', float('nan'))):.1f}deg "
        f"gripper_best={dbg.get('gripper_body_closing_axis_best', '')}:"
        f"{float(dbg.get('gripper_body_closing_axis_best_deg', float('nan'))):.1f}deg"
    )


def _scene_add_sphere(scn, pos: np.ndarray, radius: float, rgba: np.ndarray) -> None:
    if scn.ngeom >= len(scn.geoms):
        return
    geom = scn.geoms[scn.ngeom]
    mujoco.mjv_initGeom(
        geom,
        mujoco.mjtGeom.mjGEOM_SPHERE,
        np.array([float(radius), 0.0, 0.0], dtype=np.float64),
        np.asarray(pos, dtype=np.float64),
        np.eye(3, dtype=np.float64).reshape(9),
        np.asarray(rgba, dtype=np.float32),
    )
    scn.ngeom += 1


def _scene_add_arrow(scn, start: np.ndarray, end: np.ndarray, width: float, rgba: np.ndarray) -> None:
    if scn.ngeom >= len(scn.geoms):
        return
    geom = scn.geoms[scn.ngeom]
    try:
        mujoco.mjv_connector(
            geom,
            mujoco.mjtGeom.mjGEOM_ARROW,
            float(width),
            np.asarray(start, dtype=np.float64),
            np.asarray(end, dtype=np.float64),
        )
        geom.rgba[:] = np.asarray(rgba, dtype=np.float32)
        scn.ngeom += 1
    except Exception:
        _scene_add_sphere(scn, end, width * 2.0, rgba)


def _draw_overlays(
    viewer,
    target_pos: np.ndarray,
    *,
    draw_target: bool = True,
    grasp_candidates=None,
    selected_grasp=None,
    pregrasp_pos: np.ndarray | None = None,
    grasp_pos: np.ndarray | None = None,
) -> None:
    """在 passive viewer 上画目标球和 AnyGrasp 候选。"""
    try:
        with viewer.lock():
            scn = viewer.user_scn
            scn.ngeom = 0
            if bool(draw_target):
                _scene_add_sphere(
                    scn,
                    np.asarray(target_pos, dtype=np.float64),
                    0.015,
                    np.array([1.0, 0.15, 0.15, 0.95], dtype=np.float32),
                )
            if grasp_candidates is not None:
                for cand in list(grasp_candidates)[:12]:
                    pos = np.asarray(cand.pos_world, dtype=np.float64).reshape(3)
                    app = np.asarray(cand.approach_world, dtype=np.float64).reshape(3)
                    app /= max(float(np.linalg.norm(app)), 1e-12)
                    _scene_add_sphere(scn, pos, 0.004, np.array([1.0, 0.85, 0.05, 0.85], dtype=np.float32))
                    _scene_add_arrow(
                        scn,
                        pos - 0.025 * app,
                        pos + 0.055 * app,
                        0.0025,
                        np.array([1.0, 0.85, 0.05, 0.75], dtype=np.float32),
                )
            if selected_grasp is not None:
                pos = np.asarray(selected_grasp.pos_world, dtype=np.float64).reshape(3)
                app = np.asarray(selected_grasp.approach_world, dtype=np.float64).reshape(3)
                app /= max(float(np.linalg.norm(app)), 1e-12)
                _scene_add_sphere(scn, pos, 0.007, np.array([0.0, 1.0, 0.1, 1.0], dtype=np.float32))
                _scene_add_arrow(
                    scn,
                    pos - 0.035 * app,
                    pos + 0.075 * app,
                    0.005,
                    np.array([0.0, 1.0, 0.1, 0.95], dtype=np.float32),
                )
            if pregrasp_pos is not None:
                _scene_add_sphere(scn, pregrasp_pos, 0.008, np.array([0.0, 0.7, 1.0, 0.9], dtype=np.float32))
            if grasp_pos is not None:
                _scene_add_sphere(scn, grasp_pos, 0.006, np.array([0.0, 1.0, 0.1, 0.95], dtype=np.float32))
    except Exception:
        pass


def _compute_with_soft_cbf(stepper, model, data, target_pos, target_quat, args):
    cfg = getattr(stepper, "cbf_cfg", None)
    if cfg is None:
        return stepper.compute_targets(model, data, target_pos, target_quat)
    orig = (
        float(cfg.d_safe),
        float(cfg.gamma),
        float(cfg.activate_margin),
        float(cfg.lambda_cbf),
    )
    cfg.d_safe = float(args.settle_cbf_d_safe)
    cfg.gamma = float(args.settle_cbf_gamma)
    cfg.activate_margin = float(args.settle_cbf_activate_margin)
    cfg.lambda_cbf = float(args.settle_cbf_lambda)
    try:
        return stepper.compute_targets(model, data, target_pos, target_quat)
    finally:
        cfg.d_safe, cfg.gamma, cfg.activate_margin, cfg.lambda_cbf = orig


def _arr(x) -> list[float]:
    return np.asarray(x, dtype=np.float64).reshape(-1).tolist()


def _append_jsonl(path: str | Path | None, rec: dict) -> None:
    if not path:
        return
    p = Path(path).expanduser().resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _quat_wxyz_from_rotmat(R: np.ndarray) -> np.ndarray:
    mat = np.asarray(R, dtype=np.float64).reshape(3, 3)
    q = np.zeros(4, dtype=np.float64)
    mujoco.mju_mat2Quat(q, mat.reshape(9))
    q /= max(float(np.linalg.norm(q)), 1e-12)
    if q[0] < 0.0:
        q = -q
    return q


def _orthonormalize_axes(x_axis: np.ndarray, z_axis: np.ndarray) -> np.ndarray:
    x = np.asarray(x_axis, dtype=np.float64).reshape(3)
    z = np.asarray(z_axis, dtype=np.float64).reshape(3)
    z /= max(float(np.linalg.norm(z)), 1e-12)
    x = x - float(np.dot(x, z)) * z
    if float(np.linalg.norm(x)) < 1e-8:
        fallback = np.array([1.0, 0.0, 0.0], dtype=np.float64)
        if abs(float(np.dot(fallback, z))) > 0.9:
            fallback = np.array([0.0, 1.0, 0.0], dtype=np.float64)
        x = fallback - float(np.dot(fallback, z)) * z
    x /= max(float(np.linalg.norm(x)), 1e-12)
    y = np.cross(z, x)
    y /= max(float(np.linalg.norm(y)), 1e-12)
    z = np.cross(x, y)
    z /= max(float(np.linalg.norm(z)), 1e-12)
    return np.column_stack([x, y, z])


def _basis_from_axis_and_preferred(axis: np.ndarray, preferred: np.ndarray) -> np.ndarray:
    z = np.asarray(axis, dtype=np.float64).reshape(3)
    z /= max(float(np.linalg.norm(z)), 1e-12)
    x = np.asarray(preferred, dtype=np.float64).reshape(3)
    x = x - float(np.dot(x, z)) * z
    if float(np.linalg.norm(x)) < 1e-8:
        x = np.array([1.0, 0.0, 0.0], dtype=np.float64)
        if abs(float(np.dot(x, z))) > 0.9:
            x = np.array([0.0, 1.0, 0.0], dtype=np.float64)
        x = x - float(np.dot(x, z)) * z
    x /= max(float(np.linalg.norm(x)), 1e-12)
    y = np.cross(z, x)
    y /= max(float(np.linalg.norm(y)), 1e-12)
    return np.column_stack([x, y, z])


def _rot_from_local_axis_alignment(
    local_axis: np.ndarray,
    desired_axis_world: np.ndarray,
    *,
    local_preferred: np.ndarray,
    desired_preferred_world: np.ndarray,
) -> np.ndarray:
    local_basis = _basis_from_axis_and_preferred(local_axis, local_preferred)
    world_basis = _basis_from_axis_and_preferred(desired_axis_world, desired_preferred_world)
    return world_basis @ local_basis.T


def _preferred_closing_axis_world(approach: np.ndarray, raw_closing: np.ndarray) -> np.ndarray:
    app = np.asarray(approach, dtype=np.float64).reshape(3)
    app /= max(float(np.linalg.norm(app)), 1e-12)
    raw = np.asarray(raw_closing, dtype=np.float64).reshape(3)
    raw /= max(float(np.linalg.norm(raw)), 1e-12)
    return raw


def _raw_axis_from_rot(R: np.ndarray, spec: str) -> np.ndarray:
    R = np.asarray(R, dtype=np.float64).reshape(3, 3)
    s = str(spec).strip().lower()
    sign = 1.0
    if s.startswith("-"):
        sign = -1.0
        s = s[1:]
    elif s.startswith("+"):
        s = s[1:]
    idx_map = {"x": 0, "y": 1, "z": 2}
    if s not in idx_map:
        raise ValueError(f"unknown AnyGrasp raw axis spec: {spec!r}")
    axis = sign * R[:, idx_map[s]]
    axis /= max(float(np.linalg.norm(axis)), 1e-12)
    return axis


def _raw_axis_label_for_print(spec: str) -> str:
    s = str(spec).strip().lower()
    if s.startswith("+"):
        s = s[1:]
    return s


def _tcp_rot_from_anygrasp_rot(
    R_any_world: np.ndarray,
    approach_local_axis: np.ndarray | None = None,
    raw_approach_axis: str = "x",
) -> tuple[np.ndarray, np.ndarray]:
    """Map GraspNet/AnyGrasp gripper frame to this project's pinch TCP frame.

    The default AnyGrasp/GraspNet interpretation uses local x as gripper
    depth/approach and local y as gripper width. Some SDK visualizations expose
    a different convention, so raw_approach_axis is configurable for diagnosis.
    The trained policy TCP uses local x as the closing axis between fingertips
    and local z as the approach axis.
    """
    Rg = np.asarray(R_any_world, dtype=np.float64).reshape(3, 3)
    approach = _raw_axis_from_rot(Rg, raw_approach_axis)
    closing = _preferred_closing_axis_world(approach, Rg[:, 1])
    if approach_local_axis is None:
        R_tcp = _orthonormalize_axes(closing, approach)
        tcp_approach = R_tcp[:, 2]
    else:
        local_axis = np.asarray(approach_local_axis, dtype=np.float64).reshape(3)
        local_axis /= max(float(np.linalg.norm(local_axis)), 1e-12)
        R_tcp = _rot_from_local_axis_alignment(
            local_axis,
            approach,
            local_preferred=np.array([1.0, 0.0, 0.0], dtype=np.float64),
            desired_preferred_world=closing,
        )
        tcp_approach = R_tcp @ local_axis
    tcp_approach /= max(float(np.linalg.norm(tcp_approach)), 1e-12)
    return R_tcp, tcp_approach


def _body_id_or_none(model: mujoco.MjModel, name: str) -> int | None:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
    return int(bid) if bid >= 0 else None


def _geom_radius_or_default(model: mujoco.MjModel, name: str, default: float) -> float:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, name)
    if gid < 0:
        return float(default)
    return float(model.geom_size[int(gid)][0])


def _geom_floor_center_z_or_default(model: mujoco.MjModel, name: str, default: float) -> float:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, name)
    if gid < 0:
        return float(default)
    gtype = int(model.geom_type[int(gid)])
    size = np.asarray(model.geom_size[int(gid)], dtype=np.float64)
    if gtype == int(mujoco.mjtGeom.mjGEOM_SPHERE):
        return float(size[0])
    if gtype == int(mujoco.mjtGeom.mjGEOM_BOX):
        return float(size[2])
    if gtype in (int(mujoco.mjtGeom.mjGEOM_CYLINDER), int(mujoco.mjtGeom.mjGEOM_CAPSULE)):
        return float(size[1] + (size[0] if gtype == int(mujoco.mjtGeom.mjGEOM_CAPSULE) else 0.0))
    return float(default)


_GRASP_TARGET_OBJECTS = {
    "cube": ("target_object", "target_object_geom"),
    "bottle": ("target_bottle", "target_bottle_geom"),
    "sphere": ("target_sphere", "target_sphere_geom"),
}


def _select_grasp_target_object(args) -> None:
    obj = str(args.grasp_target_object).strip().lower()
    if obj == "custom":
        return
    if obj not in _GRASP_TARGET_OBJECTS:
        raise ValueError(f"unknown grasp target object: {args.grasp_target_object!r}")
    body, geom = _GRASP_TARGET_OBJECTS[obj]
    args.target_body = body
    args.target_geom = geom


def _configure_grasp_target_visibility(model: mujoco.MjModel, selected_geom_name: str) -> None:
    selected = str(selected_geom_name)
    for _, geom_name in _GRASP_TARGET_OBJECTS.values():
        gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, geom_name)
        if gid < 0:
            continue
        if geom_name == selected:
            model.geom_contype[int(gid)] = 1
            model.geom_conaffinity[int(gid)] = 1
            model.geom_rgba[int(gid)] = np.array([1.0, 0.05, 0.05, 1.0], dtype=np.float32)
        else:
            model.geom_contype[int(gid)] = 0
            model.geom_conaffinity[int(gid)] = 0
            model.geom_rgba[int(gid)] = np.array([1.0, 0.05, 0.05, 0.0], dtype=np.float32)


def _park_inactive_grasp_targets(model: mujoco.MjModel, data: mujoco.MjData, selected_body_name: str) -> None:
    selected = str(selected_body_name)
    for body_name, _ in _GRASP_TARGET_OBJECTS.values():
        if body_name == selected:
            continue
        _set_static_body_pos(model, data, body_name, np.array([0.0, 0.0, -1.0], dtype=np.float64))


def _geom_contact_count(model: mujoco.MjModel, data: mujoco.MjData, geom_name: str) -> int:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, str(geom_name))
    if gid < 0:
        return 0
    count = 0
    for i in range(int(data.ncon)):
        con = data.contact[i]
        if int(con.geom1) == int(gid) or int(con.geom2) == int(gid):
            count += 1
    return count


def _body_descendant_ids(model: mujoco.MjModel, root_body_name: str) -> set[int]:
    root = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(root_body_name))
    if root < 0:
        return set()
    out = {int(root)}
    changed = True
    while changed:
        changed = False
        for bid in range(int(model.nbody)):
            if bid in out:
                continue
            parent = int(model.body_parentid[bid])
            if parent in out:
                out.add(int(bid))
                changed = True
    return out


def _geom_contact_count_with_body(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    geom_name: str,
    other_root_body_name: str,
) -> int:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, str(geom_name))
    if gid < 0:
        return 0
    bodies = _body_descendant_ids(model, str(other_root_body_name))
    if not bodies:
        return 0
    count = 0
    for i in range(int(data.ncon)):
        con = data.contact[i]
        g1 = int(con.geom1)
        g2 = int(con.geom2)
        if g1 == int(gid):
            other = g2
        elif g2 == int(gid):
            other = g1
        else:
            continue
        if int(model.geom_bodyid[other]) in bodies:
            count += 1
    return count


def _mj_name(model: mujoco.MjModel, obj_type, obj_id: int) -> str:
    if int(obj_id) < 0:
        return ""
    name = mujoco.mj_id2name(model, obj_type, int(obj_id))
    return str(name) if name is not None else ""


def _target_contact_pairs(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    target_geom_name: str,
    max_pairs: int = 12,
) -> list[dict]:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, str(target_geom_name))
    if gid < 0:
        return []
    pairs: list[dict] = []
    for i in range(int(data.ncon)):
        con = data.contact[i]
        g1 = int(con.geom1)
        g2 = int(con.geom2)
        if g1 == int(gid):
            other = g2
        elif g2 == int(gid):
            other = g1
        else:
            continue
        other_body = int(model.geom_bodyid[other])
        pairs.append(
            {
                "other_geom": _mj_name(model, mujoco.mjtObj.mjOBJ_GEOM, other),
                "other_body": _mj_name(model, mujoco.mjtObj.mjOBJ_BODY, other_body),
                "dist_m": float(con.dist),
                "normal_world": _arr(np.asarray(con.frame[:3], dtype=np.float64)),
            }
        )
        if len(pairs) >= int(max_pairs):
            break
    return pairs


def _set_static_body_pos(model: mujoco.MjModel, data: mujoco.MjData, body_name: str, pos: np.ndarray) -> None:
    bid = _body_id_or_none(model, body_name)
    if bid is None:
        return
    target = np.asarray(pos, dtype=np.float64).reshape(3)
    free_jid = -1
    for jid in range(int(model.njnt)):
        if int(model.jnt_bodyid[jid]) == int(bid) and int(model.jnt_type[jid]) == int(mujoco.mjtJoint.mjJNT_FREE):
            free_jid = int(jid)
            break
    if free_jid >= 0:
        qadr = int(model.jnt_qposadr[free_jid])
        dadr = int(model.jnt_dofadr[free_jid])
        data.qpos[qadr : qadr + 3] = target
        data.qpos[qadr + 3 : qadr + 7] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        data.qvel[dadr : dadr + 6] = 0.0
    else:
        model.body_pos[bid] = target
    mujoco.mj_forward(model, data)


def _load_joint_bank(npz_path: Path) -> np.ndarray | None:
    z = np.load(str(npz_path))
    if "joint_pos" not in z.files:
        return None
    joint_bank = np.asarray(z["joint_pos"], dtype=np.float64)
    if joint_bank.ndim != 2 or joint_bank.shape[1] < ACTION_DIM:
        return None
    return joint_bank[:, :ACTION_DIM].copy()


def _set_robot_qpos(model: mujoco.MjModel, data: mujoco.MjData, ids, q: np.ndarray) -> None:
    q_arr = np.asarray(q, dtype=np.float64).reshape(-1)
    if q_arr.shape[0] < len(ids.qpos_adr):
        raise ValueError(f"robot qpos needs {len(ids.qpos_adr)} joints, got {q_arr.shape[0]}")
    q_arr = q_arr[: len(ids.qpos_adr)].copy()
    q_arr = np.clip(q_arr, ids.q_low, ids.q_high)
    for i, adr in enumerate(ids.qpos_adr):
        data.qpos[int(adr)] = float(q_arr[i])
    for adr in ids.dof_adr:
        data.qvel[int(adr)] = 0.0
    set_ctrl(data, ids, q_arr)
    mujoco.mj_forward(model, data)


def _select_grasp_ready_bank_idx(bank_pos: np.ndarray, target_pos: np.ndarray, joint_bank: np.ndarray | None = None) -> int:
    pos = np.asarray(bank_pos, dtype=np.float64)
    target = np.asarray(target_pos, dtype=np.float64).reshape(3)
    xy_dist = np.linalg.norm(pos[:, :2] - target[:2].reshape(1, 2), axis=1)
    mask = (
        (pos[:, 2] > 0.18)
        & (pos[:, 0] > 0.08)
        & (pos[:, 0] < 0.34)
        & (np.abs(pos[:, 1]) < 0.08)
        & (xy_dist > 0.12)
    )
    if not np.any(mask):
        mask = (pos[:, 2] > 0.16) & (np.abs(pos[:, 1]) < 0.16) & (xy_dist > 0.08)
    idxs = np.where(mask)[0]
    if idxs.size == 0:
        return int(np.argmax(pos[:, 2]))
    compact_radius = np.linalg.norm(pos[idxs, :2], axis=1)
    score = (
        1.0 * pos[idxs, 2]
        - 3.0 * np.abs(pos[idxs, 1])
        - 1.8 * compact_radius
        + 0.25 * np.minimum(xy_dist[idxs], 0.25)
    )
    if joint_bank is not None:
        q = np.asarray(joint_bank, dtype=np.float64)
        if q.ndim == 2 and q.shape[0] == pos.shape[0] and q.shape[1] >= 6:
            # Ready pose should be compact, near the y=0 plane, and folded downward.
            score -= 0.45 * np.abs(q[idxs, 0])  # shoulder_rotation yaw
            score -= 0.35 * np.abs(q[idxs, 2] - 1.5)  # ellbow bends downward instead of staying too straight
            score -= 0.25 * np.abs(q[idxs, 4])  # wrist_jaw lateral twist
            score -= 0.20 * np.abs(q[idxs, 5] + 0.6)  # wrist_roll slightly downward
    return int(idxs[int(np.argmax(score))])


def _body_pos_or_default(model: mujoco.MjModel, data: mujoco.MjData, body_name: str, default: np.ndarray) -> np.ndarray:
    bid = _body_id_or_none(model, body_name)
    if bid is None:
        return np.asarray(default, dtype=np.float64).reshape(3).copy()
    return np.asarray(data.xpos[int(bid)], dtype=np.float64).copy()


def _body_quat_or_default(model: mujoco.MjModel, data: mujoco.MjData, body_name: str, default: np.ndarray) -> np.ndarray:
    bid = _body_id_or_none(model, body_name)
    if bid is None:
        return np.asarray(default, dtype=np.float64).reshape(4).copy()
    q = np.asarray(data.xquat[int(bid)], dtype=np.float64).copy()
    q /= max(float(np.linalg.norm(q)), 1e-12)
    return q


def _body_freejoint_vel(model: mujoco.MjModel, data: mujoco.MjData, body_name: str) -> np.ndarray:
    bid = _body_id_or_none(model, body_name)
    if bid is None:
        return np.zeros(6, dtype=np.float64)
    for jid in range(int(model.njnt)):
        if int(model.jnt_bodyid[jid]) == int(bid) and int(model.jnt_type[jid]) == int(mujoco.mjtJoint.mjJNT_FREE):
            dadr = int(model.jnt_dofadr[jid])
            return np.asarray(data.qvel[dadr : dadr + 6], dtype=np.float64).copy()
    return np.zeros(6, dtype=np.float64)


def _pos_compare_text(pos: np.ndarray, target: np.ndarray, bbox_min=None, bbox_max=None) -> str:
    p = np.asarray(pos, dtype=np.float64).reshape(3)
    t = np.asarray(target, dtype=np.float64).reshape(3)
    d = p - t
    horiz = float(np.linalg.norm(d[:2]))
    parts = [
        f"rel=({d[0]*1000:+.1f},{d[1]*1000:+.1f},{d[2]*1000:+.1f})mm",
        f"horiz={horiz*1000:.1f}mm",
    ]
    if bbox_min is not None and bbox_max is not None:
        b0 = np.asarray(bbox_min, dtype=np.float64).reshape(3)
        b1 = np.asarray(bbox_max, dtype=np.float64).reshape(3)
        top_gap = float(p[2] - b1[2])
        xy_inside = bool((p[0] >= b0[0]) and (p[0] <= b1[0]) and (p[1] >= b0[1]) and (p[1] <= b1[1]))
        parts.append(f"z-vs-mask-top={top_gap*1000:+.1f}mm")
        parts.append(f"xy_in_mask_bbox={xy_inside}")
    return " ".join(parts)


def _grasp_direction_class(approach: np.ndarray) -> str:
    app = np.asarray(approach, dtype=np.float64).reshape(3)
    app /= max(float(np.linalg.norm(app)), 1e-12)
    horiz = float(np.linalg.norm(app[:2]))
    z = float(app[2])
    if z < -0.55:
        return "top"
    if horiz > 0.85 and abs(z) < 0.35:
        return "side"
    return "diag"


def _copy_data_state(model: mujoco.MjModel, src: mujoco.MjData) -> mujoco.MjData:
    tmp = mujoco.MjData(model)
    tmp.qpos[:] = src.qpos
    tmp.qvel[:] = src.qvel
    tmp.ctrl[:] = src.ctrl
    mujoco.mj_forward(model, tmp)
    return tmp


def _tcp_pose_jacobian_fd(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    *,
    n_arm: int,
    eps: float = 1e-5,
) -> np.ndarray:
    j = np.zeros((6, n_arm), dtype=np.float64)
    q_saved = data.qpos.copy()
    qvel_saved = data.qvel.copy()
    for i, qadr in enumerate(ids.qpos_adr[:n_arm]):
        data.qpos[qadr] = q_saved[qadr] + float(eps)
        mujoco.mj_forward(model, data)
        tcp_plus, quat_plus = tcp_pose_w(data, ids)

        data.qpos[qadr] = q_saved[qadr] - float(eps)
        mujoco.mj_forward(model, data)
        tcp_minus, quat_minus = tcp_pose_w(data, ids)

        j[:3, i] = (tcp_plus - tcp_minus) / (2.0 * float(eps))
        q_delta = _quat_multiply_wxyz(quat_plus, _quat_conjugate_wxyz(quat_minus))
        j[3:, i] = _quat_to_rotvec_wxyz(q_delta) / (2.0 * float(eps))
        data.qpos[qadr] = q_saved[qadr]

    data.qpos[:] = q_saved
    data.qvel[:] = qvel_saved
    mujoco.mj_forward(model, data)
    return j


def _candidate_ik_check(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    pregrasp_pos: np.ndarray,
    grasp_quat: np.ndarray,
    approach_axis: np.ndarray,
    *,
    steps: int,
    max_pos_step: float,
    max_rot_step: float,
    pos_tol: float,
    approach_tol_deg: float,
    approach_gate_axis: str,
    mapped_local_axis: np.ndarray | None,
) -> dict:
    target_pos = np.asarray(pregrasp_pos, dtype=np.float64).reshape(3)
    target_quat = np.asarray(grasp_quat, dtype=np.float64).reshape(4)
    target_quat /= max(float(np.linalg.norm(target_quat)), 1e-12)
    desired_app = np.asarray(approach_axis, dtype=np.float64).reshape(3)
    desired_app /= max(float(np.linalg.norm(desired_app)), 1e-12)
    if str(approach_gate_axis).lower().strip() == "mapped" and mapped_local_axis is not None:
        local = np.asarray(mapped_local_axis, dtype=np.float64).reshape(3)
    else:
        local = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    local /= max(float(np.linalg.norm(local)), 1e-12)

    steps = max(0, int(steps))
    n_arm = max(ACTION_DIM - 1, 1)
    q_curr = joint_pos(data, ids)
    q_low = np.asarray(ids.q_low, dtype=np.float64)
    q_high = np.asarray(ids.q_high, dtype=np.float64)
    q_mid = 0.5 * (q_low + q_high)
    q_mid[-1] = q_curr[-1]
    seeds = [q_curr.copy(), np.clip(q_mid, q_low, q_high)]
    if n_arm >= 6:
        for delta in (-0.5 * math.pi, 0.5 * math.pi):
            q_seed = q_curr.copy()
            q_seed[5] = np.clip(q_seed[5] + delta, q_low[5], q_high[5])
            seeds.append(q_seed)

    def evaluate(tmp_data: mujoco.MjData) -> dict:
        tcp, quat = tcp_pose_w(tmp_data, ids)
        pos_err = float(np.linalg.norm(target_pos - tcp))
        quat_err = _quat_angle_deg(quat, target_quat)
        R = _quat_to_rotmat_wxyz(quat)
        app = R @ local
        app /= max(float(np.linalg.norm(app)), 1e-12)
        app_err = _axis_angle_deg(app, desired_app)
        q_now = joint_pos(tmp_data, ids)
        margins = np.minimum(q_now[:n_arm] - q_low[:n_arm], q_high[:n_arm] - q_now[:n_arm])
        limit_margin = float(np.min(margins)) if len(margins) else float("nan")
        return {
            "pos_err_m": pos_err,
            "quat_err_deg": quat_err,
            "approach_err_deg": app_err,
            "reachable": bool(pos_err <= float(pos_tol) and app_err <= float(approach_tol_deg)),
            "end_tcp": tcp.copy(),
            "end_quat": quat.copy(),
            "q_solution": q_now.copy(),
            "limit_margin_rad": limit_margin,
            "hit_limit": bool(math.isfinite(limit_margin) and limit_margin < 1e-4),
        }

    best: dict | None = None
    for seed in seeds:
        tmp = _copy_data_state(model, data)
        _set_robot_qpos(model, tmp, ids, np.clip(seed, q_low, q_high))
        for _ in range(steps):
            tcp, quat = tcp_pose_w(tmp, ids)
            pos_err_vec = target_pos - tcp
            pos_norm = float(np.linalg.norm(pos_err_vec))
            q_err = _quat_multiply_wxyz(target_quat, _quat_conjugate_wxyz(quat))
            rot_err = _quat_to_rotvec_wxyz(q_err)
            rot_norm = float(np.linalg.norm(rot_err))
            if pos_norm <= float(pos_tol) and _axis_angle_deg((_quat_to_rotmat_wxyz(quat) @ local), desired_app) <= float(approach_tol_deg):
                break

            pos_step = pos_err_vec.copy()
            if pos_norm > float(max_pos_step):
                pos_step *= float(max_pos_step) / max(pos_norm, 1e-12)
            rot_step = rot_err.copy()
            if rot_norm > float(max_rot_step):
                rot_step *= float(max_rot_step) / max(rot_norm, 1e-12)

            j = _tcp_pose_jacobian_fd(model, tmp, ids, n_arm=n_arm)
            rot_weight = 0.7
            err6 = np.concatenate([pos_step, rot_weight * rot_step])
            j6 = j.copy()
            j6[3:, :] *= rot_weight
            lhs = j6 @ j6.T + 2e-3 * np.eye(6, dtype=np.float64)
            try:
                dq_arm = j6.T @ np.linalg.solve(lhs, err6)
            except np.linalg.LinAlgError:
                dq_arm = j6.T @ np.linalg.pinv(lhs) @ err6
            max_joint_step = max(float(max_pos_step), 0.5 * float(max_rot_step))
            dq_arm = np.clip(dq_arm, -max_joint_step, max_joint_step)
            q_next = joint_pos(tmp, ids)
            q_next[:n_arm] = np.clip(q_next[:n_arm] + dq_arm, q_low[:n_arm], q_high[:n_arm])
            _set_robot_qpos(model, tmp, ids, q_next)
            if float(np.linalg.norm(dq_arm)) < 1e-7:
                break
        res = evaluate(tmp)
        if best is None:
            best = res
        else:
            old_key = (
                0 if bool(best["reachable"]) else 1,
                float(best["pos_err_m"]),
                float(best["approach_err_deg"]),
                float(best["quat_err_deg"]),
            )
            new_key = (
                0 if bool(res["reachable"]) else 1,
                float(res["pos_err_m"]),
                float(res["approach_err_deg"]),
                float(res["quat_err_deg"]),
            )
            if new_key < old_key:
                best = res

    if best is None:
        best = {
            "pos_err_m": float("inf"),
            "quat_err_deg": float("inf"),
            "approach_err_deg": float("inf"),
            "reachable": False,
            "end_tcp": np.full(3, float("nan")),
            "end_quat": np.full(4, float("nan")),
            "q_solution": np.full(ACTION_DIM, float("nan")),
            "limit_margin_rad": float("nan"),
            "hit_limit": False,
        }
    best.update(
        {
            "solver": "bounded_dls_ik",
            "pos_tol_m": float(pos_tol),
            "approach_tol_deg": float(approach_tol_deg),
        }
    )
    return {
        k: (v.tolist() if isinstance(v, np.ndarray) else v)
        for k, v in best.items()
    }


def _choose_anygrasp_candidate(
    bridge,
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    target_pos: np.ndarray,
    target_radius: float,
    pregrasp_distance: float,
    max_center_offset: float,
    approach_local_axis: np.ndarray | None = None,
    raw_approach_axis: str = "x",
    enable_ik_filter: bool = True,
    ik_steps: int = 80,
    ik_pos_tol: float = 0.005,
    ik_approach_tol_deg: float = 3.0,
    approach_gate_axis: str = "tcp_z",
    debug_axes: bool = False,
    debug_axes_count: int = 12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, object | None]:
    candidates = bridge.predict(model, data, target_pos_w=target_pos)
    target = np.asarray(target_pos, dtype=np.float64).reshape(3)
    dbg = getattr(bridge, "last_debug", None)
    if dbg is not None:
        print(
            f"[anygrasp_mask] depth_valid={int(getattr(dbg, 'n_depth_valid', 0))} "
            f"workspace={int(getattr(dbg, 'n_workspace', 0))} "
            f"mask_source={getattr(dbg, 'mask_source', '')} "
            f"target_pts={int(getattr(dbg, 'n_target_roi', 0))} "
            f"centroid_err={float(getattr(dbg, 'mask_centroid_error_m', float('nan')))*1000:.1f}mm "
            f"roi_radius={float(getattr(dbg, 'target_roi_radius_m', 0.0))*1000:.1f}mm "
            f"candidates={int(getattr(dbg, 'n_candidates', 0))} "
            f"best_score={float(getattr(dbg, 'best_score', float('nan'))):.3f} "
            f"msg={getattr(dbg, 'message', '')}"
        )
        winfo = getattr(dbg, "worker_info", {}) or {}
        if winfo:
            print(
                f"[anygrasp_worker] raw={int(winfo.get('n_raw_grasps', 0))} "
                f"after_nms={int(winfo.get('n_after_nms', 0))} "
                f"score_filtered={int(winfo.get('n_score_filtered', 0))} "
                f"width_filtered={int(winfo.get('n_width_filtered', 0))} "
                f"top_scores={winfo.get('top_raw_scores', [])[:5]} "
                f"top_widths_mm={[round(float(x)*1000.0, 1) for x in winfo.get('top_raw_widths', [])[:5]]}"
            )
        for i, item in enumerate(getattr(dbg, "top_candidates", [])[:8]):
            pos = np.asarray(item.get("pos_world", [float("nan")] * 3), dtype=np.float64)
            app = np.asarray(item.get("approach_world", [float("nan")] * 3), dtype=np.float64)
            bbox_min = getattr(dbg, "mask_bbox_min_world", []) or None
            bbox_max = getattr(dbg, "mask_bbox_max_world", []) or None
            print(
                f"[anygrasp_top {i:02d}] "
                f"score={float(item.get('score', float('nan'))):.3f} "
                f"width={float(item.get('width_m', float('nan')))*1000:.1f}mm "
                f"dist={float(item.get('dist_to_target_m', float('nan')))*1000:.1f}mm "
                f"pos=({pos[0]:+.3f},{pos[1]:+.3f},{pos[2]:+.3f}) "
                f"approach=({app[0]:+.2f},{app[1]:+.2f},{app[2]:+.2f}) "
                f"{_pos_compare_text(pos, target, bbox_min, bbox_max)}"
            )
    if not candidates:
        raise RuntimeError(getattr(bridge.last_debug, "message", "no AnyGrasp candidates"))
    if bool(debug_axes):
        n_dbg = max(0, min(int(debug_axes_count), len(candidates)))
        print(
            "[anygrasp_axes_header] "
            "x/y/z are raw AnyGrasp rotation-matrix columns after world transform; "
            "center_dir is candidate->target; ang_* is angle(axis, center_dir). "
            f"Current code uses raw {_raw_axis_label_for_print(raw_approach_axis)} as approach."
        )
        for i, c in enumerate(candidates[:n_dbg]):
            pos = np.asarray(c.pos_world, dtype=np.float64).reshape(3)
            R = np.asarray(c.rot_world, dtype=np.float64).reshape(3, 3)
            rel = target - pos
            dist = float(np.linalg.norm(rel))
            center_dir = rel / max(dist, 1e-12)
            axes = [R[:, 0], R[:, 1], R[:, 2]]
            axes = [a / max(float(np.linalg.norm(a)), 1e-12) for a in axes]
            neg_axes = [-a for a in axes]
            ang = [_axis_angle_deg(a, center_dir) for a in axes]
            ang_neg = [_axis_angle_deg(a, center_dir) for a in neg_axes]
            best_labels = ["+x", "+y", "+z", "-x", "-y", "-z"]
            best_angles = ang + ang_neg
            best_i = int(np.argmin(np.asarray(best_angles, dtype=np.float64)))
            print(
                f"[anygrasp_axes {i:02d}] "
                f"score={float(c.score):.3f} width={float(c.width)*1000:.1f}mm "
                f"dist={dist*1000:.1f}mm "
                f"rel_target=({rel[0]*1000:+.1f},{rel[1]*1000:+.1f},{rel[2]*1000:+.1f})mm "
                f"x=({axes[0][0]:+.2f},{axes[0][1]:+.2f},{axes[0][2]:+.2f}) "
                f"y=({axes[1][0]:+.2f},{axes[1][1]:+.2f},{axes[1][2]:+.2f}) "
                f"z=({axes[2][0]:+.2f},{axes[2][1]:+.2f},{axes[2][2]:+.2f}) "
                f"ang_x/y/z=({ang[0]:.1f},{ang[1]:.1f},{ang[2]:.1f})deg "
                f"best_to_center={best_labels[best_i]}:{best_angles[best_i]:.1f}deg"
            )
    max_dist = float(target_radius) + max(float(max_center_offset), 0.0)
    near_candidates = [
        c
        for c in candidates
        if float(np.linalg.norm(np.asarray(c.pos_world, dtype=np.float64).reshape(3) - target)) <= max_dist
    ]
    if not near_candidates:
        dists = [
            float(np.linalg.norm(np.asarray(c.pos_world, dtype=np.float64).reshape(3) - target)) * 1000.0
            for c in candidates[: min(8, len(candidates))]
        ]
        raise RuntimeError(
            f"no AnyGrasp candidate near target: max_allowed={max_dist*1000.0:.1f}mm; "
            f"top_score_dists_mm={[round(x, 1) for x in dists]}"
        )
    scored = []
    for raw_i, c in enumerate(near_candidates):
        tcp_rot_i, approach_i = _tcp_rot_from_anygrasp_rot(
            c.rot_world,
            approach_local_axis=approach_local_axis,
            raw_approach_axis=raw_approach_axis,
        )
        approach_i /= max(float(np.linalg.norm(approach_i)), 1e-12)
        grasp_pos_i = np.asarray(c.pos_world, dtype=np.float64).reshape(3)
        grasp_quat_i = _quat_wxyz_from_rotmat(tcp_rot_i)
        pregrasp_pos_i = grasp_pos_i - float(pregrasp_distance) * approach_i
        dist_i = float(np.linalg.norm(grasp_pos_i - target))
        dir_cls = _grasp_direction_class(approach_i)
        ik = {
            "pos_err_m": float("nan"),
            "quat_err_deg": float("nan"),
            "approach_err_deg": float("nan"),
            "reachable": True,
        }
        if bool(enable_ik_filter):
            ik = _candidate_ik_check(
                model,
                data,
                ids,
                pregrasp_pos_i,
                grasp_quat_i,
                approach_i,
                steps=int(ik_steps),
                max_pos_step=0.018,
                max_rot_step=0.18,
                pos_tol=float(ik_pos_tol),
                approach_tol_deg=float(ik_approach_tol_deg),
                approach_gate_axis=approach_gate_axis,
                mapped_local_axis=approach_local_axis,
            )
        scored.append(
            {
                "cand": c,
                "raw_i": raw_i,
                "tcp_rot": tcp_rot_i,
                "approach": approach_i,
                "grasp_pos": grasp_pos_i,
                "grasp_quat": grasp_quat_i,
                "pregrasp_pos": pregrasp_pos_i,
                "dist": dist_i,
                "dir_cls": dir_cls,
                "ik": ik,
            }
        )
    scored = sorted(
        scored,
        key=lambda s: (
            0 if bool(s["ik"].get("reachable", True)) else 1,
            -float(s["cand"].score)
            if bool(s["ik"].get("reachable", True))
            else float(s["ik"].get("pos_err_m", float("inf"))),
            float(s["dist"])
            if bool(s["ik"].get("reachable", True))
            else float(s["ik"].get("approach_err_deg", float("inf"))),
            float(s["dist"]),
        ),
    )
    if bool(enable_ik_filter) and not bool(scored[0]["ik"].get("reachable", False)):
        print("[anygrasp_ik] no candidate passed IK thresholds; falling back to smallest IK residual candidate")
    for i, s in enumerate(scored[: min(8, len(scored))]):
        c = s["cand"]
        ik = s["ik"]
        print(
            f"[anygrasp_ranked {i:02d}] raw_idx={int(s['raw_i'])} "
            f"score={float(c.score):.3f} cls={s['dir_cls']} "
            f"dist={float(s['dist'])*1000:.1f}mm "
            f"ik_pos={float(ik.get('pos_err_m', float('nan')))*1000:.1f}mm "
            f"ik_app={float(ik.get('approach_err_deg', float('nan'))):.1f}deg "
            f"limit_margin={float(ik.get('limit_margin_rad', float('nan'))):.3f}rad "
            f"hit_limit={bool(ik.get('hit_limit', False))} "
            f"reachable={bool(ik.get('reachable', True))}"
        )
    chosen = scored[0]
    cand = chosen["cand"]
    tcp_rot = chosen["tcp_rot"]
    approach = chosen["approach"]
    grasp_pos = chosen["grasp_pos"]
    grasp_quat = chosen["grasp_quat"]
    if float(np.linalg.norm(grasp_pos - target)) > max_dist:
        dists = [
            float(np.linalg.norm(np.asarray(c.pos_world, dtype=np.float64).reshape(3) - target)) * 1000.0
            for c in candidates[: min(5, len(candidates))]
        ]
        raise RuntimeError(
            f"nearest AnyGrasp candidate too far from target: "
            f"{float(np.linalg.norm(grasp_pos - target))*1000.0:.1f}mm; "
            f"max_allowed={max_dist*1000.0:.1f}mm; "
            f"top_dists_mm={[round(x, 1) for x in dists]}"
        )
    pregrasp_pos = grasp_pos - float(pregrasp_distance) * approach
    dbg = getattr(bridge, "last_debug", None)
    bbox_min = getattr(dbg, "mask_bbox_min_world", []) or None
    bbox_max = getattr(dbg, "mask_bbox_max_world", []) or None
    print(
        f"[anygrasp_selected] score={float(cand.score):.3f} width={float(cand.width)*1000:.1f}mm "
        f"grasp=({grasp_pos[0]:+.3f},{grasp_pos[1]:+.3f},{grasp_pos[2]:+.3f}) "
        f"pre=({pregrasp_pos[0]:+.3f},{pregrasp_pos[1]:+.3f},{pregrasp_pos[2]:+.3f}) "
        f"approach=({approach[0]:+.2f},{approach[1]:+.2f},{approach[2]:+.2f}) "
        f"{_pos_compare_text(grasp_pos, target, bbox_min, bbox_max)}"
    )
    raw_rot = np.asarray(cand.rot_world, dtype=np.float64).reshape(3, 3)
    print(
        "[anygrasp_frame_map] "
        f"raw_app_axis={_raw_axis_label_for_print(raw_approach_axis)} "
        f"raw_x_app=({raw_rot[0,0]:+.2f},{raw_rot[1,0]:+.2f},{raw_rot[2,0]:+.2f}) "
        f"raw_y_width=({raw_rot[0,1]:+.2f},{raw_rot[1,1]:+.2f},{raw_rot[2,1]:+.2f}) "
        f"raw_z=({raw_rot[0,2]:+.2f},{raw_rot[1,2]:+.2f},{raw_rot[2,2]:+.2f}) "
        f"tcp_x_close=({tcp_rot[0,0]:+.2f},{tcp_rot[1,0]:+.2f},{tcp_rot[2,0]:+.2f}) "
        f"tcp_z=({tcp_rot[0,2]:+.2f},{tcp_rot[1,2]:+.2f},{tcp_rot[2,2]:+.2f}) "
        f"used_app=({approach[0]:+.2f},{approach[1]:+.2f},{approach[2]:+.2f})"
    )
    return grasp_pos, pregrasp_pos, approach, grasp_quat, cand


def _anygrasp_debug_record(
    *,
    ep: int,
    target_idx: int,
    target_pos: np.ndarray,
    target_radius: float,
    bridge,
    selected_grasp,
    pregrasp_pos: np.ndarray,
    grasp_pos: np.ndarray,
    grasp_quat: np.ndarray,
    approach_axis: np.ndarray,
) -> dict:
    dbg = getattr(bridge, "last_debug", None) if bridge is not None else None
    candidates = list(getattr(bridge, "last_candidates", [])) if bridge is not None else []
    target = np.asarray(target_pos, dtype=np.float64).reshape(3)
    top = []
    for i, c in enumerate(candidates[:20]):
        pos = np.asarray(c.pos_world, dtype=np.float64).reshape(3)
        app = np.asarray(c.approach_world, dtype=np.float64).reshape(3)
        rot_w = np.asarray(c.rot_world, dtype=np.float64).reshape(3, 3)
        rot_any = np.asarray(c.rot_camera_anygrasp, dtype=np.float64).reshape(3, 3)
        top.append(
            {
                "rank": int(i),
                "score": float(c.score),
                "width_m": float(c.width),
                "depth_m": float(c.depth),
                "dist_to_target_m": float(np.linalg.norm(pos - target)),
                "pos_world": _arr(pos),
                "approach_world": _arr(app),
                "rot_world_columns": {
                    "x": _arr(rot_w[:, 0]),
                    "y": _arr(rot_w[:, 1]),
                    "z": _arr(rot_w[:, 2]),
                },
                "pos_camera_anygrasp": _arr(c.pos_camera_anygrasp),
                "rot_camera_anygrasp_columns": {
                    "x": _arr(rot_any[:, 0]),
                    "y": _arr(rot_any[:, 1]),
                    "z": _arr(rot_any[:, 2]),
                },
            }
        )
    sel_pos = None if selected_grasp is None else np.asarray(selected_grasp.pos_world, dtype=np.float64).reshape(3)
    mask_source = str(getattr(dbg, "mask_source", "")) if dbg is not None else ""
    target_points = int(getattr(dbg, "n_target_roi", 0)) if dbg is not None else 0
    mask_centroid_world = list(getattr(dbg, "mask_centroid_world", [])) if dbg is not None else []
    mask_bbox_min_world = list(getattr(dbg, "mask_bbox_min_world", [])) if dbg is not None else []
    mask_bbox_max_world = list(getattr(dbg, "mask_bbox_max_world", [])) if dbg is not None else []
    selected_score = float(getattr(selected_grasp, "score", float("nan"))) if selected_grasp is not None else float("nan")
    selected_width_m = float(getattr(selected_grasp, "width", float("nan"))) if selected_grasp is not None else float("nan")
    selected_dist_m = float(np.linalg.norm(sel_pos - target)) if sel_pos is not None else float("nan")
    return {
        "ep": int(ep),
        "target_idx": int(target_idx),
        "target_pos": _arr(target),
        "target_radius_m": float(target_radius),
        "mask_source": mask_source,
        "target_pts": target_points,
        "mask_centroid_world": mask_centroid_world,
        "mask_bbox_min_world": mask_bbox_min_world,
        "mask_bbox_max_world": mask_bbox_max_world,
        "selected_score": selected_score,
        "selected_width_m": selected_width_m,
        "selected_dist_to_target_m": selected_dist_m,
        "selected_pos_world": _arr(sel_pos) if sel_pos is not None else None,
        "selected_pregrasp_world": _arr(
            sel_pos - float(np.linalg.norm(np.asarray(grasp_pos, dtype=np.float64).reshape(3) - np.asarray(pregrasp_pos, dtype=np.float64).reshape(3))) * np.asarray(approach_axis, dtype=np.float64).reshape(3)
        )
        if sel_pos is not None
        else None,
        "selected_approach_world": _arr(approach_axis) if selected_grasp is not None else None,
        "selected_quat_wxyz": _arr(grasp_quat) if selected_grasp is not None else None,
        "tcp_goal_pos_world": _arr(grasp_pos),
        "pregrasp_goal_pos_world": _arr(pregrasp_pos),
        "tcp_goal_offset_from_selected_m": _arr(np.asarray(grasp_pos, dtype=np.float64).reshape(3) - sel_pos) if sel_pos is not None else None,
        "candidates": top,
        "mask": {
            "source": mask_source,
            "target_geom_name": str(getattr(dbg, "target_geom_name", "")) if dbg is not None else "",
            "target_geom_id": int(getattr(dbg, "target_geom_id", -1)) if dbg is not None else -1,
            "depth_valid": int(getattr(dbg, "n_depth_valid", 0)) if dbg is not None else 0,
            "workspace": int(getattr(dbg, "n_workspace", 0)) if dbg is not None else 0,
            "target_points": target_points,
            "roi_radius_m": float(getattr(dbg, "target_roi_radius_m", 0.0)) if dbg is not None else 0.0,
            "centroid_world": mask_centroid_world,
            "bbox_min_world": mask_bbox_min_world,
            "bbox_max_world": mask_bbox_max_world,
            "centroid_error_m": float(getattr(dbg, "mask_centroid_error_m", float("nan"))) if dbg is not None else float("nan"),
            "worker": dict(getattr(dbg, "worker_info", {})) if dbg is not None else {},
            "message": str(getattr(dbg, "message", "")) if dbg is not None else "",
        },
        "selected": {
            "score": selected_score,
            "width_m": selected_width_m,
            "dist_to_target_m": selected_dist_m,
            "grasp_pos": _arr(grasp_pos),
            "pregrasp_pos": _arr(pregrasp_pos),
            "approach_world": _arr(approach_axis),
            "grasp_quat_wxyz": _arr(grasp_quat),
        },
        "top_candidates": top,
    }


def _motion_spec(
    kind: str,
    center: str,
    amplitude: str,
    period_s: float,
    seed: int = 42,
    active_time_s: float = 2.0,
    clear_offset: str = "0.18,0.12,0.00",
    clear_time_s: float = 2.0,
) -> MotionSpec:
    return MotionSpec(
        kind=str(kind),
        center=_dyn.parse_vec3(center, default=(0.0, 0.0, 0.0)),
        amplitude=_dyn.parse_vec3(amplitude, default=(0.0, 0.0, 0.0)),
        period_s=float(period_s),
        seed=int(seed),
        random_active_s=float(active_time_s),
        clear_offset=_dyn.parse_vec3(clear_offset, default=(0.18, 0.12, 0.0)),
        clear_time_s=float(clear_time_s),
    )


def _apply_workspace_sdf_preset(obs_source, preset: str) -> None:
    cfg = getattr(obs_source, "cfg", None)
    if cfg is None:
        return
    p = str(preset).lower().strip()
    if p == "static":
        return
    if p == "dynamic":
        cfg.persistence_hits = 1
        cfg.persistence_forget_frames = 2
        cfg.persistence_voxel_size_m = 0.012
        return
    raise ValueError(f"unknown workspace SDF preset: {preset!r}")


def _traj_log_record(
    ep: int,
    step: int,
    t_s: float,
    idx: int,
    q_before: np.ndarray,
    q_after: np.ndarray,
    q_target: np.ndarray,
    tcp_after: np.ndarray,
    tcp_quat_after: np.ndarray,
    target_pos: np.ndarray,
    info: dict,
    obs_source,
    prev_dq_total: np.ndarray | None,
    grasp_source=None,
    task_state: str = "APPROACH",
    success_counter: int = 0,
    success_latched: bool = False,
    control_target_pos: np.ndarray | None = None,
    pregrasp_pos: np.ndarray | None = None,
    grasp_pos: np.ndarray | None = None,
    approach_axis: np.ndarray | None = None,
    approach_local_axis: np.ndarray | None = None,
    target_contact_count: int = 0,
    target_gripper_contact_count: int = 0,
    target_contact_pairs: list[dict] | None = None,
    grasp_track_debug: dict | None = None,
    grasp_replan_debug: dict | None = None,
    model: mujoco.MjModel | None = None,
    ids=None,
) -> dict:
    dq_nom = np.asarray(info.get("dq_nom", np.zeros_like(q_before)), dtype=np.float64).reshape(-1)
    dq_cbf = np.asarray(info.get("dq_cbf", np.zeros_like(q_before)), dtype=np.float64).reshape(-1)
    dq_total = np.asarray(q_target - q_before, dtype=np.float64).reshape(-1)
    if prev_dq_total is None:
        ddq_total = np.zeros_like(dq_total)
    else:
        ddq_total = dq_total - np.asarray(prev_dq_total, dtype=np.float64).reshape(-1)
    dbg = getattr(obs_source, "last_debug", None) if obs_source is not None else None
    gdbg = getattr(grasp_source, "last_debug", None) if grasp_source is not None else None
    desired_quat = np.asarray(info.get("desired_quat", np.full(4, np.nan)), dtype=np.float64).reshape(4)
    tcp_quat = np.asarray(tcp_quat_after, dtype=np.float64).reshape(4)
    tcp_rot = _quat_to_rotmat_wxyz(tcp_quat) if np.all(np.isfinite(tcp_quat)) else np.full((3, 3), np.nan)
    local_app = np.asarray(
        approach_local_axis if approach_local_axis is not None else np.array([0.0, 0.0, 1.0], dtype=np.float64),
        dtype=np.float64,
    ).reshape(3)
    local_app /= max(float(np.linalg.norm(local_app)), 1e-12)
    actual_approach = tcp_rot @ local_app if np.all(np.isfinite(tcp_rot)) else np.full(3, np.nan)
    desired_approach = np.asarray(approach_axis if approach_axis is not None else np.full(3, np.nan), dtype=np.float64).reshape(3)
    control_target = np.asarray(control_target_pos if control_target_pos is not None else target_pos, dtype=np.float64).reshape(3)
    grasp_target = np.asarray(grasp_pos if grasp_pos is not None else np.full(3, np.nan), dtype=np.float64).reshape(3)
    control_err = float(np.linalg.norm(np.asarray(tcp_after, dtype=np.float64).reshape(3) - control_target))
    final_err = (
        float(np.linalg.norm(np.asarray(tcp_after, dtype=np.float64).reshape(3) - grasp_target))
        if np.all(np.isfinite(grasp_target))
        else float("nan")
    )
    quat_err_deg = (
        _quat_angle_deg(tcp_quat, desired_quat)
        if np.all(np.isfinite(tcp_quat)) and np.all(np.isfinite(desired_quat))
        else float("nan")
    )
    approach_err_deg = (
        _axis_angle_deg(actual_approach, desired_approach)
        if np.all(np.isfinite(actual_approach)) and np.all(np.isfinite(desired_approach))
        else float("nan")
    )
    grasp_axis_debug = _grasp_pose_axis_debug(
        tcp_quat,
        desired_quat,
        desired_approach,
        local_app,
        model=model,
        ids=ids,
        q=q_after,
    )
    axis_align = _axis_alignment_errors_deg(tcp_quat, desired_approach)
    best_axis, best_axis_err = min(
        axis_align.items(),
        key=lambda kv: float(kv[1]) if math.isfinite(float(kv[1])) else float("inf"),
    )
    gripper_axes = {"+x": float("nan"), "+y": float("nan"), "+z": float("nan"), "-x": float("nan"), "-y": float("nan"), "-z": float("nan")}
    gripper_axis_vecs = {
        "+x": np.full(3, np.nan),
        "+y": np.full(3, np.nan),
        "+z": np.full(3, np.nan),
        "-x": np.full(3, np.nan),
        "-y": np.full(3, np.nan),
        "-z": np.full(3, np.nan),
    }
    gripper_best_axis = ""
    gripper_best_err = float("nan")
    if model is not None and ids is not None and np.all(np.isfinite(desired_approach)):
        tmp = mujoco.MjData(model)
        _set_robot_qpos(model, tmp, ids, q_after)
        R_gripper = np.asarray(tmp.xmat[int(ids.gripper_body)], dtype=np.float64).reshape(3, 3)
        axes = {
            "+x": R_gripper[:, 0],
            "+y": R_gripper[:, 1],
            "+z": R_gripper[:, 2],
            "-x": -R_gripper[:, 0],
            "-y": -R_gripper[:, 1],
            "-z": -R_gripper[:, 2],
        }
        gripper_axis_vecs = axes
        gripper_axes = {k: _axis_angle_deg(v, desired_approach) for k, v in axes.items()}
        gripper_best_axis, gripper_best_err = min(
            gripper_axes.items(),
            key=lambda kv: float(kv[1]) if math.isfinite(float(kv[1])) else float("inf"),
        )
    return {
        "ep": int(ep),
        "step": int(step),
        "t_s": float(t_s),
        "target_idx": int(idx),
        "task_state": str(task_state),
        "success_counter": int(success_counter),
        "success_latched": bool(success_latched),
        "target_contacts": int(target_contact_count),
        "target_gripper_contacts": int(target_gripper_contact_count),
        "target_contact_pairs": list(target_contact_pairs or []),
        "grasp_track": dict(grasp_track_debug or {}),
        "grasp_replan": dict(grasp_replan_debug or {}),
        "target_pos": _arr(target_pos),
        "control_target_pos": _arr(control_target),
        "pregrasp_pos": _arr(pregrasp_pos if pregrasp_pos is not None else np.full(3, np.nan)),
        "grasp_pos": _arr(grasp_target),
        "approach_axis": _arr(approach_axis if approach_axis is not None else np.full(3, np.nan)),
        "approach_local_axis": _arr(local_app),
        "tcp_pos": _arr(tcp_after),
        "tcp_quat_wxyz": _arr(tcp_quat),
        "tcp_approach_axis": _arr(actual_approach),
        "desired_quat_wxyz": _arr(desired_quat),
        "quat_err_deg": float(quat_err_deg),
        "approach_err_deg": float(approach_err_deg),
        "grasp_pose_axes": grasp_axis_debug,
        "closing_axis_err_deg": float(grasp_axis_debug.get("closing_axis_err_deg", float("nan"))),
        "palm_axis_err_deg": float(grasp_axis_debug.get("palm_axis_err_deg", float("nan"))),
        "gripper_body_closing_err_deg": float(
            grasp_axis_debug.get("gripper_body_closing_err_deg", float("nan"))
        ),
        "gripper_body_closing_axis_best": str(
            grasp_axis_debug.get("gripper_body_closing_axis_best", "")
        ),
        "gripper_body_closing_axis_best_deg": float(
            grasp_axis_debug.get("gripper_body_closing_axis_best_deg", float("nan"))
        ),
        "control_err_m": float(control_err),
        "final_err_m": float(final_err),
        "tcp_axis_alignment_deg": {k: float(v) for k, v in axis_align.items()},
        "tcp_axis_alignment_best": str(best_axis),
        "tcp_axis_alignment_best_deg": float(best_axis_err),
        "gripper_body_axes_world": {k: _arr(v) for k, v in gripper_axis_vecs.items() if not k.startswith("-")},
        "gripper_body_axis_alignment_deg": {k: float(v) for k, v in gripper_axes.items()},
        "gripper_body_axis_alignment_best": str(gripper_best_axis),
        "gripper_body_axis_alignment_best_deg": float(gripper_best_err),
        "q": _arr(q_after),
        "q_before": _arr(q_before),
        "q_target": _arr(q_target),
        "dist_m": float(info.get("distance", float("nan"))),
        "quat_dot": float(info.get("quat_dot", float("nan"))),
        "dq_nom": _arr(dq_nom),
        "dq_cbf": _arr(dq_cbf),
        "dq_total": _arr(dq_total),
        "ddq_total_norm": float(np.linalg.norm(ddq_total)),
        "dq_nom_norm": float(np.linalg.norm(dq_nom)),
        "dq_cbf_norm": float(np.linalg.norm(dq_cbf)),
        "dq_total_norm": float(np.linalg.norm(dq_total)),
        "raw_action": _arr(info.get("raw_action", np.zeros_like(dq_total))),
        "h_min_m": float(info.get("h_min", float("inf"))),
        "cbf_active": bool(info.get("cbf_active", False)),
        "cbf_feasible": bool(info.get("cbf_feasible", True)),
        "cbf_projected": bool(info.get("cbf_projected", False)),
        "n_constraints": int(info.get("n_constraints", 0)),
        "worst_monitor": str(info.get("cbf_worst_monitor", "")),
        "worst_obstacle": str(info.get("cbf_worst_obstacle", "")),
        "worst_obs_step": float(info.get("cbf_worst_obs_step", 0.0)),
        "nom_violation": float(info.get("nom_violation", 0.0)),
        "vision_detected": bool(getattr(dbg, "detected", False)) if dbg is not None else False,
        "depth_valid_points": int(getattr(dbg, "n_depth_valid", 0)) if dbg is not None else 0,
        "robot_masked_points": int(getattr(dbg, "n_robot_masked", 0)) if dbg is not None else 0,
        "workspace_points": int(getattr(dbg, "n_workspace", 0)) if dbg is not None else 0,
        "vision_roi_points": int(getattr(dbg, "n_roi", 0)) if dbg is not None else 0,
        "table_filtered_points": int(getattr(dbg, "n_table_filtered", 0)) if dbg is not None else 0,
        "fused_points": int(getattr(dbg, "n_fused_points", 0)) if dbg is not None else 0,
        "persistent_voxels": int(getattr(dbg, "n_persistent_voxels", 0)) if dbg is not None else 0,
        "voxel_memory": int(getattr(dbg, "n_voxel_memory", 0)) if dbg is not None else 0,
        "sdf_points": int(getattr(dbg, "n_sdf_points", 0)) if dbg is not None else 0,
        "self_filtered_points": int(getattr(dbg, "n_self_filtered", 0)) if dbg is not None else 0,
        "anygrasp_ok": bool(getattr(gdbg, "ok", False)) if gdbg is not None else False,
        "anygrasp_msg": str(getattr(gdbg, "message", "")) if gdbg is not None else "",
        "anygrasp_points": int(getattr(gdbg, "n_points", 0)) if gdbg is not None else 0,
        "anygrasp_candidates": int(getattr(gdbg, "n_candidates", 0)) if gdbg is not None else 0,
        "anygrasp_best_score": float(getattr(gdbg, "best_score", float("nan"))) if gdbg is not None else float("nan"),
    }


def _print_camera_mounts(model: mujoco.MjModel, data: mujoco.MjData) -> None:
    """打印相机/支架世界系位姿，便于在 3D viewer 里对照检查。"""
    _cam = _load_local("so100_mj_camera", _THIS / "camera.py")
    print("[mujoco_play] 相机安装（home 位，世界系 m）")
    for body in ("scene_depth_cam_mount", "wrist_rgb_cam_mount", "scene_cam_lookat"):
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body)
        if bid < 0:
            continue
        p = data.xpos[bid]
        print(f"  body {body:24s} pos=({p[0]:+.3f}, {p[1]:+.3f}, {p[2]:+.3f})")
    for cam_name in (SCENE_DEPTH_CAM, WRIST_RGB_CAM):
        ext = _cam.camera_extrinsics(model, data, cam_name)
        view = _cam.camera_view_direction(data, model, cam_name)
        p = ext.pos_world
        print(
            f"  cam  {cam_name:24s} pos=({p[0]:+.3f}, {p[1]:+.3f}, {p[2]:+.3f}) "
            f"view=({view[0]:+.2f}, {view[1]:+.2f}, {view[2]:+.2f})"
        )
    print("  3D 中深灰盒=scene_depth 支架，夹爪顶缝小盒=wrist_rgb；右侧选 body 可高亮")


class _CameraPreview:
    """兼容 play.py：委托给 camera.LiveCameraPreview。"""

    def __init__(
        self,
        model: mujoco.MjModel,
        *,
        show_depth: bool = False,
        backend: str = "auto",
        save_dir: str | None = None,
    ) -> None:
        _cam = _load_local("so100_mj_camera", _THIS / "camera.py")
        self._inner = _cam.LiveCameraPreview(
            model,
            show_depth=show_depth,
            backend=backend,
            save_dir=save_dir,
        )

    def update(self, data: mujoco.MjData) -> None:
        self._inner.update(data)

    def close(self) -> None:
        self._inner.close()


def run(args: argparse.Namespace) -> int:
    if bool(args.enable_sdf_cbf_qp):
        args.enable_cbf = True
        if str(args.obstacle_source).strip().lower() == "geom":
            args.obstacle_source = "geom_sdf"
    if bool(args.enable_grasp_chain) and str(args.mjcf) == str(DEFAULT_MJCF):
        args.mjcf = str(DEFAULT_MJCF_GRASP_OBSTACLE if bool(args.enable_obstacle) else DEFAULT_MJCF_NOROD)
    ckpt = Path(args.checkpoint).expanduser().resolve()
    mjcf = Path(args.mjcf).expanduser().resolve()
    npz = Path(args.npz).expanduser().resolve()
    if not ckpt.is_file():
        print(f"[ERROR] checkpoint not found: {ckpt}", file=sys.stderr)
        return 1
    if not mjcf.is_file():
        print(f"[ERROR] mjcf not found: {mjcf}", file=sys.stderr)
        return 1
    if not npz.is_file():
        print(f"[ERROR] npz not found: {npz}", file=sys.stderr)
        return 1

    # 有界面默认按仿真时间播放；headless 默认全速
    use_realtime = bool(args.realtime) if args.realtime is not None else (not args.headless)
    speed = max(float(args.speed), 1e-3)
    ctrl_dt = float(SIM_DT) * int(DECIMATION)
    sleep_s = (ctrl_dt / speed) if use_realtime else 0.0

    print(f"[mujoco_play] checkpoint: {ckpt}")
    print(f"[mujoco_play] mjcf: {mjcf}")
    print(f"[mujoco_play] npz: {npz}")
    print(
        f"[mujoco_play] realtime={use_realtime} speed={speed}x  "
        f"(有界面默认实时；太快用 --speed 0.5)"
    )
    if bool(args.enable_grasp_chain):
        print(
            "[mujoco_play] grasp chain=ON  static target object + pregrasp/final/close; "
            "obstacles disabled unless --enable-obstacle or --mjcf is explicit"
        )
        print(f"[mujoco_play] obstacle scene={'ON' if bool(args.enable_obstacle) else 'OFF'}")
        if bool(args.enable_sdf_cbf_qp):
            print(f"[mujoco_play] SDF-CBF-QP avoidance=ON source={args.obstacle_source}")

    model = mujoco.MjModel.from_xml_path(str(mjcf))
    model.opt.timestep = float(SIM_DT)
    data = mujoco.MjData(model)
    if bool(args.enable_grasp_chain):
        _select_grasp_target_object(args)
        _configure_grasp_target_visibility(model, str(args.target_geom))
        _park_inactive_grasp_targets(model, data, str(args.target_body))
        print(
            f"[mujoco_play] grasp target object={str(args.grasp_target_object).strip().lower()} "
            f"body={args.target_body} geom={args.target_geom}"
        )
    if bool(args.enable_grasp_chain) and _body_id_or_none(model, str(args.target_body)) is None:
        print(
            f"[ERROR] grasp chain requires body {args.target_body!r}; "
            f"use --mjcf {DEFAULT_MJCF_NOROD}",
            file=sys.stderr,
        )
        return 1
    ids = resolve_robot_ids(model)
    ee_tcp_offset = _dyn.parse_vec3(str(args.ee_tcp_offset), default=(0.0, 0.0, 0.0))
    ids.tcp_offset_local = np.asarray(ee_tcp_offset, dtype=np.float64).reshape(3)
    if bool(args.enable_grasp_chain) or float(np.linalg.norm(ids.tcp_offset_local)) > 1e-12:
        print(
            f"[mujoco_play] EE/TCP local offset="
            f"({ids.tcp_offset_local[0]:+.3f},{ids.tcp_offset_local[1]:+.3f},{ids.tcp_offset_local[2]:+.3f})m "
            "(applied to robot TCP pose, not to AnyGrasp target)"
        )
    approach_local_axis = None
    pregrasp_gate_local_axis = None
    if bool(args.enable_grasp_chain):
        approach_mode = "tcp_z"
        approach_local_axis = np.array([0.0, 0.0, 1.0], dtype=np.float64)
        print(
            f"[mujoco_play] grasp approach axis={approach_mode} "
            f"local_in_policy_tcp=({approach_local_axis[0]:+.3f},{approach_local_axis[1]:+.3f},{approach_local_axis[2]:+.3f})"
        )
        gate_mode = "tcp_z"
        pregrasp_gate_local_axis = np.array([0.0, 0.0, 1.0], dtype=np.float64)
        print(
            f"[mujoco_play] pregrasp gate approach axis={gate_mode} "
            f"local=({pregrasp_gate_local_axis[0]:+.3f},{pregrasp_gate_local_axis[1]:+.3f},{pregrasp_gate_local_axis[2]:+.3f})"
        )
        print("[mujoco_play] grasp roll mode=anygrasp")
        print("[mujoco_play] AnyGrasp raw approach axis=x")
        print("[mujoco_play] grasp controller=policy")
    policy = SkrlGaussianPolicy(ckpt)
    cbf_cfg = None
    if args.enable_cbf:
        cbf_cfg = CbfConfig(
            d_safe=float(args.cbf_d_safe),
            gamma=float(args.cbf_gamma),
            lambda_cbf=float(args.cbf_lambda),
            dq_max=float(args.action_scale),
            activate_margin=float(args.cbf_activate_margin),
            capsule_sample_count=int(args.cbf_capsule_samples),
            qp_metric=str(args.cbf_qp_metric),
            task_preserve_weight=float(args.cbf_task_preserve_weight),
            target_guidance=bool(args.cbf_target_guidance),
            target_guidance_clearance=float(args.cbf_target_guidance_clearance),
            target_guidance_reach=float(args.cbf_target_guidance_reach),
            target_guidance_forward=float(args.cbf_target_guidance_forward),
            target_guidance_dynamic_clearance=float(args.cbf_target_guidance_dynamic_clearance),
            target_guidance_dynamic_forward=float(args.cbf_target_guidance_dynamic_forward),
            target_guidance_dynamic_speed_thresh=float(args.cbf_target_guidance_dynamic_speed_thresh),
            target_guidance_dynamic_closing_speed_thresh=float(args.cbf_target_guidance_dynamic_closing_speed_thresh),
            target_guidance_release_steps=int(args.cbf_target_guidance_release_steps),
            target_guidance_switch_slack=float(args.cbf_target_guidance_switch_slack),
            target_guidance_dynamic_lookahead_steps=float(args.cbf_target_guidance_dynamic_lookahead_steps),
            dynamic_obstacle_lookahead_steps=float(args.cbf_dynamic_lookahead_steps),
        )
        print(
            f"[mujoco_play] CBF=ON  d_safe={cbf_cfg.d_safe}m  gamma={cbf_cfg.gamma}  "
            f"lambda={cbf_cfg.lambda_cbf}  activate<{cbf_cfg.activate_margin}m  "
            f"samples={cbf_cfg.capsule_sample_count} metric={cbf_cfg.qp_metric} "
            f"target_guidance={cbf_cfg.target_guidance}"
        )

    stepper = ReachStepper(
        policy=policy,
        ids=ids,
        model=model,
        action_scale=float(args.action_scale),
        filter_tau=float(args.filter_tau),
        cbf_filter_tau=float(args.cbf_filter_tau),
        enable_cbf_correction_filter=bool(args.cbf_correction_filter),
        cbf_bypass_filter_when_unsafe=bool(args.cbf_bypass_filter_when_unsafe),
        sim_dt=float(SIM_DT),
        decimation=int(DECIMATION),
        enable_cbf=bool(args.enable_cbf),
        cbf_cfg=cbf_cfg,
    )

    grasp_source_mode = str(args.grasp_source).strip().lower()
    anygrasp_bridge = None
    if bool(args.enable_grasp_chain) and grasp_source_mode == "anygrasp":
        try:
            anygrasp_bridge = AnyGraspBridge(
                model,
                AnyGraspConfig(
                    checkpoint_path=str(args.anygrasp_checkpoint),
                    top_k=int(args.anygrasp_top_k),
                    min_score=float(args.anygrasp_min_score),
                    max_width=float(args.anygrasp_max_width),
                    collision_detection=bool(args.anygrasp_collision_detection),
                    conda_env=str(args.anygrasp_conda_env),
                    target_roi_radius_m=float(args.anygrasp_target_roi_radius),
                    mask_source=str(args.anygrasp_mask_source),
                    target_geom_name=str(args.target_geom),
                    target_mask_dilate_px=int(args.anygrasp_target_mask_dilate_px),
                    target_mask_expand_ratio=float(args.anygrasp_target_mask_expand_ratio),
                ),
            )
            print(
                f"[mujoco_play] grasp source=AnyGrasp top_k={args.anygrasp_top_k} "
                f"min_score={float(args.anygrasp_min_score):.2f} "
                f"mask_source={args.anygrasp_mask_source}"
            )
            print("[mujoco_play] AnyGrasp 可视化：黄=top候选，绿=选中grasp/approach，青=pregrasp，红=目标球")
        except Exception as exc:
            print(f"[ERROR] AnyGrasp bridge unavailable: {exc}", file=sys.stderr)
            return 1
    elif bool(args.enable_grasp_chain):
        print(f"[mujoco_play] grasp source={grasp_source_mode}")

    grasp_tracker = None
    if bool(args.enable_grasp_chain) and bool(args.grasp_track_object):
        try:
            grasp_tracker = make_grasp_tracker(
                str(args.grasp_track_source),
                model,
                target_geom_name=str(args.target_geom),
                wrist_flip_image_y=bool(args.grasp_wrist_flip_image_y),
            )
            if grasp_tracker is not None:
                print(f"[mujoco_play] grasp tracking source={str(args.grasp_track_source).strip().lower()}")
                if str(args.grasp_track_source).strip().lower() == "wrist":
                    print(
                        "[mujoco_play] wrist tracking camera-frame y "
                        f"{'flipped' if bool(args.grasp_wrist_flip_image_y) else 'not flipped'} "
                        "(diagnostic: compare wrist_pos vs target_pos in traj log)"
                    )
        except Exception as exc:
            print(f"[ERROR] grasp tracker unavailable: {exc}", file=sys.stderr)
            return 1

    obs_source = None
    if args.enable_cbf:
        _obs = _load_local("so100_mj_obstacle_source", _THIS / "obstacle_source.py")
        obs_source = _obs.make_obstacle_source(
            str(args.obstacle_source),
            model,
            geom_names=cbf_cfg.obstacle_geom_names,
            calib_json=args.calib_json,
            use_sim_cam=bool(args.use_sim_cam),
        )
        _apply_workspace_sdf_preset(obs_source, str(args.workspace_sdf_preset))
        stepper.cbf_obstacle_source = obs_source
        print(f"[mujoco_play] obstacle source={args.obstacle_source}")
        if str(args.workspace_sdf_preset) != "static":
            print(f"[mujoco_play] workspace_sdf preset={args.workspace_sdf_preset}")
        obs_kind = str(args.obstacle_source).lower()
        if obs_kind in (
            "geom_sdf",
            "ideal_sdf",
            "pointcloud",
            "ideal_pointcloud",
            "vision",
            "scene_depth",
            "depth",
            "sdf",
            "scene_depth_sdf",
            "depth_sdf",
            "vision_sdf",
            "workspace_sdf",
            "unknown_sdf",
        ):
            if obs_kind in ("geom_sdf", "ideal_sdf", "pointcloud", "ideal_pointcloud"):
                print("[mujoco_play] 理想点云 SDF：指定 obstacle geom → 表面点云 → SDF（不走视觉链路）")
            else:
                if args.use_sim_cam:
                    print("[mujoco_play] 视觉内外参：MuJoCo fovy/xpos（调试，非标定 JSON）")
                else:
                    print(f"[mujoco_play] 视觉内外参：{Path(args.calib_json).expanduser().resolve()}")
            if obs_kind in ("vision", "scene_depth", "depth"):
                print(
                    "[mujoco_play] 视觉障碍 v1：scene_depth 深度→圆柱拟合；"
                    "wrist_rgb 暂不参与（近场补盲留后续）"
                )
            elif obs_kind in ("sdf", "scene_depth_sdf", "depth_sdf", "vision_sdf", "workspace_sdf", "unknown_sdf"):
                print(
                    "[mujoco_play] 视觉障碍 SDF：scene_depth 深度→workspace裁剪→桌面/自身过滤→未知物体点云SDF"
                )

    bank_pos, bank_quat = load_target_bank(npz)
    joint_bank = _load_joint_bank(npz)
    rng = np.random.default_rng(int(args.seed))
    steps_per_ep = int(round(EPISODE_LENGTH_S / (SIM_DT * DECIMATION)))
    if bool(args.enable_grasp_chain):
        steps_per_ep = max(steps_per_ep, int(round(steps_per_ep * max(float(args.grasp_episode_time_scale), 1.0))))
    cbf_log_path = Path(args.cbf_log).expanduser().resolve() if args.cbf_log else None
    if cbf_log_path is not None:
        cbf_log_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"[mujoco_play] CBF log → {cbf_log_path}")
    traj_log_path = Path(args.traj_log).expanduser().resolve() if args.traj_log else None
    if traj_log_path is not None:
        traj_log_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"[mujoco_play] trajectory log → {traj_log_path}")
    print(
        f"[INFO] bank={bank_pos.shape[0]}  steps/ep={steps_per_ep}  "
        f"scale={args.action_scale} tau={args.filter_tau}"
    )

    viewer = None
    cam_preview = None
    if args.show_cam:
        try:
            cam_preview = _CameraPreview(
                model,
                show_depth=bool(args.cam_depth),
                backend=str(args.cam_backend),
                save_dir=str(args.cam_save_dir) if args.cam_save_dir else None,
            )
            bk = cam_preview._inner.backend_name
            if bk == "save":
                out = cam_preview._inner._save_dir
                print(f"[mujoco_play] 相机预览 ON（写帧模式）→ {out}/live_*.png")
            elif bk == "mpl":
                print("[mujoco_play] 相机预览 ON（matplotlib 窗口）")
            else:
                print("[mujoco_play] 相机预览 ON（OpenCV 窗口）")
        except Exception as exc:
            print(f"[ERROR] 相机预览启动失败: {exc}", file=sys.stderr)
            return 1
    if not args.headless:
        try:
            import mujoco.viewer as mjv

            viewer = mjv.launch_passive(model, data)
            reset_home(model, data, ids)
            _print_camera_mounts(model, data)
            if float(args.hold_home) > 0:
                print(
                    f"[mujoco_play] home 暂停 {float(args.hold_home):.0f}s："
                    "拖动旋转视角，检查相机安装位置…"
                )
                _draw_overlays(viewer, bank_pos[int(rng.integers(0, bank_pos.shape[0]))])
                viewer.sync()
                time.sleep(float(args.hold_home))
        except Exception as exc:
            print(f"[WARN] viewer unavailable ({exc}), fallback headless")
            viewer = None
            if cam_preview is None:
                use_realtime = False
                sleep_s = 0.0

    target_motion = _motion_spec(
        str(args.target_motion),
        str(args.target_motion_center),
        str(args.target_motion_amp),
        float(args.target_motion_period),
    )
    obstacle_motion = _motion_spec(
        str(args.obstacle_motion),
        str(args.obstacle_motion_center),
        str(args.obstacle_motion_amp),
        float(args.obstacle_motion_period),
        int(args.obstacle_motion_seed),
        float(args.obstacle_motion_active_time),
        str(args.obstacle_motion_clear_offset),
        float(args.obstacle_motion_clear_time),
    )
    obstacle_runner = _dyn.MotionRunner(
        spec=obstacle_motion,
        probe_trigger_distance=float(args.obstacle_motion_probe_trigger_distance),
        probe_offset=_dyn.parse_vec3(
            str(args.obstacle_motion_probe_offset), default=(-0.07, 0.05, -0.15)
        ),
        probe_time_s=float(args.obstacle_motion_probe_time),
    )
    dynamic_target = str(args.target_motion).lower().strip() != "none"
    dynamic_obstacle = str(args.obstacle_motion).lower().strip() != "none"
    if dynamic_target:
        print(
            f"[mujoco_play] dynamic target: {args.target_motion} "
            f"amp={args.target_motion_amp} period={float(args.target_motion_period):.2f}s"
        )
    if dynamic_obstacle:
        print(
            f"[mujoco_play] dynamic obstacle body={args.obstacle_body} motion={args.obstacle_motion} "
            f"amp={args.obstacle_motion_amp} period={float(args.obstacle_motion_period):.2f}s "
            f"can_fall={bool(args.obstacle_can_fall)}"
        )
    dynamic_obstacle_home_pos = None
    obstacle_home_bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(args.obstacle_body))
    if obstacle_home_bid >= 0:
        dynamic_obstacle_home_pos = np.asarray(model.body_pos[int(obstacle_home_bid)], dtype=np.float64).copy()

    ep = 0
    try:
        while ep < int(args.episodes):
            if viewer is not None and not viewer.is_running():
                break

            if int(args.target_idx) >= 0:
                idx = int(args.target_idx)
                if idx >= bank_pos.shape[0]:
                    raise ValueError(f"--target-idx {idx} out of range [0, {bank_pos.shape[0]})")
            else:
                idx = int(rng.integers(0, bank_pos.shape[0]))
            target_pos = bank_pos[idx].copy()
            target_base_pos = target_pos.copy()
            target_quat = bank_quat[idx].copy()
            target_quat /= max(float(np.linalg.norm(target_quat)), 1e-12)

            reset_home(model, data, ids)
            obstacle_base_pos = None
            obstacle_bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(args.obstacle_body))
            if obstacle_bid >= 0:
                obstacle_base_pos = (
                    dynamic_obstacle_home_pos.copy()
                    if dynamic_obstacle_home_pos is not None
                    else np.asarray(model.body_pos[int(obstacle_bid)], dtype=np.float64).copy()
                )
                if dynamic_obstacle:
                    _dyn.set_body_pos(
                        model,
                        data,
                        str(args.obstacle_body),
                        obstacle_base_pos,
                        lock_upright=not bool(args.obstacle_can_fall),
                    )
            stepper.reset_filter()
            if args.enable_cbf:
                stepper.refresh_cbf_obstacles(data)
            best_dist = float("inf")
            best_ori = float("inf")
            arm_obstacle_contact_steps = 0
            cbf_stats = CbfEpisodeStats() if args.enable_cbf else None
            t0 = time.perf_counter()
            prev_dq_total: np.ndarray | None = None
            task_state = "MOVE_TO_PREGRASP" if bool(args.enable_grasp_chain) else "APPROACH"
            success_counter = 0
            success_latched = False
            success_step = -1
            settle_steps = 0
            max_settle_steps = int(round(max(float(args.settle_on_success), 0.0) / ctrl_dt))
            hold_target_q: np.ndarray | None = None
            pregrasp_pos = target_pos.copy()
            grasp_pos = target_pos.copy()
            target_plan_pos = target_pos.copy()
            pregrasp_plan_pos = pregrasp_pos.copy()
            grasp_plan_pos = grasp_pos.copy()
            grasp_quat = target_quat.copy()
            approach_axis = np.array([1.0, 0.0, 0.0], dtype=np.float64)
            final_approach_steps = 1
            final_approach_timeout_steps = 1
            final_approach_counter = 0
            close_steps = max(1, int(round(max(float(args.grasp_close_time), ctrl_dt) / ctrl_dt)))
            lift_steps = max(1, int(round(max(float(args.grasp_lift_time), ctrl_dt) / ctrl_dt)))
            close_counter = 0
            lift_counter = 0
            target_released = False
            frozen_grasp_q: np.ndarray | None = None
            close_start_q: np.ndarray | None = None
            verify_hold_q: np.ndarray | None = None
            selected_grasp = None
            grasp_candidates_viz = []
            replan_attempts = 0
            replan_compute_attempts = 0
            replan_wait_counter = 0
            replan_wait_steps = max(1, int(round(max(float(args.grasp_replan_settle_time), ctrl_dt) / ctrl_dt)))
            replan_retry_steps = max(1, int(round(max(float(args.grasp_replan_retry_time), ctrl_dt) / ctrl_dt)))
            replan_report_steps = max(1, int(round(max(float(args.grasp_replan_report_interval), ctrl_dt) / ctrl_dt)))
            replan_debug: dict = {}
            close_track_steps = max(0, int(round(max(float(args.grasp_tracking_close_time), 0.0) / ctrl_dt)))
            grasp_track_invalid_counter = 0
            grasp_track_ever_valid = False
            grasp_track_debug: dict = {}
            if bool(args.enable_grasp_chain):
                target_radius = _geom_radius_or_default(model, str(args.target_geom), float(args.target_radius))
                target_floor_center_z = _geom_floor_center_z_or_default(model, str(args.target_geom), target_radius)
                if str(args.grasp_target_pos).strip():
                    target_pos = np.asarray(
                        _dyn.parse_vec3(str(args.grasp_target_pos), default=tuple(target_pos)),
                        dtype=np.float64,
                    )
                    target_base_pos = target_pos.copy()
                elif bool(args.grasp_target_on_floor):
                    target_pos[0] = max(float(target_pos[0]), float(args.grasp_target_min_x))
                    target_pos[2] = target_floor_center_z + float(args.grasp_target_floor_clearance)
                    target_base_pos = target_pos.copy()
                start_mode = str(args.grasp_start_mode).lower().strip()
                start_idx = -1
                if start_mode != "home":
                    if joint_bank is None:
                        raise RuntimeError("--grasp-start-mode requires joint_pos in workspace npz")
                    if start_mode == "bank_idx":
                        start_idx = int(args.grasp_start_bank_idx)
                        if start_idx < 0:
                            raise ValueError("--grasp-start-mode bank_idx requires --grasp-start-bank-idx >= 0")
                    else:
                        start_idx = (
                            int(args.grasp_start_bank_idx)
                            if int(args.grasp_start_bank_idx) >= 0
                            else _select_grasp_ready_bank_idx(bank_pos, target_pos, joint_bank)
                        )
                    if start_idx >= joint_bank.shape[0]:
                        raise ValueError(f"--grasp-start-bank-idx {start_idx} out of range [0, {joint_bank.shape[0]})")
                    q_start = joint_bank[start_idx].copy()
                    q_start[-1] = float(args.grasp_open_q)
                    _set_robot_qpos(model, data, ids, q_start)
                tcp0, _ = tcp_pose_w(data, ids)
                if start_mode == "home":
                    start_desc = "home"
                else:
                    start_desc = f"bank[{start_idx}]"
                print(
                    f"[ep {ep:03d}][grasp_init] start={start_desc} "
                    f"tcp=({tcp0[0]:+.3f},{tcp0[1]:+.3f},{tcp0[2]:+.3f}) "
                    f"target=({target_pos[0]:+.3f},{target_pos[1]:+.3f},{target_pos[2]:+.3f}) "
                    f"xy_sep={float(np.linalg.norm(tcp0[:2] - target_pos[:2]))*1000.0:.1f}mm"
                )
                _set_static_body_pos(model, data, str(args.target_body), target_pos)
                settle_sim_steps = max(0, int(round(float(args.grasp_object_settle_time) / SIM_DT)))
                if settle_sim_steps > 0:
                    for _ in range(settle_sim_steps):
                        mujoco.mj_step(model, data)
                    target_pos = _body_pos_or_default(model, data, str(args.target_body), target_pos)
                    target_base_pos = target_pos.copy()
                    target_quat = _body_quat_or_default(model, data, str(args.target_body), target_quat)
                    target_vel6 = _body_freejoint_vel(model, data, str(args.target_body))
                    print(
                        f"[ep {ep:03d}][grasp_settle] t={float(args.grasp_object_settle_time):.2f}s "
                        f"pos=({target_pos[0]:+.3f},{target_pos[1]:+.3f},{target_pos[2]:+.3f}) "
                        f"quat=({target_quat[0]:+.3f},{target_quat[1]:+.3f},{target_quat[2]:+.3f},{target_quat[3]:+.3f}) "
                        f"|v|={float(np.linalg.norm(target_vel6[:3]))*1000.0:.2f}mm/s "
                        f"|w|={float(np.linalg.norm(target_vel6[3:])):.3f}rad/s"
                    )
                if bool(args.debug_anygrasp_frame) and cam_preview is not None:
                    preview_steps = max(1, int(round(float(args.debug_anygrasp_frame_preview_time) / SIM_DT)))
                    for _ in range(preview_steps):
                        mujoco.mj_step(model, data)
                        cam_preview.update(data)
                        if viewer is not None:
                            _draw_overlays(
                                viewer,
                                target_pos,
                                pregrasp_pos=pregrasp_pos,
                                grasp_pos=grasp_pos,
                            )
                            viewer.sync()
                        if use_realtime and sleep_s > 0.0:
                            time.sleep(sleep_s)
                    print(
                        f"[mujoco_play] 相机预览已连续更新 {float(args.debug_anygrasp_frame_preview_time):.2f}s；"
                        "debug-anygrasp-frame + show-cam 模式下跳过 AnyGrasp 执行。"
                    )
                    return 0
                if grasp_source_mode == "external":
                    if not str(args.external_grasp_pos).strip() or not str(args.external_pregrasp_pos).strip():
                        raise RuntimeError("--grasp-source external requires --external-grasp-pos and --external-pregrasp-pos")
                    grasp_pos = np.asarray(_dyn.parse_vec3(str(args.external_grasp_pos), default=tuple(target_pos)), dtype=np.float64)
                    pregrasp_pos = np.asarray(_dyn.parse_vec3(str(args.external_pregrasp_pos), default=tuple(target_pos)), dtype=np.float64)
                    q_raw = [float(x) for x in str(args.external_grasp_quat).replace(",", " ").split()]
                    if len(q_raw) != 4:
                        raise RuntimeError("--external-grasp-quat must be w,x,y,z")
                    grasp_quat = np.asarray(q_raw, dtype=np.float64)
                    grasp_quat /= max(float(np.linalg.norm(grasp_quat)), 1e-12)
                    delta = grasp_pos - pregrasp_pos
                    approach_axis = delta / max(float(np.linalg.norm(delta)), 1e-12)
                    selected_grasp = None
                    grasp_candidates_viz = []
                    cand_msg = (
                        f"External grasp width={float(args.external_gripper_width)*1000:.1f}mm "
                        f"quat=({grasp_quat[0]:+.2f},{grasp_quat[1]:+.2f},{grasp_quat[2]:+.2f},{grasp_quat[3]:+.2f}) "
                        "orientation=external"
                    )
                    print(
                        f"[external_grasp] pre=({pregrasp_pos[0]:+.3f},{pregrasp_pos[1]:+.3f},{pregrasp_pos[2]:+.3f}) "
                        f"final=({grasp_pos[0]:+.3f},{grasp_pos[1]:+.3f},{grasp_pos[2]:+.3f}) "
                        f"approach=({approach_axis[0]:+.2f},{approach_axis[1]:+.2f},{approach_axis[2]:+.2f})"
                    )
                else:
                    if anygrasp_bridge is None:
                        raise RuntimeError("grasp chain requires AnyGrasp bridge")
                    grasp_pos, pregrasp_pos, approach_axis, grasp_quat, cand = _choose_anygrasp_candidate(
                        anygrasp_bridge,
                        model,
                        data,
                        ids,
                        target_pos,
                        target_radius,
                        float(args.pregrasp_distance),
                        float(args.anygrasp_candidate_center_tolerance),
                        approach_local_axis=approach_local_axis,
                        enable_ik_filter=bool(args.anygrasp_ik_filter),
                        ik_steps=int(args.anygrasp_ik_steps),
                        ik_pos_tol=float(args.anygrasp_ik_pos_tol),
                        ik_approach_tol_deg=float(args.anygrasp_ik_approach_tol_deg),
                        approach_gate_axis="tcp_z",
                        debug_axes=bool(args.debug_anygrasp_axes),
                        debug_axes_count=int(args.debug_anygrasp_axes_count),
                    )
                    selected_grasp = cand
                    grasp_candidates_viz = list(getattr(anygrasp_bridge, "last_candidates", []))
                    dbg = getattr(anygrasp_bridge, "last_debug", None)
                    if dbg is not None:
                        print(
                            f"[anygrasp_selected_compare] target=({target_pos[0]:+.3f},{target_pos[1]:+.3f},{target_pos[2]:+.3f}) "
                            f"mask_centroid={tuple(round(float(x), 3) for x in getattr(dbg, 'mask_centroid_world', [])[:3])} "
                            f"mask_bbox_min={tuple(round(float(x), 3) for x in getattr(dbg, 'mask_bbox_min_world', [])[:3])} "
                            f"mask_bbox_max={tuple(round(float(x), 3) for x in getattr(dbg, 'mask_bbox_max_world', [])[:3])}"
                        )
                    cand_msg = (
                        f"AnyGrasp score={float(cand.score):.3f} width={float(cand.width)*1000:.1f}mm "
                        f"cand_dist={float(np.linalg.norm(cand.pos_world - target_pos))*1000:.1f}mm "
                        f"quat=({grasp_quat[0]:+.2f},{grasp_quat[1]:+.2f},{grasp_quat[2]:+.2f},{grasp_quat[3]:+.2f}) "
                        "orientation=anygrasp"
                    )
                final_dist = float(np.linalg.norm(grasp_pos - pregrasp_pos))
                target_plan_pos = target_pos.copy()
                pregrasp_plan_pos = pregrasp_pos.copy()
                grasp_plan_pos = grasp_pos.copy()
                if grasp_tracker is not None:
                    grasp_tracker.reset()
                final_approach_steps = max(
                    1,
                    int(math.ceil(final_dist / max(float(args.final_approach_speed) * ctrl_dt, 1e-5))),
                )
                final_approach_timeout_steps = max(
                    final_approach_steps,
                    int(math.ceil(final_approach_steps * max(float(args.grasp_final_timeout_scale), 1.0))),
                )
                print(
                    f"[ep {ep:03d}][grasp] target={idx} radius={target_radius*1000:.1f}mm "
                    f"pre=({pregrasp_pos[0]:.3f},{pregrasp_pos[1]:.3f},{pregrasp_pos[2]:.3f}) "
                    f"final=({grasp_pos[0]:.3f},{grasp_pos[1]:.3f},{grasp_pos[2]:.3f}) "
                    f"approach=({approach_axis[0]:+.2f},{approach_axis[1]:+.2f},{approach_axis[2]:+.2f}) "
                    f"final_steps={final_approach_steps} timeout_steps={final_approach_timeout_steps} "
                    f"{cand_msg}"
                )
                if anygrasp_bridge is not None:
                    rec = _anygrasp_debug_record(
                        ep=ep,
                        target_idx=idx,
                        target_pos=target_pos,
                        target_radius=target_radius,
                        bridge=anygrasp_bridge,
                        selected_grasp=selected_grasp,
                        pregrasp_pos=pregrasp_pos,
                        grasp_pos=grasp_pos,
                        grasp_quat=grasp_quat,
                        approach_axis=approach_axis,
                    )
                    _append_jsonl(args.anygrasp_debug_log, rec)
                if bool(args.debug_anygrasp_frame):
                    print(f"[mujoco_play] AnyGrasp debug only; log={Path(args.anygrasp_debug_log).expanduser().resolve()}")
                    if viewer is not None:
                        while viewer.is_running():
                            _draw_overlays(
                                viewer,
                                target_pos,
                                draw_target=False,
                                grasp_candidates=grasp_candidates_viz,
                                selected_grasp=selected_grasp,
                                pregrasp_pos=pregrasp_pos,
                                grasp_pos=grasp_pos,
                            )
                            viewer.sync()
                            time.sleep(0.05)
                    return 0

            for k in range(steps_per_ep):
                if viewer is not None and not viewer.is_running():
                    break

                t_s = k * ctrl_dt
                if dynamic_target:
                    target_pos = target_motion.position(t_s, base=target_base_pos)
                    if bool(args.enable_grasp_chain):
                        target_delta = target_pos - target_plan_pos
                        pregrasp_pos = pregrasp_plan_pos + target_delta
                        grasp_pos = grasp_plan_pos + target_delta
                if bool(args.enable_grasp_chain):
                    if bool(args.grasp_pin_target_until_close) and not target_released:
                        _set_static_body_pos(model, data, str(args.target_body), target_pos)
                    else:
                        target_pos = _body_pos_or_default(model, data, str(args.target_body), target_pos)
                    grasp_track_debug = {}
                    if (
                        bool(args.grasp_track_object)
                        and task_state in ("FINAL_APPROACH", "CLOSE")
                        and not target_released
                    ):
                        if grasp_tracker is not None:
                            track_res = grasp_tracker.update(
                                model,
                                data,
                                target_pos=target_pos,
                                target_plan_pos=target_plan_pos,
                            )
                            target_delta = np.asarray(track_res.delta_world, dtype=np.float64).reshape(3)
                            grasp_track_debug = {
                                "source": str(track_res.source),
                                "valid": bool(track_res.valid),
                                "reason": str(track_res.reason),
                                "confidence": float(track_res.confidence),
                                "n_points": int(track_res.n_points),
                                "delta_m": _arr(target_delta),
                                "delta_norm_m": float(np.linalg.norm(target_delta)),
                                "wrist_pos_world": _arr(track_res.pos_world)
                                if getattr(track_res, "pos_world", None) is not None
                                else None,
                                "wrist_pos_err_m": _arr(track_res.pos_err_world)
                                if getattr(track_res, "pos_err_world", None) is not None
                                else None,
                                "wrist_pos_err_norm_m": float(getattr(track_res, "pos_err_norm", float("nan"))),
                                "wrist_flip_image_y": bool(args.grasp_wrist_flip_image_y),
                            }
                        else:
                            target_delta = np.asarray(target_pos - target_plan_pos, dtype=np.float64).reshape(3)
                            grasp_track_debug = {
                                "source": "direct_target_pose",
                                "valid": True,
                                "reason": "no_tracker",
                                "confidence": 1.0,
                                "n_points": 1,
                                "delta_m": _arr(target_delta),
                                "delta_norm_m": float(np.linalg.norm(target_delta)),
                            }
                        delta_norm = float(np.linalg.norm(target_delta))
                        tracking_valid = bool(grasp_track_debug.get("valid", True))
                        track_activation_err = float(np.linalg.norm(np.asarray(tcp_pose_w(data, ids)[0], dtype=np.float64).reshape(3) - grasp_pos))
                        tracking_active = track_activation_err <= float(args.grasp_track_activate_dist)
                        if not tracking_active:
                            grasp_track_debug["active"] = False
                            grasp_track_debug["inactive_reason"] = "too_far_from_grasp"
                            grasp_track_debug["activate_dist_m"] = float(args.grasp_track_activate_dist)
                            grasp_track_debug["activation_err_m"] = float(track_activation_err)
                        else:
                            grasp_track_debug["active"] = True
                            grasp_track_debug["activate_dist_m"] = float(args.grasp_track_activate_dist)
                            grasp_track_debug["activation_err_m"] = float(track_activation_err)
                        if tracking_valid:
                            grasp_track_invalid_counter = 0
                            if tracking_active:
                                grasp_track_ever_valid = True
                        else:
                            if tracking_active:
                                grasp_track_invalid_counter += 1
                        invalid_replan_ready = (
                            grasp_track_ever_valid
                            and grasp_track_invalid_counter >= int(args.grasp_track_max_invalid_frames)
                        )
                        tracking_allowed = (
                            tracking_active
                            and
                            tracking_valid
                            and delta_norm <= float(args.grasp_track_max_delta)
                            and (task_state != "CLOSE" or close_counter <= close_track_steps)
                        )
                        if tracking_allowed:
                            gain = float(args.grasp_track_gain)
                            pregrasp_pos = pregrasp_plan_pos + gain * target_delta
                            grasp_pos = grasp_plan_pos + gain * target_delta
                        elif (
                            task_state == "FINAL_APPROACH"
                            and tracking_active
                            and
                            (
                                (tracking_valid and delta_norm >= float(args.grasp_replan_delta))
                                or (not tracking_valid and invalid_replan_ready)
                            )
                            and replan_attempts < int(args.grasp_replan_max_attempts)
                        ):
                            print(
                                f"[ep {ep:03d}][grasp_track] replan trigger: "
                                f"valid={tracking_valid} reason={grasp_track_debug.get('reason', '')} "
                                f"delta={delta_norm*1000.0:.1f}mm "
                                f"invalid={grasp_track_invalid_counter}/{int(args.grasp_track_max_invalid_frames)}; "
                                f"ever_valid={grasp_track_ever_valid}; "
                                f"attempt {replan_attempts + 1}/{int(args.grasp_replan_max_attempts)}"
                            )
                            task_state = "REPLAN_GRASP"
                            replan_wait_counter = 0
                            success_counter = 0
                            final_approach_counter = 0
                            close_counter = 0
                            frozen_grasp_q = None
                            close_start_q = None
                            verify_hold_q = None
                if dynamic_obstacle and obstacle_base_pos is not None:
                    tcp_now, _ = tcp_pose_w(data, ids)
                    obs_pos = obstacle_runner.position(
                        t_s,
                        obstacle_base_pos,
                        tcp_w=tcp_now,
                        target_w=target_pos,
                    )
                    _dyn.set_body_pos(
                        model,
                        data,
                        str(args.obstacle_body),
                        obs_pos,
                        lock_upright=not bool(args.obstacle_can_fall),
                    )

                q_before = joint_pos(data, ids)
                control_target_pos = target_pos
                if bool(args.enable_grasp_chain):
                    if task_state == "MOVE_TO_PREGRASP":
                        control_target_pos = pregrasp_pos
                        tgt, info = stepper.compute_targets(model, data, pregrasp_pos, grasp_quat)
                        tgt[-1] = float(args.grasp_open_q)
                        info["desired_quat"] = grasp_quat.copy()
                    elif task_state == "FINAL_APPROACH":
                        control_target_pos = grasp_pos
                        tgt, info = stepper.compute_targets(model, data, control_target_pos, grasp_quat)
                        # tar&ori semantics: final keeps the pregrasp-open jaw; closing starts only after arm freeze.
                        tgt[-1] = float(args.grasp_open_q)
                        info["desired_quat"] = grasp_quat.copy()
                    elif task_state == "CLOSE":
                        control_target_pos = grasp_pos
                        if frozen_grasp_q is None:
                            frozen_grasp_q = q_before.copy()
                        if close_start_q is None:
                            close_start_q = q_before.copy()
                        progress = min(1.0, close_counter / max(close_steps - 1, 1))
                        alpha = progress * progress * (3.0 - 2.0 * progress)
                        start_grip = float(close_start_q[-1])
                        if bool(args.grasp_track_object) and close_counter <= close_track_steps:
                            tgt, info = stepper.compute_targets(model, data, control_target_pos, grasp_quat)
                        else:
                            tgt = frozen_grasp_q.copy()
                            tcp_now, ee_quat_now = tcp_pose_w(data, ids)
                            info = {
                                "distance": float(np.linalg.norm(tcp_now - grasp_pos)),
                                "quat_dot": 1.0,
                                "dq_nom": tgt - q_before,
                                "dq_cbf": np.zeros_like(q_before),
                                "raw_action": np.zeros_like(q_before),
                                "h_min": float("inf"),
                                "cbf_active": False,
                                "cbf_feasible": True,
                                "cbf_projected": False,
                                "n_constraints": 0,
                                "dq_cbf_norm": 0.0,
                                "dq_nom_norm": float(np.linalg.norm(tgt - q_before)),
                                "dq_total_norm": float(np.linalg.norm(tgt - q_before)),
                                "desired_quat": grasp_quat.copy(),
                            }
                        tgt[-1] = (1.0 - alpha) * start_grip + alpha * float(args.grasp_close_q)
                        info["desired_quat"] = grasp_quat.copy()
                    elif task_state == "REPLAN_GRASP":
                        control_target_pos = pregrasp_pos
                        tgt, info = stepper.compute_targets(model, data, control_target_pos, grasp_quat)
                        tgt[-1] = float(args.grasp_open_q)
                        info["desired_quat"] = grasp_quat.copy()
                    elif task_state == "LIFT":
                        control_target_pos = grasp_pos + np.array([0.0, 0.0, float(args.grasp_lift_height)], dtype=np.float64)
                        tgt, info = stepper.compute_targets(model, data, control_target_pos, grasp_quat)
                        tgt[-1] = float(args.grasp_close_q)
                        info["desired_quat"] = grasp_quat.copy()
                    elif task_state == "VERIFY":
                        if verify_hold_q is None:
                            verify_hold_q = q_before.copy()
                        tgt = verify_hold_q.copy()
                        tgt[-1] = float(args.grasp_close_q)
                        tcp_now, _ = tcp_pose_w(data, ids)
                        control_target_pos = tcp_now.copy()
                        info = {
                            "distance": float(np.linalg.norm(tcp_now - target_pos)),
                            "quat_dot": 1.0,
                            "dq_nom": tgt - q_before,
                            "dq_cbf": np.zeros_like(q_before),
                            "raw_action": np.zeros_like(q_before),
                            "h_min": float("inf"),
                            "cbf_active": False,
                            "cbf_feasible": True,
                            "cbf_projected": False,
                            "n_constraints": 0,
                            "dq_cbf_norm": 0.0,
                            "dq_nom_norm": float(np.linalg.norm(tgt - q_before)),
                            "dq_total_norm": float(np.linalg.norm(tgt - q_before)),
                            "desired_quat": grasp_quat.copy(),
                        }
                    else:
                        tgt = q_before.copy()
                        tgt[-1] = float(args.grasp_close_q)
                        tcp_now, _ = tcp_pose_w(data, ids)
                        info = {
                            "distance": float(np.linalg.norm(tcp_now - grasp_pos)),
                            "quat_dot": 1.0,
                            "dq_nom": np.zeros_like(q_before),
                            "dq_cbf": np.zeros_like(q_before),
                            "raw_action": np.zeros_like(q_before),
                            "h_min": float("inf"),
                            "cbf_active": False,
                            "cbf_feasible": True,
                            "cbf_projected": False,
                            "n_constraints": 0,
                            "dq_cbf_norm": 0.0,
                            "dq_nom_norm": 0.0,
                            "dq_total_norm": 0.0,
                            "desired_quat": grasp_quat.copy(),
                        }
                elif task_state == "SETTLE" and str(args.settle_mode) == "hold_q" and hold_target_q is not None:
                    tgt = hold_target_q.copy()
                    tcp_now, ee_quat_now = tcp_pose_w(data, ids)
                    dist_now = float(np.linalg.norm(tcp_now - target_pos))
                    quat_dot_now = float(abs(np.dot(ee_quat_now / max(float(np.linalg.norm(ee_quat_now)), 1e-12), target_quat)))
                    info = {
                        "distance": dist_now,
                        "quat_dot": quat_dot_now,
                        "dq_nom": np.zeros_like(q_before),
                        "dq_cbf": np.zeros_like(q_before),
                        "raw_action": np.zeros_like(q_before),
                        "h_min": float("inf"),
                        "cbf_active": False,
                        "cbf_feasible": True,
                        "cbf_projected": False,
                        "n_constraints": 0,
                        "dq_cbf_norm": 0.0,
                        "dq_nom_norm": 0.0,
                        "dq_total_norm": float(np.linalg.norm(tgt - q_before)),
                        "desired_quat": target_quat.copy(),
                    }
                elif task_state == "SETTLE" and str(args.settle_mode) == "policy_soft_cbf":
                    tgt, info = _compute_with_soft_cbf(stepper, model, data, target_pos, target_quat, args)
                    info["desired_quat"] = target_quat.copy()
                else:
                    tgt, info = stepper.compute_targets(model, data, target_pos, target_quat)
                    info["desired_quat"] = target_quat.copy()
                if cbf_stats is not None:
                    cbf_stats.update(info)
                    if cbf_log_path is not None:
                        rec = cbf_step_log_record(ep, k, k * ctrl_dt, info)
                        with cbf_log_path.open("a", encoding="utf-8") as f:
                            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                set_ctrl(data, ids, tgt)
                for _ in range(int(DECIMATION)):
                    if dynamic_obstacle and obstacle_base_pos is not None:
                        _dyn.set_body_pos(
                            model,
                            data,
                            str(args.obstacle_body),
                            obs_pos,
                            lock_upright=not bool(args.obstacle_can_fall),
                        )
                    mujoco.mj_step(model, data)
                if _geom_contact_count_with_body(model, data, str(args.obstacle_geom), str(args.obstacle_contact_body)) > 0:
                    arm_obstacle_contact_steps += 1
                q_after = joint_pos(data, ids)
                tcp_after, tcp_quat_after = tcp_pose_w(data, ids)
                target_contact_count = (
                    _geom_contact_count(model, data, str(args.target_geom)) if bool(args.enable_grasp_chain) else 0
                )
                target_gripper_contact_count = (
                    _geom_contact_count_with_body(model, data, str(args.target_geom), GRIPPER_BODY)
                    if bool(args.enable_grasp_chain)
                    else 0
                )
                target_contact_pairs = (
                    _target_contact_pairs(model, data, str(args.target_geom)) if bool(args.enable_grasp_chain) else []
                )
                if traj_log_path is not None:
                    rec = _traj_log_record(
                        ep,
                        k,
                        t_s,
                        idx,
                        q_before,
                        q_after,
                        tgt,
                        tcp_after,
                        tcp_quat_after,
                        target_pos,
                        info,
                        obs_source,
                        prev_dq_total,
                        anygrasp_bridge,
                        task_state,
                        success_counter,
                        success_latched,
                        control_target_pos,
                        pregrasp_pos if bool(args.enable_grasp_chain) else None,
                        grasp_pos if bool(args.enable_grasp_chain) else None,
                        approach_axis if bool(args.enable_grasp_chain) else None,
                        pregrasp_gate_local_axis if bool(args.enable_grasp_chain) else None,
                        target_contact_count,
                        target_gripper_contact_count,
                        target_contact_pairs,
                        grasp_track_debug,
                        replan_debug,
                        model,
                        ids,
                    )
                    with traj_log_path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                prev_dq_total = np.asarray(tgt - q_before, dtype=np.float64)

                dist = float(info["distance"])
                ori = _ori_deg(float(info["quat_dot"]))
                best_dist = min(best_dist, dist)
                best_ori = min(best_ori, ori)

                if bool(args.enable_grasp_chain):
                    if task_state == "MOVE_TO_PREGRASP":
                        tcp_rot_now = _quat_to_rotmat_wxyz(tcp_quat_after)
                        tcp_app_now = tcp_rot_now @ np.asarray(pregrasp_gate_local_axis, dtype=np.float64).reshape(3)
                        tcp_app_now /= max(float(np.linalg.norm(tcp_app_now)), 1e-12)
                        pregrasp_app_err = _axis_angle_deg(tcp_app_now, approach_axis)
                        if dist <= float(args.pregrasp_success_dist) and pregrasp_app_err <= float(args.pregrasp_approach_success_deg):
                            success_counter += 1
                        else:
                            success_counter = 0
                        pregrasp_stable_steps = max(1, int(round(max(float(args.pregrasp_stable_time), ctrl_dt) / ctrl_dt)))
                        if success_counter >= pregrasp_stable_steps:
                            task_state = "FINAL_APPROACH"
                            success_counter = 0
                            final_approach_counter = 0
                            tcp_rot = _quat_to_rotmat_wxyz(tcp_quat_after)
                            tcp_app = tcp_rot @ np.asarray(pregrasp_gate_local_axis, dtype=np.float64).reshape(3)
                            tcp_app /= max(float(np.linalg.norm(tcp_app)), 1e-12)
                            axis_align = _axis_alignment_errors_deg(tcp_quat_after, approach_axis)
                            pose_axes = _grasp_pose_axis_debug(
                                tcp_quat_after,
                                grasp_quat,
                                approach_axis,
                                pregrasp_gate_local_axis,
                                model=model,
                                ids=ids,
                                q=q_after,
                            )
                            print(
                                f"[ep {ep:03d}][grasp] pregrasp reached at t={k * ctrl_dt:.2f}s "
                                f"dist={dist*1000:.1f}mm "
                                f"quat_err={_quat_angle_deg(tcp_quat_after, grasp_quat):.1f}deg "
                                f"approach_err={_axis_angle_deg(tcp_app, approach_axis):.1f}deg "
                                f"tcp_quat=({tcp_quat_after[0]:+.3f},{tcp_quat_after[1]:+.3f},{tcp_quat_after[2]:+.3f},{tcp_quat_after[3]:+.3f}) "
                                f"desired_quat=({grasp_quat[0]:+.3f},{grasp_quat[1]:+.3f},{grasp_quat[2]:+.3f},{grasp_quat[3]:+.3f}) "
                                f"tcp_app=({tcp_app[0]:+.2f},{tcp_app[1]:+.2f},{tcp_app[2]:+.2f}) "
                                f"desired_app=({approach_axis[0]:+.2f},{approach_axis[1]:+.2f},{approach_axis[2]:+.2f}) "
                                f"axis_align[{_format_axis_alignment(axis_align)}] "
                                f"{_format_grasp_axis_debug(pose_axes)} → FINAL_APPROACH"
                            )
                    elif task_state == "FINAL_APPROACH":
                        final_approach_counter += 1
                        final_err = float(np.linalg.norm(tcp_after - grasp_pos))
                        contact_ready = (
                            bool(args.grasp_close_on_contact)
                            and target_gripper_contact_count >= int(args.grasp_close_contact_count)
                            and final_err <= float(args.grasp_close_contact_max_dist)
                        )
                        if final_err <= float(args.final_grasp_dist) or contact_ready:
                            success_counter += 1
                        else:
                            success_counter = 0
                        force_close = False
                        if bool(args.grasp_close_on_timeout) and final_approach_counter >= final_approach_timeout_steps:
                            force_close = True
                        final_stable_steps = max(
                            int(args.grasp_final_stable_steps),
                            int(round(max(float(args.grasp_final_stable_time), ctrl_dt) / ctrl_dt)),
                        )
                        if success_counter >= final_stable_steps or force_close:
                            task_state = "CLOSE"
                            success_counter = 0
                            close_counter = 0
                            frozen_grasp_q = joint_pos(data, ids).copy()
                            close_start_q = frozen_grasp_q.copy()
                            if force_close and final_err > float(args.final_grasp_dist):
                                reason = "timeout"
                            elif contact_ready:
                                reason = "contact"
                            else:
                                reason = "stable"
                            target_now = _body_pos_or_default(model, data, str(args.target_body), target_pos)
                            tcp_vs_target = _pos_compare_text(tcp_after, target_now)
                            grasp_vs_target = _pos_compare_text(grasp_pos, target_now)
                            tcp_rot = _quat_to_rotmat_wxyz(tcp_quat_after)
                            tcp_app = tcp_rot @ np.asarray(pregrasp_gate_local_axis, dtype=np.float64).reshape(3)
                            tcp_app /= max(float(np.linalg.norm(tcp_app)), 1e-12)
                            axis_align = _axis_alignment_errors_deg(tcp_quat_after, approach_axis)
                            pose_axes = _grasp_pose_axis_debug(
                                tcp_quat_after,
                                grasp_quat,
                                approach_axis,
                                pregrasp_gate_local_axis,
                                model=model,
                                ids=ids,
                                q=q_after,
                            )
                            print(
                                f"[ep {ep:03d}][grasp] final reached at t={k * ctrl_dt:.2f}s "
                                f"dist={final_err*1000:.1f}mm reason={reason} "
                                f"counter={final_approach_counter}/{final_approach_timeout_steps} "
                                f"quat_err={_quat_angle_deg(tcp_quat_after, grasp_quat):.1f}deg "
                                f"approach_err={_axis_angle_deg(tcp_app, approach_axis):.1f}deg "
                                f"target_contacts={target_contact_count} gripper_contacts={target_gripper_contact_count} "
                                f"tcp=({tcp_after[0]:+.3f},{tcp_after[1]:+.3f},{tcp_after[2]:+.3f}) "
                                f"target=({target_now[0]:+.3f},{target_now[1]:+.3f},{target_now[2]:+.3f}) "
                                f"grasp=({grasp_pos[0]:+.3f},{grasp_pos[1]:+.3f},{grasp_pos[2]:+.3f}) "
                                f"tcp_quat=({tcp_quat_after[0]:+.3f},{tcp_quat_after[1]:+.3f},{tcp_quat_after[2]:+.3f},{tcp_quat_after[3]:+.3f}) "
                                f"desired_quat=({grasp_quat[0]:+.3f},{grasp_quat[1]:+.3f},{grasp_quat[2]:+.3f},{grasp_quat[3]:+.3f}) "
                                f"tcp_app=({tcp_app[0]:+.2f},{tcp_app[1]:+.2f},{tcp_app[2]:+.2f}) "
                                f"desired_app=({approach_axis[0]:+.2f},{approach_axis[1]:+.2f},{approach_axis[2]:+.2f}) "
                                f"axis_align[{_format_axis_alignment(axis_align)}] "
                                f"{_format_grasp_axis_debug(pose_axes)} "
                                f"tcp_vs_target[{tcp_vs_target}] grasp_vs_target[{grasp_vs_target}] "
                                f"hold_q={np.array2string(frozen_grasp_q, precision=3, separator=',')} → CLOSE"
                            )
                    elif task_state == "CLOSE":
                        close_counter += 1
                        if close_counter >= close_steps:
                            target_released = True
                            task_state = "LIFT"
                            lift_counter = 0
                            tcp_now, _ = tcp_pose_w(data, ids)
                            contacts_now = _geom_contact_count(model, data, str(args.target_geom))
                            gripper_contacts_now = _geom_contact_count_with_body(model, data, str(args.target_geom), GRIPPER_BODY)
                            contact_pairs_now = _target_contact_pairs(model, data, str(args.target_geom), max_pairs=6)
                            target_now = _body_pos_or_default(model, data, str(args.target_body), target_pos)
                            _, tcp_quat_now = tcp_pose_w(data, ids)
                            pose_axes = _grasp_pose_axis_debug(
                                tcp_quat_now,
                                grasp_quat,
                                approach_axis,
                                pregrasp_gate_local_axis,
                                model=model,
                                ids=ids,
                                q=q_after,
                            )
                            print(
                                f"[ep {ep:03d}][grasp] close complete at t={k * ctrl_dt:.2f}s "
                                f"tcp_err={float(np.linalg.norm(tcp_now - grasp_pos))*1000:.1f}mm "
                                f"tcp=({tcp_now[0]:+.3f},{tcp_now[1]:+.3f},{tcp_now[2]:+.3f}) "
                                f"target=({target_now[0]:+.3f},{target_now[1]:+.3f},{target_now[2]:+.3f}) "
                                f"tcp_vs_target[{_pos_compare_text(tcp_now, target_now)}] "
                                f"{_format_grasp_axis_debug(pose_axes)} "
                                f"gripper_q={q_after[-1]:.3f} target_contacts={contacts_now} "
                                f"gripper_contacts={gripper_contacts_now} "
                                f"pairs={[(p.get('other_geom'), p.get('other_body')) for p in contact_pairs_now]} → LIFT"
                            )
                    elif task_state == "REPLAN_GRASP":
                        replan_wait_counter += 1
                        replan_err = float(np.linalg.norm(tcp_after - pregrasp_pos))
                        replan_ready = replan_err <= float(args.grasp_replan_ready_dist)
                        replan_timeout = replan_wait_counter >= replan_wait_steps
                        replan_debug = {
                            "state": "waiting",
                            "wait_counter": int(replan_wait_counter),
                            "wait_steps": int(replan_wait_steps),
                            "ready": bool(replan_ready),
                            "timeout": bool(replan_timeout),
                            "ready_dist_m": float(args.grasp_replan_ready_dist),
                            "err_m": float(replan_err),
                            "compute_attempts": int(replan_compute_attempts),
                            "grasp_attempts": int(replan_attempts),
                        }
                        if replan_wait_counter == 1 or (replan_wait_counter % replan_report_steps == 0):
                            wait_reason = "ready" if replan_ready else (
                                "timeout" if replan_timeout else "waiting_for_pregrasp_or_settle"
                            )
                            print(
                                f"[ep {ep:03d}][grasp_replan] stage=WAIT "
                                f"reason={wait_reason} err={replan_err*1000.0:.1f}mm "
                                f"ready<{float(args.grasp_replan_ready_dist)*1000.0:.1f}mm "
                                f"wait={replan_wait_counter}/{replan_wait_steps} "
                                f"compute={replan_compute_attempts}/{int(args.grasp_replan_max_compute_attempts)}; "
                                "no new grasp yet"
                            )
                        if replan_ready or replan_timeout:
                            replan_compute_attempts += 1
                            target_pos = _body_pos_or_default(model, data, str(args.target_body), target_pos)
                            target_plan_pos = target_pos.copy()
                            mujoco.mj_forward(model, data)
                            print(
                                f"[ep {ep:03d}][grasp_replan] stage=COMPUTE "
                                f"attempt={replan_compute_attempts}/{int(args.grasp_replan_max_compute_attempts)} "
                                f"target=({target_pos[0]:+.3f},{target_pos[1]:+.3f},{target_pos[2]:+.3f})"
                            )
                            replan_debug.update(
                                {
                                    "state": "compute",
                                    "compute_attempts": int(replan_compute_attempts),
                                    "target_pos": _arr(target_pos),
                                }
                            )
                            if anygrasp_bridge is None:
                                raise RuntimeError("grasp chain requires AnyGrasp bridge")
                            try:
                                grasp_pos, pregrasp_pos, approach_axis, grasp_quat, cand = _choose_anygrasp_candidate(
                                    anygrasp_bridge,
                                    model,
                                    data,
                                    ids,
                                    target_pos,
                                    target_radius,
                                    float(args.pregrasp_distance),
                                    float(args.anygrasp_candidate_center_tolerance),
                                    approach_local_axis=approach_local_axis,
                                    enable_ik_filter=bool(args.anygrasp_ik_filter),
                                    ik_steps=int(args.anygrasp_ik_steps),
                                    ik_pos_tol=float(args.anygrasp_ik_pos_tol),
                                    ik_approach_tol_deg=float(args.anygrasp_ik_approach_tol_deg),
                                    approach_gate_axis="tcp_z",
                                    debug_axes=bool(args.debug_anygrasp_axes),
                                    debug_axes_count=int(args.debug_anygrasp_axes_count),
                                )
                            except Exception as exc:
                                max_compute = max(1, int(args.grasp_replan_max_compute_attempts))
                                replan_debug.update({"state": "failed", "error": str(exc)})
                                if replan_compute_attempts < max_compute:
                                    replan_wait_counter = max(0, replan_wait_steps - replan_retry_steps)
                                    print(
                                        f"[ep {ep:03d}][grasp_replan] AnyGrasp compute failed "
                                        f"{replan_compute_attempts}/{max_compute}: {exc}; retry"
                                    )
                                    continue
                                replan_final_err = float(np.linalg.norm(tcp_after - grasp_pos))
                                close_after_replan_fail = (
                                    replan_final_err <= float(args.grasp_track_activate_dist)
                                    or target_gripper_contact_count > 0
                                )
                                if close_after_replan_fail:
                                    task_state = "CLOSE"
                                    success_counter = 0
                                    close_counter = 0
                                    frozen_grasp_q = joint_pos(data, ids).copy()
                                    close_start_q = frozen_grasp_q.copy()
                                    replan_debug.update(
                                        {
                                            "state": "close_after_compute_failed",
                                            "final_err_m": float(replan_final_err),
                                            "target_gripper_contacts": int(target_gripper_contact_count),
                                            "reason": "near_grasp_or_contact",
                                        }
                                    )
                                    print(
                                        f"[ep {ep:03d}][grasp_replan] AnyGrasp compute failed "
                                        f"{replan_compute_attempts}/{max_compute}: {exc}; "
                                        f"near current grasp ({replan_final_err*1000.0:.1f}mm) "
                                        f"or contacts={target_gripper_contact_count}, forcing CLOSE"
                                    )
                                    continue
                                print(
                                    f"[ep {ep:03d}][grasp_replan] AnyGrasp compute failed "
                                    f"{replan_compute_attempts}/{max_compute}: {exc}; ending episode as failed"
                                )
                                task_state = "VERIFY"
                                success_latched = False
                                success_step = -1
                                if bool(args.stop_on_success):
                                    break
                                continue
                            selected_grasp = cand
                            grasp_candidates_viz = list(getattr(anygrasp_bridge, "last_candidates", []))
                            rec = _anygrasp_debug_record(
                                ep=ep,
                                target_idx=idx,
                                target_pos=target_pos,
                                target_radius=target_radius,
                                bridge=anygrasp_bridge,
                                selected_grasp=selected_grasp,
                                pregrasp_pos=pregrasp_pos,
                                grasp_pos=grasp_pos,
                                grasp_quat=grasp_quat,
                                approach_axis=approach_axis,
                            )
                            _append_jsonl(args.anygrasp_debug_log, rec)
                            cand_msg = (
                                f"AnyGrasp score={float(cand.score):.3f} width={float(cand.width)*1000:.1f}mm "
                                f"cand_dist={float(np.linalg.norm(cand.pos_world - target_pos))*1000:.1f}mm"
                            )
                            pregrasp_plan_pos = pregrasp_pos.copy()
                            grasp_plan_pos = grasp_pos.copy()
                            if grasp_tracker is not None:
                                grasp_tracker.reset()
                            grasp_track_invalid_counter = 0
                            grasp_track_ever_valid = False
                            replan_attempts += 1
                            replan_compute_attempts = 0
                            replan_debug.update(
                                {
                                    "state": "success",
                                    "grasp_attempts": int(replan_attempts),
                                    "pregrasp_pos": _arr(pregrasp_pos),
                                    "grasp_pos": _arr(grasp_pos),
                                }
                            )
                            final_dist = float(np.linalg.norm(grasp_pos - pregrasp_pos))
                            final_approach_steps = max(
                                1,
                                int(math.ceil(final_dist / max(float(args.final_approach_speed) * ctrl_dt, 1e-5))),
                            )
                            final_approach_timeout_steps = max(
                                final_approach_steps,
                                int(math.ceil(final_approach_steps * max(float(args.grasp_final_timeout_scale), 1.0))),
                            )
                            task_state = "MOVE_TO_PREGRASP"
                            success_counter = 0
                            final_approach_counter = 0
                            close_counter = 0
                            replan_debug = {}
                            frozen_grasp_q = None
                            close_start_q = None
                            print(
                                f"[ep {ep:03d}][grasp_replan] attempt={replan_attempts} "
                                f"target=({target_pos[0]:+.3f},{target_pos[1]:+.3f},{target_pos[2]:+.3f}) "
                                f"pre=({pregrasp_pos[0]:+.3f},{pregrasp_pos[1]:+.3f},{pregrasp_pos[2]:+.3f}) "
                                f"final=({grasp_pos[0]:+.3f},{grasp_pos[1]:+.3f},{grasp_pos[2]:+.3f}) "
                                f"approach=({approach_axis[0]:+.2f},{approach_axis[1]:+.2f},{approach_axis[2]:+.2f}) "
                                f"{cand_msg} → MOVE_TO_PREGRASP"
                            )
                    elif task_state == "LIFT":
                        lift_counter += 1
                        if lift_counter >= lift_steps:
                            target_now = _body_pos_or_default(model, data, str(args.target_body), target_pos)
                            lift_delta = float(target_now[2] - target_plan_pos[2])
                            lifted = lift_delta >= float(args.grasp_lift_success_height)
                            if lifted:
                                task_state = "VERIFY"
                                verify_hold_q = q_after.copy()
                                success_latched = True
                                success_step = k
                                print(
                                    f"[ep {ep:03d}][grasp] lift/verify at t={k * ctrl_dt:.2f}s "
                                    f"target_lift={lift_delta*1000.0:.1f}mm"
                                )
                                if bool(args.stop_on_success):
                                    break
                            elif replan_attempts < int(args.grasp_replan_max_attempts):
                                task_state = "REPLAN_GRASP"
                                replan_wait_counter = 0
                                replan_debug = {"state": "enter", "reason": "lift_failed"}
                                target_released = False
                                success_counter = 0
                                frozen_grasp_q = None
                                close_start_q = None
                                verify_hold_q = None
                                print(
                                    f"[ep {ep:03d}][grasp] lift failed at t={k * ctrl_dt:.2f}s "
                                    f"target_lift={lift_delta*1000.0:.1f}mm; replan"
                                )
                            else:
                                task_state = "VERIFY"
                                verify_hold_q = q_after.copy()
                                success_latched = False
                                success_step = -1
                                print(
                                    f"[ep {ep:03d}][grasp] lift failed at t={k * ctrl_dt:.2f}s "
                                    f"target_lift={lift_delta*1000.0:.1f}mm; no replan attempts left"
                                )
                                if bool(args.stop_on_success):
                                    break
                elif task_state == "APPROACH":
                    if dist <= float(args.success_dist):
                        success_counter += 1
                    else:
                        success_counter = 0
                    if success_counter >= int(args.success_steps):
                        success_latched = True
                        success_step = k
                        if max_settle_steps > 0:
                            task_state = "SETTLE"
                            settle_steps = 0
                            if str(args.settle_mode) == "hold_q":
                                hold_target_q = joint_pos(data, ids).copy()
                                tgt = hold_target_q.copy()
                                set_ctrl(data, ids, tgt)
                            print(
                        f"[ep {ep:03d}] success latch at t={k * ctrl_dt:.2f}s "
                        f"dist={dist*1000:.1f}mm → SETTLE {float(args.settle_on_success):.2f}s "
                                f"mode={args.settle_mode}"
                            )
                        elif bool(args.stop_on_success):
                            task_state = "SUCCESS"
                            print(
                        f"[ep {ep:03d}] success at t={k * ctrl_dt:.2f}s "
                        f"dist={dist*1000:.1f}mm"
                            )
                            break
                elif task_state == "SETTLE":
                    settle_steps += 1
                    if settle_steps >= max_settle_steps:
                        task_state = "SUCCESS"
                        print(
                            f"[ep {ep:03d}] settle complete at t={k * ctrl_dt:.2f}s "
                            f"dist={dist*1000:.1f}mm"
                        )
                        if bool(args.stop_on_success):
                            break

                if viewer is not None:
                    _draw_overlays(
                        viewer,
                        target_pos,
                        draw_target=not bool(args.enable_grasp_chain),
                        grasp_candidates=grasp_candidates_viz,
                        selected_grasp=selected_grasp,
                        pregrasp_pos=pregrasp_pos if bool(args.enable_grasp_chain) else None,
                        grasp_pos=grasp_pos if bool(args.enable_grasp_chain) else None,
                )
                    viewer.sync()
                if cam_preview is not None:
                    cam_preview.update(data)
                if sleep_s > 0:
                    time.sleep(sleep_s)

                verbose_steps = max(1, int(round(float(args.verbose_interval) / ctrl_dt)))
                if args.verbose and (k % verbose_steps == 0):
                    tcp, _ = tcp_pose_w(data, ids)
                    cbf_msg = ""
                    if args.enable_cbf:
                        cbf_msg = (
                            f"  h_min={info.get('h_min', float('nan'))*1000:.1f}mm"
                            f"  @{info.get('cbf_worst_monitor', '?')}"
                            f"  cbf={'Y' if info.get('cbf_active') else 'n'}"
                            f"  feas={'Y' if info.get('cbf_feasible', True) else 'N'}"
                            f"  proj={'Y' if info.get('cbf_projected') else 'n'}"
                            f"  n={info.get('n_constraints', 0)}"
                            f"  |dq_cbf|={info.get('dq_cbf_norm', 0.0):.4f}"
                        )
                        if args.vision_debug and obs_source is not None:
                            dbg = getattr(obs_source, "last_debug", None)
                            if dbg is not None:
                                cbf_msg += (
                                    f"  vis_pts={getattr(dbg, 'n_roi', 0)}"
                                    f"  vis_det={'Y' if getattr(dbg, 'detected', False) else 'n'}"
                                )
                                if hasattr(dbg, "n_sdf_points"):
                                    cbf_msg += (
                                        f"  sdf_pts={getattr(dbg, 'n_sdf_points', 0)}"
                                        f"  self_rm={getattr(dbg, 'n_self_filtered', 0)}"
                                    )
                                center_err_mm = getattr(dbg, "center_err_mm", None)
                                if center_err_mm is not None:
                                    cbf_msg += f"  vis_err={center_err_mm:.1f}mm"
                    print(
                        f"  t={k * ctrl_dt:5.2f}s  dist={dist*1000:.1f}mm  "
                        f"ori={ori:.1f}deg  state={task_state}  "
                        f"tcp=({tcp_after[0]:.3f},{tcp_after[1]:.3f},{tcp_after[2]:.3f})  "
                        f"ctrl=({control_target_pos[0]:.3f},{control_target_pos[1]:.3f},{control_target_pos[2]:.3f})  "
                        f"ctrl_err={float(np.linalg.norm(tcp_after - control_target_pos))*1000:.1f}mm  "
                        f"final_err={float(np.linalg.norm(tcp_after - grasp_pos))*1000.0 if bool(args.enable_grasp_chain) else float('nan'):.1f}mm  "
                        f"contacts={target_contact_count}/{target_gripper_contact_count}  "
                        f"|dq|={float(info.get('dq_total_norm', 0.0)):.4f}"
                        + (
                            f"  wrist_err={float(grasp_track_debug.get('wrist_pos_err_norm_m', float('nan'))) * 1000.0:.1f}mm"
                            if bool(args.enable_grasp_chain)
                            and isinstance(grasp_track_debug, dict)
                            and grasp_track_debug.get("wrist_pos_err_norm_m") is not None
                            else ""
                        )
                        + f"{cbf_msg}"
                    )

            wall = time.perf_counter() - t0
            tcp, _ = tcp_pose_w(data, ids)
            print(
                f"[ep {ep:03d}] idx={idx}  best_dist={best_dist*1000:.2f}mm  "
                f"best_ori={best_ori:.1f}deg  "
                f"end_dist={float(np.linalg.norm(tcp - target_pos))*1000:.2f}mm  "
                f"arm_obstacle_contacts={arm_obstacle_contact_steps}  "
                f"state={task_state}  success_step={success_step}  wall={wall:.1f}s"
            )
            if cbf_stats is not None:
                print(cbf_stats.summary_line(ep))
            ep += 1

        # 有界面时：跑完后别立刻 close（易段错误），等用户关窗口
        if viewer is not None and viewer.is_running():
            print("[mujoco_play] 回合结束，关闭窗口退出…")
            while viewer.is_running():
                viewer.sync()
                time.sleep(0.05)
    finally:
        if cam_preview is not None:
            cam_preview.close()
        if obs_source is not None and hasattr(obs_source, "close"):
            obs_source.close()
        if anygrasp_bridge is not None:
            anygrasp_bridge.close()
        if grasp_tracker is not None and hasattr(grasp_tracker, "close"):
            grasp_tracker.close()
        # 用户已关窗时再 close 容易 segfault，跳过即可
        pass

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SO-100 Reach MuJoCo play")
    p.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument("--npz", type=str, default=str(DEFAULT_NPZ_TEST))
    p.add_argument("--use-train-npz", action="store_true")
    p.add_argument("--episodes", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--target-idx", type=int, default=-1, help=">=0 时固定使用指定 target bank index")
    p.add_argument("--action-scale", type=float, default=ACTION_SCALE)
    p.add_argument("--filter-tau", type=float, default=ACTION_FILTER_TAU)
    p.add_argument("--cbf-filter-tau", type=float, default=CBF_FILTER_TAU)
    p.add_argument("--cbf-correction-filter", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--cbf-bypass-filter-when-unsafe", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--headless", action="store_true")
    p.add_argument(
        "--hold-home",
        type=float,
        default=0.0,
        help="3D 窗口打开后于 home 位暂停 N 秒（检查相机安装），再开始 episode",
    )
    p.add_argument(
        "--show-cam",
        "--view",
        action="store_true",
        help="弹出 OpenCV 窗口显示固定/腕部相机画面（--view 同义）",
    )
    p.add_argument(
        "--cam-depth",
        action="store_true",
        help="配合 --show-cam，额外显示固定相机深度伪彩",
    )
    p.add_argument(
        "--cam-backend",
        type=str,
        default="auto",
        choices=("auto", "cv2", "mpl", "save"),
        help="相机预览后端：auto 依次尝试 cv2→matplotlib→写 PNG",
    )
    p.add_argument(
        "--cam-save-dir",
        type=str,
        default="",
        help="cam-backend=save 时的输出目录（默认 log/runtime/vision_preview）",
    )
    p.add_argument(
        "--realtime",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="按仿真时间 sleep；有界面默认开，--no-realtime 可关",
    )
    p.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="播放倍率，0.5=半速更易看过程",
    )
    p.add_argument("--verbose", action="store_true", help="按 --verbose-interval 打印当前误差")
    p.add_argument("--verbose-interval", type=float, default=3.0, help="--verbose 状态行打印间隔 (s)")
    p.add_argument(
        "--success-dist",
        type=float,
        default=0.03,
        help="任务状态机：TCP 连续进入该位置半径 (m) 后判定到达",
    )
    p.add_argument(
        "--success-steps",
        type=int,
        default=10,
        help="任务状态机：连续多少个控制步在 success-dist 内才 latch",
    )
    p.add_argument(
        "--settle-on-success",
        type=float,
        default=0.0,
        help="任务状态机：到达后锁当前关节目标驻留多少秒；0=不驻留",
    )
    p.add_argument(
        "--settle-mode",
        type=str,
        default="hold_q",
        choices=("hold_q", "policy_soft_cbf"),
        help="SETTLE 阶段控制方式：hold_q=锁关节；policy_soft_cbf=继续 policy 但削弱 CBF",
    )
    p.add_argument("--settle-cbf-d-safe", type=float, default=0.005, help="policy_soft_cbf: SETTLE 阶段 CBF d_safe")
    p.add_argument("--settle-cbf-gamma", type=float, default=0.3, help="policy_soft_cbf: SETTLE 阶段 CBF gamma")
    p.add_argument("--settle-cbf-activate-margin", type=float, default=0.015, help="policy_soft_cbf: SETTLE 阶段 CBF 激活阈值")
    p.add_argument("--settle-cbf-lambda", type=float, default=0.5, help="policy_soft_cbf: SETTLE 阶段 CBF lambda")
    p.add_argument(
        "--stop-on-success",
        action="store_true",
        help="任务状态机：到达/驻留完成后结束当前 episode",
    )
    p.add_argument(
        "--enable-grasp-chain",
        action="store_true",
        help="启用静态目标物体的到达+pregrasp+final approach+close+lift 抓取链路",
    )
    p.add_argument(
        "--enable-obstacle",
        action="store_true",
        help="grasp-chain 下加载带障碍物场景；默认抓取用 norod 场景，避免障碍支线干扰抓取调试",
    )
    p.add_argument(
        "--enable-sdf-cbf-qp",
        action="store_true",
        help="便捷开启 SDF + CBF-QP 避障；会自动 enable-cbf，且默认 obstacle-source 从 geom 切到 geom_sdf",
    )
    p.add_argument(
        "--grasp-target-object",
        choices=("cube", "bottle", "sphere", "custom"),
        default="cube",
        help="抓取目标物体选择：cube=默认方块；bottle=红色圆柱水瓶；sphere=红色圆球；custom=使用 --target-body/--target-geom",
    )
    p.add_argument("--target-body", type=str, default="target_object", help="实体目标 body 名")
    p.add_argument("--target-geom", type=str, default="target_object_geom", help="实体目标 geom 名")
    p.add_argument("--target-radius", type=float, default=0.018, help="目标半径 fallback (m)，主要用于候选中心距离阈值")
    p.add_argument(
        "--grasp-source",
        type=str,
        default="anygrasp",
        choices=("anygrasp", "external"),
        help="抓取位姿来源：anygrasp=play.py 内部计算；external=使用外部传入 pre/final/quaternion",
    )
    p.add_argument("--external-pregrasp-pos", type=str, default="", help="external grasp pregrasp 世界坐标 x,y,z")
    p.add_argument("--external-grasp-pos", type=str, default="", help="external grasp final 世界坐标 x,y,z")
    p.add_argument("--external-grasp-quat", type=str, default="1,0,0,0", help="external grasp TCP 目标姿态 w,x,y,z")
    p.add_argument("--external-gripper-width", type=float, default=0.0, help="external grasp 候选夹爪宽度，仅用于日志 (m)")
    p.add_argument("--pregrasp-distance", type=float, default=0.040, help="tar&ori 风格 pregrasp：从 final grasp 沿 approach 后退的距离 (m)")
    p.add_argument("--pregrasp-success-dist", type=float, default=0.035, help="pregrasp 到达阈值 (m)")
    p.add_argument("--pregrasp-approach-success-deg", type=float, default=60.0, help="pregrasp 进入 final 前允许的进刀轴角度误差 (deg)")
    p.add_argument("--pregrasp-stable-time", type=float, default=0.05, help="pregrasp 连续稳定多久后进入 final (s)")
    p.add_argument("--final-grasp-dist", type=float, default=0.010, help="final grasp 到达阈值 (m)")
    p.add_argument("--grasp-final-stable-time", type=float, default=0.10, help="final grasp 连续稳定多久后冻结手臂并闭合 (s)")
    p.add_argument("--grasp-final-stable-steps", type=int, default=0, help="final grasp 额外稳定步数下限；0 表示只使用 --grasp-final-stable-time")
    p.add_argument(
        "--grasp-final-timeout-scale",
        type=float,
        default=2.0,
        help="grasp_close_on_timeout 开启时，final approach 内部强制闭合等待步数倍率",
    )
    p.add_argument(
        "--grasp-close-on-contact",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="final approach 中目标与夹爪接触且距离不超过上限时冻结手臂并闭合",
    )
    p.add_argument("--grasp-close-contact-count", type=int, default=1, help="触发闭合所需目标 geom 接触数量")
    p.add_argument("--grasp-close-contact-max-dist", type=float, default=0.030, help="接触触发闭合时允许的最大 TCP-final 距离 (m)")
    p.add_argument(
        "--grasp-close-on-timeout",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="final approach 路径走完但未满足 final 阈值时是否仍强制闭合",
    )
    p.add_argument("--final-approach-speed", type=float, default=0.025, help="final/lift Cartesian servo 速度上限 (m/s)")
    p.add_argument("--grasp-open-q", type=float, default=1.2, help="抓取链路中夹爪打开关节目标")
    p.add_argument("--grasp-close-q", type=float, default=0.4, help="抓取链路中夹爪闭合关节目标")
    p.add_argument("--grasp-close-time", type=float, default=0.8, help="闭合夹爪持续时间 (s)")
    p.add_argument("--grasp-lift-height", type=float, default=0.035, help="闭合后上抬高度 (m)")
    p.add_argument("--grasp-lift-time", type=float, default=0.8, help="上抬验证最长时间 (s)")
    p.add_argument("--grasp-lift-success-height", type=float, default=0.015, help="目标物体被抬高至少该高度才判定抓取成功 (m)")
    p.add_argument("--grasp-episode-time-scale", type=float, default=2.0, help="grasp-chain episode 时长倍率，给二次重规划/抓取留时间")
    p.add_argument(
        "--grasp-track-object",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="抓取过程中跟踪目标物体小位移：更新 pregrasp/final 目标；大位移进入重规划",
    )
    p.add_argument("--grasp-track-gain", type=float, default=1.0, help="目标小位移跟踪增益")
    p.add_argument(
        "--grasp-track-source",
        choices=("gt", "wrist", "none"),
        default="wrist",
        help="抓取近场目标追踪来源：gt=MuJoCo目标真值；wrist=腕部相机seg/depth诊断；none=关闭tracker",
    )
    p.add_argument(
        "--grasp-wrist-flip-image-y",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="腕部相机seg/depth反投影时是否翻转图像y轴；用于诊断相机画面上下反导致的世界坐标偏差",
    )
    p.add_argument("--grasp-track-max-delta", type=float, default=0.020, help="允许继续跟踪的目标最大位移 (m)")
    p.add_argument(
        "--grasp-track-activate-dist",
        type=float,
        default=0.080,
        help="TCP 距 final grasp 小于该距离后才允许腕部/目标 tracking 更新 grasp 或触发重规划 (m)",
    )
    p.add_argument(
        "--grasp-track-max-invalid-frames",
        type=int,
        default=3,
        help="tracker 连续失效超过该控制步数后触发重规划",
    )
    p.add_argument("--grasp-tracking-close-time", type=float, default=0.40, help="CLOSE 初期继续让 policy 跟踪目标的时间 (s)")
    p.add_argument("--grasp-replan-delta", type=float, default=0.030, help="目标位移超过该值后放弃当前 grasp 并重跑 AnyGrasp (m)")
    p.add_argument("--grasp-replan-max-attempts", type=int, default=1, help="单个 episode 内最多重跑 AnyGrasp 次数")
    p.add_argument("--grasp-replan-max-compute-attempts", type=int, default=3, help="每次重规划最多重试 AnyGrasp 计算次数")
    p.add_argument("--grasp-replan-ready-dist", type=float, default=0.018, help="REPLAN_GRASP 回撤到 pregrasp 小于该误差后立即重算 AnyGrasp (m)")
    p.add_argument("--grasp-replan-retry-time", type=float, default=0.25, help="重规划 AnyGrasp 计算失败后的重试等待时间 (s)")
    p.add_argument("--grasp-replan-report-interval", type=float, default=0.5, help="REPLAN_GRASP 等待阶段状态提示打印间隔 (s)")
    p.add_argument("--grasp-replan-settle-time", type=float, default=0.75, help="重跑 AnyGrasp 前等待物体稳定的时间 (s)")
    p.add_argument(
        "--grasp-target-on-floor",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="grasp-chain 下将目标实体放到地面：使用 target bank 的 x/y，z=球半径+clearance",
    )
    p.add_argument("--grasp-target-min-x", type=float, default=0.42, help="grasp-chain 落地目标 x 方向最小位置，避免目标离 base 过近 (m)")
    p.add_argument("--grasp-target-floor-clearance", type=float, default=0.001, help="地面目标球中心额外高度 (m)")
    p.add_argument(
        "--grasp-target-pos",
        type=str,
        default="",
        help="grasp-chain 目标实体显式世界坐标 x,y,z；非空时跳过 bank/min-x/floor 自动放置",
    )
    p.add_argument("--grasp-object-settle-time", type=float, default=0.75, help="放置动态目标后，计算抓取前先纯物理稳定的时间 (s)")
    p.add_argument(
        "--grasp-start-mode",
        type=str,
        default="bank_ready",
        choices=("home", "bank_ready", "bank_idx"),
        help="grasp-chain 机器人初始姿态：home=旧低姿态；bank_ready=从 workspace joint_pos 自动选高位 ready；bank_idx=指定 index",
    )
    p.add_argument(
        "--grasp-start-bank-idx",
        type=int,
        default=-1,
        help="grasp-chain 起始 workspace joint_pos index；-1 时 bank_ready 自动选择",
    )
    p.add_argument("--ee-tcp-offset", type=str, default="0,0,0", help="机器人 EE/TCP 局部坐标下的 TCP 定义偏置 xyz(m)；作用于当前 TCP pose，不移动 AnyGrasp 目标")
    p.add_argument(
        "--grasp-pin-target-until-close",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="调试悬空目标用：闭合前每步锁定实体目标位置；默认关闭以验证真实物理抓取",
    )
    p.add_argument(
        "--anygrasp-checkpoint",
        type=str,
        default=str(Path("anygrasp_sdk/grasp_detection/log/checkpoint_detection.tar")),
        help="AnyGrasp detection checkpoint",
    )
    p.add_argument("--anygrasp-top-k", type=int, default=45, help="AnyGrasp 候选保留数量")
    p.add_argument("--anygrasp-conda-env", type=str, default="graspnet_gpu", help="运行 AnyGrasp worker 的 conda 环境名")
    p.add_argument("--anygrasp-min-score", type=float, default=0.01, help="AnyGrasp 最低 score")
    p.add_argument("--anygrasp-max-width", type=float, default=0.10, help="AnyGrasp 最大夹爪宽度 (m)")
    p.add_argument(
        "--anygrasp-ik-filter",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="对 AnyGrasp 候选做数值 IK + 关节限位筛选",
    )
    p.add_argument("--anygrasp-ik-steps", type=int, default=80, help="每个 AnyGrasp 候选用于数值 IK 筛选的迭代步数")
    p.add_argument("--anygrasp-ik-pos-tol", type=float, default=0.005, help="AnyGrasp IK 筛选 pregrasp 位置误差阈值 (m)")
    p.add_argument("--anygrasp-ik-approach-tol-deg", type=float, default=3.0, help="AnyGrasp IK 筛选 approach 角误差阈值 (deg)")
    p.add_argument(
        "--anygrasp-mask-source",
        type=str,
        default="target_geom_seg",
        choices=("target_geom_seg", "roi"),
        help="AnyGrasp 输入 mask：target_geom_seg=仿真固定目标 geom mask；roi=旧版目标中心球形 ROI",
    )
    p.add_argument("--anygrasp-target-mask-dilate-px", type=int, default=0, help="target_geom_seg mask 像素膨胀半径")
    p.add_argument("--anygrasp-target-mask-expand-ratio", type=float, default=0.0, help="target_geom_seg mask bbox 扩张比例")
    p.add_argument(
        "--anygrasp-candidate-center-tolerance",
        type=float,
        default=0.03,
        help="候选 grasp center 允许超出目标半径的距离 (m)",
    )
    p.add_argument("--anygrasp-target-roi-radius", type=float, default=0.10, help="以目标中心裁剪 AnyGrasp 输入点云的半径 (m)")
    p.add_argument("--anygrasp-debug-log", type=str, default="log/runtime/anygrasp_debug.jsonl", help="AnyGrasp mask/candidate/selected JSONL 诊断日志")
    p.add_argument("--debug-anygrasp-frame", action="store_true", help="只显示/记录 AnyGrasp mask 与候选坐标，不执行机械臂动作")
    p.add_argument("--debug-anygrasp-frame-preview-time", type=float, default=5.0, help="debug-anygrasp-frame + show-cam 时保存相机预览前持续刷新仿真的时间 (s)")
    p.add_argument("--debug-anygrasp-axes", action="store_true", help="打印 AnyGrasp 候选三列旋转轴与候选->目标中心方向的夹角")
    p.add_argument("--debug-anygrasp-axes-count", type=int, default=20, help="debug-anygrasp-axes 打印的候选数量")
    p.add_argument(
        "--anygrasp-collision-detection",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="是否启用 AnyGrasp 自带局部 collision_detection",
    )
    p.add_argument(
        "--target-motion",
        type=str,
        default="none",
        choices=("none", "circle", "line"),
        help="动态目标轨迹：none=静态；circle/line=每步更新 target_pos",
    )
    p.add_argument(
        "--target-motion-center",
        type=str,
        default="",
        help="动态目标中心 x,y,z；留空则以 target bank 点为中心",
    )
    p.add_argument(
        "--target-motion-amp",
        type=str,
        default="0.03,0.03,0.00",
        help="动态目标振幅 x,y,z (m)",
    )
    p.add_argument("--target-motion-period", type=float, default=4.0, help="动态目标周期 (s)")
    p.add_argument(
        "--obstacle-motion",
        type=str,
        default="none",
        choices=("none", "circle", "line", "random", "random_depart", "random_depart_probe"),
        help="动态障碍轨迹：line/circle、随机、随机后让路，或接近目标后回探",
    )
    p.add_argument("--obstacle-body", type=str, default="obstacle_rod_mount", help="动态障碍 body 名")
    p.add_argument(
        "--obstacle-motion-center",
        type=str,
        default="",
        help="动态障碍中心 x,y,z；留空则以当前 body_pos 为中心",
    )
    p.add_argument(
        "--obstacle-motion-amp",
        type=str,
        default="0.03,0.00,0.00",
        help="动态障碍振幅 x,y,z (m)",
    )
    p.add_argument("--obstacle-motion-period", type=float, default=5.0, help="动态障碍周期 (s)")
    p.add_argument("--obstacle-motion-seed", type=int, default=42, help="random 轨迹随机种子；同一 seed 可复现同一轨迹")
    p.add_argument("--obstacle-geom", type=str, default="obstacle_rod", help="用于统计避障接触步数的障碍物 geom 名")
    p.add_argument("--obstacle-contact-body", type=str, default=BASE_BODY, help="统计障碍物是否碰到该 body 及其子 body")
    p.add_argument("--obstacle-can-fall", action="store_true", help="可视化用：动态杆被碰到后不再强制扶正，按 MuJoCo 物理倒下")
    p.add_argument("--obstacle-motion-active-time", type=float, default=2.0, help="random_depart：前多少秒无规则运动")
    p.add_argument("--obstacle-motion-clear-offset", type=str, default="0.18,0.12,0.00", help="random_depart：随后移动到相对初始位置的偏移 x,y,z")
    p.add_argument("--obstacle-motion-clear-time", type=float, default=2.0, help="random_depart：移到让路位置需要多久 (s)")
    p.add_argument("--obstacle-motion-probe-trigger-distance", type=float, default=0.06, help="random_depart_probe：TCP 离目标多近时触发回探 (m)")
    p.add_argument("--obstacle-motion-probe-offset", type=str, default="-0.07,0.05,-0.15", help="random_depart_probe：回探杆 mount 相对触发 TCP 的偏移 x,y,z")
    p.add_argument("--obstacle-motion-probe-time", type=float, default=1.5, help="random_depart_probe：回探靠近所用时间 (s)")
    p.add_argument("--enable-cbf", action="store_true", help="EMBODISTEER 式全身 CBF-QP 避障")
    p.add_argument("--cbf-d-safe", type=float, default=CBF_D_SAFE, help="到障碍面安全余量 (m)")
    p.add_argument("--cbf-gamma", type=float, default=CBF_GAMMA, help="CBF 增益 γ")
    p.add_argument(
        "--cbf-lambda",
        type=float,
        default=CBF_LAMBDA,
        help="仿真 CBF lambda 兼容参数；task-preserving 权重请用 --cbf-task-preserve-weight",
    )
    p.add_argument(
        "--cbf-activate-margin",
        type=float,
        default=CBF_ACTIVATE_MARGIN,
        help="h_min 低于该值 (m) 时激活 CBF",
    )
    p.add_argument(
        "--cbf-capsule-samples",
        type=int,
        default=17,
        help="仿真增强配置：每段 capsule 采样数（共享/真机默认仍为 9）",
    )
    p.add_argument(
        "--cbf-qp-metric",
        choices=("identity", "task_preserving"),
        default="task_preserving",
        help="仿真 QP 修正 metric；默认显式启用 task_preserving",
    )
    p.add_argument(
        "--cbf-task-preserve-weight",
        type=float,
        default=5.0,
        help="task_preserving metric 的 TCP Jacobian 权重；不复用 lambda_cbf",
    )
    p.add_argument("--cbf-target-guidance", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--cbf-target-guidance-clearance", type=float, default=0.07)
    p.add_argument("--cbf-target-guidance-reach", type=float, default=0.04)
    p.add_argument("--cbf-target-guidance-forward", type=float, default=0.0)
    p.add_argument("--cbf-target-guidance-dynamic-clearance", type=float, default=0.14)
    p.add_argument("--cbf-target-guidance-dynamic-forward", type=float, default=0.04)
    p.add_argument("--cbf-target-guidance-dynamic-speed-thresh", type=float, default=1e-4)
    p.add_argument("--cbf-target-guidance-dynamic-closing-speed-thresh", type=float, default=1e-4)
    p.add_argument("--cbf-target-guidance-release-steps", type=int, default=32)
    p.add_argument("--cbf-target-guidance-switch-slack", type=float, default=0.05)
    p.add_argument("--cbf-target-guidance-dynamic-lookahead-steps", type=float, default=2.0)
    p.add_argument(
        "--cbf-dynamic-lookahead-steps",
        type=float,
        default=2.0,
        help=(
            "按障碍物速度预测的 lookahead 步数；障碍物速度为 0 时不增加 dynamic padding。"
            "本动态仿真入口默认 2.0，属于入口默认而非 shared CBF 全局默认。"
        ),
    )
    p.add_argument(
        "--cbf-log",
        type=str,
        default="",
        help="CBF 逐步 JSONL 日志路径（例：log/runtime/mujoco_cbf.jsonl）",
    )
    p.add_argument(
        "--traj-log",
        type=str,
        default="",
        help="逐步轨迹 JSONL 日志路径，记录 q/tcp/dq_nom/dq_cbf/SDF debug",
    )
    p.add_argument(
        "--obstacle-source",
        type=str,
        default="geom",
        choices=(
            "geom",
            "geom_sdf",
            "ideal_sdf",
            "pointcloud",
            "ideal_pointcloud",
            "vision",
            "sdf",
            "scene_depth_sdf",
            "depth_sdf",
            "vision_sdf",
            "workspace_sdf",
            "unknown_sdf",
        ),
        help=(
            "障碍来源：geom=MuJoCo 解析GT；geom_sdf=明确障碍物理想点云SDF；"
            "vision=scene_depth 圆柱拟合；workspace_sdf=scene_depth 工作空间未知物体点云SDF"
        ),
    )
    p.add_argument(
        "--calib-json",
        type=str,
        default="log/runtime/calib/camera_calib.json",
        help="vision 模式：相机标定 JSON（内参 K + mounts.T_parent_cam）",
    )
    p.add_argument(
        "--use-sim-cam",
        action="store_true",
        help="vision 模式：用 MuJoCo fovy/xpos 代替标定 JSON（仅调试对比）",
    )
    p.add_argument(
        "--workspace-sdf-preset",
        type=str,
        default="static",
        choices=("static", "dynamic"),
        help="workspace_sdf voxel persistence 参数：dynamic 会缩短记忆以减少移动障碍残影",
    )
    p.add_argument(
        "--vision-debug",
        action="store_true",
        help="配合 --verbose --obstacle-source vision，打印视觉检测点数/误差",
    )
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    if args.use_train_npz:
        args.npz = str(DEFAULT_NPZ_TRAIN)
    raise SystemExit(run(args))
