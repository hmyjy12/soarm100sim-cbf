#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE_FRAME="base"
GRIPPER_FRAME="wrist_roll"
OUTPUT_DIR="$ROOT_DIR/log/runtime/hardware/orbbec_handeye"
SQUARE_SIZE_M="0.0144"
REJECT_DUPLICATES="false"
IMAGE_TOPIC="/camera/color/image_raw"
CAMERA_INFO_TOPIC="/camera/color/camera_info"

usage() {
  cat <<'EOF'
Usage: ./ros2/run_orbbec_handeye.sh [options]

Starts the Orbbec eye-to-hand calibrator Viewer only.
Use ./ros2/run_orbbec_handeye_manual.sh for the full powered capture loop.

Options:
  --base-frame NAME
  --gripper-frame NAME     default: wrist_roll
  --output-dir PATH
  --square-size-m VALUE    default: 0.0144
  --reject-duplicates      enable similarity rejection
  --help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-frame) BASE_FRAME="$2"; shift 2 ;;
    --gripper-frame) GRIPPER_FRAME="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --square-size-m) SQUARE_SIZE_M="$2"; shift 2 ;;
    --reject-duplicates) REJECT_DUPLICATES="true"; shift ;;
    --help|-h) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

set +u
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash
# shellcheck source=/dev/null
source "$ROOT_DIR/ros2/install/setup.bash"
set -u

echo "[orbbec_handeye] EYE-TO-HAND calibrator"
echo "[orbbec_handeye] TF=$BASE_FRAME<-$GRIPPER_FRAME"
echo "[orbbec_handeye] square=${SQUARE_SIZE_M}m reject_duplicates=$REJECT_DUPLICATES"
echo "[orbbec_handeye] image=$IMAGE_TOPIC"
echo "[orbbec_handeye] output=$OUTPUT_DIR"

exec ros2 run soarm100_vision orbbec_eye_to_hand_calibrator_node --ros-args \
  -p base_frame:="$BASE_FRAME" \
  -p gripper_frame:="$GRIPPER_FRAME" \
  -p square_size_m:="$SQUARE_SIZE_M" \
  -p reject_duplicate_samples:="$REJECT_DUPLICATES" \
  -p image_topic:="$IMAGE_TOPIC" \
  -p camera_info_topic:="$CAMERA_INFO_TOPIC" \
  -p output_dir:="$OUTPUT_DIR"
