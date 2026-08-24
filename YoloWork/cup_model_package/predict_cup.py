#!/usr/bin/env python3
"""Run image or folder inference with a trained YOLO cup model."""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=Path("best.pt"))
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.45)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--output", type=Path, default=Path("cup_predictions"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.model.exists():
        raise SystemExit(f"Model not found: {args.model}")
    if not args.source.exists():
        raise SystemExit(f"Source not found: {args.source}")

    model = YOLO(str(args.model))
    results = model.predict(
        source=str(args.source),
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        save=True,
        save_txt=True,
        save_conf=True,
        project=str(args.output.parent),
        name=args.output.name,
        exist_ok=True,
    )
    print(f"images: {len(results)}")
    print(f"detections: {sum(len(result.boxes) for result in results)}")
    print(f"output: {args.output}")


if __name__ == "__main__":
    main()
