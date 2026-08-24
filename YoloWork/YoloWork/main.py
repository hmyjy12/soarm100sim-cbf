from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

import cv2
import torch
from ultralytics import YOLO


EXPECTED_CLASS_COUNT = 3


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
        type=str,
        default="0",
        help=(
            "Camera source: index (0), device path (/dev/video6), "
            "or 'orbbec' to auto-pick Orbbec Gemini RGB. "
            "Note: Orbbec /dev/video0 is usually depth, not RGB."
        ),
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

    if len(model_names) != EXPECTED_CLASS_COUNT:
        raise ValueError(
            "Loaded checkpoint does not contain the expected number "
            "of classes.\n"
            f"Model path: {model_path}\n"
            f"Expected class count: {EXPECTED_CLASS_COUNT}\n"
            f"Loaded classes: {model_names}\n"
            "Use a trained three-class YOLO checkpoint."
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


def list_v4l_devices() -> list[tuple[int, str]]:
    root = Path("/sys/class/video4linux")
    if not root.exists():
        return []

    devices: list[tuple[int, str]] = []
    for path in sorted(root.glob("video*")):
        match = re.fullmatch(r"video(\d+)", path.name)
        if match is None:
            continue

        name_path = path / "name"
        name = (
            name_path.read_text(encoding="utf-8", errors="ignore").strip()
            if name_path.exists()
            else "unknown"
        )
        devices.append((int(match.group(1)), name))

    return devices


def v4l_pixel_format(device_index: int) -> str:
    try:
        output = subprocess.check_output(
            [
                "v4l2-ctl",
                "-d",
                f"/dev/video{device_index}",
                "--get-fmt-video",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return ""

    match = re.search(r"Pixel Format:\s+'([^']+)'", output)
    return match.group(1) if match else ""


def find_orbbec_rgb_camera() -> int:
    orbbec_devices = [
        (index, name)
        for index, name in list_v4l_devices()
        if "orbbec" in name.lower()
    ]
    if not orbbec_devices:
        raise RuntimeError(
            "No Orbbec V4L2 device found. "
            "Check USB connection, or use the ROS driver: "
            "ros2/run_orbbec_camera.sh"
        )

    preferred: list[int] = []
    fallback: list[int] = []

    for index, _name in orbbec_devices:
        pixel_format = v4l_pixel_format(index)
        if pixel_format in {"YUYV", "MJPG"}:
            preferred.append(index)
        else:
            fallback.append(index)

    for index in preferred + fallback:
        capture = _open_capture_backend(index)
        if not capture.isOpened():
            capture.release()
            continue

        frame = None
        for _ in range(8):
            success, candidate = capture.read()
            if (
                success
                and candidate is not None
                and candidate.ndim == 3
                and candidate.shape[2] == 3
                and float(candidate.std()) > 1.0
            ):
                frame = candidate
                break

        capture.release()

        if frame is None:
            continue

        # IR/Bayer nodes often appear as odd 400-tall frames under OpenCV.
        if frame.shape[0] == 400:
            continue

        print(
            f"Using Orbbec RGB camera index {index} "
            f"(/dev/video{index})"
        )
        return index

    available = ", ".join(
        f"{index}:{name}" for index, name in orbbec_devices
    )
    raise RuntimeError(
        "Found Orbbec devices but could not open an RGB stream. "
        f"Available: {available}. "
        "Try --camera 6, close OrbbecViewer, and avoid opening "
        "depth nodes (often index 0)."
    )


def resolve_camera_source(camera: str) -> int | str:
    value = camera.strip()
    lowered = value.lower()

    if lowered in {"orbbec", "gemini", "gemini336"}:
        return find_orbbec_rgb_camera()

    if value.startswith("/dev/"):
        return value

    try:
        return int(value)
    except ValueError as error:
        raise ValueError(
            "--camera must be an index, /dev/videoN path, or 'orbbec'."
        ) from error


def _open_capture_backend(camera_source: int | str) -> cv2.VideoCapture:
    if sys.platform.startswith("win"):
        return cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)

    if sys.platform.startswith("linux"):
        capture = cv2.VideoCapture(camera_source, cv2.CAP_V4L2)
        if hasattr(cv2, "CAP_PROP_OPEN_TIMEOUT_MSEC"):
            capture.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 3000)
        if hasattr(cv2, "CAP_PROP_READ_TIMEOUT_MSEC"):
            capture.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 3000)
        return capture

    return cv2.VideoCapture(camera_source)


def open_camera(
    camera_source: int | str,
    width: int,
    height: int,
) -> cv2.VideoCapture:
    capture = _open_capture_backend(camera_source)

    if not capture.isOpened():
        devices = list_v4l_devices()
        hint = ""
        if devices:
            listing = ", ".join(
                f"{index}:{name}" for index, name in devices
            )
            hint = (
                f" Visible V4L2 devices: {listing}. "
                "For Orbbec Gemini RGB use --camera orbbec "
                "(depth is usually index 0; RGB is often index 6)."
            )
        raise RuntimeError(
            f"Could not open camera {camera_source}.{hint}"
        )

    # Prefer uncompressed YUYV for Orbbec UVC RGB when possible.
    capture.set(
        cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(*"YUYV"),
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

    camera_source = resolve_camera_source(args.camera)
    print(f"Camera source: {camera_source}")

    capture = open_camera(
        camera_source=camera_source,
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
