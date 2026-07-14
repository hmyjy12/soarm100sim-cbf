# MuJoCo 推理与 CBF 避障评测日志

本文件记录 **MuJoCo 侧**（非 Isaac Lab）的推理与避障实验。策略默认 **C**：`rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt`。

---

## 实验范围说明（重要）

### 当前 CBF 批量评测：**固定杆场景**

| 项目 | 设定 |
|------|------|
| 场景文件 | `scene_plus.xml`（有杆）/ `scene_plus_norod.xml`（无杆对照） |
| 障碍物 | 竖直细杆 `obstacle_rod`（**底部 ball joint，可碰倒**；每局自动立起） |
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

### 视觉链路（sim2real 准备）

| 相机 | MJCF 名 | 挂载 | 用途 |
|------|---------|------|------|
| 固定场景深度 | `scene_depth` | 基座侧后方 `(0.05,-0.15,0.50)`，`targetbody`→`scene_cam_lookat` | 俯视工作区 |
| 腕部 RGB | `wrist_rgb` | `wrist_roll` 上与**定爪指尖**对齐（`TCP_FIXED_FINGER_TIP` + 6mm） | 近场、遮挡补检 |

```bash
python mujoco/vision_smoke.py
python mujoco/vision_smoke.py --steps 120 --frame-stride 20
# 实时看相机（本机 OpenCV 常无 GUI、未必装 matplotlib → 默认 auto 会落到写 PNG + 自动打开）：
python mujoco/play.py --show-cam --episodes 3 --speed 0.3
python mujoco/play.py --show-cam --cam-backend save --episodes 3 --speed 0.3
# 若已安装 matplotlib：--cam-backend mpl
python mujoco/vision_preview.py   # 只看相机，无 3D 窗口
```

输出：`logs/vision_smoke/`（RGB、深度可视化、可选回放帧）。

### 相机标定（世界系 ↔ 像素 / 深度）

| 相机 | 类型 | 存什么 | 每步怎么更新 |
|------|------|--------|--------------|
| `scene_depth` | **固定** | `T_base_cam` + 内参 K | 不变（或每步读 `data.cam_xpos/xmat` 作仿真 ground truth） |
| `wrist_rgb` | **随动** | 静态手眼 `T_wrist_roll_cam` + K | `T_world_cam(q) = T_world_wrist_roll(q) @ T_wrist_roll_cam` |

约定见 `mujoco/calib.py`（MuJoCo 光轴 **-Z**，深度为沿射线距离）。

```bash
# 导出仿真标定 JSON + 重投影/手眼不变性检查
python mujoco/calib_verify.py
python mujoco/calib_verify.py --out logs/calib/camera_calib.json --poses 32
python mujoco/calib_verify.py --annotate   # 本机 OpenGL：写 reproj_*.png
```

真机路径（后续）：
1. **固定深度**：棋盘格/Charuco → 一次 `T_base_cam` 写入 JSON。
2. **腕部 RGB**：眼在手外/眼在手上 → `T_wrist_roll_cam`；运行时由 `/joint_states` + FK 或 TF 更新 `T_world_wrist_roll`。
3. **勿**把腕部某一时刻的 `T_world_cam` 当常数（臂动就错）。

代码入口：`mujoco/calib.py`（`project_world` / `unproject_depth_to_world` / `export_sim_calibration`）。

**仿真棋盘格标定**（真机前验证 OpenCV 流程 + 与 GT 对比）：

```bash
pip install opencv-python   # 若未装
python mujoco/calib_chessboard_sim.py                      # 默认 --detect gt
python mujoco/calib_chessboard_sim.py --detect render      # OpenCV 从 RGB 角点（实验性）
python mujoco/calib_chessboard_sim.py --camera wrist_rgb --arm-poses 14
python mujoco/calib_chessboard_sim.py --camera both --noise-px 0.3
```

场景：`scene_calib_chess.xml`（无杆 + 可移动棋盘）；输出 `logs/calib/chess_sim/`（角点标注图 + `chess_calib_report.json`）。

---

## 批量评测脚本

