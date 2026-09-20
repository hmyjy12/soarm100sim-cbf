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

## Orbbec eye-to-hand 标定

Orbbec 固定在工作区、标定板固定在夹爪时，使用仓库根目录保留的手动采样入口：

```bash
./ros2/run_orbbec_handeye_manual.sh
```

它会启动相机、标定 viewer 和受控的手动采样流程。标定板、相机和机械臂安装位置
发生变化后，都应重新采样并生成新的 calibration artifact；不要把某次实验生成的
target snapshot 当作通用标定配置。

### Hand-eye calibration：Tsai → Park

**为什么改。** 当前固定 Orbbec 的 eye-to-hand 场景中，原来的 Tsai 方法在实际标定
和机械臂观察中的效果不如 Park，因此将求解方法切换为 Park。这里的结论只针对当前
安装方式和采样条件，不代表 Park 对所有相机、机械臂或样本集都更好。

**参考依据。** 改动直接使用 OpenCV 的 `calibrateHandEye` API，沿用本项目现有的
eye-to-hand 管线（固定相机、夹爪持标定板），并以本次实际标定和机械臂/视觉检查为
依据；没有引入或声称复现外部论文实现。

**改了什么。** `orbbec_eye_to_hand_calibrator_node.py` 将
`cv2.CALIB_HAND_EYE_TSAI` 替换为 `cv2.CALIB_HAND_EYE_PARK`；采样 metadata、
JSON/YAML artifact 的 `method` 字段和 viewer 状态文字均同步为 Park。为兼容已有的
session 引用，artifact 文件名暂时保留历史的 `*_tsai.json` / `*_tsai.yaml`；应以内容中的
`method` 字段判断实际求解方法。

**怎么测试、效果如何。** 本次使用 26 个 calibration samples 生成 Park artifact；
固定板在夹爪坐标系下的 translation RMS 约为 19.96 mm，rotation RMS 约为 5.57°。
已进行真实机械臂/视觉效果检查，当前 eye-to-hand setup 中的观察结果良好，标定结果
可用于该现场配置。

**限制。** 仓库中没有同一批样本下 Tsai 与 Park 的严格定量 A/B 对照，因此不能据此
宣称 Park 在数值上普遍优于 Tsai。更换相机、机械臂安装位置、标定板固定方式或工作区
后都需要重新标定与复核。

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

### Relative target snapshot 的保存位置

`--relative-delta` 不是读取一份固定 target：启动前，`run_policy_reach.sh` 会调用
`make_relative_policy_reach_target.py`，从 `/joint_states` 读取当前姿态、通过 MuJoCo FK
得到 TCP，再生成当前 TCP 加相对位移的 target。旧的
`ros2/config/real/policy_reach_target_relative.json` 因而会随每次现场运行覆盖，不是可复现
配置；把它 tracked 会污染 Git 状态，也可能让某次现场姿态被误当成通用 target。

现在生成文件写入已忽略的
`log/runtime/hardware/policy_reach_target_relative.json`。普通静态 target
`ros2/config/real/policy_reach_target.json` 保持不变。这个位置沿用仓库已有的
`log/runtime/hardware/` runtime artifact 约定；`policy_reach_node.py` 仍读取同一轮启动刚生成
的 JSON，target 计算、`--relative-delta` 的 frame 语义和控制行为均未改变。

本次迁移通过 `bash -n`、generator 的 Python 编译、Git ignore/path 检查，以及迁移前后
snapshot 的逐字节比较做了静态验证；未在本次路径迁移中重新执行真机 motion regression。
旧手工命令若显式使用
`--target-config ros2/config/real/policy_reach_target_relative.json`，需要改为新 runtime 路径。
`log/runtime/` 是本地运行产物，不保证长期保留；需要保留某次 target 时应主动复制归档。

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
