#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
VISION_ENV="vision_seg"
PORT="/dev/ttyACM0"
BUILD_FIRST="false"
CONFIRM=""
HOLD_SECONDS="1.0"
CONTROLLER_PID=""
POLICY_PID=""
TAIL_PID=""

# Three conservative base-frame TCP poses. Orientation is held constant.
POSE_NAMES=("center" "left_high" "right_mid")
POSE_POSITIONS=(
  "0.350,0.020,0.260"
  "0.340,0.060,0.280"
  "0.365,-0.020,0.265"
)
POSE_QUATERNION="0.359634,0.737692,0.238924,0.519027"

source_relaxed() {
  set +u
  source "$1"
  set -u
}

stop_group() {
  local pid="${1:-}"
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    kill -TERM "-$pid" 2>/dev/null || true
    for _ in $(seq 1 30); do
      kill -0 "$pid" 2>/dev/null || return 0
      sleep 0.1
    done
    kill -KILL "-$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
  fi
}

cleanup() {
  local code=$?
  trap - EXIT INT TERM
  if [[ -n "$TAIL_PID" ]]; then
    kill "$TAIL_PID" 2>/dev/null || true
    wait "$TAIL_PID" 2>/dev/null || true
  fi
  stop_group "$POLICY_PID"
  if [[ -n "$CONTROLLER_PID" ]] && kill -0 "$CONTROLLER_PID" 2>/dev/null; then
    source_relaxed /opt/ros/humble/setup.bash
    source_relaxed "$ROS_WS/install/setup.bash"
    timeout 3 ros2 service call /hardware/set_torque soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" >/dev/null 2>&1 || true
    stop_group "$CONTROLLER_PID"
  fi
  exit "$code"
}
trap cleanup EXIT INT TERM

show_residuals() {
  local found="false"
  local serial_pids process_matches nodes services

  serial_pids="$(fuser "$PORT" 2>/dev/null || true)"
  if [[ -n "$serial_pids" ]]; then
    found="true"
    echo "[preflight] serial port is occupied: $PORT" >&2
    fuser -v "$PORT" >&2 || true
    ps -fp $serial_pids >&2 || true
  else
    echo "[preflight] serial port is free: $PORT"
  fi

  process_matches="$(pgrep -af 'run_hardware_controller.py|hardware_controller_node|policy_reach_node.py' || true)"
  if [[ -n "$process_matches" ]]; then
    found="true"
    echo "[preflight] residual controller/policy process found:" >&2
    echo "$process_matches" >&2
  else
    echo "[preflight] no residual controller/policy process"
  fi

  nodes="$(ros2 node list 2>/dev/null || true)"
  if grep -Eq '^/(hardware_controller|so100_plus_hardware_controller|so100_plus_policy_reach)$' <<<"$nodes"; then
    found="true"
    echo "[preflight] residual ROS2 node found:" >&2
    grep -E '^/(hardware_controller|so100_plus_hardware_controller|so100_plus_policy_reach)$' <<<"$nodes" >&2
  else
    echo "[preflight] no residual hardware/policy ROS2 node"
  fi

  services="$(ros2 service list 2>/dev/null || true)"
  if grep -Eq '^/hardware/(set_torque|move_joint_target)$' <<<"$services"; then
    found="true"
    echo "[preflight] residual hardware ROS2 service found:" >&2
    grep '^/hardware/' <<<"$services" >&2 || true
  else
    echo "[preflight] no residual hardware ROS2 service"
  fi

  [[ "$found" == "false" ]]
}

write_target_config() {
  local path="$1"
  local position="$2"
  local px py pz qw qx qy qz
  IFS=',' read -r px py pz <<<"$position"
  IFS=',' read -r qw qx qy qz <<<"$POSE_QUATERNION"
  printf '{\n  "frame_id": "base",\n  "position_m": [%s, %s, %s],\n  "quaternion_wxyz": [%s, %s, %s, %s]\n}\n' \
    "$px" "$py" "$pz" "$qw" "$qx" "$qy" "$qz" >"$path"
}

