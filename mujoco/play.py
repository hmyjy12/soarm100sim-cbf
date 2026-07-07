#!/usr/bin/env python3
"""SO-100 Plus Reach：MuJoCo 推理（默认 C：bank-start best_agent）。

注意：本目录名为 mujoco，与官方库同名，因此本脚本用 importlib 加载本地模块。

  cd soarm100sim && python mujoco/play.py
  python mujoco/play.py --headless --episodes 20
  python mujoco/play.py --episodes 5 --speed 0.5   # 半速看过程
  python mujoco/play.py --enable-cbf --verbose     # 开启全身 CBF-QP 避障
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

    bank_pos, bank_quat = load_target_bank(npz)
    rng = np.random.default_rng(int(args.seed))
    steps_per_ep = int(round(EPISODE_LENGTH_S / (SIM_DT * DECIMATION)))
    cbf_log_path = Path(args.cbf_log).expanduser().resolve() if args.cbf_log else None
    if cbf_log_path is not None:
        cbf_log_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"[mujoco_play] CBF log → {cbf_log_path}")
    print(
        f"[INFO] bank={bank_pos.shape[0]}  steps/ep={steps_per_ep}  "
        f"scale={args.action_scale} tau={args.filter_tau}"
    )

    viewer = None
    if not args.headless:
        try:
            import mujoco.viewer as mjv

            viewer = mjv.launch_passive(model, data)
        except Exception as exc:
            print(f"[WARN] viewer unavailable ({exc}), fallback headless")
            viewer = None
            use_realtime = False
            sleep_s = 0.0

    ep = 0
    try:
        while ep < int(args.episodes):
            if viewer is not None and not viewer.is_running():
                break

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

            for k in range(steps_per_ep):
                if viewer is not None and not viewer.is_running():
                    break

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

                dist = float(info["distance"])
                ori = _ori_deg(float(info["quat_dot"]))
                best_dist = min(best_dist, dist)
                best_ori = min(best_ori, ori)

                if viewer is not None:
                    _draw_target(viewer, target_pos)
                    viewer.sync()
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
    p.add_argument("--action-scale", type=float, default=ACTION_SCALE)
    p.add_argument("--filter-tau", type=float, default=ACTION_FILTER_TAU)
    p.add_argument("--headless", action="store_true")
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
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    if args.use_train_npz:
        args.npz = str(DEFAULT_NPZ_TRAIN)
    raise SystemExit(run(args))
