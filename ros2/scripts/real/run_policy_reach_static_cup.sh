#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

usage() {
  cat <<'USAGE'
Usage:
  ./ros2/scripts/real/run_policy_reach_static_cup.sh \
    --relative-delta 0.02,0,0 \
    --relative-delta-frame tool \
    --confirm RUN_POLICY_REACH

This is the recommended preset for real-arm static cup obstacle avoidance.
It wraps run_policy_reach.sh with safer defaults:
  - obstacle selection: target-only
  - target class: cup
  - obstacle CBF: on
  - joint-limit CBF: on
  - CBF activation margin 10 cm, safe distance 7 cm, hard stop 3 cm
  - low first-test speed and acceleration limits
  - depth camera_info for Gemini 336 depth cloud geometry
  - tracking delta limit: 0.20 rad
  - success position: 0.01 m

Debug/demo overrides may include --disable-relative-delta-limit and
--obstacle-failsafe-mode hold. The latter holds the measured posture for
obstacle CBF hard-stop, infeasibility, and start-outside-training-range
conditions while the policy stays alive.

Any extra argument is forwarded to run_policy_reach.sh and can override the
preset when run_policy_reach.sh parses it later.

Relative deltas default to the legacy base frame. Pass
--relative-delta-frame tool for TCP-local +X/+Y/+Z semantics.
USAGE
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

CONFIRM_SEEN="false"
for arg in "$@"; do
  if [[ "$arg" == "RUN_POLICY_REACH" ]]; then
    CONFIRM_SEEN="true"
    break
  fi
done

if [[ "$CONFIRM_SEEN" != "true" ]]; then
  echo "[ERROR] this can move the real arm. Add --confirm RUN_POLICY_REACH" >&2
  exit 2
fi

PRESET_ARGS=(
  --rate 20
  --policy-target-tracker bounded
  --load-support position-gravity-bias
  --joint-limit-cbf on
  --obstacle-cbf on
  --obstacle-mode static
  --obstacle-gui on
  --obstacle-selection target-only
  --obstacle-target-class cup
  --obstacle-target-model YoloWork/cup_model_package/best.pt
  --obstacle-target-conf 0.25
  --obstacle-mask-refresh-hz 10.0
  --obstacle-target-mask-tolerance-s 3.0
  --obstacle-vision-device 0
  --depth-topic /camera/depth/image_raw
  --camera-info-topic /camera/depth/camera_info
  --camera-calib-json hardware/calibration/camera/real_camera_calib.json
  --obstacle-safe-distance-m 0.070
  --obstacle-activate-margin-m 0.100
  --obstacle-hard-stop-distance-m 0.030
  --obstacle-failsafe-mode hold
  --obstacle-startup-timeout-s 12.0
  --obstacle-startup-min-clouds 3
  --obstacle-cloud-timeout-s 3.0
  --max-joint-velocity-rad-s 0.10
  --max-joint-acceleration-rad-s2 0.30
  --max-tracking-error-rad 0.20
  --attached-thin-filter on
  --success-position-m 0.01
  --success-orientation-deg 8
  --timeout-s 90
)

exec "$ROOT_DIR/ros2/scripts/real/run_policy_reach.sh" \
  "${PRESET_ARGS[@]}" \
  "$@"