```bash
cd soarm100sim

# 有杆：256 局、seed=42，无 CBF + CBF（同批 idx）
python mujoco/eval_cbf.py --num-episodes 256 --seed 42 \
  --cbf-label "CBF v2.1" \
  --out-dir logs/eval/cbf_capsule_stepA

# 复用同一批 idx（公平对比）
python mujoco/eval_cbf.py \
  --indices-file logs/eval/cbf_fixed_rod/indices_seed42_n256.json \
  --num-episodes 256 --out-dir logs/eval/cbf_capsule_stepA \
  --cbf-label "CBF v2.1"

# P0：无杆对照（Reach 上限 / obstacle tax）
python mujoco/eval_cbf.py --no-obstacle \
  --indices-file logs/eval/cbf_fixed_rod/indices_seed42_n256.json \
  --num-episodes 256 --out-dir logs/eval/norod_seed42

# P1：多 seed 稳健性（各 seed 独立抽样 idx → out-dir/seed_XX/）
python mujoco/eval_cbf.py --seeds 42,0,1,100 --num-episodes 256 \
  --out-dir logs/eval/cbf_multiseed --cbf-label "CBF v2.1"

# 可选：固定同一批 idx 跨 seed（仅复现校验，非稳健性）
python mujoco/eval_cbf.py --seeds 42,0,1,100 --num-episodes 256 \
  --indices-file logs/eval/cbf_fixed_rod/indices_seed42_n256.json \
  --out-dir logs/eval/cbf_multiseed_sameidx --cbf-label "CBF v2.1"

# 仅从 episodes.csv 重算 summary（升级指标后无需重跑仿真）
python mujoco/eval_cbf.py --summarize-only --out-dir logs/eval/cbf_capsule_stepA \
  --cbf-label "CBF v2.1"
```

**输出目录**（每次 `--out-dir` 指定）：

| 文件 | 内容 |
|------|------|
| `indices_seed*_n*.json` | 可复现的目标 idx 列表 |
| `episodes.csv` | 每局配对 + **P0/P1 扩展列** |
| `summary.md` / `summary.json` | **原有指标 + P0/P1 扩展 + 条件概率 + 分层** |
| `multi_seed_summary.json` / `.md` | 多 seed 关键指标 mean/std + 各 seed 明细 |

### 指标说明（原有 + P0/P1，summary 中均保留）

#### 原有（继续作为主参考）

| 指标 | 含义 |
|------|------|
| `pos≤1/2/3cm` | 回合内最优 TCP 距离（**不管是否碰杆**） |
| `ori≤10/20/30°` | 回合内最优姿态误差 |
| `6D` / `joint_pos1cm_ori20` | 位置+姿态联合 |
| `no_contact_rate` | 整局无物理碰杆 |
| `SafeReach@2cm` | `h_min≥0` 且 `pos≤2cm`（CBF 包络意义下安全到达） |
| `h_min_ep` | 一局内 CBF 屏障 h 的最小值 |
| `Δbest_dist` / **Regress@10mm** | 同 idx 配对；后者 = CBF 比无 CBF **差超过 10mm** 的局占比 |
| **条件概率** | `P(无碰\|base有碰)`、`P(新碰\|base无碰)` 等 |

#### P0 扩展（对齐论文 COR / 严格成功）

| 指标 | 含义 |
|------|------|
| **COR_episode** | 碰撞发生率 = `1 − no_contact_rate`（至少一步碰杆） |
| **COR_step_mean** | 每局「碰杆步数/总步数」的均值 |
| **PhysReach@2cm** | **无碰杆** 且 `best_dist≤2cm`（物理安全到达，**推荐主 KPI**） |
| **PhysReach@1cm+20°** | 无碰杆 + 6D 阈值 |
| **success_strict_*** | 与 PhysReach 相同（碰杆即失败，贴近 EmbodiSteer 表 COR↓ 精神） |

#### P1 扩展（CBF 诊断）

