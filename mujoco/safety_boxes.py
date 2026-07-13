"""Point-cloud obstacle approximation with multiple axis-aligned safety boxes."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np

try:
    from .cbf import AxisAlignedBoxObstacle
    from .constants import OBSTACLE_ROD_CENTER_POS_M
except ImportError:
    from cbf import AxisAlignedBoxObstacle  # type: ignore
    from constants import OBSTACLE_ROD_CENTER_POS_M  # type: ignore


@dataclass
class PointCloudBoxConfig:
    voxel_size_m: float = 0.02
    min_points_per_voxel: int = 2
    min_component_points: int = 12
    use_pca_inlier_filter: bool = True
    inlier_dist_m: float = 0.014
    slice_length_m: float = 0.035
    min_slice_radius_m: float = 0.007
    max_slice_radius_m: float = 0.012
    inflate_m: float = 0.0
    min_half_extent_m: float = 0.006
    max_boxes: int = 96
    mode: str = "pca_slices"
    roi_x: tuple[float, float] = (0.02, 0.34)
    roi_y: tuple[float, float] = (-0.04, 0.24)
    roi_z: tuple[float, float] = (0.03, 0.36)
    use_prior_xy: bool = True
    prior_xy: tuple[float, float] = (
        float(OBSTACLE_ROD_CENTER_POS_M[0]),
        float(OBSTACLE_ROD_CENTER_POS_M[1]),
    )
    prior_xy_radius_m: float = 0.045
    name_prefix: str = "pc_box"


@dataclass
class PointCloudBoxDebug:
    n_input: int = 0
    n_roi: int = 0
    n_voxels: int = 0
    n_components: int = 0
    n_boxes: int = 0


def filter_roi(points: np.ndarray, cfg: PointCloudBoxConfig) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if pts.shape[0] == 0:
        return pts
    finite = np.all(np.isfinite(pts), axis=1)
    x0, x1 = cfg.roi_x
    y0, y1 = cfg.roi_y
    z0, z1 = cfg.roi_z
    keep = (
        finite
        & (pts[:, 0] >= x0)
        & (pts[:, 0] <= x1)
        & (pts[:, 1] >= y0)
        & (pts[:, 1] <= y1)
        & (pts[:, 2] >= z0)
        & (pts[:, 2] <= z1)
    )
    pts_roi = pts[keep]
    if pts_roi.shape[0] == 0 or not cfg.use_prior_xy:
        return pts_roi
    prior = np.asarray(cfg.prior_xy, dtype=np.float64).reshape(1, 2)
    dxy = np.linalg.norm(pts_roi[:, :2] - prior, axis=1)
    return pts_roi[dxy <= float(cfg.prior_xy_radius_m)]


def _occupied_voxels(points: np.ndarray, cfg: PointCloudBoxConfig) -> dict[tuple[int, int, int], np.ndarray]:
    if points.shape[0] == 0:
        return {}
    v = max(float(cfg.voxel_size_m), 1e-6)
    keys = np.floor(points / v).astype(np.int64)
    buckets: dict[tuple[int, int, int], list[int]] = {}
    for i, key in enumerate(keys):
        buckets.setdefault((int(key[0]), int(key[1]), int(key[2])), []).append(i)
    min_pts = max(1, int(cfg.min_points_per_voxel))
    return {
        key: np.asarray(idx, dtype=np.int64)
        for key, idx in buckets.items()
        if len(idx) >= min_pts
    }


def _refine_pca_inliers(points: np.ndarray, cfg: PointCloudBoxConfig) -> np.ndarray:
    if not cfg.use_pca_inlier_filter or points.shape[0] < int(cfg.min_component_points):
        return points
    center = points.mean(axis=0)
    centered = points - center
    cov = (centered.T @ centered) / max(points.shape[0], 1)
    _, eigvecs = np.linalg.eigh(cov)
    axis = eigvecs[:, 2]
    axis /= max(float(np.linalg.norm(axis)), 1e-12)
    dist = np.linalg.norm(np.cross(axis.reshape(1, 3), centered), axis=1)
    keep = dist <= float(cfg.inlier_dist_m)
    if int(keep.sum()) >= int(cfg.min_component_points):
        return points[keep]
    return points


def _pca_axis(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    center = points.mean(axis=0)
    centered = points - center
    cov = (centered.T @ centered) / max(points.shape[0], 1)
    _, eigvecs = np.linalg.eigh(cov)
    axis = eigvecs[:, 2]
    axis /= max(float(np.linalg.norm(axis)), 1e-12)
    if axis[2] < 0.0:
        axis = -axis
    return center, axis


def _boxes_from_pca_slices(
    points: np.ndarray,
    cfg: PointCloudBoxConfig,
) -> list[AxisAlignedBoxObstacle]:
    if points.shape[0] < int(cfg.min_component_points):
        return []
    center, axis = _pca_axis(points)
    rel = points - center
    proj = rel @ axis
    t_min = float(proj.min())
    t_max = float(proj.max())
    span = max(t_max - t_min, float(cfg.slice_length_m))
    n = max(1, min(int(np.ceil(span / max(float(cfg.slice_length_m), 1e-6))), int(cfg.max_boxes)))
    edges = np.linspace(t_min, t_max, n + 1, dtype=np.float64)
    radial = np.linalg.norm(np.cross(axis.reshape(1, 3), rel), axis=1)
    base_radius = float(np.percentile(radial, 85.0)) if radial.shape[0] else float(cfg.min_slice_radius_m)
    radius = float(np.clip(base_radius + float(cfg.inflate_m), cfg.min_slice_radius_m, cfg.max_slice_radius_m))

    boxes: list[AxisAlignedBoxObstacle] = []
    radial_half = radius * np.sqrt(np.maximum(1.0 - axis * axis, 0.0))
    for i in range(n):
        mask = (proj >= edges[i]) & (proj <= edges[i + 1])
        if int(mask.sum()) < max(1, int(cfg.min_points_per_voxel)):
            continue
        t0 = float(edges[i])
        t1 = float(edges[i + 1])
        t_mid = 0.5 * (t0 + t1)
        half_len = max(0.5 * (t1 - t0), float(cfg.min_half_extent_m))
        box_center = center + axis * t_mid
        half = np.maximum(np.abs(axis) * half_len + radial_half, float(cfg.min_half_extent_m))
        boxes.append(
            AxisAlignedBoxObstacle(
                name=f"{cfg.name_prefix}_{len(boxes):02d}",
                center=box_center.astype(np.float64),
                half_extents=half.astype(np.float64),
            )
        )
    return boxes


def boxes_from_cylinder_slices(
    name_prefix: str,
    center: np.ndarray,
    axis: np.ndarray,
    radius: float,
    half_length: float,
    *,
    slice_length_m: float = 0.035,
    max_boxes: int = 32,
) -> list[AxisAlignedBoxObstacle]:
    axis = np.asarray(axis, dtype=np.float64).reshape(3)
    axis /= max(float(np.linalg.norm(axis)), 1e-12)
    center = np.asarray(center, dtype=np.float64).reshape(3)
    length = max(2.0 * float(half_length), float(slice_length_m))
    n = max(1, min(int(np.ceil(length / max(float(slice_length_m), 1e-6))), int(max_boxes)))
    edges = np.linspace(-float(half_length), float(half_length), n + 1, dtype=np.float64)
    radial_half = float(radius) * np.sqrt(np.maximum(1.0 - axis * axis, 0.0))
    boxes: list[AxisAlignedBoxObstacle] = []
    for i in range(n):
        t0 = float(edges[i])
        t1 = float(edges[i + 1])
        t_mid = 0.5 * (t0 + t1)
        half_len = max(0.5 * (t1 - t0), 1e-6)
        half = np.maximum(np.abs(axis) * half_len + radial_half, 1e-6)
        boxes.append(
            AxisAlignedBoxObstacle(
                name=f"{name_prefix}_{i:02d}",
                center=(center + axis * t_mid).astype(np.float64),
                half_extents=half.astype(np.float64),
            )
        )
    return boxes


def _connected_components(voxels: set[tuple[int, int, int]]) -> list[list[tuple[int, int, int]]]:
    components: list[list[tuple[int, int, int]]] = []
    remaining = set(voxels)
    neighbors = (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )
    while remaining:
        seed = remaining.pop()
        comp = [seed]
        q: deque[tuple[int, int, int]] = deque([seed])
        while q:
            x, y, z = q.popleft()
            for dx, dy, dz in neighbors:
                nb = (x + dx, y + dy, z + dz)
                if nb in remaining:
                    remaining.remove(nb)
                    comp.append(nb)
                    q.append(nb)
        components.append(comp)
    return components


def boxes_from_point_cloud(
    points: np.ndarray,
    cfg: PointCloudBoxConfig | None = None,
) -> tuple[list[AxisAlignedBoxObstacle], PointCloudBoxDebug]:
    """Convert a segmented point cloud into inflated AABBs.

    Default ``mode="voxels"`` keeps occupied voxels as separate small boxes. This
    preserves free space between visible surface patches better than a single
    component bounding box.
    """
    cfg = cfg or PointCloudBoxConfig()
    pts_all = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    pts = filter_roi(pts_all, cfg)
    pts = _refine_pca_inliers(pts, cfg)
    mode = str(cfg.mode).lower().strip()

    if mode in ("pca_slice", "pca_slices", "slices"):
        boxes = _boxes_from_pca_slices(pts, cfg)
        debug = PointCloudBoxDebug(
            n_input=int(pts_all.shape[0]),
            n_roi=int(pts.shape[0]),
            n_voxels=0,
            n_components=1 if boxes else 0,
            n_boxes=int(len(boxes)),
        )
        return boxes, debug

    voxel_to_indices = _occupied_voxels(pts, cfg)
    components = _connected_components(set(voxel_to_indices))

    if mode in ("voxel", "voxels", "occupied"):
        v = max(float(cfg.voxel_size_m), 1e-6)
        half = np.full(3, max(0.5 * v + float(cfg.inflate_m), float(cfg.min_half_extent_m)))
        ranked = sorted(
            voxel_to_indices.items(),
            key=lambda item: len(item[1]),
            reverse=True,
        )
        boxes = []
        for i, (key, _indices) in enumerate(ranked[: max(0, int(cfg.max_boxes))]):
            center = (np.asarray(key, dtype=np.float64) + 0.5) * v
            boxes.append(
                AxisAlignedBoxObstacle(
                    name=f"{cfg.name_prefix}_{i:02d}",
                    center=center,
                    half_extents=half.copy(),
                )
            )
        debug = PointCloudBoxDebug(
            n_input=int(pts_all.shape[0]),
            n_roi=int(pts.shape[0]),
            n_voxels=int(len(voxel_to_indices)),
            n_components=int(len(components)),
            n_boxes=int(len(boxes)),
        )
        return boxes, debug

    candidates: list[tuple[int, AxisAlignedBoxObstacle]] = []
    min_comp = max(1, int(cfg.min_component_points))
    inflate = max(float(cfg.inflate_m), 0.0)
    min_half = max(float(cfg.min_half_extent_m), 1e-6)

    for comp_idx, comp in enumerate(components):
        indices = np.concatenate([voxel_to_indices[v] for v in comp])
        if indices.shape[0] < min_comp:
            continue
        comp_pts = pts[indices]
        p_min = comp_pts.min(axis=0) - inflate
        p_max = comp_pts.max(axis=0) + inflate
        center = 0.5 * (p_min + p_max)
        half = np.maximum(0.5 * (p_max - p_min), min_half)
        obs = AxisAlignedBoxObstacle(
            name=f"{cfg.name_prefix}_{comp_idx:02d}",
            center=center.astype(np.float64),
            half_extents=half.astype(np.float64),
        )
        candidates.append((int(indices.shape[0]), obs))

    candidates.sort(key=lambda item: item[0], reverse=True)
    boxes = [obs for _, obs in candidates[: max(0, int(cfg.max_boxes))]]
    debug = PointCloudBoxDebug(
        n_input=int(pts_all.shape[0]),
        n_roi=int(pts.shape[0]),
        n_voxels=int(len(voxel_to_indices)),
        n_components=int(len(components)),
        n_boxes=int(len(boxes)),
    )
    return boxes, debug
