#!/usr/bin/env bash
# Orbbec RGB -> continuous fixed-class YOLO tracking with a ROS2 preview.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS2_WS="$ROOT_DIR/ros2"
CONDA_ENV="${CONDA_ENV:-vision_seg}"
TARGET_CLASS="all"
CONF="0.01"
IOU="0.70"
IMGSZ="640"
DEVICE="auto"
TRACKER="botsort.yaml"
MAX_FPS="30.0"
SHOW_WINDOW="true"
START_CAMERA="true"
BUILD="false"
CAMERA_PID=""

usage() {
  cat <<'EOF'
Usage:
  ./ros2/scripts/real/run_fixed_yolo_tracking.sh [options]

Options:
  --class NAME          all, jpgCat, Chiikawa, or tissue. Default: all.
  --conf SCORE          Detection confidence. Default: 0.01.
  --iou SCORE           NMS IoU threshold. Default: 0.70.
  --imgsz PIXELS        YOLO inference size. Default: 640.
  --device DEVICE       auto, cpu, or CUDA index such as 0. Default: auto.
  --tracker FILE        botsort.yaml or bytetrack.yaml. Default: botsort.yaml.
  --max-fps FPS         Maximum inference timer rate. Default: 30.
  --camera on|off       Start Orbbec RGB. Default: on.
  --show-window on|off  Open live annotated window. Default: on.
  --build               Build ROS2 packages before launch.

Press Q/Esc in the image window or Ctrl+C in the terminal to stop.
EOF
}

parse_bool() {
  case "$1" in
    on|true|1) printf 'true' ;;
    off|false|0) printf 'false' ;;
    *) echo "[ERROR] expected on/off, got: $1" >&2; exit 2 ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --class) TARGET_CLASS="$2"; shift 2 ;;
    --conf) CONF="$2"; shift 2 ;;
    --iou) IOU="$2"; shift 2 ;;
    --imgsz) IMGSZ="$2"; shift 2 ;;
    --device) DEVICE="$2"; shift 2 ;;
    --tracker) TRACKER="$2"; shift 2 ;;
    --max-fps) MAX_FPS="$2"; shift 2 ;;
    --camera) START_CAMERA="$(parse_bool "$2")"; shift 2 ;;
    --show-window) SHOW_WINDOW="$(parse_bool "$2")"; shift 2 ;;
    --build) BUILD="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "${TARGET_CLASS,,}" in
  all) TARGET_CLASS="all" ;;
  jpgcat) TARGET_CLASS="jpgCat" ;;
  chiikawa) TARGET_CLASS="Chiikawa" ;;
  tissue) TARGET_CLASS="tissue" ;;
  *) echo "[ERROR] unsupported class: $TARGET_CLASS" >&2; exit 2 ;;
esac
case "$TRACKER" in
  botsort.yaml|bytetrack.yaml) ;;
  *) echo "[ERROR] tracker must be botsort.yaml or bytetrack.yaml" >&2; exit 2 ;;
esac

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

cleanup() {
  trap - EXIT INT TERM
  if [[ -n "$CAMERA_PID" ]] && kill -0 "$CAMERA_PID" 2>/dev/null; then
    kill -TERM -- "-$CAMERA_PID" 2>/dev/null || kill -TERM "$CAMERA_PID" 2>/dev/null || true
    wait "$CAMERA_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

source_relaxed /opt/ros/humble/setup.bash
export ROS_LOG_DIR="${ROS_LOG_DIR:-$ROOT_DIR/logs/ros2/fixed_yolo_tracking}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/matplotlib-fixed-yolo}"
mkdir -p "$ROS_LOG_DIR" "$ROOT_DIR/logs/hardware"

if [[ "$BUILD" == "true" ]]; then
  (
    cd "$ROS2_WS"
    env \
      -u CONDA_PREFIX -u CONDA_DEFAULT_ENV -u CONDA_PROMPT_MODIFIER \
      -u CONDA_EXE -u CONDA_PYTHON_EXE -u CONDA_SHLVL \
      -u CONDA_BUILD_SYSROOT -u CONDA_TOOLCHAIN_BUILD \
      -u CONDA_TOOLCHAIN_HOST -u _CONDA_PYTHON_SYSCONFIGDATA_NAME \
      -u CC -u CXX -u GCC -u CFLAGS -u CPPFLAGS -u CMAKE_PREFIX_PATH \
      PATH="/opt/ros/humble/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
      AMENT_PREFIX_PATH="/opt/ros/humble" \
      PYTHONPATH="/opt/ros/humble/lib/python3.10/site-packages:/opt/ros/humble/local/lib/python3.10/dist-packages" \
      colcon build --packages-select soarm100_interfaces soarm100_vision \
        --symlink-install --cmake-clean-cache \
        --cmake-args -DCMAKE_C_COMPILER=/usr/bin/cc \
          -DCMAKE_CXX_COMPILER=/usr/bin/c++ \
          -DPython3_EXECUTABLE=/usr/bin/python3 \
          -DPYTHON_EXECUTABLE=/usr/bin/python3
  )
fi

if [[ ! -f "$ROS2_WS/install/setup.bash" ]]; then
  echo "[ERROR] ROS2 workspace is not built; rerun with --build" >&2
  exit 1
fi
source_relaxed "$ROS2_WS/install/setup.bash"

if [[ "$START_CAMERA" == "true" ]]; then
  setsid "$ROOT_DIR/ros2/run_orbbec_camera.sh" \
    >"$ROOT_DIR/logs/hardware/fixed_yolo_tracking_orbbec.log" 2>&1 &
  CAMERA_PID="$!"
  echo "[fixed_yolo_tracking] Orbbec RGB started pid=$CAMERA_PID"
fi

set +u
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"
set -u

CONDA_PYTHON="$CONDA_PREFIX/bin/python"
for entry in "$ROS2_WS"/install/soarm100_vision/lib/soarm100_vision/*; do
  if [[ -f "$entry" && -x "$entry" ]]; then
    sed -i "1s|^#!.*python.*$|#!$CONDA_PYTHON|" "$entry"
  fi
done

echo "[fixed_yolo_tracking] source=/camera/color/image_raw (Orbbec RGB)"
echo "[fixed_yolo_tracking] class=$TARGET_CLASS conf=$CONF iou=$IOU imgsz=$IMGSZ device=$DEVICE tracker=$TRACKER"
echo "[fixed_yolo_tracking] annotated=/debug/fixed_yolo_tracking detections=/target/detections"

ros2 launch soarm100_vision fixed_yolo_tracking.launch.py \
  model:="$ROOT_DIR/models/vision/yolowork_fixed_best.pt" \
  target_class:="$TARGET_CLASS" \
  conf:="$CONF" \
  iou:="$IOU" \
  imgsz:="$IMGSZ" \
  device:="$DEVICE" \
  tracker:="$TRACKER" \
  max_fps:="$MAX_FPS" \
  show_window:="$SHOW_WINDOW"