| 指标 | 含义 |
|------|------|
| `h<0` 且无碰杆 | 包络偏瘦或激活滞后 |
| `h≥0` 但有碰杆 | 包络漏检 |
| `cbf_active/corrected_ratio` | 激活/修正步占比 |
| `worst_monitor` 分布 | 哪段连杆最紧 |
| **Regress@20mm** | 退化 >20mm 占比 |

#### 分解指标（需三次跑、同 idx）

| 量 | 计算 |
|----|------|
| **Obstacle tax** | 有杆无 CBF 的 Reach@2cm − **无杆** Reach@2cm |
| **CBF overhead** | 有杆 CBF 的 Reach@2cm − 有杆无 CBF 的 Reach@2cm |

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

---

## 实验 4：多 seed 稳健性（CBF v2.1）

- **日期**：2026-07-07
- **命令**：`--seeds 42,0,1,100 --num-episodes 256`（**各 seed 独立抽样 idx**）
- **输出**：`logs/eval/cbf_multiseed/`（`seed_XX/` + `multi_seed_summary.md`）

### 跨 seed 汇总（mean ± std，N=4×256）

| 指标 | mean | std |
|------|------|-----|
| pos≤2cm (base) | 81.2% | 3.2% |
| COR (base) | 33.4% | 2.9% |
| pos≤2cm (CBF) | 70.5% | 3.1% |
| COR (CBF) | **15.8%** | 2.1% |
| PhysReach@2cm (CBF) | **69.1%** | 2.7% |
| 无碰杆 (CBF) | **84.2%** | 2.1% |
| P(无碰\|base有碰) | **53.1%** | 3.1% |
| P(新碰\|base无碰) | **0.1%** | 0.2% |
| Regress@10mm | 31.1% | 3.0% |

### 解读

1. **避障效果稳定**：COR 从 ~33% 降到 ~16%（约 −17 pt），跨 seed std 仅 2.1%；`P(新碰|base无碰)` 近乎 0。
2. **消除碰杆能力一致**：`P(无碰|base有碰)` 均值 **53%**，与 seed=42 单跑（52.6%）吻合，std 3.1%。
3. **到达代价稳定但明显**：pos≤2cm CBF 比 base 低约 **10.7 pt**（81.2%→70.5%）；PhysReach@2cm 略升 **+2.5 pt**（66.6%→69.1%），说明在「碰杆即失败」口径下 CBF 净效益为正。
4. **Regress@10mm ~31%**：约三成局 best_dist 退化 >1 cm，与单 seed 28.5% 同量级。

> 完整各 seed 明细见 [`logs/eval/cbf_multiseed/multi_seed_summary.md`](../logs/eval/cbf_multiseed/multi_seed_summary.md)。

---

## 实验 5：Challenge-set 上的 ideal pointcloud SDF + CBF-QP 验证

- **日期**：2026-07-13
- **目的**：避免随机 target 太容易导致评估失真。先用 **no-CBF baseline** 扫描 target bank，只保留 baseline 会接触 / 推倒障碍物的 idx，再在同一批 challenge idx 上比较：
  - `none`：不开避障；
  - `geom`：解析 MuJoCo geom 距离 + CBF-QP；
  - `ideal_sdf`：明确障碍物 geom → 表面点云 → `PointCloudSdfObstacle` → CBF-QP。
- **脚本**：`mujoco/eval_sdf_challenge.py`
- **注意**：`ideal_sdf` 只把 geom 用作干净障碍物点云来源；控制时走点云 SDF/KD-tree 距离查询，不走解析 box/cylinder 距离。视觉 `scene_depth` 链路未参与本实验。

### 5.1 固定细杆 challenge-set

