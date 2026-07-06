"""姿态加权实验环境配置（cfg2）。

与 `reach_env_cfg.ReachEnvCfg`（稳定默认）并存。
本文件只覆写 ori 相关奖励阈值，其余字段继承默认 cfg，便于随时回切。

用法（train.py）::

    ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless --env-cfg 2
    ./isaaclab.sh -p ../rl_code/soarm100sim/rl/train.py --headless --env-cfg ori
"""

from __future__ import annotations

from isaaclab.utils import configclass

from reach_env_cfg import ReachEnvCfg


@configclass
class ReachEnvCfg2(ReachEnvCfg):
    """姿态增强实验配置（ori resume 参数）。

    相对默认 cfg：
    - ``rew_orientation_scale``: 2.0 → 5.0
    - ``orientation_reward_distance_threshold``: 0.03 → 0.08

    已知风险：姿态项相对成功 bonus 偏大时，策略可能为刷分而规避 6D success
    （``rew_orientation`` 在 success 区内会被关掉）。调参前建议先看
    ``Metrics/success_rate`` 与 ``Rewards/rew_orientation_mean``，勿只看总分。
    """

    rew_orientation_scale: float = 5.0
    orientation_reward_distance_threshold: float = 0.08
