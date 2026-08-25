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
OBSTACLE_PID=""
OBSTACLE_VIEWER_PID=""
TARGET_SEGMENTER_PID=""
CONTROL_RATE_HZ="20.0"
MAX_RELATIVE_DELTA_M="0.10"
MAX_TRACKING_ERROR_RAD="0.25"
LOAD_SUPPORT_MODE="off"
LOAD_SUPPORT_CONFIG="ros2/config/real/load_support.json"
POLICY_TARGET_TRACKER_MODE="off"
POLICY_TARGET_TRACKER_CONFIG="ros2/config/real/policy_target_tracker.json"
ENABLE_JOINT_LIMIT_CBF="false"
SUCCESS_POSITION_M="0.015"
SUCCESS_ORIENTATION_DEG="10.0"
MAX_JOINT_VELOCITY_RAD_S="0.20"
MAX_JOINT_ACCELERATION_RAD_S2="0.80"
POLICY_TIMEOUT_S="20.0"
HOLD_CURRENT_DURATION_S="3.0"
INITIALIZE_POLICY_POSE="true"
POLICY_READY_POSE="hardware/calibration/hardware_safe_pose_v1.json"
INIT_DURATION_S="6.0"
INIT_SETTLE_SECONDS="0.75"
INIT_TOLERANCE_RAD="0.20"
INIT_MOVE_TOLERANCE_COUNTS="80"
INIT_TRAINING_MARGIN_RAD="0.10"
ENABLE_OBSTACLE_CBF="false"
OBSTACLE_GUI="true"
RGB_TOPIC="/camera/color/image_raw"
DEPTH_TOPIC="/camera/depth/image_raw"
CAMERA_INFO_TOPIC="/camera/color/camera_info"
CAMERA_CALIB_JSON="hardware/calibration/camera/real_camera_calib.json"
TABLE_Z_MAX_M="0.055"
SELF_FILTER_MARGIN_M="0.035"
WRIST_ATTACHMENT_BOX="true"
ATTACHED_THIN_FILTER="false"
OBSTACLE_SELECTION_MODE="all-except-target"
OBSTACLE_TARGET_CLASS=""
OBSTACLE_TARGET_MODEL="models/vision/yolowork_fixed_best.pt"
OBSTACLE_TARGET_CONF="0.10"
OBSTACLE_MASK_REFRESH_HZ="2.0"
OBSTACLE_TARGET_MASK_TOLERANCE_S="3.0"
OBSTACLE_VISION_DEVICE="auto"
THIN_MAX_WIDTH_M="0.022"
THIN_MIN_LENGTH_M="0.060"
THIN_MIN_ASPECT_RATIO="4.0"
THIN_ATTACHMENT_DISTANCE_M="0.025"
THIN_MAX_ROBOT_DISTANCE_M="0.100"
OBSTACLE_CBF_D_SAFE_M="0.050"
OBSTACLE_CBF_ACTIVATE_MARGIN_M="0.040"
# The Orbbec stream occasionally pauses for about 0.8 s on this host. This
# stage uses a fixed camera and static obstacles, so retain the last cloud
# briefly while still stopping on a sustained camera outage.
OBSTACLE_CLOUD_TIMEOUT_S="3.0"
OBSTACLE_STARTUP_TIMEOUT_S="12.0"

source_relaxed() {
  set +u
  source "$1"
  set -u
}

