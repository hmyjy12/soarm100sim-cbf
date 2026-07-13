# SO-ARM100 全身避障实现规范

## 1. 目标

为 SO-ARM100 实现一个实时全身避障模块。

机器人几何使用多个 capsule 表示。避障模块接收上层策略或控制器给出的 nominal joint velocity，并用 CBF-QP 修正为安全速度。

系统必须同时支持三种障碍物来源：

1. 仿真中的真实 collision mesh；
2. 仿真生成的理想点云；
3. 深度相机生成的视觉点云。

三种来源必须共用同一个 CBF-QP 控制器，只允许替换“距离查询后端”。

---

## 2. 总体架构

```text
Cartesian policy / PPO / IK
            ↓
     nominal joint velocity
            ↓
RobotGeometry
- capsule world pose
- point Jacobian
            ↓
ObstacleDistanceBackend
- SimMeshBackend
- IdealPointCloudBackend
- VisualPointCloudBackend
            ↓
DistanceContact
- distance
- axis point
- obstacle point
- normal
- confidence
            ↓
ContactManager
- 激活阈值
- 滞回
- contact 数量限制
            ↓
CBF-QP
            ↓
safe joint velocity
            ↓
q_cmd = q_measured + dt * qd_safe
```

控制器不能依赖障碍物来源。它只能读取统一的 `DistanceContact`。

---

## 3. 机器人几何

每个 capsule 由以下参数定义：

```python
@dataclass(frozen=True)
class CapsuleSpec:
    capsule_id: str
    link_name: str
    a_local: np.ndarray   # shape (3,), meter
    b_local: np.ndarray   # shape (3,), meter
    radius: float         # meter
```

其中：

- `a_local` 和 `b_local` 是 capsule 轴线端点；
- 坐标表达在所属 link 的局部坐标系；
- 半径单位为 meter；
- 所有关节角单位为 radian。

运行时通过 FK 得到：

\[
a_j^w(q), \quad b_j^w(q)
\]

---

## 4. 统一距离查询接口

```python
@dataclass(frozen=True)
class WorldCapsule:
    capsule_id: str
    link_name: str
    a_world: np.ndarray
    b_world: np.ndarray
    radius: float


@dataclass(frozen=True)
class DistanceContact:
    capsule_id: str
    link_name: str
    obstacle_id: str

    # capsule 表面到障碍物表面的距离
    distance: float

    # capsule 中心轴线上对应的最近点
    axis_point_world: np.ndarray

    # 障碍物表面的最近点
    obstacle_point_world: np.ndarray

    # 从障碍物指向机器人的单位法向
    normal_world: np.ndarray

    feature_id: int | str | None
    confidence: float
    timestamp: float


class ObstacleDistanceBackend(Protocol):
    def update(self, observation) -> None:
        ...

    def query(
        self,
        capsules_world: list[WorldCapsule],
        activation_distance: float,
        max_contacts_per_capsule: int,
    ) -> list[DistanceContact]:
        ...
```

必须保证：

\[
n=
\frac{c-p}{\|c-p\|}
\]

其中：

- \(c\) 为 capsule 轴线上的最近点；
- \(p\) 为障碍物上的最近点；
- \(n\) 从障碍物指向机器人。

---

## 5. 开发阶段

## 5.1 阶段 1：仿真 collision mesh

目的：验证控制和几何计算，不引入视觉误差。

输入：

- 当前关节位置；
- 仿真中的 collision mesh；
- 障碍物世界位姿。

实现：

- 机器人侧使用 capsule；
- 障碍物侧使用简化 collision mesh；
- 使用 FCL、hpp-fcl、PhysX scene query 或等价 BVH 距离查询；
- 静态 mesh 的 BVH 只允许构建一次；
- 动态刚体每帧只更新 transform；
- 不允许将视觉高精度 mesh 直接作为 collision mesh。

必须返回：

- 最小表面距离；
- capsule 最近点；
- 障碍物最近点；
- 法向。

大物体不需要逐边或逐三角形遍历。必须使用 BVH broad phase 和 narrow phase。

---

## 5.2 阶段 2：理想点云

从仿真 mesh 或无噪声深度生成点云，并使用最终的 point-to-capsule 距离算法。

目的：

- 验证点云距离后端；
- 比较 mesh ground truth 和点云估计；
- 不引入真实视觉噪声。

必须记录：

\[
e_j=d_j^{pointcloud}-d_j^{mesh}
\]

重点统计点云高估距离的情况，因为高估会带来碰撞风险。

---

## 5.3 阶段 3：仿真视觉点云

处理流程：

