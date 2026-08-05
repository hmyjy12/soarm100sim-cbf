#!/usr/bin/env python3
"""Mirror read-only hardware joint packets into a MuJoCo viewer."""

from __future__ import annotations

import argparse
import json
import socket
import time
from pathlib import Path

import mujoco
import mujoco.viewer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MJCF = (
    PROJECT_ROOT
    / "SO-ARM100"
    / "Simulation"
    / "SO100"
    / "mujoco"
    / "so100_plus.xml"
)
JOINT_NAMES = (
    "shoulder_rotation_joint",
    "shoulder_pitch_joint",
    "ellbow_joint",
    "wrist_pitch_joint",
    "wrist_jaw_joint",
    "wrist_roll_joint",
    "gripper_joint",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mjcf", type=Path, default=DEFAULT_MJCF)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--udp-port", type=int, default=15001)
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--print-period", type=float, default=1.0)
    return parser.parse_args()


def apply_packet(model: mujoco.MjModel, data: mujoco.MjData, packet: dict) -> None:
    if packet.get("source") != "so100_plus_feetech_read_only":
        raise ValueError("unexpected packet source")
    policy = packet["policy"]
    if set(policy) != set(JOINT_NAMES):
        raise ValueError("packet does not contain the expected policy joints")
    for name in JOINT_NAMES:
        joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
        qpos_address = model.jnt_qposadr[joint_id]
        value = float(policy[name])
        if model.jnt_limited[joint_id]:
            low, high = model.jnt_range[joint_id]
            value = min(float(high), max(float(low), value))
        data.qpos[qpos_address] = value
    mujoco.mj_forward(model, data)


def main() -> int:
    args = parse_args()
    model = mujoco.MjModel.from_xml_path(str(args.mjcf.resolve()))
    data = mujoco.MjData(model)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.host, args.udp_port))
    sock.setblocking(False)
    latest_packet = None
    last_packet_time = None
    next_print = time.monotonic()

    print(
        f"[policy_joint_mirror] listening={args.host}:{args.udp_port}; "
        "waiting for read-only hardware stream"
    )
    try:
        with mujoco.viewer.launch_passive(model, data) as viewer:
            while viewer.is_running():
                while True:
                    try:
                        encoded, _ = sock.recvfrom(65535)
                    except BlockingIOError:
                        break
                    latest_packet = json.loads(encoded.decode("ascii"))
                    apply_packet(model, data, latest_packet)
                    last_packet_time = time.monotonic()

                now = time.monotonic()
                if latest_packet and now >= next_print:
                    age = (
                        float("inf")
                        if last_packet_time is None
                        else now - last_packet_time
                    )
                    status = "LIVE" if age <= args.timeout else "STALE"
                    print(
                        f"[policy_joint_mirror] status={status} "
                        f"seq={latest_packet['sequence']} age={age:.3f}s"
                    )
                    next_print = now + args.print_period
                viewer.sync()
                time.sleep(1 / 60)
    finally:
        sock.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
