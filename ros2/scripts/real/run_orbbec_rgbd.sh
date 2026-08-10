#!/usr/bin/env bash
# Launch the real Orbbec Gemini 336 RGB-D streams used by target segmentation.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ORBBEC_WS="${ORBBEC_WS:-$ROOT_DIR/third_party/orbbec_293_ws}"
COLOR_WIDTH="${COLOR_WIDTH:-1280}"
COLOR_HEIGHT="${COLOR_HEIGHT:-720}"
DEPTH_WIDTH="${DEPTH_WIDTH:-1280}"
DEPTH_HEIGHT="${DEPTH_HEIGHT:-720}"
FPS="${FPS:-30}"

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

if [[ ! -f "$ORBBEC_WS/install/setup.bash" ]]; then
  echo "[orbbec_rgbd] missing $ORBBEC_WS/install/setup.bash" >&2
  exit 1
fi

source_relaxed /opt/ros/humble/setup.bash
source_relaxed "$ORBBEC_WS/install/setup.bash"

echo "[orbbec_rgbd] workspace=$ORBBEC_WS"
echo "[orbbec_rgbd] color=${COLOR_WIDTH}x${COLOR_HEIGHT}@${FPS} depth=${DEPTH_WIDTH}x${DEPTH_HEIGHT}@${FPS}"
echo "[orbbec_rgbd] depth registration enabled; point cloud disabled"
echo "[orbbec_rgbd] topics=/camera/color/image_raw /camera/depth/image_raw /camera/color/camera_info"

exec ros2 launch orbbec_camera gemini_330_series.launch.py \
  enable_color:=true \
  enable_depth:=true \
  enable_point_cloud:=false \
  enable_colored_point_cloud:=false \
  depth_registration:=true \
  color_width:="$COLOR_WIDTH" \
  color_height:="$COLOR_HEIGHT" \
  depth_width:="$DEPTH_WIDTH" \
  depth_height:="$DEPTH_HEIGHT" \
  color_fps:="$FPS" \
  depth_fps:="$FPS"
