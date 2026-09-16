# SO-ARM100 ROS2 开发日志

## 2026-07-21 视觉抓取链路骨架

本次新增 ROS2 视觉抓取链路的第一版结构，目标是把 MuJoCo 中已经验证过的思路迁移到 ROS2 框架下，同时保留避障开关和后续 SDF-CBF-QP 模块化接入空间。

### 新增包

```text
ros2/soarm100_interfaces
ros2/soarm100_vision
```

`soarm100_interfaces` 负责 action/service 接口：

```text
action/ExecuteGrasp.action
action/PlanGrasp.action
srv/SegmentTarget.srv
srv/SetAvoidance.srv
```

`soarm100_vision` 负责视觉相关节点：

```text
target_segmenter_node
wrist_tracker_node
debug_viewer_node
grasp_orchestrator_node
```

### 当前功能边界

当前版本是 ROS2 框架骨架，不直接替代 MuJoCo 内的抓取状态机。它先固定 topic、service、action 的边界，后续再把 AnyGrasp、policy controller、SDF-CBF-QP 接入。

### 一键启动脚本

新增：

```text
ros2/run_vision_grasp.sh
```

默认使用 `vision_seg` 环境启动 ROS2 视觉抓取骨架：

```bash
cd ~/soarm100sim_project
./ros2/run_vision_grasp.sh --build
```

已验证构建通过：

```text
soarm100_interfaces
soarm100_vision
```

注意：接口包构建必须使用系统 ROS/Python 编译环境，不能继承 conda 的 `CC/CXX/GCC/CONDA_BUILD_SYSROOT/CMAKE_PREFIX_PATH`。脚本现在的顺序是：

```text
source /opt/ros/humble/setup.bash
  -> 使用干净系统环境 colcon build
  -> source ros2/install/setup.bash
  -> conda activate vision_seg
  -> ros2 launch
```

这样避免 ROSIDL 生成接口时误用 conda Python 或 conda sysroot。

常用参数：

```bash
./ros2/run_vision_grasp.sh --target "red cube" --avoidance off
./ros2/run_vision_grasp.sh --target "red bottle" --avoidance on
./ros2/run_vision_grasp.sh --rgb-topic /camera/color/image_raw --depth-topic /camera/depth/image_rect_raw
./ros2/run_vision_grasp.sh --visualizer on --show-window on
./ros2/run_vision_grasp.sh --mujoco on --mujoco-target-object cube --mujoco-target-pos 0.42,0.08,0.021
```

脚本默认会同时启动 MuJoCo GUI：

```text
--mujoco on
```

MuJoCo GUI 来自：

```text
python mujoco/play.py --enable-grasp-chain ...
```

注意区分：

```text
MuJoCo GUI:        仿真窗口，显示机械臂和物体
debug_viewer_node: OpenCV/ROS 图像 overlay，只显示相机 RGB + mask
```

如果只想启动 ROS2 节点，不启动 MuJoCo：

```bash
./ros2/run_vision_grasp.sh --mujoco off
```

避障抓取一键脚本：

```bash
./ros2/run_obstacle_grasp.sh --build
```

等价于：

```bash
./ros2/run_vision_grasp.sh \
  --avoidance on \
  --mujoco on \
  --mujoco-obstacle on \
  --mujoco-sdf-cbf on
```

开关含义：

```text
--avoidance on
  ROS2 grasp_orchestrator 默认 enable_avoidance=true

--mujoco-obstacle on
  MuJoCo play.py 增加 --enable-obstacle，加载/显示障碍物场景

--mujoco-sdf-cbf on
  MuJoCo play.py 增加 --enable-sdf-cbf-qp，实际开启 SDF-CBF-QP 避障

--mujoco-obstacle-pos 0.16,0.09,0.02
  障碍杆 body=obstacle_rod_mount 的静态位置。XML 默认是 0.15,0.09,0.02；当前脚本默认往 +x 方向前移 1cm，提高“不开避障会碰撞/干扰”的参考性。
```

`run_vision_grasp.sh` 中 `--mujoco-obstacle auto` 和 `--mujoco-sdf-cbf auto` 默认跟随 `--avoidance`。所以：

```bash
./ros2/run_vision_grasp.sh --avoidance on
```

会默认让 ROS2 orchestrator 和 MuJoCo 避障抓取一起开启。

三组一致性测试建议：

```bash
# 1. 无障碍、无避障
./ros2/run_vision_grasp.sh --mujoco-obstacle off --mujoco-sdf-cbf off --avoidance off \
  --mujoco-traj-log log/runtime/ros2_grasp_no_obstacle_no_avoid.jsonl

# 2. 有障碍、不开避障
./ros2/run_vision_grasp.sh --mujoco-obstacle on --mujoco-sdf-cbf off --avoidance off \
  --mujoco-traj-log log/runtime/ros2_grasp_obstacle_no_avoid.jsonl

# 3. 有障碍、开启 SDF-CBF-QP 避障
./ros2/run_vision_grasp.sh --mujoco-obstacle on --mujoco-sdf-cbf on --avoidance on \
  --mujoco-traj-log log/runtime/ros2_grasp_obstacle_sdf_cbf.jsonl
```

可通过环境变量覆盖：

```text
CONDA_ENV=vision_seg
ROS_SETUP=/opt/ros/humble/setup.bash
```

当前主线设计：

```text
主相机 RGB-D
  -> YOLO-World 检测目标 bbox
  -> MobileSAM 输出目标 mask
  -> mask + depth 反投影 target_cloud / target_center
  -> AnyGrasp 规划 grasp/pregrasp/final
  -> policy 执行
  -> wrist camera 近场追踪 target center
  -> 小位移只平移抓取位姿
  -> 大位移或丢失触发 SAM + AnyGrasp replan
```

### target_segmenter_node

用途：按需执行一次目标分割。

输入 topic：

```text
/camera/color/image_raw
/camera/depth/image_rect_raw
/camera/color/camera_info
```

服务：

```text
/segment_target    soarm100_interfaces/srv/SegmentTarget
```

输出：

```text
/target/mask
/target/cloud
/target/center
/target/segmentation_status
```

默认模型路径：

```text
models/vision/yolov8s-world.pt
models/vision/mobile_sam.pt
```

注意：该节点应在 `vision_seg` 环境运行。若 `ultralytics` 或模型加载失败，节点仍可启动，但 `/segment_target` 会返回明确失败原因。

### wrist_tracker_node

用途：抓取近场时跟踪目标中心点，只估计 position 平移，不修改 AnyGrasp 给出的姿态、approach axis 和 gripper width。

输入：

```text
/wrist/depth/image_rect_raw
/wrist/depth/camera_info
/target/mask
```

重要：`/target/mask` 必须和 wrist depth 处在同一个图像坐标系。如果初始分割来自主相机，不能直接把主相机 mask 套到腕部 depth 上；需要先将目标 3D ROI 投影到腕部相机，或在腕部视角用点/框 prompt 再跑一次 SAM refinement，得到 wrist-frame mask。

输出：

```text
/target/tracked_center
/target/tracking_status
```

当前 tracking 逻辑：

```text
初始 SAM mask
  -> 计算 mask bbox
  -> 每帧在 bbox 扩张 ROI 内读取 depth
  -> 反投影局部点云
  -> median center 作为 target_center_t
  -> delta = target_center_t - target_center_0
```

状态：

```text
TRACK_OK
TRACK_WARN
TRACK_LOST_SHORT
REPLAN_REQUIRED
TRACK_ERROR
```

默认阈值：

```text
roi_expand_px      24 px
min_points         20
max_step_m         0.035 m
warn_delta_m       0.020 m
replan_delta_m     0.050 m
```

## 2026-07-22 ROS2 MuJoCo 验证闭环补充

本次把 ROS2 视觉抓取链路继续往 MuJoCo 第一验证场景靠拢，补齐了两个此前缺失的运行边界：

```text
MuJoCo RGB-D camera publisher
  -> 发布主相机/腕部相机 ROS2 topic

workspace obstacle cloud + SDF status backend
  -> 从主相机深度得到可达工作空间内的障碍点云
  -> 发布 SDF-CBF-QP backend 状态
```

### policy 与 wrist tracking 的关系

这里不要把腕部 tracking 理解成“笛卡尔伺服直接追物体”。当前设计应该是：

```text
AnyGrasp 先给 grasp pose / pregrasp pose / gripper width
  -> policy 负责追踪这个目标位姿并输出关节动作
  -> wrist tracking 只估计目标中心小位移 delta_xyz
  -> delta_xyz 只平移 pregrasp/final 的 position
  -> 姿态、roll、approach axis 仍沿用 AnyGrasp 规划结果
  -> policy 继续追踪平移后的目标位姿
```

这样做的原因是原 policy 已经验证过到达行为更平滑，tracking 只负责补偿物体被轻微推走后的目标位置变化；如果让腕部相机直接改姿态，很容易把 AnyGrasp 的候选姿态和 policy 的到达行为再次耦合乱。

当前限制：`mujoco_policy_backend_node` 仍是通过 subprocess 启动 `mujoco/play.py --grasp-source external`。这种结构可以验证 ROS2 action 到 MuJoCo 抓取状态机的打通，但不能在执行过程中实时订阅 `/target/tracked_center` 并逐步修正目标。要做真正的 ROS2 tracking 闭环，需要后续把 `play.py` 的执行循环拆成 in-process policy backend，或给 `play.py` 增加明确的实时目标更新 IPC/topic 接口。

