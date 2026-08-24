#!/usr/bin/env bash
# Manual Orbbec eye-to-hand capture loop.
# Viewer stays open; SPACE powers on / captures; m powers off; q force-cleans all.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
ORBBEC_WS="${ORBBEC_WS:-$ROOT_DIR/third_party/orbbec_293_ws}"
SERIAL_PORT="/dev/ttyACM0"
CAMERA_PID=""
VIEWER_PID=""
CONTROLLER_PID=""
POWERED="false"

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

kill_orbbec_viewer_patterns() {
  local sig="${1:-TERM}"
  # Calibrator / OpenCV GUI
  pkill "-${sig}" -f 'orbbec_eye_to_hand_calibrator_node' 2>/dev/null || true
  pkill "-${sig}" -f 'soarm100_vision.*orbbec_eye_to_hand' 2>/dev/null || true
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_orbbec_handeye.sh" 2>/dev/null || true
  # Orbbec ROS driver / launch / containers
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_orbbec_camera.sh" 2>/dev/null || true
  pkill "-${sig}" -f 'ros2 launch orbbec_camera gemini_330_series.launch.py' 2>/dev/null || true
  pkill "-${sig}" -f 'orbbec_camera' 2>/dev/null || true
  pkill "-${sig}" -f '__ns:=/camera' 2>/dev/null || true
  pkill "-${sig}" -f 'component_container.*camera' 2>/dev/null || true
  pkill "-${sig}" -f 'OrbbecViewer' 2>/dev/null || true
  # Do not leave wrist handeye leftovers interfering either
  pkill "-${sig}" -f 'wrist_handeye_calibrator_node' 2>/dev/null || true
  pkill "-${sig}" -f 'wrist_handeye_pose_sequence_node' 2>/dev/null || true
}

count_leftovers() {
  pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|$ROOT_DIR/ros2/run_hardware_controller.sh|hardware_controller.launch.py|hardware_controller_node|__node:=hardware_controller|__node:=hardware_robot_state_publisher|orbbec_eye_to_hand_calibrator_node|$ROOT_DIR/ros2/run_orbbec_handeye.sh|$ROOT_DIR/ros2/run_orbbec_camera.sh|gemini_330_series.launch.py|OrbbecViewer|__ns:=/camera" \
    2>/dev/null | grep -v -E 'cursorsandbox|run_orbbec_handeye_manual\.sh|grep|pgrep' || true
}

ros_torque_off() {
  if command -v ros2 >/dev/null 2>&1; then
    timeout 8s ros2 service call /hardware/set_torque \
      soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" \
      >/tmp/orbbec_handeye_torque.log 2>&1 || true
    if [[ -s /tmp/orbbec_handeye_torque.log ]]; then
      cat /tmp/orbbec_handeye_torque.log
    fi
  fi
}

serial_torque_off() {
  if [[ -e "$SERIAL_PORT" ]] && command -v conda >/dev/null 2>&1; then
    conda run --no-capture-output -n lerobot python \
      "$ROOT_DIR/hardware/tools/disable_all_torque.py" \
      --port "$SERIAL_PORT" --confirm DISABLE_ALL_TORQUE \
      >/tmp/orbbec_handeye_torque_fallback.log 2>&1 || true
    if [[ -s /tmp/orbbec_handeye_torque_fallback.log ]]; then
      cat /tmp/orbbec_handeye_torque_fallback.log
    fi
  fi
}

