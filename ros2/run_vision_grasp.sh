#!/usr/bin/env bash
set -euo pipefail

# One-command launcher for the SO-ARM100 ROS2 vision grasp skeleton.
#
# Coordinate contract:
#   - YOLO-World and SAM operate in 2D image pixel coordinates on the main RGB image.
#   - target_segmenter_node converts SAM mask + main depth + CameraInfo into
#     /target/cloud and /target/center in the main camera optical frame.
#   - AnyGrasp should consume /target/cloud in that same camera optical frame and
#     return grasp poses tagged with the same frame_id, then TF converts them into
#     robot base/world before policy execution.
#   - wrist_tracker_node requires a wrist-frame mask aligned with wrist depth. A
#     main-camera mask must not be used directly on wrist depth without projection
#     or wrist-view SAM refinement.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS2_WS="$ROOT_DIR/ros2"
CONDA_ENV="${CONDA_ENV:-vision_seg}"
ROS_SETUP="${ROS_SETUP:-/opt/ros/humble/setup.bash}"

TARGET_PROMPT="red cube"
ENABLE_AVOIDANCE="false"
BUILD_FIRST="false"
ENABLE_VISUALIZER="true"
SHOW_WINDOW="true"
ENABLE_MUJOCO="true"
MUJOCO_OBSTACLE="auto"
MUJOCO_SDF_CBF="auto"
MUJOCO_OBSTACLE_BODY="obstacle_rod_mount"
MUJOCO_OBSTACLE_POS="0.16,0.09,0.02"
MUJOCO_TARGET_OBJECT="cube"
MUJOCO_TARGET_POS="0.42,0.08,0.021"
MUJOCO_TRAJ_LOG="$ROOT_DIR/logs/ros2_mujoco_grasp.jsonl"
MUJOCO_SPEED="0.5"

RGB_TOPIC="/camera/color/image_raw"
DEPTH_TOPIC="/camera/depth/image_rect_raw"
CAMERA_INFO_TOPIC="/camera/color/camera_info"
WRIST_DEPTH_TOPIC="/wrist/depth/image_rect_raw"
WRIST_CAMERA_INFO_TOPIC="/wrist/depth/camera_info"
YOLO_MODEL="$ROOT_DIR/models/vision/yolov8s-world.pt"
SAM_MODEL="$ROOT_DIR/models/vision/mobile_sam.pt"

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

