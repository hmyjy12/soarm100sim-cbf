#!/usr/bin/env bash
# Manual eye-in-hand capture loop:
#   Viewer stays open; SPACE powers on + auto-captures; m powers off; q quits.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
SERIAL_PORT="/dev/ttyACM0"
SQUARE_SIZE_M="0.0144"
CAMERA_PID=""
VIEWER_PID=""
CONTROLLER_PID=""
POWERED="false"

usage() {
  cat <<'EOF'
Usage: ./ros2/run_wrist_handeye_manual.sh [options]

Options:
  --square-size-m VALUE  Measured checker square size in meters (default: 0.0144)
  --help                 Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --square-size-m) SQUARE_SIZE_M="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

kill_tree() {
  local pid="$1"
  local sig="${2:-TERM}"
  if [[ -z "$pid" ]]; then
    return 0
  fi
  if kill -0 "$pid" 2>/dev/null; then
    kill "-${sig}" -- "-${pid}" 2>/dev/null || true
    kill "-${sig}" "$pid" 2>/dev/null || true
  fi
}

kill_controller_patterns() {
  local sig="${1:-TERM}"
  pkill "-${sig}" -f "$ROOT_DIR/hardware/tools/run_hardware_controller.py" 2>/dev/null || true
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_hardware_controller.sh" 2>/dev/null || true
  pkill "-${sig}" -f 'ros2 launch soarm100_vision hardware_controller.launch.py' 2>/dev/null || true
  pkill "-${sig}" -f 'hardware_controller_node' 2>/dev/null || true
  pkill "-${sig}" -f '__node:=hardware_controller' 2>/dev/null || true
  pkill "-${sig}" -f '__node:=hardware_robot_state_publisher' 2>/dev/null || true
}

kill_viewer_camera_patterns() {
  local sig="${1:-TERM}"
  pkill "-${sig}" -f 'wrist_handeye_calibrator_node' 2>/dev/null || true
  pkill "-${sig}" -f 'soarm100_vision.*wrist_handeye_calibrator' 2>/dev/null || true
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_wrist_handeye.sh" 2>/dev/null || true
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_wrist_camera.sh" 2>/dev/null || true
  pkill "-${sig}" -f 'v4l2_camera_node.*wrist_camera|__node:=wrist_camera' 2>/dev/null || true
  pkill "-${sig}" -f 'v4l2_camera_node' 2>/dev/null || true
  pkill "-${sig}" -f 'wrist_handeye_pose_sequence_node' 2>/dev/null || true
}

count_leftovers() {
  pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|$ROOT_DIR/ros2/run_hardware_controller.sh|hardware_controller.launch.py|hardware_controller_node|__node:=hardware_controller|__node:=hardware_robot_state_publisher|wrist_handeye_pose_sequence_node|wrist_handeye_calibrator_node|$ROOT_DIR/ros2/run_wrist_handeye.sh|$ROOT_DIR/ros2/run_wrist_camera.sh|__node:=wrist_camera" \
    2>/dev/null | grep -v -E 'cursorsandbox|run_wrist_handeye_manual\.sh|grep|pgrep' || true
}

ros_torque_off() {
  if command -v ros2 >/dev/null 2>&1; then
    timeout 8s ros2 service call /hardware/set_torque \
      soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" \
      >/tmp/handeye_manual_torque.log 2>&1 || true
    if [[ -s /tmp/handeye_manual_torque.log ]]; then
      cat /tmp/handeye_manual_torque.log
    fi
  fi
}

serial_torque_off() {
  if [[ -e "$SERIAL_PORT" ]] && command -v conda >/dev/null 2>&1; then
    conda run --no-capture-output -n lerobot python \
      "$ROOT_DIR/hardware/tools/disable_all_torque.py" \
      --port "$SERIAL_PORT" --confirm DISABLE_ALL_TORQUE \
      >/tmp/handeye_manual_torque_fallback.log 2>&1 || true
    if [[ -s /tmp/handeye_manual_torque_fallback.log ]]; then
      cat /tmp/handeye_manual_torque_fallback.log
    fi
  fi
}

stop_controller_only() {
  echo "[handeye_manual] powering OFF (controller only; Viewer stays open)"
  ros_torque_off
  if [[ -n "${CONTROLLER_PID}" ]]; then
    kill_tree "$CONTROLLER_PID" TERM
    sleep 0.5
    kill_tree "$CONTROLLER_PID" KILL
    wait "$CONTROLLER_PID" 2>/dev/null || true
    CONTROLLER_PID=""
  fi
  kill_controller_patterns TERM
  sleep 0.5
  kill_controller_patterns KILL
  serial_torque_off
  POWERED="false"
}

