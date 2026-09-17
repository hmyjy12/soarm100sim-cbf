#!/usr/bin/env python3
"""运行动态障碍批量评测，并把各场景 summary 汇总为一张表。"""

from __future__ import annotations

import argparse
import csv
import json
import shlex
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "mujoco" / "eval_sdf_challenge.py"


def _split_csv(text: str) -> list[str]:
    return [x.strip() for x in str(text).split(",") if x.strip()]


def _split_vec_list(text: str) -> list[str]:
    s = str(text).strip()
    if not s:
        return []
    if ";" in s:
        return [x.strip() for x in s.split(";") if x.strip()]
    return [s]


def _metric(metrics: dict, method: str, key: str) -> float | str:
    value = metrics.get(method, {}).get(key, "")
    if isinstance(value, float):
        return value
    return value


def _fmt_pct(value: float | str) -> str:
    if isinstance(value, float):
        return f"{value * 100:.1f}%"
    return ""


def _fmt_mm(value: float | str) -> str:
    if isinstance(value, float):
        return f"{value * 1000:.1f}"
    return ""


def _scenario_name(motion: str, seed: int, amp: str, period: str, active: float, clear_time: float) -> str:
    amp_tag = amp.replace(",", "_").replace(".", "p").replace("-", "m")
    period_tag = str(period).replace(".", "p")
    name = f"{motion}_seed{seed}_amp{amp_tag}_period{period_tag}"
    if motion in {"random_depart", "random_depart_probe"}:
        name += f"_active{active:g}_clear{clear_time:g}".replace(".", "p")
    return name


def _build_command(args, motion: str, seed: int, amp: str, period: str, out_dir: Path) -> list[str]:
    cmd = [
        sys.executable,
        str(EVAL),
        "--out-dir",
        str(out_dir),
        "--seed",
        str(args.seed),
        "--scan-count",
        str(args.scan_count),
        "--max-challenges",
        str(args.max_challenges),
        "--methods",
        *args.methods,
        "--obstacle-motion",
        motion,
        "--obstacle-motion-amp",
        amp,
        "--obstacle-motion-period",
        str(period),
        "--obstacle-motion-seed",
        str(seed),
        "--workspace-sdf-preset",
        args.workspace_sdf_preset,
    ]
    if motion in {"random_depart", "random_depart_probe"}:
        cmd += [
            "--obstacle-motion-active-time",
            str(args.active_time),
            "--obstacle-motion-clear-offset",
            args.clear_offset,
            "--obstacle-motion-clear-time",
            str(args.clear_time),
        ]
    if motion == "random_depart_probe":
        cmd += [
            "--obstacle-motion-probe-trigger-distance",
            str(args.probe_trigger_distance),
            "--obstacle-motion-probe-offset",
            args.probe_offset,
            "--obstacle-motion-probe-time",
            str(args.probe_time),
        ]
    if str(args.extra_args).strip():
        cmd += shlex.split(str(args.extra_args))
    return cmd


