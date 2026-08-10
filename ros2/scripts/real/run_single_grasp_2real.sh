#!/usr/bin/env bash
# One-shot real grasp: Orbbec -> fixed YOLO(jpgCat) -> SAM -> AnyGrasp -> policy.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS2_WS="$ROOT_DIR/ros2"
PORT="/dev/ttyACM0"
TARGET_CLASS="jpgCat"
YOLO_CONF="0.01"
VISION_ENV="vision_seg"
DEVICE="0"
DEVICE_PARAM=""
SHOW_WINDOW="true"
MAX_TRACKING_ERROR_RAD="0.25"
BUILD="false"
CONFIRM=""
PIDS=()
TORQUE_ACTIVE="false"
RUN_STARTED_AT="$(date +%s)"

usage() {
  cat <<'EOF'
Usage: ./ros2/scripts/real/run_single_grasp_2real.sh [options]

Options:
  --build                    Build ROS2 packages first.
  --port DEVICE              Feetech serial port. Default: /dev/ttyACM0.
  --class NAME               Fixed detector class. Default: jpgCat.
  --conf SCORE               YOLO confidence threshold. Default: 0.01.
  --device DEVICE            YOLO/SAM CUDA device. Default: 0.
  --show-window on|off       Show YOLO+SAM mask preview. Default: on.
  --max-tracking-error-rad R Maximum policy-reference error per joint.
                             Default: 0.25 rad.
  --confirm RUN_SINGLE_GRASP Required physical-motion confirmation.

This v1 always uses real camera extrinsics, one AnyGrasp plan, no wrist
tracking, no replan and no SDF-CBF avoidance.
EOF
}

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

parse_bool() {
  case "$1" in
    on|true|1) printf true ;;
    off|false|0) printf false ;;
    *) echo "[ERROR] expected on/off, got: $1" >&2; exit 2 ;;
  esac
}

print_failure_summary() {
  "$HOME/miniconda3/envs/$VISION_ENV/bin/python" - \
    "$ROOT_DIR" "$RUN_STARTED_AT" <<'PY'
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
started = float(sys.argv[2])
controller = root / "logs/hardware/real_grasp_controller.log"
nodes = root / "logs/hardware/real_grasp_nodes.log"

if controller.is_file():
    rejected = [
        line.strip() for line in controller.read_text(errors="replace").splitlines()
        if "stream target rejected:" in line
    ]
    if rejected:
        detail = rejected[-1].split("stream target rejected:", 1)[-1].strip()
        print("[2real_grasp] FAILED_STAGE=MOVE_TO_PREGRASP")
        print(f"[2real_grasp] FAILURE_CAUSE=HARDWARE_TARGET_REJECTED detail={detail}")
        raise SystemExit

logs = sorted(
    (root / "logs/hardware/real_single_grasp").glob("policy_*.jsonl"),
    key=lambda path: path.stat().st_mtime,
    reverse=True,
)
logs = [path for path in logs if path.stat().st_mtime >= started - 1.0]
if logs:
    path = logs[0]
    terminal = None
    for line in path.read_text(errors="replace").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("event") == "status":
            terminal = row
    stage = path.stem.removeprefix("policy_").split("_20", 1)[0].upper()
    print(f"[2real_grasp] FAILED_STAGE={stage}")
    if terminal:
        status = terminal.get("status", "UNKNOWN")
        pos_mm = 1000.0 * float(terminal.get("pos_err_m", float("nan")))
        ori_deg = float(terminal.get("orientation_err_deg", float("nan")))
        print(
            f"[2real_grasp] FAILURE_CAUSE={status} "
            f"position_error={pos_mm:.1f}mm orientation_error={ori_deg:.1f}deg"
        )
    else:
        print("[2real_grasp] FAILURE_CAUSE=NO_POLICY_TERMINAL_STATUS")
    raise SystemExit

if nodes.is_file():
    failed = [
        line.strip() for line in nodes.read_text(errors="replace").splitlines()
        if "PLANNING_FAILED" in line or "plan_failed:" in line
    ]
    if failed:
        print("[2real_grasp] FAILED_STAGE=PLANNING_GRASP")
        print("[2real_grasp] FAILURE_CAUSE=NO_FEASIBLE_CANDIDATE")
        raise SystemExit

print("[2real_grasp] FAILED_STAGE=UNKNOWN")
print("[2real_grasp] FAILURE_CAUSE=SEE_COMPONENT_LOGS")
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) BUILD="true"; shift ;;
    --port) PORT="$2"; shift 2 ;;
    --class) TARGET_CLASS="$2"; shift 2 ;;
    --conf) YOLO_CONF="$2"; shift 2 ;;
    --device) DEVICE="$2"; shift 2 ;;
    --show-window) SHOW_WINDOW="$(parse_bool "$2")"; shift 2 ;;
    --max-tracking-error-rad) MAX_TRACKING_ERROR_RAD="$2"; shift 2 ;;
    --confirm) CONFIRM="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ "$CONFIRM" != "RUN_SINGLE_GRASP" ]]; then
  echo "[ERROR] pass --confirm RUN_SINGLE_GRASP after clearing the workspace" >&2
  exit 2
