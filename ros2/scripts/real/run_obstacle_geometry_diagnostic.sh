#!/usr/bin/env bash
# Perception and read-only FK only. Camera and /joint_states must already exist.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
MODE="${1:-static}"
SECONDS_TO_RECORD="${2:-60}"
case "$MODE" in static|dynamic) ;; *) echo 'Usage: bash run_obstacle_geometry_diagnostic.sh static|dynamic [seconds]'; exit 2 ;; esac
PYTHON_BIN="${VISION_PYTHON:-$HOME/anaconda3/envs/vision_seg/bin/python}"
RUN_DIR="$ROOT_DIR/log/runtime/hardware/geometry_$(date +%Y%m%d_%H%M%S)_${MODE}_$$"
mkdir -p "$RUN_DIR"
set +u
source /opt/ros/humble/setup.bash
source "$ROOT_DIR/ros2/install/setup.bash"
set -u
export PYTHONPATH="$ROOT_DIR/ros2/soarm100_vision${PYTHONPATH:+:$PYTHONPATH}"
export ROS_LOG_DIR="$RUN_DIR/ros"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$ROS_LOG_DIR"
echo "Read-only geometry diagnostic: $RUN_DIR"
# Avoid another cloud publisher or any concurrently running reach policy.
NODES="$(timeout 10 ros2 node list)"
if echo "$NODES" | rg -q '^/(so100_plus_policy_reach|soarm100_obstacle_cloud|obstacle_target_segmenter)$'; then
  echo 'Stop existing reach/perception nodes before using this standalone diagnostic.' >&2
  exit 1
fi
for TOPIC in /joint_states /camera/depth/image_raw /camera/depth/camera_info; do
  if ! timeout 8 ros2 topic echo "$TOPIC" --once --no-arr > /dev/null; then
    echo "Missing live input: $TOPIC. No controller or motor command was started." >&2
    exit 1
  fi
done
PIDS=()
cleanup() {
  trap - EXIT INT TERM
  for pid in "${PIDS[@]}"; do kill -TERM -- "-$pid" 2>/dev/null || true; done
  for pid in "${PIDS[@]}"; do wait "$pid" 2>/dev/null || true; done
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
setsid "$PYTHON_BIN" "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/target_segmenter_node.py" \
  --ros-args -r __node:=obstacle_target_segmenter \
  -p segmentation_mode:=fixed_yolo_sam -p fixed_yolo_target_class:=cup \
  -p fixed_yolo_conf:=0.01 -p fixed_yolo_device:="'0'" \
  -p fixed_yolo_model:="$ROOT_DIR/YoloWork/cup_model_package/best.pt" \
  -p sam_model:="$ROOT_DIR/models/vision/mobile_sam.pt" \
  -p rgb_topic:=/camera/color/image_raw -p depth_topic:=/camera/depth/image_raw \
  -p camera_info_topic:=/camera/depth/camera_info \
  -p mask_topic:=/obstacle/selected_mask \
  -p expanded_mask_topic:=/obstacle/selected_mask_expanded \
  -p synchronized_depth_topic:=/obstacle/selected_depth \
  -p rgb_depth_sync_tolerance_s:=0.10 \
  -p target_cloud_topic:=/obstacle/selected_cloud_camera \
  -p target_roi_cloud_topic:=/obstacle/selected_cloud_roi_camera \
  -p target_center_topic:=/obstacle/selected_center_camera \
  -p status_topic:=/obstacle/selected_segmentation_status \
  -p segment_service:=/obstacle/segment_selected \
  -p debug_dir:="$RUN_DIR/segmenter" \
  -p auto_segment_hz:=10.0 -p auto_target_prompt:=cup > "$RUN_DIR/segmenter.log" 2>&1 &
PIDS+=("$!")
PERSISTENCE_HITS=2
if [[ "$MODE" == dynamic ]]; then PERSISTENCE_HITS=1; fi
setsid "$PYTHON_BIN" "$ROOT_DIR/ros2/soarm100_vision/soarm100_vision/obstacle_cloud_node.py" \
  --ros-args -p repo_root:="$ROOT_DIR" \
  -p depth_topic:=/camera/depth/image_raw -p camera_info_topic:=/camera/depth/camera_info \
  -p use_sim_camera_extrinsics:=false \
  -p calib_json:="$ROOT_DIR/hardware/calibration/camera/real_camera_calib.json" \
  -p input_camera_name:=scene_depth -p use_robot_mask:=false \
  -p obstacle_selection_mode:=target_only -p target_mask_sync_tolerance_s:=3.0 \
  -p lock_static_target_cloud:=false -p obstacle_mode:="$MODE" \
  -p use_joint_state_self_filter:=true -p joint_sync_tolerance_s:=0.075 \
  -p self_filter_margin_m:=0.035 -p enable_wrist_attachment_box:=true \
  -p enable_attached_thin_filter:=true \
  -p workspace_x:='[0.02, 0.45]' -p workspace_y:='[-0.30, 0.30]' \
  -p workspace_z:='[0.01, 0.45]' -p remove_table_plane:=true -p table_z_max:=0.055 \
  -p persistence_voxel_size:=0.010 -p persistence_hits:="$PERSISTENCE_HITS" \
  -p persistence_forget_frames:=4 -p depth_pixel_stride:=4 \
  -p publish_rate_hz:=10.0 > "$RUN_DIR/cloud.log" 2>&1 &
PIDS+=("$!")
cp "$ROOT_DIR/hardware/calibration/camera/real_camera_calib.json" "$RUN_DIR/calibration.json"
"$PYTHON_BIN" "$ROOT_DIR/ros2/scripts/real/diagnose_obstacle_geometry.py" \
  --seconds "$SECONDS_TO_RECORD" --output "$RUN_DIR"