```text
depth
  ↓
使用对应时间戳的 camera pose
  ↓
转换到 robot base frame
  ↓
删除无效深度
  ↓
robot self-filter
  ↓
ROI crop
  ↓
voxel downsample
  ↓
spatial hash / KD-tree
  ↓
point-to-capsule query
```

视觉线程和控制线程必须异步：

- 视觉更新：10–20 Hz；
- 控制循环：30–50 Hz；
- 控制线程读取最近完成的地图快照；
- 控制线程不得等待点云更新。

---

## 5.4 阶段 4：真实相机与真实机器人

在阶段 3 通过后再接入真实深度相机。

额外考虑：

- 相机标定误差；
- 深度噪声；
- TF 和 joint state 时间同步；
- 通信延迟；
- 舵机跟踪误差；
- 未观测区域；
- 机器人自身点云过滤。

---

## 6. 点到 capsule 的距离

给定障碍点 \(p\)，capsule 轴线端点 \(a,b\)，半径 \(r\)。

先计算点在线段上的投影比例：

\[
t=
\operatorname{clip}
\left(
\frac{(p-a)^\top(b-a)}
{\|b-a\|^2},
0,1
\right)
\]

轴线最近点：

\[
c=a+t(b-a)
\]

点到 capsule 表面的距离：

\[
d=\|p-c\|-r
\]

点云点需要具有虚拟半径 \(r_{point}\)：

\[
d=\|p-c\|-r_{capsule}-r_{point}
\]

建议：

\[
r_{point}
=
\frac{\sqrt3}{2}v_{voxel}
+\sigma_{depth}
+\sigma_{calibration}
\]

其中 `v_voxel` 是 voxel size。

---

## 7. 点云查询加速

禁止 capsule 与完整点云做 Python 双重循环。

推荐 spatial hash：

1. 点云构建时，将点映射到固定体素格；
2. 对每个 capsule 计算扩大后的 AABB；
3. 只读取 AABB 覆盖的 hash cells；
4. 对候选点进行向量化 point-to-segment 距离计算；
5. 每个 capsule 最多保留 2–3 个 contact。

扩大范围：

\[
r_{capsule}+d_{off}+r_{point}
\]

向量化计算：

```python
ab = b - a
denom = np.dot(ab, ab)

t = ((points - a) @ ab) / max(denom, 1e-12)
t = np.clip(t, 0.0, 1.0)

closest = a + t[:, None] * ab
distances = (
    np.linalg.norm(points - closest, axis=1)
    - capsule_radius
    - point_radius
)
```

ROI 只保留机器人可达空间及其附近区域。整把椅子不需要全部进入点云查询。

---

## 8. Contact Manager

不要使用整个机器人唯一的全局最小距离：

\[
d_{robot}=\min_j d_j
\]

每个接近障碍物的 capsule 应单独生成约束。

每个 capsule 最多保留：

```text
K = 2
```

必要时视觉点云可增至：

```text
K = 3
```

### 8.1 激活滞回

使用两个阈值：

```text
d_on  = 进入 active set 的距离
d_off = 离开 active set 的距离
```

要求：

\[
d_{off}>d_{on}
\]

推荐初始值：

```text
mesh:
d_on  = 0.08 m
d_off = 0.10 m

vision:
d_on  = 0.10 m
d_off = 0.13 m
```

### 8.2 contact 切换滞回

只有当新 contact 明显更近时才切换：

\[
d_{new}<d_{old}-\epsilon_{switch}
\]

建议：

```text
mesh:   0.002–0.005 m
vision: 0.005–0.010 m
```

当新旧 contact 距离非常接近时，可以短时间同时保留。

---

## 9. Point Jacobian

对 capsule 轴线最近点 \(c\)：

\[
\dot c=J_c(q)\dot q
\]

如果已有 link 的 6D Jacobian：

\[
J_l=
\begin{bmatrix}
J_v\\
J_\omega
\end{bmatrix}
\]

最近点相对 link 原点的世界坐标偏移为 \(r_c\)，则：

\[
J_c=J_v-[r_c]_\times J_\omega
\]

必须确认所用运动学库的 Jacobian 排列：

- `[linear; angular]`；
- 或 `[angular; linear]`。

必须使用有限差分做单元测试，但运行时不得使用有限差分梯度。

测试：

\[
\frac{d(q+\epsilon v)-d(q)}{\epsilon}
\approx
n^\top J_c(q)v
\]

---

## 10. CBF 约束

对第 \(i\) 个 contact：

\[
h_i=d_i-d_{safe,i}
\]

距离变化率：

\[
\dot d_i=n_i^\top J_{c_i}(q)\dot q
\]

CBF 约束：

\[
n_i^\top J_{c_i}(q)\dot q
+
\alpha_i(d_i-d_{safe,i})
\geq
-\delta_i
\]

