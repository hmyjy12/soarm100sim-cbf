#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
VISION_ENV="vision_seg"
PORT="/dev/ttyACM0"
FRAMES_PER_POSE="8"
SETTLE_S="0.75"
MOVE_DURATION_S="7.0"
SCAN_CONFIG="hardware/calibration/link_self_occupancy_scan.json"
CONFIRM=""
BUILD_FIRST="false"
CONTROLLER_PID=""

source_relaxed() {
  set +u
  source "$1"
  set -u
}

cleanup() {
  local code=$?
  trap - EXIT INT TERM
  if [[ -n "$CONTROLLER_PID" ]] && kill -0 "$CONTROLLER_PID" 2>/dev/null; then
    source_relaxed /opt/ros/humble/setup.bash
    source_relaxed "$ROS_WS/install/setup.bash"
    timeout 4 ros2 service call /hardware/set_torque \
      soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" >/dev/null 2>&1 || true
    kill -TERM "-$CONTROLLER_PID" 2>/dev/null || true
    wait "$CONTROLLER_PID" 2>/dev/null || true
  fi
  exit "$code"
}
trap cleanup EXIT INT TERM

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vision-env) VISION_ENV="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --frames-per-pose) FRAMES_PER_POSE="$2"; shift 2 ;;
    --settle-s) SETTLE_S="$2"; shift 2 ;;
    --move-duration-s) MOVE_DURATION_S="$2"; shift 2 ;;
    --scan-config) SCAN_CONFIG="$2"; shift 2 ;;
    --build) BUILD_FIRST="true"; shift ;;
    --confirm) CONFIRM="$2"; shift 2 ;;
    *) echo "[ERROR] unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ "$CONFIRM" != "COLLECT_LINK_SELF_OCCUPANCY" ]]; then
  echo "[ERROR] this automatically moves the real arm." >&2
  echo "Add --confirm COLLECT_LINK_SELF_OCCUPANCY after clearing the workspace." >&2
  exit 2
fi
if ! [[ "$FRAMES_PER_POSE" =~ ^[0-9]+$ ]] || (( FRAMES_PER_POSE < 3 || FRAMES_PER_POSE > 30 )); then
  echo "[ERROR] --frames-per-pose must be an integer in [3, 30]" >&2
  exit 2
fi
if ! awk -v v="$SETTLE_S" 'BEGIN { exit !(v >= 0.3 && v <= 3.0) }'; then
  echo "[ERROR] --settle-s must be within [0.3, 3.0]" >&2
  exit 2
fi
if ! awk -v v="$MOVE_DURATION_S" 'BEGIN { exit !(v >= 3.0 && v <= 12.0) }'; then
  echo "[ERROR] --move-duration-s must be within [3.0, 12.0]" >&2
  exit 2
fi
if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi
if fuser "$PORT" >/dev/null 2>&1; then
  echo "[ERROR] serial port is already in use" >&2
  fuser -v "$PORT" || true
  exit 1
fi
if pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|hardware_controller_node" >/dev/null; then
  echo "[ERROR] residual hardware controller process detected" >&2
  pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|hardware_controller_node" >&2 || true
  exit 1
fi

printf -v SETTLE_PARAM "%.6f" "$SETTLE_S"
printf -v MOVE_DURATION_PARAM "%.6f" "$MOVE_DURATION_S"
source_relaxed /opt/ros/humble/setup.bash
if [[ "$BUILD_FIRST" == "true" ]]; then
  (cd "$ROS_WS" && colcon build --packages-select soarm100_interfaces soarm100_vision --symlink-install)
fi
source_relaxed "$ROS_WS/install/setup.bash"
mkdir -p "$ROOT_DIR/log/runtime/hardware"

echo "[link_self] camera must already publish /camera/depth/image_raw and /camera/depth/camera_info."
echo "[link_self] clear the complete workspace; no hands or external objects may enter during scanning."
echo "[link_self] poses use small offsets around the live startup pose and invalid targets are skipped."
echo "[link_self] scan config: $SCAN_CONFIG"

setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" \
  --port "$PORT" --rate 20.0 --max-stream-command-delta-rad 0.25 \
  --move-position-tolerance-counts 80 --allow-move-static-error \
  >"$ROOT_DIR/log/runtime/hardware/link_self_occupancy_controller.log" 2>&1 &
CONTROLLER_PID=$!

for _ in $(seq 1 150); do
  if ! kill -0 "$CONTROLLER_PID" 2>/dev/null; then
    echo "[ERROR] hardware controller exited; inspect link_self_occupancy_controller.log" >&2
    exit 1
  fi
  ros2 service list 2>/dev/null | grep -qx /hardware/move_joint_target && break
  sleep 0.1
done
ros2 service list 2>/dev/null | grep -qx /hardware/move_joint_target || {
  echo "[ERROR] /hardware/move_joint_target unavailable" >&2
  exit 1
}

PYTHONPATH="$ROS_WS/soarm100_vision${PYTHONPATH:+:$PYTHONPATH}" \
  conda run --no-capture-output -n "$VISION_ENV" python \
  "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/link_self_occupancy_collector_node.py" \
  --ros-args \
  -p repo_root:="$ROOT_DIR" \
  -p scan_config:="$SCAN_CONFIG" \
  -p frames_per_pose:="$FRAMES_PER_POSE" \
  -p settle_s:="$SETTLE_PARAM" \
  -p move_duration_s:="$MOVE_DURATION_PARAM" \
  -p confirmation:=COLLECT_LINK_SELF_OCCUPANCY

echo "[link_self] collection complete; torque-off requested during cleanup."
