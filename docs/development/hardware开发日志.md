# SO-100 Plus 真机硬件开发日志

本文记录 7 舵机 SO-100 Plus 的 2Real 硬件接入进度。这里仅记录真机硬件、
LeRobot/Feetech、标定和后续 `ros2_control` 接入；MuJoCo 和视觉链路继续使用各自
目录中的开发日志。

## 2026-07-30：LeRobot 环境和七电机只读映射

### 1. 环境

- LeRobot 源码：`lerobot-main`
- LeRobot 版本：`0.6.1`
- Conda 环境：`lerobot`
- Python：`3.12`
- 安装方式：本地 editable 安装
- 硬件依赖：
  - `feetech-servo-sdk==1.0.0`
  - `pyserial==3.5`
  - `deepdiff==8.6.2`
- 真机串口：`/dev/ttyACM0`
- USB 设备：QinHeng Electronics USB Single Serial
- 串口用户组：`dialout`

LeRobot `0.6.1` 要求 Python 3.12，而 ROS2 Humble 使用 Python 3.10。当前方案是：

1. LeRobot 环境负责 Feetech 通信验证、设置工具和标定参考；
2. 正式运行时由 ROS2 Humble 下的 `ros2_control` hardware interface 驱动真机；
3. 不把 LeRobot Python 3.12 直接导入 ROS2 Humble Python 节点。

### 2. 只读诊断工具

新增：

```text
hardware/tools/read_feetech7.py
```

功能：

- 定义并 ping ID 1～7；
- 检查七个电机是否均为 STS3215；
- 读取原始 `Present_Position`；
- 读取 `Torque_Enable`；
- 可输出 JSONL 日志；
- 默认覆盖同名日志，只有 `--append` 才追加。

严格只读保证：

- `sync_read(..., normalize=False)`，未标定前不做归一化；
- 不调用 `SOFollower.connect()`；
- 不调用 `configure_motors()`；
- 不写 PID、Operating Mode、电机 ID、限位或 Goal Position；
- 退出时使用 `disconnect(disable_torque=False)`，避免 LeRobot 默认断开流程写
  `Torque_Enable=0`。

标准运行方式：

```bash
cd /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim
conda activate lerobot

python hardware/tools/read_feetech7.py \
  --port /dev/ttyACM0 \
  --samples 20 \
  --period 0.5 \
  --log log/runtime/hardware/feetech7_first_read.jsonl
```

### 3. 首次通信结果

日志：

```text
log/runtime/hardware/feetech7_first_read.jsonl
```

结果：

- ID 1～7 均在线；
- 七个电机均识别为 STS3215；
- 连续 20 次读取无通信错误；
- 所有电机 `Torque_Enable=0`；
- 静止时编码器读数稳定，无跳变。

首次原始编码器位置：

| 电机 | ID | 原始值 |
|---|---:|---:|
| `shoulder_pan` | 1 | 2068 |
| `shoulder_lift` | 2 | 949 |
| `elbow_flex` | 3 | 3012 |
| `wrist_flex` | 4 | 2602 |
| `wrist_yaw` | 5 | 2002 |
| `wrist_roll` | 6 | 2014 |
| `gripper` | 7 | 2036 |

这些数值只表示当时姿态下的原始编码器值，不是零位，也不是标定后的关节角。

### 4. 七轴物理映射结果

在 `Torque_Enable=0` 时逐个手动移动物理关节，并同时读取全部电机。最终确认：

| 真机物理关节 | 电机 ID | LeRobot 名称 | Policy/MuJoCo 名称 | 单轮主要跨度 |
|---|---:|---|---|---:|
| 底座水平旋转 | 1 | `shoulder_pan` | `shoulder_rotation_joint` | 511 |
| 肩部抬升 | 2 | `shoulder_lift` | `shoulder_pitch_joint` | 245 |
| 肘部弯曲 | 3 | `elbow_flex` | `ellbow_joint` | 406 |
| 腕部俯仰 | 4 | `wrist_flex` | `wrist_pitch_joint` | 327 |
| 腕部偏航 | 5 | `wrist_yaw` | `wrist_jaw_joint` | 929 |
| 腕部滚转 | 6 | `wrist_roll` | `wrist_roll_joint` | 268 |
| 夹爪开合 | 7 | `gripper` | `gripper_joint` | 362 |

结论：

```text
6 个机械臂关节 + 1 个夹爪 = 7 个舵机/7 维控制
```

七个物理关节和电机 ID 均已明确对应。定制部分也已确认：

