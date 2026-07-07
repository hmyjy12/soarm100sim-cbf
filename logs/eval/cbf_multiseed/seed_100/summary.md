# CBF 避障评测汇总

- 生成时间：2026-07-07T16:02:24
- Git commit：`f8374a7`
- Checkpoint：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt`
- MJCF：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- NPZ：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/workspace_cache/workspace_tcp_merged_test.npz`
- Episodes：256（seed=100）
- **场景**：固定细杆 `obstacle_rod` @ (0.15, 0.09, 0.17) m
- CBF：d_safe=0.02 γ=0.8 activate<0.04

## 总体对比（原有指标，保留）

| 指标 | 无 CBF | CBF v2.1 | Δ (CBF v2.1−base) |
|------|--------|--------|--------------|
| pos le 1cm | 67.6% | 58.2% | -9.4 pt |
| pos le 2cm | 77.3% | 66.4% | -10.9 pt |
| pos le 3cm | 82.8% | 68.8% | -14.1 pt |
| ori le 20deg | 71.1% | 64.1% | -7.0 pt |
| joint pos1cm ori20 | 59.0% | 50.8% | -8.2 pt |
| cbf safe rate | — | 51.2% | — |
| safe reach 2cm | — | 51.2% | — |
| safe reach 1cm ori20 | — | 43.0% | — |
| no contact rate | 62.9% | 81.2% | +18.4 pt |
| median best dist mm | 6.1mm | 7.5mm | +1.5 mm |
| p90 best dist mm | 63.6mm | 114.8mm | +51.2 mm |
| h min median mm | — | 0.9mm | — |

## 到达代价（同 idx 配对，原有）

- Δbest_dist 中位数：**+0.0 mm**
- Δbest_dist p75：**+30.4 mm**
- Δbest_dist p90：**+65.6 mm**
- 退化 >10 mm（Regress@10mm）：**35.5%**
- 退化 >20 mm（Regress@20mm）：**30.9%**

## P0 扩展：COR / 物理安全到达 / 严格成功

| 指标 | 无 CBF | CBF v2.1 | Δ |
|------|--------|--------|---|
| cor_episode | 37.1% | 18.8% | -18.4 pt |
| phys_reach_2cm | 62.9% | 65.2% | +2.3 pt |
| phys_reach_1cm_ori20 | 52.3% | 49.6% | -2.7 pt |
| success_strict_2cm | 62.9% | 65.2% | +2.3 pt |
| success_strict_1cm_ori20 | 52.3% | 49.6% | -2.7 pt |
| cor_step_mean | 32.3% | 8.1% | -24.2 pt |

> **COR_episode** = 至少一步碰杆的回合占比（= 1 − no_contact_rate）。 **PhysReach@2cm** = 无碰杆且 best_dist≤2cm。 **success_strict** 与 PhysReach 同义（碰杆即失败，对齐论文精神）。

## 条件概率（原有，保留）

> `no_contact` = 整局 `contact_steps==0`（任意一步未与杆发生物理接触）。

### 样本构成

- baseline 全程无碰杆：**161/256** (62.9%)
- baseline 有碰杆：**95/256** (37.1%)
- 全局无碰杆率提升：**+18.4 pt** (62.9% → 81.2%)

### 2×2：baseline 碰杆与否 × CBF 结果

| baseline | N | CBF 无碰杆 | CBF 仍碰杆 |
|----------|---|-----------|-----------|
| 有碰杆 | 95 | 49.5% (47 局) | 50.5% |
| 无碰杆 | 161 | 100.0% | 0.0% (0 局) |

### 关键条件指标

| 指标 | 全体 | baseline 有碰 | baseline 无碰 |
|------|------|-------------|-------------|
| CBF 消除碰杆 P(无碰\|base有碰) | — | **49.5%** | — |
| CBF 新引入碰杆 P(碰\|base无碰) | — | — | **0.0%** |
| CBF 安全率 P(h_min≥0) | 51.2% | 0.0% | 81.4% |
| SafeReach@2cm | 51.2% | 0.0% | 81.4% |
| PhysReach@2cm | 65.2% | 8.4% | 98.8% |

> **读表提示**：全局 +10 pt 无碰杆会被「本来就不会碰」的样本稀释；应优先看 `P(无碰|base有碰)` 与 hard 档分层。

### 条件概率 · 按难度分层

| 档位 | N | base有碰 | P(无碰\|base有碰) | P(碰\|base无碰) | CBF安全\|base有碰 |
|------|---|---------|-------------------|------------------|-------------------|
| hard | 94 | 74 | 48.6% | 0.0% | 0.0% |
| medium | 32 | 1 | 100.0% | 0.0% | 0.0% |
| easy | 130 | 20 | 50.0% | 0.0% | 0.0% |

## P1 扩展：CBF 诊断

- h<0 且无碰杆（包络偏瘦/滞后）：**30.1%**
- h≥0 但有碰杆（包络漏检）：**0.0%**
- CBF 激活步占比均值：**66.5%**
- CBF 修正步占比均值：**47.0%**

**worst_monitor 分布（CBF 局内累计）：**

- `ellbow->wrist_pitch`：203
- `gripper`：26
- `wrist_roll`：15
- `tcp`：7
- `shoulder_pitch`：5

## 按难度分层（原有 + P0）

| 档位 | N | SafeReach@2cm | PhysReach@2cm | pos≤2cm base | pos≤2cm CBF | COR base | COR CBF | h_min 中位 |
|------|---|---------------|---------------|-------------|-------------|----------|---------|-----------|
| hard | 94 | 1.1% | 24.5% | 52.1% | 25.5% | 78.7% | 40.4% | -5.2 mm |
| medium | 32 | 75.0% | 100.0% | 100.0% | 100.0% | 3.1% | 0.0% | 9.6 mm |
| easy | 130 | 81.5% | 86.2% | 90.0% | 87.7% | 15.4% | 7.7% | 18.1 mm |
