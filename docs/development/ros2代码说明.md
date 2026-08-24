# SO-ARM100 ROS2 代码说明

本文面向第一次接触 ROS2 的开发者，说明当前项目为什么拆成这些节点、数据
如何流动、MuJoCo 在哪里，以及以后如何迁移到真实机械臂。

## 1. 先理解 ROS2 在本项目中的作用

可以把 ROS2 理解成一套让多个程序互相通信和协作的框架。

本项目没有把视觉、AnyGrasp、机械臂控制和 GUI 全写进一个 Python 文件，
而是把它们拆成多个 ROS2 node（节点）：

```text
相机节点负责产生图像
视觉节点负责找目标
AnyGrasp 节点负责生成抓取位姿
状态机节点负责决定下一阶段
policy backend 负责实际控制
障碍点云节点负责生成避障输入
GUI 节点只负责显示
```

这样做的主要目的不是让仿真代码变多，而是让以后接真机时可以只替换相机
和执行后端，不必重写整条抓取逻辑。

## 2. Topic、Service 和 Action

### 2.1 Topic：连续广播的数据流

Topic 适合持续产生的数据。发布者不需要等待订阅者执行完成。

项目中的例子：

```text
/camera/color/image_raw            主相机 RGB
/camera/depth/image_rect_raw       主相机 depth
/camera/color/camera_info          主相机内参
/robot/mask                        机械臂像素 mask
/target/mask                       目标 SAM mask
/target/cloud                      目标点云
/obstacle/cloud                    障碍点云
/wrist/color/image_raw             腕部 RGB
/target/tracked_2d                 腕部二维 tracking 结果
/mujoco/sim_state                  MuJoCo qpos 镜像状态
```

直观类比：topic 像直播频道。节点可以持续发布，其他节点按需收看。

### 2.2 Service：一次请求，一次快速回答

Service 适合耗时较短、请求和响应一一对应的操作。

项目中的例子：

```text
segment_target
  请求：目标 prompt，例如 "red cube"
  返回：是否找到、目标中心、bbox、mask topic

set_avoidance
  请求：开启或关闭避障
  返回：设置是否成功
```

直观类比：service 像调用一个普通函数，只是函数运行在另一个节点里。

### 2.3 Action：耗时任务，有反馈、结果和取消

抓取和 AnyGrasp 规划可能需要几秒甚至几十秒，因此使用 Action。

项目中的 action：

```text
plan_grasp
  输入目标点云
  反馈候选数量和最高分
  返回选中的 grasp/pregrasp

execute_planned_grasp
  输入已经选好的抓取计划
  持续反馈 MOVE_TO_PREGRASP、FINAL_APPROACH、CLOSE、LIFT 等阶段
  返回抓取成功、失败原因和提升高度

execute_grasp
  对外暴露的完整任务
  内部串联分割、AnyGrasp 和 policy 执行
```

直观类比：action 像提交一份任务单。任务执行过程中可以查询进度，也可以
取消。

## 3. ROS2 工作空间结构

```text
ros2/
├── soarm100_interfaces/       # action/msg/srv
├── so100_plus_description/    # URDF/RViz/FK 对照
├── soarm100_vision/           # 当前 ROS2 Python 实现包
│   ├── launch/
│   ├── soarm100_vision/
│   └── test/
├── config/                    # real/sim/experiments 参数文件
├── scripts/                   # real/sim/calibration 规范启动入口
├── README.md                   # 当前目录职责与迁移边界
├── 开发日志.md                 # 历史开发记录
└── 代码说明.md                 # 本文
```

当前根目录下的 `run_*.sh` 为兼容既有指令而保留。以后新增真机、仿真回归、
标定入口分别放入 `scripts/real`、`scripts/sim`、`scripts/calibration`，避免
继续在 `ros2/` 根目录堆放脚本。`build/`、`install/`、`log/`、`log/runtime/` 是运行
生成物，不是源码编辑位置。

### `soarm100_interfaces`

这里只定义节点之间的数据格式，不实现算法。

```text
msg/TrackedTarget2D.msg
  腕部 RGB tracking 输出

srv/SegmentTarget.srv
  YOLO-World + SAM 分割请求

srv/SetAvoidance.srv
  避障开关

action/PlanGrasp.action
  AnyGrasp 规划接口

action/ExecutePlannedGrasp.action
  已规划位姿的执行接口

action/ExecuteGrasp.action
  完整抓取接口
```

修改这些接口后通常需要重新：