其中：

- \(\delta_i\geq0\) 为 slack；
- 正常情况下 slack 应接近 0；
- slack 只用于防止 QP infeasible；
- slack 过大必须触发停止或重规划。

---

## 11. CBF-QP

输入：

\[
\dot q_{nom}
\]

优化变量：

\[
\dot q,\delta
\]

目标：

\[
\min_{\dot q,\delta}
\frac12\|\dot q-\dot q_{nom}\|_W^2
+
\frac{\lambda_s}{2}
\|\dot q-\dot q_{prev}\|^2
+
\frac{\lambda_\delta}{2}\|\delta\|^2
\]

约束：

\[
n_i^\top J_{c_i}\dot q
+
\alpha_i(d_i-d_{safe,i})
+
\delta_i
\geq0
\]

\[
\delta_i\geq0
\]

\[
\dot q_{min}\leq\dot q\leq\dot q_{max}
\]

\[
-\ddot q_{max}\Delta t
\leq
\dot q-\dot q_{prev}
\leq
\ddot q_{max}\Delta t
\]

\[
q_{min}+m_q
\leq
q+\Delta t\dot q
\leq
q_{max}-m_q
\]

使用 OSQP 或等价小型 QP solver。

必须：

- 固定最大约束数量；
- 初始化时 setup solver；
- 每周期只 update 数值；
- 使用 warm start；
- 不允许每周期重新 setup solver。

---

## 12. 安全距离

基础安全距离：

```text
mesh:
0.015–0.025 m

vision:
0.020–0.030 m
```

视觉有效安全距离：

\[
d_{safe,eff}
=
d_{safe,base}
+
d_{perception}
+
v_{closing}\tau_{latency}
+
d_{tracking}
\]

其中：

\[
v_{closing}
=
\max(0,-n^\top J_c\dot q_{nom})
\]

视觉感知 margin 初始建议：

```text
0.015–0.030 m
```

最终数值必须根据 mesh ground truth 与视觉距离误差统计确定。

---

## 13. SO-ARM100 命令输出

如果底层接收位置命令：

\[
q_{cmd}
=
q_{measured}
+
\Delta t\dot q_{safe}
\]

禁止仅基于上一帧命令积分：

\[
q_{cmd}\neq q_{cmd,prev}+\Delta t\dot q_{safe}
\]

必须以最新测量关节状态为基准。

还需限制：

- joint limit；
- 单周期最大 position step；
- 最大速度；
- 最大加速度；
- 命令滤波。

---

## 14. Emergency 与 deadlock

### 14.1 Emergency

满足任一条件时进入 emergency：

- 距离小于紧急阈值；
- QP 失败；
- 法向无效；
- 点云或 TF 超时；
- slack 超过阈值。

行为：

1. 丢弃 nominal action；
2. 限制速度；
3. 只允许远离障碍物；
4. 无可靠方向时停止；
5. 回到最近安全状态或请求上层重规划。

### 14.2 Deadlock

当以下条件持续一段时间时判定 stuck：

- 距目标进展小于阈值；
- 多条 CBF 长期 active；
- nominal action 长期被大幅修改；
- slack 持续非零。

大椅子完全挡住工作空间时，正确行为是返回 `infeasible`，不是持续震荡。

CBF 只负责局部安全，不保证能绕过所有大障碍物。需要绕行时由 RRT、cuRobo 或中间 waypoint 生成新的 nominal path。

---

## 15. 性能目标

控制频率：

```text
30–50 Hz
```

视觉频率：

```text
10–20 Hz
```

50 Hz 时单周期预算：

```text
FK + capsule update       < 1 ms
broad phase               < 1 ms
distance query            < 3–5 ms
contact manager           < 1 ms
Jacobian assembly         < 1–2 ms
QP                        < 1–2 ms
total safety pipeline     p99 < 10 ms
```

必须记录：

- p50；
- p95；
- p99；
- max；
- timeout 次数。

计时项：

```python
timing = {
    "fk": ...,
    "broadphase": ...,
    "distance": ...,
    "contact_manager": ...,
    "jacobian": ...,
    "qp": ...,
    "total": ...,
}
```

---

## 16. 推荐目录结构

