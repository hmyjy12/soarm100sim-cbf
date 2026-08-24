#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
ROS_SETUP="${ROS_SETUP:-/opt/ros/humble/setup.bash}"
LEROBOT_ENV="${LEROBOT_ENV:-lerobot}"
ROS_LOG_DIR="${ROS_LOG_DIR:-$ROOT_DIR/log/runtime/hardware/ros2}"
PORT="/dev/ttyACM0"
CALIBRATION="hardware/calibration/lerobot/so100_plus_new_arm.json"
UDP_PORT="15001"
RATE="20"
USE_RVIZ="true"
BUILD_FIRST="false"

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

usage() {
  cat <<'EOF'
Usage: ./ros2/run_hardware_state.sh [options]

Read-only hardware feedback to ROS2 /joint_states. This script never sends a
motor command and the hardware reader refuses to start if any torque is enabled.

Options:
  --build              Build the required ROS2 packages first.
  --port DEVICE        Feetech serial port. Default: /dev/ttyACM0.
  --calibration FILE   LeRobot calibration JSON. Default: new-arm calibration.
  --udp-port PORT      Local bridge UDP port. Default: 15001.
  --rate HZ            Hardware read rate, 1..50. Default: 20.
  --rviz on|off        Start RViz. Default: on.
  --lerobot-env NAME   Conda environment. Default: lerobot.
  -h, --help           Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) BUILD_FIRST="true"; shift ;;
    --port) PORT="$2"; shift 2 ;;
    --calibration) CALIBRATION="$2"; shift 2 ;;
    --udp-port) UDP_PORT="$2"; shift 2 ;;
    --rate) RATE="$2"; shift 2 ;;
    --rviz)
      case "$2" in
        on|true|1) USE_RVIZ="true" ;;
        off|false|0) USE_RVIZ="false" ;;
        *) echo "[ERROR] --rviz must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --lerobot-env) LEROBOT_ENV="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  echo "Run 'newgrp dialout' in this terminal or log in with dialout active." >&2
  exit 1
fi

if [[ "$CALIBRATION" != /* ]]; then
  CALIBRATION="$ROOT_DIR/$CALIBRATION"
fi
if [[ ! -f "$CALIBRATION" ]]; then
  echo "[ERROR] calibration file not found: $CALIBRATION" >&2
  exit 1
fi

source_relaxed "$ROS_SETUP"
mkdir -p "$ROS_LOG_DIR"
export ROS_LOG_DIR
if [[ "$BUILD_FIRST" == "true" ]]; then
  (
    cd "$ROS_WS"
    colcon build --packages-select so100_plus_description soarm100_vision
  )
fi
source_relaxed "$ROS_WS/install/setup.bash"

reader_pid=""
cleanup() {
  if [[ -n "$reader_pid" ]] && kill -0 "$reader_pid" 2>/dev/null; then
    kill -TERM "$reader_pid" 2>/dev/null || true
    wait "$reader_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

echo "[hardware_state] mode=STRICT_READ_ONLY port=$PORT rate=${RATE}Hz udp=$UDP_PORT"
echo "[hardware_state] calibration=$CALIBRATION"
echo "[hardware_state] rviz=$USE_RVIZ topic=/joint_states stale=/hardware/joint_state_stale"

conda run --no-capture-output -n "$LEROBOT_ENV" \
  python "$ROOT_DIR/hardware/tools/stream_policy_joint_udp.py" \
  --port "$PORT" \
  --calibration "$CALIBRATION" \
  --mapping "$ROOT_DIR/hardware/calibration/policy_joint_mapping.json" \
  --host 127.0.0.1 \
  --udp-port "$UDP_PORT" \
  --rate "$RATE" \
  --print-period 3 \
  --log "$ROOT_DIR/log/runtime/hardware/policy_joint_ros2_stream.jsonl" &
reader_pid=$!

ros2 launch soarm100_vision hardware_state.launch.py \
  udp_port:="$UDP_PORT" \
  use_rviz:="$USE_RVIZ"