run_pose() {
  local index="$1"
  local run_dir="$2"
  local name="${POSE_NAMES[$index]}"
  local position="${POSE_POSITIONS[$index]}"
  local target_file="$run_dir/target_$((index + 1))_${name}.json"
  local console_log="$run_dir/policy_$((index + 1))_${name}.log"
  local trajectory_log="$run_dir/trajectory_$((index + 1))_${name}.jsonl"
  local terminal_line=""

  write_target_config "$target_file" "$position"
  echo "[three_pose] target $((index + 1))/3 name=$name position=($position)"

  setsid conda run --no-capture-output -n "$VISION_ENV" python \
    "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/policy_reach_node.py" \
    --ros-args \
    -p repo_root:="$ROOT_DIR" \
    -p target_config:="$target_file" \
    -p log_path:="$trajectory_log" \
    -p joint_state_timeout_s:=1.5 \
    -p start_on_launch:=true >"$console_log" 2>&1 &
  POLICY_PID=$!
  tail -n +1 -F "$console_log" &
  TAIL_PID=$!

  for _ in $(seq 1 150); do
    terminal_line="$(rg 'policy reach stopped:' "$console_log" | tail -n 1 || true)"
    if [[ -n "$terminal_line" ]]; then
      break
    fi
    if ! kill -0 "$POLICY_PID" 2>/dev/null; then
      break
    fi
    sleep 0.2
  done

  if [[ "$terminal_line" != *"SUCCESS"* ]]; then
    echo "[three_pose] target $((index + 1)) failed; stopping sequence." >&2
    [[ -n "$terminal_line" ]] && echo "$terminal_line" >&2
    stop_group "$POLICY_PID"
    POLICY_PID=""
    kill "$TAIL_PID" 2>/dev/null || true
    wait "$TAIL_PID" 2>/dev/null || true
    TAIL_PID=""
    return 1
  fi

  echo "[three_pose] target $((index + 1)) reached; holding ${HOLD_SECONDS}s"
  sleep "$HOLD_SECONDS"
  stop_group "$POLICY_PID"
  POLICY_PID=""
  kill "$TAIL_PID" 2>/dev/null || true
  wait "$TAIL_PID" 2>/dev/null || true
  TAIL_PID=""
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) BUILD_FIRST="true"; shift ;;
    --port) PORT="$2"; shift 2 ;;
    --vision-env) VISION_ENV="$2"; shift 2 ;;
    --hold-seconds) HOLD_SECONDS="$2"; shift 2 ;;
    --confirm) CONFIRM="$2"; shift 2 ;;
    *) echo "[ERROR] unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ "$CONFIRM" != "RUN_POLICY_REACH_THREE_POSE" ]]; then
  echo "[ERROR] this moves the real arm. Add --confirm RUN_POLICY_REACH_THREE_POSE" >&2
  exit 2
fi
if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi

source_relaxed /opt/ros/humble/setup.bash
if [[ "$BUILD_FIRST" == "true" ]]; then
  (cd "$ROS_WS" && colcon build --packages-select soarm100_interfaces soarm100_vision --symlink-install)
fi
source_relaxed "$ROS_WS/install/setup.bash"

if ! show_residuals; then
  echo "[ERROR] preflight failed. Stop the reported process/node before retrying." >&2
  exit 1
fi

RUN_DIR="$ROOT_DIR/log/runtime/hardware/policy_three_pose_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RUN_DIR"
echo "[three_pose] logs: $RUN_DIR"

setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" --port "$PORT" \
  >"$RUN_DIR/controller.log" 2>&1 &
CONTROLLER_PID=$!

for _ in $(seq 1 100); do
  kill -0 "$CONTROLLER_PID" 2>/dev/null || {
    echo "[ERROR] hardware controller exited during startup" >&2
    tail -n 80 "$RUN_DIR/controller.log" >&2 || true
    exit 1
  }
  ros2 service list 2>/dev/null | grep -qx /hardware/set_torque && break
  sleep 0.1
done
ros2 service list 2>/dev/null | grep -qx /hardware/set_torque || {
  echo "[ERROR] hardware controller did not become ready" >&2
  exit 1
}

for index in 0 1 2; do
  run_pose "$index" "$RUN_DIR"
done

echo "[three_pose] all three targets completed; cleanup will disable all torque."
