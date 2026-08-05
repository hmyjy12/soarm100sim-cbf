# ============================================================
# 3. 启动相机（日志写入文件）
# ============================================================
PID_CAM=""
if [[ ${START_CAMERA} -eq 1 ]]; then
  if [[ ! -f "${ORBBEC_DIR}/install/setup.bash" ]]; then
    echo "[Camera] [ERROR] 找不到 ${ORBBEC_DIR}/install/setup.bash"
  else
    : > "${CAMERA_LOG}"
    echo "[Camera] 日志 -> ${CAMERA_LOG}"
    (
      export FASTRTPS_DEFAULT_PROFILES_FILE="${FASTRTPS_DEFAULT_PROFILES_FILE}"
      export ROS_LOCALHOST_ONLY=0
      unset ROS_DOMAIN_ID
      cd "${ORBBEC_DIR}" || exit 1
      # shellcheck disable=SC1091
      source install/setup.bash
      echo "[Camera] 启动中... (1280x720)"
      exec ros2 launch orbbec_camera gemini_330_series.launch.py \
        color_width:=1280 color_height:=720 \
        depth_width:=1280 depth_height:=720 \
        enable_temporal_filter:=true \
        enable_spatial_filter:=true
    ) >>"${CAMERA_LOG}" 2>&1 &
    PID_CAM=$!
    disown "${PID_CAM}" 2>/dev/null || true
    echo "[Camera] PID=${PID_CAM}"
    sleep 8
    if ros2 topic list 2>/dev/null | grep -q "/camera/color/image_raw"; then
      echo "[Camera] 已在线。"
    else
      echo "[Camera] 警告：topic 未出现，可能需要等待或检查 USB。详见 ${CAMERA_LOG}"
    fi
  fi
fi