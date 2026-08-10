#!/usr/bin/env bash
# Real-camera smoke test: Orbbec RGB-D -> fixed-class YOLO bbox -> SAM mask.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROS2_WS="$ROOT_DIR/ros2"
CONDA_ENV="${CONDA_ENV:-vision_seg}"
TARGET_CLASS="jpgCat"
CONF="0.01"
IOU="0.70"
DEVICE="auto"
BUILD="false"
START_CAMERA="true"
SHOW_WINDOW="true"
CAMERA_PID=""
VISION_PID=""

usage() {
  cat <<'EOF'
Usage:
  ./ros2/scripts/real/run_fixed_yolo_sam_mask.sh [options]

Options:
  --class NAME          Fixed model class: jpgCat, Chiikawa, or tissue.
  --conf SCORE          YOLO confidence threshold. Default: 0.01.
  --iou SCORE           YOLO NMS IoU threshold. Default: 0.70.
  --device DEVICE       auto, cpu, or CUDA index such as 0. Default: auto.
  --camera on|off       Start the real Orbbec RGB-D driver. Default: on.
  --show-window on|off  Open the mask overlay window. Default: on.
  --build               Build ROS2 packages first.
  -h, --help            Show this help.

Runtime keys:
  r + ENTER             Run detection and SAM again on the latest frame.
  q + ENTER             Stop all processes cleanly.
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
    --device) DEVICE="$2"; shift 2 ;;
    --camera) START_CAMERA="$(parse_bool "$2")"; shift 2 ;;
    --show-window) SHOW_WINDOW="$(parse_bool "$2")"; shift 2 ;;
    --build) BUILD="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[ERROR] unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "${TARGET_CLASS,,}" in
  jpgcat) TARGET_CLASS="jpgCat" ;;
  chiikawa) TARGET_CLASS="Chiikawa" ;;
  tissue) TARGET_CLASS="tissue" ;;
  *) echo "[ERROR] unknown class '$TARGET_CLASS'; choose jpgCat, Chiikawa, or tissue" >&2; exit 2 ;;
esac

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

cleanup() {
  trap - EXIT INT TERM
  for pid in "$VISION_PID" "$CAMERA_PID"; do
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    fi
  done
  wait "$VISION_PID" 2>/dev/null || true
  wait "$CAMERA_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

source_relaxed /opt/ros/humble/setup.bash
mkdir -p "$ROOT_DIR/logs/hardware"
export ROS_LOG_DIR="${ROS_LOG_DIR:-$ROOT_DIR/logs/ros2/fixed_yolo_sam}"
mkdir -p "$ROS_LOG_DIR"

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
        --cmake-args \
          -DCMAKE_C_COMPILER=/usr/bin/cc \
          -DCMAKE_CXX_COMPILER=/usr/bin/c++ \
          -DPython3_EXECUTABLE=/usr/bin/python3 \
          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
          "-DPYTHON_INCLUDE_DIR=/usr/include/python3.10;/usr/include/x86_64-linux-gnu/python3.10" \
          -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.10.so
  )
fi

if [[ ! -f "$ROS2_WS/install/setup.bash" ]]; then
  echo "[ERROR] missing ros2/install/setup.bash; run with --build first" >&2
  exit 1
fi
source_relaxed "$ROS2_WS/install/setup.bash"

if [[ "$START_CAMERA" == "true" ]]; then
  setsid "$ROOT_DIR/ros2/scripts/real/run_orbbec_rgbd.sh" \
    >"$ROOT_DIR/logs/hardware/fixed_yolo_sam_orbbec.log" 2>&1 &
  CAMERA_PID="$!"
  echo "[fixed_yolo_sam] Orbbec started pid=$CAMERA_PID"
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

echo "[fixed_yolo_sam] class=$TARGET_CLASS conf=$CONF iou=$IOU device=$DEVICE"
echo "[fixed_yolo_sam] detector=$ROOT_DIR/models/vision/yolowork_fixed_best.pt"
echo "[fixed_yolo_sam] SAM=$ROOT_DIR/models/vision/mobile_sam.pt"

setsid ros2 launch soarm100_vision fixed_yolo_sam_mask.launch.py \
  repo_root:="$ROOT_DIR" \
  target_class:="$TARGET_CLASS" \
  detector_model:="$ROOT_DIR/models/vision/yolowork_fixed_best.pt" \
  sam_model:="$ROOT_DIR/models/vision/mobile_sam.pt" \
  detector_conf:="$CONF" \
  detector_iou:="$IOU" \
  detector_device:="$DEVICE" \
  show_window:="$SHOW_WINDOW" \
  >"$ROOT_DIR/logs/hardware/fixed_yolo_sam_nodes.log" 2>&1 &
VISION_PID="$!"

echo "[fixed_yolo_sam] waiting for /segment_target ..."
for _ in $(seq 1 60); do
  if ros2 service list 2>/dev/null | grep -qx '/segment_target'; then
    break
  fi
  if ! kill -0 "$VISION_PID" 2>/dev/null; then
    echo "[ERROR] vision launch exited; see logs/hardware/fixed_yolo_sam_nodes.log" >&2
    exit 1
  fi
  sleep 0.5
done
if ! ros2 service list 2>/dev/null | grep -qx '/segment_target'; then
  echo "[ERROR] /segment_target did not become ready" >&2
  exit 1
fi

segment_once() {
  ros2 service call /segment_target soarm100_interfaces/srv/SegmentTarget \
    "{target_prompt: '$TARGET_CLASS', force_yolo: true}"
}

echo "[fixed_yolo_sam] waiting for synchronized RGB, depth and CameraInfo"
FIRST_SUCCESS="false"
for _ in $(seq 1 20); do
  RESULT="$(segment_once 2>&1 || true)"
  printf '%s\n' "$RESULT"
  if grep -q 'success=True' <<<"$RESULT"; then
    FIRST_SUCCESS="true"
    break
  fi
  sleep 1
done
if [[ "$FIRST_SUCCESS" != "true" ]]; then
  echo "[WARN] initial mask was not produced; use r after checking the logs and camera view"
fi
echo "[fixed_yolo_sam] r=refresh mask, q=quit"
while IFS= read -r command; do
  case "${command,,}" in
    r|"") segment_once || true ;;
    q) break ;;
    *) echo "[fixed_yolo_sam] use r or q" ;;
  esac
done
