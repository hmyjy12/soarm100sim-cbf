#!/usr/bin/env python3
"""SO-100 Plus 单臂 6D Reach — 推理 / 可视化（obs=27, act=7）。

================================================================================
启动方式
================================================================================

1) 交互选择最新 checkpoint（默认开 GUI 看红/绿球）
   cd ~/isaac_lab/isaac_ws/IsaacLab
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/execute.py

2) 指定 checkpoint
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/execute.py \\
     --checkpoint ../rl_code/soarm100sim/rl/checkpoints/<run>/agent.pt

3) 无界面快速跑
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/execute.py --headless \\
     --checkpoint <path/to/agent.pt>

4) 采集关节轨迹 JSON（加 --collect-log）
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/execute.py --collect-log

推理文本日志默认写入 rl/logs/inference/，含每回合 position/orientation 成功率。
"""

from __future__ import annotations

import argparse
import atexit
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

RL_ROOT = Path(__file__).resolve().parent
CKPT_ROOT = RL_ROOT / "checkpoints"


def _pick_checkpoint_interactive() -> str:
    from inference_runtime import list_checkpoints

    pts = list_checkpoints(CKPT_ROOT)
    if not pts:
        raise FileNotFoundError(f"在 {CKPT_ROOT} 下未找到 .pt，请先运行 train.py。")
    print("\n========== 可用 Checkpoint ==========")
    for i, p in enumerate(pts):
        tag = " ← 最新" if i == len(pts) - 1 else ""
        print(f"  [{i}] {os.path.relpath(p, CKPT_ROOT)}{tag}")
    print("======================================")
    while True:
        raw = input(f"请输入序号（回车=最新 [{len(pts) - 1}]）: ").strip()
        if raw == "":
            return pts[-1]
        if raw.isdigit() and 0 <= int(raw) < len(pts):
            return pts[int(raw)]
        print(f"无效输入，请输入 0 ~ {len(pts) - 1}")


_pre_parser = argparse.ArgumentParser(add_help=False)
_pre_parser.add_argument("--checkpoint", type=str, default=None)
_pre_parser.add_argument("--num_envs", type=int, default=1)
_pre_args, _remaining = _pre_parser.parse_known_args()

if _pre_args.checkpoint:
    from inference_runtime import resolve_checkpoint

    resume_path = resolve_checkpoint(_pre_args.checkpoint)
    print(f"[INFO] checkpoint: {resume_path}")
else:
    resume_path = _pick_checkpoint_interactive()
    print(f"\n[INFO] 已选择: {resume_path}")

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="SO-100 Plus 单臂 Reach 推理")
parser.add_argument("--checkpoint", type=str, default=None)
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--collect-log", action="store_true", help="采集关节轨迹 JSON")
parser.add_argument(
    "--log-path",
    type=str,
    default=str(RL_ROOT / "logs" / "joint_log.json"),
    help="关节 JSON 输出路径（仅 --collect-log）",
)
parser.add_argument("--log-env-id", type=int, default=0)
parser.add_argument("--log-every", type=int, default=1)
parser.add_argument(
    "--run-log-dir",
    type=str,
    default=str(RL_ROOT / "logs" / "inference"),
    help="推理文本日志目录",
)
parser.add_argument("--no-run-log", action="store_true", help="关闭推理文本日志")
parser.add_argument("--use-train-npz", action="store_true", help="使用 train NPZ 而非 test NPZ")
AppLauncher.add_app_launcher_args(parser)
args_cli, hydra_args = parser.parse_known_args()
sys.argv = [sys.argv[0]] + hydra_args

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import torch

sys.path.insert(0, str(RL_ROOT))

from inference_runtime import create_inference_stack, resolve_checkpoint
from sample.constants import REACH_JOINT_NAMES


