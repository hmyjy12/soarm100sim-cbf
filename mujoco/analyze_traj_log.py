#!/usr/bin/env python3
"""Summarize mujoco/play.py --traj-log JSONL files."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def _rate(values: list[bool]) -> float:
    if not values:
        return float("nan")
    return float(np.mean(np.asarray(values, dtype=np.float64)))


def _mean(values: list[float]) -> float:
    vals = np.asarray(values, dtype=np.float64)
    vals = vals[np.isfinite(vals)]
    return float(np.mean(vals)) if vals.shape[0] else float("nan")


def _min(values: list[float]) -> float:
    vals = np.asarray(values, dtype=np.float64)
    vals = vals[np.isfinite(vals)]
    return float(np.min(vals)) if vals.shape[0] else float("nan")


def summarize(path: Path) -> None:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if not rows:
        print("empty log")
        return

    by_ep: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        by_ep[int(row["ep"])].append(row)

    print(f"log={path} rows={len(rows)} episodes={len(by_ep)}")
    print(
        "ep target steps best_dist_mm min_h_mm active% proj% "
        "mean|dq_cbf| max|dq_cbf| mean_ddq max_ddq "
        "mean_depth mean_robot_mask mean_ws mean_table_rm mean_self_rm mean_persist mean_mem mean_sdf"
    )
    for ep in sorted(by_ep):
        rs = by_ep[ep]
        target_idx = int(rs[0].get("target_idx", -1))
        dist = [float(r.get("dist_m", float("nan"))) for r in rs]
        h = [float(r.get("h_min_m", float("nan"))) for r in rs]
        dq_cbf = [float(r.get("dq_cbf_norm", 0.0)) for r in rs]
        ddq = [float(r.get("ddq_total_norm", 0.0)) for r in rs]
        depth = [float(r.get("depth_valid_points", 0.0)) for r in rs]
        robot_mask = [float(r.get("robot_masked_points", 0.0)) for r in rs]
        ws = [float(r.get("workspace_points", 0.0)) for r in rs]
        table_rm = [float(r.get("table_filtered_points", 0.0)) for r in rs]
        fused = [float(r.get("fused_points", 0.0)) for r in rs]
        mem = [float(r.get("voxel_memory", 0.0)) for r in rs]
        sdf = [float(r.get("sdf_points", 0.0)) for r in rs]
        self_rm = [float(r.get("self_filtered_points", 0.0)) for r in rs]
        active = [bool(r.get("cbf_active", False)) for r in rs]
        projected = [bool(r.get("cbf_projected", False)) for r in rs]
        print(
            f"{ep:03d} {target_idx:6d} {len(rs):5d} "
            f"{_min(dist)*1000.0:12.1f} {_min(h)*1000.0:8.1f} "
            f"{100.0*_rate(active):7.1f} {100.0*_rate(projected):6.1f} "
            f"{_mean(dq_cbf):12.4f} {max(dq_cbf) if dq_cbf else float('nan'):12.4f} "
            f"{_mean(ddq):8.4f} {max(ddq) if ddq else float('nan'):8.4f} "
            f"{_mean(depth):10.1f} {_mean(robot_mask):15.1f} {_mean(ws):7.1f} {_mean(table_rm):13.1f} "
            f"{_mean(self_rm):12.1f} {_mean(fused):12.1f} {_mean(mem):8.1f} {_mean(sdf):8.1f}"
        )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("log", type=str)
    args = p.parse_args()
    summarize(Path(args.log).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
