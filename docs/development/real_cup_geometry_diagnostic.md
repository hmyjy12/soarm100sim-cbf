# 真机杯子 CBF 几何诊断（2026-09-10）

## 已确认与未确认

源码确认旧版真机 PointCloudSdfObstacle 的搜索半径是 0.15m。超出半径时
pointcloud_sdf_h_and_grad_p 直接返回 0.15 和零梯度，不扣胶囊半径、安全距离。
正常分支是 h = 中心到点云距离 - radius - inflate - d_safe。
因此旧日志 h=0.15 不能作为 clearance。真机现改为未截断最近邻查询；共享仿真
CBF 算法及安全距离、激活阈值、hard stop 未改变。

当前标定文件 T_parent_cam @ diag(1,-1,-1,1) 与 source_handeye 中
T_base_camera.matrix 最大元素差为 0，旋转行列式约 1。这排除了当前两个文件
之间的转换不一致，不证明物理标定精度足够。

留存 segment_target_latest.json 的 camera 中心是
(0.022370,-0.002766,0.385000)m，转换后为
(0.267982,0.176849,0.159415)m。cloud 日志曾记录 bbox
[(0.215,0.123,0.055),(0.314,0.221,0.201)]m。两者在位置上相容，但不是同帧，
不能据此宣称现场 2–3cm clearance 已验证。

self-filter 使用胶囊 radius + 0.035m 删除点。测试已证明胶囊外 25mm 的点会
被删除；这属于实际盲区机制，但原实验是否因此受影响必须看同帧过滤前后数据。
不能把过滤掉的点一律加回来：它们也可能是线缆、机身和标定误差。

只读 ROS 实测探测 5 秒没有收到任何有效配对，geometry.jsonl 为空。没有发送
运动指令，也没有完成物理静态/动态避障验收。现有日志没有保存完整原始点云和
同帧关节，不能离线还原最早 h=0.15 的摆杯现场。

## 修改

- policy 使用未截断最近邻，普通 tick 记录最近障碍物点、monitor 中心、半径和 clearance。
- 点云源时间与接收时间一起检查 freshness；不足 min_points 时停止，避免空障碍列表继续运动。
- 已成功发布的 depth 不再因新 mask 重复处理。失败帧仍可在 mask 到达时重试。
- dynamic 每帧清除历史体素，包括同一体素内的历史均值；static 锁定行为保留。
- cloud 日志新增 geometry=JSON：optical/base 前后统计、self-filter 前后 clearance、胶囊端点。
- 新增只读诊断脚本：所有 CBF monitor 端点、当前 shared 默认 9 点采样距离、精确线段距离、旧截断值、
  同帧关节和完整最终点云 NPZ，可离线重放。

## 一条命令采集（不启动机械臂控制器）

前提：相机及已有 /joint_states 发布端运行，机械臂保持静止；停止 reach policy 和
此前的 obstacle cloud/segmenter，避免同名节点及多点云发布者。
此入口不初始化姿态、不切换力矩、不发布动作。缺少输入直接退出。

```bash
cd ~/soarm100sim_project
bash ros2/scripts/real/run_obstacle_geometry_diagnostic.sh static 60
```

杯子先摆好再运行。static 会锁住首次满足 min_points 的过滤后杯子点云，后续仅更新
心跳时间戳。cloud.log 中 locked/source_stamp 说明真正来源，不能用心跳判断杯子移动。

采集目录打印在终端：log/runtime/hardware/geometry_<时间>_static_<PID>/。
包含 geometry.jsonl、snapshot_*.npz、cloud.log、segmenter.log、calibration.json。
预设与 static_cup 脚本一致：cup best.pt、safe=0.03、self margin=0.035、thin filter on。
使用其他配置时，直接订阅工具的 --mjcf/--safe-distance/--inflate 应与 policy 参数一致。

如果视觉节点已独立运行，只启动订阅器。先激活本机可运行 ROS 2、MuJoCo 与 vision 的环境；
可用 `VISION_PYTHON` 指定该环境的解释器：

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
PYTHON_BIN="${VISION_PYTHON:-python}"
"$PYTHON_BIN" ros2/scripts/real/diagnose_obstacle_geometry.py --seconds 60
```

离线重放（替换实际 NPZ 路径）：

```bash
PYTHON_BIN="${VISION_PYTHON:-python}"
"$PYTHON_BIN" ros2/scripts/real/diagnose_obstacle_geometry.py \
  --snapshot /absolute/path/to/snapshot.npz
```

## 判读顺序

1. cloud.log 的 optical_selected：mask 内深度点数、centroid、bbox。
2. base_before_filters 与 base_output：变换及裁剪前后的位置。
3. before_self_clearance_m 与 output_clearance_m，加原状态中的 capsule_self_rm、
   wrist_box_rm、thin_removed_points：判断近处点是否被删除。clearance 为到名义胶囊
   表面的距离，不包含 35mm 过滤 margin；这里是连续线段，policy 使用当前 real-safe 的 9 点采样。
4. geometry.jsonl 的 monitors：a_base_m/b_base_m/radius_m 定位机器人几何，
   center_base_m 与 nearest_point_base_m 定位计算距离的两个点。
5. worst.h_m + d_safe_m = worst.clearance_m。
   legacy_h_min_m=0.15 且 legacy_truncated=true 表示旧搜索半径分支被触发。
6. continuous_clearance_m 与 clearance_m 的差表示胶囊采样误差。

激活阈值是 h<0.04，因此在 safe=0.03 下对应 clearance<0.07m。
hard stop 对应 h<0.015-0.03=-0.015m。active=True 不要求 correction>0；
名义动作满足约束时可以零修正。合成测试验证了向障碍物接近且违反约束时会得到
非零修正并减少接近分量，不代表真机已验收。

## 下一阶段：静止机械臂检查动态点云

静态几何吻合后，机械臂仍保持静止，运行：

```bash
cd ~/soarm100sim_project
bash ros2/scripts/real/run_obstacle_geometry_diagnostic.sh dynamic 60
```

缓慢移动杯子，检查 source stamp 前进、centroid/bbox 跟随、h 随距离变化、无历史位置
残留；这仍然只做感知和 FK，不发动作。若断流或配对失败，报告 invalid，不放宽同步。

当前真机 obstacle.velocity 仍为零：dynamic 只实现随帧更新位置的反应式 CBF。
接入速度预测需在现场几何和动态观测通过后进行；离散 CBF 的 velocity 表示每控制步
位移，不能直接把 m/s 填进去。最终真机动作测试仍未执行。

## 验证

vision_seg 无 pytest；直接加载并运行三个无 fixture 的测试模块，共13个测试函数通过：
test_real_geometry_diagnostic.py、test_obstacle_robust_cbf.py、test_sdf_cbf_core.py。
包含旧截断复现、真实模型/FK/CBF 距离逐 monitor 对比、近障碍动作修正、重复帧、
空点云/过期点云拒绝、self-filter 25mm 盲区。shell 语法检查通过。
