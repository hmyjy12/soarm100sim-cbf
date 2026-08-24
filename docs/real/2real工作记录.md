# 2Real 工作记录

本文记录 SO-ARM100 Plus 从仿真迁移到真机过程中已经确认的硬件版本、设备编号、相机标定流程和验证结果。设备节点（如 `/dev/video8`）可能在重新插拔或重启后变化，实际部署应优先使用 VID:PID 和序列号识别设备。

## 0. 2Real 代码边界

真机算法与仿真环境采用分离原则：

- `mujoco/` 保留独立的仿真场景、`play.py` 和回归实验；不作为真机控制入口。
- `ros2/soarm100_vision/` 是当前可部署控制、感知、SDF-CBF-QP 与硬件节点的实现包。
- `ros2/config/real/` 用于真实相机、外参、工作空间与安全参数；不得把机器相关数值散落在节点源码中。
- `ros2/scripts/real/` 是后续真机到达/避障的一键启动入口；`ros2/scripts/sim/` 仅用于 ROS2 算法经过 MuJoCo 后端的回归，不影响 `mujoco/play.py`。

本阶段不拆分现有 ROS2 Python 包，以免破坏已经验证过的硬件控制与相机标定入口；新文件依职责放入 `perception`、`safety`、`control`、`hardware` 对应模块，稳定后再做专门的多包重构。

### 0.1 真机七轴校准教程

#### 0.1.1 先区分三类数据

真机调试中容易把下面三件事统称为“校准”，但它们不能互相替代：

1. **LeRobot 电机校准**：建立各舵机原始编码器值与 LeRobot 角度之间的关系，
   记录 `range_min`、`range_max`、`homing_offset`。当前文件是
   `hardware/calibration/lerobot/so100_plus_new_arm.json`。
2. **Policy/MuJoCo 关节映射**：把 LeRobot 角度转换成 policy 使用的七关节角，
   包括关节名称、方向符号和 policy 零点。当前文件是
   `hardware/calibration/policy_joint_mapping.json`。
3. **安全姿态**：只是一组允许上电保持或返回的关节目标，不决定编码器范围、
   关节正负方向或 policy 零点。

重新做 LeRobot 校准后，即使七个舵机型号和 ID 没变，归一化角度和零点也可能
变化。因此必须重新采集 policy home 并完成 MuJoCo 只读映射验证，不能直接恢复
policy 抓取。

七个电机 ID 为：`shoulder_pan=1`、`shoulder_lift=2`、`elbow_flex=3`、
`wrist_flex=4`、`wrist_yaw=5`、`wrist_roll=6`、`gripper=7`。

#### 0.1.2 校准前检查与备份

校准期间机械臂必须断力矩并由人托住，周围不得有碰撞物。先进入项目和 LeRobot
环境：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
conda activate lerobot
```

检查串口权限和占用：

```bash
id -nG
test -r /dev/ttyACM0 && echo "串口可读" || echo "串口不可读"
test -w /dev/ttyACM0 && echo "串口可写" || echo "串口不可写"
sudo fuser -v /dev/ttyACM0
```

`fuser` 无输出才表示串口空闲。若有输出，应先识别并正常停止对应的硬件节点；
不要使用无范围的 `pkill python`。随后只读检查七轴状态：

```bash
python hardware/tools/read_feetech7.py \
  --port /dev/ttyACM0 \
  --samples 3 \
  --period 0.2 \
  --log log/runtime/hardware/new_arm_pre_calibration_read.jsonl
```

七个 `Torque_Enable` 必须全部为 `0`。如果不是，执行显式断力矩：

```bash
python hardware/tools/disable_all_torque.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_new_arm.json \
  --confirm DISABLE_ALL_TORQUE
```

保存校准前寄存器快照并备份当前 JSON：

```bash
python hardware/tools/snapshot_feetech7.py \
  --port /dev/ttyACM0 \
  --output log/runtime/hardware/new_arm_register_before_recalibration.json

cp hardware/calibration/lerobot/so100_plus_new_arm.json \
  hardware/calibration/lerobot/so100_plus_new_arm.before_recalibration.json
```

#### 0.1.3 怀疑单个关节时先做只读审计

如果只是怀疑第三轴 `elbow_flex` 的校准上限不合理，先不要直接重写寄存器。断力矩
并托住机械臂，运行较长时间的只读记录：

```bash
python hardware/tools/read_feetech7.py \
  --port /dev/ttyACM0 \
  --samples 400 \
  --period 0.05 \
  --log log/runtime/hardware/elbow_range_audit.jsonl
```

记录期间只缓慢转动第三轴，覆盖机械结构允许的完整安全范围，不顶机械限位。
当前校准中 `elbow_flex` 的范围是 `[899, 3105]` counts；真机流式控制还会在
两端保留安全余量。如果肉眼觉得没有越界，但日志中的原始编码器确实超过当前
范围，才说明校准范围可能需要重做。负载、电流或目测角度不能代替原始编码器值。

当前工程只有 `wrist_roll` 专用的有限范围重校工具，没有 elbow 单轴写入工具；
不要把 `recalibrate_wrist_roll_range.py` 用于第三轴。官方 LeRobot 校准是七轴全量
校准，执行时七个轴都必须完整活动。

#### 0.1.4 执行官方七轴校准

确认机械臂断力矩、串口空闲并有人托住后运行：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
conda activate lerobot

lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=so100_plus_new_arm \
  --robot.calibration_dir="$PWD/hardware/calibration/lerobot"
```

如果终端提示使用已有校准文件或重新校准，输入小写 `c` 再按 Enter，才会进入
重新采集；直接按 Enter 表示把已有 JSON 再写回电机，并不会重新测量范围。

正式采集顺序：