```text
ID 5 = 新增有限位 wrist_yaw
ID 6 = 有线缆范围限制的 wrist_roll
ID 7 = gripper
```

### 5. 映射日志

```text
log/runtime/hardware/map_wrist_yaw.jsonl
log/runtime/hardware/map_wrist_roll.jsonl
log/runtime/hardware/map_gripper.jsonl
log/runtime/hardware/map_wrist_flex.jsonl
log/runtime/hardware/map_shoulder_lift.jsonl
log/runtime/hardware/map_shoulder_pan.jsonl
```

注意：

- `map_wrist_flex.jsonl` 产生于日志覆盖行为修复前，包含两轮共 120 行；
- 前 60 行是 `wrist_flex` 测试；
- 后 60 行实际是 `elbow_flex` 测试；
- 后续日志默认覆盖同名文件，避免多轮数据混合。

### 6. 当前已确认

- [x] LeRobot 0.6.1 和 Feetech 依赖可导入
- [x] `/dev/ttyACM0` 可读写
- [x] 用户具备 `dialout` 权限
- [x] ID 1～7 全部在线
- [x] 电机型号均为 STS3215
- [x] 七轴物理关节与电机 ID 一一对应
- [x] 只读扫描不写任何舵机寄存器
- [x] 静止读数稳定

### 7. 尚未确认

- [ ] 每个关节编码器增大对应的真实物理正方向
- [ ] 真机正方向与 MuJoCo/URDF 关节正方向的 `sign=+1/-1`
- [ ] 每个关节的机械安全最小值和最大值
- [ ] `wrist_roll` 在线缆约束下的安全有限范围
- [ ] 每个关节的零位和 homing offset
- [ ] 夹爪原始编码器值与开度百分比/仿真关节角的映射
- [ ] 真机限位与 MuJoCo 训练限位的交集
- [ ] 首次低速、限幅、单关节电动测试
- [ ] `ros2_control` hardware interface
- [ ] 真机 watchdog、急停和启动防跳变

### 8. 下一阶段：两阶段安全校准

不直接运行官方 6 电机 `so101_follower` 校准。计划建立独立的 7 电机
`so100_plus_follower`，并使用两阶段校准：

#### 阶段 A：只读采集

1. 力矩关闭并可靠支撑机械臂；
2. 引导用户将机械臂放到约定中位姿态；
3. 记录各轴中位原始编码器值；
4. 每次只移动一个关节；
5. 记录安全 `range_min/range_max`；
6. 为机械限位保留额外安全余量；
7. `wrist_roll` 使用线缆安全范围，不使用官方硬编码 `0～4095`；
8. 生成候选 calibration JSON 和可读报告，但不写舵机。

#### 阶段 B：人工确认后应用

1. 人工审核七轴 ID、方向、零位和安全范围；
2. 计算真机范围与 MuJoCo/URDF 范围的交集；
3. 只有显式 `--apply` 才允许写 homing offset 和位置限位；
4. 写入后重新只读验证；
5. 首次电动测试每次只控制一个关节；
6. 初始目标必须等于当前反馈，防止开启力矩时跳变；
7. 使用小角度、低速度和单周期增量限制；
8. 全程保留硬件日志和快速断电能力。

### 9. 安全约束

- 未完成校准前不得运行 policy；
- 未确认方向前不得同时驱动多关节；
- 不运行官方 6 电机 `lerobot-calibrate --robot.type=so101_follower`；
- 不运行 `lerobot-setup-motors`，现有 ID 已正确设置；
- `Torque_Enable=0` 时肩部和肘部可能因重力下落，必须支撑；
- 不允许 `wrist_roll` 拉紧相机线或舵机线；
- 不使用 `sudo python` 运行 Conda 环境内的硬件程序；
- 相机作为独立 ROS2 节点部署，不进入舵机总线控制周期。

## 2026-07-30：七轴硬件层基础补全

新增独立目录 `hardware/so100_plus/`，不修改 `lerobot-main`：

- `hardware/so100_plus/config.py`
  - 统一维护 ID 1～7 的电机映射；
  - 统一维护电机名到 policy/MuJoCo joint 名的映射；
  - 记录当前 MuJoCo 模型限位；
  - 提供 PID、夹爪保护和单步动作安全配置结构。
- `hardware/tools/read_feetech7.py`
  - 改为导入统一电机表，避免映射重复。
- `hardware/tools/snapshot_feetech7.py`
  - 严格只读保存七电机配置与状态寄存器快照。
