# CBF 避障改进记录

本文是简短阶段记录；接口定义、默认值、验证状态与真机边界见[总说明](避障加动态所有新增修改.md)。

| 阶段 | 后续改动 | 原因与当前结果 |
|---|---|---|
| 约束整理 | CbfConstraint 与统一 stack 接口 | 保持单臂旧调用，同时让约束来源可追踪。 |
| 显式 shared config | 9-point / identity 成为共享默认；17-point 与 task-preserving 改为 opt-in | 防止仿真增强默认悄然改变真机数值行为。 |
| Runtime 配置 | WaypointManager、correction filter、unsafe bypass 都有显式开关 | 默认不启用 waypoint，unsafe bypass 默认关闭。 |
| 动态运动 | MotionSpec / MotionRunner 支持 random、depart、probe | 默认 motion 仍为 none；seed 可复现。 |
| 动态评测 | dynamic challenge 的接触、速度、safe reach 统计 | 动态 evaluator lookahead 默认 2.0；静态 evaluator 默认 0.0。 |
| 批量 sweep | scripts/sweep_dynamic_obstacles.py 扫描 seed、motion、幅度与周期 | 汇总 summary.json 为 CSV/Markdown，输出位于已忽略的 logs/。 |

当前真机仍为单臂静态 cup CBF：9-point、identity、障碍速度 0。waypoint、动态 MotionRunner、sweep 与真机动态速度估计均未接入。

dual-arm、inter-arm constraints、joint QP、observer 与 guided-target telemetry 仍是未合入的 experimental / future work，不属于当前正式能力。

纯 Python、AST、CLI/config 与 seed 静态检查已完成；MuJoCo model-level、GUI/physics、长时间 benchmark 与真机 regression 尚未完成。
