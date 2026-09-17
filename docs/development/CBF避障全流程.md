# CBF 单臂静态/动态避障全流程

本文说明当前单臂仿真的端到端控制路径。配置边界、数学接口与验证状态见[总说明](避障加动态所有新增修改.md)。

## 一帧控制流程

~~~text
MuJoCo 当前状态
    ↓
刷新障碍物位置与速度
    ↓
（仅 target_guidance=true）选择临时 waypoint
    ↓
policy 生成名义动作 dq_nom
    ↓
胶囊/监视点与障碍物生成 CBF 约束
    ↓
QP 求安全修正 dq_cbf
    ↓
（按配置）CBF correction filter 或 unsafe bypass
    ↓
执行最终动作 dq_total
~~~

CBF 是局部安全修正，不是完整路径规划器。默认 runtime 不启用 waypoint；仿真增强入口才显式启用 target guidance。

## 入口选择

| 入口 | 用途 | lookahead 默认 |
|---|---|---:|
| mujoco/play.py | 单局可视化与 target-bank 复现 | 2.0 |
| mujoco/eval_cbf.py | 静态固定杆评测 | 0.0 |
| mujoco/eval_random_rod_sdf.py | 静态随机杆评测 | 0.0 |
| mujoco/eval_sdf_challenge.py | 动态障碍 challenge | 2.0 |
| scripts/sweep_dynamic_obstacles.py | 多 seed/motion 批量评测 | evaluator 默认 2.0 |

## 静态评测

~~~bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

python mujoco/eval_cbf.py \
  --num-episodes 32 \
  --seed 42 \
  --cbf-capsule-samples 17 \
  --cbf-qp-metric task_preserving \
  --cbf-task-preserve-weight 5.0 \
  --out-dir logs/eval/static_example
~~~

关注 summary.json 中的接触率、safe_reach_2cm_rate、最佳/结束距离。无接触不等于到达目标。

## 动态评测

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
  --workspace-sdf-preset dynamic
~~~

动态 evaluator 默认使用 17-point、task-preserving、guidance/filter/bypass 与 lookahead 2.0。严格复现时建议显式写出关键参数和 seed。

## 单局可视化

~~~bash
python mujoco/play.py \
  --episodes 1 \
  --enable-cbf \
  --target-idx 1729 \
  --obstacle-motion random_depart \
  --obstacle-motion-seed 42
~~~

obstacle motion 默认 none。--target-indices-file 可按 JSON 内 index 顺序连续播放 target bank，适用于复现 evaluator 写出的 challenge_indices.json。

## 当前真机边界

真实 policy_reach 使用 9-point、identity、静态 cup obstacle、obstacle velocity 0 与 lookahead 0。它不接入本页的 WaypointManager、MotionRunner、sweep 或双臂实验能力。