当前折中实现：ROS2 policy backend 启动 `play.py` 时默认不再关闭 MuJoCo 内部 tracking，而是传入：

```text
--grasp-track-object
--grasp-track-source wrist
--grasp-track-max-delta 0.020
--grasp-replan-max-attempts 0
```

也就是说，仿真验证阶段仍由 `play.py` 在同一个 MuJoCo 实例内读取腕部相机并做小范围目标平移修正；policy 继续负责实际关节控制。这里暂时不在 `external` 模式下启用二次 AnyGrasp replan，因为外部 AnyGrasp 由 ROS2 planner action 管理，避免两个规划器同时抢状态。

脚本可选项：

```bash
--mujoco-internal-tracking on|off
--mujoco-track-source wrist|gt|none
```

### MuJoCo camera publisher

新增节点：

```text
soarm100_vision/mujoco_camera_publisher_node.py
```

发布 topic：

```text
/camera/color/image_raw
/camera/depth/image_rect_raw
/camera/color/camera_info
/wrist/color/image_raw
/wrist/depth/image_rect_raw
/wrist/depth/camera_info
```

启动脚本开关：

```bash
./ros2/run_vision_grasp.sh --mujoco-camera on
```

注意：当前 camera publisher 是一个独立 MuJoCo 实例，主要用于让 ROS2 视觉节点收到仿真 RGB-D topic。若要做到“相机画面、policy 执行、物体被夹动”完全共享同一个仿真状态，下一步应把 camera publisher 和 policy backend 合并到同一个 MuJoCo backend 进程。

### obstacle cloud / SDF backend

新增节点：

```text
soarm100_vision/obstacle_cloud_node.py
soarm100_vision/sdf_cbf_backend_node.py
```

当前障碍点云逻辑：

```text
主相机 depth
  -> 可选 robot/self mask 去除机械臂自身点
  -> depth 反投影为点云
  -> workspace crop，只保留机械臂可达/有意义范围
  -> table_z_max 去掉桌面附近点
  -> voxel persistence 抑制瞬时抖动
  -> /obstacle/cloud
  -> /sdf/status
```

启动脚本开关：

```bash
./ros2/run_vision_grasp.sh --sdf-backend on
```

当前限制：`sdf_cbf_backend_node` 目前是 ROS2 侧的 SDF 状态边界和诊断节点，还没有把 SDF 点云实时送进 policy 执行循环做每个 control tick 的 CBF-QP 修正。MuJoCo 内部的 `--enable-sdf-cbf-qp` 已经可用；ROS2 化后的真正避障闭环需要和上面的 in-process policy backend 一起落地。

### debug_viewer_node

用途：调试视觉链路的可视化界面。

输入：

```text
/camera/color/image_raw
/target/mask
/target/segmentation_status
/target/tracking_status
```

输出：

```text
/debug/target_overlay
```

行为：

```text
RGB 上叠加 target mask
黄色框显示 mask bbox
左上角显示 segmentation/tracking 状态文本
默认打开 OpenCV 窗口
```

启动脚本默认开启：

```bash
./ros2/run_vision_grasp.sh --visualizer on --show-window on
```

如果当前机器没有 GUI 或 OpenCV 窗口不可用，可以关闭本地窗口但保留 overlay topic：

```bash
./ros2/run_vision_grasp.sh --visualizer on --show-window off
```

然后用 ROS 工具查看：

```bash
rqt_image_view /debug/target_overlay
```

### grasp_orchestrator_node

用途：完整抓取任务的 ROS2 action 边界。

Action：

```text
/execute_grasp    soarm100_interfaces/action/ExecuteGrasp
```

Service：

```text
/set_avoidance    soarm100_interfaces/srv/SetAvoidance
```

反馈字段包含：

```text
stage
target_visible_score
grasp_score
tcp_pos_err
tcp_ori_err
sdf_min_dist
cbf_active
tracking_valid
replan_running
reason
```

当前 `grasp_orchestrator_node` 只是接口骨架，会返回：

```text
skeleton_only_policy_anygrasp_not_connected
```

这表示 policy、AnyGrasp、CBF-QP 尚未接入 ROS2 action 内部。

### 避障接入原则

避障作为控制过滤器接入，不改变抓取状态机：

```text
policy dq_nom
  -> if enable_avoidance: cbf_qp_filter(dq_nom, sdf)
  -> dq_safe
  -> robot command
```

目标物体不应同时进入 obstacle_cloud，否则 final approach 会被避障推开。

### 相机与坐标系约定

当前规划的坐标链路如下：

```text
主相机 RGB 图像坐标系 u,v
  -> YOLO-World 输出 bbox_xyxy，单位是像素
  -> MobileSAM 输出 mask，单位仍是像素
  -> mask + 主相机 depth + 主相机 CameraInfo
  -> 反投影得到 target_cloud，frame_id=主相机 optical frame
  -> AnyGrasp 使用 target_cloud，输出 grasp pose，frame_id 应保持为同一个主相机 optical frame
  -> TF: 主相机 optical frame -> robot base/world
  -> policy/控制器使用 robot base/world 下的 grasp/pregrasp/final pose
```

也就是说：

```text
YOLO-World: 2D 主相机像素坐标
SAM:        2D 主相机像素 mask
AnyGrasp:   3D 主相机 optical frame 点云/位姿
policy:     robot base/world 坐标下的目标位姿
CBF-QP:     robot base/world 坐标下的 robot state + obstacle cloud/SDF
```

腕部相机用于近场 tracking：

```text
wrist RGB-D
  -> wrist-frame mask 或 wrist-frame ROI
  -> wrist depth + wrist CameraInfo 反投影
  -> wrist optical frame 下 target_center
  -> TF 转到 robot base/world
  -> 只计算 delta position
  -> 平移原始 AnyGrasp grasp/pregrasp/final pose，姿态不变
```

重要限制：

```text
主相机 mask 不能直接套到 wrist depth 上。
```

原因是两个相机图像平面不同。正确做法是二选一：

```text
1. 将主相机 target 3D ROI 通过 TF 投影到 wrist 图像，得到 wrist ROI；
2. 在 wrist 视角用点/框 prompt 再跑一次 SAM refinement，得到 wrist mask。
```

标定需要至少提供：

```text
主相机内参 CameraInfo
腕部相机内参 CameraInfo
TF: robot base -> main camera optical frame
TF: robot base/link6/ee -> wrist camera optical frame
```

棋盘格标定主要用于确定相机外参，也就是相机 optical frame 和 robot base/world 之间的 TF。YOLO/SAM 本身不关心真实尺度；真实尺度来自 depth + CameraInfo；跨相机/跨机器人坐标的对照来自 TF。

### 后续任务

1. 拷贝视觉模型到当前项目：

```text
models/vision/yolov8s-world.pt
models/vision/mobile_sam.pt
```

2. 在 `vision_seg` 环境验证 `target_segmenter_node` 是否能加载 YOLO-World 和 MobileSAM。
3. 接入真实相机 topic 名称和 camera_info。
4. 将 `/target/cloud` 接入 AnyGrasp 规划 action。
5. 将 AnyGrasp 结果接入 policy controller。
6. 将 SDF-CBF-QP 作为可开关控制过滤器接入。

## 启动脚本可选项总表

当前主要入口：

```bash
./ros2/run_vision_grasp.sh [options]
```

避障抓取快捷入口：

```bash
./ros2/run_obstacle_grasp.sh [options]
```

`run_obstacle_grasp.sh` 会先固定：

```text
--avoidance on
--mujoco on
--mujoco-obstacle on
--mujoco-sdf-cbf on
--mujoco-traj-log log/runtime/ros2_mujoco_obstacle_sdf_cbf_grasp.jsonl
```

然后把用户后续传入的参数继续转发给 `run_vision_grasp.sh`。

### 常用坐标指定

显式指定 MuJoCo 目标物体坐标：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco-target-object cube \
  --mujoco-target-pos 0.42,0.08,0.021
```

含义：

```text
--mujoco-target-object
  选择 MuJoCo 里显示/抓取的目标物体。

--mujoco-target-pos X,Y,Z
  目标物体在 MuJoCo world 坐标系下的位置，单位 m。
```

显式指定障碍物坐标：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco-obstacle on \
  --mujoco-obstacle-pos 0.16,0.09,0.02
```

含义：

```text
--mujoco-obstacle-pos X,Y,Z
  障碍物 body 的 MuJoCo world 坐标，单位 m。
  当前默认 0.16,0.09,0.02，比 XML 默认 0.15,0.09,0.02 在 +x 方向前移 1cm。
```

### 基础选项

```text
--build
```

运行前先执行 `colcon build --packages-select soarm100_interfaces soarm100_vision`。脚本会在 build 阶段清理 conda 编译环境变量，避免 ROSIDL 被 conda Python/sysroot 污染。

```text
--target TEXT
```

ROS2 视觉目标文本 prompt，默认 `red cube`。用于后续 YOLO-World/SAM/service/action 语义目标，不等同于 MuJoCo 实体选择；MuJoCo 实体由 `--mujoco-target-object` 控制。

```text
--avoidance on|off
```

ROS2 orchestrator 默认避障开关。默认 `off`。

当 `--mujoco-obstacle auto` 和 `--mujoco-sdf-cbf auto` 时，该选项也会决定 MuJoCo 是否加载障碍物和开启 SDF-CBF-QP。

