# soarm100sim-cbf

SO-ARM100 的 MuJoCo、视觉、抓取与 SDF-CBF-QP 避障工程。算法和开发说明见
[docs/README.md](docs/README.md)，真机入口见
[ros2/scripts/real/README.md](ros2/scripts/real/README.md)。

## Fresh machine setup

源码、SO-ARM100 自定义模型资产和 Orbbec 源码由 Git submodule 固定。新 Ubuntu 22.04
x86_64 电脑应从带 submodule 的 clone 开始：

```bash
git clone --recurse-submodules -b exp/geom \
  https://github.com/hmyjy12/soarm100sim-cbf.git
cd soarm100sim-cbf
bash scripts/setup/bootstrap_ubuntu22.sh --check
bash scripts/setup/bootstrap_ubuntu22.sh
```

第一次进行 ROS 2 build 或真机部署时，建议先退出未经明确支持的 Conda environment：

```bash
conda deactivate
```

没有安装 Conda 时无需执行这一步。

bootstrap 会同步 submodule，检查 Ubuntu/架构、ROS 2 Humble、核心源码资产、Python 的
`numpy`/`mujoco`、可选 GPU 与设备状态，并在已初始化时更新 `rosdep` 索引。它不会安装
GPU driver/CUDA、自动校准、创建 Conda 环境、执行 `colcon build` 或移动机器人。脚本结束时会
打印当前仓库对应的 Orbbec 293 与主 ROS 2 workspace build/source 命令；完成 build 后可再次运行
`--check`。

硬件标定、串口权限、Orbbec udev 规则、模型 checkpoint 与运行时 target snapshot 都是设备或现场相关
状态，不能由 Git 通用恢复；接入 Gemini 或机械臂、尤其开始运动前，必须为实际设备重新验证这些条件。

### Why this exists

此前源码虽可 fresh clone，但系统环境步骤分散，容易遗漏 ROS、submodule、MuJoCo 或设备条件。该脚本
依据当前 Ubuntu 22.04 / ROS 2 Humble workspace 结构、已有运行文档和 fresh-clone 验证，提供统一的
检查与恢复入口。它已通过 shell 静态检查和本机 `--check` 路径验证；尚未在全新 OS 上完成完整依赖安装、
workspace build 与真机 runtime 回归。
