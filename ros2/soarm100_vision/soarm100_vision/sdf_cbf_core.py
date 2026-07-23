from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class WorkspaceCrop:
    x_min: float = -0.30
    x_max: float = 0.30
    y_min: float = -0.30
    y_max: float = 0.30
    z_min: float = 0.05
    z_max: float = 1.20

    def apply(self, points: np.ndarray) -> np.ndarray:
        pts = _points(points)
        if pts.shape[0] == 0:
            return pts
        keep = (
            (pts[:, 0] >= self.x_min)
            & (pts[:, 0] <= self.x_max)
            & (pts[:, 1] >= self.y_min)
            & (pts[:, 1] <= self.y_max)
            & (pts[:, 2] >= self.z_min)
            & (pts[:, 2] <= self.z_max)
        )
        return pts[keep]


@dataclass
class TableFilter:
    enabled: bool = True
    z_max: float = 0.055

    def apply(self, points: np.ndarray) -> tuple[np.ndarray, int]:
        pts = _points(points)
        if not self.enabled or pts.shape[0] == 0:
            return pts, 0
        keep = pts[:, 2] > float(self.z_max)
        return pts[keep], int(np.count_nonzero(~keep))


@dataclass
class VoxelRecord:
    point: np.ndarray
    hits: int
    last_frame: int


@dataclass
class VoxelPersistence:
    voxel_size: float = 0.012
    min_hits: int = 2
    forget_frames: int = 4
    frame: int = 0
    records: dict[tuple[int, int, int], VoxelRecord] = field(default_factory=dict)

    def update(self, points: np.ndarray) -> np.ndarray:
        self.frame += 1
        pts = _points(points)
        if pts.shape[0] > 0:
            unique: dict[tuple[int, int, int], list[np.ndarray]] = {}
            inv = 1.0 / max(float(self.voxel_size), 1e-6)
            for pt in pts:
                key = tuple(np.floor(pt * inv).astype(np.int64).tolist())
                unique.setdefault(key, []).append(pt)
            for key, vals in unique.items():
                point = np.mean(np.asarray(vals, dtype=np.float64), axis=0)
                rec = self.records.get(key)
                if rec is None:
                    self.records[key] = VoxelRecord(point=point, hits=1, last_frame=self.frame)
                else:
                    rec.point = 0.6 * rec.point + 0.4 * point
                    rec.hits += 1
                    rec.last_frame = self.frame

        stale = [k for k, v in self.records.items() if self.frame - v.last_frame > int(self.forget_frames)]
        for key in stale:
            self.records.pop(key, None)

        out = [v.point for v in self.records.values() if v.hits >= int(self.min_hits)]
        if not out:
            return np.zeros((0, 3), dtype=np.float32)
        return np.asarray(out, dtype=np.float32).reshape(-1, 3)

    def reset(self) -> None:
        self.frame = 0
        self.records.clear()


@dataclass
class SdfCloudState:
    points: np.ndarray = field(default_factory=lambda: np.zeros((0, 3), dtype=np.float32))
    frame_id: str = ""
    stamp_s: float = 0.0
    inflate_m: float = 0.015
    min_points: int = 30

    @property
    def detected(self) -> bool:
        return int(self.points.shape[0]) >= int(self.min_points)

    def status_text(self) -> str:
        n = int(self.points.shape[0])
        if n == 0:
            return "detected=false points=0"
        pts = _points(self.points)
        mn = pts.min(axis=0)
        mx = pts.max(axis=0)
        centroid = pts.mean(axis=0)
        return (
            f"detected={self.detected} points={n} frame={self.frame_id} "
            f"centroid=({centroid[0]:+.3f},{centroid[1]:+.3f},{centroid[2]:+.3f}) "
            f"bbox_min=({mn[0]:+.3f},{mn[1]:+.3f},{mn[2]:+.3f}) "
            f"bbox_max=({mx[0]:+.3f},{mx[1]:+.3f},{mx[2]:+.3f}) "
            f"inflate={float(self.inflate_m):.3f}"
        )


def _points(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return np.zeros((0, 3), dtype=np.float64)
    return pts[np.all(np.isfinite(pts), axis=1)]


def filter_robot_mask(points: np.ndarray, robot_mask_flat: np.ndarray | None) -> tuple[np.ndarray, int]:
    pts = _points(points)
    if robot_mask_flat is None or pts.shape[0] == 0:
        return pts, 0
    mask = np.asarray(robot_mask_flat, dtype=bool).reshape(-1)
    n = min(mask.shape[0], pts.shape[0])
    keep = np.ones(pts.shape[0], dtype=bool)
    keep[:n] = ~mask[:n]
    return pts[keep], int(np.count_nonzero(~keep))