- `hardware/tools/collect_feetech7_calibration.py`
  - 交互式采集七轴参考中心和有限安全范围；
  - `wrist_roll` 与其他关节一样采集真实范围，不再硬编码 `0～4095`；
  - 生成候选 JSON，不写舵机；
  - 候选默认 `approved_for_motion=false`。
- `docs/development/hardware工具说明.md`
  - 整理当前命令、人工步骤和坐标转换边界。

旧版 7 轴 `so_follower.py` 中以下内容被确认可沿用：

- 七电机 ID 与关节名称；
- Feetech STS3215 总线实现；
- LeRobot 的标准观测与动作接口思路；
- `max_relative_target` 安全限幅思路；
- 夹爪力矩与电流保护参数的初始值。

以下内容暂不沿用：

- 将 `wrist_roll` 排除行程标定；
- 将 `wrist_roll` 范围硬编码为 `0～4095`；
- 未经逐轴确认直接把硬件角度当 policy/MuJoCo 关节角；
- 连接时无条件写 PID 和其他配置；
- 未完成方向与零位校准前允许多轴动作。

### 首轮候选采集诊断

首轮 `so100_plus_candidate.json` 未批准：

- `elbow_flex`、`wrist_flex`、`gripper` 的参考点落到添加余量后的范围外；
- `shoulder_pan`、`shoulder_lift`、`elbow_flex` 和 `wrist_flex` 主要只采到
  参考点的一侧，不适合作为 LeRobot half-turn 参考；
- `wrist_roll` 的原始值跨过 `4095→0`，旧采集算法错误地产生
  `74～4054` 的近整圈范围。

采集器已改为计算相对 `center_raw` 的环形有符号位移，并要求每个关节在扣除
安全余量后仍覆盖参考点两侧。跨编码器零点的范围会明确记录
`crosses_encoder_wrap=true`，不会再按普通最小/最大原始值解释。

## 2026-07-30：LeRobot 官方 follower 最小七轴合并

将下载版 `/home/sophie/下载/so_follower.py` 的七电机映射合并至：

```text
lerobot-main/src/lerobot/robots/so_follower/so_follower.py
```

最终映射为：

```text
1 shoulder_pan
2 shoulder_lift
3 elbow_flex
4 wrist_flex
5 wrist_yaw
6 wrist_roll
7 gripper
```

未直接覆盖整个文件，因为 `lerobot-main` 当前版本已包含下载版没有的 RGB-D
相机支持和 PID 配置项。保留这些较新的功能，只合并七轴差异。

同时删除官方/下载版中对 `wrist_roll` 的无限旋转特殊处理：

- 不再跳过 `wrist_roll` 行程记录；
- 不再硬编码范围 `0～4095`；
- 七个电机全部进入 LeRobot `record_ranges_of_motion()`；
- 标定提示明确要求 `wrist_roll` 只走线缆安全有限范围。

### LeRobot 七轴标定结果

有效标定文件：

```text
hardware/calibration/lerobot/so100_plus_7dof.json
```

保存时间为 `2026-07-30 15:09:27 +08:00`。范围审核如下：

```text
shoulder_pan   1030～3038   约 176.5°
shoulder_lift   956～3354   约 210.8°
elbow_flex      775～2990   约 194.7°
wrist_flex     1047～3015   约 173.0°
wrist_yaw      1054～3051   约 175.5°
wrist_roll     1092～3277   约 192.0°
gripper        1973～3450   约 129.8° 编码器行程
```

`wrist_roll` 不再使用 `0～4095`，范围连续覆盖半圈参考值 `2047`：

```text
相对 2047：-955～+1230 counts
约等于：-83.9°～+108.1°
```

在人工操作未拉紧线缆的前提下，该组可作为首个可用标定。首次动作前仍需
读取电机寄存器，确认写入值与 JSON 一致，并进行单轴小角度测试。

### 单关节首次动作工具

新增：

```text
hardware/tools/test_single_joint.py
```

默认测试 `wrist_roll +1°` 后返回起点。工具要求显式确认短语，只使能选定
电机，使能前同步当前位置目标，限制测试幅度不超过 `2°`，并在启动位置距离
标定端点不足 100 counts 时拒绝执行。全过程写入 JSONL 遥测日志，退出时关闭
所选电机力矩。

