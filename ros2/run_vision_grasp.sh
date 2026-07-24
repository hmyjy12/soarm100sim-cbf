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
#   - wrist_tracker_node consumes wrist RGB only. The backend projects the
#     base-frame grasp reference through the live wrist-camera pose to seed ROI.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS2_WS="$ROOT_DIR/ros2"
CONDA_ENV="${CONDA_ENV:-vision_seg}"
ROS_SETUP="${ROS_SETUP:-/opt/ros/humble/setup.bash}"
ROS_LOG_DIR="${ROS_LOG_DIR:-$ROOT_DIR/logs/ros2}"

TARGET_PROMPT="red cube"
ENABLE_AVOIDANCE="false"
BUILD_FIRST="false"
ENABLE_VISUALIZER="false"
SHOW_WINDOW="false"
ENABLE_MUJOCO="true"
ENABLE_MUJOCO_BACKEND="false"
ENABLE_MUJOCO_CAMERA="false"
ENABLE_SDF_BACKEND="false"
ENABLE_ANYGRASP_PLANNER="false"
MUJOCO_OBSTACLE="auto"
MUJOCO_SDF_CBF="auto"
OBSTACLE_MODE="static"
MUJOCO_OBSTACLE_BODY="obstacle_rod_mount"
MUJOCO_OBSTACLE_POS="0.16,0.09,0.02"
MUJOCO_MJCF=""
MUJOCO_TARGET_OBJECT="cube"
MUJOCO_TARGET_POS="0.42,0.08,0.021"
MUJOCO_TRAJ_LOG="$ROOT_DIR/logs/ros2_mujoco_grasp.jsonl"
MUJOCO_SPEED="1.0"
MUJOCO_PYTHON="${MUJOCO_PYTHON:-/home/sophie/miniconda3/bin/python}"
MUJOCO_BACKEND_MODE="subprocess"
MUJOCO_INPROCESS_VIEWER="false"
MUJOCO_INTERNAL_TRACKING="true"
MUJOCO_TRACK_SOURCE="wrist"
MUJOCO_REPLAN_ATTEMPTS="2"
MUJOCO_FINAL_APPROACH_TIMEOUT="10.0"
AUTO_PLANNED_GRASP="false"
AUTO_PREGRASP_POS="0.35,0.08,0.09"
AUTO_GRASP_POS="0.39,0.08,0.06"
AUTO_GRASP_QUAT="1,0,0,0"
AUTO_GRIPPER_WIDTH="0.05"
AUTO_GOAL_DELAY="4.0"
AUTO_EXECUTE_GRASP="false"