usage() {
  cat <<'EOF'
Usage:
  ./ros2/run_vision_grasp.sh [options]

Options:
  --build                         Run colcon build before launch.
  --target TEXT                   Target prompt for later action/service calls. Default: "red cube".
  --avoidance on|off              Default avoidance flag for orchestrator. Default: off.
  --visualizer on|off             Start debug overlay viewer. Default: on.
  --show-window on|off            Open local OpenCV preview window. Default: on.
  --mujoco on|off                 Start MuJoCo GUI play.py in parallel. Default: on.
  --mujoco-obstacle on|off|auto   Show/load MuJoCo obstacle scene. Default: auto follows --avoidance.
  --mujoco-sdf-cbf on|off|auto    Enable MuJoCo SDF-CBF-QP. Default: auto follows --avoidance.
  --mujoco-obstacle-body NAME     MuJoCo obstacle body to reposition. Default: obstacle_rod_mount.
  --mujoco-obstacle-pos X,Y,Z     Static obstacle body position when obstacle is on. Default: 0.16,0.09,0.02.
  --mujoco-target-object NAME     MuJoCo grasp target: cube/bottle/sphere/custom. Default: cube.
  --mujoco-target-pos X,Y,Z       MuJoCo target world position. Default: 0.42,0.08,0.021.
  --mujoco-traj-log PATH          MuJoCo trajectory log path.
  --mujoco-speed SPEED            MuJoCo playback speed. Default: 0.5.
  --rgb-topic TOPIC               Main RGB topic.
  --depth-topic TOPIC             Main depth topic.
  --camera-info-topic TOPIC       Main camera_info topic.
  --wrist-depth-topic TOPIC       Wrist depth topic.
  --wrist-camera-info-topic TOPIC Wrist camera_info topic.
  --yolo-model PATH               YOLO-World model path.
  --sam-model PATH                MobileSAM model path.
  --conda-env NAME                Conda environment. Default: vision_seg.
  --ros-setup PATH                ROS setup.bash. Default: /opt/ros/humble/setup.bash.
  -h, --help                      Show this help.

Examples:
  ./ros2/run_vision_grasp.sh --build
  ./ros2/run_vision_grasp.sh --target "red bottle" --avoidance off
  ./ros2/run_vision_grasp.sh --avoidance on --mujoco-obstacle on --mujoco-sdf-cbf on
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build)
      BUILD_FIRST="true"
      shift
      ;;
    --target)
      TARGET_PROMPT="$2"
      shift 2
      ;;
    --avoidance)
      case "$2" in
        on|true|1) ENABLE_AVOIDANCE="true" ;;
        off|false|0) ENABLE_AVOIDANCE="false" ;;
        *) echo "[ERROR] --avoidance must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --visualizer)
      case "$2" in
        on|true|1) ENABLE_VISUALIZER="true" ;;
        off|false|0) ENABLE_VISUALIZER="false" ;;
        *) echo "[ERROR] --visualizer must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --show-window)
      case "$2" in
        on|true|1) SHOW_WINDOW="true" ;;
        off|false|0) SHOW_WINDOW="false" ;;
        *) echo "[ERROR] --show-window must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco)
      case "$2" in
        on|true|1) ENABLE_MUJOCO="true" ;;
        off|false|0) ENABLE_MUJOCO="false" ;;
        *) echo "[ERROR] --mujoco must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-obstacle)
      case "$2" in
        on|true|1) MUJOCO_OBSTACLE="true" ;;
        off|false|0) MUJOCO_OBSTACLE="false" ;;
        auto) MUJOCO_OBSTACLE="auto" ;;
        *) echo "[ERROR] --mujoco-obstacle must be on/off/auto" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-sdf-cbf)
      case "$2" in
        on|true|1) MUJOCO_SDF_CBF="true" ;;
        off|false|0) MUJOCO_SDF_CBF="false" ;;
        auto) MUJOCO_SDF_CBF="auto" ;;
        *) echo "[ERROR] --mujoco-sdf-cbf must be on/off/auto" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-obstacle-body)
      MUJOCO_OBSTACLE_BODY="$2"
      shift 2
      ;;
    --mujoco-obstacle-pos)
      MUJOCO_OBSTACLE_POS="$2"
      shift 2
      ;;
    --mujoco-target-object)
      MUJOCO_TARGET_OBJECT="$2"
      shift 2
      ;;
    --mujoco-target-pos)
      MUJOCO_TARGET_POS="$2"
      shift 2
      ;;
    --mujoco-traj-log)
      MUJOCO_TRAJ_LOG="$2"
      shift 2
      ;;
    --mujoco-speed)
      MUJOCO_SPEED="$2"
      shift 2
      ;;
    --rgb-topic)
      RGB_TOPIC="$2"
      shift 2
      ;;
    --depth-topic)
      DEPTH_TOPIC="$2"
      shift 2
      ;;
    --camera-info-topic)
      CAMERA_INFO_TOPIC="$2"
      shift 2
      ;;
    --wrist-depth-topic)
      WRIST_DEPTH_TOPIC="$2"
      shift 2
      ;;
    --wrist-camera-info-topic)
      WRIST_CAMERA_INFO_TOPIC="$2"
      shift 2
      ;;
    --yolo-model)
      YOLO_MODEL="$2"
      shift 2
      ;;
    --sam-model)
      SAM_MODEL="$2"
      shift 2
      ;;
    --conda-env)
      CONDA_ENV="$2"
      shift 2
      ;;
    --ros-setup)
      ROS_SETUP="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ "$MUJOCO_OBSTACLE" == "auto" ]]; then
  MUJOCO_OBSTACLE="$ENABLE_AVOIDANCE"
fi
if [[ "$MUJOCO_SDF_CBF" == "auto" ]]; then
  MUJOCO_SDF_CBF="$ENABLE_AVOIDANCE"
fi

if [[ ! -f "$ROS_SETUP" ]]; then
  echo "[ERROR] ROS setup not found: $ROS_SETUP" >&2
  echo "Set ROS_SETUP=/path/to/setup.bash or pass --ros-setup." >&2
  exit 1
fi

source_relaxed "$ROS_SETUP"

cd "$ROS2_WS"