class InferenceDataLogger:
    """按 sample JSON 格式记录单臂 7 关节 + TCP 位姿。"""

    def __init__(self, reach_env, *, enabled: bool, save_path: str, env_id: int, sample_every: int):
        self.reach_env = reach_env
        self.enabled = enabled
        self.save_path = os.path.abspath(os.path.expanduser(save_path))
        self.env_id = env_id
        self.sample_every = max(1, int(sample_every))
        self.records: list[dict] = []
        self._step_counter = 0
        self._joint_ids: dict[str, int] = {}

        if not self.enabled:
            return
        if not (0 <= self.env_id < self.reach_env.num_envs):
            raise ValueError(f"log-env-id 越界: {self.env_id}")
        for name in REACH_JOINT_NAMES:
            ids, _ = self.reach_env.robot.find_joints(name)
            if len(ids) == 0:
                raise RuntimeError(f"未找到关节: {name}")
            self._joint_ids[name] = int(ids[0])
        os.makedirs(os.path.dirname(self.save_path) or ".", exist_ok=True)
        with open(self.save_path, "w", encoding="utf-8") as handle:
            json.dump([], handle, ensure_ascii=False, indent=2)

    def collect(self, time_s: float) -> None:
        if not self.enabled:
            return
        self._step_counter += 1
        if self._step_counter % self.sample_every != 0:
            return

        env_i = self.env_id
        root = self.reach_env.robot.data.root_pos_w[env_i, :3]
        tcp_w, tcp_quat = self.reach_env._tcp_pose_w()
        tcp_rel = tcp_w[env_i] - root
        quat = tcp_quat[env_i]

        arm_state = {}
        for name in REACH_JOINT_NAMES:
            jid = self._joint_ids[name]
            arm_state[name] = {
                "pos": float(self.reach_env.robot.data.joint_pos[env_i, jid].item()),
                "vel": float(self.reach_env.robot.data.joint_vel[env_i, jid].item()),
            }

        self.records.append(
            {
                "time": float(time_s),
                "arm": arm_state,
                "tcp": {
                    "pos": {
                        "x": float(tcp_rel[0].item()),
                        "y": float(tcp_rel[1].item()),
                        "z": float(tcp_rel[2].item()),
                    },
                    "quat": {
                        "w": float(quat[0].item()),
                        "x": float(quat[1].item()),
                        "y": float(quat[2].item()),
                        "z": float(quat[3].item()),
                    },
                },
            }
        )

    def save(self, *, quiet: bool = False) -> None:
        if not self.enabled:
            return
        with open(self.save_path, "w", encoding="utf-8") as handle:
            json.dump(self.records, handle, ensure_ascii=False, indent=2)
        if not quiet:
            print(f"[INFO] 关节 JSON 已保存: {self.save_path} (records={len(self.records)})", flush=True)