RGB_TOPIC="/camera/color/image_raw"
DEPTH_TOPIC="/camera/depth/image_rect_raw"
CAMERA_INFO_TOPIC="/camera/color/camera_info"
WRIST_RGB_TOPIC="/wrist/color/image_raw"
YOLO_MODEL="$ROOT_DIR/models/vision/yolov8s-world.pt"
SAM_MODEL="$ROOT_DIR/models/vision/mobile_sam.pt"
ANYGRASP_SDK_ROOT="$ROOT_DIR/anygrasp_sdk"
ANYGRASP_CHECKPOINT="$ROOT_DIR/anygrasp_sdk/grasp_detection/log/checkpoint_detection.tar"

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
  --visualizer on|off             Start debug overlay viewer. Default: off.
  --show-window on|off            Open local OpenCV preview window. Default: off.
  --mujoco on|off                 Start MuJoCo GUI play.py in parallel. Default: on.
  --mujoco-backend on|off         Start ROS2 MuJoCo policy backend action server. Default: off.
  --mujoco-camera on|off          Publish MuJoCo RGB-D camera topics. Default: off.
  --sdf-backend on|off            Start ROS2 SDF-CBF backend status node. Default: off.
  --anygrasp-planner on|off       Start ROS2 AnyGrasp planner action server. Default: off.
  --mujoco-obstacle on|off|auto   Show/load MuJoCo obstacle scene. Default: auto follows --avoidance.
  --mujoco-sdf-cbf on|off|auto    Enable MuJoCo SDF-CBF-QP. Default: auto follows --avoidance.
  --obstacle-mode static|dynamic  Static snapshot SDF or continuously updated depth SDF. Default: static.
  --mujoco-obstacle-body NAME     MuJoCo obstacle body to reposition. Default: obstacle_rod_mount.
  --mujoco-obstacle-pos X,Y,Z     Static obstacle body position when obstacle is on. Default: 0.16,0.09,0.02.
  --mujoco-target-object NAME     MuJoCo grasp target: cube/bottle/sphere/custom. Default: cube.
  --mujoco-target-pos X,Y,Z       MuJoCo target world position. Default: 0.42,0.08,0.021.
  --mujoco-traj-log PATH          MuJoCo trajectory log path.
  --mujoco-speed SPEED            MuJoCo playback speed. Default: 1.0.
  --mujoco-python PATH            Python executable for MuJoCo backend subprocess. Default: /home/sophie/miniconda3/bin/python.
  --mujoco-backend-mode subprocess|inprocess
                                  Policy backend implementation. Default: subprocess.
  --mujoco-inprocess-viewer on|off
                                  Open MuJoCo viewer from ROS2 inprocess backend. Default: off.
  --mujoco-internal-tracking on|off
                                  Let play.py perform near-field target tracking inside its policy loop. Default: on.
  --mujoco-track-source wrist|gt|none
                                  Tracking source passed to play.py. Default: wrist.
  --mujoco-replan-attempts N      Maximum in-place SAM+AnyGrasp replans. Default: 2.
  --final-approach-timeout SEC    Maximum FINAL_APPROACH time before CLOSE. Default: 10.0.
  --auto-planned-grasp on|off     Send one ExecutePlannedGrasp goal after launch. Default: off.
  --auto-pregrasp-pos X,Y,Z       Planned pregrasp pose position for auto goal.
  --auto-grasp-pos X,Y,Z          Planned final grasp pose position for auto goal.
  --auto-grasp-quat W,X,Y,Z       Planned grasp orientation for auto goal.
  --auto-gripper-width M          Planned gripper width for auto goal. Default: 0.05.
  --auto-goal-delay SEC           Delay before sending auto goal. Default: 4.0.
  --auto-execute-grasp on|off     Send one full ExecuteGrasp goal through segment+AnyGrasp+policy. Default: off.
  --rgb-topic TOPIC               Main RGB topic.
  --depth-topic TOPIC             Main depth topic.
  --camera-info-topic TOPIC       Main camera_info topic.
  --wrist-rgb-topic TOPIC         Wrist RGB tracking topic.
  --yolo-model PATH               YOLO-World model path.
  --sam-model PATH                MobileSAM model path.
  --anygrasp-sdk-root PATH        AnyGrasp SDK root. Default: ./anygrasp_sdk.
  --anygrasp-checkpoint PATH      AnyGrasp checkpoint tar.
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
    --mujoco-backend)
      case "$2" in
        on|true|1) ENABLE_MUJOCO_BACKEND="true" ;;
        off|false|0) ENABLE_MUJOCO_BACKEND="false" ;;
        *) echo "[ERROR] --mujoco-backend must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-camera)
      case "$2" in
        on|true|1) ENABLE_MUJOCO_CAMERA="true" ;;
        off|false|0) ENABLE_MUJOCO_CAMERA="false" ;;
        *) echo "[ERROR] --mujoco-camera must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --sdf-backend)
      case "$2" in
        on|true|1) ENABLE_SDF_BACKEND="true" ;;
        off|false|0) ENABLE_SDF_BACKEND="false" ;;
        *) echo "[ERROR] --sdf-backend must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --anygrasp-planner)
      case "$2" in
        on|true|1) ENABLE_ANYGRASP_PLANNER="true" ;;
        off|false|0) ENABLE_ANYGRASP_PLANNER="false" ;;
        *) echo "[ERROR] --anygrasp-planner must be on/off" >&2; exit 2 ;;
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
    --obstacle-mode)
      case "$2" in
        static|dynamic) OBSTACLE_MODE="$2" ;;
        *) echo "[ERROR] --obstacle-mode must be static/dynamic" >&2; exit 2 ;;
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
    --mujoco-python)
      MUJOCO_PYTHON="$2"
      shift 2
      ;;
    --mujoco-backend-mode)
      case "$2" in
        subprocess|inprocess) MUJOCO_BACKEND_MODE="$2" ;;
        *) echo "[ERROR] --mujoco-backend-mode must be subprocess/inprocess" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-inprocess-viewer)
      case "$2" in
        on|true|1) MUJOCO_INPROCESS_VIEWER="true" ;;
        off|false|0) MUJOCO_INPROCESS_VIEWER="false" ;;
        *) echo "[ERROR] --mujoco-inprocess-viewer must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-internal-tracking)
      case "$2" in
        on|true|1) MUJOCO_INTERNAL_TRACKING="true" ;;
        off|false|0) MUJOCO_INTERNAL_TRACKING="false" ;;
        *) echo "[ERROR] --mujoco-internal-tracking must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-track-source)
      case "$2" in
        wrist|gt|none) MUJOCO_TRACK_SOURCE="$2" ;;
        *) echo "[ERROR] --mujoco-track-source must be wrist/gt/none" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --mujoco-replan-attempts)
      MUJOCO_REPLAN_ATTEMPTS="$2"
      shift 2
      ;;
    --final-approach-timeout)
      MUJOCO_FINAL_APPROACH_TIMEOUT="$2"
      shift 2
      ;;
    --auto-planned-grasp)
      case "$2" in
        on|true|1) AUTO_PLANNED_GRASP="true" ;;
        off|false|0) AUTO_PLANNED_GRASP="false" ;;
        *) echo "[ERROR] --auto-planned-grasp must be on/off" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --auto-pregrasp-pos)
      AUTO_PREGRASP_POS="$2"
      shift 2
      ;;
    --auto-grasp-pos)
      AUTO_GRASP_POS="$2"
      shift 2
      ;;
    --auto-grasp-quat)
      AUTO_GRASP_QUAT="$2"
      shift 2
      ;;
    --auto-gripper-width)
      AUTO_GRIPPER_WIDTH="$2"
      shift 2
      ;;
    --auto-goal-delay)
      AUTO_GOAL_DELAY="$2"
      shift 2
      ;;
    --auto-execute-grasp)
      case "$2" in
        on|true|1) AUTO_EXECUTE_GRASP="true" ;;
        off|false|0) AUTO_EXECUTE_GRASP="false" ;;
        *) echo "[ERROR] --auto-execute-grasp must be on/off" >&2; exit 2 ;;
      esac
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
    --wrist-rgb-topic)
      WRIST_RGB_TOPIC="$2"
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
    --anygrasp-sdk-root)
      ANYGRASP_SDK_ROOT="$2"
      shift 2
      ;;
    --anygrasp-checkpoint)
      ANYGRASP_CHECKPOINT="$2"
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
if [[ -z "$MUJOCO_MJCF" ]]; then
  if [[ "$MUJOCO_OBSTACLE" == "true" ]]; then
    MUJOCO_MJCF="SO-ARM100/Simulation/SO100/mujoco/scene_plus_grasp_obstacle.xml"
  else
    MUJOCO_MJCF="SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"
  fi
