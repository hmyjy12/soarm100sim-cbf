from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


DEFAULT_SELF_FILTER_CAPSULES: tuple[tuple[str, str, float], ...] = (
    ("base", "shoulder_rotation", 0.035),
    ("shoulder_rotation", "shoulder_pitch", 0.035),
    ("shoulder_pitch", "ellbow", 0.038),
    ("ellbow", "wrist_pitch", 0.040),
    ("wrist_pitch", "wrist_jaw", 0.035),
    ("wrist_jaw", "wrist_roll", 0.032),
    ("wrist_roll", "gripper", 0.030),
)


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
class AttachedThinFilterConfig:
    voxel_size_m: float = 0.010
    connectivity_m: float = 0.018
    min_points: int = 5
    min_length_m: float = 0.060
    max_width_m: float = 0.022
    min_aspect_ratio: float = 4.0
    attachment_distance_m: float = 0.025
    max_robot_distance_m: float = 0.100
    min_near_robot_fraction: float = 0.80


@dataclass
class AttachedThinFilterResult:
    kept_points: np.ndarray
    removed_points: np.ndarray
    components_checked: int = 0
    components_removed: int = 0


class AttachedThinComponentFilter:
    """Remove thin connected components attached to wrist-link surfaces."""

    def __init__(self, config: AttachedThinFilterConfig | None = None) -> None:
        self.config = config or AttachedThinFilterConfig()

    def apply(
        self,
        points: np.ndarray,
        wrist_capsules: list[tuple[np.ndarray, np.ndarray, float]],
    ) -> AttachedThinFilterResult:
        pts = _points(points)
        if pts.shape[0] == 0 or not wrist_capsules:
            return AttachedThinFilterResult(pts, np.zeros((0, 3), dtype=np.float64))

        components = _voxel_components(
            pts,
            voxel_size_m=self.config.voxel_size_m,
            connectivity_m=self.config.connectivity_m,
        )
        remove = np.zeros(pts.shape[0], dtype=bool)
        removed_components = 0
        for indices in components:
            component = pts[indices]
            if component.shape[0] < int(self.config.min_points):
                continue
            length, width = _component_dimensions(component)
            aspect = length / max(width, 1.0e-6)
            if (
                length < float(self.config.min_length_m)
                or width > float(self.config.max_width_m)
                or aspect < float(self.config.min_aspect_ratio)
            ):
                continue
            surface_distance = _distance_to_capsule_surfaces(component, wrist_capsules)
            attached = float(np.min(surface_distance)) <= float(
                self.config.attachment_distance_m
            )
            near_fraction = float(
                np.mean(surface_distance <= float(self.config.max_robot_distance_m))
            )
            if attached and near_fraction >= float(self.config.min_near_robot_fraction):
                remove[indices] = True
                removed_components += 1

        return AttachedThinFilterResult(
            kept_points=pts[~remove],
            removed_points=pts[remove],
            components_checked=len(components),
            components_removed=removed_components,
        )


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


def nearest_joint_sample(
    samples: list[tuple[float, np.ndarray]],
    stamp_s: float,
    max_delta_s: float,
) -> tuple[np.ndarray | None, float]:
    """Return the joint sample nearest a sensor timestamp."""
    if not samples or not np.isfinite(stamp_s):
        return None, float("inf")
    best_stamp, best_q = min(samples, key=lambda item: abs(float(item[0]) - stamp_s))
    delta = abs(float(best_stamp) - float(stamp_s))
    if delta > float(max_delta_s):
        return None, delta
    q = np.asarray(best_q, dtype=np.float64).reshape(-1)
    if q.size == 0 or not np.all(np.isfinite(q)):
        return None, delta
    return q.copy(), delta


def points_near_segment(
    points: np.ndarray,
    start: np.ndarray,
    end: np.ndarray,
    radius_m: float,
) -> np.ndarray:
    pts = _points(points)
    if pts.shape[0] == 0:
        return np.zeros(0, dtype=bool)
    a = np.asarray(start, dtype=np.float64).reshape(3)
    b = np.asarray(end, dtype=np.float64).reshape(3)
    ab = b - a
    denom = float(ab @ ab)
    if denom < 1.0e-12:
        distance = np.linalg.norm(pts - a.reshape(1, 3), axis=1)
    else:
        t = np.clip(((pts - a.reshape(1, 3)) @ ab) / denom, 0.0, 1.0)
        closest = a.reshape(1, 3) + t.reshape(-1, 1) * ab.reshape(1, 3)
        distance = np.linalg.norm(pts - closest, axis=1)
    return distance <= max(float(radius_m), 0.0)