class InferenceRunTextLogger:
    def __init__(self, enabled: bool, log_dir: str, meta: dict[str, object]):
        self.enabled = enabled
        self._fp = None
        self.path: str | None = None
        if not enabled:
            return
        log_dir = os.path.abspath(os.path.expanduser(log_dir))
        os.makedirs(log_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.path = os.path.join(log_dir, f"inference_{ts}_{os.getpid()}.txt")
        self._fp = open(self.path, "w", encoding="utf-8")
        self._fp.write("# SO-100 Reach execute 推理运行日志\n")
        for key, value in meta.items():
            self._fp.write(f"{key}={value}\n")
        self._fp.write(
            "# episode_end: target_success_rate=位置; orientation_success_rate=姿态; "
            "success_rate=6D; ever_*=回合内曾进入对应成功区\n---\n"
        )
        self._fp.flush()

    def log_episode(
        self,
        ep: int,
        steps_in_ep: int,
        sim_time_s: float,
        reward_mean: float,
        *,
        target_success_rate: float,
        orientation_success_rate: float,
        success_rate: float,
        ever_target_success_rate: float,
        ever_orientation_success_rate: float,
        ever_success_rate: float,
    ) -> None:
        if not self.enabled or self._fp is None:
            return
        self._fp.write(
            f"episode_end ep={ep} steps_in_ep={steps_in_ep} sim_t={sim_time_s:.4f}s "
            f"reward_mean={reward_mean:.6f} "
            f"target_success_rate={target_success_rate:.6f} "
            f"orientation_success_rate={orientation_success_rate:.6f} "
            f"success_rate={success_rate:.6f} "
            f"ever_target_success_rate={ever_target_success_rate:.6f} "
            f"ever_orientation_success_rate={ever_orientation_success_rate:.6f} "
            f"ever_success_rate={ever_success_rate:.6f}\n"
        )
        self._fp.flush()

    def close(self, total_env_steps: int, episode_ends: int) -> None:
        if not self.enabled or self._fp is None:
            return
        self._fp.write(f"---\nrun_end total_env_steps={total_env_steps} episode_ends={episode_ends}\n")
        self._fp.close()
        self._fp = None
        print(f"[INFO] 推理文本日志已保存: {self.path}", flush=True)


ckpt = resolve_checkpoint(args_cli.checkpoint or resume_path)
stack = create_inference_stack(
    checkpoint=ckpt,
    num_envs=args_cli.num_envs,
    seed=args_cli.seed,
    use_test_npz=not args_cli.use_train_npz,
    enable_contact_sensors=False,
    debug_vis=not args_cli.headless,
)
reach_env = stack["reach_env"]
env = stack["env"]
runner = stack["runner"]
step_dt = stack["step_dt"]

print("[INFO] eval 模式运行中……", flush=True)
print(f"[INFO] checkpoint: {stack['checkpoint']}", flush=True)
print(f"[INFO] workspace NPZ: {reach_env.cfg.workspace_npz_path}", flush=True)

obs, _ = env.reset()
data_logger = InferenceDataLogger(
    reach_env,
    enabled=args_cli.collect_log,
    save_path=args_cli.log_path,
    env_id=args_cli.log_env_id,
    sample_every=args_cli.log_every,
)
if args_cli.collect_log:
    atexit.register(data_logger.save)

run_logger = InferenceRunTextLogger(
    enabled=not args_cli.no_run_log,
    log_dir=args_cli.run_log_dir,
    meta={
        "wall_time": datetime.now().isoformat(timespec="seconds"),
        "checkpoint": stack["checkpoint"],
        "seed": args_cli.seed,
        "num_envs": args_cli.num_envs,
        "step_dt_s": step_dt,
        "collect_joint_json": args_cli.collect_log,
    },
)

step = 0
total_steps = 0
episode_ends = 0
sim_time = 0.0

try:
    while simulation_app.is_running():
        t0 = time.time()
        with torch.inference_mode():
            outputs = runner.agent.act(obs, timestep=0, timesteps=0)
            actions = outputs[-1].get("mean_actions", outputs[0])
            obs, rewards, terminated, truncated, _info = env.step(actions)
        step += 1
        total_steps += 1
        sim_time += step_dt
        data_logger.collect(time_s=sim_time)

        if truncated.any() or terminated.any():
            target_sr = float(reach_env._last_target_success_rate.item())
            orient_sr = float(reach_env._last_orientation_success_rate.item())
            success_sr = float(reach_env._last_success_rate.item())
            ever_tgt = float(reach_env._last_ever_target_success_rate.item())
            ever_ori = float(reach_env._last_ever_orientation_success_rate.item())
            ever_sr = float(reach_env._last_ever_success_rate.item())
            episode_ends += 1
            run_logger.log_episode(
                episode_ends,
                step,
                sim_time,
                float(rewards.mean().item()),
                target_success_rate=target_sr,
                orientation_success_rate=orient_sr,
                success_rate=success_sr,
                ever_target_success_rate=ever_tgt,
                ever_orientation_success_rate=ever_ori,
                ever_success_rate=ever_sr,
            )
            print(
                f"[episode] step={step} reward_mean={rewards.mean().item():.4f} "
                f"target_sr={target_sr:.3f} orient_sr={orient_sr:.3f} success_sr={success_sr:.3f} "
                f"ever_tgt={ever_tgt:.3f} ever_ori={ever_ori:.3f} ever_sr={ever_sr:.3f}",
                flush=True,
            )
            step = 0
            if args_cli.collect_log:
                data_logger.save(quiet=True)

        elapsed = time.time() - t0
        sleep_time = step_dt - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
finally:
    try:
        data_logger.save()
    except Exception as exc:
        print(f"[WARN] 关节 JSON 保存失败: {exc}", flush=True)
    try:
        run_logger.close(total_steps, episode_ends)
    except Exception as exc:
        print(f"[WARN] 推理文本日志 close 失败: {exc}", flush=True)
    try:
        env.close()
    except Exception as exc:
        print(f"[WARN] env.close() 失败: {exc}", flush=True)
    if simulation_app.is_running():
        print("[INFO] 正在关闭 Isaac Sim...", flush=True)
        simulation_app.close()
