# AnyGrasp Pre-Grasp 设置与执行规范

## 1. 目标

Pre-grasp 是最终抓取姿态之前的安全过渡姿态，用来：

- 提前对齐夹爪方向；
- 避免机械臂从任意方向直接撞向目标；
- 为最后几厘米的低速直线接近留出空间；
- 检查 IK、关节限位、桌面和邻近物体碰撞；
- 为动态目标保留跟踪、预测和制动余量。

AnyGrasp 只生成抓取候选，不直接负责 pre-grasp 轨迹和整臂避障。

---

## 2. AnyGrasp 输出与 approach 方向

常用字段：

```python
grasp.translation       # (3,)
grasp.rotation_matrix   # (3, 3)
grasp.width
grasp.depth
grasp.score
```

通常：

```python
approach_camera = grasp.rotation_matrix[:, 0]
```

表示抓取坐标系的 approach 轴。

注意：

- `[:, 0]` 表示旋转矩阵第一列；
- 该方向通常位于相机坐标系；
- 正负号必须通过可视化确认；
- 未确认前不得直接执行。

---

## 3. 坐标变换

假设 AnyGrasp 输出位于相机坐标系，机器人控制使用 base 坐标系。

位置：

\[
p_g^B = R_{BC}p_g^C + t_{BC}
\]

方向：

\[
a^B = R_{BC}a^C
\]

代码：

```python
grasp_pos_base = (
    R_base_camera @ grasp.translation
    + t_base_camera
)

approach_base = (
    R_base_camera @ grasp.rotation_matrix[:, 0]
)
approach_base /= np.linalg.norm(approach_base) + 1e-12
```

方向向量只乘旋转，不加平移。

---

## 4. Approach 方向确认

在 viewer 中画箭头：

```python
arrow_start = grasp_pos_base
arrow_end = grasp_pos_base + 0.08 * approach_base
```

检查箭头是否表示夹爪从外部指向物体的进入方向。

若方向反了：

```python
approach_base = -approach_base
```

必须同时确认：

- approach 轴；
- 手指开合轴；
- TCP 原点；
- 夹爪前端位置。

---

## 5. 静态目标的 Pre-Grasp

设：

- 最终抓取位置为 \(p_g\)；
- 接近方向为 \(a\)；
- pre-grasp 距离为 \(L_{pre}\)。

若 \(a\) 从 pre-grasp 指向 final grasp：

\[
p_{pre} = p_g - L_{pre}a
\]

代码：

```python
pregrasp_pos = (
    grasp_pos_base
    - pregrasp_distance * approach_base
)
```

推荐初始值：

```text
pregrasp_distance = 0.05–0.06 m
```

常用可调范围：

```text
0.04–0.08 m
```

---

## 6. Pre-Grasp 姿态

第一版推荐：

```python
pregrasp_rotation = grasp_rotation_base
```

即 pre-grasp 与 final grasp 保持相同姿态，只改变位置。

这样最后阶段只需要沿 approach 轴平移，不需要同时大幅旋转手腕。

---

## 7. AnyGrasp 坐标系与真实 TCP

AnyGrasp 的抓取坐标系通常不等于机器人 TCP。

最终变换：

\[
{}^BT_E
=
{}^BT_C
{}^CT_G
{}^GT_E
\]

其中：

- \(C\)：相机坐标系；
- \(G\)：AnyGrasp 抓取坐标系；
- \(E\)：机器人 TCP；
- \(T_G^E\)：固定 TCP 对齐变换。

需要单独标定：

- TCP 原点；
- 指尖中心；
- approach 轴；
- 手指开合轴；
- TCP 到夹爪前端的距离。

---

## 8. 候选过滤顺序

不要直接执行 top-1。

建议保留：

```text
top-K = 20–50
```

然后依次检查：

1. AnyGrasp score；
2. 候选是否属于目标 mask；
3. 夹爪宽度是否可执行；
4. final grasp IK；
5. pre-grasp IK；
6. 关节限位；
7. 奇异位形或 manipulability；
8. final grasp 夹爪碰撞；
9. pre-grasp 夹爪碰撞；
10. approach line 碰撞；
11. 整条机械臂碰撞；
12. 桌面 clearance；
13. 关节移动量；
14. 最终综合排序。

