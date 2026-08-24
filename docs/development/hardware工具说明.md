# SO-100 Plus 七电机硬件工具

该目录保留 LeRobot 0.6.1 的 Feetech 总线实现，但不修改
`lerobot-main`。七电机的唯一映射定义位于：

```text
hardware/so100_plus/config.py
```

## 当前工具

### 0. 七轴保持下的交互式逐关节检查

该工具启动时让七个舵机共同保持当前姿态。终端中选择电机 ID，再输入相对
角度；完成后保持新姿态并继续接受下一项检查。输入 `q`、按 `Ctrl+C` 或发生
未捕获异常时都会关闭并核验七轴力矩。

```bash
conda activate lerobot
python hardware/tools/interactive_joint_check.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_new_arm.json \
  --max-angle-deg 20 \
  --speed-deg-s 5 \
  --log log/runtime/hardware/interactive_joint_check.jsonl \
  --confirm RUN_INTERACTIVE_JOINT_CHECK
```

每条命令仍须通过标定范围内缩 `100 counts` 后的软限位检查。角度是相对当前
保持目标的舵机轴角度，不是 policy/MuJoCo 关节角，也不是 TCP 位移。

### 1. 通信与位置只读扫描

```bash
conda activate lerobot
python hardware/tools/read_feetech7.py \
  --port /dev/ttyACM0 \
  --samples 20 \
  --period 0.5 \
  --log log/runtime/hardware/feetech7_read.jsonl
```

### 2. 寄存器只读快照

```bash
conda activate lerobot
python hardware/tools/snapshot_feetech7.py \
  --port /dev/ttyACM0 \
  --output log/runtime/hardware/feetech7_register_snapshot.json
```

该命令读取运行模式、位置限位、homing offset、PID、力矩/电流限制、
负载、温度和电压，不写寄存器。

### 3. 候选标定采集

```bash
conda activate lerobot
python hardware/tools/collect_feetech7_calibration.py \
  --port /dev/ttyACM0 \
  --range-seconds 15 \
  --margin-counts 30 \
  --output hardware/calibration/so100_plus_candidate.json
```

运行要求：

1. 机械臂断力矩并由人可靠支撑；
2. 首先摆到舒适参考姿态并记录七轴中心值；
3. 按终端提示，每次只移动一个关节；
4. 每个关节在 15 秒内走过安全范围；
5. `wrist_roll` 只移动到线缆允许的范围；
6. 夹爪只移动到机构自然极限，不用力掰动。

这里的“参考姿态”要求每个轴都能从该位置分别向正、反两个方向移动。
采集程序会拒绝只记录到参考点一侧的结果。编码器是 `0～4095` 的环形计数，
程序使用相对于参考点的有符号位移处理 `4095→0` 回绕，避免把腕部的小范围
跨零运动误判为接近整圈。

输出只是候选文件，其中 `direction` 和 `zero_offset_rad` 保持空值，
`approved_for_motion=false`。它不会写舵机，也不能直接用于驱动。

## 坐标转换边界

硬件接口最终需要两层转换：

```text
Feetech raw
  -> LeRobot 电机标准值
  -> sign + zero_offset
  -> policy/MuJoCo joint radians
```

不能把“校准参考中位”直接当作 MuJoCo 零位。后续需要逐轴确认真实正方向，
再求出 `direction` 和 `zero_offset_rad`。

## 暂未提供的动作命令

完成标定审核后，可运行单关节低速测试。默认只移动 `wrist_roll` 约 `+1°`
并返回起点：

```bash
python hardware/tools/test_single_joint.py \
  --port /dev/ttyACM0 \
  --joint wrist_roll \
  --delta-deg 1 \
  --duration 1.0 \
  --hold 0.5 \
  --calibration hardware/calibration/lerobot/so100_plus_7dof.json \
  --log log/runtime/hardware/test_wrist_roll_plus1.jsonl \
  --confirm MOVE_SINGLE_JOINT
```

安全行为：

- 启动时要求七轴力矩全部关闭；
- 只使能 `--joint` 指定的一个电机；
- 使能前先将目标写为当前位置；
- 拒绝超过 `5°` 的测试；
- 拒绝在标定端点 100 counts 内启动；
- 插值运动并自动返回起点；
- 记录目标、反馈、误差、负载、电流、电压和温度；
- 正常结束、异常和 `Ctrl+C` 都关闭所选关节力矩。

## Policy home 零位采集

在 `base` 环境显示 MuJoCo 参考姿态：

```bash
conda activate base
python hardware/tools/show_mujoco_reference_pose.py
```

保持 GUI 开启，在真机力矩关闭状态下手动摆成同一姿态。然后另开终端：

