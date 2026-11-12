# V3-5 independent numerical and scientific-scope audit

2026-11-12. English first; Chinese follows.

The isolated snapshot passes all **96 tests** and recomputes all **211 cases**. The two simulation JSON files are byte-identical to the V3.3 numerical baseline. No model coefficient or physical law was changed by this audit. This establishes numerical reproducibility, not measured-device accuracy.

隔离快照通过全部**96项测试**，重新计算全部**211个工况**；两份仿真JSON与V3.3数值基线逐字节一致。本次审计未改变模型系数或物理定律。这证明数值可再现，不证明与实测器件的准确率。

## What the library actually contains / 器件库实际内容

The 20 numerical entries comprise **3 illustrative device models, 1 statistical parameter model, 2 prescribed mechanism benches and 14 circuit/system benches**. P01/P02 retain their legacy IDs but should be presented as mechanism benches: their prescribed commutation/recovery behavior is not a self-consistent multi-terminal compact model. All 20 use authored illustrative coefficients; none has verified foundry/PDK or measurement calibration.

20项数值内容包括**3个示意器件模型、1个统计参数模型、2个预设机制台架、14个电路/系统台架**。P01/P02保留历史ID，但展示时应列为机制台架：预设换流/恢复行为不是自洽的多端口紧凑模型。全部20项使用教学假设系数，均未完成晶圆厂/PDK或实测校准。

The 75 printable items are a separate geometry catalogue. Printing a MOS cross-section does not validate its I–V curve; an STL does not contain doping profiles or foundry process dimensions.

75项可打印内容属于独立几何目录。打印MOS剖面不能验证其I–V曲线；STL不包含掺杂分布或晶圆厂工艺尺寸。

## Numerical evidence and its limits / 数值证据及边界

Four isolated suites pass: historical analog/research 36, historical DC/DC 25, current analog numerics 18, and current DC/DC numerics 17. Thus 61 tests exercise historical implementations and 35 exercise current numerics/artifacts. Tests include analytic/high-precision comparison, KCL/charge/energy identities, periodicity, event timing, convergence and source/schema checks. The 96 total is not 96 independent silicon-validation experiments. Per-model test associations overlap and must not be summed.

四组隔离测试通过：历史模拟/研究36项、历史DC/DC 25项、当前模拟数值18项、当前DC/DC数值17项。因此61项执行历史实现，35项检查当前数值或产物。测试包括解析/高精度对照、KCL/电荷/能量恒等式、周期性、事件时序、收敛和来源/格式检查。96项不等于96个独立硅器件验证实验；逐模型关联测试有重叠，不能相加。

No new inconsistency was found in the recomputed published cases. This conclusion is bounded by the equations, saved cases and tests inspected; unmodeled physics remains unverified. A previous numerical-error reduction of at least 10% for selected metrics must not be rephrased as a 10% improvement in physical simulation accuracy.

重新计算的已发布工况未发现新的不一致。该结论仅适用于审查的方程、保存工况和测试，未建模物理仍未验证。历史上部分指标的数值误差降低至少10%，不能改写成物理仿真准确率提升10%。

## Intentional failure cases and rating boundaries / 有意失效工况与额定值边界

- **P03:** 15 of 36 cases have negative bootstrap UVLO margin: all 3.3 nF cases at 60–150 V. The 40 V small-capacitor margin remains positive. Gate pulses are not disabled by the diagnostic UVLO flag.
- **P04:** 6 of 12 cases cross the 0.7 V threshold; weak-path unclamped excursions are about 3.49–5.77 V. They are disturbance warnings, not qualified logic-pin waveforms.
- **P09:** all 18 cases intentionally settle near 9.6 V after the 6 Ω overload, consistent with the 1.6 A reference ceiling. This is not successful 12 V regulation.
- **P07:** the 150 V example starts at an assumed 172.5 V switch-node peak. That illustrates why input voltage and device rating differ; it does not establish a rated device requirement by itself.
- **P08:** none of the 18 cases leaves the assumed −40…175 °C coefficient domain; the hottest effective node is about 151.70 °C. It is not a measured individual junction temperature.