### MuJoCo 选项

```text
--mujoco on|off
```

是否同时启动 `mujoco/play.py`。默认 `on`。开启时会弹出 MuJoCo GUI；关闭时只启动 ROS2 节点。

```text
--mujoco-obstacle on|off|auto
```

是否给 `mujoco/play.py` 增加 `--enable-obstacle`。默认 `auto`，跟随 `--avoidance`。

```text
--mujoco-sdf-cbf on|off|auto
```

是否给 `mujoco/play.py` 增加 `--enable-sdf-cbf-qp`。默认 `auto`，跟随 `--avoidance`。

```text
--mujoco-obstacle-body NAME
```

要移动的 MuJoCo 障碍物 body 名称。默认 `obstacle_rod_mount`。

```text
--mujoco-obstacle-pos X,Y,Z
```

障碍物静态位置，单位 m。通过 `--obstacle-motion line --obstacle-motion-amp 0,0,0` 实现静态挪位，不修改 XML。

```text
--mujoco-target-object cube|bottle|sphere|custom
```

MuJoCo 抓取目标物体类型。默认 `cube`。

```text
--mujoco-target-pos X,Y,Z
```

MuJoCo 抓取目标物体 world 坐标，单位 m。默认 `0.42,0.08,0.021`。

```text
--mujoco-traj-log PATH
```

MuJoCo 轨迹 JSONL 日志路径。默认 `log/runtime/ros2_mujoco_grasp.jsonl`；避障快捷脚本默认 `log/runtime/ros2_mujoco_obstacle_sdf_cbf_grasp.jsonl`。

```text
--mujoco-speed SPEED
```

MuJoCo 播放倍率。默认 `0.5`，便于观察抓取过程。

### 可视化选项

```text
--visualizer on|off
```

是否启动 ROS2 debug overlay 节点。默认 `on`。这不是 MuJoCo GUI，只是 RGB/mask/status 图像调试。

```text
--show-window on|off
```

是否让 debug overlay 节点打开 OpenCV 窗口。默认 `on`。如果窗口不可用但还想保留 overlay topic，可设为 `off`，然后用 `rqt_image_view /debug/target_overlay` 查看。

### ROS2 相机 topic 选项

```text
--rgb-topic TOPIC
```

主相机 RGB topic。默认 `/camera/color/image_raw`。

```text
--depth-topic TOPIC
```

主相机 depth topic。默认 `/camera/depth/image_rect_raw`。

```text
--camera-info-topic TOPIC
```

主相机 CameraInfo topic。默认 `/camera/color/camera_info`。

```text
--wrist-depth-topic TOPIC
```

腕部相机 depth topic。默认 `/wrist/depth/image_rect_raw`。

```text
--wrist-camera-info-topic TOPIC
```

腕部相机 CameraInfo topic。默认 `/wrist/depth/camera_info`。

### 模型与环境选项

```text
--yolo-model PATH
```

YOLO-World 权重路径。默认 `models/vision/yolov8s-world.pt`。

```text
--sam-model PATH
```

MobileSAM 权重路径。默认 `models/vision/mobile_sam.pt`。

```text
--conda-env NAME
```

启动 ROS2 视觉节点前激活的 conda 环境。默认 `vision_seg`。

```text
--ros-setup PATH
```

ROS2 setup 脚本路径。默认 `/opt/ros/humble/setup.bash`。

### 三组一致性测试指令

无障碍、无避障：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco-obstacle off \
  --mujoco-sdf-cbf off \
  --avoidance off \
  --mujoco-target-object cube \
  --mujoco-target-pos 0.42,0.08,0.021 \
  --mujoco-traj-log log/runtime/ros2_grasp_no_obstacle_no_avoid.jsonl
```

有障碍、不开避障：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco-obstacle on \
  --mujoco-sdf-cbf off \
  --avoidance off \
  --mujoco-obstacle-pos 0.16,0.09,0.02 \
  --mujoco-target-object cube \
  --mujoco-target-pos 0.42,0.08,0.021 \
  --mujoco-traj-log log/runtime/ros2_grasp_obstacle_no_avoid.jsonl
```

有障碍、开启 SDF-CBF-QP 避障：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco-obstacle on \
  --mujoco-sdf-cbf on \
  --avoidance on \
  --mujoco-obstacle-pos 0.16,0.09,0.02 \
  --mujoco-target-object cube \
  --mujoco-target-pos 0.42,0.08,0.021 \
  --mujoco-traj-log log/runtime/ros2_grasp_obstacle_sdf_cbf.jsonl
```

### 2026-07-21 腕部相机换边记录

文件：`SO-ARM100/Simulation/SO100/mujoco/so100_plus.xml`

`wrist_rgb_cam_mount` 已从 `wrist_roll` 局部坐标 `pos="0 -0.031 0.036"` 改为 `pos="0 0.031 0.036"`，即沿 `y=0` 轴镜像到另一侧。当前只改位置，`quat="0 0 0.9809 0.1946"` 暂时保持不变；如果后续预览里发现视野方向不合理，再单独调整相机朝向。

### 2026-07-22 双相机标定与坐标转换落地

同步文件：

- `mujoco/constants.py`
  - `WRIST_RGB_CAM_POS_LOCAL_WRIST_ROLL` 已同步为 `(0.0, 0.031, 0.036)`，与 MJCF 中镜像后的腕部相机安装位一致。
- `mujoco/calib.py`
  - 新增 `T_target_cam_source_cam(model, data, cal, source_cam, target_cam)`。
  - 新增 `transform_points_between_cameras(model, data, cal, points_source_cam, source_cam, target_cam)`。

坐标链路：

```text
p_wrist_cam --T_scene_cam_wrist_cam(q)--> p_scene_cam

T_scene_cam_wrist_cam(q)
  = inv(T_base_scene_cam) @ T_base_wrist_roll(q) @ T_wrist_roll_wrist_cam
```

其中：

- `T_base_scene_cam`：主相机固定外参，来自标定 JSON。
- `T_wrist_roll_wrist_cam`：腕部相机静态手眼外参，来自标定 JSON。
- `T_base_wrist_roll(q)`：运行时由当前关节角 FK 实时得到。

已重新导出仿真标定：

```bash
python mujoco/calib_verify.py --out log/runtime/calib/camera_calib.json --poses 32
```

关键验证结果：

```text
FK 合成外参误差: scene=0.00e+00, wrist=1.67e-16
腕部 T_wrist_roll_cam 随机关节不变性: |dt|_max=8.84e-17m, |dR|_fro_max=2.68e-15
MJCF 标称 vs 仿真 wrist T_parent_cam: |dT|=5.88e-05
双相机转换 roundtrip_err_m=1.42e-16
```

### 2026-07-22 ROS2 视觉抓取/避障链路第一版落地

目标：把原先 MuJoCo 内部验证过的视觉抓取、腕部 tracking、workspace SDF 障碍点云思路迁移到 ROS2 结构中；MuJoCo 暂时只作为 sim backend。

#### 目标分割节点

文件：`ros2/soarm100_vision/soarm100_vision/target_segmenter_node.py`

服务：

```text
/segment_target  soarm100_interfaces/srv/SegmentTarget
```

输入：

```text
target_prompt: 用户 prompt，例如 "red cube"
force_yolo: 是否强制重新 YOLO/SAM
```

输出 topic：

```text
/target/mask           SAM 原始目标 mask
/target/mask_expanded  bbox 外扩 5% 的 ROI mask
/target/cloud          默认由原始 mask + depth 得到的目标点云
/target/cloud_roi      由 expanded mask + depth 得到的宽松 ROI 点云
/target/center         目标点云中心
/target/segmentation_status
```

默认策略：

- `mask_expand_ratio=0.05`
- 默认不把 expanded mask 用作目标点云，避免目标外环境污染 AnyGrasp 输入。
- expanded mask 保留给 ROI/debug/后续可选 AnyGrasp 宽松输入。

#### 障碍点云节点

文件：`ros2/soarm100_vision/soarm100_vision/obstacle_cloud_node.py`

输出：

```text
/obstacle/cloud
/obstacle/status
```

处理链路参考 MuJoCo `workspace_sdf`：

```text
depth
  -> 可选 /robot/mask 排除机械臂自身
  -> depth + CameraInfo 反投影点云
  -> workspace crop
  -> table/floor z 阈值过滤
  -> voxel persistence
  -> /obstacle/cloud
```

默认参数：

```text
use_robot_mask=true
workspace_x=[-0.30,0.30]
workspace_y=[-0.30,0.30]
workspace_z=[0.05,1.20]
remove_table_plane=true
table_z_max=0.055
persistence_voxel_size=0.012
persistence_hits=2
persistence_forget_frames=4
```

注意：当前 ROS2 节点以输入 depth/camera_info 的相机 frame 发布点云；接 CBF 控制前需要通过 TF/标定转到 base/world。

#### AnyGrasp 独立 action server

文件：`ros2/soarm100_vision/soarm100_vision/anygrasp_planner_node.py`

Action：

```text
/plan_grasp  soarm100_interfaces/action/PlanGrasp
```

输入：

```text
target_prompt
approximate_target_pose
target_cloud
top_k
```

输出：

```text
selected_grasp_pose
selected_pregrasp_pose
grasp_score
gripper_width
candidate_count
```

启动脚本：

```bash
./ros2/run_anygrasp_planner.sh
```

默认环境：

```text
conda_env=graspnet_gpu
sdk_root=anygrasp_sdk
checkpoint=anygrasp_sdk/grasp_detection/log/checkpoint_detection.tar
```

#### Grasp Orchestrator

文件：`ros2/soarm100_vision/soarm100_vision/grasp_orchestrator_node.py`

Action：

```text
/execute_grasp  soarm100_interfaces/action/ExecuteGrasp
```

当前已从 skeleton 升级为：

```text
SEGMENTING
  -> 调 /segment_target
  -> 读取 /target/cloud