```bash
cd ros2
colcon build --packages-select soarm100_interfaces soarm100_vision
source install/setup.bash
```

### `soarm100_vision`

这里包含实际节点和核心算法。

`launch/vision_grasp.launch.py` 负责一次启动多个节点，并把 bash 参数传给
各节点。

`setup.py` 中的 `console_scripts` 决定 `ros2 run soarm100_vision ...`
可以启动哪些程序。

## 4. 完整抓取链路

### 4.1 初次识别与规划

```text
用户发送 ExecuteGrasp goal
→ grasp_orchestrator_node
→ 请求 segment_target
→ target_segmenter_node 运行 YOLO-World
→ 根据 prompt 选择 bbox
→ MobileSAM 生成原始目标 mask
→ mask + depth + CameraInfo 反投影为目标点云
→ 请求 plan_grasp
→ anygrasp_planner_node 调用 graspnet_gpu 环境中的 AnyGrasp
→ NMS、分数/宽度筛选、IK 和关节限位筛选
→ 返回 selected grasp + pregrasp + gripper width
→ 请求 execute_planned_grasp
```

当前目标点云默认使用原始 SAM mask。5% 外扩 mask 会发布用于调试或 ROI，
但不会默认混入目标抓取点云，避免把桌面和邻近物体交给 AnyGrasp。

### 4.2 AnyGrasp 的环境隔离

AnyGrasp 依赖 `graspnet_gpu` conda 环境，而 ROS2 视觉节点主要运行在
`vision_seg`。当前 planner 通过独立 worker 调用 AnyGrasp，避免把
MinkowskiEngine、PyTorch 和 ROS2 Python 依赖强行安装进同一环境。

AnyGrasp 输出的 pose 带有输入相机 frame。它不能直接当世界坐标使用，
必须先转换到 `base`。

### 4.3 抓取状态机

状态机核心在：

```text
soarm100_vision/grasp_core.py
```

阶段为：

```text
MOVE_TO_PREGRASP
→ FINAL_APPROACH
→ CLOSE
→ LIFT
→ VERIFY
```

失败时可能进入：

```text
REPLAN_GRASP
→ 重新获取主相机 RGB-D
→ SAM
→ AnyGrasp
→ IK 筛选
→ 接受新计划或拒绝
```

replan 失败、次数耗尽或 runner 总 step budget 耗尽后进入：

```text
RETURN_HOME
```

返回过程仍使用 policy；如果启用避障，也继续经过 CBF-QP。

## 5. 每个主要节点负责什么

### `target_segmenter_node.py`

职责：

```text
订阅主相机 RGB/depth/CameraInfo
加载 YOLO-World 和 MobileSAM
根据 prompt 识别目标
生成 mask、目标点云和目标中心
提供 segment_target service
```

仿真里允许红色 mask fallback，主要用于模型未加载或固定红色目标调试。
2real 正式验证时应关闭 fallback，防止系统看似成功但实际没有使用
YOLO/SAM。

### `anygrasp_planner_node.py`

职责：

```text
接收 PlanGrasp goal 和目标点云
调用 AnyGrasp
读取候选分数、宽度、位置和旋转
转换到 base frame
进行 NMS
进行 IK + 关节限位筛选
返回最优可达候选
```

当前重要默认值：

```text
top_k=45
min_score=0.01
IK position tolerance=0.005 m
IK rotation tolerance=3 deg
pregrasp distance=0.07 m
```

### `grasp_orchestrator_node.py`

这是完整任务的调度者，不直接做视觉或控制。

它负责：

```text
接收 execute_grasp action
调用 segment_target
等待 /target/cloud
调用 plan_grasp
调用 execute_planned_grasp
转发反馈和最终结果
```

### `wrist_tracker_node.py`

腕部相机只使用 RGB，不依赖深度。

链路：

```text
backend 将世界系 tracking reference 投影到腕部图像
→ 发布 /wrist/tracking_roi
→ tracker 在局部搜索窗做多尺度模板匹配
→ 输出 observed-reference 像素偏差
→ backend 根据实时腕部相机姿态转换成世界系小平移
→ 只修正抓取位置，不修改 AnyGrasp 姿态
```

tracking 不能代替 AnyGrasp。它只适合抓取过程中目标发生小位移；偏移过大或
连续丢失时必须 replan。

### `obstacle_cloud_node.py`

障碍点云前端：

```text
主相机 depth
→ 去除 robot mask
→ base frame 变换
→ workspace crop
→ 去除桌面
→ voxel 处理
→ /obstacle/cloud
```

