#!/usr/bin/env python3
"""视觉障碍检测冒烟：home 位对比 GT geom vs scene_depth 拟合（使用标定 JSON）。

  cd soarm100sim
  python mujoco/vision_obstacle_smoke.py
  python mujoco/vision_obstacle_smoke.py --calib-json logs/calib/camera_calib.json
  python mujoco/vision_obstacle_smoke.py --use-sim-cam   # 对比：MuJoCo 真值内外参
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
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


_c = _load_local("c", _THIS / "constants.py")
_cbf = _load_local("cbf", _THIS / "cbf.py")
_rt = _load_local("rt", _THIS / "runtime.py")
_obs = _load_local("obs", _THIS / "obstacle_source.py")
_cal = _load_local("cal", _THIS / "calib.py")


def main() -> int:
    p = argparse.ArgumentParser(description="视觉障碍检测冒烟（标定 JSON）")
    p.add_argument("--calib-json", type=str, default=str(_cal.DEFAULT_CALIB_JSON))
    p.add_argument("--use-sim-cam", action="store_true")
    args = p.parse_args()

    model = mujoco.MjModel.from_xml_path(str(_c.DEFAULT_MJCF))
    data = mujoco.MjData(model)
    ids = _rt.resolve_robot_ids(model)
    _rt.reset_home(model, data, ids)

    gt_list = _cbf.load_obstacles(model, data, ("obstacle_rod",))
    if not gt_list:
        print("[vision_smoke] 无 obstacle_rod geom")
        return 1
    gt = gt_list[0]

    src = _obs.make_obstacle_source(
        "vision",
        model,
        calib_json=args.calib_json,
        use_sim_cam=bool(args.use_sim_cam),
    )
    try:
        src.update(model, data)
        est = src.get_obstacles()
    finally:
        src.close()

    mode = "sim_cam" if args.use_sim_cam else f"json:{Path(args.calib_json).resolve()}"
    dbg = src.last_debug
    print(f"[vision_smoke] calib={mode}")
    print(f"[vision_smoke] depth_valid={dbg.n_depth_valid}  roi_pts={dbg.n_roi}  detected={dbg.detected}")
    if not est:
        print("[vision_smoke] FAIL: 未检测到杆")
        return 1

    rod = est[0]
    center_err = float(np.linalg.norm(rod.center - gt.center) * 1000.0)
    dot = float(np.clip(abs(np.dot(rod.axis, gt.axis)), 0.0, 1.0))
    axis_deg = float(np.degrees(np.arccos(dot)))
    print(f"[vision_smoke] GT center   = {np.round(gt.center, 4)}")
    print(f"[vision_smoke] EST center  = {np.round(rod.center, 4)}  err={center_err:.1f} mm")
    print(f"[vision_smoke] GT axis     = {np.round(gt.axis, 4)}")
    print(f"[vision_smoke] EST axis    = {np.round(rod.axis, 4)}  angle={axis_deg:.2f} deg")

    # 标定 JSON vs MuJoCo 外参一致性（仅仿真）
    if not args.use_sim_cam:
        cal = _cal.load_json(args.calib_json)
        T_json = _cal.T_world_cam_calibrated(model, data, cal, _c.SCENE_DEPTH_CAM)
        T_mj = _cal.T_world_cam(model, data, _c.SCENE_DEPTH_CAM)
        e = float(np.linalg.norm(T_json - T_mj))
        print(f"[vision_smoke] |T_world_cam(json) - T_world_cam(mj)| = {e:.2e}")

    ok = center_err < 25.0 and axis_deg < 10.0
    print(f"[vision_smoke] {'PASS' if ok else 'WARN'} (threshold center<25mm axis<10deg)")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