stop_all() {
  local reason="${1:-cleanup}"
  echo "[handeye_manual] stopping full stack ($reason)"
  stop_controller_only
  if [[ -n "${VIEWER_PID}" ]]; then
    kill_tree "$VIEWER_PID" TERM
  fi
  if [[ -n "${CAMERA_PID}" ]]; then
    kill_tree "$CAMERA_PID" TERM
  fi
  sleep 0.5
  kill_viewer_camera_patterns TERM
  sleep 0.5
  if [[ -n "${VIEWER_PID}" ]]; then
    kill_tree "$VIEWER_PID" KILL
    wait "$VIEWER_PID" 2>/dev/null || true
    VIEWER_PID=""
  fi
  if [[ -n "${CAMERA_PID}" ]]; then
    kill_tree "$CAMERA_PID" KILL
    wait "$CAMERA_PID" 2>/dev/null || true
    CAMERA_PID=""
  fi
  kill_viewer_camera_patterns KILL
  local leftovers
  leftovers="$(count_leftovers)"
  if [[ -n "$leftovers" ]]; then
    echo "[handeye_manual] WARNING: leftover processes after $reason:" >&2
    echo "$leftovers" >&2
    echo "[handeye_manual] If needed: sudo pkill -9 -f hardware_controller" >&2
  else
    echo "[handeye_manual] stack stopped; no matching leftovers."
  fi
}

cleanup() {
  trap - EXIT INT TERM
  stop_all "script exit"
}
trap cleanup EXIT INT TERM

wait_for_topic() {
  local topic="$1"
  local timeout_sec="${2:-20}"
  local start
  start="$(date +%s)"
  while true; do
    if ros2 topic list 2>/dev/null | grep -qx "$topic"; then
      # Require at least one message soon after discovery.
      if timeout 3s ros2 topic echo "$topic" --once >/dev/null 2>&1; then
        return 0
      fi
    fi
    if (( "$(date +%s)" - start >= timeout_sec )); then
      return 1
    fi
    sleep 0.4
  done
}

wait_for_service() {
  local service="$1"
  local timeout_sec="${2:-20}"
  local start
  start="$(date +%s)"
  while true; do
    if ros2 service list 2>/dev/null | grep -qx "$service"; then
      return 0
    fi
    if (( "$(date +%s)" - start >= timeout_sec )); then
      return 1
    fi
    sleep 0.3
  done
}

power_on_hold() {
  if [[ "$POWERED" == "true" ]]; then
    echo "[handeye_manual] already powered. Release your hands, confirm Viewer shows DETECTED, then press SPACE to CAPTURE."
    return 0
  fi
  if [[ -e "$SERIAL_PORT" ]] && fuser "$SERIAL_PORT" >/dev/null 2>&1; then
    echo "[handeye_manual] serial port busy; attempting controller cleanup first"
    stop_controller_only
  fi
  if [[ ! -r "$SERIAL_PORT" || ! -w "$SERIAL_PORT" ]]; then
    echo "[handeye_manual] ERROR: serial port $SERIAL_PORT not usable" >&2
    return 1
  fi
  echo "[handeye_manual] powering ON and holding the current pose (NO capture yet)"
  : >"$ROOT_DIR/log/runtime/hardware/handeye_manual_controller.log"
  setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" \
    >"$ROOT_DIR/log/runtime/hardware/handeye_manual_controller.log" 2>&1 &
  CONTROLLER_PID="$!"
  if ! wait_for_topic "/joint_states" 25; then
    echo "[handeye_manual] ERROR: /joint_states not available after power-on" >&2
    echo "[handeye_manual] see log/runtime/hardware/handeye_manual_controller.log" >&2
    stop_controller_only
    return 1
  fi
  POWERED="true"
  sleep 1.0
  cat <<EOF
[handeye_manual] POWERED ON and holding.
  1) Release your hands from the arm
  2) Confirm the arm is still / stable
  3) Confirm Viewer shows DETECTED with the full board
  4) Press SPACE again to CAPTURE this powered pose
  Or press m to power OFF without capturing.
EOF
}

