# MuJoCo CBF 动态避障 Demo

本文只说明仿真 demo 的运行方式。算法、配置层次和真机边界见[总说明](避障加动态所有新增修改.md)。示例不是已完成的物理或真机 regression 结论。

## 运行准备

在可运行 MuJoCo 的 Python 环境中执行：

~~~bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
~~~

play.py 的仿真增强默认是 17-point、task-preserving、guidance/filter/bypass true，lookahead 2.0。示例仍显式传入关键参数以便复现。共享 CbfConfig 默认是 9-point、identity、guidance false、lookahead 0；障碍 velocity 为 0 时不会增加 dynamic padding。

## Random depart demo

~~~bash
python mujoco/play.py \
  --episodes 1 \
  --enable-cbf \
  --target-idx 1729 \
  --cbf-capsule-samples 17 \
  --cbf-qp-metric task_preserving \
  --cbf-task-preserve-weight 5.0 \
  --cbf-target-guidance \
  --cbf-correction-filter \
  --cbf-bypass-filter-when-unsafe \
  --cbf-dynamic-lookahead-steps 2.0 \
  --obstacle-motion random_depart \
  --obstacle-motion-center 0.25,0.075,0.02 \
  --obstacle-motion-amp 0.035,0.05,0.00 \
  --obstacle-motion-period 1.0 \
  --obstacle-motion-seed 42 \
  --obstacle-motion-active-time 2.0 \
  --obstacle-motion-clear-offset 0.18,-0.12,0.00 \
  --obstacle-motion-clear-time 2.0
~~~

## Random depart probe demo

~~~bash
python mujoco/play.py \
  --episodes 1 \
  --enable-cbf \
  --target-idx 3106 \
  --cbf-capsule-samples 17 \
  --cbf-qp-metric task_preserving \
  --cbf-task-preserve-weight 5.0 \
  --cbf-target-guidance \
  --cbf-correction-filter \
  --cbf-bypass-filter-when-unsafe \
  --cbf-dynamic-lookahead-steps 2.0 \
  --obstacle-motion random_depart_probe \
  --obstacle-motion-amp 0.02,0.02,0.00 \
  --obstacle-motion-period 1.0 \
  --obstacle-motion-seed 43 \
  --obstacle-motion-probe-trigger-distance 0.06 \
  --obstacle-motion-probe-offset=-0.07,0.05,-0.15
~~~

random_depart_probe 的触发时刻取决于 TCP 接近目标的过程，更适合展示交互反应，不适合作为严格百分比对比的唯一场景。

## 可视化与日志

--obstacle-can-fall 只适合观察碰撞后的物理画面；正式可比评测应关闭它，因为倒杆会改变后续轨迹。需要记录时可使用 --cbf-log 与 --traj-log，输出建议写在 logs/，该目录已被忽略。

## 常见问题

- **结果不同**：固定 target index、target seed、motion seed、motion 参数和 CBF 参数。
- **只要批量统计**：使用 eval_sdf_challenge.py 或 scripts/sweep_dynamic_obstacles.py，不必打开 viewer。
- **把 demo 当成真机配置**：不要这样做；当前真机仍是静态 cup、9-point、identity 的单臂链路。
