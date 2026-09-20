#!/usr/bin/env bash
# 新电脑的软件环境与源码完整性检查入口。
#
# 默认模式只同步 submodule、检查基础环境并更新已初始化的 rosdep 索引；它不会安装
# ROS/GPU 驱动/CUDA，不会创建 Conda 环境，也不会构建或启动任何机器人程序。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOARM100_COMMIT="5d7c1cce4ecec709d8b8d0a394bf9b4558fad779"
ORBBEC_293_COMMIT="bfc0883a50b68f1117e449aaaac65d5675904f95"
ROS_SETUP="/opt/ros/humble/setup.bash"
CHECK_ONLY=false
FAILURES=0
WARNINGS=0

usage() {
  cat <<'EOF'
Usage:
  bash scripts/setup/bootstrap_ubuntu22.sh [--check]

Modes:
  --check  Read-only environment check. Does not update submodules, rosdep,
           packages, build outputs, or system configuration.
  default  Synchronizes/initializes submodules, verifies Ubuntu/ROS 2 Humble,
           and runs `rosdep update` only when rosdep was already initialized.

The script intentionally does not install GPU drivers, CUDA, ROS apt sources,
Python/Conda environments, camera udev rules, or build any workspace.
EOF
}

pass() { printf '[PASS] %s\n' "$*"; }
warn() { printf '[WARN] %s\n' "$*"; WARNINGS=$((WARNINGS + 1)); }
fail() { printf '[FAIL] %s\n' "$*"; FAILURES=$((FAILURES + 1)); }

source_relaxed() {
  set +u
  # shellcheck source=/dev/null
  source "$1"
  set -u
}