- **场景**：`SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- **输出**：`logs/eval/sdf_challenge_rod/`
- **扫描**：`scan_count=512, seed=42`
- **challenge 集**：64 个 idx，全部满足 no-CBF baseline 与 `obstacle_rod` 发生接触。

| 方法 | N | contact rate ↓ | reach@2cm ↑ | mean best_dist ↓ | mean end_dist ↓ | mean h_min | mean max\|dq_cbf\| |
|------|---:|---------------:|------------:|-----------------:|----------------:|-----------:|------------------:|
| none | 64 | **100.0%** | **92.2%** | **8.4 mm** | **9.9 mm** | — | 0.000 |
| geom | 64 | 23.4% | 3.1% | 97.3 mm | 104.7 mm | −0.88 mm | 0.356 |
| ideal_sdf | 64 | 23.4% | 3.1% | 95.7 mm | 103.6 mm | −2.31 mm | 0.374 |

**配对观察**：

| geom 是否接触 | ideal_sdf 是否接触 | 数量 |
|---------------|--------------------|-----:|
| 否 | 否 | 49 |
| 是 | 是 | 15 |
| 是 | 否 | 0 |
| 否 | 是 | 0 |

**解读**：

1. `ideal_sdf` 与解析 `geom` 在细杆 challenge-set 上行为高度一致：contact rate 相同，配对接触结果完全一致。
2. `ideal_sdf` 的 mean best/end distance 略优，但 mean h_min 更负、max correction 略大，说明点云 SDF 有轻微距离误差 / 更激进的约束表现。
3. CBF 确实把 baseline 的 100% 接触降到 23.4%，但到达代价很大：reach@2cm 从 92.2% 降到 3.1%。这说明当前主要瓶颈不是 SDF 后端，而是 **CBF safety filter 缺少绕行/重规划能力**，在必须穿过障碍附近的目标上会牺牲到达。
4. 推荐可视化成功样本：`1198`, `2502`, `799`。其中 `1198`：none 接触 5 步，geom/ideal_sdf 均 0 接触，best_dist 约 10–11 mm。

### 5.2 长方体墙 challenge-set

- **场景**：`SO-ARM100/Simulation/SO100/mujoco/scene_plus_wall.xml`
- **障碍物**：将原细杆替换为长方体 box；geom 名仍为 `obstacle_rod` 以兼容现有 CBF 配置。
- **输出**：`logs/eval/sdf_challenge_wall/`
- **扫描**：`scan_count=512, seed=42`
- **challenge 集**：64 个 idx，全部满足 no-CBF baseline 与长方体墙发生接触。

| 方法 | N | contact rate ↓ | reach@2cm ↑ | mean best_dist ↓ | mean end_dist ↓ | mean h_min | mean max\|dq_cbf\| |
|------|---:|---------------:|------------:|-----------------:|----------------:|-----------:|------------------:|
| none | 64 | **100.0%** | **92.2%** | **8.8 mm** | **10.1 mm** | — | 0.000 |
| geom | 64 | 32.8% | 6.3% | 100.5 mm | 109.0 mm | −1.35 mm | 0.365 |
| ideal_sdf | 64 | **31.3%** | **7.8%** | **96.3 mm** | **103.5 mm** | −1.69 mm | 0.375 |

**配对观察**：

| geom 是否接触 | ideal_sdf 是否接触 | 数量 |
|---------------|--------------------|-----:|
| 否 | 否 | 43 |
| 是 | 是 | 20 |
| 是 | 否 | 1 |
| 否 | 是 | 0 |

**解读**：

1. 长方体墙比细杆更难：contact rate 从 rod 的 23.4% 升到约 31–33%；baseline 平均 contact steps 也更高。
2. `ideal_sdf` 在 wall 上略优于解析 `geom`：contact rate 31.3% vs 32.8%，reach@2cm 7.8% vs 6.3%，mean best/end distance 也略低。
3. 配对结果没有出现系统性的 “geom 成功但 SDF 失败”；反而有 1 个样本 `idx=1157` 是 ideal_sdf 0 接触、geom 仍接触 7 步。
4. 推荐可视化成功样本：
   - `2088`：none 接触 5 步；geom/ideal_sdf 均 0 接触；best_dist 约 2.9 mm。
   - `2746`：none 接触 39 步；geom/ideal_sdf 均 0 接触；best_dist 约 8.3–8.5 mm。
   - `1573`, `3925`：均为 baseline 接触、CBF 两后端无接触，且 best_dist < 2 cm 左右。
5. 推荐可视化失败样本：`2390`, `1788`, `1107`, `1089`。这些样本 ideal_sdf 仍有大量接触，通常表现为目标与障碍冲突强，policy 持续朝目标方向推，CBF 只能局部反推，无法主动生成绕行轨迹。

### 5.3 阶段性结论

1. **SDF 后端作为距离查询替代基本成立**：在细杆和长方体墙两个 challenge-set 上，`ideal_sdf` 与解析 `geom` 的表现接近；wall 场景中 `ideal_sdf` 还略优。
2. **先前 scene_depth SDF 失败不是 SDF+CBF-QP 本身失败**：问题来自把整张深度 ROI 当成障碍点云，导致机器人/背景点污染距离场。当前 `ideal_sdf` 使用明确障碍物点云后不再打废 policy。
3. **主要瓶颈转移到控制策略层**：当前 CBF-QP 是速度级 safety filter，能显著降低 contact，但在 challenge targets 上 reach@2cm 大幅下降。仅靠硬约束修正 nominal policy，缺少绕行、局部 waypoint 或切向引导时，很难兼顾高到达率和低接触率。
4. **下一步建议**：
   - 继续使用 challenge-set 评估，不再用随机容易目标做主要结论；
   - 对 CBF 参数做网格消融（`d_safe`, `gamma`, `activate_margin`, `cbf_filter_tau`）；
   - 引入 slack CBF 或分层优先级，降低不可达目标下的硬阻塞；
   - 加入切向绕行项 / 局部 waypoint，引导 policy 绕过障碍而不是持续正面顶住 CBF；
   - 后续视觉/open-vocab 阶段必须输出“障碍物点云”，不能直接使用整图 ROI 点云。

## 实验 6：视觉 `workspace_sdf` + soft-settle 状态机对比

### 6.1 实验设置

- **日期**：2026-07-14
- **场景**：`SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- **challenge idx**：复用 rod challenge-set 前 8 个 baseline 会碰撞目标：
  - `799, 2472, 2601, 582, 2988, 1788, 3919, 3767`
