# 代码结构与 Sim2Real 说明

本文只描述需要理解和维护的主干代码。`build/`、`install/`、`log/`、
`ros2/build/`、`ros2/install/`、`ros2/log/`、`__pycache__/` 都是生成物，不能作为
源码入口阅读，也不应手工修改。

## 1. 项目不是两层，而是三层

```text
Isaac Lab / rl              PPO 训练、评估、workspace 数据
        |
        | best_agent.pt
        v
MuJoCo / mujoco             轻量推理、FK、TCP、几何与仿真验证
        |
        | 共享 observation、policy、FK 约定
        v
ROS2 / real hardware        RGB-D、分割、AnyGrasp、CBF、舵机控制和安全停止
```

这里的 `2real` 不是另一套 policy。它仍加载同一个 PPO checkpoint，并尽量复用
训练时的关节顺序、observation、action 和 MuJoCo FK；变化发生在状态来源、目标
来源、执行器、坐标变换和安全约束。

## 2. 顶层目录职责

| 目录 | 职责 | 是否主干 |
|---|---|---|
| `rl/` | Isaac Lab reach PPO 训练、采样、评估、checkpoint | 是 |
| `mujoco/` | checkpoint 轻量加载、MuJoCo runtime、CBF 与仿真工具 | 是 |
| `ros2/soarm100_vision/` | ROS2 视觉、规划、policy 后端、真机节点 | 是 |
| `ros2/scripts/real/` | 真机任务的一键入口和进程清理 | 是 |
| `hardware/` | 舵机映射、标定、安全姿态、底层诊断工具 | 是 |
| `models/vision/` | YOLO、MobileSAM 等视觉权重 | 运行资源 |
| `anygrasp_sdk/` | AnyGrasp 第三方 SDK | 第三方依赖 |
| `SO-ARM100/` | 机械结构、MJCF、STL/STEP 等模型资源 | 运行资源/上游仓库 |
| `third_party/` | Orbbec ROS 驱动等第三方代码 | 第三方依赖 |
| `YoloWork/` | 固定类别 YOLO 的原始训练/实验工程 | 辅助工程 |
| `log/runtime/` | 真机、视觉、标定和任务日志 | 运行产物 |
| `outputs/` | 图片和其他实验输出 | 运行产物 |

## 3. 建议阅读顺序

### 3.1 Policy 与训练

```text
rl/reach_env_cfg.py          训练任务配置、目标和 observation/action 约定
rl/reach_env.py              reach 环境逻辑
rl/train.py                  PPO 训练入口
rl/inference_runtime.py      Isaac 环境中的 checkpoint 推理栈
mujoco/policy.py             27 -> 7 PPO policy 的轻量 checkpoint 加载器
mujoco/runtime.py            MuJoCo 关节、TCP、observation 和动作执行约定
```

先理解 `mujoco/policy.py` 和 `mujoco/runtime.py`，再读 ROS2 policy 节点。真机节点
使用 MuJoCo 主要是为了复用 FK 和训练 observation，不是在后台运行物理仿真。

### 3.2 视觉与抓取

```text
target_segmenter_node.py       YOLO/颜色检测 + MobileSAM，生成目标 mask/点云
anygrasp_planner_node.py       调用 AnyGrasp，筛选抓取候选
mujoco_ik_filter.py            用完整位置和四元数检查 pregrasp/final 可达性
grasp_orchestrator_node.py     SEGMENT -> PLAN -> EXECUTE 状态机
mujoco_policy_backend_node.py  sim 中执行抓取
real_policy_grasp_backend_node.py 2real 中执行 OPEN/PREGRASP/FINAL/CLOSE/LIFT
```

### 3.3 真机 reach 与安全层

```text
policy_reach_node.py                    PPO 真机闭环 reach + CBF
control/policy_command_shaper.py        速度、加速度和跟踪误差整形
control/joint_limit_cbf.py              关节限位 CBF
hardware_joint_limit_filter.py          标定后的舵机 raw 安全限位
hardware_controller_node.py             ROS2 真机串口控制器
hardware/tools/run_hardware_controller.py 真实 Feetech 总线所有者
```

控制权必须保持单一：只能有一个 hardware controller 持有串口，不能同时启动
`run_policy_reach.sh` 和 `run_single_grasp_2real.sh`。

### 3.4 障碍感知与 CBF