stop_controller_only() {
  echo "[orbbec_handeye] powering OFF (controller only; Orbbec Viewer stays open)"
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
  echo "[orbbec_handeye] stopping full stack ($reason) — clearing processes + GUI"
  stop_controller_only
  if [[ -n "${VIEWER_PID}" ]]; then
    kill_tree "$VIEWER_PID" TERM
  fi
  if [[ -n "${CAMERA_PID}" ]]; then
    kill_tree "$CAMERA_PID" TERM
  fi
  sleep 0.5
  kill_orbbec_viewer_patterns TERM
  sleep 1
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
  kill_orbbec_viewer_patterns KILL
  kill_controller_patterns KILL
  sleep 0.5
  local leftovers
  leftovers="$(count_leftovers)"
  if [[ -n "$leftovers" ]]; then
    echo "[orbbec_handeye] WARNING: leftover processes after $reason:" >&2
    echo "$leftovers" >&2
    echo "[orbbec_handeye] If needed: sudo pkill -9 -f 'orbbec_camera|gemini_330|hardware_controller|OrbbecViewer'" >&2
  else
    echo "[orbbec_handeye] stack stopped; no matching leftovers (GUI/camera/controller cleared)."
  fi
}

cleanup() {
  trap - EXIT INT TERM
  stop_all "script exit / quit"
}
trap cleanup EXIT INT TERM

wait_for_topic() {
  local topic="$1"
  local timeout_sec="${2:-30}"
  local start
  start="$(date +%s)"
  while true; do
    if ros2 topic list 2>/dev/null | grep -qx "$topic"; then
      if timeout 4s ros2 topic echo "$topic" --once >/dev/null 2>&1; then
        return 0
      fi
    fi
    if (( "$(date +%s)" - start >= timeout_sec )); then
      return 1
    fi
    sleep 0.5
  done
}

wait_for_service() {
  local service="$1"
  local timeout_sec="${2:-30}"
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
    echo "[orbbec_handeye] already powered. Release hands, confirm DETECTED, then SPACE to CAPTURE."
    return 0
  fi
  if [[ -e "$SERIAL_PORT" ]] && fuser "$SERIAL_PORT" >/dev/null 2>&1; then
    echo "[orbbec_handeye] serial port busy; cleaning controller first"
    stop_controller_only
  fi
  if [[ ! -r "$SERIAL_PORT" || ! -w "$SERIAL_PORT" ]]; then
    echo "[orbbec_handeye] ERROR: serial port $SERIAL_PORT not usable" >&2
    return 1
  fi
  echo "[orbbec_handeye] powering ON and holding current pose (NO capture yet)"
  : >"$ROOT_DIR/log/runtime/hardware/orbbec_handeye_controller.log"
  setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" \
    >"$ROOT_DIR/log/runtime/hardware/orbbec_handeye_controller.log" 2>&1 &
  CONTROLLER_PID="$!"
  if ! wait_for_topic "/joint_states" 25; then
    echo "[orbbec_handeye] ERROR: /joint_states unavailable after power-on" >&2
    echo "[orbbec_handeye] see log/runtime/hardware/orbbec_handeye_controller.log" >&2
    stop_controller_only
    return 1
  fi
  POWERED="true"
  sleep 1.0
  cat <<EOF
[orbbec_handeye] POWERED ON and holding.
  1) Release your hands
  2) Confirm arm is stable; gripper opening unchanged; board not slipped
  3) Confirm Viewer shows DETECTED (full 9x6 board)
  4) Press SPACE again to CAPTURE
  Or press m to power OFF without capturing.
EOF
}

capture_sample() {
  if [[ "$POWERED" != "true" ]]; then
    echo "[orbbec_handeye] not powered yet. First SPACE = power ON; second SPACE = capture."
    return 1
  fi
  if ! wait_for_service "/orbbec_handeye/capture" 10; then
    echo "[orbbec_handeye] ERROR: /orbbec_handeye/capture missing (Viewer down?)" >&2
    return 1
  fi
  echo "[orbbec_handeye] requesting capture..."
  local result
  result="$(
    timeout 15s ros2 service call /orbbec_handeye/capture std_srvs/srv/Trigger '{}' 2>&1 || true
  )"
  echo "$result"
  if echo "$result" | grep -q 'success=True'; then
    echo "[orbbec_handeye] capture OK. Press m to power OFF before moving the arm."
    return 0
  fi
  echo "[orbbec_handeye] capture FAILED. Fix DETECTED while powered, SPACE again; or m to power OFF."
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

