# MuJoCo 推理与 CBF 避障评测日志

本文件记录 **MuJoCo 侧**（非 Isaac Lab）的推理与避障实验。策略默认 **C**：`rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt`。

---

## 实验范围说明（重要）

### 当前 CBF 批量评测：**固定杆场景**

| 项目 | 设定 |
|------|------|
| 场景文件 | `SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml` |
| 障碍物 | 竖直细杆 `obstacle_rod` |
| **杆位置（固定）** | **世界系 `(0.15, 0.09, 0.17)` m**，偏基座左侧 (+Y) |
| 杆几何 | 半径 12 mm，半长 150 mm（总高 30 cm） |
| 物理碰撞 | 开启（`contype/conaffinity=1`） |
| 机械臂起点 | 每局 **home** |
| 目标位姿 | 从 NPZ bank 抽样；**`--seed` 只影响目标 idx，不移动杆** |
| CBF 版本 | v2.1 Step A（v2 + **前臂胶囊** `ellbow→wrist_pitch`, r=4 cm, 9 点采样） |

> **未覆盖**：杆位置/朝向随机化、多杆、移动障碍。若要做杆位扫参，需改 MJCF 或增加运行时 body 位姿接口后再开实验 2。

### 与 `rl/log.md` 的关系

- `rl/log.md`：Isaac Lab 上 A/B/C 策略 **无避障** 的 reach 对比。
- **本文件**：MuJoCo 上 **有固定杆 + 可选 CBF** 的推理与避障评测。

---

## 批量评测脚本

```bash
cd soarm100sim

# 默认：256 局、seed=42、同一批 idx 跑无 CBF + CBF v2
python mujoco/eval_cbf.py --num-episodes 256 --seed 42

# 快速冒烟（2 局）
python mujoco/eval_cbf.py --num-episodes 2 --seed 42 --log-every 1
```

**输出目录**（默认 `logs/eval/cbf_fixed_rod/`）：

| 文件 | 内容 |
|------|------|
| `indices_seed42_n256.json` | 可复现的目标 idx 列表 |
| `episodes.csv` | 每局配对：baseline vs CBF |
| `summary.md` / `summary.json` | 总体、**条件概率**、hard/medium/easy 分层汇总 |

```bash
# 仅从已有 episodes.csv 重算 summary（改统计项后无需重跑仿真）
python mujoco/eval_cbf.py --summarize-only
```

### 成功指标（脚本内定义）

- **到达**：`best_dist` / `best_ori`（回合内最优，对齐 Isaac `ever_*`）
- **CBF 安全**：`h_min_ep ≥ 0`
- **物理**：与 `obstacle_rod` 接触的仿真步数（`contact_steps`）；**无碰杆** = 整局 `contact_steps==0`
- **联合 SafeReach@2cm**：`h_min_ep ≥ 0` 且 `best_dist ≤ 2 cm`
- **条件概率**（`summary.md` 第二节）：`P(CBF无碰|baseline有碰)`、`P(CBF新碰|baseline无碰)` 等；用于解读全局 `no_contact_rate` 被「本来不碰」样本稀释的问题

### 目标难度分层（启发式，固定杆下）

| 档位 | 规则 |
|------|------|
| hard | `target_y > 0.05` 且 `0.12 < target_x < 0.32`（易路径经杆侧） |
| medium | `|target_y| ≤ 0.05` |
| easy | 其余 |

---

## 交互式单局（GUI / verbose）

```bash
python mujoco/play.py --episodes 1 --speed 0.3 --seed 42
python mujoco/play.py --enable-cbf --verbose --cbf-log logs/mujoco_cbf_v2.jsonl \
  --episodes 1 --speed 0.3 --seed 42
```

---

## 评测记录

### 2026-07-07：固定杆 CBF v2 @ seed=42, N=256

- **时间**：2026-07-07T14:41:01
- **Git commit**：`c8b6f3d`
- **策略**：C（bank-start `best_agent.pt`）
- **场景**：`scene_plus.xml`，固定杆 `obstacle_rod` @ `(0.15, 0.09, 0.17)` m
- **NPZ**：`workspace_tcp_merged_test.npz`（4000 目标池）
- **CBF 参数**：d_safe=0.02 m，γ=0.8，activate<0.04 m
- **原始输出**：`logs/eval/cbf_fixed_rod/`（`indices_seed42_n256.json`、`episodes.csv`、`summary.json`）

