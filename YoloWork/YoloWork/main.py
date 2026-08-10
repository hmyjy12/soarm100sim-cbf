from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import torch
from ultralytics import YOLO


EXPECTED_CLASS_NAMES = {
    0: "jpgCat",
    1: "Chiikawa",
    2: "tissue",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run live webcam object detection and tracking "
            "using a trained Ultralytics YOLO model."
        )
    )

    parser.add_argument(
        "--model",
        type=Path,
        default=Path("model/best.pt"),
        help="Path to the trained best.pt checkpoint.",
    )

    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Webcam index. Usually 0 for the default camera.",
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Minimum detection confidence threshold.",
    )

    parser.add_argument(
        "--iou",
        type=float,
        default=0.70,
        help="IoU threshold used for detection filtering.",
    )

    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="YOLO inference image size.",
    )

    parser.add_argument(
        "--tracker",
        type=str,
        default="botsort.yaml",
        choices=[
            "botsort.yaml",
            "bytetrack.yaml",
        ],
        help="Tracking algorithm.",
    )

    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help=(
            "Inference device: auto, cpu, 0, 1, and so on. "
            "Use 0 for the first CUDA GPU."
        ),
    )

    parser.add_argument(
        "--width",
        type=int,
        default=1280,
        help="Requested webcam capture width.",
    )

    parser.add_argument(
        "--height",
        type=int,
        default=720,
        help="Requested webcam capture height.",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the annotated output video.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tracked_output.mp4"),
        help="Output video path when --save is enabled.",
    )

    return parser.parse_args()


def normalize_model_names(
    names: dict[int, str] | list[str],
) -> dict[int, str]:
    if isinstance(names, dict):
        return {
            int(class_id): class_name
            for class_id, class_name in names.items()
        }

    return {
        class_id: class_name
        for class_id, class_name in enumerate(names)
    }


def validate_trained_model(
    model: YOLO,
    model_path: Path,
) -> dict[int, str]:
    model_names = normalize_model_names(model.names)

    if model_names != EXPECTED_CLASS_NAMES:
        raise ValueError(
            "Loaded checkpoint does not match the expected trained "
            "three-class model.\n"
            f"Model path: {model_path}\n"
            f"Expected classes: {EXPECTED_CLASS_NAMES}\n"
            f"Loaded classes: {model_names}\n"
            "Use your trained best.pt file, not the base pretrained "
            "YOLO checkpoint."
        )

    return model_names


def select_device(requested_device: str) -> str | int:
    if requested_device != "auto":
        if requested_device.lower() == "cpu":
            return "cpu"

        try:
            return int(requested_device)
        except ValueError:
            return requested_device

    return 0 if torch.cuda.is_available() else "cpu"


def open_camera(
    camera_index: int,
    width: int,
    height: int,
) -> cv2.VideoCapture:
    # CAP_DSHOW can reduce camera startup delay on Windows.
    if sys.platform.startswith("win"):
        capture = cv2.VideoCapture(
            camera_index,
            cv2.CAP_DSHOW,
        )
    else:
        capture = cv2.VideoCapture(camera_index)

    if not capture.isOpened():
        raise RuntimeError(
            f"Could not open camera index {camera_index}. "
            "Try --camera 1 or check camera permissions."
        )

    capture.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        width,
    )
    capture.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        height,
    )

    # A small buffer can reduce visible webcam latency.
    capture.set(
        cv2.CAP_PROP_BUFFERSIZE,
        1,
    )

    return capture


def create_video_writer(
    output_path: Path,
    fps: float,
    frame_width: int,
    frame_height: int,
) -> cv2.VideoWriter:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    codec = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(output_path),
        codec,
        fps,
        (frame_width, frame_height),
    )

    if not writer.isOpened():
        raise RuntimeError(
            f"Could not create output video: {output_path}"
        )

    return writer