check_platform() {
  if [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    source /etc/os-release
    if [[ "${ID:-}" == "ubuntu" && "${VERSION_ID:-}" == "22.04" ]]; then
      pass "OS is Ubuntu 22.04"
    else
      fail "Ubuntu 22.04 is required; found ${PRETTY_NAME:-unknown}"
    fi
  else
    fail "cannot read /etc/os-release"
  fi

  if [[ "$(uname -m)" == "x86_64" ]]; then
    pass "architecture is x86_64"
  else
    fail "x86_64 is required; found $(uname -m)"
  fi
}

check_command() {
  local command_name="$1"
  if command -v "$command_name" >/dev/null 2>&1; then
    pass "command available: $command_name"
  else
    fail "required command missing: $command_name"
  fi
}

check_submodule_head() {
  local path="$1"
  local expected="$2"
  local actual
  if [[ ! -d "$REPO_ROOT/$path" ]]; then
    fail "submodule directory missing: $path"
    return
  fi
  if ! actual="$(git -C "$REPO_ROOT/$path" rev-parse HEAD 2>/dev/null)"; then
    # A stale local gitfile must not hide the pin recorded by the superproject.
    # A fresh clone has normal submodule metadata and takes the branch above.
    actual="$(git -C "$REPO_ROOT" ls-files -s -- "$path" 2>/dev/null | awk 'NR == 1 { print $2 }')"
    if [[ "$actual" == "$expected" ]]; then
      warn "submodule checkout metadata is unreadable, but the recorded gitlink is correct: $path ($actual)"
    else
      fail "submodule is not initialized as a Git checkout: $path"
    fi
    return
  fi
  if [[ "$actual" == "$expected" ]]; then
    pass "submodule pin verified: $path ($actual)"
  else
    fail "unexpected submodule commit for $path: $actual (expected $expected)"
  fi
}

check_file() {
  local relative_path="$1"
  if [[ -f "$REPO_ROOT/$relative_path" ]]; then
    pass "asset/source exists: $relative_path"
  else
    fail "required asset/source missing: $relative_path"
  fi
}

check_python_module() {
  local module_name="$1"
  if python3 -c "import $module_name" >/dev/null 2>&1; then
    pass "Python module importable: $module_name"
  else
    fail "core Python module missing: $module_name"
  fi
}

check_devices() {
  if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
    pass "NVIDIA GPU runtime is available"
  else
    warn "NVIDIA GPU runtime is unavailable; GPU-only workflows remain optional"
  fi

  if compgen -G '/dev/video*' >/dev/null; then
    pass "video device detected"
  else
    warn "no /dev/video* device detected; normal before connecting the Gemini camera"
  fi
  if compgen -G '/dev/ttyACM*' >/dev/null; then
    pass "serial ACM device detected"
  else
    warn "no /dev/ttyACM* device detected; normal before connecting the robot"
  fi
}

run_checks() {
  printf 'Repository: %s\n' "$REPO_ROOT"
  check_platform

  for command_name in git python3 cmake make gcc g++; do
    check_command "$command_name"
  done

  if [[ -f "$ROS_SETUP" ]]; then
    pass "ROS 2 Humble setup exists: $ROS_SETUP"
    source_relaxed "$ROS_SETUP"
  else
    fail "ROS 2 Humble is missing: $ROS_SETUP"
  fi
  check_command ros2
  check_command colcon

  check_submodule_head "SO-ARM100" "$SOARM100_COMMIT"
  check_submodule_head "third_party/orbbec_293_ws/src/OrbbecSDK_ROS2" "$ORBBEC_293_COMMIT"

  check_file "SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml"
  check_file "SO-ARM100/Simulation/SO100/mujoco/scene_plus_grasp_obstacle.xml"
  check_file "SO-ARM100/Simulation/SO100/mujoco/so100_plus.xml"
  check_file "third_party/orbbec_293_ws/src/OrbbecSDK_ROS2/orbbec_camera/package.xml"

  if command -v python3 >/dev/null 2>&1; then
    pass "Python version: $(python3 --version)"
    check_python_module numpy
    check_python_module mujoco
  fi

  if [[ -f "$REPO_ROOT/third_party/orbbec_293_ws/install/setup.bash" ]]; then
    pass "Orbbec 293 workspace is built"
  else
    warn "Orbbec 293 workspace has not been built yet"
  fi
  if [[ -f "$REPO_ROOT/ros2/install/setup.bash" ]]; then
    pass "main ROS 2 workspace is built"
  else
    warn "main ROS 2 workspace has not been built yet"
  fi

  check_devices
  printf 'Summary: %d failure(s), %d warning(s).\n' "$FAILURES" "$WARNINGS"
}

print_next_steps() {
  cat <<EOF

Next steps (run only after resolving any [FAIL] lines):

  source "$ROS_SETUP"

  # Install declared ROS/system dependencies after rosdep is initialized.
  cd "$REPO_ROOT/third_party/orbbec_293_ws"
  rosdep install --from-paths src --ignore-src -r -y
  colcon build --event-handlers console_direct+ --cmake-args -DCMAKE_BUILD_TYPE=Release

  cd "$REPO_ROOT/ros2"
  rosdep install --from-paths so100_plus_description soarm100_interfaces soarm100_vision --ignore-src -r -y
  colcon build --symlink-install

  source "$REPO_ROOT/third_party/orbbec_293_ws/install/setup.bash"
  source "$REPO_ROOT/ros2/install/setup.bash"
  bash "$REPO_ROOT/scripts/setup/bootstrap_ubuntu22.sh" --check

Before any hardware motion: connect the Gemini/robot, install the Orbbec udev
rules from the upstream driver instructions, and validate calibration for this
specific machine. This script never starts a robot or creates calibration data.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK_ONLY=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf '[FAIL] unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ "$CHECK_ONLY" == true ]]; then
  run_checks
  (( FAILURES == 0 ))
  exit
fi

if ! git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf '[FAIL] not a Git working tree: %s\n' "$REPO_ROOT" >&2
  exit 1
fi

check_platform
if (( FAILURES > 0 )); then
  printf '[FAIL] bootstrap stopped before changing source state.\n' >&2
  exit 1
fi

printf '[INFO] synchronizing Git submodules...\n'
git -C "$REPO_ROOT" submodule sync --recursive
git -C "$REPO_ROOT" submodule update --init --recursive

if [[ ! -f "$ROS_SETUP" ]]; then
  cat >&2 <<EOF
[FAIL] ROS 2 Humble is required but was not found at $ROS_SETUP.
Install ROS 2 Humble using the official Ubuntu 22.04 instructions, then rerun:
  https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
EOF
  exit 1
fi
source_relaxed "$ROS_SETUP"

if ! command -v rosdep >/dev/null 2>&1; then
  warn "rosdep is not installed; install it and initialize it before dependency resolution"
elif [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
  warn "rosdep is not initialized; run 'sudo rosdep init' once, then rerun this script"
else
  printf '[INFO] updating rosdep index...\n'
  rosdep update
fi

run_checks
print_next_steps
(( FAILURES == 0 ))
