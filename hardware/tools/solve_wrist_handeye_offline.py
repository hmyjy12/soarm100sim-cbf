#!/usr/bin/env python3
"""Re-solve a saved wrist hand-eye session with a selected OpenCV method."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np


METHODS = {
    "tsai": cv2.CALIB_HAND_EYE_TSAI,
    "park": cv2.CALIB_HAND_EYE_PARK,
    "horaud": cv2.CALIB_HAND_EYE_HORAUD,
    "andreff": cv2.CALIB_HAND_EYE_ANDREFF,
    "daniilidis": cv2.CALIB_HAND_EYE_DANIILIDIS,
}


def _rotation_angle_deg(rotation: np.ndarray) -> float:
    cosine = float(np.clip((np.trace(rotation) - 1.0) * 0.5, -1.0, 1.0))
    return math.degrees(math.acos(cosine))


def _matrix_dict(transform: np.ndarray) -> dict:
    return {
        "matrix": transform.tolist(),
        "translation_m": transform[:3, 3].tolist(),
        "rotation_matrix": transform[:3, :3].tolist(),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--method", choices=tuple(METHODS), default="park")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-yaml", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    dataset = json.loads(args.samples.read_text())
    samples = dataset.get("samples", [])
    if len(samples) < 12:
        raise ValueError(f"need at least 12 samples, got {len(samples)}")

    gripper_to_base = [np.asarray(s["T_base_gripper"], dtype=np.float64) for s in samples]
    target_to_camera = [np.asarray(s["T_camera_board"], dtype=np.float64) for s in samples]
    rotation, translation = cv2.calibrateHandEye(
        [t[:3, :3] for t in gripper_to_base],
        [t[:3, 3].reshape(3, 1) for t in gripper_to_base],
        [t[:3, :3] for t in target_to_camera],
        [t[:3, 3].reshape(3, 1) for t in target_to_camera],
        method=METHODS[args.method],
    )
    wrist_to_camera = np.eye(4, dtype=np.float64)
    wrist_to_camera[:3, :3] = rotation
    wrist_to_camera[:3, 3] = np.asarray(translation).reshape(3)

    board_poses = [
        base_to_wrist @ wrist_to_camera @ camera_to_board
        for base_to_wrist, camera_to_board in zip(gripper_to_base, target_to_camera)
    ]
    board_translations = np.stack([pose[:3, 3] for pose in board_poses])
    translation_center = np.mean(board_translations, axis=0)
    translation_errors = np.linalg.norm(board_translations - translation_center, axis=1)
    reference_rotation = board_poses[0][:3, :3]
    rotation_errors = np.asarray(
        [_rotation_angle_deg(reference_rotation.T @ pose[:3, :3]) for pose in board_poses]
    )
    reprojection_errors = np.asarray(
        [float(sample["reprojection_rms_px"]) for sample in samples]
    )

    validation = {
        "fixed_board_translation_rms_mm": float(
            np.sqrt(np.mean(translation_errors**2)) * 1000.0
        ),
        "fixed_board_translation_max_mm": float(np.max(translation_errors) * 1000.0),
        "fixed_board_rotation_rms_deg_vs_first": float(
            np.sqrt(np.mean(rotation_errors**2))
        ),
        "fixed_board_rotation_max_deg_vs_first": float(np.max(rotation_errors)),
        "mean_pnp_reprojection_rms_px": float(np.mean(reprojection_errors)),
    }
    result = {
        "schema": "soarm100_real_wrist_handeye_result_v1",
        "method": f"{args.method.capitalize()} (cv2.calibrateHandEye)",
        "source_samples": str(args.samples),
        "opencv_version": cv2.__version__,
        "transform_semantics": (
            "T_gripper_camera maps wrist camera optical coordinates into wrist_roll coordinates"
        ),
        "base_frame": dataset["base_frame"],
        "gripper_frame": dataset["gripper_frame"],
        "camera_frame": dataset["camera_frame"],
        "sample_count": len(samples),
        "pattern_inner_corners": dataset["pattern_inner_corners"],
        "square_size_m": dataset["square_size_m"],
        "T_gripper_camera": _matrix_dict(wrist_to_camera),
        "validation": validation,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_yaml.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n")
    storage = cv2.FileStorage(str(args.output_yaml), cv2.FILE_STORAGE_WRITE)
    if not storage.isOpened():
        raise RuntimeError(f"cannot open YAML output: {args.output_yaml}")
    storage.write("method", args.method.capitalize())
    storage.write("base_frame", result["base_frame"])
    storage.write("gripper_frame", result["gripper_frame"])
    storage.write("camera_frame", result["camera_frame"])
    storage.write("T_gripper_camera", wrist_to_camera)
    storage.write("sample_count", len(samples))
    storage.write("fixed_board_translation_rms_mm", validation["fixed_board_translation_rms_mm"])
    storage.write(
        "fixed_board_rotation_rms_deg",
        validation["fixed_board_rotation_rms_deg_vs_first"],
    )
    storage.release()

    print(f"Method: {result['method']} (OpenCV {cv2.__version__})")
    print(f"Samples: {len(samples)}")
    print(
        "Validation: "
        f"translation={validation['fixed_board_translation_rms_mm']:.3f} mm RMS, "
        f"rotation={validation['fixed_board_rotation_rms_deg_vs_first']:.3f} deg RMS, "
        f"reprojection={validation['mean_pnp_reprojection_rms_px']:.3f} px"
    )
    print(f"JSON: {args.output_json.resolve()}")
    print(f"YAML: {args.output_yaml.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
