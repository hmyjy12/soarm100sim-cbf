# SO-ARM100 项目文档

本目录保存项目自己维护的 Markdown。第三方仓库文档和与 JSON/CSV 配套的自动
评估报告保留在各自目录，不纳入此处。

## 项目架构

- [代码结构与 Sim2Real 说明](project/代码结构与Sim2Real说明.md)：目录职责、
  sim/2real 数据流、共享边界和当前完成状态。
- [新手目录地图](project/新手目录地图.md)：用白话说明每个一层目录是什么、
  调实机避障应该先看哪条代码线。
- [脚本与代码索引](project/脚本与代码索引.md)：按用途解释 `.sh` 入口、
  ROS2 节点、硬件工具、MuJoCo 和 RL 文件。
- [项目清理审计](project/项目清理审计.md)：哪些内容必须保留、可以归档、可以
  重新生成，以及建议的后续清理步骤。
- [日志目录说明](project/日志目录说明.md)：统一日志根目录及三个子目录的来源。

## 真机与 2Real

- [2Real 工作记录](real/2real工作记录.md)：真机开发过程、标定、抓取和避障记录。
- [2Real 部署指南](real/2Real部署指南.md)：部署和运行说明。

## 算法

- [SDF-CBF-QP 避障算法](algorithms/避障算法.md)
- [SDF-CBF-QP 避障与动态障碍完整说明](development/SDF-CBF-QP避障与动态障碍完整说明.md)
- [AnyGrasp Pre-Grasp 规范](algorithms/anygrasp_pregrasp_spec.md)
- [tar&ori Reach 迁移说明](algorithms/tarori迁移algo.md)

## 开发历史

- [硬件工具说明](development/hardware工具说明.md)
- [硬件开发日志](development/hardware开发日志.md)
- [MuJoCo 实验记录](development/mujoco实验记录.md)
- [MuJoCo 开发日志](development/mujoco开发日志.md)
- [RL 实验记录](development/rl实验记录.md)
- [ROS2 结构说明](development/ros2结构说明.md)
- [ROS2 代码说明](development/ros2代码说明.md)
- [ROS2 开发日志](development/ros2开发日志.md)
- [ROS2 开发目标](development/ros2开发目标.md)

## 不移动的 Markdown

以下文档必须保留原位：

- `SO-ARM100/`、`anygrasp_sdk/`、`lerobot-main/`、`third_party/`、
  `YoloWork/` 中的上游 README、CHANGELOG、LICENSE 和模板；
- `log/runtime/eval/**/summary.md`、`rl/logs/eval/*.md` 等与对应实验数据绑定的报告；
- 构建目录中由工具生成的 Markdown。这些目录本身应被忽略或重建，而不是整理
  进项目文档。

新增第一方设计文档时，请直接放入本目录对应分类，不再放到仓库根目录或源码
目录中。

## 变更记录要求

对于影响算法、控制、标定、数据流或运行行为的改动，应在对应 README 或技术文档中
同步记录：为什么改、参考依据、改动内容、测试方法、测试结果及已知限制。
