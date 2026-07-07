# CBF 避障评测汇总

- 生成时间：2026-07-07T15:52:47
- Git commit：`f8374a7`
- Checkpoint：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt`
- MJCF：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- NPZ：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/workspace_cache/workspace_tcp_merged_test.npz`
- Episodes：256（seed=0）
- **场景**：固定细杆 `obstacle_rod` @ (0.15, 0.09, 0.17) m
- CBF：d_safe=0.02 γ=0.8 activate<0.04

## 总体对比（原有指标，保留）

| 指标 | 无 CBF | CBF v2.1 | Δ (CBF v2.1−base) |
|------|--------|--------|--------------|
| pos le 1cm | 75.0% | 66.4% | -8.6 pt |
| pos le 2cm | 82.8% | 73.8% | -9.0 pt |
| pos le 3cm | 85.2% | 76.2% | -9.0 pt |
| ori le 20deg | 72.7% | 67.2% | -5.5 pt |
| joint pos1cm ori20 | 65.6% | 57.8% | -7.8 pt |
| cbf safe rate | — | 50.8% | — |
| safe reach 2cm | — | 50.8% | — |
| safe reach 1cm ori20 | — | 44.9% | — |
| no contact rate | 68.4% | 86.3% | +18.0 pt |
| median best dist mm | 5.2mm | 6.6mm | +1.3 mm |
| p90 best dist mm | 70.9mm | 115.0mm | +44.1 mm |
| h min median mm | — | 0.8mm | — |

## 到达代价（同 idx 配对，原有）

- Δbest_dist 中位数：**+0.0 mm**
- Δbest_dist p75：**+16.5 mm**
- Δbest_dist p90：**+50.9 mm**
- 退化 >10 mm（Regress@10mm）：**28.1%**
- 退化 >20 mm（Regress@20mm）：**23.8%**

## P0 扩展：COR / 物理安全到达 / 严格成功

| 指标 | 无 CBF | CBF v2.1 | Δ |
|------|--------|--------|---|
| cor_episode | 31.6% | 13.7% | -18.0 pt |
| phys_reach_2cm | 68.4% | 71.9% | +3.5 pt |
| phys_reach_1cm_ori20 | 60.2% | 57.0% | -3.1 pt |
| success_strict_2cm | 68.4% | 71.9% | +3.5 pt |
| success_strict_1cm_ori20 | 60.2% | 57.0% | -3.1 pt |
| cor_step_mean | 27.1% | 5.1% | -22.1 pt |

> **COR_episode** = 至少一步碰杆的回合占比（= 1 − no_contact_rate）。 **PhysReach@2cm** = 无碰杆且 best_dist≤2cm。 **success_strict** 与 PhysReach 同义（碰杆即失败，对齐论文精神）。

## 条件概率（原有，保留）

> `no_contact` = 整局 `contact_steps==0`（任意一步未与杆发生物理接触）。

### 样本构成

- baseline 全程无碰杆：**175/256** (68.4%)
- baseline 有碰杆：**81/256** (31.6%)
- 全局无碰杆率提升：**+18.0 pt** (68.4% → 86.3%)

### 2×2：baseline 碰杆与否 × CBF 结果

| baseline | N | CBF 无碰杆 | CBF 仍碰杆 |
|----------|---|-----------|-----------|
| 有碰杆 | 81 | 58.0% (47 局) | 42.0% |
| 无碰杆 | 175 | 99.4% | 0.6% (1 局) |

### 关键条件指标

| 指标 | 全体 | baseline 有碰 | baseline 无碰 |
|------|------|-------------|-------------|
| CBF 消除碰杆 P(无碰\|base有碰) | — | **58.0%** | — |
| CBF 新引入碰杆 P(碰\|base无碰) | — | — | **0.6%** |
| CBF 安全率 P(h_min≥0) | 50.8% | 0.0% | 74.3% |
| SafeReach@2cm | 50.8% | 0.0% | 74.3% |
| PhysReach@2cm | 71.9% | 18.5% | 96.6% |

> **读表提示**：全局 +10 pt 无碰杆会被「本来就不会碰」的样本稀释；应优先看 `P(无碰|base有碰)` 与 hard 档分层。

### 条件概率 · 按难度分层

| 档位 | N | base有碰 | P(无碰\|base有碰) | P(碰\|base无碰) | CBF安全\|base有碰 |
|------|---|---------|-------------------|------------------|-------------------|
| hard | 77 | 61 | 60.7% | 0.0% | 0.0% |
| medium | 52 | 1 | 100.0% | 2.0% | 0.0% |
| easy | 127 | 19 | 47.4% | 0.0% | 0.0% |

## P1 扩展：CBF 诊断

- h<0 且无碰杆（包络偏瘦/滞后）：**35.5%**
- h≥0 但有碰杆（包络漏检）：**0.0%**
- CBF 激活步占比均值：**68.8%**
- CBF 修正步占比均值：**43.9%**

**worst_monitor 分布（CBF 局内累计）：**

- `ellbow->wrist_pitch`：206
- `gripper`：21
- `wrist_roll`：14
- `shoulder_pitch`：9
- `tcp`：6

## 按难度分层（原有 + P0）

| 档位 | N | SafeReach@2cm | PhysReach@2cm | pos≤2cm base | pos≤2cm CBF | COR base | COR CBF | h_min 中位 |
|------|---|---------------|---------------|-------------|-------------|----------|---------|-----------|
| hard | 77 | 0.0% | 36.4% | 61.0% | 40.3% | 79.2% | 31.2% | -5.3 mm |
| medium | 52 | 71.2% | 98.1% | 100.0% | 100.0% | 1.9% | 1.9% | 4.6 mm |
| easy | 127 | 73.2% | 82.7% | 89.0% | 83.5% | 15.0% | 7.9% | 18.1 mm |
