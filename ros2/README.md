# ROS2 目录说明

这里是这个项目连接真实机械臂、相机、视觉、抓取和仿真的地方。

先记住一句话：

```text
ros2/scripts/real/ 是现在推荐看的真机入口。
ros2/run_*.sh 是早期写在根目录的旧入口，先保留兼容。
```

## 新手先看哪里

| 路径 | 用途 |
|---|---|
| `scripts/README.md` | 脚本总菜单 |
| `scripts/real/README.md` | 真机脚本菜单 |
| `soarm100_vision/soarm100_vision/` | ROS2 Python 节点主代码 |
| `soarm100_interfaces/` | ROS2 service/action/message 定义 |
| `so100_plus_description/` | 机器人模型和 RViz 展示 |
| `config/` | launch/config 辅助配置 |

## 根目录旧脚本怎么处理

根目录的 `run_*.sh` 暂时不删，因为它们可能还被文档、旧命令或实验习惯引用。

分类看：

| 文件 | 处置 | 原因 |
|---|---|---|
| `run_hardware_controller.sh` | 保留 | 真机 controller 主入口，会长期持有舵机 |
| `run_hardware_state.sh` | 保留 | 只读关节状态入口，调试常用 |
| `run_single_joint_service.sh` | 保留，高风险 | 单关节真机调试，会碰舵机 |
| `run_orbbec_camera.sh` | 保留，后续可迁移 | 旧 Orbbec RGB-only 入口 |
| `run_wrist_camera.sh` | 保留，后续可迁移 | 腕部相机入口 |
| `run_anygrasp_planner.sh` | 保留，后续可迁移 | AnyGrasp planner 单独入口 |
| `run_vision_grasp.sh` | 保留，但不建议新手先读 | 抓取/仿真/视觉/避障大组合入口，太大 |
| `run_obstacle_grasp.sh` | 保留 wrapper | 只是给 `run_vision_grasp.sh` 加避障默认参数 |
| `run_orbbec_handeye.sh` | 保留，标定专用 | 外置 Orbbec 手眼标定 |
| `run_orbbec_handeye_manual.sh` | 保留，标定专用 | 外置 Orbbec 手动采样全流程 |
| `run_wrist_handeye.sh` | 保留，标定专用 | 腕部相机手眼标定 |
| `run_wrist_handeye_manual.sh` | 保留，标定专用 | 腕部相机手动采样全流程 |
| `run_wrist_handeye_all.sh` | 保留，标定专用 | 腕部手眼一键流程 |
| `run_wrist_handeye_poses.sh` | 保留，标定专用 | 手眼标定姿态序列 |

## 后续优化方向

可以分三步慢慢清：

1. 新脚本都放进 `scripts/real/`、`scripts/sim/`、`scripts/calibration/`。
2. 根目录旧脚本先改成短 wrapper，真正内容搬进分类目录。
3. 等确认没人再用旧路径，再把旧 wrapper 删掉。

这样不会一下子把真实机械臂实验环境搞断。