cleanup() {
  local code=$?
  trap - EXIT INT TERM
  if [[ -n "$TARGET_SEGMENTER_PID" ]] && kill -0 "$TARGET_SEGMENTER_PID" 2>/dev/null; then
    kill -TERM "-$TARGET_SEGMENTER_PID" 2>/dev/null || true
    wait "$TARGET_SEGMENTER_PID" 2>/dev/null || true
  fi
  if [[ -n "$OBSTACLE_VIEWER_PID" ]] && kill -0 "$OBSTACLE_VIEWER_PID" 2>/dev/null; then
    kill -TERM "-$OBSTACLE_VIEWER_PID" 2>/dev/null || true
    wait "$OBSTACLE_VIEWER_PID" 2>/dev/null || true
  fi
  if [[ -n "$OBSTACLE_PID" ]] && kill -0 "$OBSTACLE_PID" 2>/dev/null; then
    kill -TERM "-$OBSTACLE_PID" 2>/dev/null || true
    wait "$OBSTACLE_PID" 2>/dev/null || true
  fi
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
    "$ROOT_DIR/log/runtime/hardware/policy_reach_controller.log" 2>/dev/null
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
    --load-support) LOAD_SUPPORT_MODE="$2"; shift 2 ;;
    --load-support-config) LOAD_SUPPORT_CONFIG="$2"; shift 2 ;;
    --policy-target-tracker) POLICY_TARGET_TRACKER_MODE="$2"; shift 2 ;;
    --policy-target-tracker-config) POLICY_TARGET_TRACKER_CONFIG="$2"; shift 2 ;;
    --joint-limit-cbf) ENABLE_JOINT_LIMIT_CBF="$2"; shift 2 ;;
    --obstacle-cbf) ENABLE_OBSTACLE_CBF="$2"; shift 2 ;;
    --obstacle-gui) OBSTACLE_GUI="$2"; shift 2 ;;
    --rgb-topic) RGB_TOPIC="$2"; shift 2 ;;
    --depth-topic) DEPTH_TOPIC="$2"; shift 2 ;;
    --camera-info-topic) CAMERA_INFO_TOPIC="$2"; shift 2 ;;
    --camera-calib-json) CAMERA_CALIB_JSON="$2"; shift 2 ;;
    --table-z-max-m) TABLE_Z_MAX_M="$2"; shift 2 ;;
    --self-filter-margin-m) SELF_FILTER_MARGIN_M="$2"; shift 2 ;;
    --wrist-attachment-box) WRIST_ATTACHMENT_BOX="$2"; shift 2 ;;
    --attached-thin-filter) ATTACHED_THIN_FILTER="$2"; shift 2 ;;
    --obstacle-selection) OBSTACLE_SELECTION_MODE="$2"; shift 2 ;;
    --obstacle-target-class) OBSTACLE_TARGET_CLASS="$2"; shift 2 ;;
    --obstacle-target-model) OBSTACLE_TARGET_MODEL="$2"; shift 2 ;;
    --obstacle-target-conf) OBSTACLE_TARGET_CONF="$2"; shift 2 ;;
    --obstacle-mask-refresh-hz) OBSTACLE_MASK_REFRESH_HZ="$2"; shift 2 ;;
    --obstacle-target-mask-tolerance-s) OBSTACLE_TARGET_MASK_TOLERANCE_S="$2"; shift 2 ;;
    --obstacle-vision-device) OBSTACLE_VISION_DEVICE="$2"; shift 2 ;;
    --thin-max-width-m) THIN_MAX_WIDTH_M="$2"; shift 2 ;;
    --thin-min-length-m) THIN_MIN_LENGTH_M="$2"; shift 2 ;;
    --thin-min-aspect-ratio) THIN_MIN_ASPECT_RATIO="$2"; shift 2 ;;
    --thin-attachment-distance-m) THIN_ATTACHMENT_DISTANCE_M="$2"; shift 2 ;;
    --thin-max-robot-distance-m) THIN_MAX_ROBOT_DISTANCE_M="$2"; shift 2 ;;
    --obstacle-safe-distance-m) OBSTACLE_CBF_D_SAFE_M="$2"; shift 2 ;;
    --obstacle-activate-margin-m) OBSTACLE_CBF_ACTIVATE_MARGIN_M="$2"; shift 2 ;;
    --obstacle-cloud-timeout-s) OBSTACLE_CLOUD_TIMEOUT_S="$2"; shift 2 ;;
    --obstacle-startup-timeout-s) OBSTACLE_STARTUP_TIMEOUT_S="$2"; shift 2 ;;
    --max-joint-velocity-rad-s) MAX_JOINT_VELOCITY_RAD_S="$2"; shift 2 ;;
    --max-joint-acceleration-rad-s2) MAX_JOINT_ACCELERATION_RAD_S2="$2"; shift 2 ;;
    --timeout-s) POLICY_TIMEOUT_S="$2"; shift 2 ;;
    --hold-current-duration-s) HOLD_CURRENT_DURATION_S="$2"; shift 2 ;;
    --initialize-policy-pose) INITIALIZE_POLICY_POSE="$2"; shift 2 ;;
    --policy-ready-pose) POLICY_READY_POSE="$2"; shift 2 ;;
    --init-duration-s) INIT_DURATION_S="$2"; shift 2 ;;
    --init-settle-seconds) INIT_SETTLE_SECONDS="$2"; shift 2 ;;
    --init-tolerance-rad) INIT_TOLERANCE_RAD="$2"; shift 2 ;;
    --init-move-tolerance-counts) INIT_MOVE_TOLERANCE_COUNTS="$2"; shift 2 ;;
    --init-training-margin-rad) INIT_TRAINING_MARGIN_RAD="$2"; shift 2 ;;
    --success-position-m) SUCCESS_POSITION_M="$2"; shift 2 ;;
    --success-orientation-deg) SUCCESS_ORIENTATION_DEG="$2"; shift 2 ;;
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
if [[ "$LOAD_SUPPORT_MODE" != "off" && "$LOAD_SUPPORT_MODE" != "position-gravity-bias" ]]; then
  echo "[ERROR] --load-support must be off or position-gravity-bias" >&2
  exit 2
