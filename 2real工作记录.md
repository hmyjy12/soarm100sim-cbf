# 2Real 工作记录

本文记录 SO-ARM100 Plus 从仿真迁移到真机过程中已经确认的硬件版本、设备编号、相机标定流程和验证结果。设备节点（如 `/dev/video8`）可能在重新插拔或重启后变化，实际部署应优先使用 VID:PID 和序列号识别设备。

## 1. 主摄像头

### 1.1 设备信息

- 型号：Orbbec Gemini 336
- USB VID:PID：`2bc5:0803`
- 序列号：`CP9KB53000JX`
- 固件版本：`1.8.10`
- Orbbec SDK 版本：`2.9.3`
- Orbbec ROS 2 Wrapper 版本：`2.9.3`
- 已验证连接类型：USB 3.2
- ROS 2：Humble

项目当前使用隔离构建的 Wrapper/SDK 2.9.3：

```text
third_party/orbbec_293_ws/
```

加载环境：

```bash
source /opt/ros/humble/setup.bash
source /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_293_ws/install/setup.bash
```

已验证的双流规格：

```text
RGB:   1280 x 720, 30 FPS, MJPG
Depth:  848 x 480, 30 FPS, Y16
```

直连电脑时 RGB 与 Depth 可以同时在线。此前经过 USB Hub 时发生过 USB 设备掉线和重枚举，因此标定和性能验证阶段优先直连电脑。

设备查询：

```bash
lsusb -d 2bc5:0803
v4l2-ctl --list-devices
```

## 2. 腕部摄像头

### 2.1 设备信息

- 设备名称：RYS USB Camera
- USB VID:PID：`0bda:1376`
- 序列号：`200901010001`
- 驱动：Linux `uvcvideo`
- 视频节点（本次连接）：`/dev/video8`
- 元数据节点（本次连接）：`/dev/video9`
- 推荐采集规格：`1280 x 720`
- MJPEG：最高 60 FPS，可使用 30 FPS
- YUYV：`1280 x 720` 下最高约 10 FPS

`/dev/video8` 可能在重新插拔后变化。使用以下命令确认真实视频节点：

```bash
v4l2-ctl --list-devices

udevadm info --query=property --name=/dev/video8 | \
  grep -E '^(ID_VENDOR_ID|ID_MODEL_ID|ID_SERIAL=|ID_SERIAL_SHORT=|ID_PATH=|DEVNAME=)'
```

预期关键输出：

```text
ID_VENDOR_ID=0bda
ID_MODEL_ID=1376
ID_SERIAL_SHORT=200901010001
```

注意：系统中还出现过 `345f:9133 MS USB Video`，它是另一块复合 USB 设备，不是当前产生腕部 RGB 画面的 UVC 节点，不应作为腕部相机选择依据。

腕部相机预览：

```bash
ffplay -f video4linux2 \
  -input_format mjpeg \
  -video_size 1280x720 \
  -framerate 30 \
  /dev/video8
```

## 3. 棋盘格标定

### 3.1 棋盘格规格

- 方格数量：10 列 x 7 行
- OpenCV 内角点：9 列 x 6 行
- 实测单格边长：24.28 mm
- 传给标定程序的尺寸：`0.02428 m`

配置文件：

```text
hardware/calibration/camera/real_checkerboard.json
```

棋盘格必须固定在硬质平板上并保持平整。纸张弯曲会破坏平面棋盘模型，显著增加重投影误差。

### 3.2 安装标定工具

```bash
sudo apt-get install -y \
  ros-humble-camera-calibration \
  ros-humble-image-view
```

ROS 2 Humble 使用系统 Python 3.10。不要在 `lerobot`、`vision_seg`、`graspnet_gpu` 或 Conda `base` 的 Python 环境中运行 ROS 2 GUI。如有 Python 版本冲突，使用：

```bash
conda deactivate 2>/dev/null || true
unset PYTHONPATH PYTHONHOME
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:$PATH
source /opt/ros/humble/setup.bash

which python3
python3 --version
```

预期为 `/usr/bin/python3` 和 Python 3.10.x。

### 3.3 发布腕部相机 ROS 2 图像

终端一保持运行：

