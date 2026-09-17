"""供动态目标和障碍物 smoke test 使用的小型运动辅助工具。"""

from __future__ import annotations

import math
from dataclasses import dataclass

import mujoco
import numpy as np


# 当前 target bank 的 x/y 范围；动态杆只在这个测试工作区内活动。
_WORKSPACE_XY_MIN = np.array([0.08, -0.25], dtype=np.float64)
_WORKSPACE_XY_MAX = np.array([0.45, 0.25], dtype=np.float64)


@dataclass(frozen=True)
class MotionSpec:
    kind: str = "none"
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    amplitude: tuple[float, float, float] = (0.0, 0.0, 0.0)
    period_s: float = 4.0
    phase: float = 0.0
    seed: int = 42
    random_active_s: float = 2.0
    clear_offset: tuple[float, float, float] = (0.18, 0.12, 0.0)
    clear_time_s: float = 2.0

    def _random_waypoint(self, index: int, amp: np.ndarray) -> np.ndarray:
        """可复现的随机路点；第一个点固定在原始位置，避免 episode 开头瞬移。"""
        if int(index) <= 0:
            return np.zeros(3, dtype=np.float64)
        rng = np.random.default_rng(np.random.SeedSequence([int(self.seed), int(index)]))
        return rng.uniform(-1.0, 1.0, size=3) * amp

    def _random_position(self, t_s: float, origin: np.ndarray, amp: np.ndarray) -> np.ndarray:
        segment = max(float(self.period_s), 1e-3)
        segment_idx = max(0, int(math.floor(float(t_s) / segment)))
        local_t = (float(t_s) - segment_idx * segment) / segment
        smooth_t = local_t * local_t * (3.0 - 2.0 * local_t)
        start = self._random_waypoint(segment_idx, amp)
        end = self._random_waypoint(segment_idx + 1, amp)
        return origin + (1.0 - smooth_t) * start + smooth_t * end

    @staticmethod
    def _clamp_to_workspace(pos: np.ndarray) -> np.ndarray:
        out = np.asarray(pos, dtype=np.float64).reshape(3).copy()
        out[:2] = np.clip(out[:2], _WORKSPACE_XY_MIN, _WORKSPACE_XY_MAX)
        return out

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
        if k == "random":
            # 每 period_s 秒换一个随机方向；smoothstep 让两个随机路点之间连续移动。
            return self._clamp_to_workspace(self._random_position(t_s, origin, amp))
        if k in ("random_depart", "random_depart_probe"):
            # 先无规则运动，随后连续移到工作区边缘，让机械臂有机会重新追目标。
            active_s = max(float(self.random_active_s), 0.0)
            if float(t_s) <= active_s:
                return self._clamp_to_workspace(self._random_position(t_s, origin, amp))
            start = self._random_position(active_s, origin, amp)
            clear_target = self._clamp_to_workspace(
                origin + np.asarray(self.clear_offset, dtype=np.float64).reshape(3)
            )
            clear_t = np.clip(
                (float(t_s) - active_s) / max(float(self.clear_time_s), 1e-3),
                0.0,
                1.0,
            )
            smooth_t = clear_t * clear_t * (3.0 - 2.0 * clear_t)
            return (1.0 - smooth_t) * start + smooth_t * clear_target
        raise ValueError(f"unknown motion kind: {self.kind!r}")


@dataclass
class MotionRunner:
    """带状态的动态障碍轨迹；probe 模式仅在夹爪接近目标后再回探一次。"""

    spec: MotionSpec
    probe_trigger_distance: float = 0.06
    probe_offset: tuple[float, float, float] = (-0.07, 0.05, -0.15)
    probe_time_s: float = 1.5
    trigger_time_s: float | None = None
    probe_start: np.ndarray | None = None
    probe_target: np.ndarray | None = None

    def position(
        self,
        t_s: float,
        base: np.ndarray,
        *,
        tcp_w: np.ndarray | None = None,
        target_w: np.ndarray | None = None,
    ) -> np.ndarray:
        nominal = self.spec.position(t_s, base=base)
        if str(self.spec.kind).lower() != "random_depart_probe":
            return nominal
        if self.trigger_time_s is None:
            can_trigger = float(t_s) >= float(self.spec.random_active_s + self.spec.clear_time_s)
            if can_trigger and tcp_w is not None and target_w is not None:
                tcp = np.asarray(tcp_w, dtype=np.float64).reshape(3)
                target = np.asarray(target_w, dtype=np.float64).reshape(3)
                if float(np.linalg.norm(tcp - target)) <= float(self.probe_trigger_distance):
                    self.trigger_time_s = float(t_s)
                    self.probe_start = nominal.copy()
                    self.probe_target = MotionSpec._clamp_to_workspace(
                        tcp + np.asarray(self.probe_offset, dtype=np.float64).reshape(3)
                    )
        if self.trigger_time_s is None or self.probe_start is None or self.probe_target is None:
            return nominal
        u = np.clip(
            (float(t_s) - self.trigger_time_s) / max(float(self.probe_time_s), 1e-3),
            0.0,
            1.0,
        )
        smooth_u = u * u * (3.0 - 2.0 * u)
        return (1.0 - smooth_u) * self.probe_start + smooth_u * self.probe_target


def parse_vec3(text: str, *, default: tuple[float, float, float]) -> tuple[float, float, float]:
    s = str(text).strip()
    if not s:
        return tuple(float(x) for x in default)
    parts = [p.strip() for p in s.replace(";", ",").split(",") if p.strip()]
    if len(parts) != 3:
        raise ValueError(f"expected vec3 as 'x,y,z', got {text!r}")
    return (float(parts[0]), float(parts[1]), float(parts[2]))


def set_body_pos(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    body_name: str,
    pos: np.ndarray,
    *,
    lock_upright: bool = False,
) -> bool:
    """移动由脚本驱动的障碍物；可选地锁住 ball joint，防止它被碰倒。"""
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, str(body_name))
    if bid < 0:
        return False
    model.body_pos[int(bid)] = np.asarray(pos, dtype=np.float64).reshape(3)
    if lock_upright:
        jnt_id = int(model.body_jntadr[int(bid)])
        if jnt_id >= 0 and int(model.jnt_type[jnt_id]) == int(mujoco.mjtJoint.mjJNT_BALL):
            qadr = int(model.jnt_qposadr[jnt_id])
            dadr = int(model.jnt_dofadr[jnt_id])
            data.qpos[qadr:qadr + 4] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
            data.qvel[dadr:dadr + 3] = 0.0
    mujoco.mj_forward(model, data)
    return True