```text
obstacle_cloud_node.py          深度 -> base 点云 -> 场景/自身过滤 -> obstacle cloud
sdf_cbf_core.py                 点云 persistence、自过滤和基础几何算法
obstacle_overlay_viewer_node.py 将最终 CBF 点云投影到 RGB GUI
mujoco/cbf.py                   policy reach 使用的 CBF-QP 数学实现
link_self_occupancy_collector_node.py 采集 link-relative 非刚性附件数据
hardware/tools/build_link_self_occupancy.py 构建附件 occupancy 模型
```

当前实际在线主链路仍是 FK capsule + `wrist_jaw` 局部 box；link occupancy 已有采集
与构建工具，但尚未成为默认在线过滤条件。

### 3.5 标定

```text
orbbec_eye_to_hand_calibrator_node.py   眼在手外标定
wrist_handeye_calibrator_node.py        眼在手上标定
wrist_handeye_pose_sequence_node.py     腕部标定姿态序列
hardware/calibration/camera/            相机内参和手眼外参结果
hardware/calibration/lerobot/           舵机标定
hardware/calibration/policy_joint_mapping.json policy rad <-> servo raw 映射
```

## 4. Sim 抓取数据流

ROS2 MuJoCo 仿真抓取主链可以概括为：

```text
MuJoCo camera
  -> RGB / depth / CameraInfo / robot segmentation
  -> target_segmenter_node
  -> /target/mask + /target/cloud
  -> anygrasp_planner_node
  -> grasp pose + pregrasp pose
  -> grasp_orchestrator_node
  -> mujoco_policy_backend_node
  -> PPO policy
  -> MuJoCo joint control
```

仿真能够直接得到：

- 完整、低噪声关节状态；
- 精确相机位姿；
- robot geom segmentation；
- 目标和障碍物 ground truth；
- 可重复的碰撞、接触和动力学；
- 无通信延迟的 action 执行。

因此 sim 中很多信息不是“识别出来的”，而是仿真器直接知道的。

## 5. 2real 抓取数据流

当前单次真机抓取入口是：

```text
ros2/scripts/real/run_single_grasp_2real.sh
```

其数据流为：

```text
Orbbec RGB-D
  -> fixed YOLO + MobileSAM
  -> /target/mask + /target/cloud
  -> AnyGrasp
  -> camera grasp pose
  -> 手眼外参转换到 base
  -> MuJoCo IK + 真机 raw limit 候选筛选
  -> grasp_orchestrator_node
  -> real_policy_grasp_backend_node
  -> PPO 输出 joint delta
  -> command shaper / joint-limit safety
  -> /hardware/joint_target
  -> hardware controller
  -> Feetech servo
  -> encoder /joint_states 反馈闭环
```

当前真机抓取固定为一次分割、一次 AnyGrasp 规划，不做 tracking 和 replan。
`real_policy_grasp_backend_node.py` 仍拒绝 `avoidance=true`，所以完整抓取的
PREGRASP、FINAL 和 LIFT 尚未接入障碍 CBF。

## 6. 真机 policy reach + 避障数据流

入口：

```text
ros2/scripts/real/run_policy_reach.sh
```

控制链：

```text
encoder /joint_states
  -> MuJoCo FK/observation（只计算，不推进仿真）
  -> PPO policy
  -> joint-limit CBF + obstacle CBF
  -> velocity/acceleration/tracking shaper
  -> hardware raw limit
  -> /hardware/joint_target
  -> servo
```

障碍链：

```text
Orbbec aligned depth
  -> camera-to-base 手眼外参
  -> workspace crop
  -> table filter
  -> encoder q + FK capsule/box self filter
  -> 可选目标 mask 选择
  -> voxel persistence
  -> /obstacle/cloud
  -> policy_reach_node obstacle CBF
```

障碍选择模式：

```text
all-except-target  指定目标和机器人自身之外的场景点都是障碍物
target-only        只有指定类别实例的 mask 深度点是障碍物
```

抓取目标和指定障碍物已经使用独立命名空间：

```text
抓取：/target/*，服务 /segment_target
障碍：/obstacle/selected_*，服务 /obstacle/segment_selected
```

## 7. Sim 与 2real 的本质区别