```bash
source /opt/ros/humble/setup.bash

ros2 run v4l2_camera v4l2_camera_node \
  --ros-args \
  -p video_device:=/dev/video8 \
  -p image_size:="[1280,720]" \
  -p pixel_format:=YUYV \
  -r image_raw:=/wrist/color/image_raw \
  -r camera_info:=/wrist/color/camera_info
```

首次标定前出现以下提示是正常的，表示尚未生成内参文件，不代表相机打开失败：

```text
Camera calibration file ... not found
```

检查图像频率：

```bash
ros2 topic hz /wrist/color/image_raw
```

### 3.4 实时预览

终端二：

```bash
source /opt/ros/humble/setup.bash
ros2 run rqt_image_view rqt_image_view
```

在窗口中选择：

```text
/wrist/color/image_raw
```

正式标定时可以关闭独立预览窗口，直接使用 `cameracalibrator` 自带的实时画面和角点覆盖进度。

### 3.5 腕部相机内参标定

终端一继续保持相机发布。终端二运行：

```bash
source /opt/ros/humble/setup.bash

ros2 run camera_calibration cameracalibrator \
  --size 9x6 \
  --square 0.02428 \
  --no-service-check \
  image:=/wrist/color/image_raw \
  camera:=/wrist/color
```

标定程序连续接收图像，并自动接受差异足够大的有效视角，不需要手动按快门。GUI 中：

- `X`：棋盘格覆盖图像左右区域的程度；
- `Y`：棋盘格覆盖图像上下区域的程度；
- `Size`：距离和成像尺寸变化；
- `Skew`：棋盘格倾角变化。

采集要求：

1. 棋盘格固定在平整硬板上。
2. 每个姿态稳定停留约 0.5 至 1 秒。
3. 覆盖画面中心、四边和四角。
4. 包含近、中、远距离，但避免近到失焦。
5. 包含不同倾角，但避免极端斜视。
6. 棋盘格必须完整可见。
7. 建议采集 25 至 35 个清晰且差异明显的有效姿态。

进度充分后：

1. 点击 `CALIBRATE` 计算内参；
2. 点击 `SAVE` 保存原始图像与结果；
3. 先检查重投影误差，再决定是否 `COMMIT`。

`SAVE` 默认生成：

```text
/tmp/calibrationdata.tar.gz
```

### 3.6 第一轮腕部标定结果（不建议用于最终部署）

第一轮采集保存了 53 张图像，原始结果已归档：

```text
hardware/calibration/camera/wrist_camera_1280x720_calibrationdata.tar.gz
```

第一轮内参：

```text
fx = 782.26422
fy = 766.84630
cx = 647.76562
cy = 368.98615

D = [0.128643, -0.065683, -0.011981, -0.027350, 0.0]
```

对应 YAML：

```text
hardware/calibration/camera/wrist_camera_1280x720.yaml
```

复核结果：

```text
原始图像：53 张
重新检测成功：47 张
总体 RMS：6.54 px
平均单帧误差：5.18 px
中位误差：4.03 px
最大误差：16.01 px
```

该误差过高，主要原因是纸质棋盘格明显弯曲，并存在部分过近、失焦和极端倾斜样本。该结果仅保留用于排查和流程验证，腕部相机需要使用平整硬板重新标定。目标总体 RMS 建议低于 1 px，理想范围约 0.3 至 0.8 px。

### 3.7 当前采用的腕部内参（V5）

2026-08-04 完成第五轮腕部相机标定并确认采用。该版本使用固定机械臂、移动标定板的采集方式，四个图像象限均有覆盖。

```text
保存图像：40 张
稳定重检：35 张
总体 RMS：1.38 px
平均单帧误差：1.33 px
中位误差：1.17 px
最大误差：2.48 px
```

当前正式内参：

```text
fx = 789.39512
fy = 805.93573
cx = 670.72304
cy = 361.61493

D = [0.159324, -0.200953, -0.014695, -0.008062, 0.0]
```

项目文件：

```text
hardware/calibration/camera/wrist_camera_1280x720.yaml
hardware/calibration/camera/wrist_camera_1280x720_calibrationdata_v5.tar.gz
```

V5 已作为当前 2Real 阶段腕部内参使用。其精度足以继续完成链路部署和手眼标定验证，但最终高精度抓取前仍建议使用无弯曲、无反光的专业硬质标定板复标，目标 RMS 小于 1 px。

