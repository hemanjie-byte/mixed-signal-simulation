# From a switching path to a regulated rail

# 从开关通路到稳定电源

**A first lesson in 40–150 V DC/DC conversion · V3.2.0 · 2026-11-03**

**40～150 V DC/DC入门课程 · V3.2.0 · 2026-11-03**

Start with three questions: Where can the current flow? Where is the energy stored? Which voltage does each device actually see? These questions connect an introductory circuit course to the more detailed models in this repository. This lesson uses the teaching perspective of an experienced researcher; it does not represent an actual academician's lecture or endorsement.

先问三个问题：电流能够走哪条路？能量存在哪里？每个器件实际承受什么电压？这三个问题把大学电路基础与仓库中的详细模型联系起来。本讲采用资深研究者讲授基础课的方式，不代表某位真实院士的授课或背书。

[Watch the English-only animation](buck_energy_flow.gif) · [Open its still image](buck_energy_flow_poster.png)

[观看仅英文标注的动画](buck_energy_flow.gif) · [查看静态示意图](buck_energy_flow_poster.png)

## 1. What a buck converter changes

## 1. 降压转换器改变了什么

A buck converter delivers a lower average output voltage by rapidly changing the connection to its input. A 100 V input does not mean that the difference between 100 V and 12 V must become heat. In the ideal case, 12 V at 1 A is 12 W, so a 100 V source supplies only 0.12 A **on average**. Its instantaneous current is pulsed. The inductor current can remain continuous.

降压转换器通过快速改变输入连接，获得较低的平均输出电压。100 V降到12 V，不意味着88 V的压差必须全部变成热。理想情况下，12 V、1 A输出为12 W，因此100 V电源的**平均**输入电流仅0.12 A。输入瞬时电流是脉冲，电感电流却可以保持连续。

The switch acts like a controlled connection, the inductor stores magnetic energy, and the capacitor stores electric-field energy. “The inductor smooths current” means that changing current requires voltage and time. “The capacitor smooths voltage” means that changing voltage requires charge. Neither statement says that current or voltage is perfectly constant in real hardware.

开关是受控连接，电感储存磁场能量，电容储存电场能量。“电感平滑电流”是说，改变电流需要电压作用一段时间；“电容平滑电压”是说，改变电压需要电荷。真实硬件中的电流、电压都不因此变得绝对恒定。

## 2. Four equations explain the picture

## 2. 用四个方程读懂图

With positive inductor current directed from SW toward the output, and positive capacitor current directed into its upper plate:

把电感电流从SW流向输出规定为正，把流入电容上极板的电流规定为正：

$$
v_L=L\frac{di_L}{dt}=v_{SW}-v_{out},\qquad
i_C=i_L-I_{load},\qquad
i_C=C\frac{dv_{out}}{dt},\qquad
E_L=\tfrac12 L i_L^2.
$$

If $v_L>0$, positive $i_L$ rises and the inductor gains energy. If $v_L<0$ while $i_L>0$, it releases energy. Capacitor charging depends on **$i_L-I_{load}$**, not simply on which transistor is ON. The capacitor may continue charging after the high-side switch turns OFF if $i_L$ is still above the load current.

当$v_L>0$时，正向$i_L$上升，电感能量增加。当$v_L<0$、$i_L>0$时，电感释放能量。电容充电取决于**$i_L-I_{load}$**，不能简单按哪个晶体管导通判断。如果电感电流仍高于负载电流，高侧关断后电容仍可能继续充电。

The animation uses the P02 fixed-output approximation. Its capacitor-current arrows satisfy KCL, but **the animation does not solve capacitor voltage ripple**. Use the V3 B07 dynamic LC example for that separate question.

动画采用P02的固定输出电压近似，电容电流箭头满足KCL，但**动画没有求解电容电压纹波**。若要研究该问题，可另看V3的B07动态LC示例。

## 3. Follow one switching cycle

## 3. 沿着一个开关周期观察

The GIF renders the exported [P02 teaching trace](../results/teaching_buck_100V_25C.json): 100 V input, 12 V output, 1 A average load, 100 µH, 250 kHz and two 40 ns dead times. These are assumed demonstration values. The gate-command annotations use assumed 0/10 V levels; they are not a calculated gate-charge waveform.

GIF直接绘制导出的[P02教学数据](../results/teaching_buck_100V_25C.json)：100 V输入、12 V输出、1 A平均负载、100 µH、250 kHz及两段40 ns死区。这些数值是演示假设。图中的栅极命令电平假设为0/10 V，并非计算得到的栅电荷波形。

