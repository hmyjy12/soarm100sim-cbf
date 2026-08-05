#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
ROS_SETUP="${ROS_SETUP:-/opt/ros/humble/setup.bash}"
ROS_LOG_DIR="${ROS_LOG_DIR:-$ROOT_DIR/logs/hardware/ros2}"
PORT="/dev/ttyACM0"
LEROBOT_ENV="${LEROBOT_ENV:-lerobot}"
BUILD_FIRST="false"

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) BUILD_FIRST="true"; shift ;;
    --port) PORT="$2"; shift 2 ;;
    --lerobot-env) LEROBOT_ENV="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: ./ros2/run_single_joint_service.sh [--build] [--port DEVICE]"
      exit 0
      ;;
    *) echo "[ERROR] unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi

source_relaxed "$ROS_SETUP"
mkdir -p "$ROS_LOG_DIR"
export ROS_LOG_DIR
if [[ "$BUILD_FIRST" == "true" ]]; then
  (
    cd "$ROS_WS"
    colcon build --packages-select soarm100_interfaces soarm100_vision
  )
fi
source_relaxed "$ROS_WS/install/setup.bash"

echo "[single_joint_service] port=$PORT max_delta=2deg automatic_return=true"
echo "[single_joint_service] Do not run run_hardware_state.sh at the same time."
ros2 launch soarm100_vision hardware_single_joint.launch.py \
  repo_root:="$ROOT_DIR" \
  port:="$PORT" \
  lerobot_env:="$LEROBOT_ENV"