### 3.8 显式加载内参

确认新标定结果合格后，启动相机时通过 `camera_info_url` 显式加载，不依赖 `COMMIT` 的默认文件命名：

项目已提供固定配置的一键脚本，正常使用时推荐直接运行：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
./ros2/run_wrist_camera.sh
```

脚本使用相机序列号对应的稳定设备路径，不依赖可能变化的 `/dev/video8`：

```text
/dev/v4l/by-id/usb-RYS_USB_Camera_200901010001-video-index0
```

脚本固定配置：

```text
节点：/wrist/color/wrist_camera
图像：/wrist/color/image_raw
内参：/wrist/color/camera_info
坐标系：wrist_camera_optical_frame
内参文件：hardware/calibration/camera/wrist_camera_1280x720.yaml
```

需要临时覆盖设备或内参时可使用 `--device` 和 `--calibration`。以下为脚本内部对应的完整命令，通常无需手动输入：

```bash
source /opt/ros/humble/setup.bash

ros2 run v4l2_camera v4l2_camera_node \
  --ros-args \
  -p video_device:=/dev/video8 \
  -p image_size:="[1280,720]" \
  -p pixel_format:=YUYV \
  -p camera_info_url:="file:///home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/hardware/calibration/camera/wrist_camera_1280x720.yaml" \
  -p camera_frame_id:=wrist_camera_optical_frame \
  -r image_raw:=/wrist/color/image_raw \
  -r camera_info:=/wrist/color/camera_info
```

验证内参已经加载：

```bash
ros2 topic echo /wrist/color/camera_info --once
```

验收条件：`distortion_model` 为 `plumb_bob`，并且 `d`、`k`、`r`、`p` 不再是空数组或全零矩阵。

### 3.9 后续标定顺序

1. 重新完成腕部相机内参标定并检查 RMS。
2. 读取并验证 Orbbec RGB/Depth 出厂内参。
3. 标定 Orbbec 主相机相对机器人基座的外参。
4. 标定腕部相机相对机械臂末端的手眼外参。
5. 使用同一个棋盘角点验证两个相机到机器人基座坐标系的转换误差。

### 3.10 腕部相机手眼标定（当前执行方案）

当前采用眼在手上（Eye-in-Hand）标定：棋盘格固定在工作空间，机械臂带着
腕部相机改变姿态。刚性参考帧使用 `wrist_roll`，不使用会随夹爪开合转动的
`gripper` 链接。

新棋盘打印后的实测单格边长为：

```text
9 x 6 内角点
10 x 7 外格子
实际 square_size = 14.4 mm = 0.0144 m
```

该尺寸只用于手眼标定中的 PnP 平移尺度，不影响已经完成的腕部相机内参；
因此当前 V5 内参继续使用，不因为更换棋盘格而重新标定内参。

手眼标定代码和仿真代码分离，入口如下：

```text
ros2/soarm100_vision/soarm100_vision/wrist_handeye_calibrator_node.py
ros2/soarm100_vision/soarm100_vision/wrist_handeye_pose_sequence_node.py
ros2/run_wrist_handeye.sh
ros2/run_wrist_handeye_poses.sh
hardware/calibration/handeye/wrist_handeye_poses.json
```

推荐启动顺序：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim

# 终端 1：机械臂上电保持，并发布 /joint_states 与 base -> wrist_roll TF
./ros2/run_hardware_controller.sh

# 终端 2：启动腕部 RGB 相机和当前 V5 内参
./ros2/run_wrist_camera.sh

# 终端 3：启动只读手眼标定 Viewer
./ros2/run_wrist_handeye.sh

# 终端 4：逐个审批并执行候选姿态
./ros2/run_wrist_handeye_poses.sh
```

`run_wrist_handeye.sh` 当前默认使用 `0.0144 m`。也可以显式指定：

```bash
./ros2/run_wrist_handeye.sh --square-size-m 0.0144
```

姿态序列不会自动运动。启动后先读取当前实时关节姿态作为视觉中心，需要输入：

```text
START
```

随后每个候选姿态都会打印七轴目标和变化量，只有输入完全匹配的：

```text
MOVE
```