fi
if [[ "$DEVICE" =~ ^[0-9]+$ ]]; then
  DEVICE_PARAM="cuda:$DEVICE"
else
  DEVICE_PARAM="$DEVICE"
fi
if [[ ! -r "$PORT" || ! -w "$PORT" ]]; then
  echo "[ERROR] serial port is not readable/writable: $PORT" >&2
  exit 1
fi
if fuser "$PORT" >/dev/null 2>&1; then
  echo "[ERROR] serial port is occupied:" >&2
  fuser -v "$PORT" >&2 || true
  exit 1
fi

cleanup() {
  trap - EXIT INT TERM
  echo "[2real_grasp] stopping; requesting verified torque-off"
  # Also covers failures after the controller powers the arm but before the
  # complete-stack readiness gate has passed.
  timeout 8s ros2 service call /hardware/set_torque \
    soarm100_interfaces/srv/SetHardwareTorque \
    "{enabled: false, confirmation: SET_HARDWARE_TORQUE}" >/dev/null 2>&1 || true
  for ((i=${#PIDS[@]}-1; i>=0; i--)); do
    pid="${PIDS[$i]}"
    if kill -0 "$pid" 2>/dev/null; then
      kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    fi
  done
  sleep 1
  for pid in "${PIDS[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill -KILL -- "-$pid" 2>/dev/null || kill -KILL "$pid" 2>/dev/null || true
    fi
    wait "$pid" 2>/dev/null || true
  done
}
trap cleanup EXIT INT TERM

source_relaxed /opt/ros/humble/setup.bash
if [[ "$BUILD" == "true" ]]; then
  (cd "$ROS2_WS" && colcon build \
    --packages-select soarm100_interfaces soarm100_vision --symlink-install)
fi
source_relaxed "$ROS2_WS/install/setup.bash"
mkdir -p "$ROOT_DIR/logs/hardware" "$ROOT_DIR/logs/ros2/real_single_grasp"
export ROS_LOG_DIR="$ROOT_DIR/logs/ros2/real_single_grasp"

echo "[2real_grasp] preflight: real_extrinsics=false(sim flag), class=$TARGET_CLASS yolo_conf=$YOLO_CONF"
echo "[2real_grasp] phase policy: one plan; tracking=off replan=off avoidance=off"
echo "[2real_grasp] joint tracking limit=$MAX_TRACKING_ERROR_RAD rad"

setsid "$ROOT_DIR/ros2/scripts/real/run_orbbec_rgbd.sh" \
  >"$ROOT_DIR/logs/hardware/real_grasp_orbbec.log" 2>&1 &
PIDS+=("$!")

# Vision and policy dependencies are both verified in vision_seg. Launch the
# source modules explicitly so behavior does not depend on generated shebangs.
setsid bash -lc "
  source /opt/ros/humble/setup.bash
  source '$ROS2_WS/install/setup.bash'
  source '$HOME/miniconda3/etc/profile.d/conda.sh'
  conda activate '$VISION_ENV'
  python '$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/target_segmenter_node.py' \
    --ros-args -r __node:=fixed_yolo_sam_segmenter \
    -p repo_root:='$ROOT_DIR' -p segmentation_mode:=fixed_yolo_sam \
    -p fixed_yolo_target_class:='$TARGET_CLASS' \
    -p fixed_yolo_conf:=$YOLO_CONF \
    -p fixed_yolo_model:='$ROOT_DIR/models/vision/yolowork_fixed_best.pt' \
    -p sam_model:='$ROOT_DIR/models/vision/mobile_sam.pt' \
    -p fixed_yolo_device:='$DEVICE_PARAM' \
    -p rgb_topic:=/camera/color/image_raw \
    -p depth_topic:=/camera/depth/image_raw \
    -p camera_info_topic:=/camera/color/camera_info \
    -p use_expanded_mask_for_target_cloud:=false &
  SEG_PID=\$!
  if [[ '$SHOW_WINDOW' == true ]]; then
    python '$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/debug_viewer_node.py' \
      --ros-args -r __node:=fixed_yolo_sam_viewer \
      -p rgb_topic:=/camera/color/image_raw -p mask_topic:=/target/mask \
      -p show_window:=true &
    VIEW_PID=\$!
    wait \$SEG_PID
    RC=\$?
    kill \$VIEW_PID 2>/dev/null || true
    wait \$VIEW_PID 2>/dev/null || true
    exit \$RC
  else
    wait \$SEG_PID
  fi
" >"$ROOT_DIR/logs/hardware/real_grasp_vision.log" 2>&1 &
VISION_PID="$!"
PIDS+=("$VISION_PID")

setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" \
  --port "$PORT" --rate 20.0 \
  --max-stream-command-delta-rad "$MAX_TRACKING_ERROR_RAD" \
  >"$ROOT_DIR/logs/hardware/real_grasp_controller.log" 2>&1 &
PIDS+=("$!")

setsid bash -lc "
  source /opt/ros/humble/setup.bash
  source '$ROS2_WS/install/setup.bash'
  source '$HOME/miniconda3/etc/profile.d/conda.sh'
  conda activate '$VISION_ENV'
  python '$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/anygrasp_planner_node.py' \
    --ros-args -r __node:=real_anygrasp_planner \
    -p repo_root:='$ROOT_DIR' -p use_sim_camera_extrinsics:=false \
    -p calib_json:=hardware/calibration/camera/real_camera_calib.json \
    -p input_camera_name:=scene_depth -p top_k:=45 \
    -p pregrasp_distance:=0.040 \
    -p grasp_approach_offset_m:=-0.040 \
    -p policy_workspace_min:="[0.08,-0.30,0.01]" \
    -p enable_ik_filter:=true -p ik_position_tolerance_m:=0.005 \
    -p ik_rotation_tolerance_deg:=3.0 \
    -p enable_hardware_limit_filter:=true \
    -p hardware_calibration_json:=hardware/calibration/lerobot/so100_plus_new_arm.json \
    -p hardware_mapping_json:=hardware/calibration/policy_joint_mapping.json \
    -p hardware_limit_margin_counts:=100 &
  PLAN_PID=\$!
  python '$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/real_policy_grasp_backend_node.py' \
    --ros-args -r __node:=real_policy_grasp_backend \
    -p repo_root:='$ROOT_DIR' \
    -p calib_json:=hardware/calibration/camera/real_camera_calib.json \
    -p python_executable:='$HOME/miniconda3/envs/$VISION_ENV/bin/python' \
    -p workspace_min_z_m:=0.010 \
    -p max_tracking_error_rad:=$MAX_TRACKING_ERROR_RAD &
  BACKEND_PID=\$!
  python '$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/grasp_orchestrator_node.py' \
    --ros-args -r __node:=real_grasp_orchestrator \
    -p max_attempts:=1 -p default_enable_avoidance:=false \
    -p wait_timeout_s:=90.0 &
  ORCH_PID=\$!
  wait -n \$PLAN_PID \$BACKEND_PID \$ORCH_PID
  RC=\$?
  kill \$PLAN_PID \$BACKEND_PID \$ORCH_PID 2>/dev/null || true
  wait \$PLAN_PID \$BACKEND_PID \$ORCH_PID 2>/dev/null || true
  exit \$RC
" >"$ROOT_DIR/logs/hardware/real_grasp_nodes.log" 2>&1 &
CORE_PID="$!"
PIDS+=("$CORE_PID")

echo "[2real_grasp] waiting for RGB-D, segmentation, hardware and actions"
for _ in $(seq 1 180); do
  if ! kill -0 "$VISION_PID" 2>/dev/null; then
    echo "[ERROR] YOLO/SAM process exited during startup" >&2
    tail -n 40 "$ROOT_DIR/logs/hardware/real_grasp_vision.log" >&2 || true
    exit 1
  fi
  if ! kill -0 "$CORE_PID" 2>/dev/null; then
    echo "[ERROR] grasp planner/backend/orchestrator process exited during startup" >&2
    tail -n 40 "$ROOT_DIR/logs/hardware/real_grasp_nodes.log" >&2 || true
    exit 1
  fi
  if ros2 topic list 2>/dev/null | grep -qx '/camera/color/image_raw' && \
     ros2 topic list 2>/dev/null | grep -qx '/camera/depth/image_raw' && \
     ros2 service list 2>/dev/null | grep -qx '/segment_target' && \
     ros2 service list 2>/dev/null | grep -qx '/hardware/set_torque' && \
     ros2 action list 2>/dev/null | grep -qx '/plan_grasp' && \
     ros2 action list 2>/dev/null | grep -qx '/execute_planned_grasp' && \
     ros2 action list 2>/dev/null | grep -qx '/execute_grasp'; then
    TORQUE_ACTIVE="true"
    break
  fi
  sleep 0.5
done
if [[ "$TORQUE_ACTIVE" != "true" ]]; then
  echo "[ERROR] stack did not become ready" >&2
  echo "  vision:     logs/hardware/real_grasp_vision.log" >&2
  echo "  controller: logs/hardware/real_grasp_controller.log" >&2
  echo "  nodes:      logs/hardware/real_grasp_nodes.log" >&2
  exit 1
fi

# Topic discovery does not prove that the camera is producing frames. Require
# one real message from each input before any physical motion begins.
echo "[2real_grasp] checking live color/depth/camera_info frames"
for topic in \
  /camera/color/image_raw \
  /camera/depth/image_raw \
  /camera/color/camera_info; do
  if ! timeout 12s ros2 topic echo "$topic" --once \
      --qos-reliability best_effort >/dev/null 2>&1; then
    echo "[ERROR] no live message received from $topic" >&2
    echo "  Orbbec log: logs/hardware/real_grasp_orbbec.log" >&2
    exit 1
  fi
done

echo "[2real_grasp] READY. Keep clear: sending one '$TARGET_CLASS' grasp goal."
set +e
ros2 run soarm100_vision send_execute_grasp \
  --target "$TARGET_CLASS" --wait-timeout 120
RESULT=$?
set -e
if [[ "$RESULT" -eq 0 ]]; then
  echo "[2real_grasp] RESULT success=true"
else
  echo "[2real_grasp] RESULT success=false rc=$RESULT"
  print_failure_summary
fi
exit "$RESULT"
