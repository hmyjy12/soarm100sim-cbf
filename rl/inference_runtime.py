"""SO-100 Reach 推理运行时：checkpoint 解析、eval PPO 配置、环境栈构建。"""

from __future__ import annotations

import glob
import os
import re
from pathlib import Path
from typing import Any

RL_ROOT = Path(__file__).resolve().parent
DEFAULT_CKPT_ROOT = RL_ROOT / "checkpoints"


def list_checkpoints(root: str | Path | None = None) -> list[str]:
    ckpt_root = Path(root or DEFAULT_CKPT_ROOT)
    pts = glob.glob(str(ckpt_root / "**" / "*.pt"), recursive=True)
    pts.sort(key=os.path.getmtime)
    return pts


def sanitize_cli_path(path: str) -> str:
    p = (path or "").strip()
    p = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", p)
    p = p.replace("\x1b[200~", "").replace("\x1b[201~", "")
    if p.endswith("~"):
        p = p[:-1]
    return p.strip().strip('"').strip("'")


def resolve_checkpoint(path: str, ckpt_root: str | Path | None = None) -> str:
    root = Path(ckpt_root or DEFAULT_CKPT_ROOT)
    p = sanitize_cli_path(os.path.expanduser(path))
    if p and os.path.isabs(p) and os.path.isfile(p):
        return os.path.normpath(p)

    candidates: list[str] = []
    if p:
        candidates.append(os.path.abspath(p))
        candidates.append(str(root / p))
        marker = "checkpoints" + os.sep
        norm = p.replace("\\", "/")
        if marker in norm or "checkpoints/" in norm:
            idx = norm.find("checkpoints/")
            if idx >= 0:
                tail = norm[idx:].replace("/", os.sep)
                candidates.append(str(RL_ROOT / tail))

    for candidate in candidates:
        candidate = os.path.normpath(candidate)
        if os.path.isfile(candidate):
            return candidate

    latest = list_checkpoints(root)
    if latest:
        return latest[-1]
    raise FileNotFoundError(f"未找到 checkpoint: {path!r}（已搜索 {root}）")


def build_play_agent_cfg(*, seed: int = 42) -> dict[str, Any]:
    return {
        "seed": int(seed),
        "models": {
            "separate": False,
            "policy": {
                "class": "GaussianMixin",
                "clip_actions": False,
                "clip_log_std": True,
                "min_log_std": -20.0,
                "max_log_std": 2.0,
                "initial_log_std": 0.0,
                "network": [
                    {
                        "name": "net",
                        "input": "OBSERVATIONS",
                        "layers": [256, 128, 64],
                        "activations": "elu",
                    }
                ],
                "output": "ACTIONS",
            },
            "value": {
                "class": "DeterministicMixin",
                "clip_actions": False,
                "network": [
                    {
                        "name": "net",
                        "input": "OBSERVATIONS",
                        "layers": [256, 128, 64],
                        "activations": "elu",
                    }
                ],
                "output": "ONE",
            },
        },
        "memory": {"class": "RandomMemory", "memory_size": -1},
        "agent": {
            "class": "PPO",
            "rollouts": 24,
            "learning_epochs": 5,
            "mini_batches": 4,
            "discount_factor": 0.99,
            "lambda": 0.95,
            "learning_rate": 1e-4,
            "learning_rate_scheduler": "KLAdaptiveLR",
            "learning_rate_scheduler_kwargs": {"kl_threshold": 0.01},
            "state_preprocessor": "RunningStandardScaler",
            "state_preprocessor_kwargs": None,
            "value_preprocessor": "RunningStandardScaler",
            "value_preprocessor_kwargs": None,
            "random_timesteps": 0,
            "learning_starts": 0,
            "grad_norm_clip": 1.0,
            "ratio_clip": 0.2,
            "value_clip": 0.2,
            "clip_predicted_values": True,
            "entropy_loss_scale": 0.0,
            "value_loss_scale": 2.0,
            "rewards_shaper_scale": 0.01,
            "time_limit_bootstrap": True,
            "experiment": {
                "directory": "/tmp/so100_reach_play",
                "experiment_name": "play",
                "write_interval": 0,
                "checkpoint_interval": 0,
            },
        },
        "trainer": {
            "class": "SequentialTrainer",
            "timesteps": 1000,
            "environment_info": "log",
            "close_environment_at_exit": False,
        },
    }


def create_inference_stack(
    *,
    checkpoint: str,
    num_envs: int = 1,
    seed: int = 42,
    use_test_npz: bool = True,
    enable_contact_sensors: bool = False,
    debug_vis: bool = True,
) -> dict[str, Any]:
    """构建 ReachEnv + skrl Runner（eval）。"""
    from isaaclab_rl.skrl import SkrlVecEnvWrapper
    from skrl.utils.runner.torch import Runner

    from reach_env import ReachEnv
    from reach_env_cfg import ReachEnvCfg

    env_cfg = ReachEnvCfg()
    env_cfg.seed = int(seed)
    env_cfg.scene.num_envs = int(num_envs)
    env_cfg.debug_vis = bool(debug_vis)
    env_cfg.enable_contact_sensors = bool(enable_contact_sensors)
    if use_test_npz and (env_cfg.workspace_npz_path_test or "").strip():
        env_cfg.workspace_npz_path = os.path.abspath(env_cfg.workspace_npz_path_test)

    ckpt_path = resolve_checkpoint(checkpoint)
    reach_env = ReachEnv(env_cfg)
    if debug_vis:
        reach_env.set_debug_vis(True)
    env = SkrlVecEnvWrapper(reach_env, ml_framework="torch")

    runner = Runner(env, build_play_agent_cfg(seed=seed))
    runner.agent.load(ckpt_path)
    runner.agent.set_running_mode("eval")

    step_dt = float(env_cfg.sim.dt * env_cfg.decimation)
    return {
        "env_cfg": env_cfg,
        "reach_env": reach_env,
        "env": env,
        "runner": runner,
        "checkpoint": ckpt_path,
        "step_dt": step_dt,
    }
