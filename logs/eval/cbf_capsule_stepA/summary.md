# CBF 固定杆评测汇总

- 生成时间：2026-07-07T15:08:41
- Git commit：`d2aabe1`
- Checkpoint：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt`
- MJCF：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- NPZ：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/workspace_cache/workspace_tcp_merged_test.npz`
- Episodes：256（seed=42）
- **障碍物：固定细杆 `obstacle_rod` @ (0.15, 0.09, 0.17) m（见 mujoco/log.md）**
- CBF：d_safe=0.02 γ=0.8 activate<0.04

## 总体对比

| 指标 | 无 CBF | CBF v2 | Δ (CBF−base) |
|------|--------|--------|--------------|
| pos le 1cm | 75.0% | 63.7% | -11.3 pt |
| pos le 2cm | 85.5% | 73.0% | -12.5 pt |
| joint pos1cm ori20 | 66.0% | 57.4% | -8.6 pt |
| cbf safe rate | — | 54.7% | — |
| safe reach 2cm | — | 54.7% | — |
| safe reach 1cm ori20 | — | 46.9% | — |
| no contact rate | 70.3% | 85.9% | +15.6 pt |
| median best dist mm | 5.5mm | 6.6mm | +1.1 mm |
| h min median mm | — | 5.1mm | — |

## 到达代价（同 idx 配对）

- Δbest_dist 中位数：**+0.0 mm**
- Δbest_dist p90：**+60.1 mm**
- 退化 >10 mm 比例：**28.5%**

## 条件概率（解读全局 no_contact 用）

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

> **读表提示**：全局 +10 pt 无碰杆会被「本来就不会碰」的样本稀释；应优先看 `P(无碰|base有碰)` 与 hard 档分层。

### 条件概率 · 按难度分层

| 档位 | N | base有碰 | P(无碰\|base有碰) | P(碰\|base无碰) | CBF安全\|base有碰 |
|------|---|---------|-------------------|------------------|-------------------|
| hard | 85 | 65 | 53.8% | 0.0% | 0.0% |
| medium | 48 | 1 | 100.0% | 0.0% | 0.0% |
| easy | 123 | 10 | 40.0% | 0.0% | 0.0% |

## 按难度分层

| 档位 | N | SafeReach@2cm (CBF) | pos≤2cm base | pos≤2cm CBF | h_min 中位 (CBF) |
|------|---|---------------------|-------------|-------------|------------------|
| hard | 85 | 2.4% | 67.1% | 34.1% | -5.2 mm |
| medium | 48 | 68.8% | 100.0% | 97.9% | 5.1 mm |
| easy | 123 | 85.4% | 92.7% | 90.2% | 18.1 mm |