只有 pre-grasp 和 final grasp 都可达的候选才能执行。

---

## 9. Approach Line 检查

从 pre-grasp 到 final grasp：

\[
p(s)
=
p_{pre}
+
s(p_g-p_{pre}),\quad s\in[0,1]
\]

建议：

```text
采样间隔：2–5 mm
采样数量：10–30
```

每个采样位置检查：

- 夹爪手掌是否碰撞；
- 手指外侧是否碰撞；
- 是否撞桌面；
- 是否撞邻近物体；
- 前臂和手腕是否安全；
- IK 是否连续；
- 关节是否跳变。

必须使用完整局部场景，而不是只使用目标物体点云。

---

## 10. 静态抓取状态机

```text
DETECT
  ↓
FILTER_CANDIDATES
  ↓
MOVE_TO_PREGRASP
  ↓
RECHECK
  ↓
FINAL_APPROACH
  ↓
CLOSE
  ↓
RETREAT / LIFT
  ↓
VERIFY
```

### MOVE_TO_PREGRASP

- 可使用 PPO、IK 控制器或轨迹规划；
- 整臂 SDF-CBF-QP 持续工作；
- 夹爪保持打开。

### RECHECK

到达 pre-grasp 后重新读取视觉，确认：

- 目标是否移动；
- 抓取姿态是否仍有效；
- final grasp 是否仍可达；
- approach corridor 是否仍安全。

### FINAL_APPROACH

- 使用低速 Cartesian servo；
- 尽量保持姿态固定；
- 沿 approach 轴直线接近；
- 继续约束前臂、手腕和夹爪外部几何；
- 不允许突然切换到完全不同的 grasp。

### CLOSE

- 到达抓取深度后再闭合；
- 低速闭合；
- 等待接触或位置稳定。

### RETREAT / LIFT

- 先沿 approach 反方向退出少量距离；
- 再执行抬升；
- 抓住后将目标加入 attached-object 几何。

---

## 11. Final Approach 控制

最后几厘米建议使用 Cartesian servo，而不是自由形式 PPO。

位置误差：

\[
e_p = p_{target}-p_{ee}
\]

速度参考：

\[
v_{ee}=K_pe_p
\]

推荐初始速度：

```text
0.01–0.03 m/s
```

上限可根据系统能力调到：

```text
0.05 m/s
```

通过 Jacobian 或 QP 转为关节速度，再经过 CBF-QP 安全过滤。

---

## 12. 动态目标仍需要 Pre-Grasp

动态目标不能使用“一次检测后固定不动”的 pre-grasp。

应使用：

```text
moving pre-grasp
或
tracking standoff
```

当前抓取姿态：

\[
p_g(t), R_g(t)
\]

approach 方向：

\[
a(t)=R_g(t)[:,0]
\]

动态 pre-grasp：

\[
p_{pre}(t)
=
p_g(t)-L_{pre}a(t)
\]

机器人持续跟随更新后的 pre-grasp，而不是到达旧位置后等待。

---

## 13. 动态目标延迟补偿

总延迟：

\[
	au_{total}
=
	au_{camera}
+
	au_{pointcloud}
+
	au_{detector}
+
	au_{tracker}
+
	au_{filter}
+
	au_{controller}
+
	au_{robot}
\]

若目标速度估计为 \(v_g\)：

\[
p_g(t+	au)
=
p_g(t)+v_g	au
\]

预测后的 pre-grasp：

\[
p_{pre,pred}
=
p_g(t+	au)
-
L_{pre}a(t+	au)
\]

动态目标应跟踪预计执行时刻的位置，而不是只追逐当前测量值。

---

## 14. 动态抓取状态机

```text
DETECT
  ↓
TRACK_STANDOFF
  ↓
SYNCHRONIZE
  ↓
COMMIT_APPROACH
  ↓
OCCLUSION_COMMIT
  ↓
CLOSE
  ↓
LIFT
```

### TRACK_STANDOFF

- 使用 tracking.tar 跟踪同一个 grasp；
- 使用 One Euro 等滤波器减少抖动；
- 持续更新 moving pre-grasp；
- 保持安全距离。

### SYNCHRONIZE