1. 先把七个关节手动放到各自安全活动范围的大致中间位置，再按 Enter。
2. 进入 `Recording positions` 后，依次让每个关节缓慢覆盖完整安全范围。
3. `wrist_roll` 只能覆盖线缆允许的有限范围，禁止为了接近 `0..4095` 而绕线。
4. 夹爪也要从安全全开移动到安全全闭。
5. 七个轴全部完成后按 Enter 结束，确认文件保存到
   `hardware/calibration/lerobot/so100_plus_new_arm.json`。

不要只活动 elbow：未活动的轴会被记录成很窄或错误的范围，随后所有真机控制都
可能被错误拒绝。

#### 0.1.5 校准后核验

先保持断力矩，再读取并保存校准后的寄存器：

```bash
python hardware/tools/snapshot_feetech7.py \
  --port /dev/ttyACM0 \
  --output log/runtime/hardware/new_arm_register_after_recalibration.json

python hardware/tools/read_feetech7.py \
  --port /dev/ttyACM0 \
  --samples 20 \
  --period 0.2 \
  --log log/runtime/hardware/new_arm_after_recalibration_read.jsonl
```

检查项：七轴 `Torque_Enable=0`；当前位置位于各自 `Min/Max_Position_Limit`
之间；电压约为 12 V；温度无异常；`wrist_roll` 范围没有超过线缆安全区。

然后把断力矩机械臂手动放到 MuJoCo/policy 的标准 home 姿态，采集该姿态的真机
编码器对应值：

```bash
python hardware/tools/capture_policy_home.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_new_arm.json \
  --output hardware/calibration/policy_home_capture_new_arm.json
```

该命令**只采集并输出对照数据，不会自动更新**
`hardware/calibration/policy_joint_mapping.json`。必须比较新的 home 采集结果，确认
七轴符号仍正确并更新必要的零点偏置，然后执行下一节的 MuJoCo 严格只读映射
验证。映射未通过前，不运行 policy、抓取、回原点或多关节上电动作。

如果新校准明显错误，可用备份 JSON 恢复文件；但只复制 JSON 不等于恢复电机
寄存器。需要再次运行 `lerobot-calibrate`，在提示处直接按 Enter，才会把该 ID
关联的已有校准写回电机。执行恢复前仍需断力矩、托住机械臂并保存当前快照。

完整通过条件：

- 七轴原始范围覆盖真实安全活动范围，不触碰机械止挡或拉扯线缆。
- 当前位置和常用安全姿态位于校准范围内部，而不是紧贴端点。
- policy home 对照完成，名称、方向和零点映射均已复核。
- 下一节 MuJoCo 镜像中七轴一一对应、方向一致且静止无跳变。
- 最后再进行 `interactive_joint_check.py` 的低速小角度上电验证。

### 0.2 MuJoCo 严格只读关节映射验证

在启用真机 policy 主动控制前，先用 MuJoCo GUI 检查七个真机关节的
名称、方向、零点和大致转动幅度是否与仿真模型一致。该链路严格只读：
真机端只读取 Feetech 编码器，通过 UDP 发送 policy 关节角；MuJoCo 端只
更新 `qpos` 并调用 `mj_forward()` 显示姿态，不执行 `mj_step()`，也没有反向
下发电机命令的通道。

相关文件：

- `hardware/tools/stream_policy_joint_udp.py`：读取编码器，执行 LeRobot 标定和关节映射，发送 UDP 并写日志。
- `hardware/tools/show_policy_joint_mirror.py`：接收 UDP 关节角并在 MuJoCo GUI 中显示。
- `hardware/calibration/lerobot/so100_plus_new_arm.json`：当前新机械臂的 LeRobot 标定。
- `hardware/calibration/policy_joint_mapping.json`：真机关节到 policy/MuJoCo 关节的名称、符号和零点映射。

验证前必须确认七轴力矩全部关闭，且串口没有被其他进程占用：

```bash
sudo fuser -v /dev/ttyACM0
```

无输出表示当前没有进程占用串口。若任一电机的 `Torque_Enable` 不为 `0`，
只读发送端应拒绝继续运行。

终端 A 启动 MuJoCo 映射窗口：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
conda activate base

python hardware/tools/show_policy_joint_mirror.py \
  --mjcf SO-ARM100/Simulation/SO100/mujoco/so100_plus.xml \
  --host 127.0.0.1 \
  --udp-port 15001
```

终端 B 启动真机严格只读发送：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
conda activate lerobot

python hardware/tools/stream_policy_joint_udp.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_new_arm.json \
  --mapping hardware/calibration/policy_joint_mapping.json \
  --host 127.0.0.1 \
  --udp-port 15001 \
  --rate 20 \
  --print-period 3 \
  --log log/runtime/hardware/new_arm_policy_joint_mirror.jsonl
```

启动顺序为终端 A、终端 B。在真机断力矩状态下，每次只缓慢转动一个
关节，观察 MuJoCo 中对应关节的方向和大致幅度。依次检查五个臂关节、
`wrist_roll` 和夹爪；`wrist_roll` 只能在线缆安全的有限范围内转动。

通过条件：

- 七个关节一一对应，真机与 MuJoCo 转动方向一致。
- 真机静止时，MuJoCo 姿态稳定，没有跳变或持续漂移。
- 真机小幅转动时，MuJoCo 中只有对应关节产生同向变化。
- 夹爪开合方向一致，手腕 roll 方向与线缆安全范围一致。
- 发送端日志持续更新，接收端显示数据为 `LIVE`。

该测试只验证关节映射、方向和粗略零点，不能代替 TCP/FK 精度验证、
相机内参或手眼标定。MuJoCo 显示端会将超出 MJCF 限位的值裁剪到模型范围，
因此应在正常工作区间内进行映射检查，不使用该窗口判断真机机械限位。
任一终端均可使用 `Ctrl+C` 结束；该链路不会给机械臂上电。

### 0.3 七轴保持下的交互式逐关节检测（2026-08-06）

#### 0.3.1 目的与适用边界

