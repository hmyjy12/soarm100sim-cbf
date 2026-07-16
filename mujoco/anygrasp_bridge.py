"""Bridge MuJoCo RGB-D frames to AnyGrasp grasp candidates."""

from __future__ import annotations

import os
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np

try:
    from .calib import T_world_cam, camera_intrinsics
    from .camera import MujocoCameraRig
    from .constants import CAM_HEIGHT, CAM_WIDTH, REPO_ROOT, SCENE_DEPTH_CAM
    from .vision_obstacle import unproject_depth_map
except ImportError:
    from calib import T_world_cam, camera_intrinsics  # type: ignore
    from camera import MujocoCameraRig  # type: ignore
    from constants import CAM_HEIGHT, CAM_WIDTH, REPO_ROOT, SCENE_DEPTH_CAM  # type: ignore
    from vision_obstacle import unproject_depth_map  # type: ignore


MUJOCO_TO_ANYGRASP_CAM = np.diag([1.0, -1.0, -1.0]).astype(np.float64)


@dataclass
class AnyGraspCandidate:
    pos_world: np.ndarray
    rot_world: np.ndarray
    approach_world: np.ndarray
    width: float
    depth: float
    score: float
    pos_camera_anygrasp: np.ndarray
    rot_camera_anygrasp: np.ndarray


@dataclass
class AnyGraspDebug:
    enabled: bool = False
    ok: bool = False
    message: str = ""
    n_points: int = 0
    n_raw: int = 0
    n_depth_valid: int = 0
    n_workspace: int = 0
    n_target_roi: int = 0
    mask_source: str = ""
    target_geom_name: str = ""
    target_geom_id: int = -1
    mask_centroid_world: list[float] = field(default_factory=list)
    mask_bbox_min_world: list[float] = field(default_factory=list)
    mask_bbox_max_world: list[float] = field(default_factory=list)
    mask_centroid_error_m: float = float("nan")
    worker_info: dict = field(default_factory=dict)
    n_candidates: int = 0
    best_score: float = float("nan")
    target_roi_radius_m: float = 0.0
    top_candidates: list[dict] = field(default_factory=list)


@dataclass
class AnyGraspConfig:
    checkpoint_path: str = str(REPO_ROOT / "anygrasp_sdk" / "grasp_detection" / "log" / "checkpoint_detection.tar")
    sdk_root: str = str(REPO_ROOT / "anygrasp_sdk")
    cam_name: str = SCENE_DEPTH_CAM
    min_depth_m: float = 0.12
    max_depth_m: float = 1.1
    top_k: int = 20
    min_score: float = 0.05
    min_width: float = 0.0
    max_width: float = 0.10
    dense_grasp: bool = False
    collision_detection: bool = True
    max_points: int = 20000
    mask_source: str = "target_geom_seg"
    target_geom_name: str = "target_object_geom"
    target_mask_dilate_px: int = 0
    target_mask_expand_ratio: float = 0.0
    target_mask_min_points: int = 20
    camera_warmup_frames: int = 2
    roi_x: tuple[float, float] = (0.02, 0.42)
    roi_y: tuple[float, float] = (-0.20, 0.24)
    roi_z: tuple[float, float] = (0.02, 0.46)
    target_roi_radius_m: float = 0.10
    conda_env: str = "graspnet_gpu"
    subprocess_timeout_s: float = 60.0


