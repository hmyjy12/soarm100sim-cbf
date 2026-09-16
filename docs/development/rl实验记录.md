# SO-100 Reach 推理对比日志

- 评测 episode 数（各权重）：256
- 并行 env：64，seed=42
- NPZ：test (`workspace_tcp_merged_test.npz`)
- **主表（推荐）**：回合内最优误差（episode-best，对齐训练 `ever_*`）

## 对比对象

| 代号 | 名称 | Checkpoint |
|------|------|------------|
| A | 2026-07-03_cfg1_agent_102400 | `rl/checkpoints/2026-07-03_18-11-38/26-07-03_18-11-38-258181_PPO/checkpoints/agent_102400.pt` |
| B | 2026-07-06_cfg2_pathA_best | `rl/checkpoints/2026-07-06_11-37-06_resume/PPO_resume/checkpoints/best_agent.pt` |
| C | 2026-07-06_bank_start_best | `rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt` |

### 背景简述

- **A（7.3）**：cfg1，home 起点 → 随机 NPZ 目标；`agent_102400.pt`
- **B**：从 A 续训 cfg2；`best_agent.pt`
- **C**：cfg1，bank 起点重训（TCP 最小距离 5 cm）；`2026-07-06_14-44-29/best_agent.pt`

---

## 一、历史 A vs B（home 起点，2026-07-06T13:40:02）

> JSON：`orient_bins_compare.json`。起点为 home。

### 姿态 / 位置 / 联合（episode-best）

| 指标 | A | B | Δ (B−A) |
|------|---|---|--------|
| ori ≤10° | 28.5% | 30.1% | +1.6 pt |
| ori≤20° | 58.2% | 57.0% | -1.2 pt |
| ori≤30° | 75.0% | 75.4% | +0.4 pt |
| pos≤1 cm | 91.8% | 88.7% | -3.1 pt |
| pos≤2 cm | 99.6% | 99.2% | -0.4 pt |
| pos≤1cm ∧ ori≤10° | 28.1% | 29.7% | +1.6 pt |

**小结**：B 相对 A 收益有限；home 任务上仍可主用 A。

---

## 二、追加 A vs C（bank 起点，2026-07-06T15:54:57）

> 协议：`reset_start_from_bank=True`（与 C 训练一致）。JSON：`orient_bins_bank_start.json`。

### 姿态（episode-best）

| 阈值 | A | C | Δ (C−A) |
|------|---|---|--------|
| ≤ 10° | 20.7% | 52.0% | +31.2 pt |
| ≤ 20° | 42.2% | 75.4% | +33.2 pt |
| ≤ 30° | 56.6% | 82.0% | +25.4 pt |
| 均值 / 中位数 / P90 | 35.5° / 24.8° / 84.4° | 17.1° / 9.2° / 44.0° | — |

### 位置（episode-best）

| 阈值 | A | C | Δ (C−A) |
|------|---|---|--------|
| ≤ 1 cm | 73.0% | 96.5% | +23.4 pt |
| ≤ 2 cm | 79.7% | 100.0% | +20.3 pt |
| ≤ 3 cm | 83.2% | 100.0% | +16.8 pt |
| 均值 / 中位数 / P90 | 2.37 / 0.42 / 6.46 cm | 0.42 / 0.39 / 0.75 cm | — |

### 联合（episode-best）

| 条件 | A | C | Δ |
|------|---|---|---|
| pos≤1cm ∧ ori≤10° | 19.1% | 50.8% | +31.6 pt |
| pos≤1cm ∧ ori≤20° | 36.7% | 73.0% | +36.3 pt |
| pos≤1cm ∧ ori≤30° | 49.2% | 79.7% | +30.5 pt |

### 附表：结束瞬间（摘要）

| 指标 | A | C | Δ |
|------|---|---|---|
| ori≤10° | 14.5% | 44.5% | +30.1 pt |
| pos≤1 cm | 67.6% | 89.8% | +22.3 pt |
| pos≤1cm ∧ ori≤10° | 14.5% | 43.4% | +28.9 pt |

**小结**：bank 起点下 C 全面优于 A；A 掉点说明旧策略对起点敏感。

---

## 三、追加：A vs C（home 起点，2026-07-06T16:05:38）

> 协议：`--home-start`（与第一节一致）。JSON：`rl/logs/eval/orient_bins_home_start.json`。

### 姿态（episode-best）

| 阈值 | A | C | Δ (C−A) |
|------|---|---|--------|
| ≤ 10° | 28.5% | 62.9% | +34.4 pt |
| ≤ 20° | 58.2% | 87.9% | +29.7 pt |
| ≤ 30° | 75.0% | 94.5% | +19.5 pt |
| 均值 / 中位数 / P90 | 21.8° / 16.9° / 48.7° | 10.5° / 7.1° / 22.0° | — |

### 位置（episode-best）

| 阈值 | A | C | Δ (C−A) |
|------|---|---|--------|
| ≤ 1 cm | 91.8% | 99.2% | +7.4 pt |
| ≤ 2 cm | 99.6% | 100.0% | +0.4 pt |
| ≤ 3 cm | 100.0% | 100.0% | +0.0 pt |
| 均值 / 中位数 / P90 | 0.41 / 0.30 / 0.96 cm | 0.39 / 0.37 / 0.62 cm | — |

### 联合（episode-best）

| 条件 | A | C | Δ |
|------|---|---|--------|
| pos≤1cm ∧ ori≤10° | 28.1% | 62.5% | +34.4 pt |
| pos≤1cm ∧ ori≤20° | 56.6% | 87.5% | +30.9 pt |
| pos≤1cm ∧ ori≤30° | 71.5% | 93.8% | +22.3 pt |

### 附表：结束瞬间（摘要）

| 指标 | A | C | Δ |
|------|---|---|--------|
| ori≤10° | 22.7% | 54.7% | +32.0 pt |
| pos≤1 cm | 87.1% | 94.1% | +7.0 pt |
| pos≤1cm ∧ ori≤10° | 22.3% | 53.9% | +31.6 pt |

### 结论（home 起点下的 C）

- home 协议下 **C 仍全面优于 A**，且姿态提升比位置更明显（ori≤10° +34.4 pt，pos≤1cm +7.4 pt）。
- 与第一节比：C 在 home 上的 ori≤10°（62.9%）也远高于 B（30.1%）。
- **综合**：无论 home 还是 bank 起点，当前都应 **主用 C**；B 可归档。

---

## 总览（episode-best 关键指标）

| 场景 | 权重 | ori≤10° | pos≤1cm | 联合≤10° |
|------|------|---------|---------|----------|
| home | A | 28.5% | 91.8% | 28.1% |
| home | B | 30.1% | 88.7% | 29.7% |
| home | C | **62.9%** | **99.2%** | **62.5%** |
| bank | A | 20.7% | 73.0% | 19.1% |
| bank | C | **52.0%** | **96.5%** | **50.8%** |

## 说明

- 误差在 `ReachEnv._get_dones` **reset 之前**快照。
- 历史 JSON：`rl/logs/eval/orient_bins_compare.json`（A vs B，home）
- bank JSON：`rl/logs/eval/orient_bins_bank_start.json`（A vs C，bank）
- home JSON：`rl/logs/eval/orient_bins_home_start.json`（A vs C，home）
- 复现：`rl/eval_orient_bins.py`（`--home-start` 固定 home 起点）