fi
if [[ "$AUTO_PLANNED_GRASP" == "true" && "$AUTO_EXECUTE_GRASP" == "true" ]]; then
  echo "[ERROR] choose only one of --auto-planned-grasp or --auto-execute-grasp" >&2
  exit 2
fi

if [[ ! -f "$ROS_SETUP" ]]; then
  echo "[ERROR] ROS setup not found: $ROS_SETUP" >&2
  echo "Set ROS_SETUP=/path/to/setup.bash or pass --ros-setup." >&2
  exit 1
fi

source_relaxed "$ROS_SETUP"
mkdir -p "$ROS_LOG_DIR"
export ROS_LOG_DIR
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/matplotlib-soarm100-ros2}"
mkdir -p "$MPLCONFIGDIR"

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
MUJOCO_CAMERA_PID=""
AUTO_GOAL_PID=""
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
  trap 'if [[ -n "${MUJOCO_PID:-}" ]]; then kill "$MUJOCO_PID" 2>/dev/null || true; fi; if [[ -n "${AUTO_GOAL_PID:-}" ]]; then kill "$AUTO_GOAL_PID" 2>/dev/null || true; fi' EXIT INT TERM
fi

if command -v conda >/dev/null 2>&1; then
  set +u
  eval "$(conda shell.bash hook)"
  conda activate "$CONDA_ENV"
  set -u
else
  echo "[WARN] conda command not found; assuming current shell already has vision deps."
fi

