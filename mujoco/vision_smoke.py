#!/usr/bin/env python3
"""双相机冒烟：渲染 RGB/深度、检查外参、可选短回放。

  cd soarm100sim
  python mujoco/vision_smoke.py
  python mujoco/vision_smoke.py --out-dir log/runtime/vision_smoke --steps 120
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import time
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
_cam = _load_local("so100_mj_camera", _THIS / "camera.py")
_rt = _load_local("so100_mj_runtime", _THIS / "runtime.py")
_pol = _load_local("so100_mj_policy", _THIS / "policy.py")

DEFAULT_MJCF = _c.DEFAULT_MJCF
DEFAULT_CHECKPOINT = _c.DEFAULT_CHECKPOINT
DEFAULT_NPZ_TEST = _c.DEFAULT_NPZ_TEST
SIM_DT = _c.SIM_DT
DECIMATION = _c.DECIMATION
ACTION_SCALE = _c.ACTION_SCALE
ACTION_FILTER_TAU = _c.ACTION_FILTER_TAU
EPISODE_LENGTH_S = _c.EPISODE_LENGTH_S
SCENE_DEPTH_CAM = _c.SCENE_DEPTH_CAM
WRIST_RGB_CAM = _c.WRIST_RGB_CAM
SCENE_DEPTH_CAM_MOUNT_POS_M = _c.SCENE_DEPTH_CAM_MOUNT_POS_M
SCENE_CAM_LOOKAT_POS_M = _c.SCENE_CAM_LOOKAT_POS_M

MujocoCameraRig = _cam.MujocoCameraRig
camera_extrinsics = _cam.camera_extrinsics
camera_view_direction = _cam.camera_view_direction
depth_to_vis = _cam.depth_to_vis
reset_home = _rt.reset_home
resolve_robot_ids = _rt.resolve_robot_ids
set_ctrl = _rt.set_ctrl
load_target_bank = _rt.load_target_bank
ReachStepper = _rt.ReachStepper
SkrlGaussianPolicy = _pol.SkrlGaussianPolicy


def _save_rgb(path: Path, rgb: np.ndarray) -> None:
    arr = np.asarray(rgb, dtype=np.uint8)
    try:
        import cv2

        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        if not cv2.imwrite(str(path), bgr):
            raise RuntimeError("cv2.imwrite failed")
        return
    except Exception:
        pass
    try:
        import imageio.v3 as iio

        iio.imwrite(path, arr)
        return
    except Exception:
        pass
    try:
        from PIL import Image

        Image.fromarray(arr).save(path)
    except Exception as exc:
        raise RuntimeError(f"cannot save image {path}") from exc


def _print_extrinsics(model: mujoco.MjModel, data: mujoco.MjData, label: str) -> None:
    for name in (SCENE_DEPTH_CAM, WRIST_RGB_CAM):
        ext = camera_extrinsics(model, data, name)
        view = camera_view_direction(data, model, name)
        print(
            f"[vision_smoke] {label} {name}: "
            f"pos=({ext.pos_world[0]:.3f},{ext.pos_world[1]:.3f},{ext.pos_world[2]:.3f}) "
            f"view=({view[0]:.2f},{view[1]:.2f},{view[2]:.2f})"
        )


def _min_dist_scene_cam_to_arm_geoms(model: mujoco.MjModel, data: mujoco.MjData) -> float:
    """固定相机外壳与机械臂碰撞 geoms 的最小距离（应 >0，避免干涉）。"""
    housing_gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, "scene_depth_cam_housing")
    if housing_gid < 0:
        return float("nan")
    cam_pos = np.asarray(data.geom_xpos[housing_gid], dtype=np.float64)
    best = float("inf")
    for gid in range(model.ngeom):
        if model.geom_contype[gid] == 0 and model.geom_conaffinity[gid] == 0:
            continue
        gname = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, gid) or ""
        if gname in ("floor", "scene_depth_cam_housing", "scene_cam_lookat_marker"):
            continue
        if gname.startswith("obstacle_rod"):
            continue
        gpos = np.asarray(data.geom_xpos[gid], dtype=np.float64)
        best = min(best, float(np.linalg.norm(cam_pos - gpos)))
    return best


def run(args: argparse.Namespace) -> int:
    mjcf = Path(args.mjcf).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    model = mujoco.MjModel.from_xml_path(str(mjcf))
    model.opt.timestep = float(SIM_DT)
    data = mujoco.MjData(model)
    ids = resolve_robot_ids(model)
    rig = MujocoCameraRig(model)

    try:
        reset_home(model, data, ids)
        _print_extrinsics(model, data, "home")
        min_dist = _min_dist_scene_cam_to_arm_geoms(model, data)
        print(
            f"[vision_smoke] scene cam housing ↔ arm geoms min center-dist ≈ {min_dist*1000:.0f} mm "
            f"(mount nom={SCENE_DEPTH_CAM_MOUNT_POS_M}, lookat nom={SCENE_CAM_LOOKAT_POS_M})"
        )

        scene_rgb = rig.capture_rgb(data, SCENE_DEPTH_CAM)
        scene_depth = rig.capture_depth_m(data, SCENE_DEPTH_CAM)
        wrist_rgb = rig.capture_rgb(data, WRIST_RGB_CAM)

        _save_rgb(out_dir / "scene_depth_rgb_home.png", scene_rgb)
        _save_rgb(out_dir / "scene_depth_vis_home.png", depth_to_vis(scene_depth))
        _save_rgb(out_dir / "wrist_rgb_home.png", wrist_rgb)
        np.save(out_dir / "scene_depth_m_home.npy", scene_depth)
        print(f"[vision_smoke] saved home frames → {out_dir}")

        if int(args.steps) <= 0:
            return 0

        ckpt = Path(args.checkpoint).expanduser().resolve()
        npz = Path(args.npz).expanduser().resolve()
        policy = SkrlGaussianPolicy(ckpt)
        stepper = ReachStepper(
            policy=policy,
            ids=ids,
            model=model,
            action_scale=float(ACTION_SCALE),
            filter_tau=float(ACTION_FILTER_TAU),
            sim_dt=float(SIM_DT),
            decimation=int(DECIMATION),
            enable_cbf=False,
        )
        bank_pos, bank_quat = load_target_bank(npz)
        idx = int(args.target_idx) if args.target_idx >= 0 else 0
        target_pos = bank_pos[idx].copy()
        target_quat = bank_quat[idx].copy()
        target_quat /= max(float(np.linalg.norm(target_quat)), 1e-12)
        reset_home(model, data, ids)
        stepper.reset_filter()

        steps = int(args.steps)
        stride = max(1, int(args.frame_stride))
        frames_dir = out_dir / "playback"
        frames_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.perf_counter()
        for k in range(steps):
            tgt, _ = stepper.compute_targets(model, data, target_pos, target_quat)
            set_ctrl(data, ids, tgt)
            for _ in range(int(DECIMATION)):
                mujoco.mj_step(model, data)
            if k % stride == 0 or k == steps - 1:
                scene_rgb = rig.capture_rgb(data, SCENE_DEPTH_CAM)
                wrist_rgb = rig.capture_rgb(data, WRIST_RGB_CAM)
                _save_rgb(frames_dir / f"scene_{k:04d}.png", scene_rgb)
                _save_rgb(frames_dir / f"wrist_{k:04d}.png", wrist_rgb)
        elapsed = time.perf_counter() - t0
        _print_extrinsics(model, data, "end")
        print(f"[vision_smoke] playback {steps} ctrl steps ({elapsed:.1f}s) → {frames_dir}")
        return 0
    finally:
        rig.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MuJoCo dual-camera vision smoke test")
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    p.add_argument("--npz", type=str, default=str(DEFAULT_NPZ_TEST))
    p.add_argument("--out-dir", type=str, default=str(_THIS.parent / "logs" / "vision_smoke"))
    p.add_argument("--steps", type=int, default=0, help=">0 时跑短回放并存帧")
    p.add_argument("--frame-stride", type=int, default=20)
    p.add_argument("--target-idx", type=int, default=0)
    return p


if __name__ == "__main__":
    raise SystemExit(run(build_parser().parse_args()))
