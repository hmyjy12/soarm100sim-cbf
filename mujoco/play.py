#!/usr/bin/env python3
"""SO-100 Plus Reach：MuJoCo 推理（默认 C：bank-start best_agent）。

注意：本目录名为 mujoco，与官方库同名，因此本脚本用 importlib 加载本地模块。

  cd soarm100sim && python mujoco/play.py
  python mujoco/play.py --headless --episodes 20
  python mujoco/play.py --episodes 5 --speed 0.5   # 半速看过程
  python mujoco/play.py --episodes 1 --hold-home 30   # 先停 30s 看 3D 里相机装位
  python mujoco/play.py --enable-cbf --verbose     # 开启全身 CBF-QP 避障
  python mujoco/play.py --enable-cbf --obstacle-source vision --vision-debug  # 视觉障碍
  python mujoco/play.py --enable-cbf --cbf-log logs/mujoco_cbf.jsonl
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

DEFAULT_CHECKPOINT = _c.DEFAULT_CHECKPOINT
DEFAULT_MJCF = _c.DEFAULT_MJCF
DEFAULT_NPZ_TEST = _c.DEFAULT_NPZ_TEST
DEFAULT_NPZ_TRAIN = _c.DEFAULT_NPZ_TRAIN
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
SCENE_DEPTH_CAM = _c.SCENE_DEPTH_CAM
WRIST_RGB_CAM = _c.WRIST_RGB_CAM
CbfConfig = _cbf.CbfConfig
cbf_step_log_record = _cbf.cbf_step_log_record


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


def _ori_deg(quat_dot: float) -> float:
    d = min(1.0, max(0.0, abs(quat_dot)))
    return float(2.0 * math.degrees(math.acos(d)))


def _draw_target(viewer, target_pos: np.ndarray) -> None:
    """在 passive viewer 上画目标球。"""
    try:
        with viewer.lock():
            scn = viewer.user_scn
            scn.ngeom = 0
            geom = scn.geoms[0]
            mujoco.mjv_initGeom(
                geom,
                mujoco.mjtGeom.mjGEOM_SPHERE,
                np.array([0.015, 0.0, 0.0], dtype=np.float64),
                np.asarray(target_pos, dtype=np.float64),
                np.eye(3, dtype=np.float64).reshape(9),
                np.array([1.0, 0.15, 0.15, 0.95], dtype=np.float32),
            )
            scn.ngeom = 1
    except Exception:
        pass


def _arr(x) -> list[float]:
    return np.asarray(x, dtype=np.float64).reshape(-1).tolist()


def _traj_log_record(
    ep: int,
    step: int,
    t_s: float,
    idx: int,
    q_before: np.ndarray,
    q_after: np.ndarray,
    q_target: np.ndarray,
    tcp_after: np.ndarray,
    target_pos: np.ndarray,
    info: dict,
    obs_source,
    prev_dq_total: np.ndarray | None,
) -> dict:
    dq_nom = np.asarray(info.get("dq_nom", np.zeros_like(q_before)), dtype=np.float64).reshape(-1)
    dq_cbf = np.asarray(info.get("dq_cbf", np.zeros_like(q_before)), dtype=np.float64).reshape(-1)
    dq_total = np.asarray(q_target - q_before, dtype=np.float64).reshape(-1)
    if prev_dq_total is None:
        ddq_total = np.zeros_like(dq_total)
    else:
        ddq_total = dq_total - np.asarray(prev_dq_total, dtype=np.float64).reshape(-1)
    dbg = getattr(obs_source, "last_debug", None) if obs_source is not None else None
    return {
        "ep": int(ep),
        "step": int(step),
        "t_s": float(t_s),
        "target_idx": int(idx),
        "target_pos": _arr(target_pos),
        "tcp_pos": _arr(tcp_after),
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
        "nom_violation": float(info.get("nom_violation", 0.0)),
        "vision_detected": bool(getattr(dbg, "detected", False)) if dbg is not None else False,
        "vision_roi_points": int(getattr(dbg, "n_roi", 0)) if dbg is not None else 0,
        "sdf_points": int(getattr(dbg, "n_sdf_points", 0)) if dbg is not None else 0,
        "self_filtered_points": int(getattr(dbg, "n_self_filtered", 0)) if dbg is not None else 0,
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

    model = mujoco.MjModel.from_xml_path(str(mjcf))
    model.opt.timestep = float(SIM_DT)
    data = mujoco.MjData(model)
    ids = resolve_robot_ids(model)
    policy = SkrlGaussianPolicy(ckpt)
    cbf_cfg = None
    if args.enable_cbf:
        cbf_cfg = CbfConfig(
            d_safe=float(args.cbf_d_safe),
            gamma=float(args.cbf_gamma),
            lambda_cbf=float(args.cbf_lambda),
            dq_max=float(args.action_scale),
            activate_margin=float(args.cbf_activate_margin),
        )
        print(
            f"[mujoco_play] CBF=ON  d_safe={cbf_cfg.d_safe}m  gamma={cbf_cfg.gamma}  "
            f"lambda={cbf_cfg.lambda_cbf}  activate<{cbf_cfg.activate_margin}m"
        )

    stepper = ReachStepper(
        policy=policy,
        ids=ids,
        model=model,
        action_scale=float(args.action_scale),
        filter_tau=float(args.filter_tau),
        sim_dt=float(SIM_DT),
        decimation=int(DECIMATION),
        enable_cbf=bool(args.enable_cbf),
        cbf_cfg=cbf_cfg,
    )

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
        stepper.cbf_obstacle_source = obs_source
        print(f"[mujoco_play] obstacle source={args.obstacle_source}")
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
            elif obs_kind in ("sdf", "scene_depth_sdf", "depth_sdf", "vision_sdf"):
                print("[mujoco_play] 视觉障碍 SDF：scene_depth 深度→ROI 表面点云 unsigned SDF")

    bank_pos, bank_quat = load_target_bank(npz)
    rng = np.random.default_rng(int(args.seed))
    steps_per_ep = int(round(EPISODE_LENGTH_S / (SIM_DT * DECIMATION)))
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
                _draw_target(viewer, bank_pos[int(rng.integers(0, bank_pos.shape[0]))])
                viewer.sync()
                time.sleep(float(args.hold_home))
        except Exception as exc:
            print(f"[WARN] viewer unavailable ({exc}), fallback headless")
            viewer = None
            if cam_preview is None:
                use_realtime = False
                sleep_s = 0.0

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
            target_quat = bank_quat[idx].copy()
            target_quat /= max(float(np.linalg.norm(target_quat)), 1e-12)

            reset_home(model, data, ids)
            stepper.reset_filter()
            if args.enable_cbf:
                stepper.refresh_cbf_obstacles(data)
            best_dist = float("inf")
            best_ori = float("inf")
            cbf_stats = CbfEpisodeStats() if args.enable_cbf else None
            t0 = time.perf_counter()
            prev_dq_total: np.ndarray | None = None

            for k in range(steps_per_ep):
                if viewer is not None and not viewer.is_running():
                    break

                q_before = joint_pos(data, ids)
                tgt, info = stepper.compute_targets(model, data, target_pos, target_quat)
                if cbf_stats is not None:
                    cbf_stats.update(info)
                    if cbf_log_path is not None:
                        rec = cbf_step_log_record(ep, k, k * ctrl_dt, info)
                        with cbf_log_path.open("a", encoding="utf-8") as f:
                            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                set_ctrl(data, ids, tgt)
                for _ in range(int(DECIMATION)):
                    mujoco.mj_step(model, data)
                q_after = joint_pos(data, ids)
                tcp_after, _ = tcp_pose_w(data, ids)
                if traj_log_path is not None:
                    rec = _traj_log_record(
                        ep,
                        k,
                        k * ctrl_dt,
                        idx,
                        q_before,
                        q_after,
                        tgt,
                        tcp_after,
                        target_pos,
                        info,
                        obs_source,
                        prev_dq_total,
                    )
                    with traj_log_path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                prev_dq_total = np.asarray(tgt - q_before, dtype=np.float64)

                dist = float(info["distance"])
                ori = _ori_deg(float(info["quat_dot"]))
                best_dist = min(best_dist, dist)
                best_ori = min(best_ori, ori)

                if viewer is not None:
                    _draw_target(viewer, target_pos)
                    viewer.sync()
                if cam_preview is not None:
                    cam_preview.update(data)
                if sleep_s > 0:
                    time.sleep(sleep_s)

                # 每秒打一行过程，方便判断是否在靠近
                if args.verbose and (k % max(1, int(round(1.0 / ctrl_dt))) == 0):
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
                        f"ori={ori:.1f}deg  tcp=({tcp[0]:.3f},{tcp[1]:.3f},{tcp[2]:.3f})"
                        f"{cbf_msg}"
                    )

            wall = time.perf_counter() - t0
            tcp, _ = tcp_pose_w(data, ids)
            print(
                f"[ep {ep:03d}] idx={idx}  best_dist={best_dist*1000:.2f}mm  "
                f"best_ori={best_ori:.1f}deg  "
                f"end_dist={float(np.linalg.norm(tcp - target_pos))*1000:.2f}mm  "
                f"wall={wall:.1f}s"
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
        help="cam-backend=save 时的输出目录（默认 logs/vision_preview）",
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
    p.add_argument("--verbose", action="store_true", help="每秒打印当前误差")
    p.add_argument("--enable-cbf", action="store_true", help="EMBODISTEER 式全身 CBF-QP 避障")
    p.add_argument("--cbf-d-safe", type=float, default=CBF_D_SAFE, help="到障碍面安全余量 (m)")
    p.add_argument("--cbf-gamma", type=float, default=CBF_GAMMA, help="CBF 增益 γ")
    p.add_argument("--cbf-lambda", type=float, default=CBF_LAMBDA, help="关节修正正则 λ")
    p.add_argument(
        "--cbf-activate-margin",
        type=float,
        default=CBF_ACTIVATE_MARGIN,
        help="h_min 低于该值 (m) 时激活 CBF",
    )
    p.add_argument(
        "--cbf-log",
        type=str,
        default="",
        help="CBF 逐步 JSONL 日志路径（例：logs/mujoco_cbf.jsonl）",
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
        ),
        help=(
            "障碍来源：geom=MuJoCo 解析GT；geom_sdf=明确障碍物理想点云SDF；"
            "vision=scene_depth 圆柱拟合；sdf=scene_depth 整图点云SDF"
        ),
    )
    p.add_argument(
        "--calib-json",
        type=str,
        default="logs/calib/camera_calib.json",
        help="vision 模式：相机标定 JSON（内参 K + mounts.T_parent_cam）",
    )
    p.add_argument(
        "--use-sim-cam",
        action="store_true",
        help="vision 模式：用 MuJoCo fovy/xpos 代替标定 JSON（仅调试对比）",
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