`wrist_roll` 的 `+1°` 和 `+2°` 测试已成功，反馈分别产生约 `0.62°` 和
`1.49°` 的可测位移，温度稳定在 `36°C`，电流原始值不超过 1。单轴测试的
最大允许幅度因此从首次验证用的 `2°` 放宽到 `5°`，用于确认物理正方向；
端点余量、单轴使能、插值、自动返回和退出断力矩保护保持不变。

### 新增腕部两轴方向确认

统一观察视角：从机械臂底座沿前臂方向看向夹爪。

```text
wrist_roll / ID6 / LeRobot +5°：逆时针旋转
wrist_yaw  / ID5 / LeRobot +5°：夹爪向右偏
```

`wrist_yaw +5°` 测试数据：

```text
起点 raw=1939
目标 raw=1996
实际最高 raw=1990，位移约 4.5°
返程 raw=1947，残差约 0.7°
电流原始值 0～2
温度 35°C
电压约 12.5V
```

通信、单轴使能、正反目标和退出断力矩均正常。新增的 `wrist_yaw` 与
`wrist_roll` 已完成硬件方向确认；下一步是建立 LeRobot 标定角度到
MuJoCo/policy 七关节弧度的零位和符号映射。

### Policy home 对齐工具

新增：

```text
hardware/tools/show_mujoco_reference_pose.py
hardware/tools/capture_policy_home.py
```

前者在 `base` 环境固定显示 policy 训练使用的 MuJoCo home：

```text
(0, -pi/2, +pi/2, 0, 0, 0, 0)
```

也可让指定关节在 home 与正向偏移之间周期切换，用于比较 MuJoCo 正方向。
后者在 `lerobot` 环境严格只读采集手动对齐后的七轴 raw 和 LeRobot 标准值，
保存到 `hardware/calibration/policy_home_capture.json`。关节符号确认前，
输出保持 `approved=false`。

首次 policy home 采集发现自然且线缆放松的 `wrist_roll raw=960`，低于首次
标定下限 `1092`。因此首次行程采集漏掉了安全区域。新增
`recalibrate_wrist_roll_range.py`，只重新记录和写入 ID6 的有限范围，保留
其 homing offset、其余六轴标定和 PID。工具使用双重确认、端点余量、跨零
跨度拒绝和写后读回验证。

### 腕部新增轴到 policy 的符号与零位

修正腕部姿态后重新采集 policy home：

```text
wrist_yaw  LeRobot home=+0.835°
wrist_roll LeRobot home=-1.099°
```

同一观察视角下对比真机与 MuJoCo 正方向：

```text
wrist_yaw：真机 + 向右，MuJoCo + 向右，sign=+1
wrist_roll：真机 + 逆时针，MuJoCo + 顺时针，sign=-1
```

采用：

```text
policy_rad = sign * radians(lerobot_deg) + zero_offset_rad
```

得到：

```text
wrist_yaw  zero_offset_rad=-0.0145763762
wrist_roll zero_offset_rad=-0.0191794423
```

结果写入 `hardware/calibration/policy_joint_mapping.json`。旧关节方向尚未在
本轮验证，保持空值；夹爪仍需百分比到 policy 关节角的两点映射，因此整体
配置暂时 `approved_for_policy_control=false`。

### 单次温度读数异常处理

`wrist_flex +5°` 首次测试中，温度连续保持 `34°C` 后在约 50 ms 内单次读到
`80°C`，同时电流原始值仅为 4。该变化不符合真实热惯性，判断为串口单次
异常值。安全工具仍正确中止并在 `finally` 中关闭了 ID4 力矩。

温度保护调整为：

- 正常低温只读一次；
- 首次读数达到 `55°C` 时立即追加两次复读；
- 取三次中位数作为确认温度；
- 两次及以上仍高温才触发停机；
- 单次异常在日志中记录 `temperature_single_read_glitch=true`；
- 持续高温保护阈值仍保持 `55°C`。

### Wrist flex 到 policy 的映射

重跑 `wrist_flex +5°` 后温度稳定在 `33～35°C`，没有再次出现异常温度：

```text
起点 raw=2612
目标 raw=2669
实际最高 raw=2665，出程约 4.7°
返程 raw=2635，残差约 2.0°
电流原始值 0～5
负载原始值最高 100
```

方向对比：

```text
真机 wrist_flex +：向下
MuJoCo wrist_pitch +：向上
sign=-1
```

policy home 采集的 LeRobot 值为 `-0.263736°`，因此：

```text
zero_offset_rad=-0.0046030662
```

已写入 `hardware/calibration/policy_joint_mapping.json`。

### Shoulder pan 到 policy 的映射

