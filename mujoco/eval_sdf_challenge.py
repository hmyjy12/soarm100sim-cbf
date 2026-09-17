#!/usr/bin/env python3
"""Challenge-set eval for obstacle avoidance.

First selects target indices where the no-CBF baseline contacts the obstacle,
then compares none / analytic geom CBF / ideal point-cloud SDF CBF on that same set.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
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
_obs = _load_local("so100_mj_obstacle_source", _THIS / "obstacle_source.py")
_dyn = _load_local("so100_mj_dynamic", _THIS / "dynamic.py")

DEFAULT_CHECKPOINT = _c.DEFAULT_CHECKPOINT
DEFAULT_MJCF = _c.DEFAULT_MJCF
DEFAULT_NPZ_TEST = _c.DEFAULT_NPZ_TEST
SIM_DT = _c.SIM_DT
DECIMATION = _c.DECIMATION
ACTION_SCALE = _c.ACTION_SCALE
ACTION_FILTER_TAU = _c.ACTION_FILTER_TAU
EPISODE_LENGTH_S = _c.EPISODE_LENGTH_S
CBF_D_SAFE = _c.CBF_D_SAFE
CBF_GAMMA = _c.CBF_GAMMA
CBF_LAMBDA = _c.CBF_LAMBDA
CBF_ACTIVATE_MARGIN = _c.CBF_ACTIVATE_MARGIN
CBF_FILTER_TAU = _c.CBF_FILTER_TAU


@dataclass
class RunResult:
    idx: int
    method: str
    contact_steps: int
    best_dist_m: float
    end_dist_m: float
    mean_dist_m: float
    max_dist_m: float
    success_latched: bool
    success_step: int
    final_state: str
    h_min_m: float
    active_steps: int
    corrected_steps: int
    max_dq_cbf: float
    max_obs_speed: float
    total_steps: int


def _obstacle_gid(model: mujoco.MjModel, geom_name: str) -> int:
    gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, geom_name)
    return int(gid) if gid >= 0 else -1


def _count_contacts(data: mujoco.MjData, obstacle_gid: int) -> int:
    if obstacle_gid < 0:
        return 0
    n = 0
    for i in range(int(data.ncon)):
        c = data.contact[i]
        if int(c.geom1) == obstacle_gid or int(c.geom2) == obstacle_gid:
            n += 1
    return n


def _make_stepper(model: mujoco.MjModel, ids, policy, method: str, args) -> _rt.ReachStepper:
    enable_cbf = method != "none"
    cfg = None
    obs_source = None
    if enable_cbf:
        cfg = _cbf.CbfConfig(
            d_safe=float(args.cbf_d_safe),
            gamma=float(args.cbf_gamma),
            lambda_cbf=float(args.cbf_lambda),
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
    stepper = _rt.ReachStepper(
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
        enable_cbf=enable_cbf,
        cbf_cfg=cfg,
    )
    if enable_cbf:
        obs_source = _obs.make_obstacle_source(
            method,
            model,
            geom_names=cfg.obstacle_geom_names,
            calib_json=str(args.calib_json),
            use_sim_cam=bool(args.use_sim_cam),
        )
        preset = str(getattr(args, "workspace_sdf_preset", "static"))
        source_cfg = getattr(obs_source, "cfg", None)
        if source_cfg is not None and preset == "dynamic":
            source_cfg.persistence_hits = 1
            source_cfg.persistence_forget_frames = 2
            source_cfg.persistence_voxel_size_m = 0.012
    stepper.cbf_obstacle_source = obs_source
    return stepper


def _motion_spec(args, prefix: str):
    kind = str(getattr(args, f"{prefix}_motion", "none"))
    center = _dyn.parse_vec3(str(getattr(args, f"{prefix}_motion_center", "")), default=(0.0, 0.0, 0.0))
    amp = _dyn.parse_vec3(str(getattr(args, f"{prefix}_motion_amp", "0,0,0")), default=(0.0, 0.0, 0.0))
    period = float(getattr(args, f"{prefix}_motion_period", 4.0))
    seed = int(getattr(args, f"{prefix}_motion_seed", getattr(args, "seed", 42)))
    active_s = float(getattr(args, f"{prefix}_motion_active_time", 2.0))
    clear_offset = _dyn.parse_vec3(
        str(getattr(args, f"{prefix}_motion_clear_offset", "0.18,0.12,0.00")),
        default=(0.18, 0.12, 0.0),
    )
    clear_time_s = float(getattr(args, f"{prefix}_motion_clear_time", 2.0))
    return _dyn.MotionSpec(
        kind=kind,
        center=center,
        amplitude=amp,
        period_s=period,
        seed=seed,
        random_active_s=active_s,
        clear_offset=clear_offset,
        clear_time_s=clear_time_s,
    )


def _method_uses_settle(method: str, args) -> bool:
    methods = {str(m).strip() for m in getattr(args, "settle_methods", []) if str(m).strip()}
    return method in methods


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


def run_episode(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    ids,
    stepper,
    method: str,
    idx: int,
    target_pos: np.ndarray,
    target_quat: np.ndarray,
    steps_per_ep: int,
    obstacle_gid: int,
    args,
) -> RunResult:
    _rt.reset_home(model, data, ids)
    stepper.reset_filter()

    contact_steps = 0
    best_dist = float("inf")
    dist_sum = 0.0
    max_dist = 0.0
    h_min = float("inf")
    active_steps = 0
    corrected_steps = 0
    max_dq_cbf = 0.0
    max_obs_speed = 0.0
    ctrl_dt = float(SIM_DT) * int(DECIMATION)
    task_state = "APPROACH"
    success_counter = 0
    success_latched = False
    success_step = -1
    settle_steps = 0
    max_settle_steps = int(round(max(float(args.settle_on_success), 0.0) / ctrl_dt))
    hold_target_q: np.ndarray | None = None
    use_settle = _method_uses_settle(method, args)
    target_base_pos = np.asarray(target_pos, dtype=np.float64).copy()
    target_motion = _motion_spec(args, "target")
    obstacle_motion = _motion_spec(args, "obstacle")
    dynamic_target = str(getattr(args, "target_motion", "none")).lower().strip() != "none"
    dynamic_obstacle = str(getattr(args, "obstacle_motion", "none")).lower().strip() != "none"
    obstacle_body = str(getattr(args, "obstacle_body", "obstacle_rod_mount"))
    obstacle_base_pos = None
    obstacle_runner = _dyn.MotionRunner(
        spec=obstacle_motion,
        probe_trigger_distance=float(args.obstacle_motion_probe_trigger_distance),
        probe_offset=_dyn.parse_vec3(
            str(args.obstacle_motion_probe_offset), default=(-0.07, 0.05, -0.15)
        ),
        probe_time_s=float(args.obstacle_motion_probe_time),
    )
    if dynamic_obstacle:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, obstacle_body)
        if bid >= 0:
            home_positions = getattr(args, "_dynamic_obstacle_home_pos", {})
            if isinstance(home_positions, dict) and obstacle_body in home_positions:
                obstacle_base_pos = np.asarray(home_positions[obstacle_body], dtype=np.float64).copy()
            else:
                obstacle_base_pos = np.asarray(model.body_pos[int(bid)], dtype=np.float64).copy()
            _dyn.set_body_pos(model, data, obstacle_body, obstacle_base_pos, lock_upright=True)

    # 动态杆先回到受脚本控制的直立起点，再建立 obstacle source 的第一帧记录。
    # 否则上一局残留的倾倒姿态会被误算成一次很大的障碍物速度。
    if method != "none":
        stepper.refresh_cbf_obstacles(data)

    for k in range(steps_per_ep):
        t_s = k * ctrl_dt
        if dynamic_target:
            target_pos = target_motion.position(t_s, base=target_base_pos)
        if dynamic_obstacle and obstacle_base_pos is not None:
            tcp_now, _ = _rt.tcp_pose_w(data, ids)
            obs_pos = obstacle_runner.position(
                t_s,
                obstacle_base_pos,
                tcp_w=tcp_now,
                target_w=target_pos,
            )
            _dyn.set_body_pos(model, data, obstacle_body, obs_pos, lock_upright=True)
        if use_settle and task_state == "SETTLE" and str(args.settle_mode) == "hold_q" and hold_target_q is not None:
            tgt = hold_target_q.copy()
            tcp_now, ee_quat_now = _rt.tcp_pose_w(data, ids)
            ee_quat_now = ee_quat_now / max(float(np.linalg.norm(ee_quat_now)), 1e-12)
            info = {
                "distance": float(np.linalg.norm(tcp_now - target_pos)),
                "quat_dot": float(abs(np.dot(ee_quat_now, target_quat))),
                "h_min": float("inf"),
                "cbf_active": False,
                "dq_cbf_norm": 0.0,
            }
        elif use_settle and task_state == "SETTLE" and str(args.settle_mode) == "policy_soft_cbf":
            tgt, info = _compute_with_soft_cbf(stepper, model, data, target_pos, target_quat, args)
        else:
            tgt, info = stepper.compute_targets(model, data, target_pos, target_quat)
        _rt.set_ctrl(data, ids, tgt)
        for _sub in range(int(DECIMATION)):
            if dynamic_obstacle and obstacle_base_pos is not None:
                _dyn.set_body_pos(model, data, obstacle_body, obs_pos, lock_upright=True)
            mujoco.mj_step(model, data)
        if _count_contacts(data, obstacle_gid) > 0:
            contact_steps += 1
        dist_now = float(info["distance"])
        best_dist = min(best_dist, dist_now)
        dist_sum += dist_now
        max_dist = max(max_dist, dist_now)
        h = float(info.get("h_min", float("inf")))
        h_min = min(h_min, h)
        if info.get("cbf_active"):
            active_steps += 1
        dq_cbf = float(info.get("dq_cbf_norm", 0.0))
        if dq_cbf > 1e-6:
            corrected_steps += 1
            max_dq_cbf = max(max_dq_cbf, dq_cbf)
        max_obs_speed = max(max_obs_speed, float(info.get("cbf_worst_obs_speed", 0.0)))
        if use_settle:
            if task_state == "APPROACH":
                if float(info["distance"]) <= float(args.success_dist):
                    success_counter += 1
                else:
                    success_counter = 0
                if success_counter >= int(args.success_steps):
                    success_latched = True
                    success_step = int(k)
                    if max_settle_steps > 0:
                        task_state = "SETTLE"
                        settle_steps = 0
                        if str(args.settle_mode) == "hold_q":
                            hold_target_q = _rt.joint_pos(data, ids).copy()
                    else:
                        task_state = "SUCCESS"
                        break
            elif task_state == "SETTLE":
                settle_steps += 1
                if settle_steps >= max_settle_steps:
                    task_state = "SUCCESS"
                    if bool(args.stop_on_success):
                        break

    tcp, _ = _rt.tcp_pose_w(data, ids)
    end_dist = float(np.linalg.norm(tcp - target_pos))
    if not math.isfinite(h_min):
        h_min = float("nan")
    return RunResult(
        idx=int(idx),
        method=method,
        contact_steps=int(contact_steps),
        best_dist_m=float(best_dist),
        end_dist_m=end_dist,
        mean_dist_m=float(dist_sum / max(int(steps_per_ep), 1)),
        max_dist_m=float(max_dist),
        success_latched=bool(success_latched),
        success_step=int(success_step),
        final_state=str(task_state),
        h_min_m=float(h_min),
        active_steps=int(active_steps),
        corrected_steps=int(corrected_steps),
        max_dq_cbf=float(max_dq_cbf),
        max_obs_speed=float(max_obs_speed),
        total_steps=int(steps_per_ep),
    )


def _write_csv(path: Path, rows: list[RunResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(RunResult.__dataclass_fields__.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: getattr(r, k) for k in fields})


def _summarize(rows: list[RunResult]) -> dict:
    out = {}
    for method in sorted({r.method for r in rows}):
        rs = [r for r in rows if r.method == method]
        h_vals = np.asarray([r.h_min_m for r in rs], dtype=np.float64)
        finite_h = h_vals[np.isfinite(h_vals)]
        out[method] = {
            "n": len(rs),
            "contact_rate": float(np.mean([r.contact_steps > 0 for r in rs])) if rs else float("nan"),
            "reach_2cm_rate": float(np.mean([r.best_dist_m <= 0.02 for r in rs])) if rs else float("nan"),
            "safe_reach_2cm_rate": float(
                np.mean([(r.contact_steps == 0) and (r.best_dist_m <= 0.02) for r in rs])
            ) if rs else float("nan"),
            "success_latch_rate": float(np.mean([r.success_latched for r in rs])) if rs else float("nan"),
            "mean_best_dist_m": float(np.mean([r.best_dist_m for r in rs])) if rs else float("nan"),
            "mean_end_dist_m": float(np.mean([r.end_dist_m for r in rs])) if rs else float("nan"),
            "mean_tracking_dist_m": float(np.mean([r.mean_dist_m for r in rs])) if rs else float("nan"),
            "mean_max_tracking_dist_m": float(np.mean([r.max_dist_m for r in rs])) if rs else float("nan"),
            "mean_h_min_m": float(np.mean(finite_h)) if finite_h.size else float("nan"),
            "mean_max_dq_cbf": float(np.mean([r.max_dq_cbf for r in rs])) if rs else float("nan"),
            "mean_max_obs_speed": float(np.mean([r.max_obs_speed for r in rs])) if rs else float("nan"),
        }
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument("--npz", type=str, default=str(DEFAULT_NPZ_TEST))
    p.add_argument("--out-dir", type=str, default="log/runtime/eval/sdf_challenge")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--scan-count", type=int, default=512)
    p.add_argument("--max-challenges", type=int, default=64)
    p.add_argument("--indices-file", type=str, default="")
    p.add_argument("--obstacle-geom", type=str, default="obstacle_rod")
    p.add_argument(
        "--methods",
        nargs="+",
        default=["none", "geom", "ideal_sdf"],
        help="Methods to evaluate, e.g. none geom ideal_sdf workspace_sdf",
    )
    p.add_argument("--calib-json", type=str, default=str(_THIS.parent / "logs" / "calib" / "camera_calib.json"))
    p.add_argument("--use-sim-cam", action="store_true")
    p.add_argument("--action-scale", type=float, default=ACTION_SCALE)
    p.add_argument("--filter-tau", type=float, default=ACTION_FILTER_TAU)
    p.add_argument("--cbf-filter-tau", type=float, default=CBF_FILTER_TAU)
    p.add_argument("--cbf-correction-filter", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--cbf-bypass-filter-when-unsafe", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--cbf-d-safe", type=float, default=CBF_D_SAFE)
    p.add_argument("--cbf-gamma", type=float, default=CBF_GAMMA)
    p.add_argument(
        "--cbf-lambda",
        type=float,
        default=CBF_LAMBDA,
        help="仿真 CBF lambda 兼容参数；task-preserving 权重单独设置",
    )
    p.add_argument("--cbf-activate-margin", type=float, default=CBF_ACTIVATE_MARGIN)
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
            "本动态评测入口默认 2.0，属于入口默认而非 shared CBF 全局默认。"
        ),
    )
    p.add_argument("--settle-methods", nargs="+", default=[], help="Methods that use success/settle state machine")
    p.add_argument("--success-dist", type=float, default=0.03)
    p.add_argument("--success-steps", type=int, default=10)
    p.add_argument("--settle-on-success", type=float, default=0.0)
    p.add_argument("--settle-mode", type=str, default="hold_q", choices=("hold_q", "policy_soft_cbf"))
    p.add_argument("--settle-cbf-d-safe", type=float, default=0.005)
    p.add_argument("--settle-cbf-gamma", type=float, default=0.3)
    p.add_argument("--settle-cbf-activate-margin", type=float, default=0.015)
    p.add_argument("--settle-cbf-lambda", type=float, default=0.5)
    p.add_argument("--stop-on-success", action="store_true")
    p.add_argument("--target-motion", type=str, default="none", choices=("none", "circle", "line"))
    p.add_argument("--target-motion-center", type=str, default="")
    p.add_argument("--target-motion-amp", type=str, default="0.03,0.03,0.00")
    p.add_argument("--target-motion-period", type=float, default=4.0)
    p.add_argument("--obstacle-motion", type=str, default="none", choices=("none", "circle", "line", "random", "random_depart", "random_depart_probe"))
    p.add_argument("--obstacle-body", type=str, default="obstacle_rod_mount")
    p.add_argument("--obstacle-motion-center", type=str, default="")
    p.add_argument("--obstacle-motion-amp", type=str, default="0.03,0.00,0.00")
    p.add_argument("--obstacle-motion-period", type=float, default=5.0)
    p.add_argument("--obstacle-motion-seed", type=int, default=42)
    p.add_argument("--obstacle-motion-active-time", type=float, default=2.0)
    p.add_argument("--obstacle-motion-clear-offset", type=str, default="0.18,0.12,0.00")
    p.add_argument("--obstacle-motion-clear-time", type=float, default=2.0)
    p.add_argument("--obstacle-motion-probe-trigger-distance", type=float, default=0.06)
    p.add_argument("--obstacle-motion-probe-offset", type=str, default="-0.07,0.05,-0.15")
    p.add_argument("--obstacle-motion-probe-time", type=float, default=1.5)
    p.add_argument("--workspace-sdf-preset", type=str, default="static", choices=("static", "dynamic"))
    p.add_argument("--log-every", type=int, default=16)
    args = p.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    model = mujoco.MjModel.from_xml_path(str(Path(args.mjcf).expanduser().resolve()))
    model.opt.timestep = float(SIM_DT)
    data = mujoco.MjData(model)
    ids = _rt.resolve_robot_ids(model)
    policy = _pol.SkrlGaussianPolicy(Path(args.checkpoint).expanduser().resolve())
    bank_pos, bank_quat = _rt.load_target_bank(Path(args.npz).expanduser().resolve())
    steps_per_ep = int(round(EPISODE_LENGTH_S / (SIM_DT * DECIMATION)))
    obstacle_gid = _obstacle_gid(model, str(args.obstacle_geom))
    if obstacle_gid < 0:
        raise ValueError(f"obstacle geom not found: {args.obstacle_geom}")
    obstacle_body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(args.obstacle_body))
    if obstacle_body_id >= 0:
        args._dynamic_obstacle_home_pos = {
            str(args.obstacle_body): np.asarray(model.body_pos[int(obstacle_body_id)], dtype=np.float64).copy()
        }

    rng = np.random.default_rng(int(args.seed))
    if args.indices_file:
        challenge_indices = [int(x) for x in json.loads(Path(args.indices_file).read_text(encoding="utf-8"))]
        if int(args.max_challenges) > 0:
            challenge_indices = challenge_indices[: int(args.max_challenges)]
    else:
        candidates = rng.choice(bank_pos.shape[0], size=min(int(args.scan_count), bank_pos.shape[0]), replace=False)
        baseline_stepper = _make_stepper(model, ids, policy, "none", args)
        challenge_indices = []
        print(f"[scan] scanning {len(candidates)} targets for no-CBF contacts", flush=True)
        for n, idx in enumerate(candidates, 1):
            res = run_episode(
                model,
                data,
                ids,
                baseline_stepper,
                "none",
                int(idx),
                bank_pos[int(idx)].copy(),
                bank_quat[int(idx)].copy(),
                steps_per_ep,
                obstacle_gid,
                args,
            )
            if res.contact_steps > 0:
                challenge_indices.append(int(idx))
                print(
                    f"[scan] challenge idx={int(idx)} contact_steps={res.contact_steps} "
                    f"best={res.best_dist_m*1000:.1f}mm",
                    flush=True,
                )
                if len(challenge_indices) >= int(args.max_challenges):
                    break
            elif n % max(1, int(args.log_every)) == 0:
                print(f"[scan] {n}/{len(candidates)} found={len(challenge_indices)}", flush=True)
        (out_dir / "challenge_indices.json").write_text(
            json.dumps(challenge_indices, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"[eval] challenge_count={len(challenge_indices)}", flush=True)
    rows: list[RunResult] = []
    for method in [str(m).strip() for m in args.methods if str(m).strip()]:
        stepper = _make_stepper(model, ids, policy, method, args)
        for i, idx in enumerate(challenge_indices, 1):
            quat = bank_quat[int(idx)].copy()
            quat /= max(float(np.linalg.norm(quat)), 1e-12)
            res = run_episode(
                model,
                data,
                ids,
                stepper,
                method,
                int(idx),
                bank_pos[int(idx)].copy(),
                quat,
                steps_per_ep,
                obstacle_gid,
                args,
            )
            rows.append(res)
            if i % max(1, int(args.log_every)) == 0 or i == len(challenge_indices):
                print(
                    f"[eval][{method}] {i}/{len(challenge_indices)} "
                    f"idx={idx} contact={res.contact_steps} best={res.best_dist_m*1000:.1f}mm "
                    f"end={res.end_dist_m*1000:.1f}mm "
                    f"success={'Y' if res.success_latched else 'n'} "
                    f"h={res.h_min_m*1000 if math.isfinite(res.h_min_m) else float('nan'):.1f}mm",
                    flush=True,
                )

    _write_csv(out_dir / "episodes.csv", rows)
    summary = {
        "mjcf": str(Path(args.mjcf).expanduser().resolve()),
        "seed": int(args.seed),
        "scan_count": int(args.scan_count),
        "challenge_indices": challenge_indices,
        "settle_methods": [str(m) for m in args.settle_methods],
        "success_dist": float(args.success_dist),
        "success_steps": int(args.success_steps),
        "settle_on_success": float(args.settle_on_success),
        "settle_mode": str(args.settle_mode),
        "target_motion": {
            "kind": str(args.target_motion),
            "center": str(args.target_motion_center),
            "amp": str(args.target_motion_amp),
            "period_s": float(args.target_motion_period),
        },
        "obstacle_motion": {
            "kind": str(args.obstacle_motion),
            "body": str(args.obstacle_body),
            "center": str(args.obstacle_motion_center),
            "amp": str(args.obstacle_motion_amp),
            "period_s": float(args.obstacle_motion_period),
            "seed": int(args.obstacle_motion_seed),
            "active_time_s": float(args.obstacle_motion_active_time),
            "clear_offset": str(args.obstacle_motion_clear_offset),
            "clear_time_s": float(args.obstacle_motion_clear_time),
        },
        "workspace_sdf_preset": str(args.workspace_sdf_preset),
        "metrics": _summarize(rows),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary["metrics"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
