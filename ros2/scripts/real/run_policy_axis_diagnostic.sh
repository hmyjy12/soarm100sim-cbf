#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
VISION_ENV="vision_seg"
PORT="/dev/ttyACM0"
RATE="20.0"
STEP_M="0.02"
HOLD_SECONDS="1.0"
SUCCESS_POSITION_M="0.010"
MAX_TRACKING_ERROR_RAD="0.25"
BUILD_FIRST="false"
CONFIRM=""
CONTROLLER_PID=""
POLICY_PID=""
TAIL_PID=""

NAMES=(plus_x minus_x plus_y minus_y plus_z minus_z)
DELTAS=(
  "${STEP_M},0,0" "-${STEP_M},0,0"
  "0,${STEP_M},0" "0,-${STEP_M},0"
  "0,0,${STEP_M}" "0,0,-${STEP_M}"
)

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
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
    timeout 4 ros2 service call /hardware/set_torque \
      soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" \
      >/dev/null 2>&1 || true
    stop_group "$CONTROLLER_PID"
  fi
  exit "$code"
}
trap cleanup EXIT INT TERM

usage() {
  cat <<'EOF'
Usage: ./ros2/scripts/real/run_policy_axis_diagnostic.sh [options]

Runs +X/-X/+Y/-Y/+Z/-Z relative TCP reaches while one hardware controller
keeps all seven joints powered. Every leg holds for one second by default.

Options:
  --build                         Build ROS2 packages first.
  --port DEVICE                   Serial device. Default: /dev/ttyACM0.
  --vision-env NAME               Policy conda environment. Default: vision_seg.
  --rate HZ                       Feedback/policy/driver rate. Default: 20.
  --step-m METERS                 Per-axis displacement, (0, 0.03]. Default: 0.02.
  --hold-seconds SECONDS          Powered hold after each success. Default: 1.0.
  --success-position-m METERS     Success tolerance. Default: 0.010.
  --max-tracking-error-rad RAD    Driver tracking limit. Default: 0.25.
  --confirm RUN_POLICY_AXIS_DIAGNOSTIC
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) BUILD_FIRST="true"; shift ;;
    --port) PORT="$2"; shift 2 ;;
    --vision-env) VISION_ENV="$2"; shift 2 ;;
    --rate) RATE="$2"; shift 2 ;;
    --step-m) STEP_M="$2"; shift 2 ;;
    --hold-seconds) HOLD_SECONDS="$2"; shift 2 ;;
    --success-position-m) SUCCESS_POSITION_M="$2"; shift 2 ;;
    --max-tracking-error-rad) MAX_TRACKING_ERROR_RAD="$2"; shift 2 ;;
    --confirm) CONFIRM="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ "$CONFIRM" != "RUN_POLICY_AXIS_DIAGNOSTIC" ]]; then
  echo "[ERROR] this moves the real arm. Add --confirm RUN_POLICY_AXIS_DIAGNOSTIC" >&2
  exit 2
fi
if ! awk -v v="$STEP_M" 'BEGIN { exit !(v > 0 && v <= 0.03) }'; then
  echo "[ERROR] --step-m must be within (0, 0.03] m" >&2
  exit 2
fi
if ! awk -v v="$SUCCESS_POSITION_M" 'BEGIN { exit !(v >= 0.005 && v <= 0.015) }'; then
  echo "[ERROR] --success-position-m must be within [0.005, 0.015] m" >&2
  exit 2
fi
if ! awk -v v="$RATE" 'BEGIN { exit !(v >= 5 && v <= 30) }'; then
  echo "[ERROR] --rate must be within [5, 30] Hz" >&2
  exit 2
fi
printf -v RATE_PARAM "%.6f" "$RATE"
printf -v SUCCESS_POSITION_PARAM "%.6f" "$SUCCESS_POSITION_M"
printf -v MAX_TRACKING_ERROR_PARAM "%.6f" "$MAX_TRACKING_ERROR_RAD"
if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi
if fuser "$PORT" >/dev/null 2>&1; then
  echo "[ERROR] serial port is already occupied:" >&2
  fuser -v "$PORT" >&2 || true
  exit 1
fi

# Rebuild deltas after argument parsing so --step-m is honored.
DELTAS=(
  "${STEP_M},0,0" "-${STEP_M},0,0"
  "0,${STEP_M},0" "0,-${STEP_M},0"
  "0,0,${STEP_M}" "0,0,-${STEP_M}"
)

