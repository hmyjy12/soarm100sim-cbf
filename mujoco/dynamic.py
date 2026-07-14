"""Small motion helpers for dynamic target and obstacle smoke tests."""

from __future__ import annotations

import math
from dataclasses import dataclass

import mujoco
import numpy as np


@dataclass(frozen=True)
class MotionSpec:
    kind: str = "none"
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    amplitude: tuple[float, float, float] = (0.0, 0.0, 0.0)
    period_s: float = 4.0
    phase: float = 0.0

    def position(self, t_s: float, base: np.ndarray | None = None) -> np.ndarray:
        base_pos = np.zeros(3, dtype=np.float64) if base is None else np.asarray(base, dtype=np.float64).reshape(3)
        center = np.asarray(self.center, dtype=np.float64).reshape(3)
        amp = np.asarray(self.amplitude, dtype=np.float64).reshape(3)
        if str(self.kind).lower() == "none":
            return base_pos.copy()
        period = max(float(self.period_s), 1e-6)
        w = 2.0 * math.pi / period
        th = w * float(t_s) + float(self.phase)
        origin = center if np.linalg.norm(center) > 1e-12 else base_pos
        k = str(self.kind).lower()
        if k == "circle":
            return origin + np.array([amp[0] * math.cos(th), amp[1] * math.sin(th), amp[2] * math.sin(th)], dtype=np.float64)
        if k == "line":
            return origin + amp * math.sin(th)
        raise ValueError(f"unknown motion kind: {self.kind!r}")


def parse_vec3(text: str, *, default: tuple[float, float, float]) -> tuple[float, float, float]:
    s = str(text).strip()
    if not s:
        return tuple(float(x) for x in default)
    parts = [p.strip() for p in s.replace(";", ",").split(",") if p.strip()]
    if len(parts) != 3:
        raise ValueError(f"expected vec3 as 'x,y,z', got {text!r}")
    return (float(parts[0]), float(parts[1]), float(parts[2]))


def set_body_pos(model: mujoco.MjModel, data: mujoco.MjData, body_name: str, pos: np.ndarray) -> bool:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(body_name))
    if bid < 0:
        return False
    model.body_pos[int(bid)] = np.asarray(pos, dtype=np.float64).reshape(3)
    mujoco.mj_forward(model, data)
    return True
