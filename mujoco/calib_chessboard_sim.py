#!/usr/bin/env python3
"""仿真棋盘格标定：OpenCV 角点检测 + 与 MuJoCo ground truth 对比。

  cd soarm100sim
  python mujoco/calib_chessboard_sim.py                    # 固定 scene_depth
  python mujoco/calib_chessboard_sim.py --camera wrist_rgb --arm-poses 12
  python mujoco/calib_chessboard_sim.py --camera both --out-dir log/runtime/calib/chess_sim

流程：
  1. 场景内放置已知尺寸的棋盘格（scene_calib_chess.xml）
  2. 多视角渲染 RGB（固定相机动棋盘 / 腕部相机动机械臂）
  3. findChessboardCorners → calibrateCamera / solvePnP
  4. 与 calib.py 导出的 GT 内参、外参比较

真机前在仿真里跑通此流程，可验证标定代码与 OpenCV 约定无误。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import mujoco
import numpy as np

_THIS = Path(__file__).resolve().parent
_RL_ROOT = _THIS.parent / "rl"
if str(_RL_ROOT) not in sys.path:
    sys.path.insert(0, str(_RL_ROOT))

_MJCF_DIR = _THIS.parent / "SO-ARM100" / "Simulation" / "SO100" / "mujoco"
DEFAULT_MJCF = _MJCF_DIR / "scene_calib_chess.xml"
TEXTURE_PATH = _MJCF_DIR / "assets" / "calib_checker.png"


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
_board = _load_local("so100_mj_calib_board", _THIS / "calib_board.py")
_rt = _load_local("so100_mj_runtime", _THIS / "runtime.py")

SCENE_DEPTH_CAM = _c.SCENE_DEPTH_CAM
WRIST_RGB_CAM = _c.WRIST_RGB_CAM
WRIST_RGB_CAM_PARENT = _c.WRIST_RGB_CAM_PARENT
BASE_BODY = _c.BASE_BODY
HOME_QPOS = _c.HOME_QPOS
CAM_WIDTH = _c.CAM_WIDTH
CAM_HEIGHT = _c.CAM_HEIGHT

reset_home = _rt.reset_home
resolve_robot_ids = _rt.resolve_robot_ids


def _ensure_texture(spec: _board.ChessboardSpec) -> None:
    if not TEXTURE_PATH.is_file():
        _board.generate_checker_texture(spec, TEXTURE_PATH)
        print(f"[chess_sim] 生成棋盘纹理 → {TEXTURE_PATH}")


def _scene_depth_board_poses(spec: _board.ChessboardSpec, n: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """固定相机：棋盘放在视线前方（尽量正对、少遮挡）。"""
    cam_pos = np.array([0.05, -0.15, 0.50], dtype=np.float64)
    view = np.array([0.20, 0.05, 0.18], dtype=np.float64) - cam_pos
    view /= max(float(np.linalg.norm(view)), 1e-9)
    poses: list[tuple[np.ndarray, np.ndarray]] = []
    rng = np.random.default_rng(7)
    for i in range(n):
        dist = 0.34 + rng.uniform(-0.04, 0.06)
        pos = cam_pos + view * dist
        pos += np.array(
            [rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05), rng.uniform(-0.03, 0.03)],
            dtype=np.float64,
        )
        q = _board.quat_board_facing_point(pos, cam_pos)
        poses.append((pos, q))
    return poses


def _corners_gt(
    spec: _board.ChessboardSpec,
    intr: _cal.CameraIntrinsics,
    T_wc: np.ndarray,
    T_wb: np.ndarray,
    *,
    noise_px: float,
    rng: np.random.Generator,
) -> np.ndarray | None:
    """仿真 GT：将已知 3D 角点投影到像素（等效完美角点检测）。"""
    pts_w = _board.object_points_world(spec, T_wb)
    uv, valid = _cal.project_world(intr, T_wc, pts_w)
    if not np.all(valid):
        return None
    if noise_px > 0.0:
        uv = uv + rng.normal(0.0, noise_px, uv.shape)
    return uv.astype(np.float64)


def _collect_view(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    renderer: mujoco.Renderer,
    spec: _board.ChessboardSpec,
    cam_name: str,
    gt_intr: _cal.CameraIntrinsics,
    detect_mode: str,
    noise_px: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray | None, np.ndarray, np.ndarray | None]:
    """返回 (corners, gray, T_wb)。"""
    gray = _capture_gray(model, data, renderer, cam_name)
    T_wb = _board.board_T_world(model, data)
    T_wc = _cal.T_world_cam(model, data, cam_name)
    corners: np.ndarray | None
    if detect_mode == "gt":
        corners = _corners_gt(spec, gt_intr, T_wc, T_wb, noise_px=noise_px, rng=rng)
    else:
        corners = _board.detect_corners(gray, spec)
    return corners, gray, T_wb


def _wrist_arm_qpos_list(n: int, seed: int) -> list[np.ndarray]:
    """腕部相机能俯视工作区棋盘的关节角采样。"""
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


def _set_board_facing_arm(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    board_pos: np.ndarray,
    cam_pos: np.ndarray,
) -> None:
    q = _board.quat_board_facing_point(board_pos, cam_pos)
    _board.set_free_body_pose(model, data, "calib_board", board_pos, q)


def _capture_gray(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    renderer: mujoco.Renderer,
    cam_name: str,
) -> np.ndarray:
    cid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, cam_name)
    renderer.update_scene(data, camera=cid)
    rgb = np.asarray(renderer.render(), dtype=np.uint8)
    import cv2

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return gray


def _calibrate_camera_views(
    spec: _board.ChessboardSpec,
    objpoints: list[np.ndarray],
    imgpoints: list[np.ndarray],
    image_size: tuple[int, int],
) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], list[np.ndarray]]:
    import cv2

    if len(objpoints) < 3:
        raise RuntimeError(
            f"有效视角不足 ({len(objpoints)}/{n_views})，请检查 {vis_dir}/fail_*.png 或增大 --views"
        )
    rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints,
        imgpoints,
        image_size,
        None,
        None,
    )
    print(f"[chess_sim] calibrateCamera RMS={rms:.4f} px  views={len(objpoints)}")
    return K, dist, rvecs, tvecs


def _intrinsic_errors(K_est: np.ndarray, gt: _cal.CameraIntrinsics) -> dict[str, float]:
    Kgt = gt.K
    return {
        "fx_abs": float(abs(K_est[0, 0] - Kgt[0, 0])),
        "fy_abs": float(abs(K_est[1, 1] - Kgt[1, 1])),
        "cx_abs": float(abs(K_est[0, 2] - Kgt[0, 2])),
        "cy_abs": float(abs(K_est[1, 2] - Kgt[1, 2])),
        "fx_rel_pct": float(abs(K_est[0, 0] - Kgt[0, 0]) / Kgt[0, 0] * 100.0),
    }


def _run_scene_depth(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    renderer: mujoco.Renderer,
    spec: _board.ChessboardSpec,
    out_dir: Path,
    n_views: int,
    detect_mode: str,
    noise_px: float,
    seed: int,
) -> dict:
    gt_intr = _cal.camera_intrinsics(model, SCENE_DEPTH_CAM)
    gt_T_wc = _cal.T_world_cam(model, data, SCENE_DEPTH_CAM)
    gt_T_base_cam = _cal.T_parent_cam_static(model, data, SCENE_DEPTH_CAM, BASE_BODY)

    objpoints: list[np.ndarray] = []
    imgpoints: list[np.ndarray] = []
    T_wc_est_views: list[np.ndarray] = []
    T_wb_views: list[np.ndarray] = []

    vis_dir = out_dir / "scene_depth"
    vis_dir.mkdir(parents=True, exist_ok=True)
    import cv2

    rng = np.random.default_rng(seed)
    print(f"[chess_sim] scene_depth detect={detect_mode}")

    for i, (pos, quat) in enumerate(_scene_depth_board_poses(spec, n_views)):
        _board.set_free_body_pose(model, data, "calib_board", pos, quat)
        corners, gray, T_wb = _collect_view(
            model, data, renderer, spec, SCENE_DEPTH_CAM, gt_intr, detect_mode, noise_px, rng
        )
        if corners is None or T_wb is None:
            print(f"[chess_sim] scene_depth view {i:02d}: 无有效角点，跳过")
            cv2.imwrite(str(vis_dir / f"fail_{i:02d}.png"), cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))
            continue
        T_wb_views.append(T_wb)
        objpoints.append(spec.object_points().astype(np.float32))
        imgpoints.append(corners.astype(np.float32))
        ok, rvec, tvec = cv2.solvePnP(
            spec.object_points().astype(np.float32),
            corners.astype(np.float32),
            gt_intr.K.astype(np.float64),
            None,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
        if ok:
            if detect_mode == "gt":
                T_wc_est = _cal.T_world_cam(model, data, SCENE_DEPTH_CAM)
            else:
                T_wc_est = _board.T_world_cam_from_opencv_rvec_tvec(rvec, tvec, T_wb)
            if T_wc_est is not None:
                T_wc_est_views.append(T_wc_est)
        vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        if detect_mode == "render":
            cv2.drawChessboardCorners(vis, spec.pattern_size, corners.astype(np.float32), True)
        else:
            for u, v in corners:
                cv2.circle(vis, (int(round(u)), int(round(v))), 4, (0, 255, 255), 1)
        cv2.imwrite(str(vis_dir / f"view_{i:02d}.png"), vis)

    if len(objpoints) < 3:
        raise RuntimeError(
            f"scene_depth 有效视角不足 ({len(objpoints)}/{n_views})，"
            f"请查看 {vis_dir}/fail_*.png 或增大 --views"
        )

    K_est, dist, rvecs, tvecs = _calibrate_camera_views(
        spec, objpoints, imgpoints, (CAM_WIDTH, CAM_HEIGHT)
    )
    intr_err = _intrinsic_errors(K_est, gt_intr)

    ext_pos_err = [
        float(np.linalg.norm(T[:3, 3] - gt_T_wc[:3, 3])) for T in T_wc_est_views
    ]
    T_base_est_list = [
        _board.T_parent_cam_from_world_cam(T, _cal.body_T_world(model, data, BASE_BODY))
        for T in T_wc_est_views
    ]
    T_base_est = T_base_est_list[len(T_base_est_list) // 2] if T_base_est_list else gt_T_base_cam
    mount_err = float(np.linalg.norm(T_base_est - gt_T_base_cam))

    print(
        f"[chess_sim] scene_depth 内参: fx_err={intr_err['fx_abs']:.3f}px "
        f"({intr_err['fx_rel_pct']:.3f}%)  cx_err={intr_err['cx_abs']:.3f}px"
    )
    if ext_pos_err:
        print(
            f"[chess_sim] scene_depth 外参(每视角PnP): "
            f"|dt| mean={np.mean(ext_pos_err)*1000:.2f}mm max={np.max(ext_pos_err)*1000:.2f}mm"
        )
    print(f"[chess_sim] scene_depth T_base_cam Frobenius err={mount_err:.4e}")

    return {
        "camera": SCENE_DEPTH_CAM,
        "n_views_ok": len(objpoints),
        "intrinsic_error": intr_err,
        "K_est": K_est.tolist(),
        "K_gt": gt_intr.K.tolist(),
        "extrinsic_pos_err_mm": ext_pos_err,
        "T_base_cam_mount_err": mount_err,
    }


def _run_wrist_rgb(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    renderer: mujoco.Renderer,
    spec: _board.ChessboardSpec,
    out_dir: Path,
    n_poses: int,
    seed: int,
    detect_mode: str,
    noise_px: float,
) -> dict:
    gt_intr = _cal.camera_intrinsics(model, WRIST_RGB_CAM)
    gt_T_wr_cam = _cal.T_parent_cam_static(model, data, WRIST_RGB_CAM, WRIST_RGB_CAM_PARENT)

    board_pos = np.array([0.36, 0.0, 0.22], dtype=np.float64)
    ids = resolve_robot_ids(model)
    # 棋盘固定在世界系；仅动机械臂（眼在手上标定）
    scene_cam = data.cam_xpos[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, SCENE_DEPTH_CAM)]
    _board.set_free_body_pose(
        model, data, "calib_board", board_pos, _board.quat_board_facing_point(board_pos, scene_cam)
    )

    objpoints: list[np.ndarray] = []
    imgpoints: list[np.ndarray] = []
    T_wr_cam_est: list[np.ndarray] = []

    vis_dir = out_dir / "wrist_rgb"
    vis_dir.mkdir(parents=True, exist_ok=True)
    import cv2

    rng = np.random.default_rng(seed + 1)
    print(f"[chess_sim] wrist_rgb detect={detect_mode}")

    for i, q in enumerate(_wrist_arm_qpos_list(n_poses, seed)):
        for j, adr in enumerate(ids.qpos_adr):
            data.qpos[adr] = q[j]
        mujoco.mj_forward(model, data)
        corners, gray, T_wb = _collect_view(
            model, data, renderer, spec, WRIST_RGB_CAM, gt_intr, detect_mode, noise_px, rng
        )
        if corners is None or T_wb is None:
            print(f"[chess_sim] wrist_rgb pose {i:02d}: 无有效角点，跳过")
            continue
        objpoints.append(spec.object_points().astype(np.float32))
        imgpoints.append(corners.astype(np.float32))
        ok, rvec, tvec = cv2.solvePnP(
            spec.object_points().astype(np.float32),
            corners.astype(np.float32),
            gt_intr.K.astype(np.float64),
            None,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
        if not ok:
            continue
        T_wc = (
            _cal.T_world_cam(model, data, WRIST_RGB_CAM)
            if detect_mode == "gt"
            else _board.T_world_cam_from_opencv_rvec_tvec(rvec, tvec, T_wb)
        )
        if T_wc is None:
            continue
        T_w_wr = _cal.body_T_world(model, data, WRIST_RGB_CAM_PARENT)
        T_wr_cam_est.append(_board.T_parent_cam_from_world_cam(T_wc, T_w_wr))
        vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        if detect_mode == "render":
            cv2.drawChessboardCorners(vis, spec.pattern_size, corners.astype(np.float32), True)
        else:
            for u, v in corners:
                cv2.circle(vis, (int(round(u)), int(round(v))), 4, (0, 255, 255), 1)
        cv2.imwrite(str(vis_dir / f"pose_{i:02d}.png"), vis)

    if len(objpoints) < 3:
        print(
            "[WARN] wrist_rgb 有效视角不足；棋盘可能不在腕部 FOV，"
            "可调整 board_pos 或 --arm-poses"
        )
        return {
            "camera": WRIST_RGB_CAM,
            "n_views_ok": len(objpoints),
            "skipped": True,
        }

    K_est, dist, rvecs, tvecs = _calibrate_camera_views(
        spec, objpoints, imgpoints, (CAM_WIDTH, CAM_HEIGHT)
    )
    intr_err = _intrinsic_errors(K_est, gt_intr)

    T0 = T_wr_cam_est[0]
    t_spread = max(float(np.linalg.norm(T[:3, 3] - T0[:3, 3])) for T in T_wr_cam_est[1:])
    r_spread = max(float(np.linalg.norm(T[:3, :3] - T0[:3, :3], ord="fro")) for T in T_wr_cam_est[1:])
    T_wr_mean = T_wr_cam_est[len(T_wr_cam_est) // 2]
    mount_err = float(np.linalg.norm(T_wr_mean - gt_T_wr_cam))

    print(
        f"[chess_sim] wrist_rgb 内参: fx_err={intr_err['fx_abs']:.3f}px "
        f"({intr_err['fx_rel_pct']:.3f}%)"
    )
    print(
        f"[chess_sim] wrist_rgb 手眼 T_wrist_roll_cam 跨姿态 spread: "
        f"|dt|_max={t_spread*1000:.3f}mm  |dR|_fro_max={r_spread:.4e}"
    )
    print(f"[chess_sim] wrist_rgb T_wrist_roll_cam vs GT Frobenius={mount_err:.4e}")

    return {
        "camera": WRIST_RGB_CAM,
        "n_views_ok": len(objpoints),
        "intrinsic_error": intr_err,
        "handeye_t_spread_mm": t_spread * 1000.0,
        "handeye_R_spread_fro": r_spread,
        "T_wrist_roll_cam_mount_err": mount_err,
    }


def run(args: argparse.Namespace) -> int:
    try:
        import cv2  # noqa: F401
    except ImportError:
        print("[ERROR] 需要 opencv-python: pip install opencv-python", file=sys.stderr)
        return 1

    spec = _board.ChessboardSpec(
        inner_cols=int(args.cols),
        inner_rows=int(args.rows),
        square_size_m=float(args.square_size),
    )
    _ensure_texture(spec)

    mjcf = Path(args.mjcf).expanduser().resolve()
    model = mujoco.MjModel.from_xml_path(str(mjcf))
    data = mujoco.MjData(model)
    ids = resolve_robot_ids(model)
    reset_home(model, data, ids)

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        renderer = mujoco.Renderer(model, height=CAM_HEIGHT, width=CAM_WIDTH)
    except Exception as exc:
        print(f"[ERROR] 无法创建 MuJoCo Renderer（需本机 OpenGL）: {exc}", file=sys.stderr)
        return 1

    results: dict = {
        "detect_mode": args.detect,
        "spec": {"cols": spec.inner_cols, "rows": spec.inner_rows, "square_m": spec.square_size_m},
    }
    try:
        if args.camera in ("scene_depth", "both"):
            results["scene_depth"] = _run_scene_depth(
                model,
                data,
                renderer,
                spec,
                out_dir,
                int(args.views),
                str(args.detect),
                float(args.noise_px),
                int(args.seed),
            )
        if args.camera in ("wrist_rgb", "both"):
            reset_home(model, data, ids)
            results["wrist_rgb"] = _run_wrist_rgb(
                model,
                data,
                renderer,
                spec,
                out_dir,
                int(args.arm_poses),
                int(args.seed),
                str(args.detect),
                float(args.noise_px),
            )
    finally:
        renderer.close()

    report_path = out_dir / "chess_calib_report.json"
    report_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[chess_sim] 报告 → {report_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MuJoCo 仿真棋盘格标定")
    p.add_argument("--mjcf", type=str, default=str(DEFAULT_MJCF))
    p.add_argument("--out-dir", type=str, default="log/runtime/calib/chess_sim")
    p.add_argument(
        "--camera",
        choices=("scene_depth", "wrist_rgb", "both"),
        default="scene_depth",
    )
    p.add_argument(
        "--detect",
        choices=("gt", "render"),
        default="gt",
        help="gt=已知 3D 角点投影（仿真主路径）；render=OpenCV 从 RGB 检测",
    )
    p.add_argument(
        "--noise-px",
        type=float,
        default=0.0,
        help="gt 模式下像素噪声 std（模拟角点检测误差）",
    )
    p.add_argument("--views", type=int, default=12, help="固定相机：棋盘视角数")
    p.add_argument("--arm-poses", type=int, default=14, help="腕部相机：机械臂姿态数")
    p.add_argument("--cols", type=int, default=9, help="内角点列数")
    p.add_argument("--rows", type=int, default=6, help="内角点行数")
    p.add_argument("--square-size", type=float, default=0.025, help="方格边长 (m)")
    p.add_argument("--seed", type=int, default=42)
    return p


if __name__ == "__main__":
    raise SystemExit(run(build_parser().parse_args()))