| 环节 | Sim | 2real |
|---|---|---|
| 关节状态 | 仿真 qpos，准确且同步 | encoder，有噪声、重力误差和通信延迟 |
| action | 直接写仿真控制量 | 经过限速、限加速度、tracking、raw limit 后发舵机 |
| FK | MuJoCo ground truth | 同一 MuJoCo 模型 + 实测 encoder q |
| 相机位姿 | MJCF 已知 | 手眼标定估计，误差直接影响点云和抓取位姿 |
| RGB-D | 可控、同步、完整 | 有噪声、空洞、帧暂停和 RGB/depth 对齐问题 |
| 自身 mask | geom ID 精确分割 | FK 简化 capsule/box 近似，线缆不在 URDF/MJCF 中 |
| 目标 | 可直接知道物体 | YOLO + SAM 检测与分割 |
| 障碍物 | body/geom ground truth | 深度点云过滤后的估计 |
| 碰撞 | MuJoCo contact 可直接查询 | 只能依赖感知、CBF、安全距离和人工急停 |
| 关节限位 | MJCF limit | MJCF policy range + 标定后的 servo raw limit 双重约束 |
| 时间 | 固定仿真步长 | ROS、相机、GPU、串口均可能抖动或超时 |
| 可重复性 | 高 | 受初始姿态、线缆、光照、负载和舵机自重影响 |

最重要的 sim-to-real gap 不是 policy 网络本身，而是：

1. `q` 是否和训练坐标定义一致；
2. camera point 是否被正确变换到 base；
3. 目标四元数是否真机可达；
4. 深度点是否正确区分 robot self 和 obstacle；
5. policy joint delta 是否经过真机可执行的动态与 raw limit 约束。

## 8. 哪些代码真正共用

以下约定应尽量保持 sim/real 一致：

- 7 个关节名称与顺序；
- 27 维 observation 和 7 维 action；
- PPO checkpoint 与网络加载；
- MuJoCo FK、TCP 和四元数约定；
- workspace 与目标位姿定义；
- CBF 数学和安全距离语义；
- AnyGrasp pose 到 pregrasp/final 的几何定义。

以下部分必须是 real 专用：

- camera intrinsics/extrinsics；
- encoder 与 policy rad 的映射；
- servo raw limit；
- 串口所有权、超时和 torque-off；
- RGB-D 同步、新鲜度与空洞处理；
- 机器人线缆和未建模附件处理。

## 9. 当前完成状态

| 能力 | Sim | 2real |
|---|---|---|
| PPO 6D reach | 已有 | 已有，仍需继续提高终点精度 |
| 关节限位保护 | 有 | 已接入 calibrated raw limit + joint-limit CBF |
| 静态障碍 CBF reach | 有 | 已接入，仍在处理 self cloud 误检 |
| 动态障碍 | 有实验基础 | 尚未作为当前真机主线 |
| YOLO + SAM 目标分割 | 有 | 已有固定类别模型 |
| AnyGrasp 单次规划 | 有 | 已有 |
| 单次抓取 policy 执行 | 有 | 已有 v1，tracking/replan/avoidance 关闭 |
| 抓取中 CBF 避障 | 有相关接口 | 未接入 real grasp backend |
| 抓取目标/障碍目标分离 | 可配置 | 视觉话题与服务已隔离 |
| 线缆概率 occupancy | 不需要 | 已采集/构建，未成为默认在线链路 |

## 10. 当前推荐主线

不要同时扩展动态避障、抓取 tracking、线缆 occupancy 和新视觉模型。推荐顺序：

1. 固定相机、静态彩色障碍物，验证 `/obstacle/cloud` 与真实物体一致；
2. 用 `policy_reach` 验证无障碍终点误差和单障碍绕行/拉开行为；
3. 将已经验证的 obstacle CBF 接入 `real_policy_grasp_backend_node.py`；
4. 分别验证 PREGRASP、FINAL、LIFT 三阶段的 CBF 可行性；
5. 再考虑动态障碍速度估计；
6. 最后决定是否启用 link-relative cable occupancy 或 LingBot 深度补洞。

## 11. 文件管理建议

- 阅读和修改源码只进入 `rl/`、`mujoco/`、`ros2/soarm100_vision/`、
  `ros2/scripts/real/`、`hardware/`。
- 不在 `build/`、`install/` 或 `__pycache__/` 中修改代码。
- `log/runtime/hardware/` 按日期保留关键失败案例，其余运行日志定期归档。
- 标定结果保留 `current` 文件和带日期备份，不覆盖唯一副本。
- `SO-ARM100/`、`anygrasp_sdk/`、`third_party/` 是嵌套/第三方仓库，主项目提交时
  不应把它们的内部生成文件混进来。
- 在代码结构稳定前不要物理移动主干文件；当前脚本和动态 import 对仓库路径有
  明确依赖。应先用本文和入口脚本建立导航，再分阶段消除路径耦合。
