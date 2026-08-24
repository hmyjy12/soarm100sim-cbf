#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
SERIAL_PORT="/dev/ttyACM0"
PIDS=()

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

# Kill one process group (negative PID) then the leader itself.
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

# Match only this project's handeye/controller stack.
kill_handeye_patterns() {
  local sig="${1:-TERM}"
  pkill "-${sig}" -f "$ROOT_DIR/hardware/tools/run_hardware_controller.py" 2>/dev/null || true
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_hardware_controller.sh" 2>/dev/null || true
  pkill "-${sig}" -f 'ros2 launch soarm100_vision hardware_controller.launch.py' 2>/dev/null || true
  pkill "-${sig}" -f 'soarm100_vision/hardware_controller_node|soarm100_vision/lib/soarm100_vision/hardware_controller_node' 2>/dev/null || true
  pkill "-${sig}" -f 'hardware_controller_node' 2>/dev/null || true
  pkill "-${sig}" -f '__node:=hardware_controller' 2>/dev/null || true
  pkill "-${sig}" -f '__node:=hardware_robot_state_publisher' 2>/dev/null || true
  pkill "-${sig}" -f 'wrist_handeye_pose_sequence_node' 2>/dev/null || true
  pkill "-${sig}" -f 'wrist_handeye_calibrator_node' 2>/dev/null || true
  pkill "-${sig}" -f 'soarm100_vision.*wrist_handeye_calibrator' 2>/dev/null || true
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_wrist_handeye.sh" 2>/dev/null || true
  pkill "-${sig}" -f "$ROOT_DIR/ros2/run_wrist_camera.sh" 2>/dev/null || true
  pkill "-${sig}" -f 'v4l2_camera_node.*wrist_camera|__node:=wrist_camera' 2>/dev/null || true
  pkill "-${sig}" -f 'v4l2_camera_node' 2>/dev/null || true
}

count_handeye_leftovers() {
  pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|$ROOT_DIR/ros2/run_hardware_controller.sh|hardware_controller.launch.py|hardware_controller_node|__node:=hardware_controller|__node:=hardware_robot_state_publisher|wrist_handeye_pose_sequence_node|wrist_handeye_calibrator_node|$ROOT_DIR/ros2/run_wrist_handeye.sh|$ROOT_DIR/ros2/run_wrist_camera.sh|__node:=wrist_camera" \
    2>/dev/null | grep -v -E 'cursorsandbox|run_wrist_handeye_all\.sh|grep|pgrep' || true
}

stop_handeye_stack() {
  local reason="${1:-cleanup}"
  echo "[handeye_all] stopping stack ($reason)"

  # Prefer a clean torque-off while the ROS service may still be alive.
  if command -v ros2 >/dev/null 2>&1; then
    timeout 8s ros2 service call /hardware/set_torque \
      soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" \
      >/tmp/handeye_disable_torque.log 2>&1 || true
    if [[ -s /tmp/handeye_disable_torque.log ]]; then
      cat /tmp/handeye_disable_torque.log
    fi
  fi

  # First: tracked session leaders started by this script.
  local pid
  for pid in "${PIDS[@]:-}"; do
    kill_tree "$pid" TERM
  done
  sleep 0.5

  # Second: pattern-based TERM for orphans / previous runs.
  # The Feetech driver is started with start_new_session=True, so it must be
  # matched explicitly; killing only the ROS node is not enough.
  kill_handeye_patterns TERM
  sleep 1

  for pid in "${PIDS[@]:-}"; do
    kill_tree "$pid" KILL
    if [[ -n "$pid" ]]; then
      wait "$pid" 2>/dev/null || true
    fi
  done
  kill_handeye_patterns KILL
  sleep 0.5

  # Final hardware torque-off even if ROS services already disappeared.
  if [[ -e "$SERIAL_PORT" ]] && command -v conda >/dev/null 2>&1; then
    conda run --no-capture-output -n lerobot python \
      "$ROOT_DIR/hardware/tools/disable_all_torque.py" \
      --port "$SERIAL_PORT" --confirm DISABLE_ALL_TORQUE \
      >/tmp/handeye_disable_torque_fallback.log 2>&1 || true
    if [[ -s /tmp/handeye_disable_torque_fallback.log ]]; then
      cat /tmp/handeye_disable_torque_fallback.log
    fi
  fi

  local leftovers
  leftovers="$(count_handeye_leftovers)"
  if [[ -n "$leftovers" ]]; then
    echo "[handeye_all] WARNING: leftover processes after $reason:" >&2
    echo "$leftovers" >&2
    echo "[handeye_all] If these persist across users/privileges, run: sudo pkill -9 -f hardware_controller" >&2
  else
    echo "[handeye_all] stack stopped; no matching leftovers."
  fi
  PIDS=()
}