def _read_summary(path: Path, scenario: str, motion: str, seed: int, amp: str, period: str) -> dict:
    summary = json.loads(path.read_text(encoding="utf-8"))
    metrics = summary.get("metrics", {})
    row = {
        "scenario": scenario,
        "motion": motion,
        "obstacle_seed": seed,
        "amp": amp,
        "period_s": period,
        "n": _metric(metrics, "geom", "n"),
        "geom_contact_rate": _metric(metrics, "geom", "contact_rate"),
        "geom_no_contact_rate": 1.0 - float(_metric(metrics, "geom", "contact_rate")),
        "geom_reach_2cm_rate": _metric(metrics, "geom", "reach_2cm_rate"),
        "geom_safe_reach_2cm_rate": _metric(metrics, "geom", "safe_reach_2cm_rate"),
        "geom_mean_best_dist_m": _metric(metrics, "geom", "mean_best_dist_m"),
        "geom_mean_end_dist_m": _metric(metrics, "geom", "mean_end_dist_m"),
        "geom_mean_h_min_m": _metric(metrics, "geom", "mean_h_min_m"),
        "none_contact_rate": _metric(metrics, "none", "contact_rate"),
        "none_safe_reach_2cm_rate": _metric(metrics, "none", "safe_reach_2cm_rate"),
    }
    return row


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _write_md(path: Path, rows: list[dict]) -> None:
    lines = [
        "# 动态障碍批量测试汇总",
        "",
        "这张表是脚本自动从每组 `summary.json` 里摘出来的。`geom` 是当前 CBF，`none` 是不开 CBF 的对照。",
        "",
        "| 场景 | 障碍 seed | 无碰杆率 | 完整成功率 | 到目标 2cm | avg best/mm | avg end/mm | mean h_min/mm |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['motion']} amp={row['amp']} period={row['period_s']} | "
            f"{row['obstacle_seed']} | "
            f"{_fmt_pct(row['geom_no_contact_rate'])} | "
            f"{_fmt_pct(row['geom_safe_reach_2cm_rate'])} | "
            f"{_fmt_pct(row['geom_reach_2cm_rate'])} | "
            f"{_fmt_mm(row['geom_mean_best_dist_m'])} | "
            f"{_fmt_mm(row['geom_mean_end_dist_m'])} | "
            f"{_fmt_mm(row['geom_mean_h_min_m'])} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="批量扫描动态障碍 seed 与运动参数。")
    parser.add_argument("--out-root", default="logs/eval/dynamic_obstacle_sweep")
    parser.add_argument("--seed", type=int, default=42, help="目标采样 seed；比较不同障碍轨迹时应保持固定")
    parser.add_argument("--obstacle-seeds", default="42,43,44,45")
    parser.add_argument("--motions", default="random,random_depart")
    parser.add_argument("--amps", default="0.02,0.02,0.00")
    parser.add_argument("--periods", default="1.0")
    parser.add_argument("--scan-count", type=int, default=64)
    parser.add_argument("--max-challenges", type=int, default=16)
    parser.add_argument("--methods", nargs="+", default=["none", "geom"])
    parser.add_argument("--workspace-sdf-preset", default="dynamic", choices=("static", "dynamic"))
    parser.add_argument("--active-time", type=float, default=2.0)
    parser.add_argument("--clear-offset", default="0.18,0.12,0.00")
    parser.add_argument("--clear-time", type=float, default=2.0)
    parser.add_argument("--probe-trigger-distance", type=float, default=0.06)
    parser.add_argument("--probe-offset", default="-0.07,0.05,-0.15")
    parser.add_argument("--probe-time", type=float, default=1.5)
    parser.add_argument("--extra-args", default="", help="额外透传给 eval_sdf_challenge.py 的参数")
    parser.add_argument("--skip-existing", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    out_root = (ROOT / args.out_root).resolve() if not Path(args.out_root).is_absolute() else Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for motion in _split_csv(args.motions):
        for amp in _split_vec_list(args.amps):
            for period in _split_csv(args.periods):
                for seed_text in _split_csv(args.obstacle_seeds):
                    obstacle_seed = int(seed_text)
                    scenario = _scenario_name(motion, obstacle_seed, amp, period, args.active_time, args.clear_time)
                    out_dir = out_root / scenario
                    summary_path = out_dir / "summary.json"
                    cmd = _build_command(args, motion, obstacle_seed, amp, period, out_dir)
                    if args.dry_run:
                        print(" ".join(shlex.quote(x) for x in cmd))
                        continue
                    if args.skip_existing and summary_path.exists():
                        print(f"[skip] {scenario}")
                    else:
                        print(f"[run] {scenario}", flush=True)
                        subprocess.run(cmd, cwd=ROOT, check=True)
                    if summary_path.exists():
                        rows.append(_read_summary(summary_path, scenario, motion, obstacle_seed, amp, period))

    if not args.dry_run:
        _write_csv(out_root / "sweep_summary.csv", rows)
        _write_md(out_root / "sweep_summary.md", rows)
        print(f"[done] wrote {out_root / 'sweep_summary.csv'}")
        print(f"[done] wrote {out_root / 'sweep_summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