真机 policy 位姿到达测试中观察到 TCP 存在额外的 Y/Z 偏移，并怀疑第三轴
`elbow_flex` 在机械臂自重下抬升能力不足。为区分 policy、TCP/FK 与舵机运控层
问题，新增独立硬件诊断工具：

```text
hardware/tools/interactive_joint_check.py
```

该工具不加载 PPO，不计算 TCP，不调用 AnyGrasp、视觉或避障。启动后七个舵机
共同保持当前姿态，用户在同一个终端内反复选择一个电机 ID 和相对角度；每次只
修改该轴目标，其余六轴持续保持。动作结束后不自动返回，而是保持新的七轴姿态，
继续等待下一项检查。输入 `q`、按 `Ctrl+C`、终端输入关闭或发生未捕获的通信/
温度异常时，统一关闭并核验七轴力矩。

该测试回答的是“某个舵机在整机真实负载下能否跟随一个小角度位置命令”，不能
单独证明 policy、关节映射、TCP 标定或笛卡尔轨迹正确。

#### 0.3.2 电机 ID

| ID | 硬件名称 | policy/MuJoCo 名称 |
|---:|---|---|
| 1 | `shoulder_pan` | `shoulder_rotation_joint` |
| 2 | `shoulder_lift` | `shoulder_pitch_joint` |
| 3 | `elbow_flex` | `ellbow_joint` |
| 4 | `wrist_flex` | `wrist_pitch_joint` |
| 5 | `wrist_yaw` | `wrist_jaw_joint` |
| 6 | `wrist_roll` | `wrist_roll_joint` |
| 7 | `gripper` | `gripper_joint` |

交互输入的角度是**舵机编码器轴相对角度**，不是 TCP 位移，也没有经过 policy
关节符号映射。此前方向验证结果为 `elbow_flex` 正方向向下，因此检查第三轴抬升
能力时使用负角度。

#### 0.3.3 运行方式

启动前确认串口没有被其他硬件控制器或残留进程占用：

```bash
sudo fuser -v /dev/ttyACM0
```

无输出后运行：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
conda activate lerobot

python hardware/tools/interactive_joint_check.py \
  --port /dev/ttyACM0 \
  --calibration hardware/calibration/lerobot/so100_plus_new_arm.json \
  --max-angle-deg 20 \
  --speed-deg-s 5 \
  --log log/runtime/hardware/interactive_joint_check.jsonl \
  --confirm RUN_INTERACTIVE_JOINT_CHECK
```

第三轴建议先分段验证，不直接从未知负载姿态一次走满：

```text
Motor ID [1-7, q]: 3
Relative angle ...: -10

# 第一段正常后，再次选择 ID 3；第二个 -10° 相对当前保持目标累计到 -20°
Motor ID [1-7, q]: 3
Relative angle ...: -10
```

测试完成输入：

```text
Motor ID [1-7, q]: q
```

随后必须看到七个 `Torque_Enable` 均为 `0` 的核验输出。

#### 0.3.4 当前安全规则

- 启动时要求七轴原本全部断力矩、全部处于位置模式。
- 上电前先把七轴 `Goal_Position` 写为各自实测位置，避免上电跳变。
- 单条相对角命令必须有限、非零且位于 `±20 deg` 内。
- 默认速度为 `5 deg/s`，20 deg 动作至少插值执行 4 s。
- 目标必须位于当前新机械臂 LeRobot 标定范围内缩 `100 counts` 后的软区间。
- 若目标越界或实测位置与当前保持目标相差超过 `80 counts`，打印
  `REFUSE ANGLE`，不执行该命令，并继续等待输入。
- 等待终端输入期间仍每秒刷新七轴保持目标并记录健康状态。
- 动作和等待期间记录七轴位置误差、电流、负载与温度；任一轴达到
  `55 C` 时按安全异常退出并断电。
- 选中轴在目标附近连续三帧达到默认 `15 counts` 容差时打印 `PASS`；超时则
  打印 `NOT_CONVERGED`，但保留目标继续保持，供观察静态下坠和稳态误差。

日志默认保存到：

```text
log/runtime/hardware/interactive_joint_check.jsonl
```

关键阶段包括 `startup_hold`、`command`、`motion`、`settle`、`result`、
`idle_health` 和 `torque_off_verification`。分析第三轴时重点比较
`goal_raw`、`position_raw`、`error_counts`、`current_raw` 与 `load_raw`：若小角度
开始就持续落后，优先检查舵机、机械阻力或供电；若只有负载较大或角度较大时
失去跟随，则更像负载能力不足。

**当前状态：** 工具已完成 Python 静态编译与参数入口检查，真机动态结果待本轮
`interactive_joint_check.jsonl` 产生后确认。

### 0.4 真机 policy 位姿到达（首版）

首版不依赖相机、YOLO、SAM、AnyGrasp 或避障。目标 TCP 位姿以 `base` 坐标系
写入：

```text
ros2/config/real/policy_reach_target.json
```

字段 `position_m` 单位为 m，四元数为 `quaternion_wxyz`。后续 AnyGrasp 只需向
同一输入接口提供 `base` 下 TCP pose；不应把 AnyGrasp 相机系位姿直接传给 policy。

控制链为：

```text
/joint_states -> 27D training observation -> PPO mean action
-> action scale/filter -> per-step clamp -> /hardware/joint_target
-> Feetech streaming safety validation -> motor bus
```

#### 0.4.1 关节限位 CBF-QP 安全过滤（2026-08-11）

为避免 policy 在接近关节边界时反复生成越界目标、最终被硬件层整帧拒绝，
在命令整形器生成参考速度后、积分得到 `q_ref` 前加入关节空间 CBF。它读取
当前 LeRobot 校准和 `policy_joint_mapping.json`，把内缩后的 raw 安全范围转换为
policy radians。对每个关节施加：

```text
-alpha * (q - q_safe_min) <= qdot
qdot <= alpha * (q_safe_max - q)
```

远离边界时该约束不改变 policy；越靠近边界，继续向外的允许速度越小；已经位于
软边界外时，只允许以恢复速度返回安全区。该凸 QP 的目标是最小化安全速度与
policy 参考速度的差，当前独立盒约束具有闭式投影解，因此不依赖外部 QP 求解器。

实现文件：

- `control/joint_limit_cbf.py`：生成线性 CBF 速度上下界。
- `control/policy_command_shaper.py`：在参考速度积分前执行最小修改投影。
- `hardware_joint_limit_filter.py`：将真机 raw 安全范围转换为 policy radians。
- `policy_reach_node.py`：接入过滤、逐帧日志和无进展判定。

默认参数：

- `enable_joint_limit_cbf=true`
- `hardware_limit_margin_counts=100`
- `joint_limit_cbf_alpha=4.0`
- `joint_limit_cbf_activation_margin_rad=0.25`
- `joint_limit_cbf_recovery_velocity_rad_s=0.05`
- 连续受限 `2.0 s` 且 TCP 最佳误差改善不足 `0.003 m` 时返回
  `JOINT_LIMIT_STALLED`，不再等待完整 policy timeout。

完整抓取默认开启。显式对比开关：

```bash
./ros2/scripts/real/run_single_grasp_2real.sh \
  --class jpgCat \
  --device 0 \
  --show-window on \
  --joint-limit-cbf on \
  --max-tracking-error-rad 0.25 \
  --confirm RUN_SINGLE_GRASP