def _distance_to_segment(
    points: np.ndarray, start: np.ndarray, end: np.ndarray
) -> np.ndarray:
    pts = _points(points)
    a = np.asarray(start, dtype=np.float64).reshape(3)
    b = np.asarray(end, dtype=np.float64).reshape(3)
    ab = b - a
    denom = float(ab @ ab)
    if denom < 1.0e-12:
        return np.linalg.norm(pts - a.reshape(1, 3), axis=1)
    t = np.clip(((pts - a.reshape(1, 3)) @ ab) / denom, 0.0, 1.0)
    closest = a.reshape(1, 3) + t.reshape(-1, 1) * ab.reshape(1, 3)
    return np.linalg.norm(pts - closest, axis=1)


def _distance_to_capsule_surfaces(
    points: np.ndarray,
    capsules: list[tuple[np.ndarray, np.ndarray, float]],
) -> np.ndarray:
    pts = _points(points)
    distances = np.full(pts.shape[0], np.inf, dtype=np.float64)
    for start, end, radius in capsules:
        surface = np.maximum(_distance_to_segment(pts, start, end) - float(radius), 0.0)
        distances = np.minimum(distances, surface)
    return distances


def _component_dimensions(points: np.ndarray) -> tuple[float, float]:
    pts = _points(points)
    if pts.shape[0] < 2:
        return 0.0, 0.0
    centered = pts - pts.mean(axis=0, keepdims=True)
    _, _, axes = np.linalg.svd(centered, full_matrices=False)
    projected = centered @ axes.T
    extents = np.ptp(projected, axis=0)
    extents = np.pad(extents, (0, max(0, 3 - extents.size)))[:3]
    extents = np.sort(extents)[::-1]
    return float(extents[0]), float(max(extents[1], extents[2]))


def _voxel_components(
    points: np.ndarray, voxel_size_m: float, connectivity_m: float
) -> list[np.ndarray]:
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree

    pts = _points(points)
    if pts.shape[0] == 0:
        return []
    voxel = max(float(voxel_size_m), 1.0e-6)
    keys = np.floor(pts / voxel).astype(np.int64)
    _, inverse, counts = np.unique(keys, axis=0, return_inverse=True, return_counts=True)
    cell_count = int(counts.shape[0])
    centers = np.column_stack(
        [np.bincount(inverse, weights=pts[:, axis], minlength=cell_count) for axis in range(3)]
    ) / counts.reshape(-1, 1)
    pairs = cKDTree(centers).query_pairs(
        r=max(float(connectivity_m), voxel), output_type="ndarray"
    )
    if pairs.shape[0] == 0:
        labels = np.arange(cell_count, dtype=np.int64)
    else:
        rows = np.concatenate((pairs[:, 0], pairs[:, 1]))
        cols = np.concatenate((pairs[:, 1], pairs[:, 0]))
        graph = coo_matrix(
            (np.ones(rows.shape[0], dtype=np.uint8), (rows, cols)),
            shape=(cell_count, cell_count),
        ).tocsr()
        _, labels = connected_components(graph, directed=False, return_labels=True)
    point_labels = labels[inverse]
    order = np.argsort(point_labels, kind="stable")
    boundaries = np.flatnonzero(np.diff(point_labels[order])) + 1
    return [group for group in np.split(order, boundaries) if group.size > 0]


def filter_capsule_self_points(
    points: np.ndarray,
    capsules: list[tuple[np.ndarray, np.ndarray, float]],
    margin_m: float,
) -> tuple[np.ndarray, int]:
    """Remove points inside current robot link capsules plus a small margin."""
    pts = _points(points)
    if pts.shape[0] == 0 or not capsules:
        return pts, 0
    remove = np.zeros(pts.shape[0], dtype=bool)
    margin = max(float(margin_m), 0.0)
    for start, end, radius in capsules:
        remove |= points_near_segment(pts, start, end, float(radius) + margin)
    return pts[~remove], int(np.count_nonzero(remove))


def filter_oriented_box_self_points(
    points: np.ndarray,
    center_world: np.ndarray,
    rotation_world_from_local: np.ndarray,
    half_size_m: np.ndarray,
    margin_m: float = 0.0,
) -> tuple[np.ndarray, int]:
    """Remove points inside a link-attached oriented box."""
    pts = _points(points)
    if pts.shape[0] == 0:
        return pts, 0
    center = np.asarray(center_world, dtype=np.float64).reshape(3)
    rotation = np.asarray(rotation_world_from_local, dtype=np.float64).reshape(3, 3)
    half_size = np.maximum(
        np.asarray(half_size_m, dtype=np.float64).reshape(3) + max(float(margin_m), 0.0),
        0.0,
    )
    local = (pts - center.reshape(1, 3)) @ rotation
    remove = np.all(np.abs(local) <= half_size.reshape(1, 3), axis=1)
    return pts[~remove], int(np.count_nonzero(remove))


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
