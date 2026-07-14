"""MuJoCo 双相机渲染封装（固定场景深度 + 腕部 RGB）。"""

from __future__ import annotations

from dataclasses import dataclass

import mujoco
import numpy as np

try:
    from .constants import CAM_HEIGHT, CAM_WIDTH, SCENE_DEPTH_CAM, WRIST_RGB_CAM
except ImportError:
    from constants import CAM_HEIGHT, CAM_WIDTH, SCENE_DEPTH_CAM, WRIST_RGB_CAM  # type: ignore


@dataclass
class CameraFrame:
    rgb: np.ndarray | None = None
    depth_m: np.ndarray | None = None


@dataclass
class CameraExtrinsics:
    name: str
    pos_world: np.ndarray
    rot_world: np.ndarray  # 3x3, camera frame → world


def camera_id(model: mujoco.MjModel, name: str) -> int:
    cid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, name)
    if cid < 0:
        raise ValueError(f"camera not found: {name}")
    return int(cid)


def camera_extrinsics(model: mujoco.MjModel, data: mujoco.MjData, name: str) -> CameraExtrinsics:
    """相机世界系位姿（MuJoCo 相机光轴沿 -Z）。"""
    cid = camera_id(model, name)
    pos = np.asarray(data.cam_xpos[cid], dtype=np.float64).copy()
    rot = np.asarray(data.cam_xmat[cid], dtype=np.float64).reshape(3, 3).copy()
    return CameraExtrinsics(name=name, pos_world=pos, rot_world=rot)


def camera_view_direction(data: mujoco.MjData, model: mujoco.MjModel, name: str) -> np.ndarray:
    ext = camera_extrinsics(model, data, name)
    return -ext.rot_world[:, 2]


class MujocoCameraRig:
    """离屏渲染 RGB / 深度（米）。"""

    def __init__(
        self,
        model: mujoco.MjModel,
        width: int = CAM_WIDTH,
        height: int = CAM_HEIGHT,
    ) -> None:
        self.model = model
        self.width = int(width)
        self.height = int(height)
        self._renderer = mujoco.Renderer(model, height=self.height, width=self.width)

    def close(self) -> None:
        self._renderer.close()

    def capture_rgb(self, data: mujoco.MjData, cam_name: str) -> np.ndarray:
        cid = camera_id(self.model, cam_name)
        self._renderer.disable_depth_rendering()
        self._renderer.update_scene(data, camera=cid)
        rgb = self._renderer.render()
        return np.asarray(rgb, dtype=np.uint8)

    def capture_depth_m(self, data: mujoco.MjData, cam_name: str) -> np.ndarray:
        cid = camera_id(self.model, cam_name)
        self._renderer.enable_depth_rendering()
        self._renderer.update_scene(data, camera=cid)
        depth = self._renderer.render()
        self._renderer.disable_depth_rendering()
        return np.asarray(depth, dtype=np.float64)

    def capture_segmentation(self, data: mujoco.MjData, cam_name: str) -> np.ndarray:
        cid = camera_id(self.model, cam_name)
        self._renderer.disable_depth_rendering()
        self._renderer.enable_segmentation_rendering()
        self._renderer.update_scene(data, camera=cid)
        seg = self._renderer.render()
        self._renderer.disable_segmentation_rendering()
        return np.asarray(seg, dtype=np.int32)

    def capture(
        self,
        data: mujoco.MjData,
        cam_name: str,
        *,
        with_depth: bool = False,
    ) -> CameraFrame:
        rgb = self.capture_rgb(data, cam_name)
        depth_m = self.capture_depth_m(data, cam_name) if with_depth else None
        return CameraFrame(rgb=rgb, depth_m=depth_m)


def depth_to_vis(depth_m: np.ndarray) -> np.ndarray:
    """深度可视化：近处亮、远处暗（uint8）。"""
    d = np.asarray(depth_m, dtype=np.float64)
    valid = np.isfinite(d) & (d > 1e-4)
    if not np.any(valid):
        return np.zeros(d.shape, dtype=np.uint8)
    dmin = float(np.percentile(d[valid], 5))
    dmax = float(np.percentile(d[valid], 95))
    span = max(dmax - dmin, 1e-3)
    vis = np.clip((d - dmin) / span, 0.0, 1.0)
    vis = (255.0 * (1.0 - vis)).astype(np.uint8)
    vis[~valid] = 0
    return vis


DEFAULT_CAMERAS: tuple[str, ...] = (SCENE_DEPTH_CAM, WRIST_RGB_CAM)


def _save_rgb_png(path, rgb: np.ndarray) -> None:
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
        from PIL import Image

        Image.fromarray(arr).save(path)
    except Exception as exc:
        raise RuntimeError(f"cannot save {path}") from exc


def _try_open_image(path) -> None:
    """有 DISPLAY 时用系统图片查看器打开（仅 save 模式首次调用）。"""
    import os
    import shutil
    import subprocess
    from pathlib import Path

    if not os.environ.get("DISPLAY"):
        return
    p = Path(path)
    if not p.is_file():
        return
    for cmd in (["xdg-open", str(p)], ["eog", str(p)], ["gio", "open", str(p)]):
        if shutil.which(cmd[0]):
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return