| Phase | Conventional-current path | What to notice |
|---|---|---|
| High-side ON | Input → QH → inductor → output → return | SW is 100 V, so $v_L=88$ V and current rises. |
| First dead time | Ground → low-side body diode → inductor → output → ground | Both channels are OFF. Positive inductor current forward-biases the diode and pulls SW to −0.8 V. |
| Low-side ON | Ground → QL channel → inductor → output → ground | The enhanced MOSFET channel conducts source-to-drain in this positive-current freewheel state. |
| Second dead time | Ground → body diode → inductor → output → ground | QL turns OFF before QH turns ON. Non-overlapping commands avoid intentionally shorting the input. |

| 阶段 | 传统电流方向 | 观察重点 |
|---|---|---|
| 高侧导通 | 输入→QH→电感→输出→回路 | SW为100 V，电感电压88 V，电流上升。 |
| 第一段死区 | 地→低侧体二极管→电感→输出→地 | 两个沟道均关断；正向电感电流使体二极管导通，把SW拉到−0.8 V。 |
| 低侧导通 | 地→QL沟道→电感→输出→地 | MOSFET导通沟道可双向导电，此处续流沿源到漏方向。 |
| 第二段死区 | 地→体二极管→电感→输出→地 | QL先关断，QH后导通；不重叠的命令避免主动把输入短路。 |

An OFF switch does not make inductor current disappear. A reverse-recovery pulse, finite gate delay, Miller-induced turn-on and ringing require additional models. The GIF does not add those effects to its ideal switching trace. Dead time is useful, but actual shoot-through immunity also depends on driver delays, parasitics and operating conditions. The body-diode path and recovery mechanisms are described in TI's technical note [S02, §3.3](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf).

开关关断不会让电感电流消失。反向恢复脉冲、有限栅延迟、Miller误导通和振铃需要额外模型；GIF没有把这些效应叠加到理想开关轨迹中。死区有用，但真实抗直通能力仍依赖驱动延迟、寄生和工作条件。体二极管与恢复机制见TI技术文档[S02，第3.3节](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)。

**Animation time is deliberately stretched differently for each phase.** The actual period is 4 µs; the GIF loop lasts about 18 s, including introductory/comparison slides. The horizontal axes under the circuit use physical time. Moving arrows indicate conventional current direction, not electron speed or the magnitude of current.

**各阶段的动画时间被有意按不同倍数放慢。**真实周期为4 µs；含开场与比较页的GIF循环约18 s。电路下方横轴仍为物理时间。移动箭头表示传统电流方向，不表示电子速度或电流大小。

## 4. Derive duty ratio before memorizing it

## 4. 先推导占空比，再记公式

In periodic steady state, current returns to its starting value, so $\int_0^{T_s}v_L\,dt=0$. With ideal high/low switches and no dead time, the average switch-node voltage is $D V_{in}$, hence $V_{out}=D V_{in}$. At 250 kHz, $T_s=4$ µs. A 12 V output therefore needs ideal ON times of 1.20 µs at 40 V, 0.48 µs at 100 V and 0.32 µs at 150 V.

在周期稳态下，电流回到起始值，因此$\int_0^{T_s}v_L\,dt=0$。若高低侧为理想开关且无死区，开关节点平均电压为$D V_{in}$，得到$V_{out}=D V_{in}$。250 kHz对应$T_s=4$ µs。12 V输出的理想导通时间：40 V输入时1.20 µs，100 V时0.48 µs，150 V时0.32 µs。

The P02 illustration includes two body-diode intervals, each with drop $V_F$ and duration $t_d$. Its volt-second balance gives:

P02示例包含两段体二极管续流，每段压降$V_F$、时间$t_d$。伏秒平衡得到：

$$
D=\frac{V_{out}+2V_Ft_d/T_s}{V_{in}}
=\frac{12+2(0.8)(40\,\mathrm{ns})/(4\,\mathrm{\mu s})}{100}
=0.12016.
$$

Thus the calculated ON interval is 480.64 ns, not exactly 480 ns. Its current ripple is $(100-12)\times480.64\,\mathrm{ns}/100\,\mathrm{\mu H}=0.4229632$ A peak-to-peak. The exported current spans 0.7885184–1.2114816 A. This is a useful hand-check of the numerical trace, not a prediction for a particular manufactured transistor.

因此计算导通时间为480.64 ns，而不是恰好480 ns。电流峰峰纹波为$(100-12)\times480.64\,\mathrm{ns}/100\,\mathrm{\mu H}=0.4229632$ A，导出电流范围为0.7885184～1.2114816 A。这是对数值轨迹的手算校核，不是对某个实际制造晶体管的预测。