```bash
conda activate lerobot
python hardware/tools/capture_policy_home.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_7dof.json \
  --output hardware/calibration/policy_home_capture.json
```

采集严格只读。结果保存真机 raw、LeRobot 标准值和对应 policy home 弧度，
但在关节符号审核完成前不会自动批准映射。

## 真机到 MuJoCo 只读镜像

终端 A 使用 `base` 环境启动 MuJoCo UDP 接收器：

```bash
conda activate base
python hardware/tools/show_policy_joint_mirror.py \
  --host 127.0.0.1 \
  --udp-port 15001
```

终端 B 使用 `lerobot` 环境启动严格只读硬件流：

```bash
conda activate lerobot
python hardware/tools/stream_policy_joint_udp.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_7dof.json \
  --mapping hardware/calibration/policy_joint_mapping.json \
  --host 127.0.0.1 \
  --udp-port 15001 \
  --rate 20 \
  --log log/runtime/hardware/policy_joint_stream.jsonl
```

真机端要求七轴力矩全部关闭，只读取反馈并发送本机 UDP，不写任何电机寄存器。
手动小幅移动单个关节时，MuJoCo 应以相同物理方向跟随。接收超时后 GUI
保持最后姿态并打印 `STALE`，不会产生真机动作。

如果 policy home 的自然、线缆放松 `wrist_roll` 姿态落在已有标定范围外，
只重新采集并写入 ID6 范围：

```bash
python hardware/tools/recalibrate_wrist_roll_range.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_7dof.json \
  --seconds 15 \
  --margin-counts 30 \
  --confirm APPLY_WRIST_ROLL_RANGE
```

该工具保留 ID6 homing offset 和其他六轴全部标定，只更新腕部 roll 的
`Min_Position_Limit`、`Max_Position_Limit` 及对应 JSON。采集结束后仍需在
终端再次输入完整确认短语才会写入。

## ROS2 只读关节状态

七轴方向、零位和 MuJoCo 镜像确认后，可以由一个脚本启动硬件读取、ROS2
`/joint_states`、TF 和 RViz：

```bash
./ros2/run_hardware_state.sh --build
```

后续重复运行无需构建：

```bash
./ros2/run_hardware_state.sh
```

该脚本在 `lerobot` 环境读取 Feetech，在 ROS2 Humble 环境接收本机 UDP。
它发布：

```text
/joint_states                 sensor_msgs/JointState
/hardware/joint_state_stale   std_msgs/Bool
```

读取器发现任一电机力矩已开启时会拒绝启动。ROS2 接收端不会加载 LeRobot，
也没有电机写入接口；UDP 超过 0.5 秒未更新时 stale 变为 true。

## ROS2 受限单关节动作

这是 ROS2 真机写入链路的第一阶段，不能与只读状态脚本同时运行。终端 A：

```bash
./ros2/run_single_joint_service.sh --build
```

终端 B 先以 `wrist_roll +1°` 验证：

```bash
source /opt/ros/humble/setup.bash
source ros2/install/setup.bash
ros2 service call /hardware/move_single_joint \
  soarm100_interfaces/srv/MoveSingleJoint \
  "{joint: wrist_roll, delta_deg: 1.0, duration: 1.5, hold: 0.5, confirmation: MOVE_SINGLE_JOINT}"
```

约束：

- ROS2 层只接受 `±2°`；
- 底层再次检查标定范围与 100 counts 端点余量；
- 启动时要求七轴力矩全部关闭；
- 仅使能被指定的单个关节，并先写入当前位置防止跳变；
- 插值到目标、短暂停留、自动回到起点；
- 温度达到 55°C 时中止；
- 正常、异常、`Ctrl+C` 和服务超时均执行断力矩；
- 每次动作保存独立 JSONL 到 `log/runtime/hardware/`。

动作完成判定使用反馈闭环，而非仅判断命令是否发送完成。出程和返程在插值后
继续保持目标，默认要求连续 3 个样本误差不超过 8 counts（约 0.70°），
收敛限时 1 秒。该阈值由 wrist_roll 实测静态死区/齿隙确定，不是放宽到
任意过程误差。
任一阶段不收敛则服务返回失败；退出前关闭力矩并读回七轴
`Torque_Enable=0`，验证记录写入同一 JSONL。

如果动作进程异常退出，先停止所有占用串口的进程，再执行：

```bash
conda activate lerobot
python hardware/tools/disable_all_torque.py \
  --port /dev/ttyACM0 \
  --confirm DISABLE_ALL_TORQUE
```

工具会打印操作前后的七轴 `Torque_Enable`，只有读回全部为 0 才报告成功。

