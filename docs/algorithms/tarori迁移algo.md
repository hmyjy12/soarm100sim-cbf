# tar&ori Reach 算法迁移说明

> 本文档整理自 `~/isaac_lab/isaac_ws/rl_code/tar&ori` 项目中 **HX02 双臂 Reach** 任务的强化学习实现，供 `soarm100sim`（SO-100）后续开发与合并参考。  
> 源文件主路径：`reach_env.py`、`reach_env_cfg.py`、`train.py`；推理侧结构定义见 `ros2_ws/.../reach_runtime.py`。

---

## 1. 任务概述

| 项目 | 说明 |
|------|------|
| 任务 | 单目标 **Reach**：将当前工作臂 TCP 移动到目标 6D 位姿（位置 + 可选姿态） |
| 仿真 | Isaac Sim + Isaac Lab `DirectRLEnv` |
| 机器人 | HX02 人形双臂（每臂 7 关节 + Robotiq 2F-85 夹爪；**Reach 训练不控夹爪**） |
| 臂选择 | 每个 env 仅一侧工作：目标在基座局部坐标 **y ≥ 0 → 左臂**，**y < 0 → 右臂** |
| 目标采样 | 从 `workspace_tcp_merged_train.npz` 随机取 TCP 目标点（及可选 `tcp_quat_wxyz`） |
| 算法库 | [skrl](https://github.com/Toni-SM/skrl) PPO，经 `isaaclab_rl.skrl.SkrlVecEnvWrapper` 接入 |

**与 SO-100 的关系**：运动学、维度、工作空间、夹爪模型均不同；**HX02 checkpoint 不可直接加载**。可迁移的是任务范式、奖励结构、滤波与 PPO 超参思路。

---

## 2. 仿真与控制时序

| 参数 | 值 | 来源 |
|------|-----|------|
| 物理步长 `sim.dt` | `1/60` s（60 Hz） | `reach_env_cfg.py` |
| `decimation` | `2` | 每 2 个物理步执行一次 RL 控制 |
| 控制频率 | **30 Hz**（`dt_ctrl = sim.dt × decimation`） | |
| `episode_length_s` | `10.0` s | 每回合约 300 个控制步 |
| 执行器 | `ImplicitActuatorCfg` 位置伺服（stiffness/damping 分臂/躯干/夹爪配置） | `HX02_CFG` |

### 2.1 动作语义

- **动作维度**：`action_space = 14`（右臂 7 + 左臂 7，连续，范围 `[-1, 1]`）。
- **有效动作**：非工作侧 7 维在 `_pre_physics_step` 中 **置零**；物理上该侧关节 **锁回 default**。
- **关节目标**（工作侧）：

  ```
  q_target = clamp(q_current + action_scale × a_filtered, q_min, q_max)
  ```

  默认 `action_scale = 0.25`（弧度增量，每控制步）。

- **躯干/头**：`downbody`…`head_joint` 等固定为 default；`head_joint` 默认 `0.5` rad。

### 2.2 动作一阶低通滤波器

在将动作写入关节目标 **之前** 对 raw action 滤波（`_pre_physics_step`）：

```
a_raw = clamp(policy_output, -1, 1)   # 并已对工作侧 mask
beta = dt_ctrl / (tau + dt_ctrl)
a_filtered[k] = a_filtered[k-1] + beta × (a_raw[k] - a_filtered[k-1])
```

| 参数 | `reach_env_cfg` 默认 | `train.py` CLI 默认 |
|------|----------------------|---------------------|
| `enable_action_filter` | `True` | `True`（`--disable_action_filter` 可关） |
| `action_filter_tau` | `0.15` s | **`0.08` s**（`--action_filter_tau`） |

> 训练脚本会覆盖 cfg 的 tau；实际训练常用 **0.08 s**。`beta ≈ 0.21`（30 Hz 控制下）。

设计意图（cfg 注释）：抑制高频抖动；`rew_action_rate` 仅作轻量补充，主靠滤波器平滑。

---

## 3. 观测空间（28 维）

仅取 **当前工作臂** 的状态（左右臂通过 `torch.where` 选择），拼接到 `obs["policy"]`：

| 分量 | 维数 | 含义 |
|------|------|------|
| `joint_pos` | 7 | 工作臂关节角 |
| `joint_vel` | 7 | 工作臂关节速度 |
| `tcp_rel` | 3 | TCP 世界坐标 − 机器人 root 位置（基座系） |
| `target_rel` | 3 | 目标世界坐标 − root 位置 |
| `arm_side` | 1 | 左/中线 `+1`，右侧 `-1` |
| `pos_err` | 3 | `target_pos - tcp_pos`（世界系） |
| `quat_err` | 4 | `q_des ⊗ q_ee^{-1}`，归一化并统一到四元数半球 |

**TCP 定义**：

- body：`Rarm_link6` / `Larm_link6`
- `tcp = body_pos + R(body) × tcp_center_offset_local`，默认 offset `(0.16, 0, 0)` m

**目标姿态**（`orientation_desired_reference`）：

- 训练默认 `"dataset"`：与 npz 中 `tcp_quat_wxyz` 同索引配对
- 对齐模式 `orientation_align_mode = "full_quaternion"`（\|q·q_des\|）

---

## 4. 奖励函数

总奖励（每控制步）：

```
R = rew_dist + rew_success + rew_hold + rew_action_rate + rew_joint_vel + rew_contact + rew_orientation
```

以下公式中 `d = ‖tcp - target‖`，`dt = sim.dt × decimation`。

### 4.1 势能型距离奖励 `rew_dist`

```
rew_dist = rew_distance_scale × (d_prev - d)
```

- `rew_distance_scale = 2.0`
- 靠近目标为正，远离为负（potential-based shaping）

### 4.2 分级到达 + 成功奖励 `rew_success`

```
rew_level1 = one_level_reward_scale × 𝟙[d < one_level_threshold]
rew_level2 = two_level_reward_scale × max(0, two_level_threshold - d)
rew_success_bonus = rew_success_scale × 𝟙[in_success_region]
rew_success = rew_level1 + rew_level2 + rew_success_bonus
```

| 参数 | 值 |
|------|-----|
| `one_level_threshold` | 0.10 m |
| `two_level_threshold` | 0.05 m |
| `one_level_reward_scale` | 1.0 |
| `two_level_reward_scale` | 45.0 |
| `rew_success_scale` | 3.0 |

`in_success_region`：**位置成功区** ∧ **姿态成功区**（均带迟滞，见下）。

### 4.3 成功区判定（迟滞）

**位置成功**：

- 进入：`d < success_threshold`（0.01 m）
- 保持：`d < success_exit_threshold`（0.013 m）

**姿态成功**（`enable_orientation_constraint=True` 时）：

- 度量：`align_quat = |q_ee · q_des|`（full_quaternion）或前向轴 cos（forward_axis 模式）
- 进入：`d < orientation_success_enter_distance`（0.05 m）且 `align ≥ orientation_enter_dot_threshold`（0.9962，约 10°）
- 保持：`d < orientation_success_exit_distance`（0.055 m）且 `align ≥ orientation_exit_dot_threshold`（0.994）

### 4.4 停留奖励 `rew_hold`

```
rew_hold = 𝟙[in_success_region] × 𝟙[tcp_speed < success_still_speed_threshold] × hold_reward_per_sec × dt
```

| 参数 | 值 |
|------|-----|
| `success_still_speed_threshold` | 0.025 m/s |
| `hold_reward_per_sec` | 10.0 |

鼓励进圈后 **低速悬停**，减少边界抖动刷分。

### 4.5 姿态 shaping `rew_orientation`

仅在 **未进入组合成功区** 且距离门控内生效：

```
orient_w = clamp((d_out - d) / (d_out - d_in), 0, 1)   # d_in=0.03, d_out=0.20
rew_orientation = rew_orientation_scale × align_quat² × orient_w × 𝟙[¬in_success_region]
```

- `rew_orientation_scale = 2.0`
- 进入成功区后关闭，避免为姿态分在边界抖动

### 4.6 正则与避碰惩罚

| 项 | 公式 | 系数 |
|----|------|------|
| `rew_action_rate` | `scale × Σ(Δa_active²)`，仅工作侧 7 维 | `-0.003` |
| `rew_joint_vel` | `scale × Σ(q̇_active²)` | `-0.005` |
| `rew_contact` | `scale × Σ clamp(‖F_link‖ - contact_threshold, 0, contact_force_clip)` | `-0.3` |

接触传感器匹配工作侧 link（regex：`Rarm_link.*` / `Larm_link.*` 等）：

- `contact_threshold = 1.5` N
- `contact_force_clip = 3.0` N（单 link 超额上限）

> 当前 **无显式障碍物/动态避障奖励**；碰撞抑制主要靠接触力惩罚 + 场景几何。后续 SO-100 若加避障，可在此项扩展或增加距离场惩罚。

### 4.7 Episode 终止

- `terminated`：恒为 `False`（Reach 训练不因失败提前结束）
- `time_out`：`episode_length_s` 到达（抓取 demo 激活时会重置 episode 计数，与 Reach 训练默认无关）

---

## 5. PPO 算法配置（skrl）

训练入口：`tar&ori/train.py`

### 5.1 训练规模

| 项 | 默认 |
|----|------|
| `num_envs` | 512 |
| `max_iterations` | 500 |
| `ROLLOUTS` | 128 |
| `total_timesteps` | `max_iterations × ROLLOUTS`（传给 `SequentialTrainer`） |
| 随机种子 | CLI `--seed`，同时写入 env 与 agent |

### 5.2 网络结构

共享结构（policy / value 分离网络，`separate: False` 指不共享权重）：

| 头 | 类型 | 结构 |
|----|------|------|
| Policy | `GaussianMixin` | MLP `[256, 128, 64]` + ELU → 连续动作 |
| Value | `DeterministicMixin` | MLP `[256, 128, 64]` + ELU → 标量 V(s) |

Policy 噪声：

- `initial_log_std = 0.0`
- `clip_log_std = True`，`min_log_std = -20`，`max_log_std = 2`
- `clip_actions = False`（环境内 clamp ±1）

### 5.3 PPO 超参（训练）

| 参数 | 值 |
|------|-----|
| `learning_epochs` | 5 |
| `mini_batches` | 4 |
| `discount_factor` γ | 0.99 |
| `lambda` (GAE) | 0.95 |
| `learning_rate` | **1e-4** |
| LR 调度 | `KLAdaptiveLR`，`kl_threshold=0.01` |
| `ratio_clip` ε | 0.2 |
| `value_clip` | 0.2 |
| `clip_predicted_values` | True |
| `grad_norm_clip` | 1.0 |
| `entropy_loss_scale` | **0.0**（无熵 bonus） |
| `value_loss_scale` | 2.0 |
| **`rewards_shaper_scale`** | **0.05** |
| `time_limit_bootstrap` | True |
| 状态预处理 | `RunningStandardScaler` |
| 价值预处理 | `RunningStandardScaler` |
| Memory | `RandomMemory`，`memory_size=-1`（自动） |

### 5.4 推理加载（`reach_runtime.py`）

推理时 `build_skrl_agent_cfg()` 中 PPO 结构 **与训练一致**（网络层宽相同），但：

- `rollouts=24`，`rewards_shaper_scale=0.01`（仅构建 Runner 用，eval 不更新）
- `learning_rate=3e-4`（训练脚本为 1e-4）

加载 checkpoint 后 policy 为 **确定性或采样** 由推理节点控制（默认 eval 取 mean action）。

### 5.5 Checkpoint

- 目录：`tar&ori/checkpoints/<YYYY-MM-DD_HH-MM-SS>/`
- 格式：skrl `.pt`
- 续训：`python train.py --checkpoint <path>`

---

## 6. 训练数据流（无 ROS）

```
reset: 从 workspace_npz 随机索引 → target_pos (+ quat)
     → 按 target.y 选左/右臂
     → 可选关节噪声 reset_active_arm_joint_noise_rad（默认 0）

loop:  policy(obs_28) → act_14 → mask/filter → joint position target
     → Isaac 物理步进 → reward → PPO 更新
```

- `use_ros_external_target = False`（`train.py` 强制）
- 测试集：`workspace_npz_path_test`（`execute.py` / 推理）

---

## 7. 迁移到 SO-100（soarm100sim）时的差异清单

| 模块 | tar&ori (HX02) | SO-100 待办 |
|------|----------------|-------------|
| 机器人资产 | HX02 USD | `Simulation/SO100/so100.urdf` → **USD 转换** |
| 动作维 | 14（双臂） | **6**（单臂 5+1 或 5，夹爪是否纳入 policy 待定） |
| 观测维 | 28 | 需按单臂 TCP/关节重新定义 |
| 臂选择 | y 分半区双臂 | 单臂可删除 `arm_side` 逻辑 |
| 工作空间 npz | HX02 扫出 | **重新 workspace_scan** |
| TCP / 姿态参考 | link6 + offset 0.16 m | 按 SO-100 URDF 末端 link 重定 |
| 接触惩罚 | 双臂 link regex | 按 SO-100 mesh/link 重配 |
| 场景 | 办公桌 + office USD | 简化桌面；**避障**需新增障碍物体与奖励/约束 |
| PPO 配置 | 上表 | 可先复用，再按收敛情况调 `rewards_shaper_scale` / 网络宽度 |

### 7.1 避障扩展建议（尚未在 tar&ori 实现）

在保留 Reach 主奖励的前提下，可考虑：

1. **惩罚项**：障碍距离 < 安全半径时增加负奖励；或 SDF 惩罚。
2. **观测增广**：障碍相对位置/占用栅格/深度特征（若做视觉 policy）。
3. **终止/约束**：硬碰撞终止或 large negative spike（当前 tar&ori 无碰撞终止）。
4. **课程**：先无障 Reach，再逐步加障。

---

## 8. 关键源文件索引

| 文件 | 内容 |
|------|------|
| `tar&ori/train.py` | PPO 训练入口、agent_cfg、滤波 CLI |
| `tar&ori/reach_env_cfg.py` | 超参、奖励系数、滤波、场景、关节名 |
| `tar&ori/reach_env.py` | `_get_observations`、`_get_rewards`、`_pre_physics_step`、`_apply_action` |
| `tar&ori/zipr2r/execute.py` | 无 ROS 推理 / 可视化 |
| `tar&ori/ros2_ws/.../reach_runtime.py` | 推理 Runner 与 checkpoint 解析 |
| `tar&ori/ros2_ws/.../reach_inference_node.py` | Isaac + PPO + ROS2 闭环（含 grasp demo，非纯 Reach 训练） |

---

## 9. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-30 | 初版：从 tar&ori 当前默认配置整理，供 soarm100sim 合并开发 |
