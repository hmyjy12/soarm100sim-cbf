#!/usr/bin/env python3
"""仅看双相机画面（无 MuJoCo 3D 窗口）。

  python mujoco/vision_preview.py
  python mujoco/vision_preview.py --enable-cbf --cam-depth
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
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


# 复用 play 主循环，强制 headless + show_cam
_play = _load_local("so100_mj_play", _THIS / "play.py")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MuJoCo dual-camera live preview only")
    p.add_argument("--checkpoint", type=str, default=str(_play.DEFAULT_CHECKPOINT))
    p.add_argument("--mjcf", type=str, default=str(_play.DEFAULT_MJCF))
    p.add_argument("--npz", type=str, default=str(_play.DEFAULT_NPZ_TEST))
    p.add_argument("--episodes", type=int, default=3)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--speed", type=float, default=0.3)
    p.add_argument("--enable-cbf", action="store_true")
    p.add_argument("--cam-depth", action="store_true")
    p.add_argument(
        "--cbf-dynamic-lookahead-steps",
        type=float,
        default=2.0,
        help=(
            "按障碍物速度预测的 lookahead 步数；障碍物速度为 0 时不增加 dynamic padding。"
            "本动态预览入口默认 2.0，属于入口默认而非 shared CBF 全局默认。"
        ),
    )
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.headless = True
    args.show_cam = True
    args.realtime = True
    args.verbose = False
    args.use_train_npz = False
    args.action_scale = _play.ACTION_SCALE
    args.filter_tau = _play.ACTION_FILTER_TAU
    args.cbf_d_safe = _play.CBF_D_SAFE
    args.cbf_gamma = _play.CBF_GAMMA
    args.cbf_lambda = _play.CBF_LAMBDA
    args.cbf_activate_margin = _play.CBF_ACTIVATE_MARGIN
    # Keep the preview aligned with the explicit enhanced simulation defaults.
    args.cbf_capsule_samples = 17
    args.cbf_qp_metric = "task_preserving"
    args.cbf_task_preserve_weight = 5.0
    args.cbf_target_guidance = True
    args.cbf_target_guidance_clearance = 0.07
    args.cbf_target_guidance_reach = 0.04
    args.cbf_target_guidance_forward = 0.0
    args.cbf_target_guidance_dynamic_clearance = 0.14
    args.cbf_target_guidance_dynamic_forward = 0.04
    args.cbf_target_guidance_dynamic_speed_thresh = 1e-4
    args.cbf_target_guidance_dynamic_closing_speed_thresh = 1e-4
    args.cbf_target_guidance_release_steps = 32
    args.cbf_target_guidance_switch_slack = 0.05
    args.cbf_target_guidance_dynamic_lookahead_steps = 2.0
    args.cbf_filter_tau = _play.CBF_FILTER_TAU
    args.cbf_correction_filter = True
    args.cbf_bypass_filter_when_unsafe = True
    args.cbf_log = ""
    raise SystemExit(_play.run(args))