PLANNING_GRASP
  -> 调 /plan_grasp
READY_TO_EXECUTE_POLICY
```

当前边界：

- 已完成视觉分割与 AnyGrasp planning 的 ROS2 串联。
- policy 执行 / MuJoCo sim backend / close-lift-verify 尚未接成 ROS2 backend，所以 action result 当前会返回：

```text
success=false
reason=planned_only_policy_backend_not_connected
```

这是明确边界，不是抓取失败。

#### 启动与验证

主视觉链路：

```bash
./ros2/run_vision_grasp.sh --build --mujoco off --visualizer off --show-window off
```

AnyGrasp planner：

```bash
./ros2/run_anygrasp_planner.sh
```

验证情况：

- `colcon build --packages-select soarm100_interfaces soarm100_vision` 已通过。
- `run_vision_grasp.sh --mujoco off --visualizer off --show-window off` 可启动：
  - `target_segmenter_node`
  - `obstacle_cloud_node`
  - `wrist_tracker_node`
  - `grasp_orchestrator_node`
- `run_anygrasp_planner.sh` 可启动 `AnyGrasp planner ready: action=plan_grasp`。
- 当前 Codex 沙箱里 ROS2 DDS 会报 `Operation not permitted` socket 错误，这是沙箱网络权限限制；节点仍能进入 ready。用户本机正常 ROS2 环境下不应作为功能错误处理。

下一步：

1. 增加 MuJoCo sim backend ROS2 node/action，把现有 policy 抓取状态机接到 `/execute_grasp` 后半段。
2. 将 `/obstacle/cloud` 转为 SDF-CBF-QP 控制输入，补 `/sdf/status` 和 CBF debug。
3. 把腕部 tracking 输出接入抓取执行阶段的目标平移修正与 replan 判定。

### 2026-07-22 ROS2 Policy Backend 接入

目标：让 `/execute_grasp` 不再停在 planning，而是把 ROS2 AnyGrasp 规划出的 pregrasp/final pose 传给 MuJoCo policy 状态机执行。

#### MuJoCo 外部抓取位姿入口

文件：`mujoco/play.py`

新增参数：

```text
--grasp-source anygrasp|external
--external-pregrasp-pos x,y,z
--external-grasp-pos x,y,z
--external-grasp-quat w,x,y,z
--external-gripper-width m
```

默认仍是：

```text
--grasp-source anygrasp
```

因此原先手动运行 `play.py` 的 AnyGrasp 链路不受影响。ROS2 backend 使用：

```text
--grasp-source external
```

让 MuJoCo 直接执行 ROS2 传入的 pregrasp/final/quaternion。

验证命令：

```bash
python mujoco/play.py \
  --headless --episodes 1 --target-idx 123 \
  --enable-grasp-chain \
  --grasp-source external \
  --external-pregrasp-pos 0.35,0.08,0.09 \
  --external-grasp-pos 0.39,0.08,0.06 \
  --external-grasp-quat 1,0,0,0 \
  --grasp-target-object cube \
  --grasp-target-pos 0.42,0.08,0.021 \
  --traj-log log/runtime/external_grasp_smoke.jsonl \
  --verbose \
  --no-grasp-track-object \
  --grasp-replan-max-attempts 0
```

结果：外部位姿成功进入 MuJoCo policy 状态机，并执行到 `MOVE_TO_PREGRASP -> FINAL_APPROACH -> CLOSE -> LIFT -> VERIFY`。该测试位姿是手写 smoke pose，未用于验证抓取成功率。

#### ROS2 policy backend action

新增接口：

```text
ros2/soarm100_interfaces/action/ExecutePlannedGrasp.action
```

新增节点：

```text
ros2/soarm100_vision/soarm100_vision/mujoco_policy_backend_node.py
```

Action：

```text
/execute_planned_grasp
```

职责：

```text
planned pregrasp/grasp pose
  -> 必要时从 scene_depth optical frame 转到 base/world
  -> 调用 base 环境 python 执行 mujoco/play.py --grasp-source external
  -> 解析 MuJoCo 输出中的阶段、target_lift、成功提示
  -> 返回 ExecutePlannedGrasp result
```

坐标转换：

- ROS2 AnyGrasp 输出默认在主相机 optical frame。
- MuJoCo `play.py` external pose 需要 base/world frame。
- backend 使用 `log/runtime/calib/camera_calib.json` 中 `scene_depth` 的 `T_parent_cam` 完成转换。
- ROS optical frame 到 MuJoCo camera frame 使用：

```text
D = diag(1, -1, -1)
p_mj_cam = D @ p_ros_cam
R_mj_cam = D @ R_ros_cam
p_base = R_base_mj_cam @ p_mj_cam + t_base_mj_cam
R_base = R_base_mj_cam @ R_mj_cam
```

环境：

- backend 节点本身可随 ROS2 vision launch 在 `vision_seg` 中启动。
- MuJoCo subprocess 使用 `--mujoco-python` 指定的 python，默认：

```text
python（由 PATH 或 --mujoco-python 指定）
```

避免用 `vision_seg` 或 `graspnet_gpu` 运行 MuJoCo。

#### Orchestrator 串联

文件：`ros2/soarm100_vision/soarm100_vision/grasp_orchestrator_node.py`

`/execute_grasp` 当前链路：

```text
SEGMENTING
  -> /segment_target
PLANNING_GRASP
  -> /plan_grasp
READY_TO_EXECUTE_POLICY
  -> /execute_planned_grasp
EXECUTING_POLICY
  -> 返回 lift result
```

现在 `/execute_grasp` 的最终 result 已经来自 MuJoCo policy backend，而不是固定返回 `planned_only_policy_backend_not_connected`。

#### 启动方式

主 ROS2 视觉 + orchestrator + MuJoCo policy backend：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco off \
  --mujoco-backend on \
  --visualizer off \
  --show-window off
```

AnyGrasp action server 单独在 `graspnet_gpu` 中启动：

```bash
./ros2/run_anygrasp_planner.sh
```

验证：

- `colcon build --packages-select soarm100_interfaces soarm100_vision` 已通过。
- `--mujoco-backend on` 短启动验证已看到：

```text
MuJoCo policy backend ready: action=execute_planned_grasp
grasp_orchestrator ready: action=execute_grasp
```

当前剩余关键缺口：

1. MuJoCo 相机数据尚未作为 ROS2 camera topic 发布，因此完整 `camera -> YOLO/SAM -> AnyGrasp -> policy` 需要再补 sim camera publisher，或接真实相机 topic。
2. `/obstacle/cloud` 还未接入 SDF-CBF-QP action/backend；目前只是 ROS2 点云前端。
3. 腕部 tracking 还未接到 policy backend 的实时修正，只保留了独立 `/target/tracked_center` 输出。

## 2026-07-22 算法/仿真剥离第一步

目标：停止把 `mujoco/play.py` 继续扩成真机主程序，开始把可部署算法从 MuJoCo I/O 中拆出来。当前原则：

```text
算法 core
  不 import mujoco
  不读写 MjModel/MjData
  只接收观测数据，输出控制意图/状态/诊断

MuJoCo backend
  负责仿真 qpos/qvel/camera/contact/actuator
  调用算法 core

Real backend
  后续负责真机 joint_states/camera/gripper/电流或力反馈
  调用同一套算法 core
```

### grasp_core.py

新增：

```text
ros2/soarm100_vision/soarm100_vision/grasp_core.py
```

目前抽出的内容：

```text
GraspPhase
  MOVE_TO_PREGRASP
  FINAL_APPROACH
  CLOSE
  LIFT
  VERIFY
  REPLAN_GRASP
  FAILED

GraspThresholds
  pregrasp/final/close/lift/tracking/replan 阈值

GraspPlan
  pregrasp_pos
  grasp_pos
  grasp_quat_wxyz
  approach_axis_world
  gripper_width
  score

TrackingObservation
  valid
  delta_world
  source
  confidence
  n_points

GraspObservation
  tcp_pos
  dist_to_control
  approach_error_deg
  final_err
  target_lift
  target_gripper_contacts
  tracking

GraspStateMachine
  根据观测推进状态
  输出 ControlIntent
```

这个文件不依赖 MuJoCo。它只决定：

```text
当前阶段是什么
应该追 pregrasp 还是 final 还是 lift target
夹爪应该 open/close
是否应该冻结手臂
是否应该请求 replan
是否完成或失败
```

它不会做：

```text
policy 推理
IK
CBF-QP
MuJoCo contact 读取
相机读取
关节命令发送
```

这些由 backend 负责。

### sdf_cbf_core.py

新增：

```text
ros2/soarm100_vision/soarm100_vision/sdf_cbf_core.py
```

目前抽出的内容：