if [[ -n "${CONDA_PREFIX:-}" && -d "$ROS2_WS/install/soarm100_vision/lib/soarm100_vision" ]]; then
  CONDA_PYTHON="$CONDA_PREFIX/bin/python"
  for entry in "$ROS2_WS"/install/soarm100_vision/lib/soarm100_vision/*; do
    if [[ -f "$entry" && -x "$entry" ]]; then
      sed -i "1s|^#!.*python.*$|#!$CONDA_PYTHON|" "$entry"
    fi
  done
fi

if [[ "$ENABLE_MUJOCO_CAMERA" == "true" ]]; then
  echo "[soarm100_ros2] starting MuJoCo camera publisher in $CONDA_ENV"
  (
    cd "$ROOT_DIR"
    export MUJOCO_GL="${MUJOCO_GL:-egl}"
    python -m soarm100_vision.mujoco_camera_publisher_node --ros-args \
      -p repo_root:="$ROOT_DIR" \
      -p mjcf:="$MUJOCO_MJCF" \
      -p target_object:="$MUJOCO_TARGET_OBJECT" \
      -p target_pos:="$MUJOCO_TARGET_POS" \
      -p enable_obstacle:="$MUJOCO_OBSTACLE" \
      -p obstacle_body:="$MUJOCO_OBSTACLE_BODY" \
      -p obstacle_pos:="$MUJOCO_OBSTACLE_POS"
  ) &
  MUJOCO_CAMERA_PID="$!"
  trap 'if [[ -n "${MUJOCO_PID:-}" ]]; then kill "$MUJOCO_PID" 2>/dev/null || true; fi; if [[ -n "${MUJOCO_CAMERA_PID:-}" ]]; then kill "$MUJOCO_CAMERA_PID" 2>/dev/null || true; fi; if [[ -n "${AUTO_GOAL_PID:-}" ]]; then kill "$AUTO_GOAL_PID" 2>/dev/null || true; fi' EXIT INT TERM
fi

echo "[soarm100_ros2] conda_env=$CONDA_ENV"
echo "[soarm100_ros2] target=$TARGET_PROMPT avoidance=$ENABLE_AVOIDANCE"
echo "[soarm100_ros2] visualizer=$ENABLE_VISUALIZER show_window=$SHOW_WINDOW"
echo "[soarm100_ros2] mujoco=$ENABLE_MUJOCO mujoco_backend=$ENABLE_MUJOCO_BACKEND backend_mode=$MUJOCO_BACKEND_MODE inprocess_viewer=$MUJOCO_INPROCESS_VIEWER mujoco_camera=$ENABLE_MUJOCO_CAMERA sdf_backend=$ENABLE_SDF_BACKEND anygrasp_planner=$ENABLE_ANYGRASP_PLANNER obstacle=$MUJOCO_OBSTACLE obstacle_mode=$OBSTACLE_MODE sdf_cbf=$MUJOCO_SDF_CBF mjcf=$MUJOCO_MJCF target_object=$MUJOCO_TARGET_OBJECT target_pos=$MUJOCO_TARGET_POS obstacle_body=$MUJOCO_OBSTACLE_BODY obstacle_pos=$MUJOCO_OBSTACLE_POS speed=$MUJOCO_SPEED internal_tracking=$MUJOCO_INTERNAL_TRACKING track_source=$MUJOCO_TRACK_SOURCE replan_attempts=$MUJOCO_REPLAN_ATTEMPTS final_approach_timeout=$MUJOCO_FINAL_APPROACH_TIMEOUT"
echo "[soarm100_ros2] auto_planned_grasp=$AUTO_PLANNED_GRASP auto_execute_grasp=$AUTO_EXECUTE_GRASP pregrasp=$AUTO_PREGRASP_POS grasp=$AUTO_GRASP_POS quat=$AUTO_GRASP_QUAT width=$AUTO_GRIPPER_WIDTH delay=$AUTO_GOAL_DELAY"
echo "[soarm100_ros2] mujoco_python=$MUJOCO_PYTHON"
echo "[soarm100_ros2] yolo=$YOLO_MODEL"
echo "[soarm100_ros2] sam=$SAM_MODEL"
echo "[soarm100_ros2] anygrasp_sdk=$ANYGRASP_SDK_ROOT"
echo "[soarm100_ros2] anygrasp_checkpoint=$ANYGRASP_CHECKPOINT"

if [[ "$AUTO_PLANNED_GRASP" == "true" ]]; then
  if [[ "$ENABLE_MUJOCO_BACKEND" != "true" ]]; then
    echo "[ERROR] --auto-planned-grasp requires --mujoco-backend on" >&2
    exit 2
  fi
  (
    sleep "$AUTO_GOAL_DELAY"
    AUTO_ARGS=(
      --pregrasp-pos "$AUTO_PREGRASP_POS"
      --grasp-pos "$AUTO_GRASP_POS"
      --grasp-quat "$AUTO_GRASP_QUAT"
      --gripper-width "$AUTO_GRIPPER_WIDTH"
      --target-object "$MUJOCO_TARGET_OBJECT"
      --target-pos "$MUJOCO_TARGET_POS"
      --traj-log "$MUJOCO_TRAJ_LOG"
    )
    if [[ "$ENABLE_AVOIDANCE" == "true" ]]; then
      AUTO_ARGS+=(--enable-avoidance)
    fi
    ros2 run soarm100_vision send_planned_grasp "${AUTO_ARGS[@]}"
  ) &
  AUTO_GOAL_PID="$!"
fi

if [[ "$AUTO_EXECUTE_GRASP" == "true" ]]; then
  if [[ "$ENABLE_MUJOCO_BACKEND" != "true" ]]; then
    echo "[ERROR] --auto-execute-grasp requires --mujoco-backend on" >&2
    exit 2
  fi
  if [[ "$ENABLE_MUJOCO_CAMERA" != "true" ]]; then
    echo "[ERROR] --auto-execute-grasp requires --mujoco-camera on" >&2
    exit 2
  fi
  if [[ "$ENABLE_ANYGRASP_PLANNER" != "true" ]]; then
    echo "[ERROR] --auto-execute-grasp requires --anygrasp-planner on" >&2
    exit 2
  fi
  (
    sleep "$AUTO_GOAL_DELAY"
    AUTO_ARGS=(
      --target "$TARGET_PROMPT"
      --approx-target-pos "$MUJOCO_TARGET_POS"
    )
    if [[ "$ENABLE_AVOIDANCE" == "true" ]]; then
      AUTO_ARGS+=(--enable-avoidance)
    fi
    ros2 run soarm100_vision send_execute_grasp "${AUTO_ARGS[@]}"
  ) &
  AUTO_GOAL_PID="$!"
fi

ros2 launch soarm100_vision vision_grasp.launch.py \
  target_prompt:="$TARGET_PROMPT" \
  enable_avoidance:="$ENABLE_AVOIDANCE" \
  rgb_topic:="$RGB_TOPIC" \
  depth_topic:="$DEPTH_TOPIC" \
  camera_info_topic:="$CAMERA_INFO_TOPIC" \
  wrist_rgb_topic:="$WRIST_RGB_TOPIC" \
  yolo_model:="$YOLO_MODEL" \
  sam_model:="$SAM_MODEL" \
  enable_mujoco_backend:="$ENABLE_MUJOCO_BACKEND" \
  enable_mujoco_camera:="false" \
  enable_anygrasp_planner:="$ENABLE_ANYGRASP_PLANNER" \
  anygrasp_sdk_root:="$ANYGRASP_SDK_ROOT" \
  anygrasp_checkpoint:="$ANYGRASP_CHECKPOINT" \
  enable_sdf_backend:="$ENABLE_SDF_BACKEND" \
  repo_root:="$ROOT_DIR" \
  mujoco_mjcf:="$MUJOCO_MJCF" \
  mujoco_target_object:="$MUJOCO_TARGET_OBJECT" \
  mujoco_target_pos:="$MUJOCO_TARGET_POS" \
  mujoco_enable_obstacle:="$MUJOCO_OBSTACLE" \
  mujoco_obstacle_body:="$MUJOCO_OBSTACLE_BODY" \
  mujoco_obstacle_pos:="$MUJOCO_OBSTACLE_POS" \
  mujoco_traj_log:="$MUJOCO_TRAJ_LOG" \
  mujoco_python:="$MUJOCO_PYTHON" \
  mujoco_speed:="$MUJOCO_SPEED" \
  mujoco_backend_mode:="$MUJOCO_BACKEND_MODE" \
  mujoco_inprocess_viewer:="$MUJOCO_INPROCESS_VIEWER" \
  mujoco_internal_tracking:="$MUJOCO_INTERNAL_TRACKING" \
  mujoco_track_source:="$MUJOCO_TRACK_SOURCE" \
  mujoco_replan_attempts:="$MUJOCO_REPLAN_ATTEMPTS" \
  mujoco_final_approach_timeout:="$MUJOCO_FINAL_APPROACH_TIMEOUT" \
  obstacle_mode:="$OBSTACLE_MODE" \
  enable_visualizer:="$ENABLE_VISUALIZER" \
  show_window:="$SHOW_WINDOW"