```

单独 policy 到达也可使用：

```bash
./ros2/scripts/real/run_policy_reach.sh \
  --relative-delta 0.02,0,0 \
  --rate 20 \
  --joint-limit-cbf on \
  --confirm RUN_POLICY_REACH
```

回归对比时可传 `--joint-limit-cbf off`，但硬件控制器的 raw 限位始终保留，
不能通过该开关关闭。CBF只能平滑避免关节撞向边界；如果目标本身对 policy
不可达，最终会返回 `JOINT_LIMIT_STALLED`，应换 AnyGrasp 候选。

**同步过渡层（2026-08-06）：** 电机内部位置环并不是 `10 Hz`；原来的
`10 Hz` 是 ROS2 `/joint_states` 反馈发布频率，底层驱动原本已以 `20 Hz`
重复写入最新 `Goal_Position`。现在默认将反馈、policy 和驱动上位机循环
统一设为 `20 Hz`，并改为每收到一帧新关节反馈才计算和发送一次 policy
目标。反馈断流时 watchdog 仅负责停止，不使用旧状态继续生成命令。

独立整形模块：

```text
ros2/soarm100_vision/soarm100_vision/control/policy_command_shaper.py
```

当前默认功能和保守参数：

- 使用每帧实际 `dt` 计算 action 和编码器速度低通，不假设计时器绝对准时。
- 独立维护连续 `q_ref`，不再把每帧编码器量化波动直接复制到新目标。
- 最大参考速度 `0.20 rad/s`。
- 最大参考加速度 `0.80 rad/s^2`，正反方向切换必须经过连续过渡。
- `q_ref` 与实测关节的最大跟踪误差默认设为 `0.25 rad`（约 `14.3°`）；该值是参考关节位置相对实测关节位置的最大允许偏差，不是单步转角。可通过 `run_policy_reach.sh --max-tracking-error-rad` 显式覆盖
  （约 `5.7 deg`），使肩部/肘部负载轴可以建立足够的位置环误差；硬件驱动
  仍以独立的 `6 deg` 流式目标限制兜底。
- 夹爪在位姿到达阶段仍冻结在实测初始位置。

一键脚本参数 `--rate` 会同时传递给反馈、policy 和底层驱动：

```bash
./ros2/scripts/real/run_policy_reach.sh \
  --rate 20 \
  --confirm RUN_POLICY_REACH
```

`--rate 20` 表示上位机每秒使用新反馈执行约 20 次 policy 推理和关节目标下发，
即周期约 `50 ms`；它不是舵机内部位置环频率。当前允许范围为 `5～30 Hz`。

相对 TCP 测试目标使用独立限制，默认允许三维位移向量的欧氏范数不超过
`0.10 m`。例如 `--relative-delta 0.08,0,0` 的范数为 `0.08 m`，允许执行；
同时生成后的绝对目标还必须满足 base 工作空间：

```text
x: [0.08, 0.45] m
y: [-0.30, 0.30] m
z: [0.05, 0.45] m
```

需要采用更小的实验上限时可以显式指定：

```bash
./ros2/scripts/real/run_policy_reach.sh \
  --relative-delta 0.04,0,0 \
  --max-relative-delta-m 0.05 \
  --rate 20 \
  --confirm RUN_POLICY_REACH
```

不能仅根据设定值宣称实际频率已达到 `20 Hz`。新 policy JSONL 日志会逐帧记录
`raw_dt_s`、`dt_s`、`qvel_raw`、`qvel_filtered`、`filtered_action`、
`desired_velocity_rad_s`、`reference_velocity_rad_s`、`q_ref` 和 `tracking_error_rad`。
底层 `controller_*.jsonl` 新增每条成功接收的 `stream_target`，可以对照
policy 发送值、映射后编码器目标和当时编码器反馈。首轮真机试验应先统计
`raw_dt_s` 的平均值、P95、最大值和丢帧，确认 `20 Hz` 串口链路稳定后再考虑
提升到训练频率 `30 Hz`。

MuJoCo 在该链路中仅用于与训练一致的 FK、TCP 定义和 observation 构造，不启动
物理仿真、GUI 或 `mujoco/play.py`。硬件侧额外执行关节模型限位、原始编码器安全
区间、单次流式目标最大 6 deg、温度保护、串口断开保护和 0.5 s 无新命令保持。

初次运行命令：

```bash
./ros2/scripts/real/run_policy_reach.sh \
  --build \
  --confirm RUN_POLICY_REACH