```text
WorkspaceCrop
  可达空间裁剪

TableFilter
  桌面/地面 z 平面过滤

VoxelPersistence
  短窗口 voxel 记忆，避免瞬时点云抖动

SdfCloudState
  保存最新 obstacle cloud 状态并生成诊断文本
```

`obstacle_cloud_node.py` 已经改为调用 `WorkspaceCrop / TableFilter / VoxelPersistence`，节点本身只负责 ROS2 topic 输入输出。

`sdf_cbf_backend_node.py` 已经改为持有 `SdfCloudState`，节点本身只负责订阅 `/obstacle/cloud` 和发布 `/sdf/status`。

### 当前真实进度

已经完成：

```text
状态机算法 core 初版
SDF 点云前端 core 初版
ROS2 节点开始调用 core，而不是把算法写死在 node 内
py_compile 通过
```

还没有完成：

```text
play.py 主循环尚未替换为 GraspStateMachine
ROS2 MuJoCo backend 仍是 subprocess 调 play.py
SDF-CBF-QP 的逐 tick QP 修正尚未搬入 ROS2 backend
ROS2 wrist tracking 的 /target/tracked_center 尚未实时修正 policy 目标
MuJoCo camera publisher 与 policy backend 仍不是同一个 MuJoCo 实例
```

下一步应做：

```text
1. 从 play.py 抽 policy 执行 runner
2. 让 MuJoCo backend in-process 调用 GraspStateMachine
3. 把 wrist tracking delta 接入 GraspObservation
4. 把 /obstacle/cloud 转成 PointCloudSdfObstacle
5. 在 policy step 内调用 SDF-CBF-QP 修正 dq
```

## 2026-07-22 policy backend 适配层拆分

继续把 ROS2 action node 和具体仿真执行方式解耦。

新增：

```text
ros2/soarm100_vision/soarm100_vision/policy_backend_core.py
```

抽出的内容：

```text
PoseWxyz
  ROS PoseStamped 与算法内部 position/quaternion 表达的中间格式

PlannedGraspCommand
  pregrasp / grasp / gripper_width

MujocoExternalGraspConfig
  MuJoCo external grasp backend 参数

build_mujoco_external_grasp_cmd
  构造 play.py external grasp 命令

pose_to_base_from_calib
  使用 log/runtime/calib/camera_calib.json 做 camera optical -> base/world 转换

ExecutionParseState
  解析 play.py stdout 中的 stage/lift/success_hint
```

`mujoco_policy_backend_node.py` 已经改为调用 `policy_backend_core.py`。现在 node 只负责：

```text
接收 ExecutePlannedGrasp action
读取 ROS2 参数
调用 core 做 pose 转换和 backend command 构造
启动当前临时 subprocess backend
把 stdout 解析结果转成 action feedback/result
```

这一步仍然没有完成 in-process backend，但已经把“ROS action 生命周期”和“MuJoCo 执行适配器”拆开了。后续把 subprocess backend 换成 in-process MuJoCo runner 时，`ExecutePlannedGrasp` action 的外部接口不需要变。

新增轻量测试：

```text
ros2/soarm100_vision/test/test_core.py
```

覆盖：

```text
tracking 只平移 grasp/pregrasp，不修改 AnyGrasp 姿态
workspace crop + table filter + voxel persistence
MuJoCo external command builder 的 tracking/avoidance 参数
```

## 2026-07-22 MuJoCo in-process runner 初版

新增：

```text
ros2/soarm100_vision/soarm100_vision/mujoco_inprocess_runner.py
```

作用：把 MuJoCo 仿真执行从 `play.py` subprocess 逐步迁移成可被 ROS2 backend 直接调用的 runner。

当前 runner 能做：

```text
加载 MuJoCo model/data
加载 PPO policy checkpoint
复位 robot home
设置 target body 位置
接收 ROS2/AnyGrasp 已规划好的 external pregrasp/final pose
调用 GraspStateMachine 推进 MOVE_TO_PREGRASP / FINAL_APPROACH / CLOSE / LIFT
用 ReachStepper 让 policy 追踪状态机给出的目标位姿
用 MuJoCo actuator ctrl 执行关节目标
返回 success/reason/lift_height/final_phase/steps
```

`mujoco_policy_backend_node.py` 新增参数：

```text
backend_mode = subprocess | inprocess
```

脚本新增：

```bash
--mujoco-backend-mode subprocess|inprocess
```

默认仍然是：

```text
subprocess
```

原因：`play.py` 当前仍包含更完整的可视化、日志、AnyGrasp 诊断、contact 诊断和 wrist tracking 细节。`inprocess` 是迁移路径的第一版，不应立刻替代全部调试入口。

当前 in-process runner 尚未完成：

```text
未接 ROS2 /target/tracked_center 到每个 control tick
未接 ROS2 /obstacle/cloud 到 SDF-CBF-QP
未做 MuJoCo GUI viewer
未复刻 play.py 的完整抓取诊断 JSONL
未接 AnyGrasp replan，因为 AnyGrasp 规划应由 ROS2 planner action 管理
```

已验证：

```text
python py_compile 通过
inprocess runner 可加载 MuJoCo + policy 并执行短步进 smoke
```

## 2026-07-22 in-process tracking + SDF-CBF 纵向接入

本次把 in-process backend 的关键闭环接上：

```text
/target/tracked_center
  -> mujoco_policy_backend_node
  -> camera optical 转 base/world
  -> tracking_provider
  -> MujocoInProcessRunner 每个 control tick 读取
  -> TrackingObservation
  -> GraspStateMachine 只平移 pregrasp/grasp position，不修改姿态

/obstacle/cloud
  -> mujoco_policy_backend_node
  -> PointCloud2 转 xyz
  -> camera optical 转 base/world
  -> obstacle_provider
  -> MujocoInProcessRunner 每个 control tick 读取
  -> PointCloudSdfObstacle
  -> ReachStepper / solve_cbf_correction
  -> policy dq_nom + CBF-QP dq_cbf
```

改动文件：

```text
policy_backend_core.py
  新增 points_to_base_from_calib，用于 obstacle cloud 坐标转换

mujoco_policy_backend_node.py
  新增 /target/tracked_center 订阅
  新增 /obstacle/cloud 订阅
  inprocess 模式下把 tracking_provider / obstacle_provider 传给 runner

mujoco_inprocess_runner.py
  每个 tick 接收 tracking delta
  每个 tick 接收 obstacle cloud
  enable_cbf=True 时生成 PointCloudSdfObstacle 并调用 CBF-QP

vision_grasp.launch.py
  暴露 tracking_topic / obstacle_cloud_topic 参数
```

当前 `inprocess` 模式已经不再只是壳，而是具备最小完整闭环：

```text
ROS2 AnyGrasp planned pose
  -> ROS2 policy backend
  -> in-process MuJoCo runner
  -> GraspStateMachine
  -> PPO policy
  -> wrist tracking position correction
  -> obstacle cloud SDF-CBF-QP correction
  -> MuJoCo actuator control
```

仍然保留 `subprocess` 默认模式，是为了继续兼容 `play.py` 的完整 GUI/日志/诊断。后续验证 `inprocess` 稳定后，可以把默认切到 `inprocess`。

## 2026-07-22 MuJoCo 源码边界与 ROS2 in-process 可视化

边界确认：

```text
后续新功能尽量只写在 ros2/ 下
mujoco/ 作为 legacy sim helper 和现有验证入口
不再继续往 mujoco/play.py 添加新功能，除非明确需要
```

为了让 ROS2 链路也能在 MuJoCo 仿真中可视化验证，`MujocoInProcessRunner` 新增 viewer 开关：

```text
MujocoRunnerConfig.show_viewer
mujoco_policy_backend_node 参数 inprocess_viewer
run_vision_grasp.sh 参数 --mujoco-inprocess-viewer on|off
```

注意这个 viewer 属于 ROS2 in-process backend，不是 `mujoco/play.py`。因此验证“算法是否被剥离”时，应使用：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco off \
  --mujoco-backend on \
  --mujoco-backend-mode inprocess \
  --mujoco-inprocess-viewer on \
  --mujoco-camera on \
  --sdf-backend on \
  --visualizer off \
  --show-window off
```

这里：

```text
--mujoco off
  不启动 play.py

--mujoco-backend-mode inprocess
  由 ROS2 backend 直接创建 MuJoCo model/data 并执行 policy 控制循环

--mujoco-inprocess-viewer on
  打开该 in-process MuJoCo 实例的 viewer
```

这样看到的 MuJoCo 窗口来自 ROS2 backend，而不是旧 `play.py`。

## 2026-07-22 ROS2 in-process 日志与自动触发可视化

现象：

```text
只运行 run_vision_grasp.sh 时，ROS2 action server 会启动，但不会自动执行抓取。
in-process MuJoCo viewer 是在 execute_planned_grasp action 真正开始执行后才创建的。
所以如果没有发送 action goal，即使 --mujoco-inprocess-viewer on，也不会看到 MuJoCo GUI。
```

本次补充：

```text
soarm100_vision/send_planned_grasp_node.py
  新增 ExecutePlannedGrasp action client

setup.py
  注册命令：ros2 run soarm100_vision send_planned_grasp

run_vision_grasp.sh
  新增 --auto-planned-grasp on|off
  新增 --auto-pregrasp-pos X,Y,Z
  新增 --auto-grasp-pos X,Y,Z
  新增 --auto-grasp-quat W,X,Y,Z
  新增 --auto-gripper-width M
  新增 --auto-goal-delay SEC