静态模式：

```text
短窗口一致性过滤
→ 冻结障碍点云
```

动态模式：

```text
只保留当前帧 voxel
→ 不 union 历史位置
→ 持续发布动态点云
```

当前 workspace 默认值：

```text
x: 0.02--0.36 m
y: -0.08--0.26 m
z: 0.055--0.42 m
```

这些范围必须根据真实机械臂安装位置重新验证，不能直接照搬。

### `sdf_cbf_backend_node.py`

该节点目前主要订阅障碍点云并维护/发布 SDF 状态，便于 ROS2 模块诊断。

当前仿真实际施加到关节命令上的 CBF-QP 仍在
`mujoco_inprocess_runner.py` 使用的 `ReachStepper` 内完成。2real 前应将
这部分整理成与 MuJoCo 无关的 controller/filter node：

```text
nominal joint command
+ robot joint state
+ robot kinematics
+ obstacle SDF
→ safe joint command
```

### `mujoco_policy_backend_node.py`

这是仿真执行 action server。它负责：

```text
接收 ExecutePlannedGrasp
转换 pose 到 base
创建 MujocoInProcessRunner
发布仿真相机
读取 wrist tracking
读取 obstacle cloud
执行 policy + CBF + 状态机
处理 replan
发布 action feedback/result
```

该节点是仿真专用执行后端，不能直接控制真机。

### `mujoco_inprocess_runner.py`

只负责 MuJoCo 环境中的：

```text
model/data
physics step
policy 推理
执行状态机 intent
CBF 修正
相机离屏渲染
动态障碍运动
轨迹日志
RETURN_HOME
```

它使用 EGL 产生无窗口仿真相机图像。

### `mujoco_mirror_viewer_node.py`

只负责 GUI：

```text
订阅 /mujoco/sim_state
→ 把 qpos 写入自己的 MuJoCo model
→ GLFW viewer 显示
```

GUI 和 EGL backend 分进程，防止 OpenGL context 冲突。GUI 关闭不应改变
算法结果。

### `mujoco_camera_publisher_node.py`

抓取 backend 尚未接管仿真时，发布初始化场景 RGB-D。backend 开始执行后，
通过 `/mujoco/backend_camera_active` 通知它暂停，避免两个 MuJoCo renderer
同时发布不同仿真状态的图像。

## 6. 坐标系与标定

### 6.1 常用 frame

```text
scene_depth_optical   主相机光学坐标
wrist_rgb_optical     腕部相机光学坐标
base                  机械臂基座坐标
world                 当前仿真中通常与 base 安装关系固定
policy TCP            policy 训练时使用的末端控制点
```

图像像素坐标、相机三维坐标、base 坐标和 TCP 坐标不是同一个概念。

### 6.2 主相机点云

```text
pixel (u,v) + depth
→ CameraInfo 内参反投影
→ scene_depth_optical 三维点
→ T_base_camera 外参
→ base 三维点
```

MuJoCo 使用 MJCF 中相机实时位姿。真机应使用 TF2 中发布的标定外参。

### 6.3 腕部相机

腕部相机安装在末端，因此相对 base 的位姿持续变化：

```text
T_base_wrist_camera(t)
= T_base_ee(t) × T_ee_wrist_camera
```

`T_ee_wrist_camera` 来自手眼标定；`T_base_ee(t)` 来自实时关节状态和正运动学。
不能使用一次测量得到的固定 `T_base_camera` 代替。

### 6.4 TCP

TCP 是 policy 和抓取位姿真正对齐的末端控制点，不一定等于最后一个 link
原点。2real 时必须保证：

```text
训练时 TCP
= 仿真执行 TCP
= 真机 TF 中 tool/TCP frame
```

不一致会表现为“数值到达 grasp pose，但夹爪实际高出或偏离物体”。

## 7. SDF-CBF-QP 避障

policy 给出名义关节增量：

```text
dq_nom
```

CBF-QP 求最小修正：

```text
min ||dq_cbf||^2

dq_total = dq_nom + dq_cbf
```

约束要求机械臂监测点与障碍物保持安全距离。动态障碍额外包含障碍物位移：

```text
grad(h) * dq_total >= obstacle_step - gamma * h
```

因此障碍物朝机械臂移动时，约束会比静态情况更早收紧。

当前动态仿真参数：

```text
--mujoco-obstacle-motion line|circle
--mujoco-obstacle-motion-amp ax,ay,az
--mujoco-obstacle-motion-period seconds
```

