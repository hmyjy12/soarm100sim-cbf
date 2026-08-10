#!/usr/bin/env bash
# Launch the Orbbec Gemini 330-series RGB stream.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ORBBEC_WS="${ORBBEC_WS:-$ROOT_DIR/third_party/orbbec_293_ws}"
COLOR_WIDTH="${COLOR_WIDTH:-1280}"
COLOR_HEIGHT="${COLOR_HEIGHT:-720}"

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

if [[ ! -f "$ORBBEC_WS/install/setup.bash" ]]; then
  echo "[orbbec_camera] missing $ORBBEC_WS/install/setup.bash" >&2
  exit 1
fi

source_relaxed /opt/ros/humble/setup.bash
source_relaxed "$ORBBEC_WS/install/setup.bash"

echo "[orbbec_camera] workspace=$ORBBEC_WS"
echo "[orbbec_camera] RGB ${COLOR_WIDTH}x${COLOR_HEIGHT}; depth disabled"
echo "[orbbec_camera] topics=/camera/color/image_raw /camera/color/camera_info"

# Close any leftover Orbbec Viewer first (exclusive USB access).
pkill -TERM -f 'OrbbecViewer' 2>/dev/null || true

exec ros2 launch orbbec_camera gemini_330_series.launch.py \
  enable_color:=true \
  enable_depth:=false \
  enable_point_cloud:=false \
  enable_colored_point_cloud:=false \
  depth_registration:=false \
  color_width:="$COLOR_WIDTH" \
  color_height:="$COLOR_HEIGHT"