机械臂才会移动。Viewer 中只有显示 `CAPTURE RECOMMENDED` 且完整棋盘稳定可见
时，才按空格保存样本；`TRANSITION ONLY` 仅用于回到中心姿态，不应重复采样。

建议采集 15～20 个有效姿态，覆盖腕部 pitch、yaw、roll 的正负方向以及少量
机械臂视点变化。棋盘格必须在整个采集过程中固定不动。结果保存在：

```text
logs/hardware/wrist_handeye/<timestamp>/samples.json
logs/hardware/wrist_handeye/<timestamp>/wrist_handeye_tsai.json
logs/hardware/wrist_handeye/<timestamp>/wrist_handeye_tsai.yaml
```

求解方法固定为：

```text
cv2.CALIB_HAND_EYE_TSAI
```

验收时重点查看固定棋盘反算结果的位姿离散度，而不是只看是否生成了矩阵。
### 3.11 标定起始姿态

`hardware_safe_pose.json` 只用于上电保持和异常恢复，不保证腕部相机能够看到
桌面棋盘。因此姿态序列增加了独立的标定起始姿态：

```text
hardware/calibration/handeye/calibration_seed_pose.json
```

运行姿态序列后，程序先要求输入 `MOVE_SEED`，让机械臂移动到该标定起始姿态。
确认 Viewer 中完整棋盘稳定可见后，再输入 `START`，之后才执行相对该姿态的
采样序列。每个候选运动仍需输入 `MOVE`，只有 Viewer 显示 `DETECTED` 且标记
`CAPTURE RECOMMENDED` 时才按空格采样。

如果起始姿态仍看不到棋盘，只需修改
`calibration_seed_pose.json` 中的七轴 `policy_position_rad`，不要修改
`hardware_safe_pose.json`。
## 3.12 手动初始姿态 + 一键启动手眼标定

为避免让系统把一个不合适的预设姿态误认为安全姿态，当前手眼标定支持直接使用操作者手动摆好的真实姿态作为序列参考：

1. 在控制器未启动、所有关节未上电时，手动把机械臂摆到希望的起始姿态。
2. 固定棋盘格，确认它在腕部相机视野内；棋盘格可以平放在桌面上，不要求竖直，但整个采集过程中必须保持固定。
3. 只在一个终端执行：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
./ros2/run_wrist_handeye_all.sh
```

脚本会依次启动硬件控制器、腕部相机、手眼标定 Viewer，然后前台运行姿态序列节点。控制器上电后保持手动摆好的当前姿态，节点读取 `/joint_states`，不会先移动到 `calibration_seed_pose.json`。

终端会先显示当前 7 个关节角，并等待空格确认上电。后续候选姿态使用单键：

```text
m = 批准移动
q = 退出
```

只有在 Viewer 中能看到完整、稳定棋盘格时才批准移动。机械臂到达后，在 Viewer 窗口按空格采集当前图像，再回到终端按 Enter 进入下一候选姿态。程序仍会自动跳过超出关节限位的姿态，但不再提供手动 `s` 跳过选项。

完成后按 `q` 退出 Viewer 或按 `Ctrl+C` 结束，脚本会清理相机和控制器进程；控制器的退出流程会执行全轴断力矩。

注意：手动姿态仍需满足策略关节限位，并且不能处于机械极限、碰撞风险或腕部线缆扭转风险位置。程序只做关节限位检查，不替代人工检查碰撞和线缆。

## 3.13 空格确认上电与 Viewer 清理

当前一键脚本的顺序已经改为：

1. 启动腕部相机和 Viewer，机械臂保持未上电。
2. 手动摆放机械臂和棋盘格。
3. 在启动脚本所在终端按一次空格。
4. 脚本才启动硬件控制器，上电并读取当前姿态作为手眼标定参考。

因此，启动后的第一个确认不是 `APPROVE`，而是直接按空格。后续候选姿态仍使用 `MOVE`、`s`、`q` 进行逐个确认。

脚本启动前和退出时都会清理本流程遗留的 `wrist_handeye_calibrator_node`，退出时还会调用 ROS 断力矩服务、终止底层驱动，并使用 `disable_all_torque.py` 进行兜底确认。

## 3.14 2026-08-05 手眼标定落地调整与可用结果

本日将腕部相机手眼标定从“自动姿态序列半自动 move”切换为**手动掰臂 + 上电保持 + 采集**流程，并完成第一版可用外参。自动姿态脚本 `run_wrist_handeye_all.sh` 仍保留，但当前推荐使用手动入口。

### 3.14.1 当日问题与处理

1. **僵尸硬件控制器占用服务**  
   多次启动后残留多个 `hardware_controller` / `hardware_robot_state_publisher`，导致 `/hardware/move_joint_target` 落到死节点，报错 `hardware driver is not running`。  
   已在一键/手动脚本中加强启动前与退出后清理：按进程组 `TERM→KILL`，并显式杀掉 `run_hardware_controller.py`（该驱动以 `start_new_session=True` 拉起，仅杀 ROS 节点不够）。

2. **夹爪接近标定极限导致 move 被拒**  
   报错形如 `gripper raw target ... outside safe interval`。手眼采集不需要动夹爪；手动流程中保持夹爪略张开即可。

3. **自动 move 不收敛**  
   `target did not converge` 时机械臂几乎未到位，Viewer 再按空格会因姿态几乎不变被当成重复样本。本日改为手动换姿，不再依赖 33 点自动序列完成首轮标定。

4. **采集与上电时序**  
   手动脚本改为两步空格：第一次只上电保持；松手并确认 Viewer `DETECTED` 后，第二次空格才采集，避免手仍扶着臂时采到不稳样本。

### 3.14.2 当前推荐入口与操作

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
./ros2/run_wrist_handeye_manual.sh
```

