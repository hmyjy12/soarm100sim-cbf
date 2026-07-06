"""从 skrl PPO checkpoint 加载 27→7 Gaussian policy（eval mean）。"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

try:
    from .constants import ACTION_DIM, OBS_DIM
except ImportError:
    from constants import ACTION_DIM, OBS_DIM  # type: ignore


class SkrlGaussianPolicy(torch.nn.Module):
    """与 skrl GaussianMixin [256,128,64]+ELU 权重布局对齐。"""

    def __init__(self, checkpoint_path):
        super().__init__()
        ckpt = torch.load(str(checkpoint_path), map_location="cpu", weights_only=False)
        policy = ckpt["policy"]
        pre = ckpt["state_preprocessor"]
        self.register_buffer("running_mean", pre["running_mean"].float())
        self.register_buffer("running_variance", pre["running_variance"].float())
        self.fc0 = torch.nn.Linear(OBS_DIM, 256)
        self.fc1 = torch.nn.Linear(256, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.policy_layer = torch.nn.Linear(64, ACTION_DIM)
        with torch.no_grad():
            self.fc0.weight.copy_(policy["net_container.0.weight"])
            self.fc0.bias.copy_(policy["net_container.0.bias"])
            self.fc1.weight.copy_(policy["net_container.2.weight"])
            self.fc1.bias.copy_(policy["net_container.2.bias"])
            self.fc2.weight.copy_(policy["net_container.4.weight"])
            self.fc2.bias.copy_(policy["net_container.4.bias"])
            self.policy_layer.weight.copy_(policy["policy_layer.weight"])
            self.policy_layer.bias.copy_(policy["policy_layer.bias"])
        self.eval()

    @torch.inference_mode()
    def act_mean(self, obs_np):
        obs = torch.as_tensor(obs_np, dtype=torch.float32).reshape(1, OBS_DIM)
        obs = (obs - self.running_mean) / (torch.sqrt(self.running_variance) + 1e-8)
        obs = torch.clamp(obs, min=-5.0, max=5.0)
        x = F.elu(self.fc0(obs))
        x = F.elu(self.fc1(x))
        x = F.elu(self.fc2(x))
        return self.policy_layer(x).cpu().numpy().reshape(ACTION_DIM)
