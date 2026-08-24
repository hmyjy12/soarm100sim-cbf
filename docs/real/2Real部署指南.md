# SO-ARM100 2Real 部署指南

本文说明如何把当前已经能在 MuJoCo 中运行的 ROS2 抓取系统迁移到真实
SO-ARM100。目标不是立即让机械臂全自动抓取，而是按可验证、可回退的顺序，
逐层替换仿真输入输出。

本文假定读者第一次接触 `ros2_control`。所有步骤都尽量说明：

- 这一步在做什么；
- 为什么必须做；
- 成功时应该看到什么；
- 失败时不要继续做什么。

---

## 1. 先说结论

当前项目不应该从“MuJoCo 版本”直接改成“真机版本”。正确做法是保留两套
可切换的机器人 backend：

```text
相同的视觉、AnyGrasp、状态机、policy、CBF-QP
                         |
                  RobotBackend 接口
                    /          \
        MuJoCoBackend            Ros2ControlBackend
        仿真验证                  真机执行
```

因此：

- MuJoCo、MJCF、GUI、仿真相机和仿真日志继续保留；
- 新建真机 hardware package 和 bringup package；
- 默认仍可启动 MuJoCo；
- 只有启动参数选择 `ros2_control` 时才允许连接真机；
- 不在视觉节点、状态机或 policy 中直接写串口代码。

---

## 2. 当前仓库已经有什么

### 2.1 `SO-ARM100` 目录包含什么

[`SO-ARM100`](/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100)
主要包含：

```text
机械结构和打印文件
SO-100 / SO-101 的 URDF、MJCF、USD
MuJoCo 资产
硬件物料清单
装配和 LeRobot 文档入口
```

从本地文档可以确认，标准单台 follower SO-100 使用：

```text
6 个 Feetech STS3215 舵机
1 个电机控制板
1 个 USB-C 连接
独立舵机电源
```

相关说明位于：

- [`SO100.md`](/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/SO100.md)
- [`README.md`](/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/README.md)

### 2.2 它不包含什么

当前没有发现以下可直接使用的实现：

```text
ros2_control SystemInterface 插件
STS3215 ROS2 hardware driver
真机 controller YAML
真机 URDF 中的 <ros2_control> 配置
真机启动 launch
舵机 ID、零位和方向的本机标定文件
```

URDF 中的：

```xml
<hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
```

只是旧式 transmission/interface 描述，不是已经实现好的驱动。它不会自动
连接串口，也不会自动控制 STS3215。

### 2.3 本机软件现状

当前系统已经安装：

```text
ROS Humble ros2_control
ROS Humble ros2_controllers
Conda 环境 lerobot
Conda 环境 vision_seg
Conda 环境 graspnet_gpu
```

当前检查时没有发现 `/dev/ttyACM*` 或 `/dev/ttyUSB*`，说明控制板尚未连接，
或者系统尚未识别/授权该串口。

---

## 3. 真机前必须解决的零号问题：7 维 policy 与 6 舵机

这是当前最重要的阻塞项。

### 3.1 当前 policy 使用 7 维关节

[`mujoco/constants.py`](/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/mujoco/constants.py)
定义：

```text
shoulder_rotation_joint
shoulder_pitch_joint
ellbow_joint
wrist_pitch_joint
wrist_jaw_joint
wrist_roll_joint
gripper_joint
```

即：

```text
6 个手臂关节 + 1 个夹爪 = 7 维 action
```

当前 checkpoint 的：

```text
OBS_DIM    = 27
ACTION_DIM = 7
```

活动仿真模型
[`so100_plus.xml`](/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/so100_plus.xml)
也确实具有 7 个 actuator。

### 3.2 标准 SO-100 是 6 个舵机

仓库中的标准模型
[`so_100.xml`](/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/so_100.xml)
是：

```text
5 个手臂关节 + 1 个夹爪 = 6 个舵机
```

因此，在确认真实机械臂结构前，绝对不能把当前 7 维 action 直接发给真机。

### 3.3 必须先回答的问题

在实现真机 backend 前，需要实物确认：

1. 真实 follower 上到底安装了几个 STS3215？
2. 是否真的存在独立的 `wrist_jaw` 和 `wrist_roll` 两个舵机？
3. 每个舵机的总线 ID 是多少？
4. 夹爪对应哪个 ID？
5. 当前 policy 的第 5、6、7 维分别对应真实哪个电机？

只有两种可接受结论：

```text
A. 真机是自定义 7 舵机结构
   → 建立完整 7 对 7 映射，可以继续迁移当前 policy。

B. 真机是标准 6 舵机 SO-100
   → 当前 7 维 policy 与机械结构不一致。
   → 必须使用匹配 6 舵机结构的模型/policy，或重新训练。
```