方向对比：

```text
真机 shoulder_pan +：向右
MuJoCo shoulder_rotation +：向左
sign=-1
```

policy home 的 LeRobot 值为 `-1.230769°`，得到：

```text
zero_offset_rad=-0.0214809754
```

`shoulder_pan +5°` 动作数据：

```text
起点 raw=2024
目标 raw=2081
实际最高 raw=2071
返程 raw=2040，残差约 1.4°
电流原始值 0～2
温度 34～35°C
```

已更新 `hardware/calibration/policy_joint_mapping.json`。

### Elbow flex 到 policy 的映射

方向对比：

```text
真机 elbow_flex +：向下
MuJoCo ellbow +：向下
sign=+1
```

policy home 为 `+pi/2`，home 采集的 LeRobot 值为 `+15.252747°`，得到：

```text
zero_offset_rad=+1.3045856673
```

`elbow_flex +5°` 动作数据：

```text
起点 raw=2118
目标 raw=2175
实际最高 raw=2155，出程约 3.3°
返程 raw=2124，残差约 0.5°
电流原始值 0～4
温度主要为 34～35°C
```

该轴受重力负载影响，出程未完全达到 5°，但方向判断明确。映射文件已更新。

### Shoulder lift 到 policy 的映射

方向对比：

```text
真机 shoulder_lift +：向前旋转
MuJoCo shoulder_pitch +：向前旋转
sign=+1
```

policy home 为 `-pi/2`，home 采集的 LeRobot 值为 `-6.769231°`，得到：

```text
zero_offset_rad=-1.4526509620
```

`shoulder_lift +3°` 动作数据：

```text
起点 raw=1416
目标 raw=1450
实际最高 raw=1448，出程约 2.8°
返程 raw=1438，残差约 1.9°
电流原始值 0～5
温度 34～35°C
```

返程受手臂重力影响较明显，但方向和出程响应正常。六个旋转关节的符号与
policy home 偏置现已全部写入映射文件。

### Gripper 到 policy 的映射

方向对比：

```text
真机 LeRobot 百分比 +：张开
MuJoCo gripper_joint +：张开
sign=+1
```

使用 MuJoCo 关节全范围 `[-0.2, 2.0] rad` 与 LeRobot `[0, 100]%` 的跨度
确定比例，并以 policy home 采集 `11.3744076% -> 0 rad` 校正零位：

```text
scale_rad_per_percent=0.022
zero_offset_rad=-0.2502369668
q_policy=clip(0.022 * percent - 0.2502369668, -0.2, 2.0)
```

动作测试：

```text
起点 raw=2145
目标 raw=2202
实际最高 raw=2193
返程 raw=2154
电流原始值 0～1
温度 36～37°C
```

七轴方向与 home 偏置现在全部具备。映射配置标记为
`approved_for_read_only_joint_state=true`，可进入 ROS2 只读姿态镜像验证；
在镜像与 MuJoCo FK 对齐前仍保持 `approved_for_policy_control=false`。

### 真机到 MuJoCo 只读镜像验证

新增共享转换模块和两个分环境进程：

```text
hardware/so100_plus/joint_mapping.py
hardware/tools/stream_policy_joint_udp.py
hardware/tools/show_policy_joint_mirror.py
```

`lerobot` 环境以 20 Hz 读取 Feetech 七轴，经
`policy_joint_mapping.json` 转换后发送到本机 UDP；启动时若任一电机
`Torque_Enable != 0` 则拒绝运行。`base` 环境接收数据并只更新 MuJoCo
`qpos`/GUI，不执行 `mj_step`，也不存在返回真机的控制通道。该阶段用于逐轴
观察方向、零位和夹爪开度是否一致。

### ROS2 只读关节状态链路

完成七轴 MuJoCo 镜像验证后，新增正式 ROS2 观测链路：

```text
Feetech 7-axis feedback (lerobot Python 3.12)
  -> calibrated policy radians
  -> localhost UDP schema v1
  -> hardware_joint_state_node (ROS2 Humble Python 3.10)
  -> /joint_states
  -> robot_state_publisher / TF / RViz
```

新增文件：

```text
ros2/soarm100_vision/soarm100_vision/hardware_joint_bridge.py
ros2/soarm100_vision/soarm100_vision/hardware_joint_state_node.py
ros2/soarm100_vision/launch/hardware_state.launch.py
ros2/run_hardware_state.sh
```