```

该脚本退出时会请求 `/hardware/set_torque` 关闭全部力矩。初次调试目标仅相对已批准
安全姿态 TCP 移动约 23 mm，并保持原姿态；确认物理方向、TCP 与动作尺度后，才可
编辑 `policy_reach_target.json` 增大范围。

**首轮联调诊断（2026-08-05）：** 若启动日志显示策略持续输出 `dq_cmd`，但 TCP
误差完全不变，应先检查硬件控制器日志中是否出现 `stream target rejected`。首次实测
中 `shoulder_pitch_joint=-3.2448 rad` 低于 MuJoCo 训练下限 `-pi`，旧逻辑裁剪回模型边界后
形成 `+5.91 deg` 指令跳变，被当时的硬件 `3 deg` 流式限幅拒绝。现在改为从真机实测角度
先从真机实测角度小步恢复到 policy 训练范围内侧，再积分 PPO 输出；超出训练范围会记录
泛化风险警告，但不拒绝启动，也不要求回到某个固定的 `hardware_safe_pose`。真机
是否允许执行仅由标定编码器安全区间、单步限幅、温度和电流保护决定。
若启动时已处于编码器端点预留区，该关节只允许向安全区内恢复，向外的指令分量保持在当前位置。

启动脚本还会在上电前拒绝以下残留状态：串口被占用、`run_hardware_controller.py` 或
`hardware_controller_node` 仍在运行、已有 `/hardware/set_torque` 或
`/hardware/move_joint_target` service。它不会自动结束未知进程；先明确打印 PID，
避免新 policy 错误接入早期遗留的 ROS2 controller。脚本仅清理自身创建的控制器进程组。

### 0.5 真机 Orbbec 静态障碍 SDF-CBF（2026-08-20）

真机首版复用 MuJoCo 的全臂胶囊、点云 SDF 和最小修正 CBF-QP，不增加路径
规划器。眼在手外 Orbbec 的注册深度转换到 `base` 后，按深度时间戳匹配最近
`/joint_states`，通过 MuJoCo FK 实时更新七段胶囊并删除机器人自身点云。静态
障碍仍逐帧更新，只将障碍速度设为零；无效深度暂不生成障碍点。

首轮固定参数：自身剔除额外 `20 mm`、CBF 表面安全距离 `50 mm`、硬停止距离
`30 mm`、体素 `10 mm`、点云/关节最大时间差 `75 ms`、障碍点云超时
`300 ms`、关节速度/加速度 `0.10 rad/s` 和 `0.40 rad/s^2`。点云缺失、坐标系
不是 `base`、QP 不可行或进入硬停止距离都会保持当前关节并终止。

先启动 Orbbec：

```bash
./ros2/scripts/real/run_orbbec_rgbd.sh
```

无位移感知检查（只保持当前 TCP 30 秒）：

```bash
./ros2/scripts/real/run_policy_reach.sh \
  --build \
  --relative-delta 0,0,0 \
  --obstacle-cbf on \
  --joint-limit-cbf on \
  --max-joint-velocity-rad-s 0.10 \
  --max-joint-acceleration-rad-s2 0.40 \
  --hold-current-duration-s 30 \
  --confirm RUN_POLICY_REACH
```

障碍物偏置后的首轮运动目标使用当前 TCP `+(0.08,0,0.02) m`：

```bash
./ros2/scripts/real/run_policy_reach.sh \
  --relative-delta 0.08,0,0.02 \
  --obstacle-cbf on \
  --joint-limit-cbf on \
  --max-joint-velocity-rad-s 0.10 \
  --max-joint-acceleration-rad-s2 0.40 \
  --success-position-m 0.010 \
  --success-orientation-deg 15 \
  --timeout-s 40 \
  --confirm RUN_POLICY_REACH
```

桌面过滤高度默认仍为 `base z=0.055 m`，现场值不同时必须通过
`--table-z-max-m` 显式覆盖。点云前端日志为
`log/runtime/hardware/policy_reach_obstacle_cloud.log`，policy 逐帧日志继续写入
`log/runtime/hardware/policy_reach.jsonl`。

#### 0.5.1 wrist_jaw 局部定向自身包络（2026-08-21）

实机点云可视化确认，腕部中央高出的白色结构属于 `wrist_jaw`，其顶部和附着
线缆无法由 `wrist_pitch -> wrist_jaw -> wrist_roll` 两段对称胶囊完整覆盖。
因此在七段胶囊自身过滤之外，增加一个随 `wrist_jaw` 位姿实时更新的定向盒。
该盒只用于从 Orbbec 障碍点云中剔除机器人自身点，不改变 CBF 的障碍安全距离。

参数来自 `assets_plus/wrist_jaw.STL` 的局部包围盒：

| 项目 | 数值 |
|---|---:|
| 绑定 body | `wrist_jaw` |
| STL 局部最小坐标 | `(-17.0, -20.613, -23.8) mm` |
| STL 局部最大坐标 | `(57.2, 20.613, 66.6) mm` |
| 局部中心 | `(20.1, 0.0, 21.4) mm` |
| STL 紧包围盒尺寸 | `74.2 x 41.226 x 90.4 mm` |
| 每侧过滤余量 | `4 mm` |
| 实际过滤盒尺寸 | `82.2 x 49.226 x 98.4 mm` |

`run_policy_reach.sh` 在启用 obstacle CBF 时默认打开该包络；需要进行关闭对照时
显式传入 `--wrist-attachment-box off`。弯曲细线连通域识别
`--attached-thin-filter` 仍默认关闭，因为首轮实测没有稳定命中。

MuJoCo 范围检查：

```bash
python hardware/tools/show_wrist_attachment_envelope.py --no-oscillate
```

洋红色为实际过滤盒，青色为 STL 紧包围盒。真机零位移检查应观察
`log/runtime/hardware/policy_reach_obstacle_cloud.log` 中的 `wrist_box_rm`：大于零表示
该局部盒确实删除了深度点；同时 GUI 中这些点不应继续显示为绿色 CBF 障碍物。

#### 0.5.2 非刚性附件 link-relative occupancy 采集（2026-08-21）

线缆不使用统一扩大的刚体包络。空场景下由机械臂自动执行 25 个相对启动姿态，
覆盖 `wrist_pitch`、`wrist_jaw`、`wrist_roll`、`ellbow+wrist_pitch` 及相邻腕部
组合。正负偏置之间插入中心过渡，任意相邻姿态最大单关节变化
`0.34 rad = 19.48 deg`，低于驱动普通目标的 `20 deg` 硬限制。默认每段运动
`7 s`，最大平均关节速度约 `0.049 rad/s`；到位后静置 `0.75 s`，保存 8 帧
原始深度、内参、目标关节角和按时间戳匹配的 encoder 关节角。

采集前必须清空机械臂完整运动空间并提前启动 Orbbec。采集器目标同时受 MuJoCo
关节范围和新臂标定 encoder 内缩安全区间约束；启动姿态或目标越界时拒绝/跳过，
不会通过裁剪生成未批准目标。异常、Ctrl+C 和正常结束都会请求断力，序列结束前
先回到采集启动姿态。

```bash
./ros2/scripts/real/run_collect_link_self_occupancy.sh \
  --frames-per-pose 8 \
  --settle-s 0.75 \
  --move-duration-s 7.0 \
  --confirm COLLECT_LINK_SELF_OCCUPANCY
