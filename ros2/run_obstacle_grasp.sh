#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

exec "$ROOT_DIR/ros2/run_vision_grasp.sh" \
  --avoidance on \
  --mujoco on \
  --mujoco-obstacle on \
  --mujoco-sdf-cbf on \
  --mujoco-traj-log "$ROOT_DIR/log/runtime/ros2_mujoco_obstacle_sdf_cbf_grasp.jsonl" \
  "$@"