终端按键：

```text
SPACE  未上电：上电保持（不采集）
       已上电：采集 1 条样本
m      断力矩 / 下电，然后手动掰臂
s      提示到 Viewer 按 S 做 Tsai 求解
q      强制清理全部相关进程，关闭 Viewer，释放串口
```

Viewer 窗口内仍可：

```text
SPACE  本地补采
S      Tsai 求解
Q      仅退出标定节点（完整退出仍建议用终端 q）
```

手动模式关闭了相邻样本“过像就拒”的限制（`--allow-duplicates` / `reject_duplicate_samples:=false`）。棋盘须全程固定；换姿优先动 `wrist_pitch` / `wrist_jaw` / `wrist_roll`。

每成功采集一条即写入磁盘，不必等退出才保存。采够后先在 Viewer 按 `S` 求解，再按终端 `q` 退出。

### 3.14.3 代码与脚本路径

```text
# 手动一键编排（当前推荐）
ros2/run_wrist_handeye_manual.sh

# Viewer / 采集节点启动包装
ros2/run_wrist_handeye.sh
  支持 --allow-duplicates
  支持 --square-size-m（默认 0.0144）

# 腕部相机
ros2/run_wrist_camera.sh

# 硬件上电保持控制器
ros2/run_hardware_controller.sh
hardware/tools/run_hardware_controller.py
hardware/tools/disable_all_torque.py

# 核心节点源码
ros2/soarm100_vision/soarm100_vision/wrist_handeye_calibrator_node.py
  - 服务：/wrist_handeye/capture  (std_srvs/Trigger)
  - 参数：reject_duplicate_samples
  - 每次采集写 samples.json；S 求解写 tsai json/yaml
ros2/soarm100_vision/soarm100_vision/wrist_handeye_pose_sequence_node.py
ros2/soarm100_vision/soarm100_vision/hardware_controller_node.py

# 旧的自动姿态一键入口（保留，非当前主流程）
ros2/run_wrist_handeye_all.sh
ros2/run_wrist_handeye_poses.sh
hardware/calibration/handeye/wrist_handeye_poses.json
hardware/calibration/handeye/calibration_seed_pose.json

# 手眼棋盘与电机标定相关
hardware/calibration/camera/handeye_checkerboard_9x6_14_4mm.svg
hardware/calibration/lerobot/so100_plus_new_arm.json
```

远程采集服务由手动脚本在第二次 `SPACE` 时调用：

```text
/wrist_handeye/capture
```

### 3.14.4 本日标定结果（先用于联调）

会话目录：

```text
logs/hardware/wrist_handeye/20260805_110442/
  samples.json
  images/sample_000.png ... sample_025.png
  wrist_handeye_tsai.json
  wrist_handeye_tsai.yaml
```

