# YoloWork

基于 Ultralytics YOLO 的实时摄像头目标检测与跟踪程序。程序会加载训练好的 `best.pt` 模型，打开本机摄像头，并在画面中标出识别到的目标。

当前模型识别的类别：

- `jpgCat`
- `Chiikawa`
- `tissue`

## 项目结构

```text
.
├── main.py
├── model/
│   └── best.pt
├── pyproject.toml
├── uv.lock
└── README.md
```

## 环境要求

- Python 3.13 或更高版本
- 摄像头权限
- 已训练好的模型文件：`model/best.pt`

项目依赖主要包括：

- `ultralytics`
- `lap`

## 使用 Anaconda 运行

先创建并进入你的 Conda 环境，然后安装依赖：

```bash
conda create -n yolowork python=3.13
conda activate yolowork
pip install ultralytics lap
```

运行程序：

```bash
python main.py --model model/best.pt
```

## 使用 uv 运行

如果你使用 `uv`，直接同步环境即可：

```bash
uv sync
```

然后运行：

```bash
uv run python main.py --model /best.pt
```

如果模型文件放在本项目的 `model` 目录下，也可以运行：

```bash
uv run python main.py --model model/best.pt
```

## 常用参数

```bash
python main.py --model model/best.pt --camera orbbec --conf 0.25 --iou 0.70
```

参数说明：

- `--model`：模型文件路径，默认是 `model/best.pt`
- `--camera`：摄像头来源。可用编号（如 `0`）、设备路径（如 `/dev/video6`），或 `orbbec` 自动选择 Orbbec Gemini 的 RGB 节点。注意：Orbbec 的 `0` 通常是深度流，不是 RGB
- `--conf`：检测置信度阈值，默认是 `0.25`
- `--iou`：IoU 阈值，默认是 `0.70`
- `--imgsz`：YOLO 推理图片尺寸，默认是 `640`
- `--tracker`：跟踪算法，可选 `botsort.yaml` 或 `bytetrack.yaml`
- `--device`：推理设备，默认 `auto`；可指定 `cpu` 或 GPU 编号，例如 `0`
- `--width`：摄像头采集宽度，默认 `1280`
- `--height`：摄像头采集高度，默认 `720`
- `--save`：保存带标注的视频输出
- `--output`：保存视频路径，默认 `tracked_output.mp4`

保存检测视频示例：

```bash
python main.py --model model/best.pt --save --output tracked_output.mp4
```

## 退出程序

运行后会弹出摄像头窗口。在窗口中按 `Q` 或 `Esc` 退出程序。

## 常见问题

如果摄像头无法打开，可以尝试：

```bash
python main.py --camera 1
```

使用 Orbbec Gemini 深度相机时，不要用默认的 `--camera 0`（那是深度节点）。应使用：

```bash
python main.py --camera orbbec
# 或直接指定 RGB 节点，当前机器上常见为：
python main.py --camera 6
```

也可用项目里的 ROS 路径（更稳定）：`./ros2/scripts/real/run_fixed_yolo_tracking.sh`。

如果提示模型类别不匹配，请确认加载的是本项目训练得到的 `best.pt`，不是 YOLO 官方预训练模型。
