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
    args.cbf_log = ""
    raise SystemExit(_play.run(args))