配置摘要：

```text
样本数：26
square_size_m：0.0144
base_frame：base
gripper_frame：wrist_roll
camera_frame：wrist_camera_optical_frame
方法：cv2.CALIB_HAND_EYE_TSAI
```

验收摘要：

```text
mean PnP reprojection RMS：0.61 px          （好）
fixed board translation RMS：17.4 mm        （联调可接受；最大约 57 mm）
fixed board rotation RMS：5.9 deg           （偏大但可用；最大约 8.5 deg）
T_gripper_camera 平移模长：约 21 mm         （腕部近端安装量级合理）
姿态覆盖：平移跨度约 14–23 cm，相对首帧最大转角约 70 deg
```

**结论：** 该结果可作为当前 2Real 链路联调与粗抓取外参使用。高精度最终抓取前仍建议复标，目标大致为棋盘反算平移 RMS &lt; 10 mm、旋转 RMS &lt; 3 deg。

下游优先加载：

```text
logs/hardware/wrist_handeye/20260805_110442/wrist_handeye_tsai.yaml
```

或同目录 `wrist_handeye_tsai.json` 中的 `T_gripper_camera`。

### 3.15 Orbbec 固定相机 eye-to-hand（棋盘夹在指尖）

#### 3.15.1 配置与眼在手上 / 眼在手外的区别

**物理布置（与腕部 eye-in-hand 相反）：**

```text
Orbbec Gemini 336：完全固定在工作空间（眼在手外 / eye-to-hand）
棋盘格：夹在夹爪指尖，随臂运动
gripper_frame：wrist_roll（会话中夹爪开合锁定，勿中途改变）
棋盘：9×6 内角点，square_size_m = 0.0144
内参：Orbbec 主摄驱动发布的 /camera/color/camera_info（K + D）
       未沿用腕部相机内参，未读 wrist_handeye 标定文件
图像：/camera/color/image_raw（1280×720，depth 关）
```

**求解器相同，输入 / 输出不同：**

| | 腕部 eye-in-hand（§3.14） | Orbbec eye-to-hand（本节） |
|---|---|---|
| 相机 | 装在手腕上 | 固定在场景 |
| OpenCV | `cv2.calibrateHandEye(..., TSAI)` | 同上 |
| 喂入机器人位姿 | `T_base_gripper` | **`inv(T_base_gripper)`** |
| 棋盘观测 | `T_camera_board`（PnP） | 同上 |
| 输出外参 | `T_gripper_camera` | **`T_base_camera`** |
| 语义 | 相机坐标 → gripper | 相机坐标 → base |
| 一致性检查 | 棋盘在 **base** 下应固定 | 棋盘在 **gripper** 下应固定 |

节点内显式标注 `configuration: eye_to_hand`，`method: Tsai (..., inverted gripper poses)`；结果 `camera_frame` 为 `camera_color_optical_frame`。

#### 3.15.2 当前推荐入口与操作

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
./ros2/run_orbbec_handeye_manual.sh
```

终端按键（与 §3.14 手动腕部流程同构）：

```text
SPACE  未上电：上电保持（不采集）
       已上电：采集 1 条样本（/orbbec_handeye/capture）
m      断力矩 / 下电，然后手动掰臂（开合不变）
s      提示到 Viewer 按 S 做 Tsai 求解
q      强制清理 Orbbec launch / component_container / OpenCV GUI / hardware_controller
```

Viewer 窗口内仍可 `SPACE` 本地补采、`S` 求解、`Q` 仅退出节点。

手动模式 `reject_duplicate_samples:=false`（相邻过像不拒）。每成功采集一条即写盘；采够后在 Viewer 按 `S`，再终端 `q` 退出。

#### 3.15.3 代码与脚本路径

```text
# 手动一键编排（当前推荐）
ros2/run_orbbec_handeye_manual.sh

# Orbbec RGB 驱动（third_party/orbbec_293_ws）
ros2/run_orbbec_camera.sh

# Viewer / 采集节点包装
ros2/run_orbbec_handeye.sh
  支持 --reject-duplicates（默认关）
  支持 --square-size-m（默认 0.0144）

# 硬件上电保持（与腕部共用）
ros2/run_hardware_controller.sh
hardware/tools/disable_all_torque.py

