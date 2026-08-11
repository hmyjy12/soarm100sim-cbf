#!/usr/bin/env python3
"""Build a small base-frame TCP reach target relative to the live arm pose.

Used to verify real-policy reach with a 2-3 cm displacement from whatever
powered-on posture the operator chose. Orientation is kept equal to the
current pinch TCP (same FK as policy_reach_node).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np


JOINT_NAMES = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)


def _load_training_runtime(repo: Path):
    repo = repo.resolve()
    os.chdir(repo / "ros2")
    sys.path[:] = [
        entry for entry in sys.path
        if entry and Path(entry).resolve() != repo
    ]
    import mujoco  # type: ignore

    source_dir = str(repo / "mujoco")
    if source_dir not in sys.path:
        sys.path.insert(0, source_dir)
    import runtime as reach_runtime  # type: ignore
    return mujoco, reach_runtime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write policy_reach_target.json as current TCP + delta."
    )
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ros2/config/real/policy_reach_target_relative.json"),
    )
    parser.add_argument(
        "--delta-m",
        required=True,
        help="Comma-separated dx,dy,dz in base frame meters, e.g. 0.023,0,0",
    )
    parser.add_argument(
        "--mjcf",
        default="SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml",
    )
    parser.add_argument("--timeout-s", type=float, default=10.0)
    parser.add_argument(
        "--max-delta-norm-m",
        type=float,
        default=0.10,
        help="Refuse delta-vector norms larger than this (default 100 mm).",
    )
    parser.add_argument(
        "--allow-zero",
        action="store_true",
        help="Allow an exact current-pose target for powered hold diagnostics.",
    )
    return parser.parse_args()


def _parse_delta(text: str) -> np.ndarray:
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 3:
        raise ValueError("--delta-m must be dx,dy,dz")
    delta = np.asarray([float(p) for p in parts], dtype=np.float64)
    if not np.all(np.isfinite(delta)):
        raise ValueError("delta contains non-finite values")
    return delta


def _wait_joint_state(timeout_s: float) -> np.ndarray:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import JointState

    rclpy.init()
    node = Node("make_relative_policy_reach_target")
    holder: dict[str, np.ndarray | None] = {"q": None}

    def _on_msg(msg: JointState) -> None:
        if tuple(msg.name) != JOINT_NAMES or len(msg.position) != 7:
            return
        q = np.asarray(msg.position, dtype=np.float64)
        if np.all(np.isfinite(q)):
            holder["q"] = q

    node.create_subscription(JointState, "/joint_states", _on_msg, 10)
    deadline = time.monotonic() + timeout_s
    try:
        while holder["q"] is None and time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    if holder["q"] is None:
        raise RuntimeError(
            f"no valid /joint_states within {timeout_s:.1f}s; "
            "is the hardware controller running?"
        )
    return holder["q"]


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve()
    delta = _parse_delta(args.delta_m)
    norm = float(np.linalg.norm(delta))
    if norm < 1.0e-4 and not args.allow_zero:
        raise SystemExit("[ERROR] delta norm is ~0; choose a non-zero 2-3 cm offset")
    if norm > float(args.max_delta_norm_m) + 1.0e-9:
        raise SystemExit(
            f"[ERROR] |delta|={norm * 1000.0:.1f}mm exceeds "
            f"max {float(args.max_delta_norm_m) * 1000.0:.1f}mm; "
            "relative policy target rejected before motion"
        )

    mujoco, runtime = _load_training_runtime(repo)
    model = mujoco.MjModel.from_xml_path(str(repo / args.mjcf))
    data = mujoco.MjData(model)
    ids = runtime.resolve_robot_ids(model)

    q = _wait_joint_state(float(args.timeout_s))
    for adr, value in zip(ids.qpos_adr, q):
        data.qpos[adr] = float(value)
    mujoco.mj_forward(model, data)
    tcp, quat = runtime.tcp_pose_w(data, ids)
    tcp = np.asarray(tcp, dtype=np.float64).reshape(3)
    quat = np.asarray(quat, dtype=np.float64).reshape(4)
    quat /= max(float(np.linalg.norm(quat)), 1e-12)
    target = tcp + delta

    # Same conservative workspace gate as policy_reach_node.
    if not (
        0.08 <= target[0] <= 0.45
        and -0.30 <= target[1] <= 0.30
        and 0.01 <= target[2] <= 0.45
    ):
        raise SystemExit(
            f"[ERROR] relative target outside conservative workspace: {target.tolist()}"
        )

    output = args.output
    if not output.is_absolute():
        output = repo / output
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "frame_id": "base",
        "hold_current": bool(norm < 1.0e-4),
        "position_m": [float(v) for v in target],
        "quaternion_wxyz": [float(v) for v in quat],
        "description": (
            f"Relative policy-verification target: current TCP + "
            f"({delta[0]:+.4f},{delta[1]:+.4f},{delta[2]:+.4f}) m "
            f"(|delta|={norm * 1000.0:.1f} mm); orientation held."
        ),
        "source_tcp_m": [float(v) for v in tcp],
        "source_quaternion_wxyz": [float(v) for v in quat],
        "delta_m": [float(v) for v in delta],
        "source_joint_position_rad": [float(v) for v in q],
    }
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "[relative_target] "
        f"tcp=({tcp[0]:+.4f},{tcp[1]:+.4f},{tcp[2]:+.4f}) "
        f"delta=({delta[0]:+.4f},{delta[1]:+.4f},{delta[2]:+.4f}) "
        f"|delta|={norm * 1000.0:.1f}mm"
    )
    print(
        "[relative_target] "
        f"target=({target[0]:+.4f},{target[1]:+.4f},{target[2]:+.4f}) "
        f"wrote {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