只有同时满足以下条件才进入 final approach：

- 位置误差足够小；
- 姿态误差足够小；
- 机器人与目标相对速度足够小；
- tracking confidence 足够高；
- approach corridor 安全。

### COMMIT_APPROACH

- 保持同一个 grasp identity；
- 只允许小幅连续修正；
- 不允许大幅姿态跳变；
- 可以使用目标速度前馈；
- 限制最大追踪速度。

### OCCLUSION_COMMIT

夹爪接近目标后可能遮挡相机。

此时使用：

```text
最后可靠抓取姿态
+ 目标速度预测
+ 短时间模型传播
+ 低速执行
```

不能在严重遮挡后继续完全相信新的视觉输出。

---

## 15. 动态 Pre-Grasp 距离

动态目标的 pre-grasp 距离可参考：

\[
L_{pre}
\geq
v_{relative}	au_{total}
+
d_{brake}
+
d_{margin}
\]

含义：

- 目标越快，pre-grasp 距离越大；
- 系统延迟越高，距离越大；
- 机器人制动越慢，距离越大。

建议分两级：

```text
tracking standoff = 0.06–0.10 m
commit standoff   = 0.02–0.04 m
```

---

## 16. 动态目标异常处理

以下情况应退出 final approach：

- grasp 位置突然跳变；
- 抓取旋转突然跳变；
- grasp identity 切换；
- tracking confidence 过低；
- 目标速度超过机器人能力；
- 目标离开工作空间；
- 点云或跟踪结果超时；
- approach corridor 被阻挡；
- IK 不连续；
- CBF 持续大幅修改 nominal action。

推荐第一轮阈值：

```text
位置跳变：20–30 mm
旋转跳变：15–25°
连续丢失：2–5 帧
```

---

## 17. Pre-Grasp 与其他模块的分工

```text
AnyGrasp
负责：生成 final grasp 候选

Pre-grasp planner
负责：生成安全进入起点

Approach-line checker
负责：验证最后直线路径

PPO / IK / trajectory planner
负责：移动到 pre-grasp

Cartesian servo
负责：最后几厘米

SDF-CBF-QP
负责：整臂实时安全过滤
```

AnyGrasp 的 obstacle-aware 和 collision detection 不等于整条机械臂和整条 approach path 都安全。

---

## 18. 推荐初始参数

```text
静态 pregrasp_distance:
0.05–0.06 m

final approach speed:
0.01–0.03 m/s

approach sample spacing:
0.002–0.005 m

top-K:
20–50

动态 tracking standoff:
0.06–0.10 m

动态 commit standoff:
0.02–0.04 m

位置跳变拒绝阈值:
0.02–0.03 m

旋转跳变拒绝阈值:
15–25°
```

---

## 19. 禁止事项

1. 不得直接执行 AnyGrasp top-1。
2. 不得未经可视化确认 approach 轴方向。
3. 不得忽略 AnyGrasp 坐标系与真实 TCP 的固定变换。
4. 不得只检查 final grasp IK。
5. 不得跳过 approach line 碰撞检查。
6. 不得在最后几厘米继续大幅旋转手腕。
7. 不得在动态目标上长期使用一次检测得到的固定 pre-grasp。
8. 不得允许 tracker 每帧切换 grasp identity。
9. 不得在严重遮挡后继续完全相信视觉更新。
10. 不得把 AnyGrasp 碰撞过滤当作整臂避障。
11. 不得只向 AnyGrasp 输入目标点云并删除周围场景。
12. 不得让低置信度视觉更新产生大幅动作。

---

## 20. 验收标准

### 静态目标

- approach 方向可视化正确；
- pre-grasp 位于 final grasp 外侧；
- pre-grasp 和 final grasp 均存在连续 IK；
- approach line 无碰撞；
- 夹爪姿态无突然翻转；
- final approach 速度受限；
- 抓取后可安全退出和抬升。

### 动态目标

- moving pre-grasp 能连续跟随目标；
- 不追逐明显过期的位置；
- 相对速度降低后才进入 final approach；
- tracker 丢失时能够停止或重新检测；
- 遮挡后只进行有限时间预测；
- 抓取姿态不在不同候选间来回跳变；
- 超出捕获能力时能够 abort。