source_relaxed /opt/ros/humble/setup.bash
if [[ "$BUILD_FIRST" == "true" ]]; then
  (cd "$ROS_WS" && colcon build \
    --packages-select soarm100_interfaces soarm100_vision --symlink-install)
fi
source_relaxed "$ROS_WS/install/setup.bash"

if pgrep -af 'run_hardware_controller.py|hardware_controller_node|policy_reach_node.py' \
  >/tmp/soarm100_axis_diag_processes 2>/dev/null; then
  echo "[ERROR] residual hardware/policy process detected:" >&2
  cat /tmp/soarm100_axis_diag_processes >&2
  exit 1
fi

RUN_DIR="$ROOT_DIR/logs/hardware/policy_axis_diagnostic_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RUN_DIR"
echo "[axis_diag] logs=$RUN_DIR"
echo "[axis_diag] sequence=+X,-X,+Y,-Y,+Z,-Z step=${STEP_M}m hold=${HOLD_SECONDS}s"
echo "[axis_diag] rate=${RATE_PARAM}Hz success_position=${SUCCESS_POSITION_PARAM}m; torque remains on between legs"

setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" \
  --port "$PORT" --rate "$RATE_PARAM" \
  --max-stream-command-delta-rad "$MAX_TRACKING_ERROR_PARAM" \
  --raw-margin-counts 0 \
  >"$RUN_DIR/controller.log" 2>&1 &
CONTROLLER_PID=$!

for _ in $(seq 1 150); do
  kill -0 "$CONTROLLER_PID" 2>/dev/null || {
    echo "[ERROR] hardware controller exited during startup" >&2
    tail -n 50 "$RUN_DIR/controller.log" >&2 || true
    exit 1
  }
  grep -q 'hardware controller ready' "$RUN_DIR/controller.log" && break
  sleep 0.1
done
if ! grep -q 'hardware controller ready' "$RUN_DIR/controller.log"; then
  echo "[ERROR] hardware controller did not become ready" >&2
  tail -n 50 "$RUN_DIR/controller.log" >&2 || true
  exit 1
fi

for index in "${!NAMES[@]}"; do
  name="${NAMES[$index]}"
  delta="${DELTAS[$index]}"
  target="$RUN_DIR/target_$((index + 1))_${name}.json"
  console="$RUN_DIR/policy_$((index + 1))_${name}.log"
  trajectory="$RUN_DIR/trajectory_$((index + 1))_${name}.jsonl"

  echo "[axis_diag] leg $((index + 1))/6 name=$name delta=($delta)"
  conda run --no-capture-output -n "$VISION_ENV" python \
    "$ROOT_DIR/ros2/scripts/real/make_relative_policy_reach_target.py" \
    --repo-root "$ROOT_DIR" --output "$target" --delta-m="$delta" \
    --max-delta-norm-m 0.04

  setsid conda run --no-capture-output -n "$VISION_ENV" python \
    "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/policy_reach_node.py" \
    --ros-args \
    -p repo_root:="$ROOT_DIR" \
    -p target_config:="$target" \
    -p log_path:="$trajectory" \
    -p control_rate_hz:="$RATE_PARAM" \
    -p max_tracking_error_rad:="$MAX_TRACKING_ERROR_PARAM" \
    -p success_position_m:="$SUCCESS_POSITION_PARAM" \
    -p enable_joint_limit_cbf:=false \
    -p start_on_launch:=true >"$console" 2>&1 &
  POLICY_PID=$!
  tail -n +1 -F "$console" &
  TAIL_PID=$!

  terminal_line=""
  for _ in $(seq 1 150); do
    terminal_line="$(rg 'policy reach stopped:' "$console" | tail -n 1 || true)"
    [[ -n "$terminal_line" ]] && break
    kill -0 "$POLICY_PID" 2>/dev/null || break
    sleep 0.2
  done

  kill "$TAIL_PID" 2>/dev/null || true
  wait "$TAIL_PID" 2>/dev/null || true
  TAIL_PID=""
  stop_group "$POLICY_PID"
  POLICY_PID=""

  if [[ "$terminal_line" != *"SUCCESS"* ]]; then
    echo "[axis_diag] FAILED leg=$name ${terminal_line:-NO_TERMINAL_STATUS}" >&2
    exit 1
  fi
  echo "[axis_diag] PASSED leg=$name; powered hold ${HOLD_SECONDS}s"
  sleep "$HOLD_SECONDS"
done

echo "[axis_diag] COMPLETE all six legs passed; cleanup will disable all torque"
