"""Smoke test for point-cloud SDF obstacle queries."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from cbf import PointCloudSdfObstacle, pointcloud_sdf_h_and_grad_p  # type: ignore
    from obstacle_source import _points_near_segment  # type: ignore
else:
    from .cbf import PointCloudSdfObstacle, pointcloud_sdf_h_and_grad_p
    from .obstacle_source import _points_near_segment


def main() -> int:
    yy, zz = np.meshgrid(
        np.linspace(-0.05, 0.05, 9),
        np.linspace(0.0, 0.10, 9),
        indexing="ij",
    )
    pts = np.stack([np.zeros_like(yy), yy, zz], axis=-1).reshape(-1, 3)
    obs = PointCloudSdfObstacle(
        name="plane_patch",
        points=pts,
        truncation_distance=0.20,
        voxel_size=0.0,
        inflate=0.0,
    )

    h, grad = pointcloud_sdf_h_and_grad_p(
        np.array([0.07, 0.0, 0.05], dtype=np.float64),
        obs,
        d_safe=0.02,
        r_link=0.01,
    )
    assert abs(h - 0.04) < 1e-9, (h, grad)
    assert np.allclose(grad, np.array([1.0, 0.0, 0.0]), atol=1e-9), grad

    h2, grad2 = pointcloud_sdf_h_and_grad_p(
        np.array([-0.03, 0.0, 0.05], dtype=np.float64),
        obs,
        d_safe=0.02,
        r_link=0.01,
    )
    assert abs(h2 - 0.0) < 1e-9, (h2, grad2)
    assert np.allclose(grad2, np.array([-1.0, 0.0, 0.0]), atol=1e-9), grad2

    pts_self = np.array([[0.05, 0.005, 0.0], [0.07, -0.006, 0.0]], dtype=np.float64)
    pts_obs = np.array([[0.05, 0.06, 0.0], [0.07, 0.07, 0.0]], dtype=np.float64)
    pts_all = np.vstack([pts_self, pts_obs])
    near = _points_near_segment(
        pts_all,
        np.array([0.0, 0.0, 0.0], dtype=np.float64),
        np.array([0.10, 0.0, 0.0], dtype=np.float64),
        0.02,
    )
    assert np.array_equal(near, np.array([True, True, False, False])), near

    print("sdf smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