capture_sample() {
  if [[ "$POWERED" != "true" ]]; then
    echo "[handeye_manual] not powered yet. Press SPACE once to power ON first (capture is the second SPACE)."
    return 1
  fi
  if ! wait_for_service "/wrist_handeye/capture" 10; then
    echo "[handeye_manual] ERROR: /wrist_handeye/capture service missing (Viewer down?)" >&2
    return 1
  fi
  echo "[handeye_manual] requesting capture of the powered/stable pose..."
  local result
  result="$(
    timeout 15s ros2 service call /wrist_handeye/capture std_srvs/srv/Trigger '{}' 2>&1 || true
  )"
  echo "$result"
  if echo "$result" | grep -q 'success=True'; then
    echo "[handeye_manual] capture OK. Press m to power OFF before moving the arm."
    return 0
  fi
  echo "[handeye_manual] capture FAILED. Fix board visibility while still powered, then SPACE again; or m to power OFF."
  return 1
}

handle_space() {
  if [[ "$POWERED" == "true" ]]; then
    capture_sample || true
  else
    power_on_hold || true
  fi
}

print_help() {
  cat <<EOF

[handeye_manual] Viewer stays open.
  SPACE  if unpowered: power ON and hold (no capture yet)
         if powered:   CAPTURE one sample
  m      power OFF / disable torque; then manually move the arm
  s      print tip: use Viewer window key S to solve Tsai
  h      show this help
  q      quit, force-clean all processes, close Viewer

Recommended cycle:
  place arm unpowered -> SPACE (power) -> release hands / check DETECTED
  -> SPACE (capture) -> m (power off) -> move wrist joints -> repeat

Tips:
  - Move mainly wrist_pitch / wrist_jaw / wrist_roll between captures.
  - Keep the checkerboard fixed.
  - Duplicate similarity rejection is DISABLED in this mode.
EOF
}

mkdir -p "$ROOT_DIR/log/runtime/hardware"
source_relaxed /opt/ros/humble/setup.bash
source_relaxed "$ROS_WS/install/setup.bash"

# Clear zombies from previous runs before starting.
stop_all "pre-start"

if [[ ! -r "$SERIAL_PORT" || ! -w "$SERIAL_PORT" ]]; then
  echo "[handeye_manual] serial port $SERIAL_PORT is not readable/writable" >&2
  exit 1
fi
if fuser "$SERIAL_PORT" >/dev/null 2>&1; then
  echo "[handeye_manual] serial port still occupied after cleanup:" >&2
  fuser -v "$SERIAL_PORT" || true
  exit 1
fi

echo "[handeye_manual] Starting wrist camera + Viewer; robot remains UNPOWERED."
setsid "$ROOT_DIR/ros2/run_wrist_camera.sh" \
  >"$ROOT_DIR/log/runtime/hardware/handeye_manual_camera.log" 2>&1 &
CAMERA_PID="$!"
sleep 3

setsid "$ROOT_DIR/ros2/run_wrist_handeye.sh" \
  --allow-duplicates \
  --square-size-m "$SQUARE_SIZE_M" \
  >"$ROOT_DIR/log/runtime/hardware/handeye_manual_viewer.log" 2>&1 &
VIEWER_PID="$!"
sleep 3

if ! wait_for_service "/wrist_handeye/capture" 20; then
  echo "[handeye_manual] ERROR: Viewer/capture service failed to start" >&2
  echo "[handeye_manual] see log/runtime/hardware/handeye_manual_viewer.log" >&2
  exit 1
fi

print_help
echo
echo "[handeye_manual] Manually place the arm (UNPOWERED), then press SPACE to power ON (capture is a second SPACE after you release)."

while true; do
  IFS= read -r -n 1 -s KEY || true
  printf '\n'
  case "$KEY" in
    " ")
      handle_space
      ;;
    m|M)
      if [[ "$POWERED" != "true" && -z "${CONTROLLER_PID}" ]]; then
        echo "[handeye_manual] already unpowered."
      else
        stop_controller_only
      fi
      echo "[handeye_manual] Robot is UNPOWERED. Manually move mainly wrist joints, then SPACE to power ON."
      ;;
    s|S)
      echo "[handeye_manual] Click the Viewer window and press S there to solve Tsai (needs enough samples)."
      ;;
    h|H|"?")
      print_help
      ;;
    q|Q)
      echo "[handeye_manual] quit requested."
      exit 0
      ;;
    "")
      ;;
    *)
      echo "[handeye_manual] unknown key '$KEY' (SPACE/m/s/h/q)"
      ;;
  esac
done