运动公式：

```text
p(t) = center + amplitude * sin(2*pi*t/period)
```

`motion-amp` 是幅度和轴方向，不是速度。最大速度为：

```text
v_max = 2*pi*amplitude/period
```

## 8. 日志怎么看

### ROS2 launch 日志

```text
log/runtime/ros2/<timestamp>/launch.log
```

主要用于确认：

```text
哪个 node 启动/退出
退出码
是否收到 Ctrl-C
是否发生原生崩溃
```

常见退出码：

```text
1    Python/参数/业务错误
-2   SIGINT，通常是用户 Ctrl-C
-11  segmentation fault，原生库崩溃
```

### 抓取轨迹 JSONL

每行是一个 control step，常用字段：

```text
phase
reason
tcp_pos
control_target
final_err
target_object_pos
target_lift
tracking_confidence
obstacle_points
obstacle_pos
obstacle_step_velocity
cbf_active
h_min
dq_nom_norm
dq_cbf_norm
```

事件行：

```text
replan_accept
replan_reject
return_home
```

### native stage 日志

```text
<trajectory>.native.log
```

用于定位 MuJoCo/OpenGL 原生崩溃前最后完成了哪项操作，例如：

```text
before_camera_render
after_camera_render
before_mj_step
after_mj_step
```

## 9. 常用构建和检查命令

首次或接口修改后：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/ros2
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

查看节点：

```bash
ros2 node list
```

查看 topic：

```bash
ros2 topic list
ros2 topic hz /camera/depth/image_rect_raw
ros2 topic echo /target/tracking_status
```

查看 action：

```bash
ros2 action list
ros2 action info /execute_grasp
```

查看 service：

```bash
ros2 service list
ros2 service type /segment_target
```

查看节点参数：

```bash
ros2 param list /mujoco_policy_backend
ros2 param get /mujoco_policy_backend obstacle_motion_period
```

## 10. 仿真运行方式

完整链路建议始终使用：

```text
--mujoco off
--mujoco-backend on
--mujoco-backend-mode inprocess
```

这里的 `--mujoco off` 表示不额外启动旧的 `play.py` 进程，不表示关闭
MuJoCo 仿真。真正的仿真由 ROS2 backend 运行。

GUI 使用：

```text
--mujoco-inprocess-viewer on
```

该参数现在启动独立 mirror viewer，不会把 GLFW 塞进 EGL backend。

## 11. 2real 部署步骤

不要一次把所有仿真模块换成真机。建议按以下顺序，每一步单独验收。

### 阶段 0：建立硬件安全边界

准备：

```text
物理急停
软件急停 topic/service
关节位置和速度限制
电机电流/力矩限制
通信超时自动停止
控制命令 watchdog
工作空间硬边界
低速调试模式
```

任何视觉和抓取算法都不能替代这些底层保护。

### 阶段 1：建立真实机器人 ROS2 driver

需要一个硬件执行节点，例如：

```text
soarm100_hardware_node
```

输入：

```text
安全过滤后的关节位置或速度命令
夹爪命令
```

输出：

```text
/joint_states
电机状态
温度/电流/故障码
```

先验证单关节、小速度、无视觉控制，再验证多关节。

### 阶段 2：建立完整 TF 树

至少需要：

```text
world/table
base
各 robot link
ee
policy_tcp
scene_camera_link
scene_camera_optical
wrist_camera_link
wrist_camera_optical
```

使用 `robot_state_publisher` 根据 URDF 和 `/joint_states` 发布机器人动态 TF。

### 阶段 3：标定主相机

主相机通常固定在场景中，完成：

```text
相机内参标定
深度尺度检查
畸变校正
T_base_scene_camera 外参标定
多姿态棋盘格验证
```

不要只看重投影误差，还要把已知三维点转换到 base 后测量毫米级误差。

### 阶段 4：腕部手眼标定

求：

```text
T_ee_wrist_camera
```

采集多个机械臂姿态，每个姿态都应看到同一标定板。然后通过实时：

```text
T_base_ee(t) × T_ee_wrist_camera
```

得到腕部相机动态位姿。

### 阶段 5：替换仿真相机

保持视觉节点订阅的 topic 名不变，停用：

```text
mujoco_camera_publisher_node
backend EGL camera publisher
```

改为真实驱动发布：

```text
/camera/color/image_raw
/camera/depth/image_rect_raw
/camera/color/camera_info
/wrist/color/image_raw
```