- **输出**：`logs/eval/state_softsettle_quick8/`
- **方法**：
  - `none`：不开 CBF/避障，完整跑 10s，用作 baseline 碰撞参考；
  - `ideal_sdf`：明确 obstacle geom 表面点云 SDF + CBF；
  - `workspace_sdf`：`scene_depth` 深度 + robot segmentation self-mask + workspace crop + voxel persistence SDF + CBF。
- **状态机**：
  - 仅对 `ideal_sdf` 和 `workspace_sdf` 启用；
  - `none` 不启用状态机，避免进圈提前停止而隐藏 baseline 碰撞；
  - `success_dist=0.04m`, `success_steps=5`, `settle_on_success=1.0s`；
  - `settle_mode=policy_soft_cbf`：SETTLE 阶段继续执行 policy，但 CBF 临时弱化为 `d_safe=0.005m`, `gamma=0.3`, `activate_margin=0.015m`。

命令：

```bash
MUJOCO_GL=egl python mujoco/eval_sdf_challenge.py \
  --indices-file logs/eval/sdf_challenge_rod/challenge_indices.json \
  --max-challenges 8 \
  --methods none ideal_sdf workspace_sdf \
  --settle-methods ideal_sdf workspace_sdf \
  --success-dist 0.04 \
  --success-steps 5 \
  --settle-on-success 1.0 \
  --settle-mode policy_soft_cbf \
  --stop-on-success \
  --use-sim-cam \
  --out-dir logs/eval/state_softsettle_quick8 \
  --log-every 1
```

### 6.2 汇总指标

| 方法 | N | contact rate ↓ | reach@2cm ↑ | success latch@4cm ↑ | mean best_dist ↓ | mean end_dist ↓ | mean h_min | mean max\|dq_cbf\| |
|------|---:|---------------:|------------:|--------------------:|-----------------:|----------------:|-----------:|------------------:|
| none | 8 | **100.0%** | **100.0%** | — | **5.6 mm** | **7.3 mm** | — | 0.000 |
| ideal_sdf + soft-settle | 8 | 37.5% | 12.5% | 25.0% | 75.8 mm | 76.4 mm | −0.47 mm | 0.346 |
| workspace_sdf + soft-settle | 8 | **0.0%** | 0.0% | 12.5% | 99.3 mm | 102.0 mm | −6.17 mm | 0.354 |