#### 总体对比（256 局，home 起点，同一批 idx）

| 指标 | 无 CBF | CBF v2 | Δ (CBF−base) |
|------|--------|--------|--------------|
| pos ≤ 1 cm | 75.0% | 67.6% | −7.4 pt |
| pos ≤ 2 cm | 85.5% | 79.7% | −5.9 pt |
| pos ≤ 3 cm | 87.1% | 83.2% | −3.9 pt |
| ori ≤ 10° | 53.5% | 50.8% | −2.7 pt |
| ori ≤ 20° | 77.7% | 72.3% | −5.5 pt |
| ori ≤ 30° | 85.2% | 82.0% | −3.1 pt |
| **6D：pos≤1cm ∧ ori≤20°** | **66.0%** | **60.2%** | **−5.9 pt** |
| **CBF 安全率 (h_min≥0)** | — | **60.9%** | — |
| CBF 近似安全 (h≥−5mm) | — | 74.6% | — |
| **SafeReach@2cm** | — | **60.2%** | — |
| **SafeReach@1cm+20°** | — | **52.0%** | — |
| 物理无碰杆（全程 0 contact 步） | 70.3% | **80.1%** | **+9.8 pt** |
| 中位 best_dist | 5.5 mm | 6.3 mm | +0.8 mm |
| p90 best_dist | 41.1 mm | 64.0 mm | +22.9 mm |
| h_min 中位 (CBF) | — | 17.8 mm | — |
| h_min p10 (CBF) | — | −7.7 mm | — |

#### 到达代价（同 idx 配对）

| 指标 | 数值 |
|------|------|
| Δbest_dist 中位数 | +0.0 mm |
| Δbest_dist p90 | +26.9 mm |
| 退化 >10 mm 比例 | 18.0% |

#### 条件概率（解读全局 no_contact +9.8 pt）

> 定义见 `eval_cbf.py` → `summary.md` 第二节；以下摘自 `logs/eval/cbf_fixed_rod/summary.json`（2026-07-07 跑次）。

**样本构成**

| 子集 | N | 占比 |
|------|---|------|
| baseline 全程无碰杆 | 180 | 70.3% |
| baseline 有碰杆 | 76 | 29.7% |

**2×2：baseline 碰杆与否 × CBF 结果**

| baseline | N | CBF 无碰杆 | CBF 仍碰杆 |
|----------|---|-----------|-----------|
| 有碰杆 | 76 | **34.2%**（26 局消除） | 65.8% |
| 无碰杆 | 180 | 99.4% | **0.6%**（1 局新碰） |

**关键条件指标**

| 指标 | 全体 | baseline 有碰 | baseline 无碰 |
|------|------|-------------|-------------|
| **P(CBF 无碰 \| base 有碰)** | — | **34.2%** | — |
| **P(CBF 新碰 \| base 无碰)** | — | — | **0.6%** |
| CBF 安全率 P(h_min≥0) | 60.9% | **2.6%** | 85.6% |
| SafeReach@2cm | 60.2% | **0.0%** | 85.6% |

**按难度 · 有碰子集上的消除率**

| 档位 | base 有碰 N | P(无碰\|base 有碰) | P(新碰\|base 无碰) |
|------|------------|-------------------|-------------------|
| hard | 65 | **35.4%** | 0.0% |
| medium | 1 | 100% | 0.0% |
| easy | 10 | 20.0% | 5.0% |

**读表结论**：全局无碰杆 +9.8 pt 主要来自 76 局 risky 里救回 26 局；**约 2/3 真碰杆局仍碰**；60.9% CBF 安全率几乎全由「baseline 本就不碰」的 180 局撑起。

#### 按难度分层

