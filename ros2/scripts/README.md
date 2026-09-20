# ROS2 脚本菜单

这个目录下面的脚本，主要是“实验启动按钮”。大部分 `.sh` 自己不写核心算法，它只是帮你把 ROS2、Python 环境、参数、节点一起启动起来。

一句话：先看这里，再决定要不要去读 Python。

## 目录分工

| 路径 | 白话意思 | 现在怎么看 |
|---|---|---|
| `real/` | 真实机械臂实验入口 | 重点看 |
| `calibration/` | 标定脚本预留目录 | 标定时再看 |
| `sim/` | 仿真脚本预留目录 | 仿真时再看 |

## 现在推荐的入口

| 你要干什么 | 跑哪个 |
|---|---|
| 开 Orbbec RGB-D 相机 | `./ros2/scripts/real/run_orbbec_rgbd.sh` |
| 测静态 cup 避障 | `./ros2/scripts/real/run_policy_reach_static_cup.sh` |
| 自己细调 reach 参数 | `./ros2/scripts/real/run_policy_reach.sh` |
| 单独看 cup mask 效果 | `./ros2/scripts/real/run_fixed_yolo_sam_mask.sh` |
| 采机械臂自身/电线附近点云 | `./ros2/scripts/real/run_collect_link_self_occupancy.sh` |

## 为什么还有 `ros2/run_*.sh`

`ros2/` 根目录下面还有一批旧启动脚本，比如：

```text
ros2/run_hardware_controller.sh
ros2/run_orbbec_handeye.sh
ros2/run_vision_grasp.sh
```

它们不是都没用，只是历史上先写在根目录。现在先不搬它们，因为搬了可能会让旧命令、launch 文件、文档里的路径断掉。

后续新增脚本尽量放到：

```text
ros2/scripts/real/
ros2/scripts/sim/
ros2/scripts/calibration/
```

这样新代码会越来越清楚，旧入口慢慢淘汰。

根目录旧脚本的详细处置表见：

```text
ros2/README.md
```

## 看 `.sh` 的方法

读脚本不要一行行硬啃。先找三件事：

1. `source ...setup.bash`：它在准备 ROS2 环境。
2. `ros2 launch` 或 `ros2 run`：它真正启动了哪个节点。
3. `--xxx` 参数：它给节点传了什么配置。

如果一个 `.sh` 里面最后启动的是 `policy_reach_node.py`，那核心逻辑不在 `.sh`，而在那个 Python 节点里。
