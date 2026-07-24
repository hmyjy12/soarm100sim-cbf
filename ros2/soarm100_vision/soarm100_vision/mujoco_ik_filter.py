from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import numpy as np


@dataclass
class IkCheckResult:
    reachable: bool
    reason: str
    pregrasp_pos_err_m: float
    pregrasp_rot_err_deg: float
    grasp_pos_err_m: float
    grasp_rot_err_deg: float
    min_joint_margin_rad: float
    q_pregrasp: np.ndarray
    q_grasp: np.ndarray


class MujocoCandidateIkFilter:
    """Bounded numerical IK against the SO-ARM100 MuJoCo kinematic model."""

    def __init__(
        self,
        *,
        repo_root: Path,
        mjcf: str,
        position_tolerance_m: float = 0.005,
        rotation_tolerance_deg: float = 3.0,
        max_iterations: int = 100,
    ) -> None:
        self.repo = Path(repo_root).expanduser().resolve()
        self.position_tolerance_m = float(position_tolerance_m)
        self.rotation_tolerance_deg = float(rotation_tolerance_deg)
        self.max_iterations = max(int(max_iterations), 1)

        old_path = list(sys.path)
        sys.path = [p for p in sys.path if Path(p or ".").resolve() != self.repo]
        import mujoco  # type: ignore

        sys.path = old_path
        mujoco_dir = str(self.repo / "mujoco")
        if mujoco_dir not in sys.path:
            sys.path.insert(0, mujoco_dir)
        import runtime  # type: ignore

        model_path = Path(mjcf)
        if not model_path.is_absolute():
            model_path = self.repo / model_path
        self.mujoco = mujoco
        self.runtime = runtime
        self.model = mujoco.MjModel.from_xml_path(str(model_path))
        self.ids = runtime.resolve_robot_ids(self.model)
        self.home_data = mujoco.MjData(self.model)
        runtime.reset_home(self.model, self.home_data, self.ids)
        self.n_arm = max(len(self.ids.qpos_adr) - 1, 1)

    def evaluate(
        self,
        *,
        pregrasp_pos: np.ndarray,
        grasp_pos: np.ndarray,
        grasp_quat_wxyz: np.ndarray,
    ) -> IkCheckResult:
        target_quat = self._normalize_quat(grasp_quat_wxyz)
        q_home = self.runtime.joint_pos(self.home_data, self.ids)
        q_low = np.asarray(self.ids.q_low, dtype=np.float64)
        q_high = np.asarray(self.ids.q_high, dtype=np.float64)
        q_mid = 0.5 * (q_low + q_high)
        q_mid[-1] = q_home[-1]
        seeds = [q_home.copy(), np.clip(q_mid, q_low, q_high)]
        if self.n_arm >= 6:
            for delta in (-0.5 * np.pi, 0.5 * np.pi):
                seed = q_home.copy()
                seed[5] = np.clip(seed[5] + delta, q_low[5], q_high[5])
                seeds.append(seed)

        pre = self._best_solution(np.asarray(pregrasp_pos), target_quat, seeds)
        if not pre["reachable"]:
            return self._result("pregrasp_unreachable", pre, None)

        final_seeds = [pre["q"].copy(), q_home.copy(), np.clip(q_mid, q_low, q_high)]
        grasp = self._best_solution(np.asarray(grasp_pos), target_quat, final_seeds)
        if not grasp["reachable"]:
            return self._result("grasp_unreachable", pre, grasp)
        return self._result("ok", pre, grasp)

    def _best_solution(self, target_pos: np.ndarray, target_quat: np.ndarray, seeds: list[np.ndarray]) -> dict:
        results = [self._solve(target_pos.reshape(3), target_quat, seed) for seed in seeds]
        return min(
            results,
            key=lambda item: (
                0 if item["reachable"] else 1,
                item["pos_err_m"],
                item["rot_err_deg"],
                -item["joint_margin_rad"],
            ),
        )

    def _solve(self, target_pos: np.ndarray, target_quat: np.ndarray, seed: np.ndarray) -> dict:
        data = self.mujoco.MjData(self.model)
        data.qpos[:] = self.home_data.qpos
        data.qvel[:] = 0.0
        self._set_q(data, seed)
        target_approach = self._quat_rotate(
            target_quat, np.array([0.0, 0.0, 1.0], dtype=np.float64)
        )

        for _ in range(self.max_iterations):
            tcp_pos, tcp_quat = self.runtime.tcp_pose_w(data, self.ids)
            pos_err = target_pos - np.asarray(tcp_pos, dtype=np.float64)
            tcp_approach = self._quat_rotate(
                tcp_quat, np.array([0.0, 0.0, 1.0], dtype=np.float64)
            )
            rot_err = np.cross(tcp_approach, target_approach)
            approach_err_deg = self._axis_angle_deg(tcp_approach, target_approach)
            if (
                np.linalg.norm(pos_err) <= self.position_tolerance_m
                and approach_err_deg <= self.rotation_tolerance_deg
            ):
                break

            pos_norm = float(np.linalg.norm(pos_err))
            if pos_norm > 0.015:
                pos_err *= 0.015 / pos_norm
            rot_norm = float(np.linalg.norm(rot_err))
            if rot_norm > 0.12:
                rot_err *= 0.12 / rot_norm

            jac = self._tcp_jacobian(data)
            rot_weight = 0.7
            jac[3:, :] *= rot_weight
            error = np.concatenate([pos_err, rot_weight * rot_err])
            lhs = jac @ jac.T + 2.0e-3 * np.eye(6, dtype=np.float64)
            try:
                dq = jac.T @ np.linalg.solve(lhs, error)
            except np.linalg.LinAlgError:
                dq = jac.T @ np.linalg.pinv(lhs) @ error
            dq = np.clip(dq, -0.10, 0.10)
            q = self.runtime.joint_pos(data, self.ids)
            q[: self.n_arm] = np.clip(
                q[: self.n_arm] + dq,
                self.ids.q_low[: self.n_arm],
                self.ids.q_high[: self.n_arm],
            )
            self._set_q(data, q)
            if float(np.linalg.norm(dq)) < 1.0e-8:
                break

        tcp_pos, tcp_quat = self.runtime.tcp_pose_w(data, self.ids)
        pos_err_m = float(np.linalg.norm(target_pos - np.asarray(tcp_pos, dtype=np.float64)))
        rot_err_deg = self._axis_angle_deg(
            self._quat_rotate(tcp_quat, np.array([0.0, 0.0, 1.0], dtype=np.float64)),
            target_approach,
        )
        q = self.runtime.joint_pos(data, self.ids)
        within_limits = bool(
            np.all(q[: self.n_arm] >= self.ids.q_low[: self.n_arm] - 1.0e-8)
            and np.all(q[: self.n_arm] <= self.ids.q_high[: self.n_arm] + 1.0e-8)
        )
        margins = np.minimum(
            q[: self.n_arm] - self.ids.q_low[: self.n_arm],
            self.ids.q_high[: self.n_arm] - q[: self.n_arm],
        )
        margin = float(np.min(margins)) if margins.size else float("nan")
        return {
            "reachable": bool(
                within_limits
                and pos_err_m <= self.position_tolerance_m
                and rot_err_deg <= self.rotation_tolerance_deg
            ),
            "pos_err_m": pos_err_m,
            "rot_err_deg": rot_err_deg,
            "joint_margin_rad": margin,
            "q": q.copy(),
        }

    def _tcp_jacobian(self, data, eps: float = 1.0e-5) -> np.ndarray:
        jac = np.zeros((6, self.n_arm), dtype=np.float64)
        q_saved = data.qpos.copy()
        for i, qadr in enumerate(self.ids.qpos_adr[: self.n_arm]):
            data.qpos[qadr] = q_saved[qadr] + eps
            self.mujoco.mj_forward(self.model, data)
            pos_plus, quat_plus = self.runtime.tcp_pose_w(data, self.ids)

            data.qpos[qadr] = q_saved[qadr] - eps
            self.mujoco.mj_forward(self.model, data)
            pos_minus, quat_minus = self.runtime.tcp_pose_w(data, self.ids)

            jac[:3, i] = (np.asarray(pos_plus) - np.asarray(pos_minus)) / (2.0 * eps)
            delta = self._quat_multiply(quat_plus, self._quat_conjugate(quat_minus))
            jac[3:, i] = self._quat_to_rotvec(delta) / (2.0 * eps)
            data.qpos[qadr] = q_saved[qadr]
        data.qpos[:] = q_saved
        self.mujoco.mj_forward(self.model, data)
        return jac

    def _set_q(self, data, q: np.ndarray) -> None:
        for value, qadr in zip(np.asarray(q, dtype=np.float64), self.ids.qpos_adr):
            data.qpos[int(qadr)] = float(value)
        data.qvel[:] = 0.0
        self.mujoco.mj_forward(self.model, data)

    def _result(self, reason: str, pre: dict, grasp: dict | None) -> IkCheckResult:
        margin = float(pre["joint_margin_rad"])
        final = grasp or {
            "pos_err_m": float("inf"),
            "rot_err_deg": float("inf"),
            "joint_margin_rad": margin,
            "q": np.full(len(self.ids.qpos_adr), float("nan")),
        }
        if grasp is not None:
            margin = min(margin, float(grasp["joint_margin_rad"]))
        return IkCheckResult(
            reachable=reason == "ok",
            reason=reason,
            pregrasp_pos_err_m=float(pre["pos_err_m"]),
            pregrasp_rot_err_deg=float(pre["rot_err_deg"]),
            grasp_pos_err_m=float(final["pos_err_m"]),
            grasp_rot_err_deg=float(final["rot_err_deg"]),
            min_joint_margin_rad=margin,
            q_pregrasp=np.asarray(pre["q"], dtype=np.float64),
            q_grasp=np.asarray(final["q"], dtype=np.float64),
        )

    @staticmethod
    def _normalize_quat(q) -> np.ndarray:
        arr = np.asarray(q, dtype=np.float64).reshape(4)
        return arr / max(float(np.linalg.norm(arr)), 1.0e-12)

    @staticmethod
    def _quat_conjugate(q) -> np.ndarray:
        q = np.asarray(q, dtype=np.float64).reshape(4)
        return np.array([q[0], -q[1], -q[2], -q[3]], dtype=np.float64)

    @staticmethod
    def _quat_multiply(a, b) -> np.ndarray:
        aw, ax, ay, az = np.asarray(a, dtype=np.float64).reshape(4)
        bw, bx, by, bz = np.asarray(b, dtype=np.float64).reshape(4)
        return np.array(
            [
                aw * bw - ax * bx - ay * by - az * bz,
                aw * bx + ax * bw + ay * bz - az * by,
                aw * by - ax * bz + ay * bw + az * bx,
                aw * bz + ax * by - ay * bx + az * bw,
            ],
            dtype=np.float64,
        )

    @classmethod
    def _quat_rotate(cls, q, vector) -> np.ndarray:
        quat = cls._normalize_quat(q)
        pure = np.concatenate(([0.0], np.asarray(vector, dtype=np.float64).reshape(3)))
        return cls._quat_multiply(
            cls._quat_multiply(quat, pure), cls._quat_conjugate(quat)
        )[1:]

    @staticmethod
    def _axis_angle_deg(a, b) -> float:
        lhs = np.asarray(a, dtype=np.float64).reshape(3)
        rhs = np.asarray(b, dtype=np.float64).reshape(3)
        lhs /= max(float(np.linalg.norm(lhs)), 1.0e-12)
        rhs /= max(float(np.linalg.norm(rhs)), 1.0e-12)
        return float(np.degrees(np.arccos(np.clip(float(np.dot(lhs, rhs)), -1.0, 1.0))))

    @classmethod
    def _quat_to_rotvec(cls, q) -> np.ndarray:
        quat = cls._normalize_quat(q)
        if quat[0] < 0.0:
            quat = -quat
        vector_norm = float(np.linalg.norm(quat[1:]))
        if vector_norm < 1.0e-12:
            return np.zeros(3, dtype=np.float64)
        angle = 2.0 * np.arctan2(vector_norm, np.clip(quat[0], -1.0, 1.0))
        return quat[1:] * (angle / vector_norm)