mujoco_policy_backend_node.py
  inprocess 模式下把 action goal 的 traj_log 传给 MujocoInProcessRunner
```

ROS2 in-process runner 现在会写逐步 JSONL：

```text
默认：log/runtime/ros2_inprocess_grasp.jsonl
脚本指定：--mujoco-traj-log PATH
```

每行主要字段：

```text
step / t / phase / reason
q_before / q_target
tcp_pos / control_target / pregrasp / grasp
dist_to_control / final_err
target_lift / best_lift
gripper_mode
tracking_valid / tracking_delta / tracking_source
obstacle_points
cbf_enabled / cbf_active / h_min / dq_nom_norm / dq_cbf_norm / dq_total_norm
```

用于验证“ROS2 算法链路 + MuJoCo 仿真 backend + GUI”的推荐命令：

```bash
./ros2/run_vision_grasp.sh \
  --mujoco off \
  --mujoco-backend on \
  --mujoco-backend-mode inprocess \
  --mujoco-inprocess-viewer on \
  --mujoco-camera on \
  --sdf-backend on \
  --auto-planned-grasp on \
  --mujoco-target-object cube \
  --mujoco-target-pos 0.42,0.08,0.021 \
  --mujoco-traj-log log/runtime/ros2_inprocess_grasp.jsonl \
  --visualizer off \
  --show-window off
```

这里没有启动旧的 `mujoco/play.py`：

```text
--mujoco off
  不启动 legacy play.py

--mujoco-backend-mode inprocess
  ROS2 policy backend 在当前进程里创建 MuJoCo model/data 并执行 policy 控制循环

--auto-planned-grasp on
  自动发送一次 ExecutePlannedGrasp goal，否则 backend 只是等待 action，不会弹出 viewer
```

当前仍需注意：

```text
--mujoco-camera on 当前还是单独的 MuJoCo camera publisher 实例。
这能验证 ROS topic 形态，但还不是和 in-process policy runner 完全同一个 MuJoCo 实例。
如果要做严格一致的闭环，下一步应把相机 topic publisher 合并进 in-process runner。
```

### 2026-07-22 in-process viewer 未出现问题修复

现象：

```text
auto planned grasp goal accepted
feedback stage=STARTING_MUJOCO_INPROCESS
result success=False reason=inprocess_backend_failed:no running event loop
没有 MuJoCo GUI
```

原因：

```text
mujoco_policy_backend_node 的 inprocess 分支曾使用 asyncio.to_thread(...)
rclpy action callback 当前执行上下文没有 running asyncio event loop
所以 runner 尚未真正进入 MuJoCo 控制循环就失败
viewer 也没有机会创建
```

修复：

```text
mujoco_policy_backend_node.py
  inprocess 分支改为同步调用 MujocoInProcessRunner.run(...)
  不再通过 asyncio.to_thread 启动 MuJoCo runner