```text
obstacle_avoidance/
├── geometry/
│   ├── capsule_model.py
│   ├── forward_kinematics.py
│   └── point_jacobian.py
│
├── backends/
│   ├── base.py
│   ├── sim_mesh_backend.py
│   ├── ideal_pointcloud_backend.py
│   └── visual_pointcloud_backend.py
│
├── perception/
│   ├── depth_to_pointcloud.py
│   ├── self_filter.py
│   ├── roi_filter.py
│   ├── voxel_downsample.py
│   └── spatial_hash.py
│
├── contacts/
│   └── contact_manager.py
│
├── control/
│   ├── cbf_constraints.py
│   ├── qp_solver.py
│   ├── emergency.py
│   └── deadlock_detector.py
│
├── runtime/
│   ├── safety_controller.py
│   ├── perception_worker.py
│   └── metrics.py
│
└── tests/
    ├── test_projection.py
    ├── test_capsule_distance.py
    ├── test_normal_direction.py
    ├── test_point_jacobian.py
    ├── test_cbf_sign.py
    ├── test_contact_hysteresis.py
    ├── test_qp_feasibility.py
    └── test_backend_consistency.py
```

---

## 17. 控制循环伪代码

```python
def safety_control_step(
    q_measured,
    qd_measured,
    nominal_action,
    dt,
):
    qd_nominal = nominal_action_to_joint_velocity(
        q=q_measured,
        action=nominal_action,
        dt=dt,
    )

    capsules_world = robot_geometry.forward_capsules(q_measured)

    raw_contacts = obstacle_backend.query(
        capsules_world=capsules_world,
        activation_distance=d_off,
        max_contacts_per_capsule=max_contacts_per_capsule,
    )

    contacts = contact_manager.update(raw_contacts)

    cbf_constraints = []

    for contact in contacts:
        d = contact.distance
        n = contact.normal_world
        c = contact.axis_point_world

        J_c = robot_kinematics.point_jacobian(
            q=q_measured,
            link_name=contact.link_name,
            point_world=c,
        )

        closing_speed = max(
            0.0,
            -(n @ J_c @ qd_nominal),
        )

        d_safe_eff = (
            d_safe_base
            + perception_margin(contact.confidence)
            + closing_speed * total_latency
            + tracking_margin
        )

        h = d - d_safe_eff
        a = n @ J_c

        cbf_constraints.append(
            CBFConstraint(
                a=a,
                lower_bound=-alpha * h,
                contact=contact,
            )
        )

    result = qp_solver.solve(
        q=q_measured,
        qd_nominal=qd_nominal,
        qd_previous=qd_measured,
        cbf_constraints=cbf_constraints,
        dt=dt,
    )

    if not result.success or result.max_slack > slack_limit:
        qd_safe = emergency_safe_velocity(
            q=q_measured,
            contacts=contacts,
        )
    else:
        qd_safe = result.qd

    q_command = q_measured + dt * qd_safe
    q_command = enforce_joint_and_step_limits(q_command)

    return q_command
```

---

## 18. 禁止事项

1. 不得每帧重新构建场景 SDF。
2. 不得每帧重新构建静态 mesh 的 BVH。
3. 不得遍历 capsule × 所有 mesh triangles。
4. 不得遍历 capsule × 整个点云的 Python 双重循环。
5. 不得只使用整个机器人的一个全局 minimum constraint。
6. 不得在运行时使用有限差分计算梯度。
7. 不得让视觉线程阻塞控制线程。
8. 不得将未观测区域直接视为绝对安全。
9. 不得混用 world、base、camera 和 link 坐标。
10. 所有长度统一为 meter，关节角统一为 radian。
11. 不得每周期重新 setup QP solver。
12. 不得假设穿透后距离查询一定返回可靠法向。
13. 不得只用 visual mesh 做 collision query。
14. 不得声称 CBF 可以绕过任意大障碍物。
15. 不得在没有 deadlock 检测时持续重复同一 nominal action。

---

## 19. 验收标准

### Mesh 阶段

1. sphere、plane、box 的距离结果正确；
2. capsule 端点、中段、边缘附近距离正确；
3. 法向始终从障碍物指向机器人；
4. point Jacobian 通过有限差分验证；
5. 远离障碍物时，QP 输出接近 nominal；
6. 到达安全边界时，不允许继续靠近；
7. 多个 capsule 同时接近不同障碍物时，多条约束同时生效；
8. 面、边、角切换时无高频抖动；
9. 无解时返回 infeasible 或 emergency，不崩溃；
10. 安全流水线 p99 小于 10 ms。

### 点云阶段

1. ideal point cloud 与 mesh ground truth 距离误差可统计；
2. 不允许明显高估真实距离；
3. ROI 和 spatial hash 明显减少候选点数；
4. 不允许出现完整点云双重循环；
5. self-filter 后机器人本体不被识别为障碍物。

### 视觉阶段

1. 深度帧、TF 和 joint state 时间同步正确；
2. 相机运动时点云无明显拖影；
3. 感知线程不会阻塞控制线程；
4. 点云超时会触发停止或降级；
5. 安全 margin 根据实测误差确定；
6. 大障碍物挡死目标时正确返回 stuck/infeasible。