### 6.3 明细观察

| idx | none contact / best | ideal_sdf contact / best / success | workspace_sdf contact / best / success |
|-----|---------------------|------------------------------------|----------------------------------------|
| 799 | 3 / 5.6 mm | 0 / 16.8 mm / Y | 0 / 24.9 mm / Y |
| 2472 | 97 / 5.0 mm | 1 / 192.3 mm / n | 0 / 205.0 mm / n |
| 2601 | 43 / 5.9 mm | 3 / 88.1 mm / n | 0 / 117.8 mm / n |
| 582 | 17 / 3.3 mm | 0 / 50.0 mm / n | 0 / 70.1 mm / n |
| 2988 | 5 / 5.6 mm | 0 / 51.5 mm / n | 0 / 65.2 mm / n |
| 1788 | 85 / 4.7 mm | 64 / 36.6 mm / Y | 0 / 48.5 mm / n |
| 3919 | 177 / 10.2 mm | 0 / 122.7 mm / n | 0 / 180.8 mm / n |
| 3767 | 4 / 4.8 mm | 0 / 48.2 mm / n | 0 / 82.4 mm / n |

### 6.4 解读

1. **baseline 目标不是不可达点**：8/8 baseline 都能到达 2cm 内，但 8/8 与障碍接触。因此这组是有效的“可达但会碰撞”challenge。
2. **`workspace_sdf` 的安全性最强**：在这 8 个样本中 contact rate 为 0%，优于 `ideal_sdf` 的 37.5%。这说明视觉链路的 robot self-mask、voxel persistence 和 CBF 组合已经能提供强安全约束。
3. **到达仍然是主要短板**：`workspace_sdf` 的 mean best_dist 为 99.3 mm，success latch@4cm 仅 12.5%。soft-settle 能改善已进圈样本（如 `idx=799`），但不能把未进圈样本伪造成成功。
4. **`idx=799` 是当前最合适的可视化正例**：baseline 会碰；`workspace_sdf` 无接触并进入 4cm 圈，soft-settle 后能继续 policy 微调并稳定在约 25 mm 以内。
5. **`idx=2472/2601/3919` 是控制层失败样本**：baseline 可达但会碰；避障后安全但离目标很远。这里不是状态机问题，而是 CBF 兜底缺少绕行/局部规划，policy 持续朝障碍后方目标推进时被安全约束长期改写。
6. **状态机结论**：`policy_soft_cbf` 比锁关节 `hold_q` 更适合作为后续抓取前的 SETTLE 阶段；它允许 policy 继续收敛，同时降低视觉 SDF 对末端的持续强干扰。但状态机只解决“进圈后驻留/微调”，不解决“未进圈的绕障到达”。

## 实验 7：随机细杆位置下 baseline / ideal_sdf / workspace_sdf 对比

### 7.1 实验设置

- **日期**：2026-07-14
- **目的**：避免只在固定细杆位置和固定 target 上得出过乐观结论；随机移动细杆位置后，重新筛选 baseline 会碰且可达的目标，再比较三组方法。
- **场景**：`SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- **输出**：`logs/eval/random_rod_sdf_5rounds/`
- **随机种子**：`seed=13`
- **随机杆底座范围**：
  - `x ∈ [0.10, 0.22] m`
  - `y ∈ [0.02, 0.16] m`
  - `z = 0.02 m`
- **rounds**：5/5 有效；每轮先扫描 target bank，选出 baseline 满足：
  - `contact_steps >= 3`
  - `best_dist <= 0.02m`
- **方法**：
  - `none`：不开避障，完整跑 10s；
  - `ideal_sdf`：明确障碍物 geom 表面点云 SDF + CBF；
  - `workspace_sdf`：`scene_depth` 深度 + robot segmentation self-mask + workspace crop + voxel persistence SDF + CBF。
- **状态机**：
  - 只对 `ideal_sdf` / `workspace_sdf` 启用；
  - `success_dist=0.04m`, `success_steps=5`, `settle_on_success=1.0s`；
  - `settle_mode=policy_soft_cbf`。

命令：

```bash
MUJOCO_GL=egl python mujoco/eval_random_rod_sdf.py \
  --rounds 5 \
  --scan-count 256 \
  --seed 13 \
  --use-sim-cam \
  --out-dir logs/eval/random_rod_sdf_5rounds
