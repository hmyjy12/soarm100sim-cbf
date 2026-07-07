# CBF 避障评测汇总

- 生成时间：2026-07-07T15:48:01
- Git commit：`f8374a7`
- Checkpoint：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt`
- MJCF：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- NPZ：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/workspace_cache/workspace_tcp_merged_test.npz`
- Episodes：256（seed=42）
- **场景**：固定细杆 `obstacle_rod` @ (0.15, 0.09, 0.17) m
- CBF：d_safe=0.02 γ=0.8 activate<0.04

## 总体对比（原有指标，保留）

| 指标 | 无 CBF | CBF v2.1 | Δ (CBF v2.1−base) |
|------|--------|--------|--------------|
| pos le 1cm | 75.0% | 63.7% | -11.3 pt |
| pos le 2cm | 85.5% | 73.0% | -12.5 pt |
| pos le 3cm | 87.1% | 76.2% | -10.9 pt |
| ori le 20deg | 77.7% | 69.1% | -8.6 pt |
| joint pos1cm ori20 | 66.0% | 57.4% | -8.6 pt |
| cbf safe rate | — | 54.7% | — |
| safe reach 2cm | — | 54.7% | — |
| safe reach 1cm ori20 | — | 46.9% | — |
| no contact rate | 70.3% | 85.9% | +15.6 pt |
| median best dist mm | 5.5mm | 6.6mm | +1.1 mm |
| p90 best dist mm | 41.1mm | 106.8mm | +65.7 mm |
| h min median mm | — | 5.1mm | — |

## 到达代价（同 idx 配对，原有）

- Δbest_dist 中位数：**+0.0 mm**
- Δbest_dist p75：**+16.4 mm**
- Δbest_dist p90：**+60.1 mm**
- 退化 >10 mm（Regress@10mm）：**28.5%**
- 退化 >20 mm（Regress@20mm）：**24.2%**

## P0 扩展：COR / 物理安全到达 / 严格成功

| 指标 | 无 CBF | CBF v2.1 | Δ |
|------|--------|--------|---|
| cor_episode | 29.7% | 14.1% | -15.6 pt |
| phys_reach_2cm | 70.3% | 71.5% | +1.2 pt |
| phys_reach_1cm_ori20 | 59.4% | 56.6% | -2.7 pt |
| success_strict_2cm | 70.3% | 71.5% | +1.2 pt |
| success_strict_1cm_ori20 | 59.4% | 56.6% | -2.7 pt |
| cor_step_mean | 24.8% | 5.5% | -19.2 pt |

> **COR_episode** = 至少一步碰杆的回合占比（= 1 − no_contact_rate）。 **PhysReach@2cm** = 无碰杆且 best_dist≤2cm。 **success_strict** 与 PhysReach 同义（碰杆即失败，对齐论文精神）。

## 条件概率（原有，保留）

> `no_contact` = 整局 `contact_steps==0`（任意一步未与杆发生物理接触）。

### 样本构成

- baseline 全程无碰杆：**180/256** (70.3%)
- baseline 有碰杆：**76/256** (29.7%)
- 全局无碰杆率提升：**+15.6 pt** (70.3% → 85.9%)

### 2×2：baseline 碰杆与否 × CBF 结果

| baseline | N | CBF 无碰杆 | CBF 仍碰杆 |
|----------|---|-----------|-----------|
| 有碰杆 | 76 | 52.6% (40 局) | 47.4% |
| 无碰杆 | 180 | 100.0% | 0.0% (0 局) |

### 关键条件指标

| 指标 | 全体 | baseline 有碰 | baseline 无碰 |
|------|------|-------------|-------------|
| CBF 消除碰杆 P(无碰\|base有碰) | — | **52.6%** | — |
| CBF 新引入碰杆 P(碰\|base无碰) | — | — | **0.0%** |
| CBF 安全率 P(h_min≥0) | 54.7% | 0.0% | 77.8% |
| SafeReach@2cm | 54.7% | 0.0% | 77.8% |
| PhysReach@2cm | 71.5% | 10.5% | 97.2% |

> **读表提示**：全局 +10 pt 无碰杆会被「本来就不会碰」的样本稀释；应优先看 `P(无碰|base有碰)` 与 hard 档分层。

### 条件概率 · 按难度分层

| 档位 | N | base有碰 | P(无碰\|base有碰) | P(碰\|base无碰) | CBF安全\|base有碰 |
|------|---|---------|-------------------|------------------|-------------------|
| hard | 85 | 65 | 53.8% | 0.0% | 0.0% |
| medium | 48 | 1 | 100.0% | 0.0% | 0.0% |
| easy | 123 | 10 | 40.0% | 0.0% | 0.0% |

## P1 扩展：CBF 诊断

- h<0 且无碰杆（包络偏瘦/滞后）：**31.2%**
- h≥0 但有碰杆（包络漏检）：**0.0%**
- CBF 激活步占比均值：**64.9%**
- CBF 修正步占比均值：**42.2%**

**worst_monitor 分布（CBF 局内累计）：**

- `ellbow->wrist_pitch`：209
- `gripper`：23
- `wrist_roll`：13
- `shoulder_pitch`：8
- `tcp`：3

## 按难度分层（原有 + P0）

| 档位 | N | SafeReach@2cm | PhysReach@2cm | pos≤2cm base | pos≤2cm CBF | COR base | COR CBF | h_min 中位 |
|------|---|---------------|---------------|-------------|-------------|----------|---------|-----------|
| hard | 85 | 2.4% | 31.8% | 67.1% | 34.1% | 76.5% | 35.3% | -5.2 mm |
| medium | 48 | 68.8% | 97.9% | 100.0% | 97.9% | 2.1% | 0.0% | 5.1 mm |
| easy | 123 | 85.4% | 88.6% | 92.7% | 90.2% | 8.1% | 4.9% | 18.1 mm |