不能简单丢弃 `wrist_jaw` action，因为 policy 的其余动作是在 7 自由度运动学
条件下训练得到的，直接删一维会改变 TCP 可达性和动作语义。

---

## 4. 迁移后的完整系统结构

推荐最终结构：

```text
主 RGB-D 相机
  ├── RGB → 颜色分割
  ├── depth + mask → 目标点云
  └── 非目标工作空间点云 → SDF

腕部 RGB 相机
  └── 颜色连通域 → target tracking

目标点云
  └── AnyGrasp → grasp / pregrasp / width

grasp_orchestrator
  └── GraspStateMachine
       ├── MOVE_TO_PREGRASP
       ├── FINAL_APPROACH
       ├── COMMIT_GRASP
       ├── CLOSE
       ├── LIFT
       ├── VERIFY
       └── REPLAN_GRASP

policy + SDF-CBF-QP
  └── q_cmd
       └── ros2_control controller
            └── SOARM100System Hardware Interface
                 └── Feetech 总线
                      └── STS3215
```

---

## 5. 哪些代码保留，哪些代码替换

### 5.1 可以直接保留

原则上保留：

```text
target_segmenter_node.py
wrist_tracker_node.py
anygrasp_planner_node.py
grasp_orchestrator_node.py
grasp_core.py
sdf_cbf_core.py
Action / Service / Message 定义
颜色分割逻辑
replan 逻辑
日志格式
```

### 5.2 仿真专用，真机不直接使用

```text
mujoco_inprocess_runner.py
mujoco_camera_publisher_node.py
mujoco_mirror_viewer_node.py
MuJoCo qpos/qvel/contact 读取
MJCF 中的目标物体和障碍物运动
仿真 ground-truth target center
```

这些文件继续保留用于回归测试，不删除。

### 5.3 真机需要新增

推荐新增三个 package：

```text
ros2/soarm100_hardware/
  C++ ros2_control SystemInterface
  Feetech/LeRobot 总线适配

ros2/soarm100_control/
  RobotBackend 抽象
  ros2_control backend
  policy 控制循环
  命令安全过滤

ros2/soarm100_bringup/
  真机 URDF/xacro
  controllers.yaml
  sim.launch.py
  real.launch.py
  参数和标定文件
```

不要把真机串口代码加入 `soarm100_vision`。

---

## 6. ros2_control 到底负责什么

普通 ROS2 topic 只是传递消息。`ros2_control` 额外规定：

```text
谁拥有硬件资源
控制器如何声明 command/state interface
控制循环如何 read → update → write
控制器如何 activate/deactivate
关节命令如何统一管理
```

### 6.1 Hardware Interface

`SOARM100System` 应实现：

```text
on_init()
  读取串口、波特率、舵机 ID、关节标定参数

on_configure()
  打开总线并 ping 每个舵机

on_activate()
  读取当前位置
  将第一条 command 设置为当前位置
  然后才允许使能位置控制

read()
  批量读取舵机 tick、速度、负载、电压、温度
  转换成 rad、rad/s

write()
  检查命令是否合法
  rad 转换成舵机 tick
  批量写入目标位置/速度限制

on_deactivate()
  停止发送新运动命令
  根据安全策略保持或释放 torque
```

### 6.2 Controller

第一版建议：

```text
joint_state_broadcaster
forward_command_controller/ForwardCommandController
```

`joint_state_broadcaster` 发布 `/joint_states`。

`ForwardCommandController` 接收 policy 产生的关节位置目标。

以后可以增加：

```text
joint_trajectory_controller
```

它适合 home、标定姿态和安全撤回，不应替代 policy 的实时控制循环。

---

## 7. 硬件通信层应如何复用 LeRobot

当前 `SO-ARM100` 文档明确指向 LeRobot，且本机已有 `lerobot` Conda 环境。
因此优先策略是：

1. 先用 LeRobot 提供的 Feetech motor bus 工具验证硬件；
2. 确认能够读取和写入 STS3215；
3. 复用其协议、寄存器和标定数据结构；
4. 在 ros2_control hardware plugin 外包一层稳定的 C++/Python bridge。

不建议从零手写 Feetech 串口协议，除非现有 SDK 无法满足同步读写和错误恢复。

### 7.1 Python 与 C++ 的取舍

`ros2_control SystemInterface` 通常使用 C++。但如果可用的 LeRobot/Feetech
驱动只有 Python，可以分两阶段：