class LiveCameraPreview:
    """实时相机预览：优先 OpenCV 窗口，失败则 matplotlib，再不行写 PNG。"""

    def __init__(
        self,
        model: mujoco.MjModel,
        *,
        show_depth: bool = False,
        backend: str = "auto",
        save_dir: str | None = None,
    ) -> None:
        self._rig = MujocoCameraRig(model)
        self._show_depth = bool(show_depth)
        self._backend = str(backend)
        self._save_dir = None
        self._cv2 = None
        self._plt = None
        self._fig = None
        self._axes: list = []
        self._save_notified = False
        self._opened_viewer = False
        self._resolve_backend(save_dir)

    @property
    def backend_name(self) -> str:
        return self._backend

    def _resolve_backend(self, save_dir: str | None) -> None:
        want = self._backend
        if want == "auto":
            for candidate in ("cv2", "mpl", "save"):
                try:
                    self._backend = candidate
                    self._setup(candidate, save_dir)
                    print(f"[camera] 预览后端：{candidate}")
                    return
                except Exception:
                    continue
            raise RuntimeError("无可用相机预览后端（cv2/mpl/save 均失败）")
        try:
            self._setup(want, save_dir)
            print(f"[camera] 预览后端：{want}")
        except Exception as exc:
            import sys

            print(
                f"[WARN] 相机预览 {want} 不可用（{exc}），改用 save 写 PNG",
                file=sys.stderr,
            )
            self._backend = "save"
            self._setup("save", save_dir)
            print("[camera] 预览后端：save")

    def _setup(self, backend: str, save_dir: str | None) -> None:
        if backend == "cv2":
            import cv2

        cv2.namedWindow("scene_depth", cv2.WINDOW_NORMAL)
        cv2.namedWindow("wrist_rgb", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("scene_depth", 640, 480)
        cv2.resizeWindow("wrist_rgb", 640, 480)
        if self._show_depth:
            cv2.namedWindow("scene_depth_depth", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("scene_depth_depth", 640, 480)
            self._cv2 = cv2
            return
        if backend == "mpl":
            import matplotlib

            last_err: Exception | None = None
            for name in ("TkAgg", "Qt5Agg", "GTK3Agg"):
                try:
                    matplotlib.use(name, force=True)
                    import matplotlib.pyplot as plt

                    n = 3 if self._show_depth else 2
                    fig, axes = plt.subplots(1, n, figsize=(4.2 * n, 4))
                    self._axes = list(axes) if n > 1 else [axes]
                    titles = ["scene_depth", "wrist_rgb"]
                    if self._show_depth:
                        titles.append("scene_depth (depth)")
                    for ax, title in zip(self._axes, titles):
                        ax.set_title(title, fontsize=10)
                        ax.axis("off")
                    plt.ion()
                    fig.tight_layout()
                    fig.canvas.manager.set_window_title("MuJoCo cameras")
                    fig.show()
                    self._plt = plt
                    self._fig = fig
                    return
                except Exception as exc:
                    last_err = exc
            raise RuntimeError(f"matplotlib 预览不可用: {last_err}") from last_err
        if backend == "save":
            from pathlib import Path

            self._save_dir = Path(save_dir or "logs/vision_preview").expanduser().resolve()
            self._save_dir.mkdir(parents=True, exist_ok=True)
            return
        raise ValueError(f"unknown camera preview backend: {backend}")

    def update(self, data: mujoco.MjData) -> None:
        scene_rgb = self._rig.capture_rgb(data, SCENE_DEPTH_CAM)
        wrist_rgb = self._rig.capture_rgb(data, WRIST_RGB_CAM)
        depth_vis = None
        if self._show_depth:
            depth_vis = depth_to_vis(self._rig.capture_depth_m(data, SCENE_DEPTH_CAM))

        if self._cv2 is not None:
            cv2 = self._cv2
        cv2.imshow("scene_depth", cv2.cvtColor(scene_rgb, cv2.COLOR_RGB2BGR))
        cv2.imshow("wrist_rgb", cv2.cvtColor(wrist_rgb, cv2.COLOR_RGB2BGR))
        if depth_vis is not None:
            cv2.imshow("scene_depth_depth", depth_vis)
            cv2.waitKey(1)
            return

        if self._plt is not None:
            imgs = [scene_rgb, wrist_rgb]
            if depth_vis is not None:
                imgs.append(np.stack([depth_vis] * 3, axis=-1))
            for ax, img in zip(self._axes, imgs):
                ax.imshow(img)
            self._fig.canvas.draw_idle()
            self._fig.canvas.flush_events()
            self._plt.pause(0.001)
            return

        assert self._save_dir is not None
        scene_path = self._save_dir / "live_scene.png"
        wrist_path = self._save_dir / "live_wrist.png"
        dual_path = self._save_dir / "live_dual.png"
        _save_rgb_png(scene_path, scene_rgb)
        _save_rgb_png(wrist_path, wrist_rgb)
        _save_rgb_png(dual_path, np.concatenate([scene_rgb, wrist_rgb], axis=1))
        if depth_vis is not None:
            _save_rgb_png(
                self._save_dir / "live_scene_depth.png",
                np.stack([depth_vis] * 3, axis=-1),
            )
        if not self._opened_viewer:
            _try_open_image(dual_path)
            self._opened_viewer = True
        if not self._save_notified:
            print(
                f"[camera] 实时画面 → {self._save_dir}/live_dual.png "
                f"（固定|腕部 左右拼接，播放时自动刷新）"
            )
            self._save_notified = True

    def close(self) -> None:
        try:
            self._rig.close()
        finally:
            if self._cv2 is not None:
                self._cv2.destroyAllWindows()
            if self._plt is not None and self._fig is not None:
                self._plt.close(self._fig)