cleanup() {
  trap - EXIT INT TERM
  stop_handeye_stack "script exit"
}
trap cleanup EXIT INT TERM

mkdir -p "$ROOT_DIR/log/runtime/hardware"
source_relaxed /opt/ros/humble/setup.bash
source_relaxed "$ROS_WS/install/setup.bash"

# Always clear previous zombies before touching the serial port.
stop_handeye_stack "pre-start"
if [[ -e "$SERIAL_PORT" ]] && fuser "$SERIAL_PORT" >/dev/null 2>&1; then
  echo "[handeye_all] serial port still busy after pre-start cleanup:" >&2
  fuser -v "$SERIAL_PORT" || true
  echo "[handeye_all] refusing to start with an occupied serial port" >&2
  exit 1
fi

if [[ ! -r "$SERIAL_PORT" || ! -w "$SERIAL_PORT" ]]; then
  echo "[handeye_all] serial port $SERIAL_PORT is not readable/writable" >&2
  exit 1
fi

echo "[handeye_all] Starting wrist camera and Viewer; robot remains unpowered."

# Start each helper in its own session so quit can kill the whole tree.
setsid "$ROOT_DIR/ros2/run_wrist_camera.sh" \
  >"$ROOT_DIR/log/runtime/hardware/handeye_camera.log" 2>&1 &
PIDS+=("$!")
sleep 3

setsid "$ROOT_DIR/ros2/run_wrist_handeye.sh" \
  >"$ROOT_DIR/log/runtime/hardware/handeye_viewer.log" 2>&1 &
PIDS+=("$!")
sleep 3

echo "[handeye_all] Viewer should now be visible."
echo "[handeye_all] Manually place the robot in the desired unpowered pose."
echo "[handeye_all] Confirm the checkerboard is visible, then press SPACE in this terminal to power on."
# IFS= is required here: without it Bash strips the space as whitespace.
IFS= read -r -n 1 -s POWER_KEY
printf '\n'
if [[ "$POWER_KEY" != " " ]]; then
  echo "[handeye_all] Aborted: expected SPACE, received a different key."
  exit 1
fi

setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" \
  >"$ROOT_DIR/log/runtime/hardware/handeye_controller.log" 2>&1 &
PIDS+=("$!")
sleep 4

echo "[handeye_all] SPACE accepted; controller is powering and holding the manual pose."
echo "[handeye_all] Only this terminal requires input."

ros2 run soarm100_vision wrist_handeye_pose_sequence_node --ros-args \
  -p repo_root:="$ROOT_DIR" \
  -p pose_file:=hardware/calibration/handeye/wrist_handeye_poses.json \
  -p seed_pose_file:=hardware/calibration/handeye/calibration_seed_pose.json \
  -p seed_mode:=live \
  -p live_auto_approve:=true \
  -p move_duration:=4.0
RC=$?
echo "[handeye_all] pose sequence exited rc=$RC; cleaning up controller/camera/viewer."
exit "$RC"