```

数据写入 `log/runtime/hardware/link_self_occupancy/<timestamp>/`。完成后离线构建：

```bash
python hardware/tools/build_link_self_occupancy.py \
  log/runtime/hardware/link_self_occupancy/<timestamp> \
  --output hardware/calibration/link_self_occupancy.npz
```

构建器先执行工作区/桌面过滤，再使用七段 FK 胶囊和已确认的 `wrist_jaw` 定向盒
删除刚性自身点。剩余近场点转换到最近的 `ellbow`、`wrist_pitch`、`wrist_jaw`
或 `wrist_roll` 局部坐标系，以 `8 mm` 体素统计跨帧出现次数和概率。

只读 MuJoCo 检查：

```bash
python hardware/tools/show_link_self_occupancy.py \
  hardware/calibration/link_self_occupancy.npz \
  --min-probability 0.10
```

生成的 JSON 元数据固定包含 `runtime_enabled=false`。本阶段模型只用于检查，不会
自动接入 CBF；确认高概率体素只覆盖电线/接头后，再实现运行时高置信度过滤和
中置信度 link/world 运动一致性分类。

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
log/runtime/hardware/wrist_handeye/<timestamp>/samples.json
log/runtime/hardware/wrist_handeye/<timestamp>/wrist_handeye_tsai.json
log/runtime/hardware/wrist_handeye/<timestamp>/wrist_handeye_tsai.yaml
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
log/runtime/hardware/wrist_handeye/20260805_110442/
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
log/runtime/hardware/wrist_handeye/20260805_110442/wrist_handeye_tsai.yaml
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
log/runtime/hardware/orbbec_handeye/20260805_140910/
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

**第二轮（20260805_143740，22 样本）— 历史采用版**

```text
log/runtime/hardware/orbbec_handeye/20260805_143740/
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

**历史结论：** **20260805_143740** 曾作为 2Real Orbbec 眼在手外外参，已于 2026-08-07 因相机高度调整而废止。

该历史结果位于：

```text
log/runtime/hardware/orbbec_handeye/20260805_143740/orbbec_eye_to_hand_tsai.yaml
```

或同目录 `orbbec_eye_to_hand_tsai.json`。

**第三轮（20260807_155222，17 样本）— 当前采用版**

本轮在 Orbbec 主相机物理高度下降后重新标定。平移 RMS `14.1 mm`、平移最大误差 `25.4 mm`、旋转 RMS `2.80 deg`、旋转最大误差 `7.20 deg`、PnP 重投影 RMS `0.259 px`。样本平移覆盖 X/Y/Z 约 `170/284/133 mm`，姿态两两差异中位数 `57.1 deg`。

原始结果：

```text
log/runtime/hardware/orbbec_handeye/20260807_155222/
```

当前稳定配置：

```text
hardware/calibration/camera/orbbec_eye_to_hand_current.json
hardware/calibration/camera/orbbec_eye_to_hand_current.yaml
hardware/calibration/camera/real_camera_calib.json
```

`orbbec_eye_to_hand_current.*` 保存原始 `camera_color_optical_frame -> base` 外参。`real_camera_calib.json` 是现有 ROS2 后端可直接读取的坐标约定适配版。真机启动时使用 `use_sim_camera_extrinsics:=false`；MuJoCo 仍使用 `true`，不受此配置影响。

#### 3.15.5 复标注意点

1. 棋盘夹死后整场勿松夹、勿换夹；夹爪开合整场锁定。
2. 第一次 SPACE 仅上电；松手稳定且 Viewer `DETECTED` 后再第二次 SPACE 采集。
3. 采完一条先 `m` 下电再挪臂，避免带力换姿。
4. 关闭官方 Orbbec Viewer 后再跑脚本（USB 独占）。
5. 若相邻采集后 board_in_gripper 仍大幅跳变，优先查夹持而非继续堆样本。

### 3.16 固定类别视觉模型接入（2026-08-07）

目标识别新增 `fixed_yolo_sam` 可选链路，第一版只验证主摄目标检测、SAM
遮罩和目标点云，不启动真机运动：

```text
Gemini 336 RGB-D（depth registration）
  -> 固定类别 YOLO：jpgCat / Chiikawa / tissue
  -> MobileSAM：bbox prompt -> 原始目标 mask
  -> mask + 对齐 depth + color CameraInfo -> camera optical frame 目标点云
```

一键启动：

```bash
./ros2/scripts/real/run_fixed_yolo_sam_mask.sh \
  --build \
  --class jpgCat \
  --device 0
```