```text
阶段 1：Python motor bus 测试工具
阶段 2：C++ hardware plugin 调用稳定的底层 SDK
```

不推荐最终采用：

```text
ros2_control C++ plugin
→ 每个周期调用 Python subprocess
```

这会引入不可控延迟。底层应在同一进程内通信，或使用明确频率的独立硬件
daemon，并提供 watchdog。

---

## 8. 舵机标定：最容易导致撞机的部分

### 8.1 三套坐标不能混淆

每个关节至少有：

```text
原始舵机 tick
标定后的物理关节角 rad
policy/MuJoCo 使用的关节角 rad
```

必须建立：

```text
q_policy ↔ q_real ↔ servo_tick
```

通用形式：

```text
q_real = direction * scale * (tick - zero_tick) + offset
```

其中：

- `zero_tick`：机械零位对应的舵机读数；
- `direction`：`+1` 或 `-1`；
- `scale`：tick 到 rad 的比例；
- `offset`：模型零位和机械零位之间的偏置。

不要在未读取具体舵机配置时假设 tick 分辨率，也不要直接套用网上的数值。

### 8.2 建议的标定文件

建议创建：

```yaml
port: /dev/soarm100
baudrate: <以实际控制板和 LeRobot 配置为准>

joints:
  shoulder_rotation_joint:
    id: 1
    zero_tick: <实测>
    direction: 1
    offset_rad: <实测>
    min_rad: <实测安全值>
    max_rad: <实测安全值>
  ...
```

ID 和数值必须来自实际扫描与标定，不能根据上面的示例填写。

### 8.3 标定验收

每个关节单独验证：

1. torque 关闭时手动缓慢转动；
2. 读取角度是否连续；
3. 向模型正方向转动时，ROS 角度是否增加；
4. 机械中位是否对应预期模型姿态；
5. 上下限是否在碰撞之前触发；
6. 重启后零位和方向是否保持一致。

---

## 9. 真机 URDF 与 TF

真机 URDF 应有三个职责：

```text
描述真实关节和 link
提供 joint limit
声明 ros2_control hardware plugin
```

示意：

```xml
<ros2_control name="SOARM100System" type="system">
  <hardware>
    <plugin>soarm100_hardware/SOARM100System</plugin>
    <param name="port">/dev/soarm100</param>
    <param name="calibration_file">...</param>
  </hardware>

  <joint name="shoulder_rotation_joint">
    <command_interface name="position"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
```

注意：最终关节数量必须先解决第 3 节的 7/6 自由度问题。

### 9.1 TCP

当前 policy 控制的是项目定义的 TCP，不一定等于最后一个 link 原点。
真机 URDF 必须包含与训练一致的固定 TCP frame：

```text
base
→ ...
→ gripper link
→ policy_tcp
```

`policy_tcp` 的平移和旋转必须与 MuJoCo/训练使用的 TCP 定义一致。不能为了
让夹爪“看起来对齐”而在 action goal 上临时加 target offset。

---

## 10. 相机 2Real

### 10.1 主相机

主相机需要：

```text
RGB
depth
CameraInfo
T_base_scene_camera
```

当前颜色模式的输入 topic：

```text
/camera/color/image_raw
/camera/depth/image_rect_raw
/camera/color/camera_info
```

如果真实相机 topic 不同，应通过 launch remap，不要改算法代码。

### 10.2 腕部相机

当前腕部 tracking 只需要 RGB：

```text
/wrist/color/image_raw
```

但像素位移转换为世界位移仍依赖：

```text
腕部相机内参
T_wrist_camera
实时 T_base_wrist
目标深度估计
```

### 10.3 仿真标定文件不能直接用于真机

当前：

[`log/runtime/calib/camera_calib.json`](/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/log/runtime/calib/camera_calib.json)

保存的是 MuJoCo 相机模型和安装位姿。它只能用于仿真，不能当作真实相机
外参。

真机需要重新获得：

```text
主相机内参
腕部相机内参
主相机到 base 的外参
腕部相机到 wrist link 的 hand-eye 外参
```

### 10.4 棋盘格标定后的 TF

固定主相机：

```text
T_base_scene_camera = 常量
```

腕部相机：

```text
T_base_wrist_camera(t)
  = T_base_wrist_link(t) × T_wrist_link_wrist_camera
```

其中 `T_base_wrist_link(t)` 来自实时 `/joint_states` 和 robot_state_publisher，
`T_wrist_link_wrist_camera` 来自手眼标定。

不要每帧重新“平均外参”。标定得到的是固定安装变换，实时变化来自机械臂
正运动学。

---

## 11. 控制频率建议

