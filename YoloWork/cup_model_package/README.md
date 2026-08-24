# 杯子检测 YOLO 模型包

这个包用于检测图片或摄像头画面中的杯子，模型类别只有一个：

```text
0 = cup
```

## 文件说明

```text
best.pt                  训练好的 YOLOv8 杯子检测模型
data.yaml                类别说明文件，记录 0 = cup；推理时不是必须文件
predict_cup.py           图片/文件夹推理脚本
webcam_cup_detect.py     电脑摄像头实时检测脚本
```

## 环境安装

建议使用 Python 3.9 或以上版本。

```bash
pip install ultralytics opencv-python
```

如果在 macOS 上遇到 OpenMP 报错，可以运行前加：

```bash
export KMP_DUPLICATE_LIB_OK=TRUE
```

## 图片或文件夹推理

```bash
python predict_cup.py --model best.pt --source /path/to/images
```

示例：

```bash
python predict_cup.py --model best.pt --source ./test_images
```

推理结果会保存到：

```text
cup_predictions/
```

里面会包含画好检测框的图片，以及 YOLO 格式的检测结果文本。

## 摄像头实时测试

```bash
python webcam_cup_detect.py --model best.pt --camera 0
```

说明：

- `--camera 0` 通常表示电脑默认摄像头
- 如果外接摄像头没有打开，可以尝试 `--camera 1`
- 按 `q` 或 `Esc` 退出窗口

## 推荐推理参数

默认参数已经写在脚本里：

```text
imgsz = 640
conf = 0.25
iou = 0.45
```

如果误检较多，可以提高置信度：

```bash
python predict_cup.py --model best.pt --source ./test_images --conf 0.4
```

如果漏检较多，可以降低置信度：

```bash
python predict_cup.py --model best.pt --source ./test_images --conf 0.15
```

## 机械臂避障说明

这个模型只负责输出杯子的二维检测框，不能单独得到杯子的真实距离。

如果要用于机械臂避障，建议结合以下任意一种距离信息：

- RGB-D 深度相机
- 双目相机
- RealSense 等深度设备
- 已标定相机 + 已知杯子尺寸的距离估计
- 激光雷达、超声波或其他测距传感器

实际避障逻辑通常是：

```text
摄像头图像
-> YOLO 检测 cup 框
-> 获取杯子距离/三维位置
-> 判断是否进入危险区域
-> 机械臂规划绕开或停止
```

## 模型信息

```text
模型类型：YOLOv8 detection
权重文件：best.pt
类别数量：1
类别名称：cup
建议输入尺寸：640
```

## 关于 data.yaml

`data.yaml` 只是为了说明类别编号：

```text
0 = cup
```

同事如果只是推理或接入项目，只需要加载 `best.pt`。  
只有重新训练时，才需要准备自己的训练集路径和新的 `data.yaml`。