## 5. Separate three voltage questions

## 5. 分清三个电压问题

**Drain-to-source stress:** the power transistor may block approximately the input voltage, plus effects of diode clamping and overshoot. A 150 V converter input does not establish that a nominal “150 V device” is sufficient. Check the relevant working rating, transient limits, SOA and isolation.

**漏源应力：**功率晶体管可能承受接近输入的关断电压，还要考虑二极管钳位和过冲。转换器最高输入150 V，不代表标称“150 V器件”就足够；还须检查工作额定、瞬态限制、SOA及隔离。

**Local gate-to-source voltage:** for an N-channel high-side device with SW at 100 V, a 10 V $V_{GS}$ means the absolute gate voltage is about 110 V. The driver follows the switching source. Gate-oxide limits apply to $V_{GS}$, not simply the gate voltage relative to system ground.

**局部栅源电压：**N沟道高侧器件的SW为100 V时，10 V的$V_{GS}$意味着栅极对系统地约110 V。驱动器跟随开关源极浮动，栅氧限制主要针对$V_{GS}$，不能只看栅极对系统地电压。

**Floating-driver supply:** a bootstrap capacitor supplies charge while the high side is ON and can recharge when SW is low. A first estimate is $\Delta V_{boot}\approx(Q_g+I_qt_{on}+Q_{leak})/C_{boot}$. Low-side time, diode/resistor charging, leakage and driver UVLO determine whether the real supply recovers sufficiently. See technical references [S01, §5.2.2](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) and [S03, §2–3.1](https://www.ti.com/lit/an/slua887a/slua887a.pdf).

**浮动驱动电源：**高侧导通时，自举电容提供电荷；SW较低时能够补充电荷。一阶估算为$\Delta V_{boot}\approx(Q_g+I_qt_{on}+Q_{leak})/C_{boot}$。低侧时间、二极管/电阻充电、漏电及驱动欠压锁定决定电源能否充分恢复。参见技术资料[S01，第5.2.2节](https://www.ti.com/lit/ml/slua618a/slua618a.pdf)及[S03，第2～3.1节](https://www.ti.com/lit/an/slua887a/slua887a.pdf)。

## 6. Add one non-ideality at a time

## 6. 每次增加一个非理想因素

| Model | Student question | What the model adds |
|---|---|---|
| P01 | Why does the transistor not switch instantly? | Gate/Miller charging and switching-energy mechanisms. |
| P02 | Where does current go in dead time? | Diode freewheel trace and a separate prescribed reverse-recovery pulse. |
| P03 | Can the floating driver stay powered? | Bootstrap charge depletion, recharge and UVLO behavior. |
| P04 | Can a fast SW edge disturb a logic receiver? | Level-shift/common-mode capacitive injection. |
| P05 | Does a sensed overcurrent stop immediately? | Current-sense filtering, threshold and delay effects. |
| P06 | Why use two undervoltage thresholds? | Startup and hysteretic UVLO behavior. |
| P07 | Why can VDS exceed Vin? | Parasitic RLC ringing and a dissipative snubber example. |
| P08 | How do watts of loss become temperature rise? | An explicit loss and thermal budget with stated accounting. |
| P09 | How does a converter start and recover after a load change? | Averaged soft-start, load-step response and current-reference limiting. |

| 模型 | 学生的问题 | 模型增加的内容 |
|---|---|---|
| P01 | 晶体管为何不瞬间完成开关？ | 栅极/Miller充电与开关能量机制。 |
| P02 | 死区电流走哪里？ | 二极管续流轨迹及单独预设的反向恢复脉冲。 |
| P03 | 浮动驱动能否保持供电？ | 自举电荷消耗、补充及欠压锁定行为。 |
| P04 | SW快沿会不会干扰逻辑接收器？ | 电平移位与共模电容注入。 |
| P05 | 检测到过流是否立即停止？ | 电流检测滤波、阈值与延迟效应。 |
| P06 | 欠压为何采用两个阈值？ | 启动供电与迟滞欠压锁定。 |
| P07 | VDS为何可能超过Vin？ | 寄生RLC振铃及耗能吸收网络示例。 |
| P08 | 损耗功率如何转为温升？ | 明确列出核算边界的损耗及热预算。 |
| P09 | 电源如何启动并响应负载变化？ | 平均模型中的软启动、负载阶跃与电流参考限幅。 |

See the [model catalog](../models/model_catalog.json) for the exact equations, assumptions and omissions of P01–P09.

模型P01～P09的准确方程、假设和缺项见[模型目录](../models/model_catalog.json)。

The models form a hierarchy, not one calibrated transistor-level simulation. Combining results requires checking assumptions and units. For a nonlinear output capacitance, $Q_{oss}(V)=\int_0^V C_{oss}(v)\,dv$ and $E_{oss}(V)=\int_0^V vC_{oss}(v)\,dv$; using $\tfrac12 C_{oss}(V)V^2$ without checking the voltage dependence can be wrong. Do not add separate Coss/recovery energies if a current-waveform integral already includes those currents. Likewise, a simple thermal-resistance model does not certify a package, layout or junction-temperature limit.

这些模型构成分层研究工具，不是一个经过校准的晶体管级联合仿真。组合结果之前须核对假设和单位。非线性输出电容应计算$Q_{oss}(V)=\int_0^V C_{oss}(v)\,dv$、$E_{oss}(V)=\int_0^V vC_{oss}(v)\,dv$；未经检查直接代入$\tfrac12 C_{oss}(V)V^2$可能错误。若电流波形积分已包含电容与反向恢复电流，就不能再把相应能量单独加一次。简单热阻模型同样不能认证封装、版图或结温限制。

## 7. Five questions to test understanding

## 7. 五个自测问题

1. **At 150 V input, what is the ideal duty ratio for 12 V output?** Answer: $12/150=0.08=8\%$; at 250 kHz, the ON interval is 320 ns. Dead time and losses change the required value.

   **150 V输入、12 V输出，理想占空比是多少？**答：8%；250 kHz下导通时间320 ns。死区与损耗会改变实际所需数值。

2. **With 100 µH and 88 V across the inductor, how much does current rise in 100 ns?** Answer: $\Delta I=88\times100\,\mathrm{ns}/100\,\mathrm{\mu H}=0.088$ A. This illustrates why sensing/turn-off delays matter; it is not a full current-limit overshoot calculation.

   **100 µH电感两端88 V，100 ns内电流增加多少？**答：0.088 A。它说明检测/关断延迟的重要性，但不是完整限流过冲计算。

3. **QH is OFF, but $i_L=1.2$ A and the load draws 1 A. Does the output capacitor charge?** Answer: yes, $i_C=+0.2$ A under the stated sign convention, even though the inductor is releasing energy.

   **QH关断，电感1.2 A、负载1 A，输出电容还会充电吗？**答：会。按所定义方向，$i_C=+0.2$ A；同时电感仍可以释放能量。

4. **A gate is at 110 V and its source is at 100 V. What is $V_{GS}$?** Answer: 10 V. Measuring gate-to-ground alone cannot establish gate-oxide stress.

   **栅极110 V、源极100 V，$V_{GS}$是多少？**答：10 V。只测栅极对地不足以判断栅氧应力。

5. **Does a smooth waveform and a passing test prove safe 150 V silicon?** Answer: no. The test checks the specified reduced equations and implementation. Device calibration, process corners, parasitics, SOA, isolation and measurements are additional evidence.

   **波形平滑、测试通过，是否证明150 V硅片安全？**答：不能。测试验证的是所列缩减方程与实现；器件校准、工艺角、寄生、SOA、隔离和实测还需要额外证据。

## 8. How to read the evidence

## 8. 怎样阅读依据

The equations above are explicit circuit-law derivations. The linked TI documents are manufacturer technical references, not peer-reviewed papers. Peer-reviewed control/design evidence and its actual reading depth are separated in the [source and gap audit](../SOURCES_AND_GAPS.md) and [source records](../research/sources.json). Inclusion of a paper identifies a mechanism; it does not mean its topology, parameters or measured performance have been reproduced.

上面的方程来自明确的电路定律推导。链接的TI资料是厂家技术文档，不是同行评审论文。同行评审的控制/设计依据及实际阅读深度在[来源与缺口审计](../SOURCES_AND_GAPS.md)和[来源记录](../research/sources.json)中单独列明。引用论文用于识别机制，不代表复现了其拓扑、参数或实测性能。

The original 200-person/182-paper cohort remains the V3.1 research baseline. This lesson adds a DC/DC learning path rather than claiming that every paper has now been modeled. All numerical examples remain public-source illustrative models without a foundry PDK or measured-device extraction.

原200人、182篇论文名单继续作为V3.1研究基线。本讲增加DC/DC学习路径，不声称所有论文都已建模。所有数值例子仍是公开资料示意模型，没有晶圆厂PDK或实测器件参数提取。
