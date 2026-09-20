#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
if ! REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null)"; then
  echo "[ERROR] cannot determine the Git repository root from: $SCRIPT_DIR" >&2
  exit 2
fi
REPO_ROOT="$(realpath -e -- "$REPO_ROOT")"
APPLY="false"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/maintenance/clean_generated.sh
  ./scripts/maintenance/clean_generated.sh --apply

Without --apply this only prints what would be removed.
It removes first-party generated caches/build logs only. It does not remove
models, calibration files, checkpoints, third_party, or external SDK folders.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      APPLY="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

paths=(
  "build"
  "install"
  "ros2/build"
  "ros2/install"
  "ros2/log"
  "ros2/logs"
  "YoloWork/__MACOSX"
  "MUJOCO_LOG.TXT"
)

echo "[clean_generated] repository: $REPO_ROOT"
if [[ "$APPLY" == "true" ]]; then
  echo "[clean_generated] mode: APPLY"
else
  echo "[clean_generated] mode: dry-run"
fi
echo "[clean_generated] categories: fixed generated artifacts; Python caches and .pyc files"

is_repo_descendant() {
  local path="$1"
  [[ "$path" != "/" && "$path" != "$REPO_ROOT" && "$path" != "${HOME:-}" ]] || return 1
  [[ "$path" == "$REPO_ROOT"/* ]]
}

resolve_removal_path() {
  local requested="$1"
  local parent base resolved

  # Keep a symlink as a leaf: deleting it must never resolve or recurse into
  # its target. Its parent still has to canonically reside in this repository.
  if [[ -L "$requested" ]]; then
    parent="$(realpath -e -- "$(dirname -- "$requested")")" || return 1
    base="$(basename -- "$requested")"
    resolved="$parent/$base"
  else
    resolved="$(realpath -e -- "$requested")" || return 1
  fi

  is_repo_descendant "$resolved" || return 1
  printf '%s\n' "$resolved"
}

remove_path() {
  local requested="$1"
  local category="$2"
  local path relative size

  if [[ ! -e "$requested" && ! -L "$requested" ]]; then
    return
  fi

  if ! path="$(resolve_removal_path "$requested")"; then
    echo "[ERROR] refusing to remove a path outside the repository: $requested" >&2
    return 1
  fi
  relative="${path#"$REPO_ROOT"/}"

  if [[ "$APPLY" == "true" ]]; then
    if [[ -d "$path" && ! -L "$path" ]]; then
      rm -rf -- "$path"
    else
      rm -f -- "$path"
    fi
    echo "removed [$category]: $relative"
  else
    size="$(du -sh -- "$path" 2>/dev/null | awk '{print $1}' || true)"
    echo "would remove [$category]: $relative (${size:-unknown})"
  fi
}

for path in "${paths[@]}"; do
  remove_path "$REPO_ROOT/$path" "fixed generated artifact"
done

find_prune_args=(
  -path "$REPO_ROOT/.git" -prune -o
  -path "$REPO_ROOT/.venv" -prune -o
  -path "$REPO_ROOT/SO-ARM100" -prune -o
  -path "$REPO_ROOT/anygrasp_sdk" -prune -o
  -path "$REPO_ROOT/third_party" -prune -o
  -path "$REPO_ROOT/lerobot-main" -prune -o
  -path "$REPO_ROOT/hardware/calibration/soarm100sim_sophie" -prune -o
  -path "$REPO_ROOT/build" -prune -o
  -path "$REPO_ROOT/install" -prune -o
  -path "$REPO_ROOT/ros2/build" -prune -o
  -path "$REPO_ROOT/ros2/install" -prune -o
  -path "$REPO_ROOT/ros2/log" -prune -o
  -path "$REPO_ROOT/ros2/logs" -prune -o
  \( -type d ! -path "$REPO_ROOT" -exec test -e '{}/.git' \; \) -prune -o
)

while IFS= read -r -d '' path; do
  remove_path "$path" "Python cache"
done < <(
  find "$REPO_ROOT" "${find_prune_args[@]}" \
    -type d \( -name '__pycache__' -o -name '.pytest_cache' \) -print0 -prune
)

while IFS= read -r -d '' path; do
  remove_path "$path" "Python bytecode"
done < <(
  find "$REPO_ROOT" "${find_prune_args[@]}" \
    \( -path '*/__pycache__/*' -o -path '*/.pytest_cache/*' \) -prune -o \
    -type f -name '*.pyc' -print0
)

if [[ "$APPLY" != "true" ]]; then
  echo "[clean_generated] dry-run only. Re-run with --apply to remove these files."
fi
