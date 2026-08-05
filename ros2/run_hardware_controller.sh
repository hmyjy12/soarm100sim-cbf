#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
PORT="/dev/ttyACM0"
LEROBOT_ENV="${LEROBOT_ENV:-lerobot}"
BUILD_FIRST="false"
SHOULDER_LIFT_P="16"
CALIBRATION_FILE="hardware/calibration/lerobot/so100_plus_new_arm.json"

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
    --shoulder-lift-p) SHOULDER_LIFT_P="$2"; shift 2 ;;
    --calibration) CALIBRATION_FILE="$2"; shift 2 ;;
    *) echo "[ERROR] unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi
if fuser "$PORT" >/dev/null 2>&1; then
  echo "[ERROR] serial port is already in use: $PORT" >&2
  fuser -v "$PORT" || true
  exit 1
fi

source_relaxed /opt/ros/humble/setup.bash
if [[ "$BUILD_FIRST" == "true" ]]; then
  (cd "$ROS_WS" && colcon build --packages-select soarm100_interfaces soarm100_vision)
fi
source_relaxed "$ROS_WS/install/setup.bash"

echo "[hardware_controller] Starting persistent seven-axis hold controller."
echo "[hardware_controller] shoulder_lift_p=$SHOULDER_LIFT_P (baseline restore=16)"
echo "[hardware_controller] calibration=$CALIBRATION_FILE"
echo "[hardware_controller] Ctrl+C performs verified all-axis torque-off."
ros2 launch soarm100_vision hardware_controller.launch.py \
  repo_root:="$ROOT_DIR" port:="$PORT" lerobot_env:="$LEROBOT_ENV" \
  calibration_file:="$CALIBRATION_FILE" \
  shoulder_lift_p:="$SHOULDER_LIFT_P"
