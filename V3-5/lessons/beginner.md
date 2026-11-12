# Beginner — notice and explain

# 入门版——观察与讲述

Use one analogy, notice one change, then state where the analogy stops.

借助一个比喻，观察一个变化，并说清比喻到哪里为止。

V3-5 teaching edition of the existing v3.3.0 numerical baseline: 20 views comprise 3 illustrative device models, 1 statistical demonstration, 2 prescribed mechanism benches and 14 circuit/system benches. The 75 printable entries include these 20 plus 55 legacy/background representations; they are not 75 independently calibrated devices. The release audit separately records reruns of the current numerical baseline. This teaching content adds no new physics, PDK, silicon fit or physical-accuracy gain.

V3-5是现有v3.3.0数值基线的教学版本：20个视图含3个示意器件、1个统计演示、2个预设机制测试台及14个电路/系统测试台。75个打印条目包含上述20项与55项旧版/背景表示，并非75种独立校准器件。发布审计另行记录现有数值基线重跑；本教学内容未新增物理机制、PDK、硅实测拟合或物理准确度提高。

## Before you begin

## 阅读前

Current tells how much charge passes each second. Voltage tells the energy difference per unit charge. A model is a useful simplified explanation; it is not the tiny object itself.

电流表示每秒有多少电荷通过；电压表示每单位电荷的能量差。模型是有用的简化解释，并不是微小实物本身。

40/60/80/100/120/150 V specify maximum DC/DC input classes. Device voltage ratings and transient margins require independent evidence.

40/60/80/100/120/150 V表示DC/DC最高输入档位；器件额定耐压及瞬态裕量需要独立依据。

A current arrow uses conventional positive charge flow; terminal signs follow the recorded model. Electrical power is voltage times current with a declared reference direction.

电流箭头采用正电荷的约定方向；端口符号遵循原模型。电功率为明确参考方向下电压与电流的乘积。

Read the horizontal-axis label: a bias, temperature, frequency or sample sweep is not elapsed time. GIF speed is pedagogical and each GIF shows one fixed recorded case.

先读横轴：偏置、温度、频率或样本扫描不是时间流逝。GIF播放速度为教学调整，每个GIF只展示一个固定保存工况。

Prints are enlarged egg-size relief concepts, roughly 60×42 mm in plan. Layer thicknesses are exaggerated; plastic connections do not represent electrical connections. Boards show functions, not fabricated layouts.

打印件是放大的鸡蛋大小浮雕概念，平面约60×42 mm；层厚被夸大，塑料连接不代表电连接，展示板表示功能而非制造版图。

Numerical residuals test the stated equations. Physical validity needs independent measured data; conservation alone cannot establish all model physics.

数值残差检验所述方程；物理有效性需要独立实测，单靠守恒不能证明全部模型物理正确。

## A01 — Four-terminal MOS interpolation

四端MOS连续插值

[GIF: A01_transfer_25C](../simulation/V3-3/education/gifs/A01.gif) · [STL: V33_A01](../printing/stl/V33_A01.stl)

**Everyday picture / 生活比喻**

A gate is like a tap handle: a small control change can change the flow.

栅极像水龙头的把手：轻轻调整，就能改变流量。

**Watch / 观察动画**

Follow the moving dot: as gate voltage rises, drain current changes. The horizontal axis is voltage, not time.

跟着圆点看：栅极电压升高时，漏极电流改变。横轴是电压，不是时间。

**Analogy limit / 比喻边界**

The gate acts through an electric field; it is not a moving door. The picture does not show individual electrons.

栅极靠电场起作用，并不是会移动的门；图片也没有逐个显示电子。

Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

## A02 — Junction charge and varactor

结电荷与变容二极管

[GIF: A02_CV_25C](../simulation/V3-3/education/gifs/A02.gif) · [STL: V33_A02](../printing/stl/V33_A02.stl)

**Everyday picture / 生活比喻**

Imagine a stretchy storage pocket: how much extra charge it can hold changes with its voltage.

想象一个可变大小的储物袋：电压不同，多放一点电荷的能力也不同。

**Watch / 观察动画**

Watch capacitance and charge while the bias changes. More reverse bias reduces the displayed capacitance.

改变偏置，观察电容和电荷；反向偏置越大，图中的电容越小。

**Analogy limit / 比喻边界**

The pocket is an analogy. This animation scans voltages and does not show a moving physical boundary.

储物袋只是比喻。动画扫描不同电压，没有计算真实边界怎样移动。

Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

## A03 — Reciprocal NPN Ebers–Moll

满足互易关系的NPN Ebers–Moll

[GIF: A03_gummel_25C](../simulation/V3-3/education/gifs/A03.gif) · [STL: V33_A03](../printing/stl/V33_A03.stl)

**Everyday picture / 生活比喻**

A small change at a control point can produce a large flow change, like gently opening a sensitive valve.

像轻轻打开一个灵敏的阀门，控制处的小变化可以带来明显的流量变化。

**Watch / 观察动画**

Watch collector and base currents grow as VBE rises. Equal height steps on the log axis mean equal multiplication factors.

观察VBE升高时集电流和基电流的增长；对数纵轴上相同的高度变化表示相同倍数。

**Analogy limit / 比喻边界**

This is a transistor, not a mechanical valve. The plot does not show carriers travelling through the base.

这是晶体管，不是机械阀门；曲线没有显示载流子穿过基区的过程。

Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

## A04 — MOS pair mismatch and correlation

MOS配对失配与相关性

[GIF: A04_area16um2](../simulation/V3-3/education/gifs/A04.gif) · [STL: V33_A04](../printing/stl/V33_A04.stl)

**Everyday picture / 生活比喻**

Two cookies made with the same cutter can still differ a little. Bigger cookies can make tiny edge differences less important.

同一个模具做的两块饼干仍可能略有不同；饼干变大时，细小差别的相对影响可能减小。

**Watch / 观察动画**

Compare the two thresholds and their difference. Each moving position is another sample, not a later moment.

比较两个阈值及其差值；光标每移动一次代表换一个样本，并不是时间过去了。

**Analogy limit / 比喻边界**

Real mismatch comes from manufacturing variation, not cookie edges. These random numbers are assumed, not factory measurements.

真实失配来自制造差异，不是饼干边缘；这里的随机数是假设，并非工厂测量。

