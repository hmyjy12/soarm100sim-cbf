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

## Static evaluator

~~~bash
python mujoco/eval_cbf.py \
  --num-episodes 32 \
  --seed 42 \
  --cbf-capsule-samples 17 \
  --cbf-qp-metric task_preserving \
  --cbf-task-preserve-weight 5.0 \
  --out-dir logs/eval/static_example
~~~

静态评测的 lookahead 默认是 0.0。输出目录包含 summary.json 与 summary.md；无接触不等于到达目标，应同时查看 safe reach 和距离指标。

## Dynamic evaluator

~~~bash
python mujoco/eval_sdf_challenge.py \
  --out-dir logs/eval/dynamic_example \
  --seed 42 \
  --scan-count 64 \
  --max-challenges 16 \
  --methods none geom \
  --obstacle-motion random_depart \
  --obstacle-motion-amp 0.02,0.02,0.00 \
  --obstacle-motion-period 1.0 \
  --obstacle-motion-seed 43 \
  --obstacle-motion-active-time 2.0 \
  --obstacle-motion-clear-offset 0.18,0.12,0.00 \
  --obstacle-motion-clear-time 2.0 \
  --workspace-sdf-preset dynamic
~~~

该入口默认使用动态 lookahead 2.0。输出中的 challenge_indices.json 可以重放 evaluator 使用的 target 顺序：

~~~bash
python mujoco/play.py \
  --episodes 16 \
  --enable-cbf \
  --target-indices-file logs/eval/dynamic_example/challenge_indices.json \
  --obstacle-motion random_depart \
  --obstacle-motion-seed 43
~~~

## Sweep

~~~bash
python scripts/sweep_dynamic_obstacles.py \
  --out-root logs/eval/dynamic_obstacle_sweep \
  --obstacle-seeds 42,43,44,45 \
  --motions random,random_depart \
  --amps 0.02,0.02,0.00 \
  --periods 1.0 \
  --scan-count 64 \
  --max-challenges 16
~~~

默认扫描两种 motion 和四个 obstacle seed，共 8 个场景。每组结果写在 out-root 下的 scenario 目录；汇总文件为 sweep_summary.csv 和 sweep_summary.md。

扫描多组振幅时，--amps 用分号分隔三维向量：

~~~bash
--amps '0.01,0.01,0.00;0.02,0.02,0.00;0.03,0.03,0.00'
~~~

--skip-existing 默认开启，已有 summary.json 的场景会跳过；用 --no-skip-existing 可重跑并更新该场景结果。所有输出建议放在 logs/，该目录已被忽略。

## Reproducibility checklist

- 固定 --seed，保持 target 扫描/抽样一致。
- 固定 --obstacle-motion-seed、motion、amplitude、period 与动态参数。
- 记录 target index 或使用 evaluator 写出的 challenge_indices.json。
- 显式写出关键 CBF 参数，不依赖环境或本机默认值。
- 不要把 single demo、未完成的 MuJoCo regression 或真机未运行结果当作完整验证。
