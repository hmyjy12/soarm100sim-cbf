#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE_FRAME="base"
GRIPPER_FRAME="wrist_roll"
OUTPUT_DIR="$ROOT_DIR/log/runtime/hardware/wrist_handeye"
SQUARE_SIZE_M="0.0144"
REJECT_DUPLICATES="true"

usage() {
  cat <<'EOF'
Usage: ./ros2/run_wrist_handeye.sh [options]

This starts only the real-hardware calibration collector. Before running it:
  1. Start ./ros2/run_wrist_camera.sh
  2. Start the read-only hardware joint stream / controller when capturing

Options:
  --base-frame NAME       TF base frame (default: base)
  --gripper-frame NAME    Rigid wrist frame (default: wrist_roll)
  --output-dir PATH       Calibration session root
  --square-size-m VALUE   Measured checker square size (default: 0.0144)
  --allow-duplicates      Do not reject samples that are too similar
  --help                  Show this help

Keys in the preview:
  SPACE capture one sample; S solve using Tsai; Q quit.
Remote capture service:
  /wrist_handeye/capture  (std_srvs/Trigger)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-frame) BASE_FRAME="$2"; shift 2 ;;
    --gripper-frame) GRIPPER_FRAME="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --square-size-m) SQUARE_SIZE_M="$2"; shift 2 ;;
    --allow-duplicates) REJECT_DUPLICATES="false"; shift ;;
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

echo "[wrist_handeye] REAL HARDWARE read-only calibration"
echo "[wrist_handeye] TF=$BASE_FRAME<-$GRIPPER_FRAME"
echo "[wrist_handeye] checker inner corners=9x6 square=${SQUARE_SIZE_M}m"
echo "[wrist_handeye] reject_duplicates=$REJECT_DUPLICATES"
echo "[wrist_handeye] output=$OUTPUT_DIR"

exec ros2 run soarm100_vision wrist_handeye_calibrator_node --ros-args \
  -p base_frame:="$BASE_FRAME" \
  -p gripper_frame:="$GRIPPER_FRAME" \
  -p square_size_m:="$SQUARE_SIZE_M" \
  -p reject_duplicate_samples:="$REJECT_DUPLICATES" \
  -p output_dir:="$OUTPUT_DIR"