第一版建议：

```text
hardware read/write：100 Hz
policy + CBF-QP：50 Hz
腕部 RGB tracking：15～30 Hz
主相机颜色分割：任务开始和 replan 时
静态 SDF：任务开始时建立
动态 SDF：按相机实际帧率更新
```

如果串口无法稳定支持全部舵机 100 Hz 同步读写，应降低 hardware update
rate，而不是让循环随机超时。

必须记录：

```text
read 耗时
write 耗时
policy 耗时
CBF-QP 耗时
tracking 数据年龄
命令数据年龄
丢包/重试次数
```

---

## 12. 安全层

### 12.1 上层算法安全

```text
policy action clip
CBF-QP
关节软限位
最大 dq
最大单周期 q 增量
tracking 最大位移
状态机阶段限制
```

### 12.2 ros2_control/hardware 安全

必须实现：

```text
硬关节限位
命令 watchdog
串口异常检测
舵机离线检测
温度上限
电压异常
负载/电流上限
启动防跳变
急停
退出时安全处理
```

### 12.3 启动防跳变

`on_activate()` 的正确顺序：

```text
读取真实当前位置 q_measured
command = q_measured
连续确认状态有效
然后使能 controller
```

错误做法：

```text
节点启动
command 默认全零
打开 torque
```

这会让机械臂立即冲向模型零位。

### 12.4 Watchdog

建议至少检查：

```text
超过 100 ms 没有新 command：停止更新目标并保持当前位置
超过 500 ms 无法读取舵机：controller error
连续多次通信失败：deactivate hardware
```

最终数值要根据实测总线延迟调整。

---

## 13. 推荐实施阶段

每一阶段都必须单独通过，不能跳级。

### 阶段 0：确认硬件结构

目标：

```text
确认真实舵机数量
确认每个舵机 ID
解决 7 维 policy 与真机维度
```

验收：

- 有一张完整的“policy joint → real joint → servo ID”表；
- 没有任何未解释的 action 维度。

### 阶段 1：只读硬件

保持机械臂 torque 关闭。

目标：

```text
识别串口
ping 全部舵机
读取 position/temperature/voltage
不发送运动命令
```

Linux 检查：

```bash
ls -l /dev/ttyACM* /dev/ttyUSB*
dmesg --follow
lsusb
groups
```

用户需要属于串口对应的组，Ubuntu 常见为 `dialout`。不要用长期
`sudo chmod 777 /dev/ttyUSB0` 代替正确 udev/用户组配置。

验收：

- 每个舵机持续读取至少 5 分钟；
- 无随机 ID 丢失；
- 读数范围合理；
- 手动移动时关节角方向正确。

### 阶段 2：单关节低速运动

机械臂悬空或拆除容易碰撞的负载，急停可触达。

目标：

```text
每次只控制一个关节
幅度 2～5 度
低速
验证方向、限位和停止
```

验收：

- 正命令对应模型正方向；
- 停止命令立即有效；
- 超过软限位的命令被拒绝；
- 拔掉上层命令后 watchdog 生效。

### 阶段 3：ros2_control 冒烟测试

启动：

```text
controller_manager
joint_state_broadcaster
arm_position_controller
robot_state_publisher
```