| 档位 | N | SafeReach@2cm (CBF) | pos≤2cm 无CBF | pos≤2cm CBF | CBF安全率 | h_min 中位 (CBF) |
|------|---|---------------------|---------------|-------------|-----------|------------------|
| **hard** | 85 | **10.6%** | 67.1% | 50.6% | 11.8% | **−7.0 mm** |
| medium | 48 | 81.2% | 100.0% | 100.0% | 81.2% | 13.6 mm |
| easy | 123 | 86.2% | 92.7% | 91.9% | 87.0% | 27.9 mm |

#### 小结

1. **CBF 在「易/中等」目标上代价小**：easy 中位 best_dist 几乎不变，medium 到达无损；整体中位 Δbest_dist=0。
2. **难例是瓶颈**：hard 档 65/85 局 baseline 会碰杆，CBF 仅消除 **35%**；CBF 安全率在该档 **11.8%**（`h_min` 中位 −7 mm）。
3. **全局 +9.8 pt 无碰杆易误导**：70% 样本 baseline 本就不碰；真 risky 子集（76 局）消除碰杆 **34%**，SafeReach@2cm 为 **0%**。
4. **副作用小**：baseline 无碰的 180 局里，仅 **1 局** CBF 新引入碰杆（0.6%）。

**下一步（可选）**：全链 capsule + mesh 自动半径（Step B）；杆位扫参（实验 2）。

---

### 2026-07-07：固定杆 CBF v2.1 Step A @ seed=42, N=256

#### 本版更新说明（相对 v2 `c8b6f3d`）

| 项目 | v2 | **v2.1 Step A** |
|------|-----|-----------------|
| 前臂几何 | `wrist_pitch` **点球**监测，r=3.5 cm | 改为 **`ellbow→wrist_pitch` 胶囊**，r=**4.0 cm** |
| 约束计算 | 单 body 原点 + `obstacle_h_and_grad_p` | 线段 **9 点采样**取最紧 h；最近点处 **Jacobian 线性插值** |
| 监测点列表 | 含 `wrist_pitch` 点 | **移除** `wrist_pitch` 点，由胶囊覆盖前臂段 |
| QP / 滤波 / 杆 / 策略 | 不变 | 不变（d_safe=0.02，γ=0.8，activate<0.04） |
| 代码 | — | `mujoco/cbf.py`：`CapsuleMonitor`、`DEFAULT_CAPSULE_SPECS`、`resolve_monitors()` |
| 评测 idx | — | **复用** `logs/eval/cbf_fixed_rod/indices_seed42_n256.json`（与 v2 同批 256 目标） |

- **时间**：2026-07-07T15:08:41
- **Git commit**：`d2aabe1`
- **原始输出**：`logs/eval/cbf_capsule_stepA/`

#### v2 → v2.1 核心变化（同 idx、同 baseline）

| 指标 | CBF v2 | **CBF v2.1** | Δ |
|------|--------|--------------|---|
| 全局无碰杆率 | 80.1% | **85.9%** | **+5.8 pt** |
| **P(无碰 \| base 有碰)** | 34.2% | **52.6%** | **+18.4 pt** |
| P(新碰 \| base 无碰) | 0.6% | **0.0%** | −0.6 pt |
| pos ≤ 2 cm | 79.7% | 73.0% | −6.8 pt |
| 6D pos≤1cm∧ori≤20° | 60.2% | 57.4% | −2.8 pt |
| 中位 best_dist | 6.3 mm | 6.6 mm | +0.3 mm |
| p90 best_dist | 64.0 mm | **106.8 mm** | +42.8 mm |
| 退化 >10 mm 比例 | 18.0% | **28.5%** | +10.5 pt |
| CBF 安全率 (h≥0) | 60.9% | 54.7% | −6.2 pt |
| h_min 中位 | 17.8 mm | **5.1 mm** | −12.7 mm |
| hard：P(无碰\|base有碰) | 35.4% | **53.8%** | **+18.4 pt** |
| hard：pos≤2cm (CBF) | 50.6% | 34.1% | −16.5 pt |

#### 总体对比（256 局）

