# 真机脚本菜单

这里的脚本都和真实机械臂实验有关。看到 `policy`、`hardware`、`grasp` 这类名字时，要默认它可能会让机械臂动。

## 最常跑

| 文件 | 会不会动机械臂 | 白话用途 |
|---|---:|---|
| `run_orbbec_rgbd.sh` | 不会 | 开 RGB-D 相机 |
| `run_fixed_yolo_sam_mask.sh` | 不会 | 只看 cup 检测和 mask |
| `run_policy_reach_static_cup.sh` | 会 | 推荐的静态 cup 避障 reach preset |
| `run_policy_reach.sh` | 会 | 通用 policy reach 大入口 |

## 调试和采数据

| 文件 | 会不会动机械臂 | 白话用途 |
|---|---:|---|
| `check_orbbec_rgbd_sync.py` | 不会 | 检查 RGB/depth 是否同步 |
| `run_fixed_yolo_tracking.sh` | 不会 | 单独测试 YOLO tracking |
| `run_collect_link_self_occupancy.sh` | 可能会 | 采机械臂自身、电线附近点云，用来做过滤 |
| `capture_policy_ready_pose.sh` | 看参数 | 记录当前机械臂姿态 |
| `run_policy_axis_diagnostic.sh` | 会 | 检查某个方向动得对不对 |
| `run_policy_reach_three_pose.sh` | 会 | 连续测多个 reach 目标 |

## 抓取相关

| 文件 | 会不会动机械臂 | 白话用途 |
|---|---:|---|
| `run_single_grasp_2real.sh` | 会 | 真机单次抓取实验 |

## 当前避障建议先用哪个

先用这个：

```bash
./ros2/scripts/real/run_policy_reach_static_cup.sh \
  --relative-delta 0.02,0,0 \
  --confirm RUN_POLICY_REACH
```

它本质上是给 `run_policy_reach.sh` 套了一层默认参数，避免每次手敲一长串。

要改目标距离，就改 `--relative-delta`。

要改避障距离，就加：

```bash
--obstacle-safe-distance-m 0.04
```

要改最大每轮关节变化，就加：

```bash
--max-tracking-error-rad 0.30
```

注意：这里参数放在最后也能覆盖 preset 里的默认值。

## 什么脚本先别乱跑

带这些词的脚本，先弄懂再跑：

```text
grasp
handeye
calibrator
single_joint
three_pose
axis_diagnostic
```

它们不是垃圾，但风险更高，或者只在特定实验阶段有用。