先只运行 YOLO/SAM 可视化，不连接机械臂控制。

### 阶段 6：验证机器人自点云去除

仿真可以直接使用 geom segmentation；真机不能。

推荐真机方案：

```text
实时 /joint_states
→ URDF 正运动学
→ 各 link collision mesh 变换到相机
→ 渲染 robot depth/mask
→ 对真实 depth 做带余量的 self removal
```

验证机械臂在多个姿态移动时：

```text
robot 点不会进入 /obstacle/cloud
真实外部障碍不会被误删
```

### 阶段 7：只部署 policy 到达

新增真机执行 backend，实现与 `ExecutePlannedGrasp` 相同的 action 接口。

第一阶段关闭：

```text
夹爪闭合
LIFT
CBF
tracking
```

只验证 policy TCP 能低速到达多个空中目标位姿，并核对真机 TCP 与 TF。

### 阶段 8：部署静态 SDF-CBF-QP

顺序：

```text
先 shadow mode：计算 dq_cbf 但不下发
→ 检查 h_min、约束激活率和可行性
→ 限速下发
→ 软障碍物测试
→ 才允许硬障碍物测试
```

真机 CBF 必须使用真实控制周期 `dt`，不能照搬 MuJoCo step。相机点云还应
带时间戳，并检查点云到关节状态的时间同步。

### 阶段 9：部署腕部 RGB tracking

先让目标物体静止：

```text
主相机识别并建立 reference
→ 腕部图像显示动态 ROI
→ 移动物体少量距离
→ 验证像素偏差方向
→ 验证世界系修正方向
```

在不下发控制时先记录 tracking 修正；确认符号和尺度后再接入 policy。

### 阶段 10：部署 AnyGrasp 和 pregrasp

先离线保存真实目标点云，在 `graspnet_gpu` 中重复运行，检查：

```text
候选是否位于目标表面
姿态轴是否正确
gripper width 是否合理
base frame 转换是否正确
IK 是否可达
是否碰桌面或自身
```

之后再连接：

```text
AnyGrasp
→ IK/关节限位
→ MOVE_TO_PREGRASP
```

### 阶段 11：最后开放 CLOSE 和 LIFT

建议逐级测试：

```text
空夹爪闭合
→ 软方块
→ 轻质瓶
→ 不规则物体
```

完成标准仍使用物体提升高度超过阈值。真机还可增加：

```text
夹爪电流变化
夹爪实际宽度
腕部视觉中物体随夹爪同步运动
```

不要仅根据“执行过 close 命令”判断成功。

## 12. 2real 架构建议

建议保留：

```text
soarm100_interfaces
target_segmenter_node
anygrasp_planner_node
wrist_tracker_node
obstacle_cloud_node
grasp_orchestrator_node
grasp_core.py
```

建议新增：

```text
soarm100_hardware_node
robot_state_publisher + URDF
tf2 标定发布节点
robot_self_filter_node
real_policy_backend_node
cbf_safety_filter_node
safety_supervisor_node
```

仿真专用、不应直接搬到真机：

```text
mujoco_inprocess_runner.py
mujoco_camera_publisher_node.py
mujoco_mirror_viewer_node.py
MJCF 动态障碍控制
EGL renderer
```

推荐最终数据流：

```text
real cameras
→ target segmentation / obstacle cloud
→ AnyGrasp
→ orchestrator + grasp state machine
→ policy nominal command
→ independent CBF safety filter
→ hardware driver
→ motors

/joint_states + TF + camera timestamps
→ tracking / self filter / policy / CBF
```

CBF safety filter 最好独立于 policy 和状态机。即使视觉节点、AnyGrasp 或
状态机卡住，底层也必须能够停止机械臂或拒绝不安全命令。

## 13. 2real 前的当前缺口

以下事项尚不能视为完成：

```text
真实 SO-ARM100 ROS2 hardware driver
真实 URDF/TF 与 policy TCP 的统一验证
真实主相机外参接入 TF2
腕部 hand-eye 标定在线使用
基于 URDF mesh 的真机 robot self removal
与 MuJoCo 无关的实时 CBF safety filter
真机控制周期和通信 watchdog
真机夹爪力/电流/宽度反馈
端到端时间同步与延迟监控
```

因此当前工程已经具备 ROS2 形状的仿真验证链路，但还不能把
`mujoco_policy_backend_node` 换一个串口地址就直接控制真机。正确迁移方式
是保持 interfaces 和上层节点不变，逐步替换仿真数据源与执行后端。