输出协议与原抓取链路一致：`/target/mask`、`/target/mask_expanded`、
`/target/cloud`、`/target/cloud_roi`、`/target/center` 和
`/target/segmentation_status`。因此后续可以直接接 AnyGrasp，而无需修改抓取
规划接口。此阶段仍需人工用叠加窗口确认 bbox 与 SAM mask 是否正确覆盖目标。

2026-08-07 首次真机调用已成功：`jpgCat` 置信度 `0.4758`，SAM mask
`2908 px`，有效目标深度点 `2850`，主相机光学系中心为
`(0.2375, 0.0675, 0.4950) m`。该结果证明 RGB-D topic、固定类别检测、SAM
和 mask-depth 反投影链路已连通；下一步仍需在有窗口模式下人工检查遮罩边界。

### 3.17 2Real 单次规划抓取闭环（2026-08-07）

本轮只验证最小真机抓取闭环：

```text
Orbbec RGB-D
  -> 固定类别 YOLO（jpgCat）
  -> MobileSAM 原始 mask
  -> mask + aligned depth + CameraInfo
  -> /target/cloud（camera_color_optical_frame）
  -> AnyGrasp top_k=45
  -> 真机外参 camera_color_optical_frame -> base
  -> pregrasp/final 完整四元数 IK + MuJoCo/真机 raw 关节限位筛选
  -> policy: OPEN -> PREGRASP -> FINAL -> CLOSE -> LIFT
```

本轮固定边界：

- `use_sim_camera_extrinsics=false`，使用
  `hardware/calibration/camera/real_camera_calib.json`。
- 目标类别默认 `jpgCat`，同类多实例选置信度最高的 bbox。
- 固定类别 YOLO 默认置信度门槛为 `0.01`（可用 `--conf` 修改），不再用 `0.25` 预先截断；同类保留框中仍选择最高分 bbox。
- AnyGrasp 只请求一次；不启用 replan。
- 真机 planner 将候选从相机光学系转换到 `base` 后，沿 base approach 应用 `-0.040 m` 深度补偿，再从补偿后的 final 后退 `0.070 m` 计算 pregrasp。补偿后的 pregrasp/final 必须同时位于 policy 工作空间，之后才进入 IK；不满足的候选会被跳过而非留到 policy 执行阶段失败。
- 不启用腕部 tracking，CLOSE/LIFT 期间也不做位置修正。
- 不启用 SDF-CBF-QP 避障。
- SAM 原始 mask 生成目标点云；5% 外扩 mask 不送入 AnyGrasp。
- pregrasp、final 和 lift 都使用同一个已验证 policy 和真机命令整形层。
- 默认夹爪打开目标 `+0.45 rad`，闭合目标 `-0.15 rad`，闭合时允许因物体阻挡而不到位。lift policy 保留闭合目标，不会将其替换为被物体阻挡后的实测位置。
- lift 默认沿 base `+Z` 移动 `0.05 m`。

#### 3.17.1 完整四元数 IK 筛选修正（2026-08-10）

此前 `MujocoCandidateIkFilter` 的姿态 IK 只比较夹爪 approach 轴。两个姿态即使
绕 approach 轴的 roll 相差很大，只要进刀方向一致，也可能被判定为 IK 可达。
这会出现以下不一致：

```text
候选筛选：approach error 接近 0 deg，认为可达
policy 执行：追踪完整 AnyGrasp 四元数，wrist_roll 大幅旋转
真机安全层：中间目标越过 wrist_roll raw 限位，拒绝命令并停止在 PREGRASP
```

现已将 IK 旋转残差改为完整四元数误差：

```text
q_error = q_target * conjugate(q_current)
rotation_error = shortest_rotation_vector(q_error)
```

求解器的三维旋转残差现在同时约束 roll、pitch 和 yaw；候选只有在位置误差不超过
`0.005 m`、完整姿态误差不超过 `3 deg`，并满足 MuJoCo 关节限位时才算 IK
可达。pregrasp 和 final 均执行相同检查，之后再经过真机标定映射对应的 raw
安全限位筛选。

四元数误差采用最短旋转路径，`q` 与 `-q` 被视为相同姿态，因此不会把同一姿态
误判为接近 360 度的旋转。候选排序仍依次考虑：是否可达、位置误差、完整姿态
误差、关节余量。

代码与测试位置：

```text
ros2/soarm100_vision/soarm100_vision/mujoco_ik_filter.py
ros2/soarm100_vision/test/test_core.py
```

离线验证结果：`q/-q` 等价检查通过、90 度 roll 可被完整识别、MuJoCo home
pose 的 pregrasp/final IK 均得到 `0 mm / 0 deg`，ROS2 包构建返回码为 0。

这一修正会使通过筛选的 AnyGrasp 候选数量减少，这是预期行为：以前仅进刀方向
正确但 roll 不可执行的候选现在会被提前剔除。后续真机日志应重点观察
`ik=...pre_err=.../...deg final_err=.../...deg`、候选剩余数量，以及是否仍出现
`wrist_roll stream target raw ... outside safe interval`。

新增文件：

```text
ros2/soarm100_vision/soarm100_vision/real_policy_grasp_backend_node.py
ros2/soarm100_vision/launch/real_single_grasp.launch.py
ros2/scripts/real/run_single_grasp_2real.sh
```

一键运行：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim

./ros2/scripts/real/run_single_grasp_2real.sh \
  --class jpgCat \
  --device 0 \
  --show-window on \
  --confirm RUN_SINGLE_GRASP