# 核心节点源码
ros2/soarm100_vision/soarm100_vision/orbbec_eye_to_hand_calibrator_node.py
  - 服务：/orbbec_handeye/capture  (std_srvs/Trigger)
  - 订阅：/camera/color/image_raw、/camera/color/camera_info
  - 每次采集写 samples.json + sample_*.png；S 求解写 tsai json/yaml

# 棋盘（与腕部相同规格）
hardware/calibration/camera/handeye_checkerboard_9x6_14_4mm.svg
```

#### 3.15.4 两轮标定结果与分析

**第一轮（20260805_140910，26 样本）— 不可用**

```text
logs/hardware/orbbec_handeye/20260805_140910/
```

| 指标 | 数值 | 备注 |
|---|---|---|
| mean PnP RMS | 0.17 px | 图像检测正常 |
| board_in_gripper 平移 RMS | 147 mm | 极差 |
| board_in_gripper 平移 max | 298 mm | |
| board_in_gripper 旋转 RMS | 23.9 deg | |
| T_base_camera 平移模长 | ~61 cm | |
| 姿态覆盖 | 平移跨度 ~26–41 cm，最大转角 ~85 deg | |

分析：PnP 极好但「棋盘在夹爪系」几乎每相邻两帧跳变 100–300 mm / 十余～数十度，leave-one-out 去掉单帧几乎救不了全局 RMS。说明整场「板相对指尖刚体固定」假设不成立（滑动 / 重夹 / 开合变化），或外参整体解歪；不是个别「倒霉姿态」问题。

**第二轮（20260805_143740，22 样本）— 当前采用版**

```text
logs/hardware/orbbec_handeye/20260805_143740/
  samples.json
  sample_000.png ... sample_021.png
  orbbec_eye_to_hand_tsai.json
  orbbec_eye_to_hand_tsai.yaml
```

| 指标 | 第一轮 → 第二轮 | 腕部 §3.14 参考 |
|---|---|---|
| 样本数 | 26 → **22** | 26 |
| mean PnP RMS | 0.17 → **0.18 px** | 0.61 px |
| board_in_gripper 平移 RMS | 147 → **51 mm** | 17.4 mm |
| board_in_gripper 平移 max | 298 → **93 mm** | 57 mm |
| board_in_gripper 旋转 RMS | 23.9 → **8.8 deg** | 5.9 deg |
| board_in_gripper 旋转 max | 44.4 → **15.9 deg** | 8.5 deg |
| T_base_camera 平移 (m) | — | **(-0.029, 0.028, 0.638)** |
| T_base_camera 平移模长 | ~61 → **~64 cm** | — |
| 姿态覆盖 | — | 平移跨度 ~24–39 cm，最大转角 ~79 deg |

第二轮相对首轮明显改善；相邻帧 board_in_gripper 中位跳变约 70 mm / 9 deg，仍高于腕部标定水平。现场操作已认为夹持足够稳，进一步提升空间有限。

**结论（工程取舍）：** 采纳 **20260805_143740** 作为当前 2Real Orbbec 眼在手外外参。精度低于腕部 eye-in-hand，但 PnP 与姿态覆盖可支撑联调与粗抓取；高精度终版抓取前可再复标。理论目标仍为 board_in_gripper 平移 RMS &lt; 20–30 mm、旋转 RMS &lt; 5 deg。

下游优先加载：

```text
logs/hardware/orbbec_handeye/20260805_143740/orbbec_eye_to_hand_tsai.yaml
```

或同目录 `orbbec_eye_to_hand_tsai.json` 中的 `T_base_camera`（`X_base = R · X_camera + t`，frame：`camera_color_optical_frame` → `base`）。深度若已与 RGB 对齐，可共用此外参。

#### 3.15.5 复标注意点

1. 棋盘夹死后整场勿松夹、勿换夹；夹爪开合整场锁定。
2. 第一次 SPACE 仅上电；松手稳定且 Viewer `DETECTED` 后再第二次 SPACE 采集。
3. 采完一条先 `m` 下电再挪臂，避免带力换姿。
4. 关闭官方 Orbbec Viewer 后再跑脚本（USB 独占）。
5. 若相邻采集后 board_in_gripper 仍大幅跳变，优先查夹持而非继续堆样本。