Sources / 来源: [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

## B01 — MOS differential pair

MOS差分对

[GIF: B01_25C](../simulation/V3-3/education/gifs/B01.gif) · [STL: V33_B01](../printing/stl/V33_B01.stl)

**Everyday picture / 生活比喻**

Two slides share one fixed stream of balls: sending more down one leaves fewer for the other.

两条滑道分同一股小球：一边分得多，另一边就少。

**Watch / 观察动画**

Watch one branch current rise while the other falls. Their sum stays at 100 µA.

观察一条支路电流上升、另一条下降；两者之和保持100 µA。

**Analogy limit / 比喻边界**

The two transistors steer electrical current. The fixed total comes from an ideal source in this example.

两只晶体管分配的是电流；本例的固定总量由理想电流源提供。

Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

## B02 — CTAT/PTAT reference sum

CTAT/PTAT基准合成

[GIF: B02_temperature](../simulation/V3-3/education/gifs/B02.gif) · [STL: V33_B02](../printing/stl/V33_B02.stl)

**Everyday picture / 生活比喻**

One ruler reading falls as a room warms while another rises. Adding the right amounts can keep the total steadier.

房间变暖时，一个读数下降，另一个上升；按合适比例相加，总数就更稳定。

**Watch / 观察动画**

Follow temperature: the two contributions tilt in opposite directions, but their sum still bends a little.

沿温度轴观察：两项朝相反方向变化，总和仍有一点弯曲。

**Analogy limit / 比喻边界**

This is a calculated voltage sum, not a real thermometer or a complete working reference chip.

这里计算的是电压之和，并不是真实温度计或完整基准芯片。

Sources / 来源: [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf)

## B03 — Input noise and sampled kT/C

输入噪声与采样kT/C

[GIF: B03_25C](../simulation/V3-3/education/gifs/B03.gif) · [STL: V33_B03](../printing/stl/V33_B03.stl)

**Everyday picture / 生活比喻**

A quiet room can still have many small sounds. Adding a wider range of sounds can make the total louder.

安静的房间也有细小声音；把更宽范围的声音加起来，总声音可能更大。

**Watch / 观察动画**

Compare the low- and high-frequency noise curves. The moving dot chooses a frequency, not a moment of random noise.

比较低频和高频噪声曲线；圆点选的是频率，并非某一时刻的随机噪声。

**Analogy limit / 比喻边界**

Sound is only a comparison. The plot shows electrical noise density, not a recording of sound or a random voltage waveform.

声音只是类比；图里是电噪声密度，不是录音或随机电压的时间波形。

Sources / 来源: [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

## B04 — Capacitor DAC and SAR ADC

电容DAC与SAR ADC

[GIF: B04_mismatch](../simulation/V3-3/education/gifs/B04.gif) · [STL: V33_B04](../printing/stl/V33_B04.stl)

**Everyday picture / 生活比喻**

An ADC is like reading a height with a ruler that has only a fixed number of marks.

ADC像用刻度数量有限的尺子量身高。

**Watch / 观察动画**

Compare the smooth input with the stepped reconstructed value and their error. The movie does not expose every internal bit decision.

比较平滑输入、台阶状重建值和误差；动画没有逐个展示内部每一位的判断。

**Analogy limit / 比喻边界**

A digital number has finite steps, but this example leaves out real electrical noise and incomplete settling.

数字结果有有限台阶，但本例没有加入真实电噪声和未充分稳定的影响。

Sources / 来源: [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

## B05 — LDO loop and load step

LDO环路与负载阶跃

[GIF: B05_25C](../simulation/V3-3/education/gifs/B05.gif) · [STL: V33_B05](../printing/stl/V33_B05.stl)

**Everyday picture / 生活比喻**

A helper keeps a water tank near a chosen level. When more water is taken out, the helper needs time to react.

小助手把水箱维持在指定高度；突然多取水时，助手需要一点时间才补得上。

**Watch / 观察动画**

Watch output voltage dip after the load step and then approach a new level.

观察负载突然增加后，输出电压先下降，再接近新的水平。

**Analogy limit / 比喻边界**

The real object regulates voltage. This small-change model does not show a completely empty tank or startup.

真实对象调节的是电压；小变化模型没有展示“完全空箱”或开机启动。

Sources / 来源: [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf)

## B06 — Phase loop and noise transfer

相位环路与噪声传递

[GIF: B06_zeta0.7](../simulation/V3-3/education/gifs/B06.gif) · [STL: V33_B06](../printing/stl/V33_B06.stl)

**Everyday picture / 生活比喻**

Two people try to clap together. A slow correction leaves them apart; a too-eager correction can overshoot.

两个人想拍手同步：调整太慢会跟不上，调整过猛又可能超过。

**Watch / 观察动画**

Watch the phase response after a small step. Compare how damping changes overshoot and settling in the available cases.

观察小阶跃后的相位响应，并在不同工况中比较阻尼对超调和稳定时间的影响。

**Analogy limit / 比喻边界**

The picture is an averaged timing rule, not a transistor oscillator or an animation of each clock edge.

图里是简化的相位规律，不是晶体管振荡器，也没有逐个时钟边沿。

Sources / 来源: [base:B09](https://chic.caltech.edu/wp-content/uploads/2013/05/general.pdf)

## B07 — 40–150 V synchronous buck

40–150V同步降压

[GIF: B07_100V_25C](../simulation/V3-3/education/gifs/B07.gif) · [STL: V33_B07](../printing/stl/V33_B07.stl)

**Everyday picture / 生活比喻**

A fast switch sends short energy packets; a coil and a storage part smooth them into a lower steady output.

快速开关送出一小包一小包能量，线圈和储能元件把它们变成较平稳的低电压。

**Watch / 观察动画**

Watch the switch-node voltage jump while inductor current ramps and output voltage ripples only slightly.

观察开关节点电压跳变、电感电流爬升或下降，而输出电压只小幅起伏。

**Analogy limit / 比喻边界**

The animation is slowed down. Its 40–150 V labels describe input cases, not a proven safe voltage for the drawn switch.

动画已经放慢；40～150 V表示输入工况，不是图中开关经过验证的安全耐压。

Sources / 来源: [base:D01](../simulation/V3-3/MODEL_CARDS.md)

## P01 — HV MOS gate charge and switching overlap

高压MOS栅电荷与开关交叠

[GIF: P01_100V_25C](../simulation/V3-3/education/gifs/P01.gif) · [STL: V33_P01](../printing/stl/V33_P01.stl)

**Everyday picture / 生活比喻**

Before a heavy gate changes position, its helper must move some charge. That takes time even when the command is quick.

像推动一扇重门前要先用力，开关改变状态前需要移动电荷，即使命令很快也要时间。

**Watch / 观察动画**

Watch gate voltage pause near a plateau while drain voltage changes; compare the voltage/current overlap.

观察栅压在平台附近暂缓变化时，漏压正在改变，并留意电压和电流的交叠。

**Analogy limit / 比喻边界**

Nothing mechanically moves. The stages are prescribed, and the current does not include every charging or recovery current.

没有机械门在移动；阶段由模型规定，图中电流未包含所有充电和恢复电流。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

## P02 — Dead-time diode and reverse recovery

死区二极管与反向恢复

[GIF: P02_100V_25C](../simulation/V3-3/education/gifs/P02.gif) · [STL: V33_P02](../printing/stl/V33_P02.stl)

**Everyday picture / 生活比喻**

When two gates take turns, a short pause avoids opening both together. During the pause, another path carries the flow.

两道门轮流开时，中间留一点空档，避免同时打开；空档里由另一条路承接流量。

**Watch / 观察动画**

Watch the small negative switch-node level during dead time. The recovery pulse is a separate trace, not part of the plotted inductor current.

观察死区时开关节点略低于零；恢复脉冲是另一条独立曲线，不是已画电感电流的一部分。

**Analogy limit / 比喻边界**

The spare path is a diode. A prescribed triangle illustrates recovery; it does not show actual stored carriers leaving a junction.

承接的是二极管通路；三角形脉冲只是恢复示意，并非逐个计算存储载流子离开结区。

Sources / 来源: [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

## P03 — Floating bootstrap supply and UVLO margin

浮地自举供电与欠压裕量

[GIF: P03_100V_25C](../simulation/V3-3/education/gifs/P03.gif) · [STL: V33_P03](../printing/stl/V33_P03.stl)

**Everyday picture / 生活比喻**

A small battery rides in a lift: its height above the floor changes, but the battery still has its own two ends.

一块小电池坐电梯：它离地面的高度改变，但电池仍有自己的两个端点。

**Watch / 观察动画**

Watch the local supply fall when charge is used and rise when recharging is possible. Compare it with the low-voltage warning line.

观察使用电荷时局部电压下降，可补充电荷时回升，并与欠压警戒线比较。

**Analogy limit / 比喻边界**

The bootstrap part is a capacitor, not a battery. Its local voltage is measured relative to the moving switch node.

自举元件是电容，不是电池；其局部电压相对正在变化的开关节点测量。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

## P04 — Level-shifter common-mode disturbance

电平移位接收端共模扰动

[GIF: P04_100V_25C_strong](../simulation/V3-3/education/gifs/P04.gif) · [STL: V33_P04](../printing/stl/V33_P04.stl)

**Everyday picture / 生活比喻**

A quick push on one side of a soft divider can disturb the other side even without a direct opening.

在柔软隔板一边猛推一下，即使没有开口，另一边也会受扰。

**Watch / 观察动画**

Watch a fast common-voltage edge produce a short receiver-voltage bump, then decay through the discharge path.

观察共同电压快速变化时接收端出现短暂凸起，随后经泄放通路消退。

**Analogy limit / 比喻边界**

Electrical coupling here uses a tiny capacitor, not a moving wall. The picture does not contain a full logic receiver.

这里通过小电容耦合，不是墙在移动；图中没有完整逻辑接收器。

Sources / 来源: [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

## P05 — Current-sense amplifier and delayed comparator

电流检测放大器与延迟比较器

[GIF: P05_25C](../simulation/V3-3/education/gifs/P05.gif) · [STL: V33_P05](../printing/stl/V33_P05.stl)

**Everyday picture / 生活比喻**

A scale measures a load, and an alarm rings after the reading becomes large enough. Both reading and ringing take time.

秤测出重量，读数足够大时警铃响起；读数变化和响铃都需要时间。

**Watch / 观察动画**

Watch current step first, the amplifier respond next, and the comparator change state later.

观察电流先跳变，放大器随后响应，比较器再改变状态。

**Analogy limit / 比喻边界**

The alarm only reports a result here; it does not turn off the current. The circuit senses near ground.

本例警铃只报告结果，不会切断电流；检测电路工作在接近地电位处。

Sources / 来源: [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

## P06 — HV startup supply and hysteretic UVLO

高压启动供电与迟滞欠压锁定

[GIF: P06_100V_25C](../simulation/V3-3/education/gifs/P06.gif) · [STL: V33_P06](../printing/stl/V33_P06.stl)

**Everyday picture / 生活比喻**

A toy waits until its energy cup is full enough to start, and stops only when the level falls to a lower mark.

玩具等“能量杯”装到较高刻度才启动，降到较低刻度才停止。

**Watch / 观察动画**

Watch the auxiliary voltage cross 9 V to enable, and 7 V to disable during the interruption.

观察辅助电压越过9 V时开启，供电中断时降到7 V关闭。

**Analogy limit / 比喻边界**

The cup is a capacitor and the marks are voltage thresholds. The model is not a physical high-voltage startup transistor.

杯子比喻电容，刻度比喻电压阈值；模型并非真实高压启动晶体管。

Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

## P07 — Switch-node parasitic ringing and damping

开关节点寄生振铃与阻尼

[GIF: P07_100V_damped](../simulation/V3-3/education/gifs/P07.gif) · [STL: V33_P07](../printing/stl/V33_P07.stl)

**Everyday picture / 生活比喻**

A swing moves back and forth after a push. Friction gradually turns its stored motion into heat.

秋千被推一下后会来回摆动，摩擦逐渐把储存的运动能量变成热。

**Watch / 观察动画**

Watch the excess voltage and current exchange energy while the oscillation becomes smaller.

观察多余电压和电流交替变化，振荡逐渐变小。

**Analogy limit / 比喻边界**

The circuit stores electric and magnetic energy, not swinging motion. Its starting push is chosen by the model.

电路储存电场能和磁场能，并非机械摆动；初始“推力”是模型预设的。

Sources / 来源: [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

## P08 — DC/DC separated losses and thermal budget

DC/DC分项损耗与热预算

[GIF: P08_100V_25C](../simulation/V3-3/education/gifs/P08.gif) · [STL: V33_P08](../printing/stl/V33_P08.stl)

**Everyday picture / 生活比喻**

An energy budget is like tracking where pocket money goes. Energy used as heat is no longer delivered to the load.

能量账本像记录零花钱花到哪里；变成热的能量就不能送给负载。

**Watch / 观察动画**

Compare the fixed loss bars, then watch one shared temperature rise toward its final level.

比较固定的损耗条形，再看一个共同温度逐渐接近最终水平。

**Analogy limit / 比喻边界**

The bars are steady losses, not moving heat maps. The shared temperature is not the temperature of each transistor junction.

条形表示稳态损耗，不是会流动的热图；共同温度也不是每只晶体管的结温。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

## P09 — Averaged buck soft-start and current-reference limit

平均Buck软启动与电流参考限幅

[GIF: P09_100V_25C](../simulation/V3-3/education/gifs/P09.gif) · [STL: V33_P09](../printing/stl/V33_P09.stl)

**Everyday picture / 生活比喻**

A helper turns the target up slowly at startup. If too many toys ask for power, the helper reaches a limit and the output can fall.

小助手启动时慢慢提高目标；若太多玩具同时要电，助手达到上限，输出就可能下降。

**Watch / 观察动画**

Watch the reference ramp, then the extra load at 4 ms. The current command stops increasing and output voltage falls.

观察参考缓升及4 ms处负载增加；电流指令不再上升，输出电压随之下降。

**Analogy limit / 比喻边界**

This movie shows averages. It does not show each switching pulse or promise a safe limit for every current peak.

动画显示平均量；没有逐个开关脉冲，也不保证每个电流尖峰都被安全限制。

Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

## Printable companion — 75 entries

## 打印配套——75项

Only V33_* entries map one-to-one to the current 20 numeric lessons. Related GIFs attached to legacy prints explain an associated topic and are not a newly simulated animation of that legacy structure.

仅V33_*条目与现有20个数值课程一一对应。旧打印件关联GIF仅解释相关主题，不是针对该旧结构新做的仿真动画。

### V1_M01 — Isolated high-side NLDMOS

高侧隔离NLDMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the gate and the island marked ISO. A high-side switch rides with a changing voltage, like a small control booth on a lift.

找到栅极及ISO岛；高侧开关随电压一起升降，像电梯上的小控制室。

[STL](../printing/stl/V1_M01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M02 — Low-side NLDMOS

低侧NLDMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Trace the long drift section beside the gate. This switch can provide the lower path for a buck converter’s current.

沿栅极旁的长漂移区观察；该开关可为降压器电流提供下方通路。

[STL](../printing/stl/V1_M02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M03 — High-voltage PLDMOS

高压PLDMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Compare its P source and drift labels with the N-channel model. It uses the opposite control polarity, not a different-looking on/off door.

把P型源区和漂移区与N沟道模型对比；它采用相反控制极性，并非只换一种外形的门。

[STL](../printing/stl/V1_M03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M04 — Drain-extended NMOS

高压DENMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the drain extension beyond the short channel. It is like giving a steep change a longer path to spread across.

找到短沟道之外的漏极延伸区，像给陡峭的变化留更长的过渡路径。

[STL](../printing/stl/V1_M04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M05 — Low-voltage NMOS

低压NMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Point to source, drain, gate and body tap. The insulated gate controls the small channel between source and drain.

指认源、漏、栅及体接触；绝缘栅控制源漏之间的小沟道。

[STL](../printing/stl/V1_M05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M06 — Low-voltage PMOS

低压PMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the N well around the P source and drain. Compare the signs of its control voltage with the NMOS model.

找到P源漏周围的N阱，并与NMOS比较控制电压的正负方向。

[STL](../printing/stl/V1_M06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M07 — Drain-extended PMOS

高压DEPMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Follow the P extension from the channel to the drain. Its long section represents a voltage-handling idea, not a measured safety distance.

沿沟道到漏端寻找P延伸区；长段表示承受电压的思路，并非测得的安全距离。

[STL](../printing/stl/V1_M07.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_Q01 — NPN bipolar transistor

NPN双极晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Trace N–P–N regions and locate the thin middle base. A small control change can alter the larger collector current.

沿N—P—N区域找到中间基区，小控制变化可以改变较大的集电流。

[STL](../printing/stl/V1_Q01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf) · [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V1_Q02 — PNP bipolar transistor

PNP双极晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

This three-region stack reads P–N–P. Compare its terminal arrows with the NPN example instead of assuming the same current direction.

这三层为P—N—P；应与NPN比较端口箭头，不能假定电流方向相同。

[STL](../printing/stl/V1_Q02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf) · [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V1_D01 — MOS body PN freewheel diode

体PN续流二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The diode is already inside the MOS body structure. During a switching pause, this built-in path can carry current.

二极管已包含在MOS体结构中；开关暂停时，这条内置通路可承接电流。

[STL](../printing/stl/V1_D01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

### V1_D02 — High-voltage bootstrap PN diode

高压自举PN二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Follow the charging direction from the supply toward the bootstrap store. The diode helps keep charge from simply flowing back.

沿电源到自举储能元件的方向看充电通路；二极管帮助阻止电荷直接倒流。

[STL](../printing/stl/V1_D02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V1_D03 — Schottky diode

肖特基二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Compare the metal-to-semiconductor contact with the two semiconductor regions of a PN diode. The contact itself forms the barrier.

将金属—半导体接触与PN二极管的两种半导体区比较，势垒在接触处形成。

[STL](../printing/stl/V1_D03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_D04 — Gate Zener clamp

栅极Zener钳位

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A clamp is like an overflow outlet that begins taking flow when the level becomes too high. Find the marked clamp path.

钳位像水位太高时开始泄流的溢流口，找出标记的钳位通路。

[STL](../printing/stl/V1_D04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_J01 — High-voltage startup JFET

高压启动JFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Point to the junction gate beside the channel. The example starts with a conducting path that can help fill the startup supply.

指认沟道旁的结栅；示例从导通通路开始，可帮助给启动电源充电。

[STL](../printing/stl/V1_J01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V1_R01 — High-voltage polysilicon resistor chain

高压多晶硅电阻链

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Trace the long resistor path and its sections. Several sections can share a total voltage, like steps sharing a climb.

沿长电阻路径看分段，多个段可分担总电压，像台阶分担上升高度。

[STL](../printing/stl/V1_R01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V1_R02 — Current-sense resistor

电流检测电阻

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the short resistor between its end pads. A small voltage across it acts like a reading of how much current passes.

找到两端焊盘之间的短电阻，跨接的小电压像电流大小的读数。

[STL](../printing/stl/V1_R02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

### V1_C01 — MIM capacitor

MIM电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find two metal plates with a separating layer. The gap stores electrical energy without the plates touching.

找出两片金属及中间隔层；两片不接触，仍能储存电能。

[STL](../printing/stl/V1_C01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf) · [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V1_C02 — MOM capacitor

MOM电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Look at two combs whose fingers alternate without touching. Their neighbouring fingers form the capacitor.

观察两把梳子，梳齿交错但不接触，相邻梳齿形成电容。

[STL](../printing/stl/V1_C02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf) · [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf)

### V1_I01 — Isolation junction and DTI equivalent network

隔离结与DTI等效网络

Isolation equivalent/structure concept / 隔离等效/结构概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the two domains and their boundary. Like neighbouring rooms, a boundary can separate them while small disturbances still pass between them.

找到两个区域及边界；像相邻房间，隔开后仍可能传来细小干扰。

[STL](../printing/stl/V1_I01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_E01 — High-voltage ESD clamp equivalent

高压ESD钳位等效器件

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Follow PAD through the clamp toward RETURN. It represents a route that diverts a sudden surge away from sensitive circuitry.

沿PAD经过钳位到RETURN，表示把突发冲击从敏感电路旁分走的通路。

[STL](../printing/stl/V1_E01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json)

### V1_L01 — External power inductor

外接功率电感

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Follow the coil from one end to the other. It resists an abrupt change of current, like a heavy wheel resists a sudden speed change.

沿线圈从一端看到另一端；它阻碍电流突变，像重轮子不易突然变速。

[STL](../printing/stl/V1_L01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

### V1_C03 — External output capacitor

外接输出电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

This store sits near the output and supplies charge when load demand briefly grows. Find its two electrodes.

这个储能元件靠近输出，负载短时多要电时可以补充电荷；找出两个电极。

[STL](../printing/stl/V1_C03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

### V1_C04 — External input capacitor

外接输入电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The input store is close to the fast switch so each energy packet does not have to come through a long wire.

输入储能元件靠近快速开关，使每包能量不必都沿长电线传来。

[STL](../printing/stl/V1_C04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

### V1_C05 — External bootstrap capacitor

外接自举电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

This small charge store travels with the high-side driver. Compare its two local ends, not just their height above ground.

这个小储能元件随高侧驱动一起升降；比较它的两个局部端点，而非只看相对地的高度。

[STL](../printing/stl/V1_C05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V2_N01 — SiC vertical MOSFET

SiC垂直MOSFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Trace the vertical path from the top source toward the bottom drain. The drawing uses silicon carbide as a material concept.

从顶部源极沿纵向找到底部漏极；图形展示碳化硅材料器件概念。

[STL](../printing/stl/V2_N01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N02 — Enhancement-mode GaN HEMT

增强型GaN HEMT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the thin channel beneath the barrier. The gate controls this path; the picture does not identify how a real normally-off gate was manufactured.

找出势垒下的薄沟道，栅极控制这条通路；图形未确定真实常关栅如何制造。

[STL](../printing/stl/V2_N02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/) · [legacy:P25](https://researchportal.hkust.edu.hk/en/publications/dynamic-performance-of-aln-passivated-algangan-mis-high-electron-/)

### V2_N03 — Silicon superjunction MOSFET

硅超结MOSFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Look for alternating P and N pillars. They illustrate how neighbouring regions can help share a high-voltage field.

寻找交替的P柱和N柱；它们表示相邻区域共同分布高压电场的思路。

[STL](../printing/stl/V2_N03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/)

### V2_N04 — IGBT

IGBT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the P collector underneath the drift region. This extra injecting region makes the device more than a MOSFET with a new label.

找到漂移区下的P集电区；该注入区域使它不是简单给MOSFET换标签。

[STL](../printing/stl/V2_N04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N05 — SiC JBS rectifier

SiC JBS整流二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find Schottky windows beside the P shielding islands. The two features have different roles in the same rectifier.

找出P屏蔽岛旁的肖特基窗口，两种结构在同一个整流器中各有作用。

[STL](../printing/stl/V2_N05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N06 — FinFET

FinFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Touch the raised fin and locate the gate around it. The gate can influence a thin channel from more than one side.

摸一摸凸起的鳍并找到周围栅极；栅极可从不止一侧控制薄沟道。

[STL](../printing/stl/V2_N06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P04](https://arxiv.org/abs/2005.02580)

### V2_N07 — a-IGZO thin-film transistor

a-IGZO TFT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the thin IGZO layer joining source and drain and the dielectric separating it from the gate.

找到连接源漏的薄IGZO层，以及把它与栅极隔开的介质。

[STL](../printing/stl/V2_N07.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P05](https://www.nature.com/articles/nature03090)

### V2_N08 — Organic polymer TFT

有机聚合物TFT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Point to the organic channel film. Its material is different from the silicon body in a conventional MOS transistor.

指认有机沟道薄膜，它的材料不同于传统MOS的硅体。

[STL](../printing/stl/V2_N08.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P06](https://www.nature.com/articles/nature25494)

### V2_N09 — Contact-limited MoS2 FET

MoS2接触受限FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Locate the very thin MoS2 sheet and its two contacts. A narrow entrance can limit flow even if the middle path is good.

找到很薄的MoS2片及两端接触；即使中间通道畅通，狭窄入口也可能限制流量。

[STL](../printing/stl/V2_N09.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P07](https://pubs.acs.org/doi/10.1021/nl303583v)

### V2_N10 — Ambipolar graphene FET

石墨烯双极性FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Follow the sheet between two contacts. Moving the gate setting away from the middle can increase conduction on either side.

沿两接触间的薄片观察；栅设置从中间向两侧移动，都可能增强导电。

[STL](../printing/stl/V2_N10.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P08](https://www.science.org/doi/10.1126/science.1102896)

### V2_N11 — Ballistic carbon-nanotube FET

碳纳米管弹道FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the narrow tube between the contacts. The ideal lesson lets carriers cross it without scattering, like a clear short tunnel.

找到接触之间的细管；理想课程让载流子无散射通过，像畅通的短隧道。

[STL](../printing/stl/V2_N11.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P19](https://www.nature.com/articles/nature22994) · [legacy:P24](https://ieeexplore.ieee.org/document/1224486/)

### V2_N12 — Ferroelectric FET memory cell

FeFET铁电存储晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the ferroelectric layer above the channel. Its remembered polarization changes how easily the gate turns the channel on.

找到沟道上方铁电层；它记住的极化状态改变栅极打开沟道的难易。

[STL](../printing/stl/V2_N12.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P09](https://www.nature.com/articles/s41928-020-00492-7)

### V2_N13 — Oxide RRAM cell

氧化物RRAM

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Look at the symbolic filament between electrodes. It is like a path that can become easier or harder to pass after a write command.

看电极间的示意细丝，像一条经写入命令后可变得更畅通或更难通过的路。

[STL](../printing/stl/V2_N13.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P10](https://www.nature.com/articles/s41928-018-0092-2) · [legacy:P19](https://www.nature.com/articles/nature22994)

### V2_N14 — Phase-change memory cell

PCM相变存储单元

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the heater beside the active storage volume. Heating and cooling can leave that material in states with different resistance.

找到存储体旁的加热器；加热和冷却可使材料停在电阻不同的状态。

[STL](../printing/stl/V2_N14.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P10](https://www.nature.com/articles/s41928-018-0092-2)

### V2_N15 — Magnetic tunnel junction

MTJ磁隧道结

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the fixed magnetic layer, barrier and free layer. Their relative directions help decide whether the electrical path is easier or harder.

找到固定磁层、势垒与自由磁层；它们的相对方向影响电流更易还是更难通过。

[STL](../printing/stl/V2_N15.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P11](https://www.sciencedirect.com/science/article/pii/S1369702117304285)

### V2_N16 — Ferroelectric capacitor

铁电电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Unlike an ordinary charge store, this dielectric can remember a polarization direction. The arrows are state labels, not moving parts.

不同于普通储电元件，这种介质能记住极化方向；箭头是状态标志，不是活动零件。

[STL](../printing/stl/V2_N16.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P09](https://www.nature.com/articles/s41928-020-00492-7) · [legacy:P23](https://www.science.org/doi/10.1126/science.1169678)

### V2_N17 — Nitride LED

氮化物LED

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the active layer between the P and N sides and the light arrow pointing outward. Electrical input can become emitted light.

找到P/N两侧中间的有源层及向外光箭头，电输入可转为发出的光。

[STL](../printing/stl/V2_N17.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P12](https://www.nature.com/articles/nphoton.2009.32)

### V2_N18 — Quantum-dot LED

量子点LED

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the dot-emission layer between transport layers. The dots represent where light is generated, not individual measured dot sizes.

找到传输层中间的量子点发光层；这些点表示发光位置，不是逐个测得的点尺寸。

[STL](../printing/stl/V2_N18.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P13](https://www.nature.com/articles/370354a0)

### V2_N19 — PIN photodetector

PIN光电探测器

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Light enters the middle region and produces an electrical signal. The light arrow is an input of light, not a third wire.

光进入中间区域产生电信号；光箭头代表光输入，不是第三根电线。

[STL](../printing/stl/V2_N19.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_N20 — Single-junction photovoltaic cell

单结光伏电池

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the light-facing side and two electrical contacts. Light can deliver energy out to a load, unlike a lamp that takes electrical energy in.

找到朝光一面及两个电接触；它可把光能送给负载，与用电发光的灯相反。

[STL](../printing/stl/V2_N20.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P14](https://www.science.org/doi/10.1126/science.1228604)

### V2_N21 — Thermoelectric generator cell

热电发电单元

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Point separately to HOT/COLD and to the electrical ends. A temperature difference can push electrical charge through the connected legs.

分别指出HOT/COLD与电端；温差能推动电荷经过互连的热电臂。

[STL](../printing/stl/V2_N21.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P15](https://www.nature.com/articles/nmat2090)

### V2_N22 — On-chip coupled transformer

片上耦合变压器

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Follow each of the two separate coils and locate all four ends. A changing current in one coil can induce voltage in the other without a wire joining them.

分别沿两线圈找出四个端头；一侧电流变化可在另一侧感应电压，不需要导线直接相连。

[STL](../printing/stl/V2_N22.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P16](https://ieeexplore.ieee.org/document/720393/)

### V2_N23 — Through-silicon via

TSV硅通孔

Interconnect concept / 互连概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the metal path passing through silicon and the liner around it. It connects levels, rather than controlling current like a transistor.

找到穿过硅体的金属通路及周围衬层；它连接不同层，不像晶体管那样控制电流。

[STL](../printing/stl/V2_N23.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P17](https://ieeexplore.ieee.org/document/5340655/)

### V2_N24 — Mach-Zehnder electro-optic modulator

MZI电光调制器

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Trace the two light paths from split to recombine. Changing one path’s timing can change how bright the combined output becomes.

从分光到合光追踪两条光路，改变一路的相位可改变合成输出亮度。

[STL](../printing/stl/V2_N24.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_N25 — Semiconductor laser diode

半导体激光二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the active stripe between two cavity ends. Above a threshold, the example turns more injected current into laser output.

找到两腔端之间的有源条带；超过阈值后，示例把更多注入电流转为激光输出。

[STL](../printing/stl/V2_N25.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_X01 — MOS gate charge and Miller coupling

MOS栅电荷与Miller耦合

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the Cgs and Cgd markers next to the MOS. They show that changing one voltage can require charge at another terminal.

找到MOS旁的Cgs和Cgd标记，它们表示一处电压改变可能需要另一端的电荷。

[STL](../printing/stl/V2_X01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf)

### V2_X02 — PN diode reverse recovery

PN二极管反向恢复

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The charge symbols beside the PN junction remind us that switching direction may need time to clear stored charge.

PN结旁的电荷符号提醒我们：改变方向前，可能要时间清走存储电荷。

[STL](../printing/stl/V2_X02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_X03 — MOS conduction-loss thermal feedback

MOS导通损耗自热反馈

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Find the thermal path from the MOS toward ambient. More current can make heat, and heat can make the resistance grow.

找到MOS到环境的热通路，电流增加可发热，升温又可能使电阻增大。

[STL](../printing/stl/V2_X03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### V2_X04 — PMOS NBTI aging

PMOS NBTI老化

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The time/stress marker shows that a transistor can slowly change after use. It is not an extra layer of visible damage.

时间/应力标记表示晶体管使用后可能缓慢变化，并不是一层可见损伤。

[STL](../printing/stl/V2_X04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P20](https://www.sciencedirect.com/science/article/pii/S0026271404001751)

### V2_X05 — MOS flicker and thermal noise

MOS 1/f与热噪声

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Compare the 1/f and WHITE markers. Slow fluctuations and broad-band noise are different contributions, not two surface textures.

比较1/f和WHITE标记：缓慢波动和宽带噪声是不同来源，不是两种表面纹理。

[STL](../printing/stl/V2_X05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P21](https://ieeexplore.ieee.org/document/34242/) · [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V2_X06 — MOS threshold and resistance statistics

MOS阈值及电阻统计分散

Parameter/statistical demonstration / 参数/统计演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The two printed transistors look alike, yet their assigned numbers can differ, like two classmates with slightly different heights.

两只打印晶体管外形相同，分配的参数却可不同，像两位同学身高略有差别。

[STL](../printing/stl/V2_X06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P22](https://ieeexplore.ieee.org/document/1210771/) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_A01 — Four-terminal MOS interpolation

四端MOS连续插值

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A gate is like a tap handle: a small control change can change the flow. The gate acts through an electric field; it is not a moving door. The picture does not show individual electrons.

栅极像水龙头的把手：轻轻调整，就能改变流量。栅极靠电场起作用，并不是会移动的门；图片也没有逐个显示电子。

[STL](../printing/stl/V33_A01.stl) · Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V33_A02 — Junction charge and varactor

结电荷与变容二极管

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Imagine a stretchy storage pocket: how much extra charge it can hold changes with its voltage. The pocket is an analogy. This animation scans voltages and does not show a moving physical boundary.

想象一个可变大小的储物袋：电压不同，多放一点电荷的能力也不同。储物袋只是比喻。动画扫描不同电压，没有计算真实边界怎样移动。

[STL](../printing/stl/V33_A02.stl) · Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V33_A03 — Reciprocal NPN Ebers–Moll

满足互易关系的NPN Ebers–Moll

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A small change at a control point can produce a large flow change, like gently opening a sensitive valve. This is a transistor, not a mechanical valve. The plot does not show carriers travelling through the base.

像轻轻打开一个灵敏的阀门，控制处的小变化可以带来明显的流量变化。这是晶体管，不是机械阀门；曲线没有显示载流子穿过基区的过程。

[STL](../printing/stl/V33_A03.stl) · Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V33_A04 — MOS pair mismatch and correlation

MOS配对失配与相关性

Parameter/statistical demonstration / 参数/统计演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Two cookies made with the same cutter can still differ a little. Bigger cookies can make tiny edge differences less important. Real mismatch comes from manufacturing variation, not cookie edges. These random numbers are assumed, not factory measurements.

同一个模具做的两块饼干仍可能略有不同；饼干变大时，细小差别的相对影响可能减小。真实失配来自制造差异，不是饼干边缘；这里的随机数是假设，并非工厂测量。

[STL](../printing/stl/V33_A04.stl) · Sources / 来源: [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_B01 — MOS differential pair

MOS差分对

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Two slides share one fixed stream of balls: sending more down one leaves fewer for the other. The two transistors steer electrical current. The fixed total comes from an ideal source in this example.

两条滑道分同一股小球：一边分得多，另一边就少。两只晶体管分配的是电流；本例的固定总量由理想电流源提供。

[STL](../printing/stl/V33_B01.stl) · Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V33_B02 — CTAT/PTAT reference sum

CTAT/PTAT基准合成

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

One ruler reading falls as a room warms while another rises. Adding the right amounts can keep the total steadier. This is a calculated voltage sum, not a real thermometer or a complete working reference chip.

房间变暖时，一个读数下降，另一个上升；按合适比例相加，总数就更稳定。这里计算的是电压之和，并不是真实温度计或完整基准芯片。

[STL](../printing/stl/V33_B02.stl) · Sources / 来源: [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf)

### V33_B03 — Input noise and sampled kT/C

输入噪声与采样kT/C

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A quiet room can still have many small sounds. Adding a wider range of sounds can make the total louder. Sound is only a comparison. The plot shows electrical noise density, not a recording of sound or a random voltage waveform.

安静的房间也有细小声音；把更宽范围的声音加起来，总声音可能更大。声音只是类比；图里是电噪声密度，不是录音或随机电压的时间波形。

[STL](../printing/stl/V33_B03.stl) · Sources / 来源: [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V33_B04 — Capacitor DAC and SAR ADC

电容DAC与SAR ADC

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

An ADC is like reading a height with a ruler that has only a fixed number of marks. A digital number has finite steps, but this example leaves out real electrical noise and incomplete settling.

ADC像用刻度数量有限的尺子量身高。数字结果有有限台阶，但本例没有加入真实电噪声和未充分稳定的影响。

[STL](../printing/stl/V33_B04.stl) · Sources / 来源: [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_B05 — LDO loop and load step

LDO环路与负载阶跃

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A helper keeps a water tank near a chosen level. When more water is taken out, the helper needs time to react. The real object regulates voltage. This small-change model does not show a completely empty tank or startup.

小助手把水箱维持在指定高度；突然多取水时，助手需要一点时间才补得上。真实对象调节的是电压；小变化模型没有展示“完全空箱”或开机启动。

[STL](../printing/stl/V33_B05.stl) · Sources / 来源: [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf)

### V33_B06 — Phase loop and noise transfer

相位环路与噪声传递

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Two people try to clap together. A slow correction leaves them apart; a too-eager correction can overshoot. The picture is an averaged timing rule, not a transistor oscillator or an animation of each clock edge.

两个人想拍手同步：调整太慢会跟不上，调整过猛又可能超过。图里是简化的相位规律，不是晶体管振荡器，也没有逐个时钟边沿。

[STL](../printing/stl/V33_B06.stl) · Sources / 来源: [base:B09](https://chic.caltech.edu/wp-content/uploads/2013/05/general.pdf)

### V33_B07 — 40–150 V synchronous buck

40–150V同步降压

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A fast switch sends short energy packets; a coil and a storage part smooth them into a lower steady output. The animation is slowed down. Its 40–150 V labels describe input cases, not a proven safe voltage for the drawn switch.

快速开关送出一小包一小包能量，线圈和储能元件把它们变成较平稳的低电压。动画已经放慢；40～150 V表示输入工况，不是图中开关经过验证的安全耐压。

[STL](../printing/stl/V33_B07.stl) · Sources / 来源: [base:D01](../simulation/V3-3/MODEL_CARDS.md)

### V33_P01 — HV MOS gate charge and switching overlap

高压MOS栅电荷与开关交叠

Mechanism demonstration / 机制演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Before a heavy gate changes position, its helper must move some charge. That takes time even when the command is quick. Nothing mechanically moves. The stages are prescribed, and the current does not include every charging or recovery current.

像推动一扇重门前要先用力，开关改变状态前需要移动电荷，即使命令很快也要时间。没有机械门在移动；阶段由模型规定，图中电流未包含所有充电和恢复电流。

[STL](../printing/stl/V33_P01.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V33_P02 — Dead-time diode and reverse recovery

死区二极管与反向恢复

Mechanism demonstration / 机制演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

When two gates take turns, a short pause avoids opening both together. During the pause, another path carries the flow. The spare path is a diode. A prescribed triangle illustrates recovery; it does not show actual stored carriers leaving a junction.

两道门轮流开时，中间留一点空档，避免同时打开；空档里由另一条路承接流量。承接的是二极管通路；三角形脉冲只是恢复示意，并非逐个计算存储载流子离开结区。

[STL](../printing/stl/V33_P02.stl) · Sources / 来源: [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

### V33_P03 — Floating bootstrap supply and UVLO margin

浮地自举供电与欠压裕量

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A small battery rides in a lift: its height above the floor changes, but the battery still has its own two ends. The bootstrap part is a capacitor, not a battery. Its local voltage is measured relative to the moving switch node.

一块小电池坐电梯：它离地面的高度改变，但电池仍有自己的两个端点。自举元件是电容，不是电池；其局部电压相对正在变化的开关节点测量。

[STL](../printing/stl/V33_P03.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V33_P04 — Level-shifter common-mode disturbance

电平移位接收端共模扰动

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A quick push on one side of a soft divider can disturb the other side even without a direct opening. Electrical coupling here uses a tiny capacitor, not a moving wall. The picture does not contain a full logic receiver.

在柔软隔板一边猛推一下，即使没有开口，另一边也会受扰。这里通过小电容耦合，不是墙在移动；图中没有完整逻辑接收器。

[STL](../printing/stl/V33_P04.stl) · Sources / 来源: [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V33_P05 — Current-sense amplifier and delayed comparator

电流检测放大器与延迟比较器

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A scale measures a load, and an alarm rings after the reading becomes large enough. Both reading and ringing take time. The alarm only reports a result here; it does not turn off the current. The circuit senses near ground.

秤测出重量，读数足够大时警铃响起；读数变化和响铃都需要时间。本例警铃只报告结果，不会切断电流；检测电路工作在接近地电位处。

[STL](../printing/stl/V33_P05.stl) · Sources / 来源: [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

### V33_P06 — HV startup supply and hysteretic UVLO

高压启动供电与迟滞欠压锁定

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A toy waits until its energy cup is full enough to start, and stops only when the level falls to a lower mark. The cup is a capacitor and the marks are voltage thresholds. The model is not a physical high-voltage startup transistor.

玩具等“能量杯”装到较高刻度才启动，降到较低刻度才停止。杯子比喻电容，刻度比喻电压阈值；模型并非真实高压启动晶体管。

[STL](../printing/stl/V33_P06.stl) · Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V33_P07 — Switch-node parasitic ringing and damping

开关节点寄生振铃与阻尼

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A swing moves back and forth after a push. Friction gradually turns its stored motion into heat. The circuit stores electric and magnetic energy, not swinging motion. Its starting push is chosen by the model.

秋千被推一下后会来回摆动，摩擦逐渐把储存的运动能量变成热。电路储存电场能和磁场能，并非机械摆动；初始“推力”是模型预设的。

[STL](../printing/stl/V33_P07.stl) · Sources / 来源: [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

### V33_P08 — DC/DC separated losses and thermal budget

DC/DC分项损耗与热预算

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

An energy budget is like tracking where pocket money goes. Energy used as heat is no longer delivered to the load. The bars are steady losses, not moving heat maps. The shared temperature is not the temperature of each transistor junction.

能量账本像记录零花钱花到哪里；变成热的能量就不能送给负载。条形表示稳态损耗，不是会流动的热图；共同温度也不是每只晶体管的结温。

[STL](../printing/stl/V33_P08.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### V33_P09 — Averaged buck soft-start and current-reference limit

平均Buck软启动与电流参考限幅

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A helper turns the target up slowly at startup. If too many toys ask for power, the helper reaches a limit and the output can fall. This movie shows averages. It does not show each switching pulse or promise a safe limit for every current peak.

小助手启动时慢慢提高目标；若太多玩具同时要电，助手达到上限，输出就可能下降。动画显示平均量；没有逐个开关脉冲，也不保证每个电流尖峰都被安全限制。

[STL](../printing/stl/V33_P09.stl) · Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

## Evidence boundary

## 依据边界

Existing source provenance is preserved. Three primary URLs were reopened for focused teaching checks; other entries retain their earlier read scope. This is not a new comprehensive paper audit, and references do not calibrate the authored model coefficients.

保留既有来源追溯，另打开3个一手网址作定向教学核对；其余保留原阅读范围。这不是新一轮全面论文审计，引用也不能校准人为模型系数。

Equations are teaching relations, not normative standards or complete SPICE implementations. A simplified exercise may use illustrative values different from its GIF.

公式为教学关系式，不是规范性标准或完整SPICE实现；简化练习可使用与GIF不同的示意数值。