```

### 7.2 汇总指标

| 方法 | N | contact rate ↓ | reach@2cm ↑ | success latch@4cm ↑ | mean best_dist ↓ | mean end_dist ↓ | mean contact steps ↓ | mean max\|dq_cbf\| |
|------|---:|---------------:|------------:|--------------------:|-----------------:|----------------:|---------------------:|------------------:|
| none | 5 | **100.0%** | **100.0%** | — | **7.2 mm** | **9.9 mm** | 41.2 | 0.000 |
| ideal_sdf + soft-settle | 5 | 40.0% | 0.0% | 20.0% | 135.9 mm | 142.9 mm | 3.2 | 0.411 |
| workspace_sdf + soft-settle | 5 | **20.0%** | 0.0% | 20.0% | 156.9 mm | 168.5 mm | 3.8 | 0.473 |

### 7.3 每轮明细

| round | rod mount (x,y,z) m | target idx | none contact / best | ideal_sdf contact / best / success | workspace_sdf contact / best / success |
|------:|---------------------|-----------:|---------------------|------------------------------------|----------------------------------------|
| 0 | (0.204, 0.140, 0.020) | 2620 | 95 / 6.2 mm | 13 / 98.5 mm / n | 19 / 110.6 mm / n |
| 1 | (0.118, 0.090, 0.020) | 2961 | 39 / 14.7 mm | 0 / 113.5 mm / n | 0 / 148.1 mm / n |
| 2 | (0.143, 0.096, 0.020) | 406 | 25 / 4.9 mm | 3 / 29.0 mm / Y | 0 / 34.2 mm / Y |
| 3 | (0.109, 0.050, 0.020) | 2606 | 43 / 5.3 mm | 0 / 344.4 mm / n | 0 / 344.4 mm / n |
| 4 | (0.113, 0.081, 0.020) | 1919 | 4 / 5.1 mm | 0 / 94.4 mm / n | 0 / 147.4 mm / n |

### 7.4 解读

1. **随机杆位姿验证了 baseline 可达性**：5/5 round 中 baseline 都能到 2cm 内，且全部与细杆接触。因此这些样本不是目标不可达，而是“可达但会撞”的有效避障测试。
2. **`workspace_sdf` 在随机位姿下安全性仍优于 `ideal_sdf`，但不再是 0 接触**：contact rate 为 20%，比 `ideal_sdf` 的 40% 更低，但 round 0 仍出现 19 步接触，说明固定样本 quick8 的 0% contact 不能直接外推到随机杆位姿。
3. **到达精度仍是主要问题**：两种 SDF 方法 reach@2cm 都是 0%，success latch@4cm 也只有 20%。`workspace_sdf` 平均 best_dist 为 156.9 mm，比 `ideal_sdf` 的 135.9 mm 更保守。
4. **round 2 是当前随机位姿正例**：baseline 接触 25 步且 best 4.9 mm；`workspace_sdf` 0 接触、best 34.2 mm、进入 4cm success 圈。这适合做随机杆位置下的可视化正例。
5. **round 3 是强失败样本**：baseline 可达且接触 43 步；两种 SDF 方法都停在约 344 mm，说明该杆位姿对当前 policy+CBF 形成了强阻挡，仅靠局部 safety filter 无法恢复到达。
6. **阶段性判断**：视觉链路的 self-mask + voxel persistence + soft-settle 已经能在随机障碍位置下显著降低接触，但还不能满足抓取前 1–2 cm 精度要求。后续应把 4cm 判定定义为 `PREGRASP` 近场入口，而不是 `GRASP_READY`；抓取前还需要更严格的 1–2cm 位姿/稳定性判定，或引入局部 pregrasp/insert 规划。
