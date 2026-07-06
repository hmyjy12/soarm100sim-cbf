#!/usr/bin/env python3
"""SO-100 Plus 工作空间采样入口。

实现代码在 `sample/` 子包：
  sample/constants.py     关节名、home 位姿等常量
  sample/pipeline.py        JSON 流、NPZ 导出、train/test 划分
  sample/robot_cfg.py       Isaac Lab 机器人/场景配置
  sample/isaac_sampler.py   关节随机采样 + FK 预筛 + Isaac 在线验证

================================================================================
启动方式
================================================================================

0) 前置：将 URDF 转为 USD（首次需要）
   cd ~/isaac_lab/isaac_ws/IsaacLab
   ./isaaclab.sh -p scripts/tools/convert_urdf.py \\
     ~/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/so100_plus.urdf \\
     ~/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/assets/so100_plus.usd \\
     --headless --fix-base

1) 默认：headless 采样 + JSON/NPZ 导出 + train/test 划分
   cd ~/isaac_lab/isaac_ws/IsaacLab
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/sample.py --headless

2) 仅采样，不划分
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/sample.py --headless --no-enable-split

3) 仅对已有 merged NPZ 做 train/test 划分（不启动 Isaac Sim）
   python3 ~/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/sample.py \\
     --no-enable-sample --enable-split

4) 小规模试跑
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/sample.py --headless \\
     --num-samples 200 --num-envs 16

5) 续跑（从 stream manifest 恢复）
   ./isaaclab.sh -p ../rl_code/soarm100sim/rl/sample.py --headless --resume

================================================================================
输出路径（默认，可在下方 DEFAULTS 或 CLI 中修改）
================================================================================
  datasets/workspace_joint_dataset.json   # 每条含 arm、tcp（捏合中心）、gripper_link
  datasets/workspace_joint_dataset_stream/
  workspace_cache/workspace_tcp_merged.npz  # tcp / tcp_quat_wxyz 为捏合中心
  workspace_cache/workspace_tcp_merged_train.npz
  workspace_cache/workspace_tcp_merged_test.npz
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# =============================================================================
# 用户常改默认配置（CLI 可覆盖）
# =============================================================================

REPO_ROOT = Path(__file__).resolve().parents[1]
RL_ROOT = Path(__file__).resolve().parent

if str(RL_ROOT) not in sys.path:
    sys.path.insert(0, str(RL_ROOT))

DEFAULTS = {
    # --- 流程开关 ---
    "enable_sample": True,
    "enable_split": True,
    # --- 输出路径 ---
    "output_json": str(RL_ROOT / "datasets" / "workspace_joint_dataset.json"),
    "merged_npz": str(RL_ROOT / "workspace_cache" / "workspace_tcp_merged.npz"),
    "train_npz": str(RL_ROOT / "workspace_cache" / "workspace_tcp_merged_train.npz"),
    "test_npz": str(RL_ROOT / "workspace_cache" / "workspace_tcp_merged_test.npz"),
    # --- 采样输出格式 ---
    "save_formats": "json,npz",
    "merge_json_at_end": True,
    "resume": False,
    "flush_every": 1000,
    # --- 机器人资产 ---
    "urdf_path": str(
        REPO_ROOT / "SO-ARM100" / "Simulation" / "SO100" / "mujoco" / "so100_plus.urdf"
    ),
    "usd_path": str(RL_ROOT / "assets" / "so100_plus.usd"),
    "usd_robot_prim_path": "",
    # --- 采样规模 ---
    "num_samples": 20000,
    "num_envs": 64,
    "seed": 42,
    # --- 仿真 ---
    "dt": 1.0 / 60.0,
    "settle_steps": 3,
    "disable_self_collision": False,
    # --- 关节/奇异性筛选 ---
    "joint_margin_ratio": 0.05,
    "sigma_min_threshold": 0.02,
    "cond_max_threshold": 100.0,
    "manipulability_threshold": 0.003,
    "max_attempt_factor": 1200,
    "collision_force_threshold": 2.0,
    # --- 工作空间（相对 base 的 TCP 位置，单位 m）---
    "x_min": 0.08,
    "x_max": 0.45,
    "y_min": -0.25,
    "y_max": 0.25,
    "z_min": 0.05,
    "z_max": 0.40,
    # --- NPZ 导出（从 JSON 字段 `tcp` 读取；旧版 end_effector 仍兼容）---
    "skip_collision": False,
    "tcp_offset_local": (0.0, 0.0, 0.0),  # 仅旧 JSON 无 tcp 字段时生效
    "max_npz_samples": 0,
    # --- split ---
    "train_ratio": 0.8,
    "split_seed": 42,
    # --- 其他 ---
    "orientation_format": "quat",
    "show_progress": True,
    "progress_refresh_sec": 1.0,
}


def _build_parser(*, with_isaac: bool = True) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SO-100 Plus workspace sampling pipeline")
    parser.add_argument(
        "--enable-sample",
        action=argparse.BooleanOptionalAction,
        default=DEFAULTS["enable_sample"],
        help="是否执行 Isaac 在线采样",
    )
    parser.add_argument(
        "--enable-split",
        action=argparse.BooleanOptionalAction,
        default=DEFAULTS["enable_split"],
        help="是否对 merged NPZ 划分 train/test",
    )
    parser.add_argument("--output-json", type=str, default=DEFAULTS["output_json"])
    parser.add_argument("--merged-npz", type=str, default=DEFAULTS["merged_npz"])
    parser.add_argument("--train-npz", type=str, default=DEFAULTS["train_npz"])
    parser.add_argument("--test-npz", type=str, default=DEFAULTS["test_npz"])
    parser.add_argument(
        "--save-formats",
        type=str,
        default=DEFAULTS["save_formats"],
        help="采样输出格式，逗号分隔：json,npz",
    )
    parser.add_argument("--flush-every", type=int, default=DEFAULTS["flush_every"])
    parser.add_argument("--resume", action="store_true", default=DEFAULTS["resume"])
    parser.add_argument(
        "--merge-json-at-end",
        action=argparse.BooleanOptionalAction,
        default=DEFAULTS["merge_json_at_end"],
    )
    parser.add_argument("--urdf-path", type=str, default=DEFAULTS["urdf_path"])
    parser.add_argument("--usd-path", type=str, default=DEFAULTS["usd_path"])
    parser.add_argument("--usd-robot-prim-path", type=str, default=DEFAULTS["usd_robot_prim_path"])
    parser.add_argument("--num-samples", type=int, default=DEFAULTS["num_samples"])
    parser.add_argument("--num-envs", type=int, default=DEFAULTS["num_envs"])
    parser.add_argument("--seed", type=int, default=DEFAULTS["seed"])
    parser.add_argument("--dt", type=float, default=DEFAULTS["dt"])
    parser.add_argument("--settle-steps", type=int, default=DEFAULTS["settle_steps"])
    parser.add_argument("--disable-self-collision", action="store_true", default=DEFAULTS["disable_self_collision"])
    parser.add_argument("--joint-margin-ratio", type=float, default=DEFAULTS["joint_margin_ratio"])
    parser.add_argument("--sigma-min-threshold", type=float, default=DEFAULTS["sigma_min_threshold"])
    parser.add_argument("--cond-max-threshold", type=float, default=DEFAULTS["cond_max_threshold"])
    parser.add_argument("--manipulability-threshold", type=float, default=DEFAULTS["manipulability_threshold"])
    parser.add_argument("--max-attempt-factor", type=int, default=DEFAULTS["max_attempt_factor"])
    parser.add_argument("--collision-force-threshold", type=float, default=DEFAULTS["collision_force_threshold"])
    parser.add_argument("--x-min", type=float, default=DEFAULTS["x_min"])
    parser.add_argument("--x-max", type=float, default=DEFAULTS["x_max"])
    parser.add_argument("--y-min", type=float, default=DEFAULTS["y_min"])
    parser.add_argument("--y-max", type=float, default=DEFAULTS["y_max"])
    parser.add_argument("--z-min", type=float, default=DEFAULTS["z_min"])
    parser.add_argument("--z-max", type=float, default=DEFAULTS["z_max"])
    parser.add_argument("--skip-collision", action="store_true", default=DEFAULTS["skip_collision"])
    parser.add_argument(
        "--tcp-offset-local",
        type=float,
        nargs=3,
        default=DEFAULTS["tcp_offset_local"],
        metavar=("X", "Y", "Z"),
    )
    parser.add_argument("--max-npz-samples", type=int, default=DEFAULTS["max_npz_samples"])
    parser.add_argument("--train-ratio", type=float, default=DEFAULTS["train_ratio"])
    parser.add_argument("--split-seed", type=int, default=DEFAULTS["split_seed"])
    parser.add_argument(
        "--orientation-format",
        type=str,
        choices=["quat", "rpy", "both"],
        default=DEFAULTS["orientation_format"],
    )
    parser.add_argument(
        "--show-progress",
        action=argparse.BooleanOptionalAction,
        default=DEFAULTS["show_progress"],
    )
    parser.add_argument("--progress-refresh-sec", type=float, default=DEFAULTS["progress_refresh_sec"])
    if with_isaac:
        from isaaclab.app import AppLauncher

        AppLauncher.add_app_launcher_args(parser)
        parser.set_defaults(headless=True)
    return parser


def _parse_args() -> argparse.Namespace:
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument(
        "--enable-sample",
        action=argparse.BooleanOptionalAction,
        default=DEFAULTS["enable_sample"],
    )
    pre_args, remaining = pre_parser.parse_known_args()
    parser = _build_parser(with_isaac=pre_args.enable_sample)
    args, hydra_args = parser.parse_known_args(remaining)
    args.enable_sample = pre_args.enable_sample
    sys.argv = [sys.argv[0]] + hydra_args
    return args


def _prepare_runtime(args: argparse.Namespace):
    from sample.pipeline import (
        ChunkedDataSink,
        PipelinePaths,
        export_npz_from_sample_outputs,
        parse_save_formats,
        split_npz,
        validate_pipeline_config,
    )

    save_formats = parse_save_formats(args.save_formats) if args.enable_sample else []
    paths = PipelinePaths(
        output_json=os.path.abspath(args.output_json),
        merged_npz=os.path.abspath(args.merged_npz),
        train_npz=os.path.abspath(args.train_npz),
        test_npz=os.path.abspath(args.test_npz),
    )
    validate_pipeline_config(
        enable_sample=args.enable_sample,
        enable_split=args.enable_split,
        save_formats=save_formats,
        paths=paths,
    )
    return paths, save_formats, export_npz_from_sample_outputs, split_npz, ChunkedDataSink


def _run_split_only(args: argparse.Namespace, split_npz, paths) -> None:
    split_npz(
        paths.merged_npz,
        paths.train_npz,
        paths.test_npz,
        train_ratio=args.train_ratio,
        seed=args.split_seed,
    )


def _run_sample_pipeline(args: argparse.Namespace, app) -> None:
    paths, save_formats, export_npz_from_sample_outputs, split_npz, ChunkedDataSink = _prepare_runtime(args)
    sink = ChunkedDataSink(
        paths=paths,
        save_formats=save_formats,
        flush_every=args.flush_every,
        resume=args.resume,
        merge_json_at_end=args.merge_json_at_end,
    )

    from sample.isaac_sampler import run_isaac_sampling

    run_isaac_sampling(args, paths, sink)
    sink.finalize()

    if "npz" in save_formats:
        export_npz_from_sample_outputs(
            paths,
            skip_collision=args.skip_collision,
            tcp_offset_local=tuple(args.tcp_offset_local),
            max_samples=args.max_npz_samples,
        )

    if args.enable_split:
        _run_split_only(args, split_npz, paths)

    print("[DONE] sample pipeline finished.")
    print(f"  json : {paths.output_json}")
    print(f"  npz  : {paths.merged_npz}")
    if args.enable_split:
        print(f"  train: {paths.train_npz}")
        print(f"  test : {paths.test_npz}")


def _validate_sample_assets(args: argparse.Namespace) -> None:
    if not os.path.isfile(args.urdf_path):
        raise FileNotFoundError(f"URDF 不存在: {args.urdf_path}")
    if not os.path.isfile(args.usd_path):
        raise FileNotFoundError(
            f"USD 不存在: {args.usd_path}\n"
            "请先转换 URDF（见 sample.py 顶部「0) 前置」），示例：\n"
            "  cd ~/isaac_lab/isaac_ws/IsaacLab\n"
            "  ./isaaclab.sh -p scripts/tools/convert_urdf.py \\\n"
            f"    {args.urdf_path} \\\n"
            f"    {args.usd_path} \\\n"
            "    --headless --fix-base"
        )


def main() -> None:
    args = _parse_args()

    paths, save_formats, export_npz_from_sample_outputs, split_npz, _ChunkedDataSink = _prepare_runtime(args)

    if args.enable_sample:
        _validate_sample_assets(args)
        from isaaclab.app import AppLauncher

        app = AppLauncher(args).app
        try:
            _run_sample_pipeline(args, app)
        except Exception:
            import traceback

            traceback.print_exc()
            raise
        finally:
            if app.is_running():
                print("[INFO] 采样已完成，正在关闭 Isaac Sim...", flush=True)
                app.close()
                print("[INFO] Isaac Sim 已关闭。", flush=True)
        return

    if args.enable_split:
        _run_split_only(args, split_npz, paths)
        print("[DONE] split-only finished.")
        print(f"  train: {paths.train_npz}")
        print(f"  test : {paths.test_npz}")


if __name__ == "__main__":
    main()