## ROS2 受限双关节同步动作

同一个硬件服务还提供：

```text
/hardware/move_joint_delta
soarm100_interfaces/srv/MoveJointDelta
```

`delta_rad` 使用固定 policy/MuJoCo 顺序：

```text
shoulder_rotation_joint
shoulder_pitch_joint
ellbow_joint
wrist_pitch_joint
wrist_jaw_joint
wrist_roll_joint
gripper_joint
```

当前最多允许两个非零分量，每轴绝对值不超过 `2°`。第一次测试：

```bash
ros2 service call /hardware/move_joint_delta \
  soarm100_interfaces/srv/MoveJointDelta \
  "{delta_rad: [0.0174533, 0.0, 0.0, 0.0, 0.0174533, 0.0, 0.0], duration: 2.0, hold: 0.5, confirmation: MOVE_MULTI_JOINT}"
```

这表示 policy 坐标下 `shoulder_rotation_joint +1°` 和
`wrist_jaw_joint +1°` 同步运动，然后同步返回。硬件端检查当前力矩、位置模式、
policy/MuJoCo 限位、标定 raw 限位、温度和反馈收敛。任一轴失败都会关闭并
读回验证七轴力矩。

`keep_target=false`（默认）会自动返程；`keep_target=true` 用于当前关节已
位于安全余量外时分段恢复，收敛后关闭力矩并保留新位置。例如 shoulder pitch
从 raw 下限附近向安全区恢复一小步：

```bash
ros2 service call /hardware/move_joint_delta \
  soarm100_interfaces/srv/MoveJointDelta \
  "{delta_rad: [0.0, 0.0349066, 0.0, 0.0, 0.0, 0.0, 0.0], duration: 3.0, hold: 0.5, keep_target: true, confirmation: MOVE_MULTI_JOINT}"
```

恢复模式只允许目标严格朝安全区移动；不能用它绕过正常限位。

## 自定义真机安全姿态

停止所有占用串口的服务，并在七轴断力矩、机械臂已摆成候选安全姿态后：

```bash
conda activate lerobot
python hardware/tools/capture_safe_pose.py \
  --port /dev/ttyACM0 \
  --output hardware/calibration/hardware_safe_pose_candidate.json
```

工具严格只读，检查七轴 raw 位置是否保留 100 counts 标定余量，以及转换后的
policy 弧度是否位于 MuJoCo 限位内。自动检查通过后仍保持：

```text
user_visual_approval=false
approved_for_recovery_motion=false
```

还需要人工确认无自碰撞/碰桌、腕部线缆松弛和相机线缆无拉扯，才能批准为
正式上电恢复目标。`hardware_safe` 表示控制器上电时可保持的默认 home，
不表示断力矩后能够抵抗重力；停机前必须支撑机械臂或先让其落到可靠支撑面。

当前已批准的恢复目标为：

```text
hardware/calibration/hardware_safe_pose.json
```

旧版目标备份为 `hardware_safe_pose_v1.json`。当前默认是重新采集的 v2：
shoulder pitch `-1.4480 rad`、elbow `+1.3683 rad`，重心更靠近底座。

ROS2 服务 `/hardware/move_named_pose` 会读取该文件，并拒绝任何未同时通过
自动检查、人工视觉确认和恢复运动批准的文件。第一阶段仅允许当前位置与目标
间最多两个关节存在有效误差，且每轴误差不超过 `2°`；这不是任意七轴姿态
控制，而是命名姿态链路的小范围回归测试。

推荐先用 `/hardware/move_joint_delta` 将两个轻载轴偏移 `+1°` 并保留目标，
再调用命名姿态服务返回：

```bash
ros2 service call /hardware/move_joint_delta \
  soarm100_interfaces/srv/MoveJointDelta \
  "{delta_rad: [0.0174533, 0.0, 0.0, 0.0, 0.0174533, 0.0, 0.0], duration: 2.5, hold: 0.5, keep_target: true, confirmation: MOVE_MULTI_JOINT}"

ros2 service call /hardware/move_named_pose \
  soarm100_interfaces/srv/MoveNamedPose \
  "{pose_name: hardware_safe, duration: 2.5, hold: 0.5, confirmation: MOVE_NAMED_POSE}"
```

两次动作结束都会关闭并读回验证七轴力矩。由于断力矩后承重轴可能受重力
移动，测试时仍需托住机械臂，并确保没有其他进程占用 `/dev/ttyACM0`。

## 常驻七轴上电控制器

正常控制不再使用“每条命令结束后断力矩”的验证脚本。启动：

```bash
./ros2/run_hardware_controller.sh
```