```

这个修复只影响 ROS2 in-process backend，不影响 legacy `mujoco/play.py`。

### 2026-07-22 ROS2 console script Python 环境修复

现象：

```text
inprocess_backend_failed:No module named 'mujoco'
```

排查结果：

```text
vision_seg 环境中实际有官方 mujoco 包
但 ros2/install/soarm100_vision/lib/soarm100_vision/* 的 shebang 是 #!/usr/bin/python3
所以 ros2 run 启动 soarm100_vision 节点时没有使用 vision_seg/bin/python
系统 Python 环境没有 mujoco，因此 in-process backend import 失败
```

修复：

```text
run_vision_grasp.sh
  conda activate vision_seg 后
  自动把 install/soarm100_vision/lib/soarm100_vision/* 的 shebang 改为当前 CONDA_PREFIX/bin/python
```

这样即使 `colcon build` 仍使用系统 Python 构建 ROS2 interface，运行时的纯 Python 节点也会使用 `vision_seg`，同时保留 ROS Humble 的 Python 3.10 ABI 兼容性。

### 2026-07-22 in-process viewer 实时播放修复

现象：

```text
action 能执行，但 MuJoCo viewer 可能看不到或一闪而过
```

原因：

```text
MujocoInProcessRunner 之前没有按 wall-clock sleep
仿真会尽快跑完整个 episode
viewer 创建后很快随 runner finally close
```

修复：

```text
MujocoRunnerConfig.speed
MujocoRunnerConfig.viewer_hold_s

viewer 开启时：
  每个 control tick 后 sleep(ctrl_dt / speed)
  终止前保留 viewer_hold_s 秒
```

`run_vision_grasp.sh` 现在会把 `--mujoco-speed` 传给 in-process backend。比如 `--mujoco-speed 0.5` 会按半速播放，更适合肉眼观察。

已验证：

```text
非 GUI ROS2 in-process action smoke：
  MOVE_TO_PREGRASP -> FINAL_APPROACH -> CLOSE -> LIFT -> REPLAN_GRASP
  写出 log/runtime/ros2_inprocess_action_smoke.jsonl，共 450 行

GUI smoke：
  inprocess_viewer=true 时无 import/GLFW 报错
  feedback 约按实时节奏输出
```

### 2026-07-22 in-process 动态目标初始化修复

现象：

```text
ROS2 in-process GUI 可弹出
但启动后所有几何体/目标物体开局弹飞
```

原因：

```text
scene_plus_norod.xml 中 cube/bottle/sphere 都是 freejoint 动态体
runner 之前只改 model.body_pos，没有写 freejoint 对应的 data.qpos/data.qvel
同时未选目标仍保持 contype/conaffinity=1，地下停放的 bottle/sphere 也会参与碰撞
```

修复：

```text
MujocoInProcessRunner._configure_grasp_targets(...)
  根据 target_object 选择 cube/bottle/sphere
  选中目标保持红色可碰撞
  未选目标设为透明且 contype/conaffinity=0，并停放到 z=-1

MujocoInProcessRunner._set_target_body(...)
  对 freejoint 动态体写 data.qpos:
    qpos[0:3] = target xyz
    qpos[3:7] = identity quaternion
  同时清零对应 qvel

MujocoInProcessRunner._settle_object(...)
  放置目标后先纯物理 settle 0.75s
  settle 后清零 qvel，再进入 policy 控制
```

验证：

```text
log/runtime/ros2_inprocess_gui_init_fixed.jsonl
rows=231
target_lift min=0.0 max=0.0
phases={'MOVE_TO_PREGRASP': 42, 'FINAL_APPROACH': 10, 'CLOSE': 40, 'LIFT': 40, 'REPLAN_GRASP': 99}
```

结论：开局 0.176m 级别的 target_lift 异常已消失；当前 planned-grasp smoke 的后续失败不再是几何体初始化爆飞，而是手写 pregrasp/final 位姿本身并非 AnyGrasp 真正规划结果。

### 2026-07-22 ROS2 接入真实 AnyGrasp 输出位姿

目标：`/execute_grasp` 不再使用手写 planned grasp，而是走完整链路：

```text
MuJoCo camera publisher
  -> /camera/color + /camera/depth
  -> target_segmenter_node 生成 /target/cloud
  -> anygrasp_planner_node 调 graspnet_gpu/AnyGrasp
  -> grasp_orchestrator_node 转发 AnyGrasp selected pregrasp/grasp
  -> mujoco_policy_backend_node 转成 base/world 后交给 in-process policy runner
```

本次修复：

```text
anygrasp_planner_node
  打印 top candidates:
    frame / score / width / pos / approach

grasp_orchestrator_node
  打印转发给 policy 的 selected_pregrasp_pose / selected_grasp_pose

mujoco_policy_backend_node
  打印 raw camera-frame pose 和 converted base-frame pose
  修复 PoseStamped header 被 set_pose_like 原地污染的问题

policy_backend_core
  新增 pose_to_base_from_mujoco_camera()
  ROS2 仿真默认使用当前 MJCF 中的 scene_depth 相机外参做转换
  真机/离线标定可关闭 use_sim_camera_extrinsics 后回到 calib_json

vision_grasp.launch.py
  将 mujoco_traj_log 传给 orchestrator/backend
  将 target_object/target_pos/default_traj_log 传给 backend

mujoco_inprocess_runner
  接通 replan_max_attempts 参数，避免当前没有二次规划回调时卡在空 replan
```

关键诊断：

```text
旧 log/runtime/calib/camera_calib.json 中 scene_depth:
  T_base_cam ~= pos=(0.03,0.00,0.55) + 倾角

当前 MJCF 中 scene_depth:
  T_base_cam ~= pos=(0.32,0.10,0.62) + 单位旋转

因此用旧 JSON 转换 AnyGrasp pose 会把目标从 cube 附近转飞。
```

验证输出：

```text
AnyGrasp raw grasp:
  frame=scene_depth_optical
  pos=(+0.100,+0.010,+0.576)
  quat=(-0.454,+0.479,+0.603,+0.449)

policy converted base grasp:
  frame=base
  pos=(+0.420,+0.090,+0.044)
  quat=(-0.479,-0.454,-0.449,+0.603)

target:
  cube pos=(+0.420,+0.080,+0.022)
```

结论：ROS2 链路现在已经在使用 AnyGrasp 的真实输出位姿；此前错位主要来自 ROS2 policy backend 使用过期相机外参。当前剩余抓取失败主要是执行/夹持/lift 层问题，而不是 AnyGrasp 位姿没有接入。

### 2026-07-22 ROS2 MuJoCo 障碍物开关与位置参数

目标：让 ROS2 in-process policy backend、MuJoCo camera publisher、SDF-CBF-QP 避障点云看到同一个仿真场景，避免只在旧 `play.py` 分支显示障碍物。

新增/接通：

```text
run_vision_grasp.sh
  --mujoco-obstacle on|off|auto
  --mujoco-obstacle-body NAME
  --mujoco-obstacle-pos X,Y,Z

自动 MJCF:
  obstacle=on  -> SO-ARM100/Simulation/SO100/mujoco/scene_plus_grasp_obstacle.xml
  obstacle=off -> SO-ARM100/Simulation/SO100/mujoco/scene_plus_norod.xml
```

参数流向：

```text
run_vision_grasp.sh
  -> mujoco_camera_publisher_node:
       mjcf / enable_obstacle / obstacle_body / obstacle_pos
  -> vision_grasp.launch.py
  -> mujoco_policy_backend_node:
       mjcf / enable_obstacle / obstacle_body / obstacle_pos
  -> MujocoInProcessRunner:
       加载同一个 mjcf，并把 obstacle_body 放到 obstacle_pos
```

坐标转换：

```text
AnyGrasp grasp pose:
  scene_depth_optical -> 当前 MJCF scene_depth 外参 -> base

Obstacle cloud:
  scene_depth_optical -> 当前 MJCF scene_depth 外参 -> base
```

注意：

```text
--avoidance on
  只表示 ExecuteGrasp goal 中 enable_avoidance=true，policy backend 会启用 CBF。

--sdf-backend on
  启动 ROS2 SDF-CBF 状态节点。

--mujoco-obstacle on
  才会让 in-process MuJoCo backend 和 camera publisher 都加载带障碍物场景。
```

### 2026-07-23 ROS2 运行中 Replan 闭环

目标：第一次抓取或 lift 失败后，不重启 MuJoCo、不回到物体初始位置，而是在同一个仿真实例中重新观察当前场景、重新计算 AnyGrasp，并继续下一轮抓取。

当前链路：

```text
GraspStateMachine:
  tracking 大位移或 lift_failed
  -> REPLAN_GRASP
  -> should_plan_grasp=true

MujocoInProcessRunner:
  暂停机械臂控制循环
  -> 从当前 model/data 发布 scene_depth + wrist_rgb RGB-D
  -> 请求 segment_target

TargetSegmenter:
  使用最新主相机 RGB-D
  -> YOLO-World + SAM
  -> 发布新的 /target/cloud

MujocoPolicyBackend:
  等待 cloud 序号更新
  -> 调用 /plan_grasp
  -> AnyGrasp 返回候选和选中位姿
  -> scene_depth_optical 转 base
  -> sm.accept_replan(new_plan)

StateMachine:
  MOVE_TO_PREGRASP
  -> FINAL_APPROACH
  -> CLOSE
  -> LIFT
```

关键修复：

```text
1. policy backend 使用 MultiThreadedExecutor + ReentrantCallbackGroup。
   MuJoCo 控制循环运行时，ROS2 仍可处理 tracking、点云、service 和 action。

2. 执行期 RGB-D 来自 policy backend 正在控制的同一个 MuJoCo model/data。
   独立 mujoco_camera_publisher 收到 /mujoco/backend_camera_active=true 后暂停，
   防止把初始静态场景的旧画面混入 replan。

3. ExecutePlannedGrasp.action 新增 target_prompt。
   replan 会沿用首次抓取的语义目标，而不是退化成固定 cube。

4. YOLO-World 缓存当前 prompt。
   同一 prompt 二次分割不重复 set_classes，避免 CPU/CUDA index_select 设备冲突。

5. replan 成功和失败均写入轨迹 JSONL：
   event=replan_accept / replan_reject
   attempt / reason / pregrasp / grasp / grasp_quat / gripper_width

6. 总控制 step 预算按抓取尝试数扩展：
   total_step_budget = max_steps * (1 + replan_max_attempts)

7. LIFT 失败会先检查 replan 次数。
   `--mujoco-replan-attempts N` 严格表示最多重新调用 N 次 AnyGrasp，
   不会在最后一次失败后多发一次规划请求。
```

新增启动参数：

```text
--mujoco-replan-attempts N
```

默认值：

```text
N=2
```

真实 AnyGrasp 冒烟验证：

```text
初次 AnyGrasp:
  target_cloud=576 points
  candidates=6
  score=0.321
  base_grasp=(+0.420,+0.090,+0.044)

lift_failed 后运行中 replan:
  fresh target_cloud=612 points
  candidates=11
  score=0.207
  elapsed=3.92s
  new base_grasp=(+0.454,-0.005,+0.052)

结果：
  新点云、第二次 AnyGrasp、新位姿坐标转换和状态机回填均已实际触发。
```

## 2026-07-23：ROS2 AnyGrasp IK 与关节限位筛选

本次将候选可达性筛选接入 ROS2 `anygrasp_planner_node`，不再只按
AnyGrasp 分数选择候选。

筛选链路：

```text
AnyGrasp 候选（按 score 降序）
  -> AnyGrasp 坐标轴映射到 policy TCP
     AnyGrasp +x(approach) -> TCP +z
     AnyGrasp +y(closing)  -> TCP +x
  -> scene_depth_optical 转 base
  -> pregrasp 有界数值 IK
  -> final grasp 有界数值 IK
  -> 检查全部机械臂关节上下限
  -> 选择第一个通过的高分候选
```

默认门槛：

```text
候选 top_k                         45
IK 位置误差                       <= 0.005 m
IK 进刀轴角度误差                 <= 3.0 deg
IK 最大迭代                       100
关节角                            必须处于 MuJoCo joint range
```

说明：

- `3 deg` 检查的是抓取进刀轴，而不是强制完整 roll 误差小于 `3 deg`。
  完整 AnyGrasp roll 仍会交给 policy；用完整 roll 作为硬 IK 门槛会对
  SO-ARM100 产生大量不可达误判。
- IK 每步都将关节角裁切到 `q_low/q_high`，最终同时打印最小关节限位余量。
- 日志逐候选打印 `pre_err`、`final_err`、进刀轴误差、`joint_margin`
  和最终关节角，便于定位候选为何被拒绝。

端到端验证：

```text
候选 0..3：IK 拒绝
候选 4：通过
pregrasp error = 4.3 mm / 0.1 deg
final error    = 3.7 mm / 0.0 deg
min joint margin = 0.639 rad
q_final = [0.208, -0.550, 0.639, -0.740, -0.255, 0.608]
```

MuJoCo 默认播放速度已由 `0.5` 恢复为 `1.0`。未开启相机预览窗口时，
主相机和腕部相机仍在后台渲染并发布 RGB-D topic；预览开关只影响显示。

## 2026-07-24：MuJoCo GUI 抓取位姿诊断

ROS2 in-process MuJoCo GUI 新增 AnyGrasp 选中位姿可视化：

```text
青色球：pregrasp
绿色球：转换到 base/world 后的 final grasp
紫色球：实时 policy TCP
白线：final grasp 到目标物体实时中心的偏差
红轴：final TCP +x（夹爪闭合轴）
绿轴：final TCP +y
蓝轴：final TCP +z（进刀轴）
```

轨迹 JSONL 同步新增：

```text
target_object_pos
grasp_target_offset
grasp_target_dist
```

GUI 使用转换后的世界系目标，因此绿色球与物体固定偏离时优先检查相机外参；
绿色球正确但紫色球未重合时检查 policy 跟踪和 TCP 定义。

## 2026-07-24：事件驱动主相机与纯 RGB 腕部 tracking

### 相机调度

新增 `--obstacle-mode static|dynamic`。

`static` 默认模式：

```text
启动后主相机 RGB-D 采集 5 个稳定帧
→ YOLO-World + SAM + AnyGrasp
→ 静态障碍点云短窗口一致性过滤并冻结
→ 执行阶段停止主相机连续渲染
→ 腕部仅渲染 RGB（约 10 Hz）
→ tracking lost / 抓取失败时临时恢复一帧主相机 RGB-D
→ 等待 0.15 s 让 ROS2 消费新帧后再请求 SAM + AnyGrasp replan
```

`dynamic` 模式：

```text
主相机 RGB 仍只用于初次识别和 replan
主相机 depth 在执行阶段约 10 Hz 连续更新
→ robot self removal
→ workspace crop
→ table removal
→ 短窗口 voxel persistence
→ SDF-CBF-QP
腕部仍只使用 RGB tracking
```

不再渲染或发布腕部 depth。

### 腕部 RGB tracking

新增接口：

```text
soarm100_interfaces/msg/TrackedTarget2D
```

链路：

```text
主相机目标点云中位中心
→ 随 PlanGrasp / ExecutePlannedGrasp action 传给 backend
→ 使用实时 MuJoCo wrist camera 位姿投影到腕部图像
→ 发布期望 ROI
→ 腕部 RGB 多尺度局部模板匹配
→ 同帧 observed pixel - expected pixel
→ 使用当前相机深度估计和动态相机旋转转换成世界系小平移
→ 只平移 pregrasp/final，保持 AnyGrasp 姿态和宽度
```

重要修复：

- 不再把主相机 SAM mask 直接当作腕部 mask。
- 不再使用固定腕部相机外参直接转换 tracking 点。
- tracking 参考是目标点云中心，不是 AnyGrasp grasp point。
- 像素误差使用同帧期望位置，避免 ROS2 异步延迟将相机运动误判为物体运动。
- 搜索窗锚定动态投影 ROI，加入 `0.70/0.85/1.0/1.20/1.40` 多尺度匹配，防止漂到背景。

### 验证数据

同一静止 cube、同一抓取位姿：

```text
旧实现（固定模板 + 异步当前相机位姿）：
  valid tracking steps = 389
  median |delta| = 49.8 mm
  max |delta| = 70.0 mm

纯 RGB 同帧多尺度实现：
  valid tracking steps = 318 / 490
  first delta = 0 px / 0 mm
  median |delta| = 6.1 mm
  p95 |delta| = 15.5 mm
  max |delta| = 15.9 mm
```

当前小范围 tracking 门槛为 `20 mm`，验证结果均未越过该门槛。

动态障碍模式冒烟验证：

```text
control rows = 285
rows with obstacle cloud = 285
max obstacle points = 3496
rows with CBF active = 285
```

性能修复：障碍点云新增递增序号。SDF 现在只在新的 depth/point-cloud
帧到达时重建，50 Hz 控制循环的其余步骤复用已有 SDF，不再对同一份点云
重复建场。

## 2026-07-28：动态目标 tracking 与 CLOSE 解耦

本轮将腕部 tracking、闭合和 replan 的职责边界固定为：

```text
MOVE_TO_PREGRASP / FINAL_APPROACH
  → 腕部 RGB 只修正 AnyGrasp 给出的目标位置，姿态保持不变
  → final_err <= 15 mm
  → tracking confidence >= 0.45
  → target speed <= 5 mm/s
  → 三项连续稳定 0.20 s
COMMIT_GRASP
  → 锁定当前 grasp pose
  → 停止目标物体的测试运动
  → 完全冻结 tracking 修正
CLOSE
  → 保持锁定的机械臂位姿并闭合夹爪
LIFT
  → 成功则 VERIFY
  → 仅在 lift 失败后进入 REPLAN_GRASP
```

因此，腕部低置信度或目标位移不再于 `FINAL_APPROACH` 阶段提前触发
replan。replan 只用于处理已经执行过 `CLOSE + LIFT` 的失败抓取；新方案
被接受后才重新启用 tracking。

动态 cube 使用世界系 Y 轴往复运动：

- 默认关闭：`--mujoco-target-motion none`
- 开启：`--mujoco-target-motion line`
- 半行程：`--mujoco-target-motion-amplitude 0.05`
- 从 `+Y` 端点到 `-Y` 端点时间：`--mujoco-target-motion-travel-time 2.0`
- 每个端点停留：`--mujoco-target-motion-dwell-time 1.0`
- 首次有效腕部 tracking 后的静止时间：
  `--mujoco-target-motion-delay 0.5`

运动采用余弦速度曲线，从初始中心连续启动，不发生位置跳变；在
`COMMIT_GRASP/CLOSE/LIFT/REPLAN_GRASP` 阶段停止主动运动。

根据首轮动态测试日志，进一步修正：

- 轨迹时间改用 ROS2 控制周期，不再误用 MuJoCo physics 子步时间。
- tracking 开启时，cube 等到第一帧有效腕部 tracking 后才开始延时和运动。
- 仿真只在 tracker 初始化时使用 cube 实际中心建立投影参考，后续位移仍由
  腕部 RGB tracker 输出，不逐帧读取物体真值。
- tracker 搜索窗由“固定投影 hint”改为跟随上一帧成功 bbox。
- tracker reason 新增 `frame_shift` 和 `reference_residual` 像素诊断。
- 稳定 CLOSE 距离设为 `35 mm`，近场超时 CLOSE 距离设为 `40 mm`。

轨迹 JSONL 新增诊断字段：

- `tracking_frozen`
- `close_gate`
- `target_motion_phase`
- `target_commanded_pos`
- `target_velocity`
- `target_speed`

`ros2/run_vision_grasp.sh --build` 同时显式固定系统 C/C++ 编译器，避免
旧 CMake 缓存误用 Conda 编译器导致 ROS2 interface 构建失败。

## 2026-07-28：默认颜色分割与腕部颜色 tracking

目标视觉来源新增统一开关：

```bash
--target-segmentation color|yolo_sam
```

默认值为 `color`，因此默认不会加载或运行 YOLO-World 和 SAM。主相机和
腕部相机共用以下颜色参数：

```bash
--target-color-rgb 255,0,0
--color-hue-tolerance 18
```

颜色检测内部使用 HSV 环形 hue 距离，并使用饱和度、亮度和连通域面积
过滤。主相机选择最大有效同色连通域，结合 depth 生成目标点云；腕部
相机选择距离上一帧目标中心最近的同色连通域，直接输出 bbox 中心用于
位置 tracking。

腕部颜色 tracking 包含：

- 最小连通域面积过滤；
- 最大单帧中心跳变过滤；
- 丢失帧计数；
- `area/frame_shift/reference_residual` 日志；
- 不再使用可能漂移到背景的灰度模板相关系数。

动态目标的 tracking 修正范围从 `20 mm` 提高到 `80 mm`，以覆盖默认
Y 轴 ±50 mm 测试范围。需要恢复原视觉链路时使用：

```bash
--target-segmentation yolo_sam
```

## 2026-08-07：固定类别 YOLO + SAM 的 2Real 第一版

新增可选目标分割来源 `fixed_yolo_sam`。职责保持解耦：

```text
Orbbec RGB
  -> YoloWork 固定类别模型（只输出类别、置信度、bbox）
  -> MobileSAM（以 bbox 为提示生成像素级 mask）
  -> Orbbec 对齐深度 + CameraInfo
  -> /target/cloud、/target/cloud_roi、/target/center
```

该模型替代的是 YOLO-World，不替代 SAM。运行时权重统一存放在：

```text
models/vision/yolowork_fixed_best.pt
models/vision/mobile_sam.pt
```

固定检测模型当前类别为：`jpgCat`、`Chiikawa`、`tissue`。类别匹配不区分
大小写，但必须是模型内已有类别；类别错误会返回全部可用类别，不会回退到
红色阈值遮罩。

独立验证链路不会启动抓取、policy、AnyGrasp 或避障：

```bash
cd ~/soarm100sim_project

./ros2/scripts/real/run_fixed_yolo_sam_mask.sh \
  --build \
  --class jpgCat \
  --device 0
```

运行中输入 `r` 后回车可用最新主摄画面重新执行检测和 SAM；输入 `q` 后
回车会关闭视觉节点与 Orbbec 进程。可选项：

| 选项 | 默认值 | 含义 |
|---|---:|---|
| `--class` | `jpgCat` | `jpgCat/Chiikawa/tissue` 三选一 |
| `--conf` | `0.25` | YOLO 检测置信度阈值 |
| `--iou` | `0.70` | YOLO NMS 的 IoU 阈值 |
| `--device` | `auto` | `auto/cpu/0`，`0` 表示第一张 CUDA GPU |
| `--camera` | `on` | 是否由脚本启动真实 Orbbec RGB-D |
| `--show-window` | `on` | 是否显示 RGB + SAM mask 叠加窗口 |

ROS2 接口保持原协议：原始 SAM 遮罩发布到 `/target/mask`，5% bbox 扩展 ROI
发布到 `/target/mask_expanded`。后续 AnyGrasp 应优先使用原始目标遮罩对应的
`/target/cloud`；扩展点云 `/target/cloud_roi` 只作为需要上下文时的可选输入。

相关文件：

```text
ros2/soarm100_vision/soarm100_vision/target_segmenter_node.py
ros2/soarm100_vision/launch/fixed_yolo_sam_mask.launch.py
ros2/scripts/real/run_orbbec_rgbd.sh
ros2/scripts/real/run_fixed_yolo_sam_mask.sh
```

首次真机无窗口验证结果：

```text
camera: Orbbec Gemini 336, USB3.2, RGB/Depth 1280x720@30
selected_class: jpgCat
YOLO score: 0.4758
bbox_xyxy: [934.6, 432.2, 1020.3, 489.3]
SAM mask: 2908 px
target depth points: 2850
expanded ROI points: 4537
center_camera: (0.2375, 0.0675, 0.4950) m
```

本次结果文件为
`log/runtime/ros2_vision/fixed_yolo_sam/segment_target_latest.json`。测试退出后确认
Orbbec container、segmenter 和 viewer 均无残留进程。

### 实时识别与 SAM 按需分割的职责拆分

固定类别 YOLO 新增连续 tracking 节点。它等价于把 `YoloWork/main.py` 的
摄像头输入从本机 OpenCV `camera=0` 替换为 Orbbec ROS2 RGB topic：

```text
/camera/color/image_raw
  -> model.track(persist=True, tracker=botsort.yaml)
  -> /debug/fixed_yolo_tracking（实时带框图像）
  -> /target/detections（类别、置信度、track_id、bbox JSON）
```

该节点不订阅深度、不运行 SAM，也不决定抓取计算帧。SAM 仍由
`/segment_target` 在任务开始或 replan 时按需触发。

实时识别一键启动：

```bash
./ros2/scripts/real/run_fixed_yolo_tracking.sh \
  --build \
  --class all \
  --device 0
```

窗口中的 `Q/Esc` 或终端 `Ctrl+C` 会退出 tracking 并关闭脚本启动的 Orbbec
进程。