检查：

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers
ros2 topic echo /joint_states
ros2 topic hz /joint_states
```

验收：

- state interface 全部 available/claimed 状态正确；
- `/joint_states` 顺序和名称固定；
- controller deactivate 后不再执行新命令；
- 重启不跳变。

### 阶段 4：home 和夹爪

先不启用 policy。

目标：

```text
缓慢进入安全 home
夹爪缓慢打开
夹爪缓慢闭合
验证最大夹持命令和负载限制
```

夹爪不能只依赖“发送一个更小的位置”。还需要：

```text
速度限制
负载/电流限制
位置停止条件
超时
温度检查
```

### 阶段 5：policy 空载到达

关闭：

```text
抓取
tracking
避障
```

只验证：

```text
真实 q → policy
policy q_cmd → ros2_control
TCP 到达静态安全目标
```

目标必须远离桌面、机械臂和人员。

验收：

- 真机 q 顺序和仿真一致；
- policy 不抖动；
- TCP 方向正确；
- 最大单周期命令不过限；
- 停止 action 后机械臂安全保持。

### 阶段 6：颜色视觉与静态目标

先使用颜色像素识别，不启用 YOLO/SAM。

目标：

```text
主相机红色 mask
目标点云
AnyGrasp
pregrasp
final
```

仍然先不 close。

验收：

- 主相机点云中心与实物误差可测；
- AnyGrasp 可视化与实物重合；
- TCP 到 pregrasp/final 的世界坐标误差可接受。

### 阶段 7：腕部颜色 tracking

目标缓慢平移，夹爪保持打开。

验收：

- 颜色 bbox 始终在真实物体上；
- `tracking_delta` 与物体运动方向一致；
- 目标停止后修正量稳定；
- 丢失目标时不追背景；
- tracking 丢失不会直接触发 close。

### 阶段 8：close 和 lift

使用柔软、轻、规则的测试物体。

验收：

- `COMMIT_GRASP` 后停止 tracking；
- close 期间不改变手臂目标；
- 夹爪受限速/限力控制；
- lift 高度来自真实观测或可靠状态，而不是 MuJoCo target body；
- lift 失败才触发 replan。

### 阶段 9：SDF-CBF-QP

先静态障碍，后动态障碍。

验收顺序：

```text
无障碍
有障碍但避障关闭
有障碍且静态避障
动态障碍且动态避障
```

每组记录：

```text
成功率
最小距离
CBF active 比例
q_cmd 修正量
到达时间
触碰/急停次数
```

---

## 14. 仿真回归如何保留

任何真机代码合入前都应继续运行 MuJoCo：

```text
颜色分割
AnyGrasp
状态机
tracking
close/lift/replan
静态避障
动态避障
```

建议最终提供两条完全独立的命令：

```bash
# 仿真
ros2 launch soarm100_bringup sim.launch.py ...

# 真机
ros2 launch soarm100_bringup real.launch.py ...
```

两者只能在 backend 和设备参数上不同。上层 Action 名称、状态机和日志字段
尽量一致。

真机 launch 必须检查：

```text
不能同时启动 MuJoCo policy backend
不能同时启动真机 hardware backend 两次
找不到串口时直接失败
标定文件缺失时直接失败
关节数量不匹配时直接失败
```

---

## 15. 真机成功判定不能照搬 MuJoCo

MuJoCo 可以直接读取：

```text
物体 body 位姿
接触对
target_lift
```

真机没有这些 ground truth。

真机的抓取成功判定应组合：

```text
夹爪最终位置没有完全闭合
夹爪负载/电流达到合理范围
腕部视觉中目标随夹爪一起上升
主相机中目标离开桌面
TCP 已执行 lift
```

第一版可以使用：

```text
TCP 上升超过阈值
+ 夹爪负载存在
+ 腕部目标仍可见且相对夹爪稳定
```

不能只用“发送了 close”判定成功。

---

## 16. 日志要求

真机每个控制周期至少记录：

```text
时间戳
状态机 phase
q_measured
dq_measured
q_command_before_safety
q_command_after_safety
servo raw tick
servo temperature/voltage/load
TCP measured
TCP target
tracking bbox/confidence/delta/data age
SDF min distance
CBF active
communication latency/error count
watchdog state
close command
lift verification signals
failure reason
```

日志必须区分：

```text
算法要求的命令
安全层裁剪后的命令
硬件实际反馈
```

否则无法判断问题来自 policy、安全层还是电机执行。

---

## 17. 当前建议的下一步

按优先级：

1. 数一下真实机械臂的舵机数量；
2. 给出控制板型号、连接方式和电源规格；
3. 连接 USB，只做串口与舵机扫描；
4. 在 `lerobot` 环境确认能读取全部舵机；
5. 导出真实舵机 ID、零位、方向和限位；
6. 根据真实 6/7 自由度决定是否能复用当前 checkpoint；
7. 再创建 `soarm100_hardware` 和 `soarm100_bringup`。

在第 6 步未解决前，不建议实现会写入真机位置命令的正式 backend。

---

## 18. 上电前检查表

每次真机实验前逐项确认：

- [ ] 机械臂牢固固定在桌面；
- [ ] 急停或断电开关可立即触达；
- [ ] 工作空间内没有人员和易碎物；
- [ ] 电源电压匹配 STS3215 版本；
- [ ] 串口设备名和 udev 规则正确；
- [ ] 舵机数量和 ID 全部匹配；
- [ ] 标定文件已加载；
- [ ] 当前反馈位置均在安全范围；
- [ ] 第一条 command 等于当前反馈位置；
- [ ] 最大速度和单周期增量已限制；
- [ ] watchdog 已启用；
- [ ] 温度、电压、负载监控已启用；
- [ ] 真机 backend 唯一运行；
- [ ] MuJoCo backend 未向同一 action server 抢占；
- [ ] 本次实验日志路径已设置；
- [ ] 先夹爪打开、低速、空载运行。

任何一项无法确认，都不应进入自动抓取。
