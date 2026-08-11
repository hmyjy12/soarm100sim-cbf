#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
TARGET_CONFIG="ros2/config/real/policy_reach_target.json"
RELATIVE_DELTA=""
VISION_ENV="vision_seg"
PORT="/dev/ttyACM0"
BUILD_FIRST="false"
CONFIRM=""
CONTROLLER_PID=""
CONTROL_RATE_HZ="20.0"
MAX_RELATIVE_DELTA_M="0.10"
MAX_TRACKING_ERROR_RAD="0.25"
ENABLE_JOINT_LIMIT_CBF="false"

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
    timeout 3 ros2 service call /hardware/set_torque soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" >/dev/null 2>&1 || true
    kill -TERM "-$CONTROLLER_PID" 2>/dev/null || true
    for _ in $(seq 1 50); do
      if ! kill -0 "$CONTROLLER_PID" 2>/dev/null; then
        break
      fi
      sleep 0.1
    done
    if kill -0 "$CONTROLLER_PID" 2>/dev/null; then
      kill -KILL "-$CONTROLLER_PID" 2>/dev/null || true
    fi
    wait "$CONTROLLER_PID" 2>/dev/null || true
  fi
  exit "$code"
}

assert_no_residual_controller() {
  local matches nodes services
  matches="$(pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|$ROOT_DIR/ros2/run_hardware_controller.sh|hardware_controller.launch.py|hardware_controller_node|__node:=hardware_controller" || true)"
  if [[ -n "$matches" ]]; then
    echo "[ERROR] residual hardware-controller process detected. Refusing to share ROS2 services:" >&2
    echo "$matches" >&2
    echo "Stop that controller cleanly first. Do not start policy reach over an existing controller." >&2
    exit 1
  fi

  nodes="$(ros2 node list 2>/dev/null || true)"
  if grep -qx '/hardware_controller' <<<"$nodes" || grep -qx '/so100_plus_hardware_controller' <<<"$nodes"; then
    echo "[ERROR] residual ROS2 hardware-controller node detected:" >&2
    echo "$nodes" | grep -E 'hardware_controller|so100_plus_hardware_controller' >&2 || true
    exit 1
  fi

  services="$(ros2 service list --no-daemon --spin-time 0.5 2>/dev/null || true)"
  if grep -qx '/hardware/set_torque' <<<"$services" || grep -qx '/hardware/move_joint_target' <<<"$services"; then
    echo "[ERROR] residual /hardware service detected. Refusing to bind to an unknown controller:" >&2
    echo "$services" | grep '^/hardware/' >&2 || true
    exit 1
  fi
}

hardware_controller_ready() {
  grep -q "hardware controller ready" \
    "$ROOT_DIR/logs/hardware/policy_reach_controller.log" 2>/dev/null
}
trap cleanup EXIT INT TERM

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) BUILD_FIRST="true"; shift ;;
    --target-config) TARGET_CONFIG="$2"; shift 2 ;;
    --relative-delta)
      RELATIVE_DELTA="$2"
      TARGET_CONFIG="ros2/config/real/policy_reach_target_relative.json"
      shift 2
      ;;
    --vision-env) VISION_ENV="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --rate) CONTROL_RATE_HZ="$2"; shift 2 ;;
    --max-relative-delta-m) MAX_RELATIVE_DELTA_M="$2"; shift 2 ;;
    --max-tracking-error-rad) MAX_TRACKING_ERROR_RAD="$2"; shift 2 ;;
    --joint-limit-cbf) ENABLE_JOINT_LIMIT_CBF="$2"; shift 2 ;;
    --confirm) CONFIRM="$2"; shift 2 ;;
    *) echo "[ERROR] unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ "$CONFIRM" != "RUN_POLICY_REACH" ]]; then
  echo "[ERROR] this can move the real arm. Add --confirm RUN_POLICY_REACH" >&2
  exit 2
fi
if ! [[ "$CONTROL_RATE_HZ" =~ ^[0-9]+([.][0-9]+)?$ ]] || \
   ! awk -v value="$CONTROL_RATE_HZ" 'BEGIN { exit !(value >= 5 && value <= 30) }'; then
  echo "[ERROR] --rate must be within [5, 30] Hz" >&2
  exit 2
fi
if ! [[ "$MAX_RELATIVE_DELTA_M" =~ ^[0-9]+([.][0-9]+)?$ ]] || \
   ! awk -v value="$MAX_RELATIVE_DELTA_M" 'BEGIN { exit !(value > 0 && value <= 0.15) }'; then
  echo "[ERROR] --max-relative-delta-m must be within (0, 0.15] m" >&2
  exit 2
fi
if ! [[ "$MAX_TRACKING_ERROR_RAD" =~ ^[0-9]+([.][0-9]+)?$ ]] || \
   ! awk -v value="$MAX_TRACKING_ERROR_RAD" 'BEGIN { exit !(value >= 0.02 && value <= 0.35) }'; then
  echo "[ERROR] --max-tracking-error-rad must be within [0.02, 0.35] rad" >&2
  exit 2
