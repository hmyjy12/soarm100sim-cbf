# CBF 固定杆评测汇总

- 生成时间：2026-07-07T14:41:01
- Git commit：`c8b6f3d`
- Checkpoint：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/checkpoints/2026-07-06_14-44-29/PPO/checkpoints/best_agent.pt`
- MJCF：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/SO-ARM100/Simulation/SO100/mujoco/scene_plus.xml`
- NPZ：`/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/rl/workspace_cache/workspace_tcp_merged_test.npz`
- Episodes：256（seed=42）
- **障碍物：固定细杆 `obstacle_rod` @ (0.15, 0.09, 0.17) m（见 mujoco/log.md）**
- CBF：d_safe=0.02 γ=0.8 activate<0.04

## 总体对比

| 指标 | 无 CBF | CBF v2 | Δ (CBF−base) |
|------|--------|--------|--------------|
| pos le 1cm | 75.0% | 67.6% | -7.4 pt |
| pos le 2cm | 85.5% | 79.7% | -5.9 pt |
| joint pos1cm ori20 | 66.0% | 60.2% | -5.9 pt |
| cbf safe rate | — | 60.9% | — |
| safe reach 2cm | — | 60.2% | — |
| safe reach 1cm ori20 | — | 52.0% | — |
| no contact rate | 70.3% | 80.1% | +9.8 pt |
| median best dist mm | 5.5mm | 6.3mm | +0.8 mm |
| h min median mm | — | 17.8mm | — |

## 到达代价（同 idx 配对）

- Δbest_dist 中位数：**+0.0 mm**
- Δbest_dist p90：**+26.9 mm**
- 退化 >10 mm 比例：**18.0%**

## 按难度分层

| 档位 | N | SafeReach@2cm (CBF) | pos≤2cm base | pos≤2cm CBF | h_min 中位 (CBF) |
|------|---|---------------------|-------------|-------------|------------------|
| hard | 85 | 10.6% | 67.1% | 50.6% | -7.0 mm |
| medium | 48 | 81.2% | 100.0% | 100.0% | 13.6 mm |
| easy | 123 | 86.2% | 92.7% | 91.9% | 27.9 mm |