节点严格检查 schema、来源、sequence、七轴集合及有限数值。数据超过
0.5 秒未更新时发布 `/hardware/joint_state_stale=true`，并每 3 秒输出
sequence、数据年龄、丢包和非法包统计。

本阶段仍是单向只读链路：

```text
approved_for_read_only_joint_state=true
approved_for_policy_control=false
```

未创建电机 command topic，硬件读取器发现任一 `Torque_Enable != 0` 时
拒绝运行。

### ROS2 受限单关节控制服务

在只读关节映射验证通过后，新增第一阶段真机写入接口：

```text
/hardware/move_single_joint
soarm100_interfaces/srv/MoveSingleJoint
```

它不是连续 policy 控制器，只允许一次小幅相对动作并自动返回。ROS2 层把
幅度限制为 `±2°`，要求明确确认短语，并拒绝并发请求。执行端复用已完成真机
验证的 `hardware/tools/test_single_joint.py`，因此保留以下硬件保护：

```text
七轴初始 Torque_Enable 必须全部为 0
只使能选中的一个关节
使能前 Goal_Position=Present_Position
标定范围端点保留 100 counts
20 Hz 插值运动
55°C 温度保护
所有退出路径关闭所选关节力矩
```

ROS2 服务超时时会向完整 conda/Python 进程组发送 `SIGTERM`，底层将其转换
为 `KeyboardInterrupt` 并进入
`finally` 断力矩；若三秒后仍未退出才强制终止。服务与只读 stream 都需要
独占 `/dev/ttyACM0`，因此当前不能同时运行。

首次 ROS2 动作测试发现只读 stream 未停止，两个进程同时访问
`/dev/ttyACM0`。动作在 `wrist_roll` 出程早期因串口冲突中止，断力矩写入
也被冲突阻断。日志显示温度 36°C、电流 0，未出现机械过载。修复包括：

```text
服务执行前使用 fuser 检测串口占用，有占用则在使能力矩前拒绝请求
新增 hardware/tools/disable_all_torque.py
断力矩工具写入 Torque_Enable=0 后必须读回七轴全部为 0
```

残留进程进一步确认为后台 `stream_policy_joint_udp.py`。后台 shell 任务可能
继承忽略 `SIGINT` 的状态，因此原 cleanup 发送 `SIGINT` 不能可靠结束读取器。
读取器现显式注册 `SIGINT/SIGTERM`，统一设置停止标志并经过 `finally` 关闭
串口；`run_hardware_state.sh` 的 cleanup 改为发送 `SIGTERM` 后等待子进程。

### 单关节反馈闭环判定

首次完整执行虽返回 success，但日志显示 `+1°` 出程只达到约 `+0.70°`，
返程最终采样相对起点残留约 `+0.62°`。因此 success 判定从“命令流程完成”
收紧为反馈闭环：

```text
插值出程 -> 最多 1 s settle -> 连续 3 帧 |error| <= 3 counts
短暂停留
插值返程 -> 最多 1 s settle -> 连续 3 帧 |error| <= 3 counts
关闭所选关节力矩
读回七轴 Torque_Enable，要求全部为 0
```

任一 settle 超时或力矩读回非零均返回失败。settle 遥测和最终
`torque_off_verification` 都写入单次动作 JSONL。

第二次闭环测试中，出程收敛到 2 counts，返程在 6 counts（约 0.53°）
稳定不再变化，因此 3-count 判定返回失败；七轴力矩最终读回全部为 0。
这反映 STS3215 小幅动作的静态死区/齿隙，而非通信或方向错误。默认容差调整
为 8 counts（约 0.70°），仍要求连续三帧满足。温度还出现一个夹在连续
36°C 之间的孤立 50°C 读数，物理上不可能瞬时跳变，温度复读门槛从 55°C
提前到 45°C，安全触发阈值仍保持 55°C。

### 受限双关节同步控制

新增 `/hardware/move_joint_delta` 服务和
`hardware/tools/test_multi_joint_delta.py`。输入为 policy/MuJoCo 固定七轴
顺序的弧度增量，第一阶段最多允许两个非零轴，每轴 `|delta| <= 2°`。

硬件执行器把当前 LeRobot 反馈转换为 policy 弧度，叠加增量后同时检查
MuJoCo 关节限位，再逆变换为 Feetech raw 目标并检查标定范围 100-count
余量。被选中轴采用同一插值比例同步执行；出程和返程都要求所有活动轴连续
三帧落入 8-count 容差。任何异常均关闭全部七轴力矩并读回验证。