驱动在 LeRobot 环境中独占串口。它先读取七轴当前位置，把七个
`Goal_Position` 写成当前值，再统一开启力矩，因此启动本身不会要求机械臂
跳到预设姿态。运行期间持续保持位置，并从同一串口会话发布 `/joint_states`。
不要同时运行 `run_hardware_state.sh`、单关节服务或其他串口读取脚本。

绝对七轴目标使用固定 policy/MuJoCo 顺序：

```bash
ros2 service call /hardware/move_joint_target \
  soarm100_interfaces/srv/MoveJointTarget \
  "{position_rad: [0.124283, -1.638308, 1.630636, 0.056771, -0.047565, 0.136558, 0.043196], duration: 3.0, confirmation: MOVE_JOINT_TARGET}"
```

第一阶段每轴单次变化不得超过 `20°`，最大速度为 `20°/s`。控制器还检查
MuJoCo 关节限位、标定 raw 100-count 余量、55°C 温度保护和 12-count
到位误差。目标到达后继续保持，不会自动断力矩。

唯一例外是目标七轴数值与已批准的 `hardware_safe_pose.json` 完全匹配：
该请求允许从较远位置返回，但自动把最大速度降至 `10°/s`，同时仍执行全部
policy/raw 限位检查。普通任意目标不能借此绕过 `20°` 单次限幅。

控制器默认保持 shoulder lift 原始 `P_Coefficient=16`，并在上电前和退出
后读回验证。可选的 `--shoulder-lift-p` 参数仅保留给后续明确批准的受控
增益实验，不会由默认启动脚本启用。日志同时记录七轴
`Present_Current`、`Present_Load`、温度和位置误差。当前未对电流/负载 raw
值设置未经标定的附加阈值，舵机自身 Protection Current 仍保持有效。

显式断力矩：

```bash
ros2 service call /hardware/set_torque \
  soarm100_interfaces/srv/SetHardwareTorque \
  "{enabled: false, confirmation: SET_HARDWARE_TORQUE}"
```

断力矩后必须重启控制器才能重新上电，这确保重新上电前再次用当前位置初始化
七个目标。`Ctrl+C`、驱动退出和温度保护同样执行七轴断力矩及读回验证。
# Real wrist-camera hand-eye calibration

This calibration is isolated from the MuJoCo calibration code. The real
checkerboard stays fixed in the workspace and the powered robot moves the
wrist camera through different poses. The collector is read-only and never
commands a motor.

The current hand-eye board has 9 x 6 inner corners and a measured 14.4 mm square. The
rigid robot reference is `wrist_roll`, not the moving `gripper` link.

Start these in three terminals from the repository root:

```bash
# Terminal 1: hold the real arm, publish /joint_states and base->wrist_roll TF.
./ros2/run_hardware_controller.sh

# Terminal 2: publish wrist RGB and its calibrated CameraInfo.
./ros2/run_wrist_camera.sh

# Terminal 3: interactive read-only hand-eye collection.
./ros2/run_wrist_handeye.sh

# Terminal 4: separately approve and execute one candidate pose at a time.
./ros2/run_wrist_handeye_poses.sh
```

In the calibration preview:

```text
SPACE  capture the current image and synchronized wrist pose
S      solve all accepted samples with Tsai
Q/ESC  quit
```

Use at least 12 samples; 15-25 is preferable. Keep the board fixed. Change
both camera position and orientation, keep the whole board sharp and visible,
and avoid collecting many nearly identical poses. Every accepted sample is
saved immediately under `log/runtime/hardware/wrist_handeye/<timestamp>/`.

The solve produces `samples.json`, `wrist_handeye_tsai.json`, and an OpenCV
YAML file. `T_gripper_camera` means `T_wrist_roll_wrist_camera`: it maps a
point expressed in `wrist_camera_optical_frame` into `wrist_roll` coordinates.
The fixed-board translation/rotation spread is the primary consistency check;
a result with a large spread must not be deployed merely because a matrix was
produced.

Before starting the pose runner, use the Viewer to place the checkerboard far
enough from the wrist camera that the complete board is detected, then rigidly
fix the board. The runner uses the live startup joint pose as its visual center;
it no longer assumes that `hardware_safe` points at the board.

The pose runner reads
`hardware/calibration/handeye/wrist_handeye_poses.json`. It never moves on its
own: first type `START` to approve the visible center, then each candidate
prints all seven targets and deltas and requires the exact uppercase `MOVE`.
Enter `s` to reject a pose or `q` to stop. Only poses marked
`CAPTURE RECOMMENDED` should be captured; repeated center poses are transitions
that keep every command within the controller's 20-degree step gate. Do not
push an energized joint by hand.