[orbbec_handeye] Eye-to-hand manual loop (Orbbec fixed, board on gripper).
  SPACE  unpowered -> power ON hold (no capture)
         powered   -> CAPTURE one sample
  m      power OFF; then move arm (keep gripper opening fixed)
  s      tip: click Viewer and press S to solve Tsai
  h      help
  q      quit; force-clear camera/controller/GUI processes

Cycle:
  clamp board on fingertips (no slip) -> pose unpowered
  -> SPACE (power) -> release / DETECTED -> SPACE (capture)
  -> m (off) -> change wrist pose -> repeat
  -> Viewer S to solve -> terminal q to exit

Notes:
  - gripper_frame=wrist_roll; do not change gripper opening mid-session
  - duplicate rejection DISABLED
  - outputs: log/runtime/hardware/orbbec_handeye/<timestamp>/
EOF
}

mkdir -p "$ROOT_DIR/log/runtime/hardware"
source_relaxed /opt/ros/humble/setup.bash
source_relaxed "$ORBBEC_WS/install/setup.bash"
source_relaxed "$ROS_WS/install/setup.bash"

stop_all "pre-start"

if [[ ! -r "$SERIAL_PORT" || ! -w "$SERIAL_PORT" ]]; then
  echo "[orbbec_handeye] serial port $SERIAL_PORT is not readable/writable" >&2
  exit 1
fi
if fuser "$SERIAL_PORT" >/dev/null 2>&1; then
  echo "[orbbec_handeye] serial still occupied after cleanup:" >&2
  fuser -v "$SERIAL_PORT" || true
  exit 1
fi

echo "[orbbec_handeye] Starting Orbbec RGB + eye-to-hand Viewer; robot UNPOWERED."
setsid "$ROOT_DIR/ros2/run_orbbec_camera.sh" \
  >"$ROOT_DIR/log/runtime/hardware/orbbec_handeye_camera.log" 2>&1 &
CAMERA_PID="$!"

echo "[orbbec_handeye] waiting for /camera/color/image_raw ..."
if ! wait_for_topic "/camera/color/image_raw" 40; then
  echo "[orbbec_handeye] ERROR: Orbbec RGB not publishing. See log/runtime/hardware/orbbec_handeye_camera.log" >&2
  exit 1
fi

setsid "$ROOT_DIR/ros2/run_orbbec_handeye.sh" \
  >"$ROOT_DIR/log/runtime/hardware/orbbec_handeye_viewer.log" 2>&1 &
VIEWER_PID="$!"
sleep 2

if ! wait_for_service "/orbbec_handeye/capture" 25; then
  echo "[orbbec_handeye] ERROR: Viewer/capture service failed. See log/runtime/hardware/orbbec_handeye_viewer.log" >&2
  exit 1
fi

print_help
echo
echo "[orbbec_handeye] Clamp board on fingertips, place pose UNPOWERED, then SPACE to power ON."

while true; do
  IFS= read -r -n 1 -s KEY || true
  printf '\n'
  case "$KEY" in
    " ")
      handle_space
      ;;
    m|M)
      if [[ "$POWERED" != "true" && -z "${CONTROLLER_PID}" ]]; then
        echo "[orbbec_handeye] already unpowered."
      else
        stop_controller_only
      fi
      echo "[orbbec_handeye] UNPOWERED. Move arm (gripper opening fixed), then SPACE to power ON."
      ;;
    s|S)
      echo "[orbbec_handeye] Click the Orbbec Viewer window and press S to solve Tsai."
      ;;
    h|H|"?")
      print_help
      ;;
    q|Q)
      echo "[orbbec_handeye] quit requested — cleaning processes and GUI."
      exit 0
      ;;
    "")
      ;;
    *)
      echo "[orbbec_handeye] unknown key '$KEY' (SPACE/m/s/h/q)"
      ;;
  esac
done