- **P03：**36项中15项自举欠压裕量为负，均为60–150 V的3.3 nF工况；40 V小电容工况仍为正。诊断UVLO标志不会禁用栅脉冲。
- **P04：**12项中6项跨过0.7 V门槛；弱通路无钳位偏移约3.49–5.77 V。这是干扰警示，不是已验证的逻辑引脚波形。
- **P09：**全部18项在6 Ω过载后有意稳定于约9.6 V，与1.6 A参考限幅一致，不代表12 V稳压成功。
- **P07：**150 V工况假设开关节点初始峰值172.5 V，说明输入电压不等于器件额定耐压；单凭该假设不能确定所需耐压等级。
- **P08：**18项均未超出假设的−40…175 °C系数范围，最高等效热节点约151.70 °C；该温度不是实测单个结温。

## Targeted primary-source checks / 重点一手来源核对

The bootstrap charge-budget principle was rechecked in the manufacturer note; it supports P03’s teaching equation but does not calibrate its assumed RC path. [TI SLUA887A](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

重新核对了厂家应用笔记中的自举电荷预算原理；它支持P03教学方程，但不能校准假设RC路径。[TI SLUA887A](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

INA381 has a 26 V common-mode range and a 400 ns typical comparator propagation delay. P05’s 35 ns delay is an authored assumption; the model is low-side only. [TI INA381](https://www.ti.com/lit/ds/symlink/ina381.pdf)

INA381共模范围上限26 V，比较器典型传播延迟400 ns；P05的35 ns为教学假设，仅用于低侧。[TI INA381](https://www.ti.com/lit/ds/symlink/ina381.pdf)

LM5116’s input operation extends to 100 V. Its architecture does not qualify P06/P09 at 120 or 150 V. [TI LM5116](https://www.ti.com/lit/ds/symlink/lm5116.pdf)

LM5116工作输入上限为100 V；其架构不能证明P06/P09在120或150 V具备硬件有效性。[TI LM5116](https://www.ti.com/lit/ds/symlink/lm5116.pdf)

The level-shifter paper reports a 20 V buck in 180 nm BCD. Its repository abstract was read again; PDF retrieval timed out, so this audit does not claim a new full-text review or implementation of its cancellation circuit. [TU Delft record](https://repository.tudelft.nl/record/uuid:d3912f8c-8e44-4c97-ace2-6974b8c570bb)

电平移位器论文对象是180 nm BCD的20 V降压芯片。本次重新阅读机构库摘要，PDF获取超时，因此不宣称重新阅读全文或复现其干扰抵消电路。[代尔夫特机构库](https://repository.tudelft.nl/record/uuid:d3912f8c-8e44-4c97-ace2-6974b8c570bb)

The ringing note describes a series parasitic loop initially, then a parallel-RLC approximation for snubber sizing. P07’s series critical resistance and the note’s snubber resistance are different formulas for different networks. [TI SLPA010](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

振铃笔记先描述串联寄生回路，再采用并联RLC近似进行吸收电路选值。P07串联临界电阻与笔记的吸收电阻属于不同网络，公式不能互换。[TI SLPA010](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

The Caltech current-programmed-converter abstract was rechecked; its PDF redirect failed. P09 omits sampled-cycle/slope-compensation behavior. ADI AN-1308’s body was read for common-mode step recovery, a mechanism omitted by low-side P05. [Caltech record](https://authors.library.caltech.edu/records/ac87w-mn171), [ADI AN-1308](https://www.analog.com/en/resources/app-notes/an-1308.html)

重新核对加州理工电流编程转换器摘要，PDF重定向失败；P09未包含逐周期采样及斜坡补偿。阅读了ADI AN-1308正文中的共模阶跃恢复；低侧P05未包含这一机理。[加州理工机构库](https://authors.library.caltech.edu/records/ac87w-mn171)、[ADI AN-1308](https://www.analog.com/en/resources/app-notes/an-1308.html)

Pelgrom’s IEEE PDF returned 502 during the new attempt. Historical targeted-reading metadata is retained, without claiming fresh full-text access. Remaining sources were checked against local model mappings but were not all reopened. This is a focused 20-model validity audit, not a renewed full-text audit of every TOP200 paper.

本次获取Pelgrom的IEEE PDF返回502；保留历史定向阅读记录，不宣称本次重新读到全文。其他来源核对了本地模型关联，但没有全部重新打开。本工作是20个模型的重点有效性审计，不是对TOP200每篇论文重新阅读全文。

## Per-model decisions / 逐模型结论

### A01 — Four-terminal MOS interpolation / 四端MOS连续插值

Low-voltage MOS: illustrative 0–1.8 V class; three assumed temperatures −40, 25, 125 °C. Terminal ranges below describe only saved sweeps.

低压MOS示意0–1.8 V等级；假设温度−40、25、125 °C。下列端口范围仅为已保存扫描。

Retain for DC interpolation, analytic small-signal derivatives and fixed-capacitor charge bookkeeping; do not use as an HV MOS or full EKV/BSIM model.

保留用于直流插值、小信号导数和固定电容电荷核算；不能当高压MOS或完整EKV/BSIM模型。

Cases: 9; direct model-specific tests: 2 current + 5 historical. Sources: B01. All linked tests pass; physical calibration remains unverified.

工况9项；直接关联测试：当前2项+历史5项；来源：B01。关联测试均通过，物理校准仍未验证。

### A02 — Junction charge and varactor / 结电荷与变容二极管

Junction law accepts −20 ≤ V < 0.35 V. Published C–V sweep is −10…0.3 V; transient −3…−1 V at 1 MHz; temperatures −40, 25, 125 °C.

结模型允许−20 ≤ V < 0.35 V；已发布C–V为−10…0.3 V，瞬态为1 MHz下−3…−1 V；温度−40、25、125 °C。

Retain for depletion C(V), integral charge and displacement current; exclude forward diffusion, reverse breakdown and series resistance.

保留用于耗尽电容、电荷积分和位移电流；不含正向扩散、反向击穿和串联电阻。

Cases: 6; direct model-specific tests: 2 current + 2 historical. Sources: B07. All linked tests pass; physical calibration remains unverified.

工况6项；直接关联测试：当前2项+历史2项；来源：B07。关联测试均通过，物理校准仍未验证。

### A03 — Reciprocal NPN Ebers–Moll / 满足互易关系的NPN Ebers–Moll

Reciprocal DC Ebers–Moll low-injection example at −40, 25, 125 °C; no qualified current, voltage or frequency rating.

−40、25、125 °C的互易Ebers–Moll低注入直流示例；无经过认证的电流、电压和频率额定值。

Retain for terminal KCL, forward gain and saturation reciprocity; no high-injection, Early effect, charge storage, breakdown or fT prediction.

保留用于端口KCL、正向增益和饱和互易性；不能预测高注入、Early效应、储存电荷、击穿或fT。

Cases: 6; direct model-specific tests: 0 current + 2 historical. Sources: B07. All linked tests pass; physical calibration remains unverified.

工况6项；直接关联测试：当前0项+历史2项；来源：B07。关联测试均通过，物理校准仍未验证。

### A04 — MOS pair mismatch and correlation / MOS配对失配与相关性

25 °C; areas 1, 4, 16, 64 µm²; 80,000 Gaussian samples each; assumed A_VT=3 mV·µm and correlation 0.25.

25 °C；面积1、4、16、64 µm²，每组80,000个高斯样本；假设A_VT=3 mV·µm、相关系数0.25。

Retain as a pair-mismatch statistics lesson. More samples reduce estimator uncertainty, not physical mismatch or guaranteed realized error.

保留为配对失配统计教学。增加样本仅降低估计不确定性，不降低器件失配，也不保证本次误差更小。

Cases: 4; direct model-specific tests: 1 current + 2 historical. Sources: B02. All linked tests pass; physical calibration remains unverified.

工况4项；直接关联测试：当前1项+历史2项；来源：B02。关联测试均通过，物理校准仍未验证。

### B01 — MOS differential pair / MOS差分对

A01 differential pair; 100 µA ideal tail, 0.85 V common mode, 1.8 V drains; differential input ±0.3 V; −40, 25, 125 °C.

A01差分对；理想尾电流100 µA、共模0.85 V、漏极1.8 V；差分输入±0.3 V；−40、25、125 °C。

Retain for current steering with an ideal tail; not a complete OTA/op-amp with finite tail resistance, active loads or compensation.

保留用于理想尾电流下的电流转向；不是包含有限尾源阻抗、有源负载和补偿的完整OTA/运放。

Cases: 3; direct model-specific tests: 0 current + 1 historical. Sources: B01. All linked tests pass; physical calibration remains unverified.

工况3项；直接关联测试：当前0项+历史1项；来源：B01。关联测试均通过，物理校准仍未验证。

### B02 — CTAT/PTAT reference sum / CTAT/PTAT基准合成

One continuous −40…125 °C sweep; first derivative cancelled at 25 °C; no supply or load qualification.

一个−40…125 °C连续扫描；25 °C处抵消一阶温度导数；未验证供电和负载能力。

Retain for CTAT/PTAT cancellation and residual curvature; not a transistor-level Brokaw circuit or measured precision reference.

保留用于CTAT/PTAT抵消与残余曲率；不是晶体管级Brokaw电路或实测精密基准。

Cases: 1; direct model-specific tests: 0 current + 2 historical. Sources: B03. All linked tests pass; physical calibration remains unverified.

工况1项；直接关联测试：当前0项+历史2项；来源：B03。关联测试均通过，物理校准仍未验证。

### B03 — Input noise and sampled kT/C / 输入噪声与采样kT/C

Noise PSD integrated over 1 Hz–1 MHz at −40, 25, 125 °C; 1 pF kT/C example; no terminal I–V operating range.

−40、25、125 °C下积分1 Hz–1 MHz噪声谱；1 pF的kT/C示例；无端口I–V适用范围。

Retain for PSD units and integration; prescribed noise shaping is not a switching chopper/auto-zero circuit.

保留用于噪声谱单位与积分；预设谱形不是开关斩波/自动调零电路。

Cases: 3; direct model-specific tests: 1 current + 1 historical. Sources: B08. All linked tests pass; physical calibration remains unverified.

工况3项；直接关联测试：当前1项+历史1项；来源：B08。关联测试均通过，物理校准仍未验证。

### B04 — Capacitor DAC and SAR ADC / 电容DAC与SAR ADC

10-bit SAR, 1.8 V reference, 2 MS/s, 25 °C; ideal and 2% unit-capacitor mismatch cases; ideal comparator and full settling.

10位SAR、1.8 V基准、2 MS/s、25 °C；理想和单位电容2%失配两种工况；比较器理想且完全建立。

Retain for quantization, actual code-transition DNL/INL and spectral metrics; no physical ENOB, reference loading or comparator timing claim.

保留用于量化、真实码转换DNL/INL和频谱指标；不宣称物理ENOB、基准负载或比较器时序能力。

Cases: 2; direct model-specific tests: 0 current + 6 historical. Sources: B05, B02. All linked tests pass; physical calibration remains unverified.

工况2项；直接关联测试：当前0项+历史6项；来源：B05, B02。关联测试均通过，物理校准仍未验证。

### B05 — LDO loop and load step / LDO环路与负载阶跃

3.3 V input, 1.8 V nominal output, 20 mA nominal load plus 10 mA step; 10 µF; −40, 25, 125 °C.

3.3 V输入、1.8 V标称输出、20 mA负载叠加10 mA阶跃；10 µF；−40、25、125 °C。

Retain as a two-state linearized loop/load-step bench; dropout, startup, saturation, ESR zeros and current limit are absent.

保留为两状态线性化环路/负载阶跃；不含压差、启动、饱和、ESR零点和限流。

Cases: 3; direct model-specific tests: 2 current + 4 historical. Sources: B06. All linked tests pass; physical calibration remains unverified.

工况3项；直接关联测试：当前2项+历史4项；来源：B06。关联测试均通过，物理校准仍未验证。

### B06 — Phase loop and noise transfer / 相位环路与噪声传递

25 °C; canonical phase-domain second-order system; natural frequency 100 kHz, damping 0.3/0.7/1.2, 0.1 rad step; noise band 100 Hz–10 MHz.

25 °C；标准二阶相位域系统；固有频率100 kHz、阻尼0.3/0.7/1.2、0.1 rad阶跃；噪声带100 Hz–10 MHz。

Retain for phase dynamics/noise-transfer lessons; not a complete type-II PLL, transistor VCO, acquisition or ISF paper reproduction.

保留用于相位动态和噪声传递；不是完整II型PLL、晶体管VCO、捕获过程或ISF论文复现。

Cases: 3; direct model-specific tests: 3 current + 3 historical. Sources: B09. All linked tests pass; physical calibration remains unverified.

工况3项；直接关联测试：当前3项+历史3项；来源：B09。关联测试均通过，物理校准仍未验证。

### B07 — 40–150 V synchronous buck / 40–150V同步降压

Six input classes 40/60/80/100/120/150 V × −40/25/125 °C; 12 V/1 A, 250 kHz, 100 µH, 22 µF; forced CCM.

40/60/80/100/120/150 V六档输入×−40/25/125 °C；12 V/1 A、250 kHz、100 µH、22 µF；强制连续导通。

Retain for switched KVL/KCL and conduction-only energy balance. Input classes are scenarios, not transistor voltage ratings.

保留用于开关KVL/KCL和仅导通损耗能量平衡。输入档位是工况，不是晶体管耐压等级。

Cases: 18; direct model-specific tests: 3 current + 4 historical. Sources: D01. All linked tests pass; physical calibration remains unverified.

工况18项；直接关联测试：当前3项+历史4项；来源：D01。关联测试均通过，物理校准仍未验证。

### P01 — HV MOS gate charge and switching overlap / 高压MOS栅电荷与开关交叠

Six input classes × −40/25/125 °C; 1 A prescribed commutation, 10 V drive, 8/5 Ω gate resistance.

六档输入×−40/25/125 °C；预设1 A换流、10 V驱动、8/5 Ω栅电阻。

Reclassify the legacy device_extension as a staged gate-charge/overlap bench. It is not a self-consistent charge-conserving multi-terminal HV MOS compact model.

将历史device_extension重分类为分阶段栅电荷/交叠损耗台架；不是自洽、端口电荷守恒的高压MOS紧凑模型。

Cases: 18; direct model-specific tests: 1 current + 6 historical. Sources: S01, S02, S10. All linked tests pass; physical calibration remains unverified.

工况18项；直接关联测试：当前1项+历史6项；来源：S01, S02, S10。关联测试均通过，物理校准仍未验证。

### P02 — Dead-time diode and reverse recovery / 死区二极管与反向恢复

Six input classes × −40/25/125 °C; 12 V/1 A, 250 kHz, 100 µH, 40 ns dead time; prescribed triangular recovery pulse.

六档输入×−40/25/125 °C；12 V/1 A、250 kHz、100 µH、40 ns死区；预设三角形反向恢复脉冲。

Reclassify as a mechanism bench. Qrr pulse and inductor commutation are not a coupled minority-carrier diode model; VIN×Qrr is bus energy, not diode heat.

重分类为机制台架；Qrr脉冲和电感换流不是耦合少子二极管模型；VIN×Qrr是母线能量，不是二极管发热。

Cases: 18; direct model-specific tests: 0 current + 3 historical. Sources: S02. All linked tests pass; physical calibration remains unverified.

工况18项；直接关联测试：当前0项+历史3项；来源：S02。关联测试均通过，物理校准仍未验证。

### P03 — Floating bootstrap supply and UVLO margin / 浮地自举供电与欠压裕量

Six input classes × −40/25/125 °C × 100 nF/3.3 nF; 10 V supply, 6 V UVLO, 250 kHz; VBS is relative to SW.

六档输入×−40/25/125 °C×100 nF/3.3 nF；10 V供电、6 V欠压门槛、250 kHz；VBS相对SW。

Retain for charge-budget/RC recharge margin. UVLO is a diagnostic flag only and does not suppress the prescribed gate pulses.

保留用于电荷预算和RC补充电裕量；UVLO只作诊断标志，不会抑制预设栅脉冲。

Cases: 36; direct model-specific tests: 0 current + 2 historical. Sources: S01, S03. All linked tests pass; physical calibration remains unverified.

工况36项；直接关联测试：当前0项+历史2项；来源：S01, S03。关联测试均通过，物理校准仍未验证。

### P04 — Level-shifter common-mode disturbance / 电平移位接收端共模扰动

Six common-mode steps at 10 V/ns; 25 °C only; receiver R=20 kΩ/500 Ω, threshold 0.7 V; unclamped linear RC.

六档共模阶跃、10 V/ns；仅25 °C；接收电阻20 kΩ/500 Ω、门槛0.7 V；无钳位线性RC。

Retain as a disturbance diagnostic. Weak-path multi-volt excursions are predictions of an unclamped equivalent, not physical logic-pin or CMTI qualification.

保留为扰动诊断；弱通路的数伏偏移仅为无钳位等效模型结果，不能当逻辑引脚真实波形或CMTI认证。

Cases: 12; direct model-specific tests: 0 current + 2 historical. Sources: S04, S10. All linked tests pass; physical calibration remains unverified.

工况12项；直接关联测试：当前0项+历史2项；来源：S04, S10。关联测试均通过，物理校准仍未验证。

### P05 — Current-sense amplifier and delayed comparator / 电流检测放大器与延迟比较器

Low-side only: 0.5→3 A, 50 mΩ nominal shunt, gain 20, 100 ns pole, assumed 35 ns comparator delay; −40/25/125 °C. No Vin sweep.

仅低侧：0.5→3 A、标称50 mΩ取样电阻、增益20、100 ns时间常数、假设35 ns比较器延迟；−40/25/125 °C。未扫描Vin。

Retain for first-order detection timing. It is not an INA381 model and provides no 150 V high-side sensing or actual switch turn-off validation.

保留用于一阶检测时序；不是INA381模型，不能验证150 V高侧检测或实际开关关断。

Cases: 3; direct model-specific tests: 1 current + 1 historical. Sources: S05, S12. All linked tests pass; physical calibration remains unverified.

工况3项；直接关联测试：当前1项+历史1项；来源：S05, S12。关联测试均通过，物理校准仍未验证。

### P06 — HV startup supply and hysteretic UVLO / 高压启动供电与迟滞欠压锁定

Six input classes × −40/25/125 °C; 1 µF auxiliary capacitor; assumed 1 mA source; 9/7 V UVLO; 11 V clamp; 14–24 ms source interruption.

六档输入×−40/25/125 °C；1 µF辅助电容；假设1 mA电流源；9/7 V欠压门槛；11 V钳位；14–24 ms断供。

Retain for event-driven bias startup/UVLO. No JFET physics, auxiliary-winding takeover or 150 V hardware rating is represented.

保留用于事件驱动的偏置启动/欠压锁定；不含JFET物理、辅助绕组接管或150 V硬件耐压。

Cases: 18; direct model-specific tests: 3 current + 3 historical. Sources: S06, S11. All linked tests pass; physical calibration remains unverified.

工况18项；直接关联测试：当前3项+历史3项；来源：S06, S11。关联测试均通过，物理校准仍未验证。

### P07 — Switch-node parasitic ringing and damping / 开关节点寄生振铃与阻尼

Six input classes at 25 °C; series RLC, 15 nH, bias-linearized Coss, initial excess voltage 0.15 Vin; weak/damped cases.

六档输入、25 °C；串联RLC、15 nH、偏置点线性化Coss、初始过电压0.15 Vin；弱/强阻尼工况。

Retain for free-response damping and energy. Rcritical=2√(L/C) is for series RLC; do not copy it into the source note’s parallel-RLC snubber design.

保留用于自由响应阻尼与能量；Rcritical=2√(L/C)属于串联RLC，不能套入来源应用笔记的并联RLC吸收电路。

Cases: 12; direct model-specific tests: 1 current + 2 historical. Sources: S07. All linked tests pass; physical calibration remains unverified.

工况12项；直接关联测试：当前1项+历史2项；来源：S07。关联测试均通过，物理校准仍未验证。

### P08 — DC/DC separated losses and thermal budget / DC/DC分项损耗与热预算

Six input classes × ambient −40/25/125 °C; 12 V/1 A, 250 kHz; Rθ=8 K/W, Cθ=0.025 J/K; assumed coefficient range −40…175 °C.

六档输入×环境−40/25/125 °C；12 V/1 A、250 kHz；热阻8 K/W、热容0.025 J/K；假设系数范围−40…175 °C。

Retain as a nine-term loss ledger plus one effective hot node. It does not predict an individual device junction or full switching electrothermal dynamics.

保留为九项损耗账本加一个等效热节点；不能预测单个器件结温或完整开关电热动态。

Cases: 18; direct model-specific tests: 1 current + 3 historical. Sources: S01, S02, S08. All linked tests pass; physical calibration remains unverified.

工况18项；直接关联测试：当前1项+历史3项；来源：S01, S02, S08。关联测试均通过，物理校准仍未验证。

### P09 — Averaged buck soft-start and current-reference limit / 平均Buck软启动与电流参考限幅

Six input classes × −40/25/125 °C; averaged 12 V buck, 1.6 A command limit, load 12→6 Ω at 4 ms; 2 ms soft-start.

六档输入×−40/25/125 °C；平均12 V降压、1.6 A指令限幅、4 ms时负载12→6 Ω；2 ms软启动。

Retain for averaged soft-start and intentional overload droop. No PWM ripple, cycle-by-cycle peak limit, slope compensation or subharmonic stability prediction.

保留用于平均软启动和有意过载压降；不能预测PWM纹波、逐周期峰值限流、斜坡补偿和次谐波稳定性。

Cases: 18; direct model-specific tests: 2 current + 2 historical. Sources: S06, S09. All linked tests pass; physical calibration remains unverified.

工况18项；直接关联测试：当前2项+历史2项；来源：S06, S09。关联测试均通过，物理校准仍未验证。

## Next scientific validation gates / 后续科学验证条件

1. Obtain authorized PDK or measured I–V/C–V/Qg/Qrr/SOA/thermal data, with units, bias, temperature and provenance. Fit on one subset and validate on a held-out subset before reporting physical error percentages.
2. Replace P01/P02 with coupled terminal-charge/commutation models if actual switching prediction is required. Add avalanche, breakdown and safe operating area only with supporting data.
3. Add closed-loop UVLO behavior to P03, explicit rail clamps/device input behavior to P04, and common-mode recovery plus output limits to P05 before treating those signals as realizable hardware waveforms.
4. For 40–150 V product claims, combine transient stress, isolation, device ratings, parasitics, temperature and reliability evidence; the six Vin scenarios alone cannot qualify a process.
5. Keep beginner analogies, undergraduate equations and graduate error/identifiability analysis separate. Every lesson should distinguish assumptions, numerical reference and missing physical evidence.

1. 获取获授权PDK或实测I–V/C–V/Qg/Qrr/SOA/热数据，记录单位、偏置、温度与出处；训练子集拟合、独立留出子集验证后，才能报告物理误差百分比。
2. 若需预测真实开关过程，应把P01/P02换成端口电荷/换流耦合模型；有数据支持后再加入雪崩、击穿和安全工作区。
3. P03增加闭环UVLO，P04增加明确电源钳位/输入器件行为，P05增加共模恢复和输出限制，再把相应波形用于硬件判断。
4. 40–150 V产品能力需共同验证瞬态应力、隔离、器件额定值、寄生、温度和可靠性；六档输入工况不能单独认证工艺。
5. 入门类比、本科方程、研究生误差/可辨识性分析应分层；每课均区分假设、数值参考与缺失的物理证据。

Machine-readable evidence: [validity JSON](validity_audit.json), [DC/DC case metrics](dcdc_case_audit.csv); isolated execution logs and hashes: [execution summary](rerun.json).

机器可读证据：[validity JSON](validity_audit.json)、[DC/DC case metrics](dcdc_case_audit.csv)；隔离执行日志与哈希：[execution summary](rerun.json)。