fi
if [[ "$LOAD_SUPPORT_CONFIG" = /* ]]; then
  LOAD_SUPPORT_CONFIG_PATH="$LOAD_SUPPORT_CONFIG"
else
  LOAD_SUPPORT_CONFIG_PATH="$ROOT_DIR/$LOAD_SUPPORT_CONFIG"
fi
if [[ "$LOAD_SUPPORT_MODE" != "off" && ! -f "$LOAD_SUPPORT_CONFIG_PATH" ]]; then
  echo "[ERROR] load-support config not found: $LOAD_SUPPORT_CONFIG_PATH" >&2
  exit 2
fi
if [[ "$POLICY_TARGET_TRACKER_MODE" != "off" && "$POLICY_TARGET_TRACKER_MODE" != "bounded" ]]; then
  echo "[ERROR] --policy-target-tracker must be off or bounded" >&2
  exit 2
fi
if [[ "$POLICY_TARGET_TRACKER_CONFIG" = /* ]]; then
  POLICY_TARGET_TRACKER_CONFIG_PATH="$POLICY_TARGET_TRACKER_CONFIG"
else
  POLICY_TARGET_TRACKER_CONFIG_PATH="$ROOT_DIR/$POLICY_TARGET_TRACKER_CONFIG"
fi
if [[ "$POLICY_TARGET_TRACKER_MODE" != "off" && ! -f "$POLICY_TARGET_TRACKER_CONFIG_PATH" ]]; then
  echo "[ERROR] policy-target tracker config not found: $POLICY_TARGET_TRACKER_CONFIG_PATH" >&2
  exit 2
fi
if ! [[ "$SUCCESS_POSITION_M" =~ ^[0-9]+([.][0-9]+)?$ ]] || \
   ! awk -v value="$SUCCESS_POSITION_M" 'BEGIN { exit !(value >= 0.003 && value <= 0.03) }'; then
  echo "[ERROR] --success-position-m must be within [0.003, 0.03] m" >&2
  exit 2
fi
if ! [[ "$SUCCESS_ORIENTATION_DEG" =~ ^[0-9]+([.][0-9]+)?$ ]] || \
   ! awk -v value="$SUCCESS_ORIENTATION_DEG" 'BEGIN { exit !(value >= 1.0 && value <= 20.0) }'; then
  echo "[ERROR] --success-orientation-deg must be within [1, 20] deg" >&2
  exit 2
fi
printf -v CONTROL_RATE_PARAM "%.6f" "$CONTROL_RATE_HZ"
printf -v MAX_TRACKING_ERROR_PARAM "%.6f" "$MAX_TRACKING_ERROR_RAD"
printf -v SUCCESS_POSITION_PARAM "%.6f" "$SUCCESS_POSITION_M"
printf -v SUCCESS_ORIENTATION_PARAM "%.6f" "$SUCCESS_ORIENTATION_DEG"
if [[ "$ENABLE_JOINT_LIMIT_CBF" != "true" && "$ENABLE_JOINT_LIMIT_CBF" != "false" && \
      "$ENABLE_JOINT_LIMIT_CBF" != "on" && "$ENABLE_JOINT_LIMIT_CBF" != "off" ]]; then
  echo "[ERROR] --joint-limit-cbf must be on/off or true/false" >&2
  exit 2
fi
if [[ "$ENABLE_JOINT_LIMIT_CBF" == "on" ]]; then ENABLE_JOINT_LIMIT_CBF="true"; fi
if [[ "$ENABLE_JOINT_LIMIT_CBF" == "off" ]]; then ENABLE_JOINT_LIMIT_CBF="false"; fi
if [[ "$ENABLE_OBSTACLE_CBF" == "on" ]]; then ENABLE_OBSTACLE_CBF="true"; fi
if [[ "$ENABLE_OBSTACLE_CBF" == "off" ]]; then ENABLE_OBSTACLE_CBF="false"; fi
if [[ "$ENABLE_OBSTACLE_CBF" != "true" && "$ENABLE_OBSTACLE_CBF" != "false" ]]; then
  echo "[ERROR] --obstacle-cbf must be on/off or true/false" >&2
  exit 2
fi
if [[ "$OBSTACLE_GUI" == "on" ]]; then OBSTACLE_GUI="true"; fi
if [[ "$OBSTACLE_GUI" == "off" ]]; then OBSTACLE_GUI="false"; fi
if [[ "$OBSTACLE_GUI" != "true" && "$OBSTACLE_GUI" != "false" ]]; then
  echo "[ERROR] --obstacle-gui must be on/off or true/false" >&2
  exit 2
fi
if [[ "$ATTACHED_THIN_FILTER" == "on" ]]; then ATTACHED_THIN_FILTER="true"; fi
if [[ "$ATTACHED_THIN_FILTER" == "off" ]]; then ATTACHED_THIN_FILTER="false"; fi
if [[ "$ATTACHED_THIN_FILTER" != "true" && "$ATTACHED_THIN_FILTER" != "false" ]]; then
  echo "[ERROR] --attached-thin-filter must be on/off or true/false" >&2
  exit 2
fi
if [[ "$OBSTACLE_SELECTION_MODE" != "all-except-target" && "$OBSTACLE_SELECTION_MODE" != "target-only" ]]; then
  echo "[ERROR] --obstacle-selection must be all-except-target or target-only" >&2
  exit 2
fi
if [[ "$OBSTACLE_SELECTION_MODE" == "target-only" && -z "$OBSTACLE_TARGET_CLASS" ]]; then
  echo "[ERROR] --obstacle-target-class is required in target-only mode" >&2
  exit 2
fi
if [[ -n "$OBSTACLE_TARGET_CLASS" ]]; then
  if [[ "$OBSTACLE_TARGET_MODEL" = /* ]]; then
    OBSTACLE_TARGET_MODEL_PATH="$OBSTACLE_TARGET_MODEL"
  else
    OBSTACLE_TARGET_MODEL_PATH="$ROOT_DIR/$OBSTACLE_TARGET_MODEL"
  fi
  if [[ ! -f "$OBSTACLE_TARGET_MODEL_PATH" ]]; then
    echo "[ERROR] obstacle detector model not found: $OBSTACLE_TARGET_MODEL_PATH" >&2
    exit 2
  fi
fi
if ! awk -v v="$OBSTACLE_TARGET_CONF" 'BEGIN { exit !(v > 0.0 && v <= 1.0) }'; then
  echo "[ERROR] --obstacle-target-conf must be within (0, 1]" >&2
  exit 2
fi
if ! awk -v v="$OBSTACLE_MASK_REFRESH_HZ" 'BEGIN { exit !(v >= 0.2 && v <= 10.0) }'; then
  echo "[ERROR] --obstacle-mask-refresh-hz must be within [0.2, 10] Hz" >&2
  exit 2
fi
if ! awk -v v="$OBSTACLE_TARGET_MASK_TOLERANCE_S" 'BEGIN { exit !(v >= 0.5 && v <= 10.0) }'; then
  echo "[ERROR] --obstacle-target-mask-tolerance-s must be within [0.5, 10] s" >&2
  exit 2
fi
if ! awk -v v="$OBSTACLE_STARTUP_TIMEOUT_S" 'BEGIN { exit !(v >= 3.0 && v <= 30.0) }'; then
  echo "[ERROR] --obstacle-startup-timeout-s must be within [3, 30] s" >&2
  exit 2
fi
if [[ "$WRIST_ATTACHMENT_BOX" == "on" ]]; then WRIST_ATTACHMENT_BOX="true"; fi
if [[ "$WRIST_ATTACHMENT_BOX" == "off" ]]; then WRIST_ATTACHMENT_BOX="false"; fi
if [[ "$WRIST_ATTACHMENT_BOX" != "true" && "$WRIST_ATTACHMENT_BOX" != "false" ]]; then
  echo "[ERROR] --wrist-attachment-box must be on/off or true/false" >&2
  exit 2
fi
if ! awk -v v="$MAX_JOINT_VELOCITY_RAD_S" 'BEGIN { exit !(v >= 0.05 && v <= 0.25) }'; then
  echo "[ERROR] --max-joint-velocity-rad-s must be within [0.05, 0.25]" >&2
  exit 2
fi
if ! awk -v v="$MAX_JOINT_ACCELERATION_RAD_S2" 'BEGIN { exit !(v >= 0.10 && v <= 1.00) }'; then
  echo "[ERROR] --max-joint-acceleration-rad-s2 must be within [0.10, 1.00]" >&2
  exit 2
fi
if ! awk -v v="$POLICY_TIMEOUT_S" 'BEGIN { exit !(v >= 5.0 && v <= 90.0) }'; then
  echo "[ERROR] --timeout-s must be within [5, 90]" >&2
  exit 2
fi
if ! awk -v v="$HOLD_CURRENT_DURATION_S" 'BEGIN { exit !(v >= 3.0 && v <= 120.0) }'; then
  echo "[ERROR] --hold-current-duration-s must be within [3, 120]" >&2
  exit 2
fi
if [[ "$INITIALIZE_POLICY_POSE" == "on" ]]; then INITIALIZE_POLICY_POSE="true"; fi
if [[ "$INITIALIZE_POLICY_POSE" == "off" ]]; then INITIALIZE_POLICY_POSE="false"; fi
if [[ "$INITIALIZE_POLICY_POSE" != "true" && "$INITIALIZE_POLICY_POSE" != "false" ]]; then
  echo "[ERROR] --initialize-policy-pose must be on/off or true/false" >&2
  exit 2
fi
if ! awk -v v="$INIT_DURATION_S" 'BEGIN { exit !(v >= 0.5 && v <= 30.0) }'; then
  echo "[ERROR] --init-duration-s must be within [0.5, 30]" >&2
  exit 2
fi
if ! awk -v v="$INIT_SETTLE_SECONDS" 'BEGIN { exit !(v >= 0.2 && v <= 5.0) }'; then
  echo "[ERROR] --init-settle-seconds must be within [0.2, 5.0]" >&2
  exit 2
fi
if ! awk -v v="$INIT_TOLERANCE_RAD" 'BEGIN { exit !(v >= 0.01 && v <= 0.30) }'; then
  echo "[ERROR] --init-tolerance-rad must be within [0.01, 0.30]" >&2
  exit 2
fi
if ! [[ "$INIT_MOVE_TOLERANCE_COUNTS" =~ ^[0-9]+$ ]] || \
   ! awk -v v="$INIT_MOVE_TOLERANCE_COUNTS" 'BEGIN { exit !(v >= 8 && v <= 100) }'; then
  echo "[ERROR] --init-move-tolerance-counts must be within [8, 100]" >&2
  exit 2
fi
if ! awk -v v="$INIT_TRAINING_MARGIN_RAD" 'BEGIN { exit !(v >= 0.0 && v <= 0.30) }'; then
  echo "[ERROR] --init-training-margin-rad must be within [0, 0.30]" >&2
  exit 2
fi
if [[ "$POLICY_READY_POSE" = /* ]]; then
  POLICY_READY_POSE_PATH="$POLICY_READY_POSE"
else
  POLICY_READY_POSE_PATH="$ROOT_DIR/$POLICY_READY_POSE"
fi
if [[ "$INITIALIZE_POLICY_POSE" == "true" && ! -f "$POLICY_READY_POSE_PATH" ]]; then
  echo "[ERROR] policy-ready pose not found: $POLICY_READY_POSE_PATH" >&2
  exit 2
fi
if ! awk -v v="$SELF_FILTER_MARGIN_M" 'BEGIN { exit !(v >= 0.010 && v <= 0.050) }'; then
  echo "[ERROR] --self-filter-margin-m must be within [0.010, 0.050] m" >&2
  exit 2
fi
if ! awk -v v="$THIN_MAX_WIDTH_M" 'BEGIN { exit !(v >= 0.005 && v <= 0.050) }'; then
  echo "[ERROR] --thin-max-width-m must be within [0.005, 0.050] m" >&2
  exit 2
fi
if ! awk -v v="$THIN_MIN_LENGTH_M" 'BEGIN { exit !(v >= 0.020 && v <= 0.200) }'; then
  echo "[ERROR] --thin-min-length-m must be within [0.020, 0.200] m" >&2
  exit 2
fi
if ! awk -v v="$THIN_MIN_ASPECT_RATIO" 'BEGIN { exit !(v >= 2.0 && v <= 20.0) }'; then
  echo "[ERROR] --thin-min-aspect-ratio must be within [2, 20]" >&2
  exit 2
fi
if ! awk -v v="$THIN_ATTACHMENT_DISTANCE_M" 'BEGIN { exit !(v >= 0.005 && v <= 0.060) }'; then
  echo "[ERROR] --thin-attachment-distance-m must be within [0.005, 0.060] m" >&2
  exit 2
fi
if ! awk -v v="$THIN_MAX_ROBOT_DISTANCE_M" 'BEGIN { exit !(v >= 0.030 && v <= 0.200) }'; then
  echo "[ERROR] --thin-max-robot-distance-m must be within [0.030, 0.200] m" >&2
  exit 2
fi
if ! awk -v v="$OBSTACLE_CBF_D_SAFE_M" 'BEGIN { exit !(v >= 0.030 && v <= 0.100) }'; then
  echo "[ERROR] --obstacle-safe-distance-m must be within [0.030, 0.100] m" >&2
  exit 2
fi
if ! awk -v v="$TABLE_Z_MAX_M" 'BEGIN { exit !(v >= -0.05 && v <= 0.20) }'; then
  echo "[ERROR] --table-z-max-m must be within [-0.05, 0.20] m" >&2
  exit 2
fi
# ROS 2 infers override types from their YAML spelling. Normalize every DOUBLE
# override so values such as "30" are not inferred as INTEGER.
printf -v MAX_JOINT_VELOCITY_PARAM "%.6f" "$MAX_JOINT_VELOCITY_RAD_S"
printf -v MAX_JOINT_ACCELERATION_PARAM "%.6f" "$MAX_JOINT_ACCELERATION_RAD_S2"
printf -v POLICY_TIMEOUT_PARAM "%.6f" "$POLICY_TIMEOUT_S"
printf -v HOLD_CURRENT_DURATION_PARAM "%.6f" "$HOLD_CURRENT_DURATION_S"
printf -v SELF_FILTER_MARGIN_PARAM "%.6f" "$SELF_FILTER_MARGIN_M"
printf -v THIN_MAX_WIDTH_PARAM "%.6f" "$THIN_MAX_WIDTH_M"
printf -v THIN_MIN_LENGTH_PARAM "%.6f" "$THIN_MIN_LENGTH_M"
printf -v THIN_MIN_ASPECT_RATIO_PARAM "%.6f" "$THIN_MIN_ASPECT_RATIO"
printf -v THIN_ATTACHMENT_DISTANCE_PARAM "%.6f" "$THIN_ATTACHMENT_DISTANCE_M"
printf -v THIN_MAX_ROBOT_DISTANCE_PARAM "%.6f" "$THIN_MAX_ROBOT_DISTANCE_M"
printf -v OBSTACLE_TARGET_CONF_PARAM "%.6f" "$OBSTACLE_TARGET_CONF"
printf -v OBSTACLE_MASK_REFRESH_PARAM "%.6f" "$OBSTACLE_MASK_REFRESH_HZ"
printf -v OBSTACLE_TARGET_MASK_TOLERANCE_PARAM "%.6f" "$OBSTACLE_TARGET_MASK_TOLERANCE_S"
printf -v TABLE_Z_MAX_PARAM "%.6f" "$TABLE_Z_MAX_M"
printf -v OBSTACLE_CLOUD_TIMEOUT_PARAM "%.6f" "$OBSTACLE_CLOUD_TIMEOUT_S"
printf -v OBSTACLE_STARTUP_TIMEOUT_PARAM "%.6f" "$OBSTACLE_STARTUP_TIMEOUT_S"
printf -v OBSTACLE_CBF_D_SAFE_PARAM "%.6f" "$OBSTACLE_CBF_D_SAFE_M"
printf -v OBSTACLE_CBF_ACTIVATE_MARGIN_PARAM "%.6f" "$OBSTACLE_CBF_ACTIVATE_MARGIN_M"
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
echo "[policy_reach] transition layer: measured-relative policy targets, feedback/policy/driver=${CONTROL_RATE_PARAM}Hz, vmax=${MAX_JOINT_VELOCITY_RAD_S}rad/s, amax=${MAX_JOINT_ACCELERATION_RAD_S2}rad/s^2."
echo "[policy_reach] previous-command lag diagnostic=${MAX_TRACKING_ERROR_PARAM}rad; driver single-command limit=${MAX_TRACKING_ERROR_PARAM}rad."
if [[ "$LOAD_SUPPORT_MODE" == "off" ]]; then
  echo "[policy_reach] load support=off."
else
  echo "[policy_reach] load support=$LOAD_SUPPORT_MODE config=$LOAD_SUPPORT_CONFIG_PATH."
fi
if [[ "$POLICY_TARGET_TRACKER_MODE" == "off" ]]; then
  echo "[policy_reach] bounded policy-target tracker=off."
else
  echo "[policy_reach] bounded policy-target tracker=$POLICY_TARGET_TRACKER_MODE config=$POLICY_TARGET_TRACKER_CONFIG_PATH."
fi
echo "[policy_reach] calibrated joint-limit CBF=$ENABLE_JOINT_LIMIT_CBF raw_margin=0 counts."
echo "[policy_reach] success threshold: position=${SUCCESS_POSITION_PARAM}m, orientation=${SUCCESS_ORIENTATION_PARAM}deg."
echo "[policy_reach] obstacle CBF=$ENABLE_OBSTACLE_CBF vmax=${MAX_JOINT_VELOCITY_RAD_S}rad/s amax=${MAX_JOINT_ACCELERATION_RAD_S2}rad/s2."
mkdir -p "$ROOT_DIR/log/runtime/hardware"
setsid "$ROOT_DIR/ros2/run_hardware_controller.sh" --port "$PORT" --rate "$CONTROL_RATE_PARAM" \
  --safe-pose "$POLICY_READY_POSE_PATH" \
  --max-stream-command-delta-rad "$MAX_TRACKING_ERROR_PARAM" \
  --raw-margin-counts 0 \
  --move-position-tolerance-counts "$INIT_MOVE_TOLERANCE_COUNTS" \
  >"$ROOT_DIR/log/runtime/hardware/policy_reach_controller.log" 2>&1 &
CONTROLLER_PID=$!

for _ in $(seq 1 150); do
  if ! kill -0 "$CONTROLLER_PID" 2>/dev/null; then
    echo "[ERROR] hardware controller exited during startup; see log/runtime/hardware/policy_reach_controller.log" >&2
    tail -n 30 "$ROOT_DIR/log/runtime/hardware/policy_reach_controller.log" >&2 || true
    exit 1
  fi
  if hardware_controller_ready; then
    break
  fi
  sleep 0.1
done
if ! hardware_controller_ready; then
  echo "[ERROR] hardware controller did not become ready; see log/runtime/hardware/policy_reach_controller.log" >&2
  tail -n 30 "$ROOT_DIR/log/runtime/hardware/policy_reach_controller.log" >&2 || true
  exit 1
fi

if [[ "$INITIALIZE_POLICY_POSE" == "true" ]]; then
  echo "[policy_reach] INITIALIZING: moving to approved policy-ready pose before vision/policy."
  echo "[policy_reach] init pose=$POLICY_READY_POSE_PATH duration=${INIT_DURATION_S}s settle=${INIT_SETTLE_SECONDS}s hardware_tolerance=${INIT_MOVE_TOLERANCE_COUNTS}counts policy_tolerance=${INIT_TOLERANCE_RAD}rad."
  if ! conda run --no-capture-output -n "$VISION_ENV" python \
    "$ROOT_DIR/ros2/scripts/real/initialize_policy_ready_pose.py" \
    --pose "$POLICY_READY_POSE_PATH" \
    --duration "$INIT_DURATION_S" \
    --settle-seconds "$INIT_SETTLE_SECONDS" \
    --tolerance-rad "$INIT_TOLERANCE_RAD" \
    --training-margin-rad "$INIT_TRAINING_MARGIN_RAD"; then
    echo "[ERROR] policy initialization failed; vision and policy were not started." >&2
    exit 1
  fi
  echo "[policy_reach] initialization complete; subsequent target uses the initialized live state."
else
  echo "[policy_reach] WARNING: policy-pose initialization disabled."
fi

if [[ "$ENABLE_OBSTACLE_CBF" == "true" ]]; then
  OBSTACLE_DEPTH_TOPIC="$DEPTH_TOPIC"
  echo "[policy_reach] starting real Orbbec obstacle cloud: self_margin=${SELF_FILTER_MARGIN_M}m table_z<=${TABLE_Z_MAX_M}m."
  echo "[policy_reach] obstacle selection=${OBSTACLE_SELECTION_MODE} target=${OBSTACLE_TARGET_CLASS:-none}."
  echo "[policy_reach] wrist attachment box=${WRIST_ATTACHMENT_BOX} (wrist_jaw-local raised housing envelope)."
  echo "[policy_reach] attached thin filter=${ATTACHED_THIN_FILTER} width<=${THIN_MAX_WIDTH_M}m length>=${THIN_MIN_LENGTH_M}m aspect>=${THIN_MIN_ASPECT_RATIO}."
  echo "[policy_reach] camera must already publish ${DEPTH_TOPIC} and ${CAMERA_INFO_TOPIC}."
  if [[ -n "$OBSTACLE_TARGET_CLASS" ]]; then
    echo "[policy_reach] starting fixed YOLO + MobileSAM mask at ${OBSTACLE_MASK_REFRESH_HZ}Hz model=${OBSTACLE_TARGET_MODEL_PATH}."
    PYTHONPATH="$ROS_WS/soarm100_vision${PYTHONPATH:+:$PYTHONPATH}" \
      setsid conda run --no-capture-output -n "$VISION_ENV" python \
      "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/target_segmenter_node.py" \
      --ros-args -r __node:=obstacle_target_segmenter \
      -p segmentation_mode:=fixed_yolo_sam \
      -p fixed_yolo_target_class:="$OBSTACLE_TARGET_CLASS" \
      -p fixed_yolo_conf:="$OBSTACLE_TARGET_CONF_PARAM" \
      -p fixed_yolo_model:="$OBSTACLE_TARGET_MODEL_PATH" \
      -p sam_model:="$ROOT_DIR/models/vision/mobile_sam.pt" \
      -p "fixed_yolo_device:='$OBSTACLE_VISION_DEVICE'" \
      -p rgb_topic:="$RGB_TOPIC" \
      -p depth_topic:="$DEPTH_TOPIC" \
      -p camera_info_topic:="$CAMERA_INFO_TOPIC" \
      -p mask_topic:=/obstacle/selected_mask \
      -p expanded_mask_topic:=/obstacle/selected_mask_expanded \
      -p synchronized_depth_topic:=/obstacle/selected_depth \
      -p target_cloud_topic:=/obstacle/selected_cloud_camera \
      -p target_roi_cloud_topic:=/obstacle/selected_cloud_roi_camera \
      -p target_center_topic:=/obstacle/selected_center_camera \
      -p status_topic:=/obstacle/selected_segmentation_status \
      -p segment_service:=/obstacle/segment_selected \
      -p debug_dir:="$ROOT_DIR/log/runtime/ros2_vision/obstacle_selected" \
      -p auto_segment_hz:="$OBSTACLE_MASK_REFRESH_PARAM" \
      -p auto_target_prompt:="$OBSTACLE_TARGET_CLASS" \
      >"$ROOT_DIR/log/runtime/hardware/policy_reach_target_segmenter.log" 2>&1 &
    TARGET_SEGMENTER_PID=$!
    OBSTACLE_DEPTH_TOPIC="/obstacle/selected_depth"
  fi
  OBSTACLE_SELECTION_PARAM="${OBSTACLE_SELECTION_MODE//-/_}"
  OBSTACLE_PERSISTENCE_HITS=2
  if [[ "$OBSTACLE_SELECTION_MODE" == "target-only" ]]; then
    OBSTACLE_PERSISTENCE_HITS=1
  fi
  PYTHONPATH="$ROS_WS/soarm100_vision${PYTHONPATH:+:$PYTHONPATH}" \
    setsid conda run --no-capture-output -n "$VISION_ENV" python \
    "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/obstacle_cloud_node.py" \
    --ros-args \
    -p repo_root:="$ROOT_DIR" \
    -p depth_topic:="$OBSTACLE_DEPTH_TOPIC" \
    -p camera_info_topic:="$CAMERA_INFO_TOPIC" \
    -p use_sim_camera_extrinsics:=false \
    -p calib_json:="$CAMERA_CALIB_JSON" \
    -p input_camera_name:=scene_depth \
    -p use_robot_mask:=false \
    -p target_mask_topic:=/obstacle/selected_mask \
    -p obstacle_selection_mode:="$OBSTACLE_SELECTION_PARAM" \
    -p target_mask_sync_tolerance_s:="$OBSTACLE_TARGET_MASK_TOLERANCE_PARAM" \
    -p lock_static_target_cloud:=true \
    -p use_joint_state_self_filter:=true \
    -p joint_sync_tolerance_s:=0.075 \
    -p self_filter_margin_m:="$SELF_FILTER_MARGIN_PARAM" \
    -p enable_wrist_attachment_box:="$WRIST_ATTACHMENT_BOX" \
    -p enable_attached_thin_filter:="$ATTACHED_THIN_FILTER" \
    -p thin_max_width_m:="$THIN_MAX_WIDTH_PARAM" \
    -p thin_min_length_m:="$THIN_MIN_LENGTH_PARAM" \
    -p thin_min_aspect_ratio:="$THIN_MIN_ASPECT_RATIO_PARAM" \
    -p thin_attachment_distance_m:="$THIN_ATTACHMENT_DISTANCE_PARAM" \
    -p thin_max_robot_distance_m:="$THIN_MAX_ROBOT_DISTANCE_PARAM" \
    -p obstacle_mode:=static \
    -p workspace_x:="[0.02, 0.45]" \
    -p workspace_y:="[-0.30, 0.30]" \
    -p workspace_z:="[0.01, 0.45]" \
    -p remove_table_plane:=true \
    -p table_z_max:="$TABLE_Z_MAX_PARAM" \
    -p persistence_voxel_size:=0.010 \
    -p persistence_hits:="$OBSTACLE_PERSISTENCE_HITS" \
    -p persistence_forget_frames:=4 \
    -p depth_pixel_stride:=4 \
    -p publish_rate_hz:=10.0 \
    >"$ROOT_DIR/log/runtime/hardware/policy_reach_obstacle_cloud.log" 2>&1 &
  OBSTACLE_PID=$!
  if [[ "$OBSTACLE_GUI" == "true" ]]; then
    echo "[policy_reach] starting obstacle GUI: green mask and yellow boxes are the exact CBF cloud."
    PYTHONPATH="$ROS_WS/soarm100_vision${PYTHONPATH:+:$PYTHONPATH}" \
      setsid conda run --no-capture-output -n "$VISION_ENV" python \
      "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/obstacle_overlay_viewer_node.py" \
      --ros-args \
      -p repo_root:="$ROOT_DIR" \
      -p calib_json:="$CAMERA_CALIB_JSON" \
      -p input_camera_name:=scene_depth \
      -p rgb_topic:="$RGB_TOPIC" \
      -p camera_info_topic:="$CAMERA_INFO_TOPIC" \
      -p obstacle_cloud_topic:=/obstacle/cloud \
      -p cloud_stale_s:="$OBSTACLE_CLOUD_TIMEOUT_PARAM" \
      -p show_window:=true \
      >"$ROOT_DIR/log/runtime/hardware/policy_reach_obstacle_viewer.log" 2>&1 &
    OBSTACLE_VIEWER_PID=$!
  fi
  if [[ -n "$OBSTACLE_TARGET_CLASS" ]]; then
    echo "[policy_reach] waiting for the first valid /obstacle/selected_mask ..."
    MASK_READY="false"
    for _ in $(seq 1 60); do
      if [[ -n "$TARGET_SEGMENTER_PID" ]] && ! kill -0 "$TARGET_SEGMENTER_PID" 2>/dev/null; then
        echo "[ERROR] target segmenter exited; see log/runtime/hardware/policy_reach_target_segmenter.log" >&2
        tail -n 30 "$ROOT_DIR/log/runtime/hardware/policy_reach_target_segmenter.log" >&2 || true
        exit 1
      fi
      if timeout 2 ros2 topic echo /obstacle/selected_mask --once \
        --field width >/dev/null 2>&1; then
        MASK_READY="true"
        break
      fi
    done
    if [[ "$MASK_READY" != "true" ]]; then
      echo "[ERROR] no target mask received; see log/runtime/hardware/policy_reach_target_segmenter.log" >&2
      tail -n 30 "$ROOT_DIR/log/runtime/hardware/policy_reach_target_segmenter.log" >&2 || true
      exit 1
    fi
    echo "[policy_reach] target mask ready."
  fi
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
  -p load_support_mode:="$LOAD_SUPPORT_MODE" \
  -p load_support_config:="$LOAD_SUPPORT_CONFIG_PATH" \
  -p policy_target_tracker_mode:="$POLICY_TARGET_TRACKER_MODE" \
  -p policy_target_tracker_config:="$POLICY_TARGET_TRACKER_CONFIG_PATH" \
  -p max_joint_velocity_rad_s:="$MAX_JOINT_VELOCITY_PARAM" \
  -p max_joint_acceleration_rad_s2:="$MAX_JOINT_ACCELERATION_PARAM" \
  -p enable_joint_limit_cbf:="$ENABLE_JOINT_LIMIT_CBF" \
  -p enable_obstacle_cbf:="$ENABLE_OBSTACLE_CBF" \
  -p obstacle_cloud_timeout_s:="$OBSTACLE_CLOUD_TIMEOUT_PARAM" \
  -p obstacle_startup_timeout_s:="$OBSTACLE_STARTUP_TIMEOUT_PARAM" \
  -p obstacle_cbf_d_safe_m:="$OBSTACLE_CBF_D_SAFE_PARAM" \
  -p obstacle_cbf_activate_margin_m:="$OBSTACLE_CBF_ACTIVATE_MARGIN_PARAM" \
  -p success_position_m:="$SUCCESS_POSITION_PARAM" \
  -p success_orientation_deg:="$SUCCESS_ORIENTATION_PARAM" \
  -p timeout_s:="$POLICY_TIMEOUT_PARAM" \
  -p hold_current_duration_s:="$HOLD_CURRENT_DURATION_PARAM" \
  -p start_on_launch:=true
