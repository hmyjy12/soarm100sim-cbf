#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS_WS="$ROOT_DIR/ros2"
PORT="/dev/ttyACM0"
LEROBOT_ENV="${LEROBOT_ENV:-lerobot}"
CALIBRATION="hardware/calibration/lerobot/so100_plus_new_arm.json"
MAPPING="hardware/calibration/policy_joint_mapping.json"
CONTROLLER_SAFE_POSE="hardware/calibration/policy_ready_static_cbf.json"
OUTPUT="hardware/calibration/policy_ready_static_cbf.json"
CONFIRM=""
CONTROLLER_PID=""
CONTROLLER_STARTED="false"
LOG_DIR="$ROOT_DIR/log/runtime/hardware"
CONTROLLER_LOG="$LOG_DIR/capture_policy_ready_controller.log"

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

absolute_path() {
  if [[ "$1" = /* ]]; then printf '%s\n' "$1"; else printf '%s/%s\n' "$ROOT_DIR" "$1"; fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      cat <<'EOF'
Usage: capture_policy_ready_pose.sh [options]

  --port PATH
  --calibration JSON
  --mapping JSON
  --controller-safe-pose JSON
  --output JSON
  --lerobot-env NAME
  --confirm CAPTURE_POLICY_READY_POSE
EOF
      exit 0
      ;;
    --port) PORT="$2"; shift 2 ;;
    --lerobot-env) LEROBOT_ENV="$2"; shift 2 ;;
    --calibration) CALIBRATION="$2"; shift 2 ;;
    --mapping) MAPPING="$2"; shift 2 ;;
    --controller-safe-pose) CONTROLLER_SAFE_POSE="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --confirm) CONFIRM="$2"; shift 2 ;;
    *) echo "[ERROR] unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ "$CONFIRM" != "CAPTURE_POLICY_READY_POSE" ]]; then
  echo "[ERROR] --confirm must be exactly CAPTURE_POLICY_READY_POSE" >&2
  exit 2
fi

CALIBRATION="$(absolute_path "$CALIBRATION")"
MAPPING="$(absolute_path "$MAPPING")"
CONTROLLER_SAFE_POSE="$(absolute_path "$CONTROLLER_SAFE_POSE")"
OUTPUT="$(absolute_path "$OUTPUT")"
CANDIDATE="${OUTPUT%.json}.candidate.json"

kill_controller_tree() {
  local sig="$1"
  if [[ -n "$CONTROLLER_PID" ]] && kill -0 "$CONTROLLER_PID" 2>/dev/null; then
    kill "-$sig" -- "-$CONTROLLER_PID" 2>/dev/null || true
    kill "-$sig" "$CONTROLLER_PID" 2>/dev/null || true
  fi
  pkill "-$sig" -f "$ROOT_DIR/hardware/tools/run_hardware_controller.py" 2>/dev/null || true
  pkill "-$sig" -f "$ROOT_DIR/ros2/run_hardware_controller.sh" 2>/dev/null || true
  pkill "-$sig" -f 'ros2 launch soarm100_vision hardware_controller.launch.py' 2>/dev/null || true
  pkill "-$sig" -f '__node:=hardware_controller' 2>/dev/null || true
  pkill "-$sig" -f '__node:=hardware_robot_state_publisher' 2>/dev/null || true
}

cleanup() {
  local rc=$?
  trap - EXIT INT TERM
  set +e
  echo "[ready_pose] cleaning up; requesting verified torque-off."
  if [[ "$CONTROLLER_STARTED" == "true" ]]; then
    timeout 6s ros2 service call /hardware/set_torque \
      soarm100_interfaces/srv/SetHardwareTorque \
      "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" >/dev/null 2>&1
    kill_controller_tree TERM
    sleep 1
    kill_controller_tree KILL
    [[ -n "$CONTROLLER_PID" ]] && wait "$CONTROLLER_PID" 2>/dev/null
  fi
  if [[ -e "$PORT" ]] && ! fuser "$PORT" >/dev/null 2>&1; then
    conda run --no-capture-output -n "$LEROBOT_ENV" python \
      "$ROOT_DIR/hardware/tools/disable_all_torque.py" \
      --port "$PORT" --calibration "$CALIBRATION" \
      --confirm DISABLE_ALL_TORQUE || true
  fi
  if fuser "$PORT" >/dev/null 2>&1; then
    echo "[ready_pose] WARNING: serial port remains occupied:" >&2
    fuser -v "$PORT" >&2 || true
  else
    echo "[ready_pose] cleanup complete; serial port is free and torque is off."
  fi
  exit "$rc"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p "$LOG_DIR" "$(dirname "$OUTPUT")"
source_relaxed /opt/ros/humble/setup.bash
source_relaxed "$ROS_WS/install/setup.bash"

if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi
if fuser "$PORT" >/dev/null 2>&1; then
  echo "[ERROR] serial port is occupied; stop the existing owner first:" >&2
  fuser -v "$PORT" >&2 || true
  exit 1
fi
if pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|$ROOT_DIR/ros2/run_hardware_controller.sh|__node:=hardware_controller" \
  | grep -v -E 'capture_policy_ready_pose|pgrep|grep' >/dev/null 2>&1; then
  echo "[ERROR] a residual hardware controller process exists; refusing to start." >&2
  pgrep -af "$ROOT_DIR/hardware/tools/run_hardware_controller.py|$ROOT_DIR/ros2/run_hardware_controller.sh|__node:=hardware_controller" >&2 || true
  exit 1
fi

conda run --no-capture-output -n "$LEROBOT_ENV" python \
  "$ROOT_DIR/hardware/tools/disable_all_torque.py" \
  --port "$PORT" --calibration "$CALIBRATION" \
  --confirm DISABLE_ALL_TORQUE

echo "[ready_pose] Robot torque is OFF. Manually place all seven joints in the desired ready pose."
echo "[ready_pose] Check table clearance, wrist cable slack and camera clearance."
echo "[ready_pose] Press SPACE to capture this pose; press any other key to abort."
IFS= read -r -n 1 -s CAPTURE_KEY
printf '\n'
if [[ "$CAPTURE_KEY" != " " ]]; then
  echo "[ready_pose] aborted before capture."
  exit 1
fi

conda run --no-capture-output -n "$LEROBOT_ENV" python \
  "$ROOT_DIR/hardware/tools/capture_safe_pose.py" \
  --port "$PORT" --calibration "$CALIBRATION" --mapping "$MAPPING" \
  --output "$CANDIDATE"

: >"$CONTROLLER_LOG"
setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" \
  --port "$PORT" --lerobot-env "$LEROBOT_ENV" \
  --calibration "$CALIBRATION" --safe-pose "$CONTROLLER_SAFE_POSE" \
  >"$CONTROLLER_LOG" 2>&1 &
CONTROLLER_PID="$!"
CONTROLLER_STARTED="true"

READY="false"
for _ in $(seq 1 30); do
  if grep -q 'hardware controller ready' "$CONTROLLER_LOG"; then READY="true"; break; fi
  if ! kill -0 "$CONTROLLER_PID" 2>/dev/null; then break; fi
  sleep 0.5
done
if [[ "$READY" != "true" ]]; then
  echo "[ERROR] controller did not power and hold the captured pose:" >&2
  tail -n 80 "$CONTROLLER_LOG" >&2 || true
  exit 1
fi

echo "[ready_pose] Captured pose is now POWERED and HELD; release your hands carefully."
echo "[ready_pose] Visually inspect stability, table clearance, cable slack and camera clearance."
echo "[ready_pose] Type APPROVE to save it, or q to reject it:"
IFS= read -r APPROVAL
if [[ "$APPROVAL" != "APPROVE" ]]; then
  echo "[ready_pose] candidate rejected; formal ready-pose file was not changed."
  exit 1
fi

conda run --no-capture-output -n "$LEROBOT_ENV" python \
  "$ROOT_DIR/hardware/tools/approve_policy_ready_pose.py" \
  --candidate "$CANDIDATE" --output "$OUTPUT" \
  --confirm APPROVE_POLICY_READY_POSE

echo "[ready_pose] APPROVED: $OUTPUT"
echo "[ready_pose] Use with: --policy-ready-pose $OUTPUT"
