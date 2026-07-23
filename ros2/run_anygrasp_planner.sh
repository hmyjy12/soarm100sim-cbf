#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS2_WS="$ROOT_DIR/ros2"
ROS_SETUP="${ROS_SETUP:-/opt/ros/humble/setup.bash}"
CONDA_ENV="${CONDA_ENV:-graspnet_gpu}"
SDK_ROOT="$ROOT_DIR/anygrasp_sdk"
CHECKPOINT="$ROOT_DIR/anygrasp_sdk/grasp_detection/log/checkpoint_detection.tar"
ROS_LOG_DIR="${ROS_LOG_DIR:-$ROOT_DIR/logs/ros2}"

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

usage() {
  cat <<'EOF'
Usage:
  ./ros2/run_anygrasp_planner.sh [options]

Options:
  --conda-env NAME       Conda environment. Default: graspnet_gpu.
  --sdk-root PATH        AnyGrasp SDK root.
  --checkpoint PATH      AnyGrasp checkpoint tar.
  --ros-setup PATH       ROS setup.bash. Default: /opt/ros/humble/setup.bash.
  -h, --help             Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --conda-env)
      CONDA_ENV="$2"
      shift 2
      ;;
    --sdk-root)
      SDK_ROOT="$2"
      shift 2
      ;;
    --checkpoint)
      CHECKPOINT="$2"
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

if [[ ! -f "$ROS_SETUP" ]]; then
  echo "[ERROR] ROS setup not found: $ROS_SETUP" >&2
  exit 1
fi

source_relaxed "$ROS_SETUP"
mkdir -p "$ROS_LOG_DIR"
export ROS_LOG_DIR
if [[ -f "$ROS2_WS/install/setup.bash" ]]; then
  source_relaxed "$ROS2_WS/install/setup.bash"
else
  echo "[WARN] $ROS2_WS/install/setup.bash not found. Run ./ros2/run_vision_grasp.sh --build first." >&2
fi

if command -v conda >/dev/null 2>&1; then
  set +u
  eval "$(conda shell.bash hook)"
  conda activate "$CONDA_ENV"
  set -u
else
  echo "[WARN] conda command not found; assuming current env has AnyGrasp dependencies."
fi

export PATH="$SDK_ROOT/tools:$PATH"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/matplotlib-anygrasp}"

echo "[soarm100_anygrasp] conda_env=$CONDA_ENV"
echo "[soarm100_anygrasp] sdk_root=$SDK_ROOT"
echo "[soarm100_anygrasp] checkpoint=$CHECKPOINT"

ros2 run soarm100_vision anygrasp_planner_node --ros-args \
  -p sdk_root:="$SDK_ROOT" \
  -p checkpoint_path:="$CHECKPOINT" \
  -p conda_env:="$CONDA_ENV"