def _filter_workspace(points_w: np.ndarray, cfg: AnyGraspConfig) -> np.ndarray:
    pts = np.asarray(points_w, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return pts
    m = (
        (pts[:, 0] >= cfg.roi_x[0])
        & (pts[:, 0] <= cfg.roi_x[1])
        & (pts[:, 1] >= cfg.roi_y[0])
        & (pts[:, 1] <= cfg.roi_y[1])
        & (pts[:, 2] >= cfg.roi_z[0])
        & (pts[:, 2] <= cfg.roi_z[1])
    )
    return pts[m]


def _limit_points(points: np.ndarray, max_points: int) -> np.ndarray:
    pts = np.asarray(points)
    n = pts.shape[0]
    if n <= int(max_points):
        return pts
    idx = np.linspace(0, n - 1, int(max_points), dtype=np.int64)
    return pts[idx]


def _dilate_mask(mask: np.ndarray, radius_px: int) -> np.ndarray:
    m = np.asarray(mask, dtype=bool)
    r = max(int(radius_px), 0)
    if r == 0 or m.size == 0:
        return m
    out = m.copy()
    h, w = m.shape
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx == 0 and dy == 0:
                continue
            y0 = max(0, dy)
            y1 = min(h, h + dy)
            x0 = max(0, dx)
            x1 = min(w, w + dx)
            sy0 = max(0, -dy)
            sy1 = min(h, h - dy)
            sx0 = max(0, -dx)
            sx1 = min(w, w - dx)
            out[y0:y1, x0:x1] |= m[sy0:sy1, sx0:sx1]
    return out


def _expand_mask_bbox(mask: np.ndarray, ratio: float) -> np.ndarray:
    m = np.asarray(mask, dtype=bool)
    if m.size == 0 or not np.any(m):
        return m
    r = max(float(ratio), 0.0)
    if r <= 0.0:
        return m
    ys, xs = np.nonzero(m)
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    h, w = m.shape
    pad_y = max(1, int(round((y1 - y0 + 1) * r)))
    pad_x = max(1, int(round((x1 - x0 + 1) * r)))
    out = np.zeros_like(m, dtype=bool)
    out[max(0, y0 - pad_y) : min(h, y1 + pad_y + 1), max(0, x0 - pad_x) : min(w, x1 + pad_x + 1)] = True
    return out


def _unproject_masked_depth(
    intr,
    T_wc: np.ndarray,
    depth: np.ndarray,
    mask: np.ndarray,
    *,
    min_depth_m: float,
    max_depth_m: float,
) -> np.ndarray:
    d = np.asarray(depth, dtype=np.float64).copy()
    m = np.asarray(mask, dtype=bool)
    if d.shape[:2] != m.shape:
        raise ValueError(f"depth/mask shape mismatch: depth={d.shape} mask={m.shape}")
    d[~m] = np.nan
    return unproject_depth_map(intr, T_wc, d, min_depth_m=min_depth_m, max_depth_m=max_depth_m)


class AnyGraspBridge:
    def __init__(self, model: mujoco.MjModel, cfg: AnyGraspConfig | None = None) -> None:
        self.cfg = cfg or AnyGraspConfig()
        self._rig = MujocoCameraRig(model, width=CAM_WIDTH, height=CAM_HEIGHT)
        self.last_debug = AnyGraspDebug(enabled=True)
        self.last_candidates: list[AnyGraspCandidate] = []
        self._model = model

    def close(self) -> None:
        self._rig.close()

    def capture_points(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        target_pos_w: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
        intr = camera_intrinsics(model, self.cfg.cam_name, width=CAM_WIDTH, height=CAM_HEIGHT)
        T_wc = T_world_cam(model, data, self.cfg.cam_name)
        mujoco.mj_forward(model, data)
        for _ in range(max(0, int(self.cfg.camera_warmup_frames))):
            self._rig.capture_rgb(data, self.cfg.cam_name)
        depth = self._rig.capture_depth_m(data, self.cfg.cam_name)
        rgb = self._rig.capture_rgb(data, self.cfg.cam_name)
        all_pts_w = unproject_depth_map(
            intr,
            T_wc,
            depth,
            min_depth_m=float(self.cfg.min_depth_m),
            max_depth_m=float(self.cfg.max_depth_m),
        )
        n_depth = int(all_pts_w.shape[0])
        workspace_pts_w = _filter_workspace(all_pts_w, self.cfg)
        pts_w = workspace_pts_w
        n_workspace = int(pts_w.shape[0])

        mask_source = str(self.cfg.mask_source).strip().lower()
        target_geom_id = -1
        if mask_source == "target_geom_seg":
            target_geom_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, str(self.cfg.target_geom_name))
            if target_geom_id < 0:
                raise RuntimeError(f"target geom not found for AnyGrasp mask: {self.cfg.target_geom_name}")
            seg = self._rig.capture_segmentation(data, self.cfg.cam_name)
            if seg.ndim != 3 or seg.shape[2] < 1:
                raise RuntimeError(f"unexpected segmentation image shape: {seg.shape}")
            mask = seg[:, :, 0].astype(np.int32) == int(target_geom_id)
            mask = _expand_mask_bbox(mask, float(self.cfg.target_mask_expand_ratio))
            mask = _dilate_mask(mask, int(self.cfg.target_mask_dilate_px))
            pts_w = _unproject_masked_depth(
                intr,
                T_wc,
                depth,
                mask,
                min_depth_m=float(self.cfg.min_depth_m),
                max_depth_m=float(self.cfg.max_depth_m),
            )
            pts_w = _filter_workspace(pts_w, self.cfg)
            if pts_w.shape[0] < int(self.cfg.target_mask_min_points):
                mujoco.mj_forward(model, data)
                depth = self._rig.capture_depth_m(data, self.cfg.cam_name)
                rgb = self._rig.capture_rgb(data, self.cfg.cam_name)
                seg = self._rig.capture_segmentation(data, self.cfg.cam_name)
                mask = seg[:, :, 0].astype(np.int32) == int(target_geom_id)
                mask = _expand_mask_bbox(mask, float(self.cfg.target_mask_expand_ratio))
                mask = _dilate_mask(mask, int(self.cfg.target_mask_dilate_px))
                pts_w = _unproject_masked_depth(
                    intr,
                    T_wc,
                    depth,
                    mask,
                    min_depth_m=float(self.cfg.min_depth_m),
                    max_depth_m=float(self.cfg.max_depth_m),
                )
                pts_w = _filter_workspace(pts_w, self.cfg)
            if pts_w.shape[0] < int(self.cfg.target_mask_min_points):
                raise RuntimeError(
                    f"target geom mask too small: {pts_w.shape[0]} points "
                    f"(geom={self.cfg.target_geom_name}, id={target_geom_id})"
                )
        elif mask_source == "roi":
            pts_w = workspace_pts_w
        else:
            raise ValueError(f"unknown AnyGrasp mask_source: {self.cfg.mask_source!r}")

        if mask_source == "roi" and target_pos_w is not None and pts_w.shape[0] > 0:
            target = np.asarray(target_pos_w, dtype=np.float64).reshape(1, 3)
            d = np.linalg.norm(pts_w - target, axis=1)
            pts_w = pts_w[d <= float(self.cfg.target_roi_radius_m)]
        n_target_roi = int(pts_w.shape[0])
        if target_pos_w is not None and pts_w.shape[0] > 0:
            centroid = pts_w.mean(axis=0)
            bbox_min = pts_w.min(axis=0)
            bbox_max = pts_w.max(axis=0)
            centroid_err = float(np.linalg.norm(centroid - np.asarray(target_pos_w, dtype=np.float64).reshape(3)))
        else:
            centroid = np.zeros(3, dtype=np.float64)
            bbox_min = np.zeros(3, dtype=np.float64)
            bbox_max = np.zeros(3, dtype=np.float64)
            centroid_err = float("nan")
        pts_w = _limit_points(pts_w, int(self.cfg.max_points))
        R_wc = T_wc[:3, :3]
        t_wc = T_wc[:3, 3]
        pts_mj_cam = (R_wc.T @ (pts_w - t_wc).T).T
        pts_any_cam = (MUJOCO_TO_ANYGRASP_CAM @ pts_mj_cam.T).T
        return (
            np.ascontiguousarray(pts_any_cam, dtype=np.float32),
            np.ascontiguousarray(pts_w, dtype=np.float64),
            rgb,
            {
                "n_depth_valid": n_depth,
                "n_workspace": n_workspace,
                "n_target_roi": n_target_roi,
                "mask_source": mask_source,
                "target_geom_name": str(self.cfg.target_geom_name),
                "target_geom_id": int(target_geom_id),
                "mask_centroid_world": centroid.tolist(),
                "mask_bbox_min_world": bbox_min.tolist(),
                "mask_bbox_max_world": bbox_max.tolist(),
                "mask_centroid_error_m": float(centroid_err),
            },
        )

    def predict(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        target_pos_w: np.ndarray | None = None,
    ) -> list[AnyGraspCandidate]:
        dbg = AnyGraspDebug(enabled=True)
        try:
            points_any, points_w, _rgb, counts = self.capture_points(model, data, target_pos_w=target_pos_w)
            dbg.n_points = int(points_any.shape[0])
            dbg.n_raw = int(points_w.shape[0])
            dbg.n_depth_valid = int(counts.get("n_depth_valid", 0))
            dbg.n_workspace = int(counts.get("n_workspace", 0))
            dbg.n_target_roi = int(counts.get("n_target_roi", 0))
            dbg.target_roi_radius_m = float(self.cfg.target_roi_radius_m)
            dbg.mask_source = str(counts.get("mask_source", ""))
            dbg.target_geom_name = str(counts.get("target_geom_name", ""))
            dbg.target_geom_id = int(counts.get("target_geom_id", -1))
            dbg.mask_centroid_world = list(counts.get("mask_centroid_world", []))
            dbg.mask_bbox_min_world = list(counts.get("mask_bbox_min_world", []))
            dbg.mask_bbox_max_world = list(counts.get("mask_bbox_max_world", []))
            dbg.mask_centroid_error_m = float(counts.get("mask_centroid_error_m", float("nan")))
            if points_any.shape[0] < 50:
                raise RuntimeError(f"not enough points for AnyGrasp: {points_any.shape[0]}")
            raw = self._predict_subprocess(points_any)
            out: list[AnyGraspCandidate] = []
            T_wc = T_world_cam(model, data, self.cfg.cam_name)
            R_wc = T_wc[:3, :3]
            t_wc = T_wc[:3, 3]
            for item in raw.get("candidates", []):
                score = float(item.get("score", float("nan")))
                width = float(item.get("width", float("nan")))
                p_any = np.asarray(item["translation"], dtype=np.float64).reshape(3)
                R_any = np.asarray(item["rotation_matrix"], dtype=np.float64).reshape(3, 3)
                p_mj_cam = MUJOCO_TO_ANYGRASP_CAM @ p_any
                R_mj_cam = MUJOCO_TO_ANYGRASP_CAM @ R_any
                p_w = R_wc @ p_mj_cam + t_wc
                R_w = R_wc @ R_mj_cam
                approach = R_w[:, 0]
                approach /= max(float(np.linalg.norm(approach)), 1e-12)
                out.append(
                    AnyGraspCandidate(
                        pos_world=p_w,
                        rot_world=R_w,
                        approach_world=approach,
                        width=width,
                        depth=float(item.get("depth", 0.0)),
                        score=score,
                        pos_camera_anygrasp=p_any,
                        rot_camera_anygrasp=R_any,
                    )
                )
            dbg.ok = len(out) > 0
            dbg.n_candidates = len(out)
            dbg.best_score = out[0].score if out else float("nan")
            dbg.worker_info = dict(raw.get("debug", {}))
            target = None if target_pos_w is None else np.asarray(target_pos_w, dtype=np.float64).reshape(3)
            top = []
            for c in out[: min(8, len(out))]:
                dist = float("nan") if target is None else float(np.linalg.norm(c.pos_world - target))
                top.append(
                    {
                        "score": float(c.score),
                        "width_m": float(c.width),
                        "dist_to_target_m": dist,
                        "pos_world": np.asarray(c.pos_world, dtype=np.float64).reshape(3).tolist(),
                        "approach_world": np.asarray(c.approach_world, dtype=np.float64).reshape(3).tolist(),
                    }
                )
            dbg.top_candidates = top
            dbg.message = str(raw.get("message", "ok" if out else "no candidate survived filters"))
            self.last_debug = dbg
            self.last_candidates = out
            return out
        except Exception as exc:
            dbg.ok = False
            dbg.message = str(exc)
            self.last_debug = dbg
            self.last_candidates = []
            return []

    def _predict_subprocess(self, points_any: np.ndarray) -> dict:
        sdk_root = Path(self.cfg.sdk_root).expanduser().resolve()
        worker = sdk_root / "grasp_detection" / "predict_npz.py"
        if not worker.is_file():
            raise FileNotFoundError(f"AnyGrasp worker not found: {worker}")
        with tempfile.TemporaryDirectory(prefix="anygrasp_bridge_") as td:
            tdir = Path(td)
            points_path = tdir / "points.npz"
            out_path = tdir / "candidates.json"
            np.savez_compressed(points_path, points=np.ascontiguousarray(points_any, dtype=np.float32))
            conda_prefix = Path(sys.executable).expanduser().resolve().parents[1]
            anygrasp_env = conda_prefix / "envs" / str(self.cfg.conda_env)
            worker_python = anygrasp_env / "bin" / "python"
            py_cmd = str(worker_python) if worker_python.is_file() else "python"
            cmd = [
                py_cmd,
                str(worker),
                "--points-npz",
                str(points_path),
                "--out-json",
                str(out_path),
                "--checkpoint-path",
                str(Path(self.cfg.checkpoint_path).expanduser().resolve()),
                "--sdk-root",
                str(sdk_root),
                "--top-k",
                str(int(self.cfg.top_k)),
                "--min-score",
                str(float(self.cfg.min_score)),
                "--max-width",
                str(float(self.cfg.max_width)),
            ]
            if bool(self.cfg.dense_grasp):
                cmd.append("--dense-grasp")
            if not bool(self.cfg.collision_detection):
                cmd.append("--no-collision-detection")
            env = os.environ.copy()
            env["PATH"] = f"{sdk_root / 'tools'}:{env.get('PATH', '')}"
            env.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-anygrasp")
            ld_prepend = [
                anygrasp_env / "lib",
                anygrasp_env / "targets" / "x86_64-linux" / "lib",
                anygrasp_env / "lib" / "python3.10" / "site-packages" / "torch" / "lib",
            ]
            ld = ":".join(str(p) for p in ld_prepend if p.exists())
            if ld:
                old_ld = env.get("LD_LIBRARY_PATH", "")
                env["LD_LIBRARY_PATH"] = ld + (":" + old_ld if old_ld else "")
            env["PYTHONNOUSERSITE"] = "1"
            env.pop("PYTHONPATH", None)
            env.setdefault("OMP_NUM_THREADS", "12")
            proc = subprocess.run(
                cmd,
                cwd=str(REPO_ROOT),
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=float(self.cfg.subprocess_timeout_s),
                check=False,
            )
            if out_path.is_file():
                raw = json.loads(out_path.read_text(encoding="utf-8"))
            else:
                raw = {
                    "ok": False,
                    "message": "AnyGrasp worker did not produce output JSON",
                    "candidates": [],
                }
            if proc.returncode != 0 and not raw.get("candidates"):
                msg = str(raw.get("message", "")).strip()
                stderr_tail = proc.stderr.strip().splitlines()[-5:]
                raise RuntimeError(f"{msg}; worker rc={proc.returncode}; stderr_tail={' | '.join(stderr_tail)}")
            return raw