```

首次或修改 ROS2 代码后增加 `--build`。脚本启动前检查串口占用，依次启动 Orbbec、`vision_seg` 中的 YOLO+SAM、持久硬件控制器、AnyGrasp planner、真机 policy backend 和 orchestrator。成功、失败或 Ctrl+C 都会请求七轴断力并清理所有子进程。

发送抓取 action 前，脚本不仅检查 topic/service/action 名称，还会分别读取一帧 RGB、对齐深度和 color CameraInfo。任何一路只有 topic 名但没有实际消息时，都会在机械臂运动前停止。YOLO 与 SAM 在 `vision_seg` 中执行；AnyGrasp worker 由 planner 单次调用 `graspnet_gpu`，本阶段不会循环推理。

终端 action feedback 会依次显示 `SEGMENTING`、`PLANNING_GRASP`、`OPEN`、`MOVE_TO_PREGRASP`、`FINAL_APPROACH`、`CLOSE` 和 `LIFT`。某阶段不继续时，以最后一个 stage 和 reason 为准，并结合对应 JSON/JSONL 日志定位。

首次联调曾因命令行 `--device 0` 被 ROS2 推断成整数、而参数声明为字符串，导致分割节点启动失败并假性停在 `SEGMENTING`。脚本现将数字 GPU 编号规范化为字符串 `cuda:0`，监控视觉/core 子进程是否存活，并为 segmentation、planning、policy 三类 ROS future 增加显式超时；节点崩溃不会再被 Viewer 或 DDS 残留名称掩盖。

第二次联调暴露 ROS2 Humble action 回调并不运行在标准 `asyncio` event loop 中，不能用 `asyncio.sleep()` 轮询 rclpy Future。超时实现已改为直接 `await rclpy Future`，由独立定时器在超时点取消 Future；该修复不改变 YOLO、SAM 或 AnyGrasp 算法。

主要日志：

```text
log/runtime/hardware/real_grasp_orbbec.log
log/runtime/hardware/real_grasp_vision.log
log/runtime/hardware/real_grasp_controller.log
log/runtime/hardware/real_grasp_nodes.log
log/runtime/hardware/real_single_grasp/
log/runtime/ros2_vision/fixed_yolo_sam/segment_target_latest.json
```

安全终止规则：任一阶段无新鲜关节反馈、policy timeout、目标超工作空间、外参转换失败、IK 无解或串口驱动拒绝命令时，当次抓取立即失败，不会自动进入下一阶段或二次规划。

#### 3.17.2 障碍物选择模式与抓取目标视觉隔离（2026-08-22）

实机障碍点云新增两种可切换的选择模式，二者都继续经过工作空间裁剪、桌面
过滤、基于 encoder joint state + FK 的机械臂 capsule 自过滤、`wrist_jaw`
局部包络和点云 persistence：

```text
all-except-target：指定目标和机械臂自身不进入障碍点云，其余工作区物体均为障碍物
target-only：仅指定类别实例的 mask 内深度点进入障碍点云
```

视觉部分复用固定类别 YOLO + MobileSAM。YOLO 检测指定类别并选取最高置信度
实例，MobileSAM 根据 bbox 生成实例 mask；障碍节点在已对齐的深度图上应用该
mask，再将保留的深度点转换到 base frame。默认自动刷新频率为 `2 Hz`。

安全降级规则：

- `all-except-target` 中 mask 缺失或过期时，不再排除指定目标，退化为将全部
  有效场景点作为障碍物。
- `target-only` 中 mask 缺失、过期或尺寸与深度图不一致时，障碍节点停止更新
  点云；policy 随后通过 `OBSTACLE_CLOUD_STALE` 停止，不将“未检测到”解释为
  “场景没有障碍物”。
- 第一张有效 mask 到来时清空一次旧 persistence，避免模型预热期间积累的目标
  点形成短暂残影。
- 启动脚本必须收到第一张有效障碍 mask 后才允许 policy 开始运行。

抓取目标与指定障碍物使用完全独立的 ROS2 命名空间：

| 用途 | mask | 点云 | 分割服务 |
|---|---|---|---|
| 抓取目标 | `/target/mask` | `/target/cloud` | `/segment_target` |
| 指定障碍物 | `/obstacle/selected_mask` | `/obstacle/selected_cloud_camera` | `/obstacle/segment_selected` |

因此可以让抓取视觉指定 `jpgCat`，同时让障碍视觉指定 `tissue`，两个分割节点
不会覆盖彼此的 mask、点云、中心、状态或服务。障碍视觉的其他独立话题包括：

```text
/obstacle/selected_mask_expanded
/obstacle/selected_cloud_roi_camera
/obstacle/selected_center_camera
/obstacle/selected_segmentation_status
```

仅将 `tissue` 作为障碍物的 policy reach 测试命令：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim

./ros2/scripts/real/run_policy_reach.sh \
  --relative-delta 0,0,0 \
  --obstacle-cbf on \
  --obstacle-gui on \
  --obstacle-selection target-only \
  --obstacle-target-class tissue \
  --obstacle-target-conf 0.10 \
  --obstacle-mask-refresh-hz 2.0 \
  --joint-limit-cbf on \
  --hold-current-duration-s 30 \
  --confirm RUN_POLICY_REACH
```

排除 `jpgCat`、将其余场景点作为障碍物时，将参数改为：

```text
--obstacle-selection all-except-target --obstacle-target-class jpgCat
```

当前边界：视觉链路和障碍点云链路已经支持抓取目标/障碍物分别指定，但
`real_policy_grasp_backend_node.py` 当前仍明确拒绝 `avoidance=true`，所以完整的
`run_single_grasp_2real.sh` 抓取运动尚未接入该障碍 CBF。不能通过同时启动
`run_policy_reach.sh` 和抓取脚本规避这一限制，因为两个脚本会争用同一个真机
硬件控制器。下一阶段需要将障碍 CBF 约束接入抓取后端的 pregrasp、final 和
lift policy 执行链。

本轮修改位置：

```text
ros2/soarm100_vision/soarm100_vision/obstacle_cloud_node.py
ros2/soarm100_vision/soarm100_vision/target_segmenter_node.py
ros2/scripts/real/run_policy_reach.sh
```

验证结果：Python 与 Bash 语法检查通过，`soarm100_interfaces` 和
`soarm100_vision` 均完成 `colcon build`。当前 base 环境未安装 `pytest`，因此
本轮没有执行 pytest 测试。