ROS2 层已用三个非零分量的请求验证安全门，返回：

```text
success=false
reason=exactly one or two non-zero deltas are required
```

该拒绝发生在串口和硬件子进程启动之前。

首次承重双轴请求被 policy 限位检查拒绝：当前
`shoulder_pitch_joint=-3.2432 rad` 已低于 MuJoCo 下限 `-3.1416 rad`，
而 `+1°` 后目标 `-3.2258 rad` 虽仍在范围外，但实际是在向合法区恢复。
限位规则因此细化为：

```text
当前在范围内：目标必须仍在范围内
当前低于下限：只允许 target > current 且不越过上限
当前高于上限：只允许 target < current 且不越过下限
```

恢复状态写入日志 `policy_limit_status`。继续远离合法区的动作仍会在使能力矩
前被拒绝。

随后 raw 余量检查发现 shoulder_lift 当前 `988`，标定硬下限 `956`，带
100-count 余量的安全下限为 `1056`。目标 `999` 虽向内，但自动返程会重新
回到硬限位附近，因此不能放宽原有往返测试。`MoveJointDelta` 新增
`keep_target`：

```text
false: 正常验证动作，收敛后自动返程
true: 仅限越界恢复，收敛后断力矩并保留目标位置
```

raw 越界恢复要求 start 位于标定硬范围内，且 target 严格朝
`[range_min+100, range_max-100]` 移动。该模式用于多个不超过 2° 的小步，
每一步都重新读取当前位置、检查方向并记录反馈。

### 自定义 hardware_safe 姿态

暂缓 PID 对照测试，优先定义真机安全初始/恢复姿态。新增
`hardware/tools/capture_safe_pose.py`，在七轴力矩全部关闭时严格只读采集：

```text
Feetech raw
LeRobot 标准值
policy/MuJoCo 七轴弧度
raw 100-count 安全余量检查
MuJoCo 关节限位检查
```

自动检查不能判断线缆张力、碰桌、自碰撞和断力矩机械稳定性，因此输出首先是
`hardware_safe_pose_candidate.json`，默认不批准用于动作。用户完成视觉和
机械检查后再标记为正式恢复姿态。

用户重新调整夹爪后，七轴 policy 限位和 raw 100-count 余量检查全部通过，
并人工确认姿态与线缆状态。候选已批准为：

```text
hardware/calibration/hardware_safe_pose.json
```

新增 `hardware/tools/move_to_named_pose.py` 和 ROS2 服务
`/hardware/move_named_pose`。脚本先验证姿态文件的三个批准标志，读取当前
policy 七轴位置，计算到 `hardware_safe` 的绝对姿态误差，再复用已有
`test_multi_joint_delta.py` 执行同步插值、反馈收敛、温度/限位检查及最终
七轴断力矩验证。

当前属于第一阶段回归门：最多两个活动关节，每轴误差不超过 `2°`。验证方法
是先让 `shoulder_rotation_joint` 与 `wrist_jaw_joint` 各偏移 `+1°`，
然后调用命名姿态服务返回。ROS2 接口和服务包已重新构建通过。

### 常驻上电七轴执行器

根据实际操作需求，结束必须手托机械臂的逐条断力矩验证流程。新增：

```text
hardware/tools/run_hardware_controller.py
ros2/soarm100_vision/soarm100_vision/hardware_controller_node.py
ros2/run_hardware_controller.sh
/hardware/move_joint_target
/hardware/set_torque
```

LeRobot 驱动进程长期独占串口，启动时先把目标寄存器设为七轴当前位置，再统一
上电保持。ROS2 代理通过 JSON Lines 与驱动通信，并由同一串口会话发布
`/joint_states`，避免只读反馈进程抢占串口。

当前绝对目标安全门为：policy/MuJoCo 限位、标定 raw 100-count 余量、
单轴单次最大 `20°`、最大 `20°/s`、温度中值复读后 `55°C` 保护，以及
连续三次 12-count 到位判定。完成目标后持续上电保持；显式断力矩、进程退出
或温度保护会关闭并读回验证七轴力矩。

首次安全姿态请求被普通目标的 `20°` 单次变化门拒绝；日志显示机械臂保持
误差为 0 counts、温度 36–38°C，但 shoulder lift 与批准姿态相差约 50°。
因此新增严格特例：仅当七轴目标与批准的 `hardware_safe_pose.json` 数值全部
匹配时，允许最大 120° 的恢复差值并把速度降至 `10°/s`。普通目标仍维持
20° 限幅。

