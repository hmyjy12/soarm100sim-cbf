#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path


def _fmt(value: object, digits: int = 4) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "nan"
    if not math.isfinite(number):
        return "nan"
    return f"{number:.{digits}f}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tail policy_reach obstacle CBF telemetry from JSONL logs."
    )
    parser.add_argument(
        "--log",
        default="log/runtime/hardware/policy_reach.jsonl",
        help="policy_reach JSONL log path",
    )
    parser.add_argument(
        "--d-safe-m",
        type=float,
        default=0.050,
        help="safe distance used to report estimated clearance",
    )
    args = parser.parse_args()

    path = Path(args.log).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    proc = subprocess.Popen(
        ["tail", "-n", "0", "-F", str(path)],
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.stdout is not None
    print(f"tailing {path}", flush=True)
    try:
        for line in proc.stdout:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("event") != "control":
                continue
            h_min = row.get("obstacle_h_min_m")
            try:
                clearance = float(h_min) + float(args.d_safe_m)
            except (TypeError, ValueError):
                clearance = float("nan")
            print(
                " ".join(
                    [
                        f"tick={row.get('tick')}",
                        f"h={_fmt(h_min)}m",
                        f"clearance={_fmt(clearance)}m",
                        f"active={row.get('obstacle_cbf_active')}",
                        f"corr={_fmt(row.get('obstacle_cbf_correction_norm'))}",
                        f"feasible={row.get('obstacle_cbf_feasible')}",
                        f"worst={row.get('obstacle_cbf_worst_monitor')}",
                        f"pts={row.get('obstacle_cloud_points')}",
                    ]
                ),
                flush=True,
            )
    except KeyboardInterrupt:
        return 130
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            proc.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main())
