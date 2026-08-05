#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEVICE="/dev/v4l/by-id/usb-RYS_USB_Camera_200901010001-video-index0"
CALIBRATION="$ROOT_DIR/hardware/calibration/camera/wrist_camera_1280x720.yaml"
WIDTH=1280
HEIGHT=720
PIXEL_FORMAT="YUYV"

usage() {
  cat <<'EOF'
Usage: ./ros2/run_wrist_camera.sh [options]

Options:
  --device PATH       Override the stable V4L2 device path.
  --calibration PATH  Override the camera-info YAML path.
  --help              Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --device) DEVICE="$2"; shift 2 ;;
    --calibration) CALIBRATION="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ ! -r "$DEVICE" || ! -w "$DEVICE" ]]; then
  echo "[ERROR] wrist camera is not readable/writable: $DEVICE" >&2
  echo "[HINT] run: v4l2-ctl --list-devices" >&2
  exit 1
fi
if [[ ! -f "$CALIBRATION" ]]; then
  echo "[ERROR] camera calibration file not found: $CALIBRATION" >&2
  exit 1
fi

set +u
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash
set -u

CALIBRATION="$(readlink -f "$CALIBRATION")"

echo "[wrist_camera] node=/wrist/color/wrist_camera"
echo "[wrist_camera] device=$DEVICE"
echo "[wrist_camera] image=/wrist/color/image_raw"
echo "[wrist_camera] camera_info=/wrist/color/camera_info"
echo "[wrist_camera] frame=wrist_camera_optical_frame"
echo "[wrist_camera] calibration=$CALIBRATION"

exec ros2 run v4l2_camera v4l2_camera_node \
  --ros-args \
  -r __node:=wrist_camera \
  -r __ns:=/wrist/color \
  -p video_device:="$DEVICE" \
  -p image_size:="[$WIDTH,$HEIGHT]" \
  -p pixel_format:="$PIXEL_FORMAT" \
  -p camera_info_url:="file://$CALIBRATION" \
  -p camera_frame_id:=wrist_camera_optical_frame