| 指标 | 无 CBF | CBF v2.1 | Δ (CBF−base) |
|------|--------|----------|--------------|
| pos ≤ 1 cm | 75.0% | 63.7% | −11.3 pt |
| pos ≤ 2 cm | 85.5% | 73.0% | −12.5 pt |
| pos ≤ 3 cm | 87.1% | 76.2% | −10.9 pt |
| ori ≤ 20° | 77.7% | 69.1% | −8.6 pt |
| **6D：pos≤1cm ∧ ori≤20°** | **66.0%** | **57.4%** | **−8.6 pt** |
| **CBF 安全率 (h_min≥0)** | — | **54.7%** | — |
| CBF 近似安全 (h≥−5mm) | — | **80.5%** | — |
| **SafeReach@2cm** | — | **54.7%** | — |
| **SafeReach@1cm+20°** | — | **46.9%** | — |
| 物理无碰杆 | 70.3% | **85.9%** | **+15.6 pt** |
| 中位 best_dist | 5.5 mm | 6.6 mm | +1.1 mm |
| p90 best_dist | 41.1 mm | 106.8 mm | +65.7 mm |
| h_min 中位 (CBF) | — | 5.1 mm | — |
| h_min p10 (CBF) | — | −6.2 mm | — |

#### 到达代价（同 idx 配对）

| 指标 | v2 | v2.1 |
|------|-----|------|
| Δbest_dist 中位数 | +0.0 mm | +0.0 mm |
| Δbest_dist p90 | +26.9 mm | **+60.1 mm** |
| 退化 >10 mm 比例 | 18.0% | **28.5%** |

#### 条件概率

**样本构成**（与 v2 相同：同一批 idx）

| 子集 | N | 占比 |
|------|---|------|
| baseline 全程无碰杆 | 180 | 70.3% |
| baseline 有碰杆 | 76 | 29.7% |

**2×2**

| baseline | N | CBF 无碰杆 | CBF 仍碰杆 |
|----------|---|-----------|-----------|
| 有碰杆 | 76 | **52.6%**（40 局） | 47.4% |
| 无碰杆 | 180 | **100.0%** | **0.0%**（0 局） |

**关键条件指标**

| 指标 | 全体 | baseline 有碰 | baseline 无碰 |
|------|------|-------------|-------------|
| **P(CBF 无碰 \| base 有碰)** | — | **52.6%** | — |
| **P(CBF 新碰 \| base 无碰)** | — | — | **0.0%** |
| CBF 安全率 P(h_min≥0) | 54.7% | **0.0%** | 77.8% |
| SafeReach@2cm | 54.7% | **0.0%** | 77.8% |

**按难度 · 消除碰杆**

| 档位 | base 有碰 N | P(无碰\|base 有碰) | v2 同指标 |
|------|------------|-------------------|-----------|
| **hard** | 65 | **53.8%** | 35.4% |
| medium | 1 | 100% | 100% |
| easy | 10 | 40.0% | 20.0% |

#### 按难度分层

| 档位 | N | SafeReach@2cm | pos≤2cm 无CBF | pos≤2cm CBF | 无碰杆率 CBF | h_min 中位 |
|------|---|---------------|---------------|-------------|-------------|-----------|
| **hard** | 85 | **2.4%** | 67.1% | **34.1%** | 64.7% | **−5.2 mm** |
| medium | 48 | 68.8% | 100.0% | 98.0% | **100%** | 5.1 mm |
| easy | 123 | 85.4% | 92.7% | 90.2% | 95.1% | 18.1 mm |

#### 小结

1. **前臂胶囊有效**：真碰杆子集消除率 **34% → 53%**（+40 局里多救 14 局）；hard 档 **35% → 54%**；**零副作用**（base 无碰 180 局无一例新碰）。
2. **更早介入**：h_min 中位从 +17.8 mm 降到 +5.1 mm，约束更常激活；全局无碰杆 **+15.6 pt**（v2 为 +9.8 pt）。
3. **到达代价加大**：pos≤2cm −12.5 pt（v2 仅 −5.9 pt）；p90 best_dist 与退化>10mm 明显变差，主要来自 hard 档绕杆更保守。
4. **包络仍偏瘦**：base 有碰子集 CBF 安全率仍为 **0%**（物理碰了但 h 仍可能<0）→ Step B（全链胶囊 / mesh 半径）仍有必要。