安全姿态运动实际完成后，shoulder lift 在目标前固定停留 58 counts，约
5.1°；连续 2 秒没有继续收敛，其他六轴误差均为 2–9 counts，温度 36°C。
这不是 timeout，但仅凭该现象不能断定 P=16 不适配；负载限制、机械阻力、
目标换算和供电状态也可能产生相同结果。默认增益继续保持原始 P=16，不进行
未经测量支持的自动增益修改。运动/保持日志新增 `Present_Current` 和
`Present_Load`，后续先用反馈区分静差来源，再决定是否进行受控增益实验。

冷却后 P=16 复测中，shoulder lift 最终误差为 -60 counts（约 -5.3°），
current_raw=28、load_raw=252、温度 40°C；负载和电流均远低于保护值，固定
静差仍存在。新增显式启动参数 `--shoulder-lift-p`，默认16不变。本轮批准
仅用 `--shoulder-lift-p 18` 临时测试 shoulder lift，其他轴保持原增益，
退出时恢复并验证 P=16。

P=18 实验确认启动时从16写入18，退出时恢复为16，七轴力矩读回全部为0。
shoulder lift 的稳定误差仅从 P=16 的 -60 counts 改善至 -56 counts
（约改善0.35°）；current_raw=27、load_raw=263、温度42°C。改善幅度不足以
支持继续提高增益，默认继续使用 P=16。后续相机标定使用实时关节反馈和实际
稳定姿态，不把“命令目标与反馈完全一致”作为外参采样前提。

重新手动采集了更自然的 v2 home：shoulder pitch=-1.4480 rad，
elbow=+1.3683 rad，七轴 policy/raw 自动检查全部通过。用户确认旧版和新版
在断力矩后都会受重力下坠，因此明确 `hardware_safe` 的语义为“上电保持的
默认 home”，而非“断力矩重力稳定姿态”。旧目标备份为
`hardware_safe_pose_v1.json`，v2 已批准并替换默认
`hardware_safe_pose.json`；停机断力矩前仍必须支撑机械臂。
## 2026-08-04 真机腕部手眼标定工具

新手眼棋盘格实测单格边长为 `14.4 mm`，因此手眼 PnP 参数更新为
`square_size_m=0.0144`。这只影响棋盘到相机的平移尺度，不改变相机内参。

新增 ROS2 真机专用 `wrist_handeye_calibrator_node`，与 `mujoco/` 仿真标定
代码完全分离。节点只订阅腕部 RGB、CameraInfo 和 TF，不具备机械臂控制接口。

当前固定约定：棋盘格为 `9x6` 内角点、实测格长 `24.28 mm`；棋盘固定，腕部
相机随机械臂运动；刚性末端参考帧使用 `wrist_roll`，避免使用会随夹爪开合转动
的 `gripper` 链接。求解只使用 Tsai，即
`cv2.CALIB_HAND_EYE_TSAI`。

采集器支持棋盘角点预览、PnP 重投影误差门、相邻姿态重复门、图像时间戳 TF
查询、逐样本图片和矩阵落盘。求解后通过每帧反算的固定棋盘世界位姿离散度
验证外参，并输出 JSON 与 OpenCV YAML。

为提供正确的真机 TF，`hardware_controller.launch.py` 已加入
`robot_state_publisher`；控制器标定文件改为显式参数，当前默认使用新机械臂的
`hardware/calibration/lerobot/so100_plus_new_arm.json`。

入口：

```text
ros2/run_wrist_handeye.sh
ros2/soarm100_vision/soarm100_vision/wrist_handeye_calibrator_node.py
log/runtime/hardware/wrist_handeye/<timestamp>/
```

新增独立姿态序列执行器和固定随机种子候选文件：

```text
hardware/calibration/handeye/wrist_handeye_poses.json
ros2/run_wrist_handeye_poses.sh
```

初版围绕旧 `hardware_safe` 做小步随机游走，实际测试发现该姿态并不保证腕部
相机能看到棋盘，而且连续候选差异不明显。现改为 V2 相对姿态序列：用户先在
Viewer 中让当前姿态完整识别棋盘并固定棋盘，执行器读取启动时 `/joint_states`
作为中心；姿态采用明确的 wrist pitch/yaw/roll 正负激励、机械臂视点平移及组合
激励。重复中心姿态只负责安全过渡，不采样；有效候选会显示
`CAPTURE RECOMMENDED`。启动中心要求额外输入 `START`，每次运动仍要求 `MOVE`。
