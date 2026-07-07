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
| CBF 版本 | v2（当前 q 评估、约束含 dq_nom、不可行投影、低通滤波） |

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
| `summary.md` / `summary.json` | 总体与 hard/medium/easy 分层汇总 |

### 成功指标（脚本内定义）

- **到达**：`best_dist` / `best_ori`（回合内最优，对齐 Isaac `ever_*`）
- **CBF 安全**：`h_min_ep ≥ 0`
- **物理**：与 `obstacle_rod` 接触的仿真步数（`contact_steps`）
- **联合 SafeReach@2cm**：`h_min_ep ≥ 0` 且 `best_dist ≤ 2 cm`

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

#### 按难度分层

| 档位 | N | SafeReach@2cm (CBF) | pos≤2cm 无CBF | pos≤2cm CBF | CBF安全率 | h_min 中位 (CBF) |
|------|---|---------------------|---------------|-------------|-----------|------------------|
| **hard** | 85 | **10.6%** | 67.1% | 50.6% | 11.8% | **−7.0 mm** |
| medium | 48 | 81.2% | 100.0% | 100.0% | 81.2% | 13.6 mm |
| easy | 123 | 86.2% | 92.7% | 91.9% | 87.0% | 27.9 mm |

#### 小结

1. **CBF 在「易/中等」目标上代价小**：easy 中位 best_dist 仅 +0.03 mm（5.3→5.3 mm），medium 到达几乎无损；整体中位 Δbest_dist=0，说明多数目标几乎不受影响。
2. **难例是瓶颈**：hard 档（85 局，路径经杆侧）CBF 安全率仅 11.8%，SafeReach@2cm 10.6%；无 CBF 时该档已有 76.5% 会发生碰杆接触，CBF 将无碰杆率提到 50.6%，但 CBF 包络仍常穿入（h_min 中位 −7 mm）。
3. **全局 trade-off**：用约 6 pt 的 pos≤2cm 成功率，换 +9.8 pt 的无碰杆率；p90 到达误差恶化明显（+22.9 mm），主要来自 hard 长尾。
4. **与 GUI 单局一致**：难例（如 idx=357）属于 hard 档典型——绕杆后到达变远，但比 v1 抖动/穿模观感好；批量结果说明 **v2 在 easy/medium 可放心开，hard 仍需监测加厚或路径规划**。

**下一步（可选）**：hard 档失败 idx 列表 GUI 回放；加大 `wrist_pitch` 监测半径或加连杆中点；杆位扫参（实验 2）。
