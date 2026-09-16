#!/usr/bin/env python3
"""Read-only cloud/FK inspector. No publishers, services or serial access.

Run from a ROS-sourced vision_seg environment. Every accepted snapshot stores
the original cloud and matching joints for offline replay with --snapshot.
"""
from __future__ import annotations

import argparse
from collections import deque
import json
import os
from pathlib import Path
import sys
import time

import numpy as np

REPO = Path(__file__).resolve().parents[3]
# Import the installed engine before exposing the repository's mujoco modules.
os.chdir(REPO / "ros2")
sys.path[:] = [p for p in sys.path if p and Path(p).resolve() != REPO]
import mujoco
sys.path.insert(0, str(REPO / "mujoco"))
sys.path.insert(0, str(REPO / "ros2/soarm100_vision"))
import cbf
import runtime

JOINT_NAMES = tuple(n + "_joint" for n in (
    "shoulder_rotation", "shoulder_pitch", "ellbow", "wrist_pitch",
    "wrist_jaw", "wrist_roll", "gripper"))


def stats(points):
    if not len(points):
        return {"points": 0}
    return dict(points=len(points), centroid_m=points.mean(0).tolist(),
                bbox_min_m=points.min(0).tolist(), bbox_max_m=points.max(0).tolist())


def evaluate(model, data, ids, points, q, safe, inflate):
    for adr, value in zip(ids.qpos_adr, q):
        data.qpos[adr] = value
    mujoco.mj_forward(model, data)
    obstacle = cbf.PointCloudSdfObstacle("diagnostic", points,
        truncation_distance=float("inf"), voxel_size=0.01, inflate=inflate)
    points = obstacle.points
    if not len(points):
        return {"valid": False, "reason": "empty_cloud"}
    records = []
    for mon in cbf.resolve_monitors(model, cbf.DEFAULT_MONITOR_SPECS,
                                    cbf.DEFAULT_CAPSULE_SPECS):
        if isinstance(mon, cbf.CapsuleMonitor):
            a, b = data.xpos[mon.body_a_id], data.xpos[mon.body_b_id]
            centers = np.linspace(a, b, cbf.CAPSULE_SEGMENT_SAMPLES)
        else:
            a = b = (runtime.tcp_pose_w(data, ids)[0] if mon.body_id is None
                     else data.xpos[mon.body_id])
            centers = np.asarray(a).reshape(1, 3)
        distances = np.linalg.norm(centers[:, None, :] - points[None, :, :], axis=2)
        i, j = np.unravel_index(np.argmin(distances), distances.shape)
        d = float(distances[i, j])
        h, _ = cbf.pointcloud_sdf_h_and_grad_p(centers[i], obstacle, safe, mon.r_link)
        # Exact continuous segment distance is a diagnostic for sampling error.
        ab = b - a
        t = np.clip((points - a) @ ab / max(float(ab @ ab), 1e-20), 0, 1)
        continuous = float(np.linalg.norm(points - (a + t[:, None] * ab), axis=1).min())
        records.append(dict(name=mon.name, a_base_m=a.tolist(), b_base_m=b.tolist(),
            radius_m=mon.r_link, sample_index=int(i), center_base_m=centers[i].tolist(),
            nearest_point_base_m=points[j].tolist(), center_distance_m=d,
            clearance_m=d-mon.r_link-inflate, h_m=float(h),
            legacy_h_m=0.15 if d >= 0.15 else float(h),
            legacy_truncated=d >= 0.15,
            continuous_clearance_m=continuous-mon.r_link-inflate))
    worst = min(records, key=lambda r: r["h_m"])
    return dict(valid=True, cloud=stats(points), q_rad=np.asarray(q).tolist(),
                d_safe_m=safe, inflate_m=inflate, worst=worst, monitors=records,
                legacy_h_min_m=min(r["legacy_h_m"] for r in records))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--output", type=Path,
                        default=REPO / "log/runtime/hardware/geometry_diagnostic")
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--mjcf", default="SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml")
    parser.add_argument("--safe-distance", type=float, default=0.03)
    parser.add_argument("--inflate", type=float, default=0.0)
    parser.add_argument("--joint-tolerance", type=float, default=0.075)
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    model = mujoco.MjModel.from_xml_path(str(REPO / args.mjcf))
    data = mujoco.MjData(model)
    ids = runtime.resolve_robot_ids(model)
    if args.snapshot:
        with np.load(args.snapshot) as s:
            report = evaluate(model, data, ids, s["points"], s["q"], args.safe_distance, args.inflate)
        print(json.dumps(report, indent=2))
        return

    import rclpy
    from rclpy.qos import qos_profile_sensor_data
    from sensor_msgs.msg import JointState, PointCloud2
    from std_msgs.msg import String
    from soarm100_vision.vision_utils import pointcloud2_to_xyz, stamp_s
    rclpy.init()
    node = rclpy.create_node("obstacle_geometry_readonly")
    joints = deque(maxlen=240)
    pending = deque(maxlen=1)
    count = 0
    last_output = 0.0
    report_file = (args.output / "geometry.jsonl").open("a")

    def emit(record):
        record["received_wall_s"] = time.time()
        report_file.write(json.dumps(record) + "\n")
        report_file.flush()

    def on_joint(msg):
        if tuple(msg.name) == JOINT_NAMES and len(msg.position) == 7:
            q = np.asarray(msg.position)
            if np.isfinite(q).all():
                joints.append((stamp_s(msg), q))

    def on_cloud(msg):
        if not pending:
            pending.append((time.monotonic(), msg))

    def process():
        nonlocal count, last_output
        if not pending or time.monotonic() - last_output < 0.5:
            return
        received, msg = pending[0]
        if time.monotonic() - received < 0.10:
            return  # Allow the joint sample after the cloud stamp to arrive.
        pending.clear()
        last_output = time.monotonic()
        stamp = stamp_s(msg)
        if msg.header.frame_id != "base" or not joints:
            emit(dict(valid=False, reason="wrong_frame_or_no_joints", frame=msg.header.frame_id))
            return
        jt, q = min(joints, key=lambda s: abs(s[0] - stamp))
        if abs(jt-stamp) > args.joint_tolerance:
            emit(dict(valid=False, reason="joint_sync_missing", nearest_dt_s=abs(jt-stamp)))
            return
        points = pointcloud2_to_xyz(msg)
        report = evaluate(model, data, ids, points, q, args.safe_distance, args.inflate)
        count += 1
        snapshot = args.output / f"snapshot_{time.time_ns()}.npz"
        np.savez_compressed(snapshot, points=points, q=q, cloud_stamp_s=stamp,
                            joint_stamp_s=jt)
        report.update(cloud_stamp_s=stamp, joint_stamp_s=jt, snapshot=str(snapshot),
                      mjcf=args.mjcf, joint_sync_dt_s=abs(jt-stamp))
        emit(report)
        if report["valid"]:
            w = report["worst"]
            print(f"n={len(points)} h={w['h_m']:.4f} clearance={w['clearance_m']:.4f} "
                  f"legacy_h={report['legacy_h_min_m']:.4f} worst={w['name']}", flush=True)

    subscriptions = [
        node.create_subscription(JointState, "/joint_states", on_joint, qos_profile_sensor_data),
        node.create_subscription(PointCloud2, "/obstacle/cloud", on_cloud, qos_profile_sensor_data),
        node.create_subscription(PointCloud2, "/obstacle/selected_cloud_camera",
            lambda m: emit(dict(kind="selected_camera_cloud", stamp_s=stamp_s(m),
                                frame=m.header.frame_id, **stats(pointcloud2_to_xyz(m)))),
            qos_profile_sensor_data),
        node.create_subscription(String, "/obstacle/status",
            lambda m: emit(dict(kind="cloud_status", status=m.data)), 10),
    ]
    timer = node.create_timer(0.05, process)
    deadline = time.monotonic() + args.seconds
    try:
        while rclpy.ok() and time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print(f"accepted_snapshots={count} output={args.output}", flush=True)
        report_file.close()
        node.destroy_node()
        rclpy.shutdown()
    if count == 0:
        raise SystemExit("NO_VALID_SNAPSHOT: inspect camera/cloud/joint publishers and geometry.jsonl")


if __name__ == "__main__":
    main()