fi
printf -v CONTROL_RATE_PARAM "%.6f" "$CONTROL_RATE_HZ"
printf -v MAX_TRACKING_ERROR_PARAM "%.6f" "$MAX_TRACKING_ERROR_RAD"
if [[ "$ENABLE_JOINT_LIMIT_CBF" != "true" && "$ENABLE_JOINT_LIMIT_CBF" != "false" && \
      "$ENABLE_JOINT_LIMIT_CBF" != "on" && "$ENABLE_JOINT_LIMIT_CBF" != "off" ]]; then
  echo "[ERROR] --joint-limit-cbf must be on/off or true/false" >&2
  exit 2
fi
if [[ "$ENABLE_JOINT_LIMIT_CBF" == "on" ]]; then ENABLE_JOINT_LIMIT_CBF="true"; fi
if [[ "$ENABLE_JOINT_LIMIT_CBF" == "off" ]]; then ENABLE_JOINT_LIMIT_CBF="false"; fi
if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi
if fuser "$PORT" >/dev/null 2>&1; then
  echo "[ERROR] serial port is already in use:" >&2
  fuser -v "$PORT" || true
  exit 1
fi
if [[ -z "$RELATIVE_DELTA" && ! -f "$ROOT_DIR/$TARGET_CONFIG" ]]; then
  echo "[ERROR] target config not found: $ROOT_DIR/$TARGET_CONFIG" >&2
  exit 1
fi

source_relaxed /opt/ros/humble/setup.bash
if [[ "$BUILD_FIRST" == "true" ]]; then
  (cd "$ROS_WS" && colcon build --packages-select soarm100_interfaces soarm100_vision --symlink-install)
fi
source_relaxed "$ROS_WS/install/setup.bash"
assert_no_residual_controller

echo "[policy_reach] target config: $ROOT_DIR/$TARGET_CONFIG"
if [[ -n "$RELATIVE_DELTA" ]]; then
  echo "[policy_reach] relative mode: current TCP + ($RELATIVE_DELTA) m (orientation held)"
  echo "[policy_reach] relative target norm limit=${MAX_RELATIVE_DELTA_M}m; final target must remain inside base workspace."
fi
echo "[policy_reach] transition layer: feedback/policy/driver=${CONTROL_RATE_PARAM}Hz, vmax=0.20rad/s, amax=0.80rad/s^2, tracking=${MAX_TRACKING_ERROR_PARAM}rad, driver_limit=${MAX_TRACKING_ERROR_PARAM}rad."
echo "[policy_reach] calibrated joint-limit CBF=$ENABLE_JOINT_LIMIT_CBF margin=100 counts."
mkdir -p "$ROOT_DIR/logs/hardware"
setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" --port "$PORT" --rate "$CONTROL_RATE_PARAM" \
  --max-stream-command-delta-rad "$MAX_TRACKING_ERROR_PARAM" \
  >"$ROOT_DIR/logs/hardware/policy_reach_controller.log" 2>&1 &
CONTROLLER_PID=$!

for _ in $(seq 1 150); do
  if ! kill -0 "$CONTROLLER_PID" 2>/dev/null; then
    echo "[ERROR] hardware controller exited during startup; see logs/hardware/policy_reach_controller.log" >&2
    tail -n 30 "$ROOT_DIR/logs/hardware/policy_reach_controller.log" >&2 || true
    exit 1
  fi
  if hardware_controller_ready; then
    break
  fi
  sleep 0.1
done
if ! hardware_controller_ready; then
  echo "[ERROR] hardware controller did not become ready; see logs/hardware/policy_reach_controller.log" >&2
  tail -n 30 "$ROOT_DIR/logs/hardware/policy_reach_controller.log" >&2 || true
  exit 1
fi

if [[ -n "$RELATIVE_DELTA" ]]; then
  echo "[policy_reach] sampling live /joint_states and writing relative target..."
  conda run --no-capture-output -n "$VISION_ENV" python \
    "$ROOT_DIR/ros2/scripts/real/make_relative_policy_reach_target.py" \
    --repo-root "$ROOT_DIR" \
    --output "$TARGET_CONFIG" \
    --delta-m "$RELATIVE_DELTA" \
    --max-delta-norm-m "$MAX_RELATIVE_DELTA_M" \
    --allow-zero
fi

echo "[policy_reach] running. Ctrl+C stops policy and requests all-axis torque-off."
conda run --no-capture-output -n "$VISION_ENV" python \
  "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/policy_reach_node.py" \
  --ros-args \
  -p repo_root:="$ROOT_DIR" \
  -p target_config:="$TARGET_CONFIG" \
  -p control_rate_hz:="$CONTROL_RATE_PARAM" \
  -p max_tracking_error_rad:="$MAX_TRACKING_ERROR_PARAM" \
  -p enable_joint_limit_cbf:="$ENABLE_JOINT_LIMIT_CBF" \
  -p start_on_launch:=true
