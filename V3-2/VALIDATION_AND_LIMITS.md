# Validation and limits — V3.2.0

# 校核与限制 — V3.2.0

All 61 recorded implementation checks pass: 25 new DC/DC checks and 36 baseline checks, executed on 2026-11-03. This demonstrates the stated reduced equations and data are internally checked; it does not establish measured accuracy or sign-off.

2026-11-03执行的61项实现检查全部通过：新增25项DC/DC检查及36项基线检查。证明已对所述简化方程与数据进行内部检查，不代表实测精度或签核。

- [New test source](tests/test_dcdc.py) and [actual outcomes](results/validation.json) — 新测试源码及实际结果
- [Baseline rerun](validation/baseline_rerun.json) — 本轮基线重跑
- [Browser QA](validation/viewer_validation.json) — 浏览器检查
- [Excel QA](validation/workbook_validation.json) — 工作簿检查
- [GIF QA](education/gif_validation.json) — 动画检查

## What the checks establish

## 检查能说明什么

The tests use analytic limits, charge/energy balances, event timing, numerical convergence, loss-ledger separation and artifact joins. Read the test source for tolerances. The baseline tests cover MOS/BJT/capacitor identities, ADC/FFT conventions, loop responses, buck energy balance and bibliography joins. A passing test is not evidence that an assumed coefficient matches a fabricated device.

检查包含解析极限、电荷/能量平衡、事件时序、数值收敛、损耗台账分项与文件关联；容差见测试源码。基线检查包括MOS/BJT/电容恒等关系、ADC/FFT约定、环路响应、Buck能量平衡及题录关联。测试通过不证明假设系数与实际器件一致。

## Keep these quantities distinct

## 必须区分的量

1. **Input voltage versus rating:** 40–150 V is converter maximum input. No breakdown, avalanche, SOA, process corner or reliability model is supplied.

   **输入与额定：**40～150V为转换器最高输入；未提供击穿、雪崩、安全工作区、工艺角或可靠性模型。
2. **Internal signals versus ports:** P01–P09 expose named internal trajectories. They do not invent complete multi-terminal supply currents. Baseline models with ports use positive current into the port; ΣVI includes storage.

   **内部信号与端口：**P01–P09展示具名内部轨迹，不虚构完整多端口供电电流。具有端口的基线模型以流入为正，ΣVI包含储能。
3. **Stored Coss energy versus commutation loss:** Eoss=∫vC(v)dv and Qoss=∫C(v)dv differ. The matched-pair hard-turn-on assumption in P08 uses upper stored-energy discharge plus lower charging loss, summing to Vin·Qoss. P01 channel overlap excludes displacement and recovery currents. Recovery Vin·Qrr is a prescribed bus-energy estimate, not heat measured in the diode.

   **Coss储能与换流损耗：**Eoss=∫vC(v)dv与Qoss=∫C(v)dv不同。P08匹配双管硬开通假设将上管储能释放与下管充电损耗相加，得到Vin·Qoss。P01沟道交叠不含位移与恢复电流；Vin·Qrr仅为规定的母线能量估算，不是二极管实测发热。
4. **Hot node versus junction:** P08 assigns all modeled losses, including inductor copper loss, to one effective shared thermal node. It is not an individual MOS junction. The time response uses converged steady loss as constant power; it is not a fully coupled P(T(t)) transient. No magnetic core or PCB loss is modeled.

   **热节点与结温：**P08将全部列出损耗（含电感铜损）归入一个等效共享热节点，并非单个MOS结温。瞬态以收敛后的稳态损耗作为恒功率，不是完整P(T(t))耦合瞬态；未含磁芯或PCB损耗。
5. **Functional protections versus implementation:** P03 reports bootstrap UVLO sizing flags without shutting down its prescribed PWM. P04 is an unclamped RC disturbance surrogate; large values are not rail-limited receiver voltages or qualified CMTI. P05 is low-side sensing. P06 models startup/brownout hysteresis. P09 limits average current reference, not cycle-by-cycle peak current.

   **功能保护与实际实现：**P03输出自举欠压尺寸检查标志，不关闭规定PWM；P04为无钳位RC扰动替代模型，过大电压不是受电源轨限幅的接收器波形或认证CMTI；P05为低侧检测；P06为启动/掉电回差；P09限制平均电流参考，不是逐周期峰值限流。
6. **Series RLC versus snubber topology:** P07 varies series damping in a linear parasitic RLC circuit. It does not solve a literal series-RC branch placed across a real transistor.

   **串联RLC与吸收拓扑：**P07改变线性寄生RLC的串联阻尼，不求解跨真实晶体管的实际串联RC吸收支路。
7. **Conceptual 3D versus physical fields:** the rotatable boxes/OBJ files are functional diagrams without process dimensions, doping, local voltage fields or current density. GIF current arrows are instructional and time-distorted.

   **概念3D与物理场：**旋转方块/OBJ为功能图，没有工艺尺寸、掺杂、局部电势场或电流密度；GIF电流箭头是教学示意，时间经过拉伸。

## Remaining research work

## 尚未完成的研究

Calibrated LDMOS/extended-drain PDK models, intrinsic charge partition, breakdown/SOA, full floating driver/level-shifter transistor networks, true cycle-by-cycle protection, coupled electrothermal partition, layout electromagnetic extraction, core loss, RF/SiGe and complete ADC/chopper/PLL circuits remain outside this release. Nine added benches must not be presented as a completed analog process library.

校准的LDMOS/扩展漏PDK模型、内禀电荷分配、击穿/SOA、完整浮动栅驱/电平转换晶体管网络、真实逐周期保护、分区电热耦合、版图电磁提取、磁芯损耗、RF/SiGe以及完整ADC/斩波/PLL电路仍未覆盖。不能把9项增强测试台描述为完整模拟工艺库。
