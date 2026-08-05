#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
POSE_FILE="hardware/calibration/handeye/wrist_handeye_poses.json"
SEED_POSE_FILE="hardware/calibration/handeye/calibration_seed_pose.json"
DURATION="4.0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pose-file) POSE_FILE="$2"; shift 2 ;;
    --seed-pose-file) SEED_POSE_FILE="$2"; shift 2 ;;
    --duration) DURATION="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: ./ros2/run_wrist_handeye_poses.sh [--pose-file PATH] [--seed-pose-file PATH] [--duration SEC]"
      exit 0
      ;;
    *) echo "[ERROR] unknown option: $1" >&2; exit 2 ;;
  esac
done

set +u
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash
# shellcheck source=/dev/null
source "$ROOT_DIR/ros2/install/setup.bash"
set -u

echo "[handeye_poses] Every candidate requires typing the exact word MOVE."
echo "[handeye_poses] pose_file=$POSE_FILE duration=${DURATION}s"
exec ros2 run soarm100_vision wrist_handeye_pose_sequence_node --ros-args \
  -p repo_root:="$ROOT_DIR" \
  -p pose_file:="$POSE_FILE" \
  -p seed_pose_file:="$SEED_POSE_FILE" \
  -p move_duration:="$DURATION"