if [[ "$BUILD_FIRST" == "true" ]]; then
  env \
    -u CONDA_PREFIX \
    -u CONDA_DEFAULT_ENV \
    -u CONDA_PROMPT_MODIFIER \
    -u CONDA_SHLVL \
    -u CONDA_BUILD_SYSROOT \
    -u CONDA_TOOLCHAIN_BUILD \
    -u CONDA_TOOLCHAIN_HOST \
    -u _CONDA_PYTHON_SYSCONFIGDATA_NAME \
    -u CC \
    -u CXX \
    -u GCC \
    -u CFLAGS \
    -u CPPFLAGS \
    -u CMAKE_PREFIX_PATH \
    PATH="/opt/ros/humble/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    AMENT_PREFIX_PATH="/opt/ros/humble" \
    PYTHONPATH="/opt/ros/humble/lib/python3.10/site-packages:/opt/ros/humble/local/lib/python3.10/dist-packages" \
    colcon build --packages-select soarm100_interfaces soarm100_vision \
    --cmake-clean-cache \
    --cmake-args \
      -DPython3_EXECUTABLE=/usr/bin/python3 \
      -DPYTHON_EXECUTABLE=/usr/bin/python3 \
      "-DPYTHON_INCLUDE_DIR=/usr/include/python3.10;/usr/include/x86_64-linux-gnu/python3.10" \
      -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.10.so
fi

if [[ -f "$ROS2_WS/install/setup.bash" ]]; then
  source_relaxed "$ROS2_WS/install/setup.bash"
else
  echo "[WARN] $ROS2_WS/install/setup.bash not found. Run with --build first if packages are not discoverable."
fi

MUJOCO_PID=""
if [[ "$ENABLE_MUJOCO" == "true" ]]; then
  echo "[soarm100_ros2] starting MuJoCo GUI in base/current env"
  MUJOCO_EXTRA_ARGS=()
  if [[ "$MUJOCO_OBSTACLE" == "true" ]]; then
    MUJOCO_EXTRA_ARGS+=(--enable-obstacle)
    MUJOCO_EXTRA_ARGS+=(
      --obstacle-body "$MUJOCO_OBSTACLE_BODY"
      --obstacle-motion line
      --obstacle-motion-center "$MUJOCO_OBSTACLE_POS"
      --obstacle-motion-amp "0,0,0"
    )
  fi
  if [[ "$MUJOCO_SDF_CBF" == "true" ]]; then
    MUJOCO_EXTRA_ARGS+=(--enable-sdf-cbf-qp)
  fi
  (
    cd "$ROOT_DIR"
    python mujoco/play.py \
      --episodes 1 \
      --target-idx 123 \
      --enable-grasp-chain \
      --grasp-target-object "$MUJOCO_TARGET_OBJECT" \
      --grasp-target-pos "$MUJOCO_TARGET_POS" \
      --traj-log "$MUJOCO_TRAJ_LOG" \
      --stop-on-success \
      --verbose \
      --speed "$MUJOCO_SPEED" \
      "${MUJOCO_EXTRA_ARGS[@]}"
  ) &
  MUJOCO_PID="$!"
  trap 'if [[ -n "${MUJOCO_PID:-}" ]]; then kill "$MUJOCO_PID" 2>/dev/null || true; fi' EXIT INT TERM
fi

if command -v conda >/dev/null 2>&1; then
  set +u
  eval "$(conda shell.bash hook)"
  conda activate "$CONDA_ENV"
  set -u
else
  echo "[WARN] conda command not found; assuming current shell already has vision deps."
fi

echo "[soarm100_ros2] conda_env=$CONDA_ENV"
echo "[soarm100_ros2] target=$TARGET_PROMPT avoidance=$ENABLE_AVOIDANCE"
echo "[soarm100_ros2] visualizer=$ENABLE_VISUALIZER show_window=$SHOW_WINDOW"
echo "[soarm100_ros2] mujoco=$ENABLE_MUJOCO obstacle=$MUJOCO_OBSTACLE sdf_cbf=$MUJOCO_SDF_CBF target_object=$MUJOCO_TARGET_OBJECT target_pos=$MUJOCO_TARGET_POS obstacle_body=$MUJOCO_OBSTACLE_BODY obstacle_pos=$MUJOCO_OBSTACLE_POS speed=$MUJOCO_SPEED"
echo "[soarm100_ros2] yolo=$YOLO_MODEL"
echo "[soarm100_ros2] sam=$SAM_MODEL"

ros2 launch soarm100_vision vision_grasp.launch.py \
  target_prompt:="$TARGET_PROMPT" \
  enable_avoidance:="$ENABLE_AVOIDANCE" \
  rgb_topic:="$RGB_TOPIC" \
  depth_topic:="$DEPTH_TOPIC" \
  camera_info_topic:="$CAMERA_INFO_TOPIC" \
  wrist_depth_topic:="$WRIST_DEPTH_TOPIC" \
  wrist_camera_info_topic:="$WRIST_CAMERA_INFO_TOPIC" \
  yolo_model:="$YOLO_MODEL" \
  sam_model:="$SAM_MODEL" \
  enable_visualizer:="$ENABLE_VISUALIZER" \
  show_window:="$SHOW_WINDOW"