def draw_status(
    frame,
    fps: float,
    device: str | int,
    detection_count: int,
) -> None:
    status = (
        f"FPS: {fps:.1f} | "
        f"Objects: {detection_count} | "
        f"Device: {device}"
    )

    cv2.putText(
        frame,
        status,
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        "Press Q or Esc to quit",
        (15, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )


def draw_detections(
    frame,
    result,
    class_names: dict[int, str],
) -> None:
    if result.boxes is None:
        return

    box_color = (255, 255, 0)
    text_color = (40, 30, 90)
    label_background = (255, 255, 0)

    for box in result.boxes:
        class_id = int(box.cls.item())
        confidence = float(box.conf.item())
        class_name = class_names[class_id]
        label = f"{class_name} {confidence:.2f}"

        x1, y1, x2, y2 = (
            int(value)
            for value in box.xyxy[0].tolist()
        )

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            box_color,
            3,
        )

        (label_width, label_height), baseline = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            2,
        )

        label_y1 = max(
            0,
            y1 - label_height - baseline - 8,
        )
        label_y2 = label_y1 + label_height + baseline + 8

        cv2.rectangle(
            frame,
            (x1, label_y1),
            (x1 + label_width + 10, label_y2),
            label_background,
            -1,
        )
        cv2.putText(
            frame,
            label,
            (x1 + 5, label_y2 - baseline - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            text_color,
            2,
            cv2.LINE_AA,
        )


def main() -> None:
    args = parse_arguments()

    if not args.model.exists():
        raise FileNotFoundError(
            f"Model checkpoint not found: {args.model}"
        )

    if not 0.0 <= args.conf <= 1.0:
        raise ValueError("--conf must be between 0 and 1.")

    if not 0.0 <= args.iou <= 1.0:
        raise ValueError("--iou must be between 0 and 1.")

    device = select_device(args.device)

    print(f"Loading model: {args.model}")
    print(f"Using device: {device}")
    print(f"Tracker: {args.tracker}")

    model = YOLO(str(args.model))
    model_names = validate_trained_model(
        model=model,
        model_path=args.model,
    )
    trained_class_ids = sorted(model_names)

    print("Classes:", model_names)

    capture = open_camera(
        camera_index=args.camera,
        width=args.width,
        height=args.height,
    )

    actual_width = int(
        capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    )
    actual_height = int(
        capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    camera_fps = capture.get(cv2.CAP_PROP_FPS)

    if camera_fps <= 1 or camera_fps > 240:
        camera_fps = 30.0

    writer: cv2.VideoWriter | None = None

    if args.save:
        writer = create_video_writer(
            output_path=args.output,
            fps=camera_fps,
            frame_width=actual_width,
            frame_height=actual_height,
        )

        print(f"Saving output to: {args.output.resolve()}")

    print(
        f"Camera resolution: "
        f"{actual_width}x{actual_height}"
    )
    print("Press Q or Esc to stop.")

    previous_time = time.perf_counter()
    smoothed_fps = 0.0

    try:
        while True:
            success, frame = capture.read()

            if not success or frame is None:
                print(
                    "Failed to read a frame from the webcam."
                )
                break

            results = model.track(
                source=frame,
                persist=True,
                tracker=args.tracker,
                conf=args.conf,
                iou=args.iou,
                imgsz=args.imgsz,
                device=device,
                classes=trained_class_ids,
                verbose=False,
            )

            result = results[0]

            annotated_frame = frame.copy()
            draw_detections(
                frame=annotated_frame,
                result=result,
                class_names=model_names,
            )

            detection_count = (
                len(result.boxes)
                if result.boxes is not None
                else 0
            )

            current_time = time.perf_counter()
            frame_time = current_time - previous_time
            previous_time = current_time

            instantaneous_fps = (
                1.0 / frame_time
                if frame_time > 0
                else 0.0
            )

            # Smooth the FPS value to reduce flickering.
            if smoothed_fps == 0.0:
                smoothed_fps = instantaneous_fps
            else:
                smoothed_fps = (
                    0.90 * smoothed_fps
                    + 0.10 * instantaneous_fps
                )

            draw_status(
                frame=annotated_frame,
                fps=smoothed_fps,
                device=device,
                detection_count=detection_count,
            )

            if writer is not None:
                writer.write(annotated_frame)

            cv2.imshow(
                "YOLO Live Object Tracking",
                annotated_frame,
            )

            pressed_key = cv2.waitKey(1) & 0xFF

            if pressed_key in {
                ord("q"),
                27,
            }:
                break

    finally:
        capture.release()

        if writer is not None:
            writer.release()

        cv2.destroyAllWindows()

        print("Camera and windows closed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as error:
        print(f"\nError: {error}")
        sys.exit(1)
