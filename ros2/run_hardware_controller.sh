#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
PORT="/dev/ttyACM0"
LEROBOT_ENV="${LEROBOT_ENV:-lerobot}"
BUILD_FIRST="false"
SHOULDER_LIFT_P="16"
CALIBRATION_FILE="hardware/calibration/lerobot/so100_plus_new_arm.json"
CONTROL_RATE_HZ="20.0"
MAX_STREAM_COMMAND_DELTA_RAD="0.25"
RAW_MARGIN_COUNTS="0"
MOVE_POSITION_TOLERANCE_COUNTS="12"
ALLOW_MOVE_STATIC_ERROR="false"

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
    --rate) CONTROL_RATE_HZ="$2"; shift 2 ;;
    --max-stream-command-delta-rad) MAX_STREAM_COMMAND_DELTA_RAD="$2"; shift 2 ;;
    --raw-margin-counts) RAW_MARGIN_COUNTS="$2"; shift 2 ;;
    --move-position-tolerance-counts) MOVE_POSITION_TOLERANCE_COUNTS="$2"; shift 2 ;;
    --allow-move-static-error) ALLOW_MOVE_STATIC_ERROR="true"; shift ;;
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
echo "[hardware_controller] feedback/driver rate=${CONTROL_RATE_HZ}Hz"
echo "[hardware_controller] stream command delta limit=${MAX_STREAM_COMMAND_DELTA_RAD}rad"
echo "[hardware_controller] raw safety margin=${RAW_MARGIN_COUNTS} counts (calibrated hard limits remain active)"
echo "[hardware_controller] move convergence tolerance=${MOVE_POSITION_TOLERANCE_COUNTS} counts"
echo "[hardware_controller] allow move static error=${ALLOW_MOVE_STATIC_ERROR}"
echo "[hardware_controller] Ctrl+C performs verified all-axis torque-off."
ros2 launch soarm100_vision hardware_controller.launch.py \
  repo_root:="$ROOT_DIR" port:="$PORT" lerobot_env:="$LEROBOT_ENV" \
  calibration_file:="$CALIBRATION_FILE" \
  shoulder_lift_p:="$SHOULDER_LIFT_P" \
  feedback_rate_hz:="$CONTROL_RATE_HZ" \
  driver_rate_hz:="$CONTROL_RATE_HZ" \
  max_stream_command_delta_rad:="$MAX_STREAM_COMMAND_DELTA_RAD" \
  raw_margin_counts:="$RAW_MARGIN_COUNTS" \
  move_position_tolerance_counts:="$MOVE_POSITION_TOLERANCE_COUNTS" \
  allow_move_static_error:="$ALLOW_MOVE_STATIC_ERROR"
