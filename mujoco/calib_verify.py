#!/usr/bin/env python3
"""相机标定验证：导出 JSON、重投影误差、腕部手眼外参随姿态不变性。

  cd soarm100sim
  python mujoco/calib_verify.py
  python mujoco/calib_verify.py --out logs/calib/camera_calib.json --poses 32
  python mujoco/calib_verify.py --annotate   # 写带投影点的 PNG（需 OpenGL 渲染）
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


_c = _load_local("so100_mj_constants", _THIS / "constants.py")
_cal = _load_local("so100_mj_calib", _THIS / "calib.py")
_rt = _load_local("so100_mj_runtime", _THIS / "runtime.py")

DEFAULT_MJCF = _c.DEFAULT_MJCF
BASE_BODY = _c.BASE_BODY
SCENE_DEPTH_CAM = _c.SCENE_DEPTH_CAM
WRIST_RGB_CAM = _c.WRIST_RGB_CAM
OBSTACLE_ROD_CENTER_POS_M = _c.OBSTACLE_ROD_CENTER_POS_M
HOME_QPOS = _c.HOME_QPOS

reset_home = _rt.reset_home
resolve_robot_ids = _rt.resolve_robot_ids


def _landmark_points_world(model: mujoco.MjModel, data: mujoco.MjData) -> dict[str, np.ndarray]:
    """标定验证用 3D 路标（世界系）。"""
    from sample.constants import TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL, TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER
    from sample.tcp_pose import quat_rotate_wxyz_single

    pts: dict[str, np.ndarray] = {}
    pts["rod_center"] = np.asarray(OBSTACLE_ROD_CENTER_POS_M, dtype=np.float64)
    pts["scene_lookat"] = np.asarray(_c.SCENE_CAM_LOOKAT_POS_M, dtype=np.float64)

    wr_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "wrist_roll")
    gr_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "gripper")
    wr_q = data.xquat[wr_id]
    gr_q = data.xquat[gr_id]
    pts["fixed_finger_tip"] = data.xpos[wr_id] + quat_rotate_wxyz_single(
        wr_q, np.array(TCP_FIXED_FINGER_TIP_LOCAL_WRIST_ROLL, dtype=np.float64)
    )
    pts["moving_finger_tip"] = data.xpos[gr_id] + quat_rotate_wxyz_single(
        gr_q, np.array(TCP_MOVING_FINGER_TIP_LOCAL_GRIPPER, dtype=np.float64)
    )
    return pts


def _reprojection_report(
    intr,
    T_wc: np.ndarray,
    landmarks: dict[str, np.ndarray],
) -> list[tuple[str, float, float, str]]:
    """返回 (name, u, v, status)；status=OK|behind|off。"""
    names = list(landmarks.keys())
    pts = np.stack([landmarks[k] for k in names], axis=0)
    uv, valid = _cal.project_world(intr, T_wc, pts)
    rows = []
    for i, name in enumerate(names):
        u, v = float(uv[i, 0]), float(uv[i, 1])
        if not valid[i]:
            rows.append((name, u, v, "behind"))
        elif 0 <= u < intr.width and 0 <= v < intr.height:
            rows.append((name, u, v, "OK"))
        else:
            rows.append((name, u, v, "off"))
    return rows


def _wrist_nearfield_landmark(model: mujoco.MjModel, data: mujoco.MjData, cam_name: str) -> np.ndarray:
    """腕部相机正前方 15cm 处测试点（home 位应在像面内）。"""
    cid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, cam_name)
    cam_pos = np.asarray(data.cam_xpos[cid], dtype=np.float64)
    rot = np.asarray(data.cam_xmat[cid], dtype=np.float64).reshape(3, 3)
    view = -rot[:, 2]  # MuJoCo 光轴 -Z
    return cam_pos + 0.15 * view


def _wrist_arm_qpos_list(n: int, seed: int) -> list[np.ndarray]:
    """与 calib_chessboard_sim 一致的腕部工作区姿态采样。"""
    rng = np.random.default_rng(seed)
    home = np.array(HOME_QPOS, dtype=np.float64)
    poses: list[np.ndarray] = []
    for _ in range(n):
        q = home.copy()
        q[0] += rng.uniform(-0.25, 0.35)
        q[1] += rng.uniform(-0.20, 0.15)
        q[2] += rng.uniform(-0.15, 0.25)
        q[3] += rng.uniform(-0.35, 0.35)
        q[4] += rng.uniform(-0.25, 0.25)
        q[5] += rng.uniform(-0.50, 0.50)
        poses.append(q)
    return poses


def _set_robot_qpos(model: mujoco.MjModel, data: mujoco.MjData, q: np.ndarray) -> None:
    for i, adr in enumerate(resolve_robot_ids(model).qpos_adr):
        data.qpos[adr] = q[i]
    mujoco.mj_forward(model, data)


def _check_wrist_across_poses(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    cal,
    n_poses: int,
    seed: int,
) -> None:
    """换姿态验证腕部：FK 链 + 正前方路标重投影；scene 路标仅统计可见性。"""
    intr = cal.intrinsics[WRIST_RGB_CAM]
    wrist_mount = cal.mounts[WRIST_RGB_CAM].T_parent_cam
    rod = np.asarray(OBSTACLE_ROD_CENTER_POS_M, dtype=np.float64)

    fk_max = 0.0
    near_ok = 0
    rod_ok = 0
    best_rod: tuple[np.ndarray, float, float] | None = None

    for q in _wrist_arm_qpos_list(n_poses, seed):
        _set_robot_qpos(model, data, q)
        T_wc = _cal.T_world_cam(model, data, WRIST_RGB_CAM)
        T_fk = _cal.T_world_cam_from_mount(
            model, data, _c.WRIST_RGB_CAM_PARENT, wrist_mount
        )
        fk_max = max(fk_max, float(np.linalg.norm(T_wc - T_fk)))

        near = _wrist_nearfield_landmark(model, data, WRIST_RGB_CAM)
        uv, valid = _cal.project_world(intr, T_wc, near.reshape(1, 3))
        u, v = float(uv[0, 0]), float(uv[0, 1])
        if valid[0] and 0 <= u < intr.width and 0 <= v < intr.height:
            near_ok += 1

        uv_r, valid_r = _cal.project_world(intr, T_wc, rod.reshape(1, 3))
        ur, vr = float(uv_r[0, 0]), float(uv_r[0, 1])
        if valid_r[0] and 0 <= ur < intr.width and 0 <= vr < intr.height:
            rod_ok += 1
            if best_rod is None:
                best_rod = (q.copy(), ur, vr)

    print(
        f"\n[calib_verify] 腕部换姿态验证 (n={n_poses}, chess 采样):"
    )
    print(f"  FK 合成外参 max err = {fk_max:.2e}")
    print(f"  cam_forward_15cm 像面内 = {near_ok}/{n_poses}")
    print(f"  rod_center 像面内 = {rod_ok}/{n_poses}")
    if best_rod is not None:
        q, ur, vr = best_rod
        print(
            f"  rod 可见姿态 q[:6]={np.round(q[:6], 3)}  proj=({ur:.1f},{vr:.1f})"
        )
    else:
        print(
            "  rod_center 在采样姿态下均不可见：wrist 朝指缝前方，"
            "杆在侧方工作区，非标定错误；请用棋盘格多姿态验证（calib_chessboard_sim）"
        )


def _check_wrist_mount_invariance(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    n_poses: int,
    seed: int,
) -> tuple[float, float]:
    """随机关节角下 T_wrist_roll_cam 应不变（手眼静态）。"""
    rng = np.random.default_rng(seed)
    parent = _c.WRIST_RGB_CAM_PARENT
    refs: list[np.ndarray] = []
    for _ in range(n_poses):
        q = np.array(HOME_QPOS, dtype=np.float64)
        q[:6] += rng.normal(0.0, 0.35, size=6)
        for i, adr in enumerate(resolve_robot_ids(model).qpos_adr):
            data.qpos[adr] = q[i]
        mujoco.mj_forward(model, data)
        refs.append(_cal.T_parent_cam_static(model, data, WRIST_RGB_CAM, parent))
    T0 = refs[0]
    t_err = max(float(np.linalg.norm(T[:3, 3] - T0[:3, 3])) for T in refs[1:])
    r_err = max(
        float(np.linalg.norm(T[:3, :3] - T0[:3, :3], ord="fro")) for T in refs[1:]
    )
    return t_err, r_err


def _check_mount_vs_fk(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    cal,
) -> tuple[float, float]:
    """T_world_cam 应等于 T_world_parent @ T_parent_cam。"""
    scene_mount = cal.mounts[SCENE_DEPTH_CAM].T_parent_cam
    wrist_mount = cal.mounts[WRIST_RGB_CAM].T_parent_cam
    T_wc_scene_mj = _cal.T_world_cam(model, data, SCENE_DEPTH_CAM)
    T_wc_scene_fk = _cal.T_world_cam_from_mount(model, data, BASE_BODY, scene_mount)
    T_wc_wrist_mj = _cal.T_world_cam(model, data, WRIST_RGB_CAM)
    T_wc_wrist_fk = _cal.T_world_cam_from_mount(
        model, data, _c.WRIST_RGB_CAM_PARENT, wrist_mount
    )
    e_scene = float(np.linalg.norm(T_wc_scene_mj - T_wc_scene_fk))
    e_wrist = float(np.linalg.norm(T_wc_wrist_mj - T_wc_wrist_fk))
    return e_scene, e_wrist


def _maybe_annotate(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    cal,
    landmarks: dict[str, np.ndarray],
    out_dir: Path,
) -> None:
    try:
        from mujoco import Renderer
    except Exception as exc:
        print(f"[calib_verify] skip annotate (Renderer): {exc}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        import cv2
    except ImportError:
        print("[calib_verify] skip annotate: no cv2")
        return

    renderer = Renderer(model, height=_c.CAM_HEIGHT, width=_c.CAM_WIDTH)
    for cam_name in (SCENE_DEPTH_CAM, WRIST_RGB_CAM):
        cid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, cam_name)
        intr = cal.intrinsics[cam_name]
        T_wc = _cal.T_world_cam(model, data, cam_name)
        renderer.update_scene(data, camera=cid)
        rgb = np.asarray(renderer.render(), dtype=np.uint8)
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        for name, p_w in landmarks.items():
            uv, valid = _cal.project_world(intr, T_wc, p_w.reshape(1, 3))
            if not valid[0]:
                continue
            u, v = int(round(uv[0, 0])), int(round(uv[0, 1]))
            if 0 <= u < intr.width and 0 <= v < intr.height:
                cv2.circle(bgr, (u, v), 6, (0, 255, 255), 2)
                cv2.putText(
                    bgr,
                    name[:12],
                    (u + 8, v - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (0, 255, 255),
                    1,
                    cv2.LINE_AA,
                )
        cv2.imwrite(str(out_dir / f"reproj_{cam_name}.png"), bgr)
    renderer.close()
    print(f"[calib_verify] 重投影标注 → {out_dir}/reproj_*.png")


def run(args: argparse.Namespace) -> int:
    mjcf = Path(args.mjcf).expanduser().resolve()
    model = mujoco.MjModel.from_xml_path(str(mjcf))
    data = mujoco.MjData(model)
    ids = resolve_robot_ids(model)
    reset_home(model, data, ids)

    cal = _cal.export_sim_calibration(model, data, world_frame=BASE_BODY)
    out_path = Path(args.out).expanduser().resolve()
    cal.save_json(out_path)
    print(f"[calib_verify] 标定 JSON → {out_path}")

    landmarks = _landmark_points_world(model, data)
    wrist_near = {"cam_forward_15cm": _wrist_nearfield_landmark(model, data, WRIST_RGB_CAM)}

    print("\n[calib_verify] home 重投影 (u,v) 像素；[OK]=像面内 [behind]=相机后方 [off]=前方但视线外")
    for cam_name in (SCENE_DEPTH_CAM, WRIST_RGB_CAM):
        intr = cal.intrinsics[cam_name]
        T_wc = _cal.T_world_cam(model, data, cam_name)
        print(f"  --- {cam_name} ---")
        if cam_name == WRIST_RGB_CAM:
            print(
                "    注: 下列 rod/lookat/指尖 为 scene 视野路标；"
                "home 时 wrist 朝指缝前方，多数在后方或视线外属正常"
            )
        lm = landmarks if cam_name == SCENE_DEPTH_CAM else {**landmarks, **wrist_near}
        for name, u, v, status in _reprojection_report(intr, T_wc, lm):
            u_s = f"{u:7.1f}" if np.isfinite(u) else "    nan"
            v_s = f"{v:7.1f}" if np.isfinite(v) else "    nan"
            print(f"    {name:18s} ({u_s}, {v_s})  [{status}]")

    e_scene, e_wrist = _check_mount_vs_fk(model, data, cal)
    print(
        f"\n[calib_verify] FK 合成外参误差 (Frobenius): "
        f"scene={e_scene:.2e}  wrist={e_wrist:.2e}"
    )

    t_err, r_err = _check_wrist_mount_invariance(model, data, int(args.poses), int(args.seed))
    print(
        f"[calib_verify] 腕部 T_wrist_roll_cam 随机关节不变性 "
        f"(n={args.poses}): |dt|_max={t_err:.2e} m  |dR|_fro_max={r_err:.2e}"
    )
    if t_err > 1e-5 or r_err > 1e-5:
        print("[WARN] 腕部静态外参随姿态漂移偏大，检查 MJCF 挂载 parent")

    _check_wrist_across_poses(model, data, cal, int(args.wrist_poses), int(args.seed))

    T_nom = _cal.wrist_mount_from_mjcf_constants()
    T_sim = cal.mounts[WRIST_RGB_CAM].T_parent_cam
    nom_err = float(np.linalg.norm(T_nom - T_sim))
    print(f"[calib_verify] MJCF 标称 vs 仿真 wrist T_parent_cam: |dT|={nom_err:.2e}")

    if args.annotate:
        ann_dir = out_path.parent / "reproj_vis"
        _maybe_annotate(model, data, cal, landmarks, ann_dir)

    print(
        "\n[calib_verify] 真机提示:\n"
        "  scene_depth: 标定一次 T_base_cam，写入 JSON mounts.scene_depth\n"
        "  wrist_rgb:   手眼标定 T_wrist_roll_cam；每步 T_world_cam = T_world_wrist_roll(q) @ T_wrist_roll_cam\n"
        "  勿将腕部 world 外参当常数使用。"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MuJoCo 双相机标定导出与验证")
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument("--out", type=str, default="logs/calib/camera_calib.json")
    p.add_argument("--poses", type=int, default=24, help="腕部不变性随机姿态数")
    p.add_argument("--wrist-poses", type=int, default=20, help="腕部换姿态重投影采样数")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--annotate",
        action="store_true",
        help="渲染 RGB 并标注路标投影（需本机 OpenGL）",
    )
    return p


if __name__ == "__main__":
    raise SystemExit(run(build_parser().parse_args()))
