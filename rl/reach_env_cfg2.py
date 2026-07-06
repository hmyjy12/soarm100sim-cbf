"""姿态加强实验配置（cfg2）— 方案 A（只改奖励数值，不改成功区关姿态逻辑）。

与 `reach_env_cfg.ReachEnvCfg`（稳定默认 cfg1）并存。
成功区内仍关闭姿态项（保证进圈后少晃），靠抬高 6D success / hold
使「进门」比「门外刷姿态分」更划算。

设计要点（相对 cfg1）：
- orient_scale 轻微抬高（2→3），给姿态更多梯度；
- orient_dist_th 略放宽到接近姿态成功距离（0.03→0.05），勿到 0.08；
- success_scale / hold 明显抬高，保证进 6D success 的净收益为正。

用法::

    ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless --env-cfg 2 \\
      --checkpoint .../agent_102400.pt --max_iterations 150

主看 Metrics/success_rate、orientation_success_rate、target_success_rate，勿只看总分。
"""

from __future__ import annotations

from isaaclab.utils import configclass

from reach_env_cfg import ReachEnvCfg


@configclass
class ReachEnvCfg2(ReachEnvCfg):
    """方案 A：保位置、轻加强姿态、抬成功区回报（成功区仍关姿态项）。"""

    # 门外姿态引导：略强于 cfg1，但小于 success_bonus，避免盗分
    rew_orientation_scale: float = 3.0
    # 与姿态成功 enter 距离对齐：近目标才满权，避免远处灌姿态分
    orientation_reward_distance_threshold: float = 0.05

    # 进 6D success 必须划算：门外 orient 最多 ~3，进门 +8（+ hold）
    rew_success_scale: float = 8.0
    hold_reward_per_sec: float = 15.0
