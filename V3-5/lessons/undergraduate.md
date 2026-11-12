# Undergraduate — define and calculate

# 本科版——定义与计算

Define quantities and units, apply the stated conditions, and solve one short problem.

定义量及单位，在适用条件下完成一道小练习。

V3-5 teaching edition of the existing v3.3.0 numerical baseline: 20 views comprise 3 illustrative device models, 1 statistical demonstration, 2 prescribed mechanism benches and 14 circuit/system benches. The 75 printable entries include these 20 plus 55 legacy/background representations; they are not 75 independently calibrated devices. The release audit separately records reruns of the current numerical baseline. This teaching content adds no new physics, PDK, silicon fit or physical-accuracy gain.

V3-5是现有v3.3.0数值基线的教学版本：20个视图含3个示意器件、1个统计演示、2个预设机制测试台及14个电路/系统测试台。75个打印条目包含上述20项与55项旧版/背景表示，并非75种独立校准器件。发布审计另行记录现有数值基线重跑；本教学内容未新增物理机制、PDK、硅实测拟合或物理准确度提高。

## Before you begin

## 阅读前

Use SI units: A for current, V for voltage, Ω for resistance, F for capacitance, H for inductance, W for power and J for energy. Absolute temperature in thermal/exponential laws is kelvin.

使用SI单位：电流A、电压V、电阻Ω、电容F、电感H、功率W、能量J。热学及指数式中的绝对温度使用开尔文。

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

**Definition / 定义**

Transconductance is the local sensitivity of drain current to gate voltage at fixed other terminal voltages.

跨导是其他端口电压固定时，漏电流对栅压的局部变化率。

**Equation / 公式**

g_m = ∂I_D/∂V_G; ΔI_D ≈ g_m ΔV_G

Units / 单位: I_D: A; V_G: V; g_m: S = A/V

**Conditions / 适用条件**

Use a small perturbation around one bias point in this 0–1.8 V interpolation. Pair capacitances are fixed; intrinsic charge partition is absent.

用于0–1.8 V插值模型某偏置点附近的小扰动。互电容固定，未包含内禀电荷分配。

**Exercise / 练习**

At g_m = 1 mS, estimate ΔI_D for a 10 mV gate change.

跨导为1 mS，栅压变化10 mV，估算漏电流变化。

**Answer / 答案**

ΔI_D ≈ 10 µA; this is a local linear estimate, not a whole-sweep slope.

ΔI_D约为10 µA；这是局部线性估算，并非整个扫描的恒定斜率。

Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

## A02 — Junction charge and varactor

结电荷与变容二极管

[GIF: A02_CV_25C](../simulation/V3-3/education/gifs/A02.gif) · [STL: V33_A02](../printing/stl/V33_A02.stl)

**Definition / 定义**

Junction differential capacitance is dQ/dV. Nonlinear stored charge is an integral, not generally C(V)V.

结的微分电容为dQ/dV；非线性储存电荷应通过积分求得，通常不等于C(V)V。

**Equation / 公式**

C(V)=C0(1−V/φ)^(−m); Q(V)=∫₀^V C(u)du; i=C(V)dV/dt

Units / 单位: C,C0: F; Q: C; V,φ: V; i: A; m: dimensionless

**Conditions / 适用条件**

Depletion-only model: −20 V ≤ V < 0.35 V; C0 = 2 pF, φ = 0.7 V, m = 0.5 at 25 °C. Forward diffusion charge is excluded.

仅耗尽电容：−20 V≤V<0.35 V；25 °C下C0=2 pF、φ=0.7 V、m=0.5；不含正向扩散电荷。

**Exercise / 练习**

Find capacitance at V = −2.1 V using the stated 25 °C parameters.

用上述25 °C参数求V=−2.1 V时的电容。

**Answer / 答案**

C = 2 pF/√4 = 1 pF. This is differential capacitance at that bias.

C=2 pF/√4=1 pF，这是该偏置下的微分电容。

Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

## A03 — Reciprocal NPN Ebers–Moll

满足互易关系的NPN Ebers–Moll

[GIF: A03_gummel_25C](../simulation/V3-3/education/gifs/A03.gif) · [STL: V33_A03](../printing/stl/V33_A03.stl)

**Definition / 定义**

The Ebers–Moll model combines forward and reverse junction injection and enforces three-terminal current conservation.

Ebers–Moll模型叠加正、反向结注入，并满足三端电流守恒。

**Equation / 公式**

I_C=α_F I_F−I_R; I_B=(1−α_F)I_F+(1−α_R)I_R; I_E=−I_F+α_R I_R; β_F=α_F/(1−α_F)

Units / 单位: I_C,I_B,I_E,I_F,I_R: A; α_F,α_R,β_F: dimensionless

**Conditions / 适用条件**

Currents are positive into the device. This generic silicon NPN is low-injection DC only; reciprocity requires α_F I_ES = α_R I_CS.

电流以流入器件为正。通用硅NPN仅用于低注入直流；互易关系要求α_F I_ES=α_R I_CS。

**Exercise / 练习**

In forward-active operation with β_F = 100 and I_C = 1 mA, estimate I_B and I_E, neglecting reverse injection.

正向放大区β_F=100、I_C=1 mA，忽略反向注入，估算I_B及I_E。

**Answer / 答案**

I_B ≈ 10 µA and I_E ≈ −1.01 mA; their sum with I_C is zero.

I_B约为10 µA、I_E约为−1.01 mA；三端电流之和为零。

Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

## A04 — MOS pair mismatch and correlation

MOS配对失配与相关性

[GIF: A04_area16um2](../simulation/V3-3/education/gifs/A04.gif) · [STL: V33_A04](../printing/stl/V33_A04.stl)

**Definition / 定义**

Pair mismatch is a difference of two device parameters; shared variation can cancel, while local variation remains.

配对失配是两个器件参数之差；共同变化可相消，局部差异仍存在。

**Equation / 公式**

σ_pair=A_VT√[(1−ρ)/(WL)]

Units / 单位: σ_pair: V; A_VT: V·µm; W,L: µm; ρ: dimensionless

**Conditions / 适用条件**

The repository defines A_VT as a pair coefficient. Gaussian local terms, equal areas and assumed correlation are used; do not mix this convention with a single-device coefficient.

本库将A_VT定义为配对系数。假设局部高斯分布、等面积及相关性；不可与单管系数约定混用。

**Exercise / 练习**

For A_VT=3 mV·µm, WL=16 µm² and ρ=0.25, find σ_pair.

A_VT=3 mV·µm、WL=16 µm²、ρ=0.25，求配对标准差。

**Answer / 答案**

σ_pair = 0.6495 mV. Quadrupling area halves this predicted standard deviation.

σ_pair=0.6495 mV；面积增加至四倍时，该预测标准差减半。

Sources / 来源: [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

## B01 — MOS differential pair

MOS差分对

[GIF: B01_25C](../simulation/V3-3/education/gifs/B01.gif) · [STL: V33_B01](../printing/stl/V33_B01.stl)

**Definition / 定义**

A MOS differential pair converts differential input voltage into a branch-current difference.

MOS差分对将差分输入电压转换为支路电流之差。

**Equation / 公式**

V_G1,2=V_CM±V_diff/2; I_1+I_2=I_tail; Δ(I_1−I_2)≈g_m V_diff

Units / 单位: V_G,V_CM,V_diff: V; I_1,I_2,I_tail: A; g_m: S (each device at balance)

**Conditions / 适用条件**

The small-signal relation assumes a matched, balanced pair; full sweeps solve A01 with fixed drains and an ideal tail source.

小信号关系要求匹配、平衡；完整扫描调用A01，固定漏端电压，尾源理想。

**Exercise / 练习**

At zero differential input and a 100 µA ideal tail, what are the currents of a matched pair?

差分输入为零、理想尾电流为100 µA，匹配支路各有多少电流？

**Answer / 答案**

I_1 = I_2 = 50 µA. This does not specify an output voltage gain without loads.

I_1=I_2=50 µA；没有负载时，不能由此指定输出电压增益。

Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

## B02 — CTAT/PTAT reference sum

CTAT/PTAT基准合成

[GIF: B02_temperature](../simulation/V3-3/education/gifs/B02.gif) · [STL: V33_B02](../printing/stl/V33_B02.stl)

**Definition / 定义**

CTAT decreases with absolute temperature; PTAT is proportional to absolute temperature. Their weighted sum cancels first-order drift near a design point.

CTAT随绝对温度下降，PTAT与绝对温度成正比；加权合成可在设计温度附近抵消一阶温漂。

**Equation / 公式**

U_T=kT/q; ΔV_BE=U_T ln N; V_ref=V_BE+aΔV_BE

Units / 单位: T: K; U_T,V_BE,V_ref: V; k: J/K; q: C; N,a: dimensionless

**Conditions / 适用条件**

Matched junctions with a current-density ratio N motivate the relation. Here the sum is ideal; startup, resistor TC, PSRR and trimming are absent.

关系式基于匹配结的电流密度比N；此处为理想求和，未含启动、电阻温漂、电源抑制和修调。

**Exercise / 练习**

At 298.15 K with N=8, estimate ΔV_BE using k/q=86.1733 µV/K.

T=298.15 K、N=8，取k/q=86.1733 µV/K，估算ΔV_BE。

**Answer / 答案**

ΔV_BE ≈ 53.42 mV. This PTAT term alone is not the full reference voltage.

ΔV_BE约53.42 mV；该PTAT项本身并不是完整参考电压。

Sources / 来源: [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf)

## B03 — Input noise and sampled kT/C

输入噪声与采样kT/C

[GIF: B03_25C](../simulation/V3-3/education/gifs/B03.gif) · [STL: V33_B03](../printing/stl/V33_B03.stl)

**Definition / 定义**

Voltage PSD integrates to variance; amplitude spectral density is its square root. An equilibrated sampled capacitor has thermal variance kT/C.

电压功率谱密度积分得到方差，幅度谱密度是其平方根；达到热平衡的采样电容热噪声方差为kT/C。

**Equation / 公式**

v_rms²=∫[f1,f2] S_v(f)df; S_v=ASD²; v_sample,rms=√(kT/C)

Units / 单位: S_v: V²/Hz; ASD: V/√Hz; f: Hz; C: F; T: K; k: J/K; v_rms: V

**Conditions / 适用条件**

One-sided PSD and the stated finite band are used. kT/C is a separate ideal sampling result, not another term already included in the plotted amplifier spectrum.

采用单边谱和规定的有限频带；kT/C是另列的理想采样结果，未重复计入图中的放大器频谱。

**Exercise / 练习**

For T=300 K and C=1 pF, estimate sampled thermal rms voltage.

T=300 K、C=1 pF，估算采样热噪声电压有效值。

**Answer / 答案**

√(1.380649×10⁻²³×300/10⁻¹²) ≈ 64.36 µV. Four times the capacitance halves this value.

结果约64.36 µV；电容增为四倍时，该电压减半。

Sources / 来源: [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

## B04 — Capacitor DAC and SAR ADC

电容DAC与SAR ADC

[GIF: B04_mismatch](../simulation/V3-3/education/gifs/B04.gif) · [STL: V33_B04](../printing/stl/V33_B04.stl)

**Definition / 定义**

A SAR ADC tests binary capacitor-DAC weights sequentially. DNL describes code-width error; INL describes transition deviation from a stated reference line.

SAR ADC逐次测试二进制电容DAC权重；DNL描述码宽误差，INL描述转换边界相对指定参考直线的偏离。

**Equation / 公式**

LSB=V_ref/2^N; DNL_k=(T_(k+1)−T_k)/LSB−1

Units / 单位: V_ref,T_k,LSB: V; N: bits; DNL: LSB units (dimensionless numeric value)

**Conditions / 适用条件**

The baseline is a 10-bit binary CDAC with dummy capacitance, ideal comparison and full settling. Endpoint INL uses first/last internal transitions.

基线为含dummy电容的10位二进制CDAC，比较器理想且充分建立；端点INL以首末内部转换点拟合。

**Exercise / 练习**

For an ideal 10-bit converter with V_ref=1.8 V, find 1 LSB.

理想10位转换器V_ref=1.8 V，求1 LSB。

**Answer / 答案**

1 LSB = 1.7578125 mV. Mismatch changes actual code widths, so this remains the nominal step.

1 LSB=1.7578125 mV；失配改变实际码宽，因此该值是标称步长。

Sources / 来源: [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

## B05 — LDO loop and load step

LDO环路与负载阶跃

[GIF: B05_25C](../simulation/V3-3/education/gifs/B05.gif) · [STL: V33_B05](../printing/stl/V33_B05.stl)

**Definition / 定义**

An LDO feedback loop adjusts pass current to oppose output-voltage disturbances. Here v and i_p are deviations from a biased operating point.

LDO反馈环调节通过电流以抵消输出电压扰动；此处v和i_p为偏置工作点附近的增量。

**Equation / 公式**

C dv/dt=i_p−v/R−ΔI_load; di_p/dt=ω_a(−Gv−i_p)

Units / 单位: v: V; i_p,ΔI_load: A; C: F; R: Ω; G: A/V; ω_a: rad/s; t: s

**Conditions / 适用条件**

Two-state linear model with no dropout, saturation, ESR zero or current limit. Large supply/load excursions exceed its scope.

二状态线性模型，无压差极限、饱和、ESR零点及限流；大幅电源或负载变化超出范围。

**Exercise / 练习**

Immediately after a +10 mA load step with C=10 µF, before pass current changes, find dv/dt.

C=10 µF，负载突然增加10 mA，在通过电流尚未改变的瞬间，求dv/dt。

**Answer / 答案**

dv/dt = −1000 V/s = −1 mV/µs, using incremental v=i_p=0 just before the step.

dv/dt=−1000 V/s=−1 mV/µs，取阶跃前增量v=i_p=0。

Sources / 来源: [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf)

## B06 — Phase loop and noise transfer

相位环路与噪声传递

[GIF: B06_zeta0.7](../simulation/V3-3/education/gifs/B06.gif) · [STL: V33_B06](../printing/stl/V33_B06.stl)

**Definition / 定义**

Phase is position within an oscillation cycle. A canonical second-order loop filters reference phase and complementary oscillator phase disturbances.

相位描述振荡周期中的位置；典型二阶环路滤波参考相位及互补的振荡器相位扰动。

**Equation / 公式**

H(s)=ω_n²/(s²+2ζω_n s+ω_n²); σ_t=σ_φ/(2πf_carrier)

Units / 单位: s,ω_n: s⁻¹; ζ,H: dimensionless; σ_φ: rad; f_carrier: Hz; σ_t: s

**Conditions / 适用条件**

Small phase perturbations and uncorrelated reference/VCO spectra; this model has no loop zero and is not a complete type-II PLL.

小相位扰动，参考/VCO噪声互不相关；此模型无环路零点，不是完整二型PLL。

**Exercise / 练习**

Convert 1 mrad rms phase error into rms time jitter at 1 GHz.

1 GHz载波下，将1 mrad相位误差有效值换算为时间抖动有效值。

**Answer / 答案**

σ_t ≈ 159.15 fs. This conversion does not specify the integration bandwidth of a measured jitter result.

σ_t约159.15 fs；该换算本身没有指定实测抖动的积分频带。

Sources / 来源: [base:B09](https://chic.caltech.edu/wp-content/uploads/2013/05/general.pdf)

## B07 — 40–150 V synchronous buck

40–150V同步降压

[GIF: B07_100V_25C](../simulation/V3-3/education/gifs/B07.gif) · [STL: V33_B07](../printing/stl/V33_B07.stl)

**Definition / 定义**

A synchronous buck alternates high- and low-side switches; in forced continuous conduction, inductor current follows piecewise circuit equations.

同步降压器交替控制高、低侧开关；强制连续导通时，电感电流遵循分段电路方程。

**Equation / 公式**

L di/dt=uV_in−(R_sw+R_L)i−v; C dv/dt=i−v/R_load; ideal D≈V_out/V_in

Units / 单位: L: H; C: F; R: Ω; i: A; v,V_in,V_out: V; u: 0 or 1; D: dimensionless

**Conditions / 适用条件**

Instantaneous switches and fixed duty; only conduction loss is included. D=V_out/V_in is the lossless approximation, not the exact resistive case.

开关瞬时切换、占空比固定；只计算导通损耗。D=V_out/V_in为无损近似，并非含电阻情况的精确值。

**Exercise / 练习**

For an ideal 100 V to 12 V buck at 250 kHz, find duty and high-side on-time.

理想100 V降至12 V、250 kHz降压器，求占空比及高侧导通时间。

**Answer / 答案**

D=0.12 and t_on=0.48 µs. The saved resistive 100 V case instead uses D≈0.123.

D=0.12，t_on=0.48 µs；已保存的含电阻100 V工况使用D约0.123。

Sources / 来源: [base:D01](../simulation/V3-3/MODEL_CARDS.md)

## P01 — HV MOS gate charge and switching overlap

高压MOS栅电荷与开关交叠

[GIF: P01_100V_25C](../simulation/V3-3/education/gifs/P01.gif) · [STL: V33_P01](../printing/stl/V33_P01.stl)

**Definition / 定义**

Miller charge is the gate-drain charge transferred during a drain-voltage transition; finite gate current sets its transition time.

Miller电荷是漏压变化期间转移的栅漏电荷；有限栅电流决定转换时间。

**Equation / 公式**

Q_gd=∫C_gd(v)dv; I_g≈(V_drive−V_plateau)/R_g; t_M≈Q_gd/I_g; E_oss=∫₀^V vC_oss(v)dv

Units / 单位: Q_gd: C; C_gd,C_oss: F; I_g: A; R_g: Ω; V: V; t_M: s; E_oss: J

**Conditions / 适用条件**

Plateau current is treated as constant and switching stages are prescribed. Nonlinear capacitance requires integration; E_oss is not generally ½C_oss(V)V².

平台电流视为恒定，开关阶段预先规定；非线性电容必须积分，E_oss通常不等于½C_oss(V)V²。

**Exercise / 练习**

For Q_gd=4 nC, V_drive=10 V, V_plateau=4 V and R_g=10 Ω, estimate t_M.

Q_gd=4 nC、驱动10 V、平台4 V、R_g=10 Ω，估算Miller时间。

**Answer / 答案**

I_g=0.6 A and t_M≈6.67 ns; illustrative exercise values differ from the recorded case.

I_g=0.6 A，t_M约6.67 ns；本练习假设值与保存工况不同。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

## P02 — Dead-time diode and reverse recovery

死区二极管与反向恢复

[GIF: P02_100V_25C](../simulation/V3-3/education/gifs/P02.gif) · [STL: V33_P02](../printing/stl/V33_P02.stl)

**Definition / 定义**

Dead time prevents simultaneous switch commands but permits diode conduction. Reverse-recovery charge is the time integral of reverse recovery current.

死区避免上下管同时收到导通指令，但可产生二极管导通；反向恢复电荷为恢复电流的时间积分。

**Equation / 公式**

Q_rr=I_pk t_rr/2; E_bus,rr≈V_in Q_rr; P_dead≈2t_d f_s V_F I_out

Units / 单位: Q_rr: C; I_pk,I_out: A; t_rr,t_d: s; V_in,V_F: V; f_s: Hz; E: J; P: W

**Conditions / 适用条件**

A triangular prescribed recovery pulse and CCM are assumed. V_in Q_rr is a full-bus energy estimate, not measured diode heat.

假设三角恢复脉冲及连续导通；V_in Q_rr为全母线换流能量估算，并非实测二极管发热。

**Exercise / 练习**

Q_rr=12 nC and t_rr=60 ns. Find I_pk and the bus-energy estimate at 100 V.

Q_rr=12 nC、t_rr=60 ns，求峰值恢复电流及100 V下母线能量估算。

**Answer / 答案**

I_pk=0.4 A; E_bus,rr≈1.2 µJ. Do not label the latter as heat in one diode.

I_pk=0.4 A，母线能量约1.2 µJ；不能把后者标为单只二极管的热量。

Sources / 来源: [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

## P03 — Floating bootstrap supply and UVLO margin

浮地自举供电与欠压裕量

[GIF: P03_100V_25C](../simulation/V3-3/education/gifs/P03.gif) · [STL: V33_P03](../printing/stl/V33_P03.stl)

**Definition / 定义**

A bootstrap capacitor powers the floating high-side driver; its differential voltage V_BS=V_B−V_S must retain adequate supply margin.

自举电容为浮动高侧驱动供电；差分电压V_BS=V_B−V_S须保持足够的供电裕量。

**Equation / 公式**

ΔV_BS=−Q_g/C_boot; ΔV_quiescent=−I_q t_on/C_boot; τ_recharge=R_charge C_boot

Units / 单位: Q_g: C; C_boot: F; I_q: A; t_on,τ: s; R_charge: Ω; ΔV: V

**Conditions / 适用条件**

Gate charge is an impulse and recharge is an RC exponential. UVLO is a margin flag here; it does not suppress gate pulses.

栅电荷作为脉冲消耗，补充过程为RC指数充电；此处UVLO仅标记裕量，不会停止栅脉冲。

**Exercise / 练习**

A 10 nC event draws charge from 100 nF. Ignoring other loads, what is the voltage drop?

10 nC电荷从100 nF电容抽取，忽略其他负载，电压下降多少？

**Answer / 答案**

|ΔV|=0.10 V. Add quiescent and leakage charge when doing a complete budget.

下降0.10 V；完整预算还须计入静态和漏电消耗。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

## P04 — Level-shifter common-mode disturbance

电平移位接收端共模扰动

[GIF: P04_100V_25C_strong](../simulation/V3-3/education/gifs/P04.gif) · [STL: V33_P04](../printing/stl/V33_P04.stl)

**Definition / 定义**

Common-mode slew injects displacement current through parasitic capacitance; receiver impedance converts it into a differential disturbance.

共模电压变化通过寄生电容注入位移电流，接收端阻抗将其变为差模扰动。

**Equation / 公式**

(C_rx+C_cm)dV_rx/dt+V_rx/R_rx=C_cm dV_cm/dt

Units / 单位: C_rx,C_cm: F; V_rx,V_cm: V; R_rx: Ω; dV/dt: V/s

**Conditions / 适用条件**

Unclamped linear RC only. Excursions beyond real supply rails indicate invalid extrapolation; no latch, clamp or CMTI test is implemented.

仅未钳位线性RC模型；越过实际电源轨的值提示外推失效；未实现锁存、钳位或CMTI测试。

**Exercise / 练习**

For C_cm=30 fF and slew=10 V/ns, find injected current.

C_cm=30 fF、变化率10 V/ns，求注入电流。

**Answer / 答案**

I=C_cm·slew=0.30 mA; receiver voltage additionally depends on R, C and edge duration.

I=0.30 mA；接收端电压还取决于R、C及边沿持续时间。

Sources / 来源: [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

## P05 — Current-sense amplifier and delayed comparator

电流检测放大器与延迟比较器

[GIF: P05_25C](../simulation/V3-3/education/gifs/P05.gif) · [STL: V33_P05](../printing/stl/V33_P05.stl)

**Definition / 定义**

A shunt converts current into voltage; finite amplifier bandwidth and comparator delay determine detection timing.

分流电阻把电流转为电压，放大器有限带宽和比较器延迟决定检测时刻。

**Equation / 公式**

V_s=R_s I; τ dV_a/dt+V_a=G R_s I+V_os; I_trip,DC=(V_th−V_os)/(G R_s)

Units / 单位: R_s: Ω; I: A; V_s,V_a,V_os,V_th: V; G: dimensionless; τ: s

**Conditions / 适用条件**

Low-side, linear, ground-referenced bench. V_os is applied at the amplifier output in this equation; no saturation or real shutdown loop exists.

低侧、线性、地参考测试台；此式V_os加在放大器输出侧，没有饱和或真实关断闭环。

**Exercise / 练习**

With G=20, R_s=0.05 Ω, V_th=2 V and V_os=1 mV, find the DC trip current.

G=20、R_s=0.05 Ω、V_th=2 V、V_os=1 mV，求直流触发电流。

**Answer / 答案**

I_trip,DC=1.999 A. The transient alert occurs later because bandwidth and propagation delay matter.

直流触发电流1.999 A；瞬态告警会因带宽和传播延迟而更晚。

Sources / 来源: [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

## P06 — HV startup supply and hysteretic UVLO

高压启动供电与迟滞欠压锁定

[GIF: P06_100V_25C](../simulation/V3-3/education/gifs/P06.gif) · [STL: V33_P06](../printing/stl/V33_P06.stl)

**Definition / 定义**

Startup current charges an auxiliary supply; UVLO hysteresis uses distinct enable and disable thresholds to avoid immediate toggling.

启动电流给辅助供电电容充电，UVLO迟滞采用不同开启和关闭阈值以避免立即反复翻转。

**Equation / 公式**

C_aux dV_aux/dt=I_start−I_load−I_clamp; Δt=C_aux ΔV/I_net (constant I_net)

Units / 单位: C_aux: F; V_aux: V; I_start,I_load,I_clamp,I_net: A; Δt: s

**Conditions / 适用条件**

Behavioral current source with compliance and an ideal 11 V clamp; 9 V enable/7 V disable. Constant-current timing applies only before compliance or state changes.

行为电流源具有顺从限制，11 V理想钳位，9 V开启、7 V关闭；恒流计时仅适用于顺从限制或状态切换前。

**Exercise / 练习**

Starting at 0 V, C_aux=1 µF, I_start=1 mA and disabled load=40 µA. How long to 9 V if compliance permits?

从0 V开始，C_aux=1 µF、启动1 mA、关闭时负载40 µA；若电流源顺从范围允许，多久达到9 V？

**Answer / 答案**

I_net=0.96 mA; t=9.375 ms. Use different net current after enable.

净电流0.96 mA，时间9.375 ms；开启后须改用新的净电流。

Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

## P07 — Switch-node parasitic ringing and damping

开关节点寄生振铃与阻尼

[GIF: P07_100V_damped](../simulation/V3-3/education/gifs/P07.gif) · [STL: V33_P07](../printing/stl/V33_P07.stl)

**Definition / 定义**

A series RLC free response transfers energy between capacitor and inductor; resistance dissipates it.

串联RLC自由响应在电容与电感间交换能量，由电阻耗散。

**Equation / 公式**

R_critical=2√(L/C); E=½Cv²+½Li²; dE/dt=−Ri²

Units / 单位: R: Ω; L: H; C: F; v: excess V around bus; i: A; E: J; t: s

**Conditions / 适用条件**

Linearized series RLC about the bus, prescribed initial disturbance. The critical resistance is not a value to copy into a parallel RC snubber.

母线附近的线性化串联RLC，初始扰动预设；该临界电阻不能照搬到并联RC吸收器。

**Exercise / 练习**

For L=15 nH and C=250 pF, find series critical resistance.

L=15 nH、C=250 pF，求串联临界电阻。

**Answer / 答案**

R_critical≈15.49 Ω. The actual recorded capacitance depends on the input-bias assumption.

临界电阻约15.49 Ω；已保存工况的电容随输入偏置假设而变。

Sources / 来源: [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

## P08 — DC/DC separated losses and thermal budget

DC/DC分项损耗与热预算

[GIF: P08_100V_25C](../simulation/V3-3/education/gifs/P08.gif) · [STL: V33_P08](../printing/stl/V33_P08.stl)

**Definition / 定义**

A loss ledger sums distinct energy mechanisms; a thermal resistance/capacitance converts assumed loss into an effective temperature rise.

损耗账本对不同能量机制分别求和，热阻/热容把假设损耗换算为等效温升。

**Equation / 公式**

T_hot=T_amb+R_θ P_loss; τ_θ=R_θ C_θ; η=P_out/(P_out+P_loss)

Units / 单位: T: °C or K (differences in K); R_θ: K/W; P: W; C_θ: J/K; τ_θ: s; η: dimensionless

**Conditions / 适用条件**

One effective node, not device junctions. The transient holds converged loss fixed; thermal coefficients and omitted core/ESR losses are not calibrated.

单个等效热节点，并非器件结温；瞬态固定收敛后的损耗，热系数及遗漏的磁芯/ESR损耗未校准。

**Exercise / 练习**

For 2 W fixed loss, R_θ=8 K/W and ambient 25 °C, find steady node temperature.

固定损耗2 W、热阻8 K/W、环境25 °C，求稳态节点温度。

**Answer / 答案**

T_hot=41 °C. This calculation does not provide the maximum temperature inside an actual package.

T_hot=41 °C；这不代表真实封装内部的最高温度。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

## P09 — Averaged buck soft-start and current-reference limit

平均Buck软启动与电流参考限幅

[GIF: P09_100V_25C](../simulation/V3-3/education/gifs/P09.gif) · [STL: V33_P09](../printing/stl/V33_P09.stl)

**Definition / 定义**

Soft-start ramps the reference; a PI voltage loop requests current through a finite-bandwidth inner loop, with a clipped current reference.

软启动使参考缓升，PI电压环经有限带宽内环请求电流，且电流参考被限幅。

**Equation / 公式**

L di/dt=D V_in−Ri−v; C dv/dt=i−v/R_load; i_ref≤1.6 A

Units / 单位: L: H; C: F; R,R_load: Ω; i,i_ref: A; v,V_in: V; D: dimensionless; t: s

**Conditions / 适用条件**

Continuous averaged duty and conditional-integration anti-windup. The 1.6 A command ceiling is not cycle-by-cycle peak-current protection.

连续平均占空比，采用条件积分抗饱和；1.6 A指令上限不是逐周期峰值电流保护。

**Exercise / 练习**

If the average current settles to 1.6 A into 6 Ω, what output voltage can be sustained?

若平均电流稳定为1.6 A、负载6 Ω，可维持多少输出电压？

**Answer / 答案**

V_out=1.6×6=9.6 V, below the 12 V target; the current ceiling and target cannot both be satisfied at that load.

V_out=9.6 V，低于12 V目标；该负载下无法同时满足限流与电压目标。

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

An isolated NLDMOS separates its source/body domain from substrate while a lateral drift region supports drain voltage. Isolation and gate-source bias are different constraints.

隔离NLDMOS将源/体域与衬底分开，横向漂移区承担漏端电压；隔离与栅源偏置是不同约束。

[STL](../printing/stl/V1_M01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M02 — Low-side NLDMOS

低侧NLDMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The low-side NLDMOS is referenced near ground; its body-drift PN junction can conduct during dead time. Channel conduction and diode conduction are different states.

低侧NLDMOS接近地参考，体区—漂移区PN结可在死区导通；沟道导通与二极管导通是不同状态。

[STL](../printing/stl/V1_M02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M03 — High-voltage PLDMOS

高压PLDMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A PLDMOS uses a P-channel in an N-type body/well with a lateral P drift region; hole transport and source-referenced gate bias distinguish it from NLDMOS.

PLDMOS在N型体/阱中形成P沟道，具有横向P漂移区；空穴输运及源参考栅压使其区别于NLDMOS。

[STL](../printing/stl/V1_M03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M04 — Drain-extended NMOS

高压DENMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Drain-extended NMOS separates the gated channel from an extended drain region. Gate oxide stress and drain voltage must be checked separately.

漏极扩展NMOS将栅控沟道与漏延伸区区分；栅氧应力和漏极电压须分别检查。

[STL](../printing/stl/V1_M04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M05 — Low-voltage NMOS

低压NMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Low-voltage NMOS supplies analog control transconductance. The body is a fourth electrical terminal even when a circuit ties it to a reference.

低压NMOS提供模拟控制跨导；即使电路将体端接参考电位，体端仍是第四电端口。

[STL](../printing/stl/V1_M05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M06 — Low-voltage PMOS

低压PMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A PMOS channel carries holes; V_SG is often used as a positive control magnitude. Its well/body connection affects junction bias and threshold.

PMOS沟道以空穴导电，常用正值V_SG描述控制幅度；阱/体连接影响结偏置与阈值。

[STL](../printing/stl/V1_M06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M07 — Drain-extended PMOS

高压DEPMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Drain-extended PMOS is a P-channel bias/level-shift device concept. Its allowed source, body, drain and gate biases are separate design constraints.

漏极扩展PMOS是P沟道偏置/电平移位器件概念；源、体、漏、栅允许偏置是不同设计约束。

[STL](../printing/stl/V1_M07.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_Q01 — NPN bipolar transistor

NPN双极晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An NPN has emitter, base and collector terminals. In forward-active operation I_C≈β_F I_B, while all terminal currents still satisfy KCL.

NPN具有发射极、基极和集电极；正向放大区I_C约为β_F I_B，三端仍满足KCL。

[STL](../printing/stl/V1_Q01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf) · [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V1_Q02 — PNP bipolar transistor

PNP双极晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

PNP reverses junction polarities and conventional current directions relative to NPN. Emitter/base/collector functions remain distinct.

PNP相对NPN反转结极性及常规电流方向；发射极、基极和集电极的职责仍不同。

[STL](../printing/stl/V1_Q02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf) · [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V1_D01 — MOS body PN freewheel diode

体PN续流二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The N-channel MOS body diode is its body-to-drift PN junction, not an extra transistor. Its forward drop adds dead-time conduction loss.

N沟道MOS体二极管是体区到漂移区的PN结，并非额外晶体管；正向压降产生死区导通损耗。

[STL](../printing/stl/V1_D01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

### V1_D02 — High-voltage bootstrap PN diode

高压自举PN二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A bootstrap PN diode charges the floating capacitor and blocks during a high switch-node interval; reverse voltage and recovery matter separately from forward drop.

自举PN二极管给浮动电容充电，在开关节点升高时截止；反压和恢复须与正向压降分别考虑。

[STL](../printing/stl/V1_D02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V1_D03 — Schottky diode

肖特基二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A Schottky barrier uses a metal–semiconductor interface. Low minority-carrier storage does not eliminate capacitive reverse current or leakage.

肖特基势垒采用金属—半导体界面；少子储存较少不等于没有电容反向电流或漏电。

[STL](../printing/stl/V1_D03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_D04 — Gate Zener clamp

栅极Zener钳位

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A gate clamp shunts excess current near a chosen voltage. The stored 6 V piecewise example specifies behavior, not an oxide-safe operating limit.

栅极钳位在选定电压附近分流多余电流；保存的6 V分段例子描述行为，不是栅氧安全工作上限。

[STL](../printing/stl/V1_D04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_J01 — High-voltage startup JFET

高压启动JFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A JFET controls channel depletion through a junction gate. The legacy example only represents V_GS=0 startup conduction.

JFET通过结栅控制沟道耗尽；旧例只表示V_GS=0的启动导通。

[STL](../printing/stl/V1_J01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V1_R01 — High-voltage polysilicon resistor chain

高压多晶硅电阻链

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Series resistors divide voltage by resistance ratio when loading is negligible; each segment also dissipates I²R and sees local electric stress.

负载可忽略时，串联电阻按阻值比例分压；各段同时耗散I²R并承受局部电应力。

[STL](../printing/stl/V1_R01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V1_R02 — Current-sense resistor

电流检测电阻

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

V_sense=IR_s and P=I²R_s: a larger shunt improves signal size but increases loss. The saved element has two modeled terminals.

V_sense=IR_s、P=I²R_s；增大取样电阻可提高信号，也增加损耗。保存元件仅有两个建模端口。

[STL](../printing/stl/V1_R02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

### V1_C01 — MIM capacitor

MIM电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A MIM capacitor uses metal–insulator–metal layers. The parallel-plate estimate C≈εA/t explains area and thickness trends, with fringe corrections.

MIM电容由金属—绝缘体—金属构成；平行板近似C≈εA/t解释面积和厚度趋势，实际还需边缘修正。

[STL](../printing/stl/V1_C01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf) · [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V1_C02 — MOM capacitor

MOM电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A MOM capacitor relies on fields between patterned metal conductors, often including fringing and interlayer coupling; geometry controls capacitance.

MOM电容利用图形化金属导体间的电场，常包含边缘和层间耦合，几何影响电容。

[STL](../printing/stl/V1_C02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf) · [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf)

### V1_I01 — Isolation junction and DTI equivalent network

隔离结与DTI等效网络

Isolation equivalent/structure concept / 隔离等效/结构概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Isolation has leakage and capacitance between domains; an RC equivalent represents those paths. A trench and a junction are different physical isolation approaches.

域间隔离具有漏电与电容，RC等效表示这些通路；沟槽和结隔离是不同物理方法。

[STL](../printing/stl/V1_I01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_E01 — High-voltage ESD clamp equivalent

高压ESD钳位等效器件

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An ESD clamp is a protection function. Trigger voltage, holding behavior and pulse-current capability must coordinate with the protected circuit.

ESD钳位是一种保护功能，其触发电压、维持行为及脉冲电流能力须与被保护电路协调。

[STL](../printing/stl/V1_E01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json)

### V1_L01 — External power inductor

外接功率电感

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

For lumped L, v=L di/dt and stored energy is ½Li². Winding DCR dissipates heat; an optional core changes inductance and loss.

集总L满足v=L di/dt，储能½Li²；绕组直流电阻发热，是否带磁芯影响电感及损耗。

[STL](../printing/stl/V1_L01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

### V1_C03 — External output capacitor

外接输出电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The output capacitor balances i_C=i_L−i_load; C dv/dt=i_C links load transients to voltage ripple. ESR adds a separate voltage component.

输出电容满足i_C=i_L−i_load，C dv/dt=i_C连接负载变化与电压纹波；ESR另产生压降。

[STL](../printing/stl/V1_C03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

### V1_C04 — External input capacitor

外接输入电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Input decoupling supplies pulsed switching current and reduces local source impedance. Differential capacitor voltage and loop inductance both matter.

输入去耦提供脉冲开关电流并降低局部源阻抗；电容两端电压和回路电感均重要。

[STL](../printing/stl/V1_C04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

### V1_C05 — External bootstrap capacitor

外接自举电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Bootstrap charge supports driver bias and gate charging; ΔV_BS=−ΔQ/C_boot. Common-mode voltage to ground differs from voltage across the capacitor.

自举电荷供给驱动偏置与栅充电，ΔV_BS=−ΔQ/C_boot；对地共模电压不同于电容两端电压。

[STL](../printing/stl/V1_C05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V2_N01 — SiC vertical MOSFET

SiC垂直MOSFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A vertical SiC MOSFET combines a gated channel with a voltage-supporting drift region. Material properties affect transport and field limits, but ratings belong to a characterized device.

垂直SiC MOSFET将栅控沟道与承压漂移区结合；材料影响输运和电场极限，额定值仍属于经表征的具体器件。

[STL](../printing/stl/V2_N01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N02 — Enhancement-mode GaN HEMT

增强型GaN HEMT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A GaN HEMT uses a heterostructure channel. Enhancement mode means the channel is normally off at the specified zero-gate bias; dynamic on-resistance can depend on prior stress.

GaN HEMT采用异质结构沟道；增强型表示规定零栅偏下常关，动态导通电阻可依赖先前应力。

[STL](../printing/stl/V2_N02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/) · [legacy:P25](https://researchportal.hkust.edu.hk/en/publications/dynamic-performance-of-aln-passivated-algangan-mis-high-electron-/)

### V2_N03 — Silicon superjunction MOSFET

硅超结MOSFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A superjunction uses compensating drift-region charges to reshape the field and trade blocking voltage against conduction resistance. Charge balance is a design condition.

超结通过漂移区电荷补偿重塑电场，权衡阻断电压与导通电阻；电荷平衡是设计条件。

[STL](../printing/stl/V2_N03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/)

### V2_N04 — IGBT

IGBT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An IGBT combines MOS gate control with bipolar injection. Stored minority charge can reduce conduction resistance and produce turn-off tail current.

IGBT结合MOS栅控制与双极注入；少子储存可降低导通电阻，也可产生关断尾电流。

[STL](../printing/stl/V2_N04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N05 — SiC JBS rectifier

SiC JBS整流二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A junction-barrier Schottky rectifier combines Schottky conduction regions with PN shielding regions. Its reverse behavior depends on depletion around those shields.

结势垒肖特基整流器结合肖特基导通区与PN屏蔽区，反向行为取决于屏蔽区周围耗尽。

[STL](../printing/stl/V2_N05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N06 — FinFET

FinFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A FinFET is a multigate transistor. Effective width and electrostatic control depend on fin geometry; a planar W/L law is only a reduced analogy.

FinFET为多栅晶体管，有效宽度与静电控制取决于鳍几何；平面W/L公式只是简化类比。

[STL](../printing/stl/V2_N06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P04](https://arxiv.org/abs/2005.02580)

### V2_N07 — a-IGZO thin-film transistor

a-IGZO TFT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An amorphous-oxide TFT controls conduction in a deposited thin film. Field-effect mobility, threshold and contact resistance describe different contributions.

非晶氧化物TFT控制沉积薄膜中的导电；场效应迁移率、阈值和接触电阻描述不同贡献。

[STL](../printing/stl/V2_N07.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P05](https://www.nature.com/articles/nature03090)

### V2_N08 — Organic polymer TFT

有机聚合物TFT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An organic TFT transports charge through a molecular/polymer film. Contact injection and morphology can be as important as gate electrostatics.

有机TFT在分子/聚合物膜中输运电荷，接触注入和形貌可能与栅静电控制同样重要。

[STL](../printing/stl/V2_N08.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P06](https://www.nature.com/articles/nature25494)

### V2_N09 — Contact-limited MoS2 FET

MoS2接触受限FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Contact-limited FET current depends on both channel conductance and source/drain injection resistance. Two-terminal mobility extraction can therefore be misleading.

接触受限FET电流同时取决于沟道电导与源漏注入电阻，因此二端迁移率提取可能有偏差。

[STL](../printing/stl/V2_N09.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P07](https://pubs.acs.org/doi/10.1021/nl303583v)

### V2_N10 — Ambipolar graphene FET

石墨烯双极性FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An ambipolar graphene transfer curve has electron- and hole-dominated branches around a charge-neutrality region; it is not a silicon MOS off-state law.

石墨烯双极性转移曲线在电中性区域两侧分别以电子或空穴导电，不能照搬硅MOS关断规律。

[STL](../printing/stl/V2_N10.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P08](https://www.science.org/doi/10.1126/science.1102896)

### V2_N11 — Ballistic carbon-nanotube FET

碳纳米管弹道FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A ballistic CNT model describes transmission between reservoirs using mode occupancy. Conductance depends on allowed channels, not a bulk resistor formula alone.

弹道CNT模型用模式占据描述两端储库间传输，电导取决于允许通道，不能只用体电阻公式。

[STL](../printing/stl/V2_N11.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P19](https://www.nature.com/articles/nature22994) · [legacy:P24](https://ieeexplore.ieee.org/document/1224486/)

### V2_N12 — Ferroelectric FET memory cell

FeFET铁电存储晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A FeFET stores information through polarization-dependent threshold shift. Its memory window is a transfer-curve separation, not an extra terminal.

FeFET通过极化相关阈值偏移存储信息，存储窗口是转移曲线间距，并非新增端口。

[STL](../printing/stl/V2_N12.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P09](https://www.nature.com/articles/s41928-020-00492-7)

### V2_N13 — Oxide RRAM cell

氧化物RRAM

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

RRAM represents nonvolatile resistive switching. In this example a bounded state w sets G=G_off+(G_on−G_off)w and evolves beyond voltage thresholds.

RRAM表示非易失阻变；本例有界状态w决定G=G_off+(G_on−G_off)w，并在电压越阈后演化。

[STL](../printing/stl/V2_N13.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P10](https://www.nature.com/articles/s41928-018-0092-2) · [legacy:P19](https://www.nature.com/articles/nature22994)

### V2_N14 — Phase-change memory cell

PCM相变存储单元

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

PCM stores state through phase-dependent resistance. A lumped thermal balance couples Joule heating to an assumed crystalline-fraction state.

PCM通过相态相关电阻存储，集总热平衡将焦耳热与假设的晶态比例耦合。

[STL](../printing/stl/V2_N14.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P10](https://www.nature.com/articles/s41928-018-0092-2)

### V2_N15 — Magnetic tunnel junction

MTJ磁隧道结

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An MTJ has different resistance for parallel and antiparallel magnetizations across a tunnel barrier. TMR=(R_AP−R_P)/R_P.

MTJ两磁层隔着隧穿势垒，平行与反平行磁化具有不同电阻；TMR=(R_AP−R_P)/R_P。

[STL](../printing/stl/V2_N15.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P11](https://www.sciencedirect.com/science/article/pii/S1369702117304285)

### V2_N16 — Ferroelectric capacitor

铁电电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A ferroelectric capacitor has Q=C_linear V+Q_sat p, where polarization state p makes charge history-dependent and hysteretic.

铁电电容满足Q=C_linear V+Q_sat p，极化状态p使电荷依赖历史并出现迟滞。

[STL](../printing/stl/V2_N16.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P09](https://www.nature.com/articles/s41928-020-00492-7) · [legacy:P23](https://www.science.org/doi/10.1126/science.1169678)

### V2_N17 — Nitride LED

氮化物LED

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A nitride LED converts injected carriers into photons; EQE is emitted photons per injected electron. Optical power depends on current, wavelength and EQE.

氮化物LED将注入载流子转为光子，外量子效率为每注入电子对应的出射光子数；光功率取决于电流、波长及EQE。

[STL](../printing/stl/V2_N17.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P12](https://www.nature.com/articles/nphoton.2009.32)

### V2_N18 — Quantum-dot LED

量子点LED

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A quantum-dot LED injects electrons and holes through transport layers into an emissive nanocrystal layer. Its stack differs from a simple silicon PN diode.

量子点LED通过传输层将电子和空穴注入发光纳米晶层，层次不同于简单硅PN二极管。

[STL](../printing/stl/V2_N18.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P13](https://www.nature.com/articles/370354a0)

### V2_N19 — PIN photodetector

PIN光电探测器

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A PIN photodetector uses an intrinsic absorption region; responsivity links photocurrent to incident optical power, I_ph=ℛP_opt.

PIN探测器采用本征吸收区，响应度连接光电流和入射光功率，I_ph=ℛP_opt。

[STL](../printing/stl/V2_N19.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_N20 — Single-junction photovoltaic cell

单结光伏电池

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A single-diode photovoltaic equivalent combines photocurrent, diode current and series/shunt loss; maximum power is the maximum of V I_out.

单二极管光伏等效组合光生电流、二极管电流与串/并联损耗；最大功率为V I_out的最大值。

[STL](../printing/stl/V2_N20.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P14](https://www.science.org/doi/10.1126/science.1228604)

### V2_N21 — Thermoelectric generator cell

热电发电单元

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A thermoelectric generator couples Seebeck voltage, Peltier heat, Joule loss and thermal conduction. HOT/COLD are thermal boundaries, not electrical terminals.

热电发电器耦合Seebeck电压、Peltier热、焦耳损耗和导热；HOT/COLD是热边界，不是电端。

[STL](../printing/stl/V2_N21.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P15](https://www.nature.com/articles/nmat2090)

### V2_N22 — On-chip coupled transformer

片上耦合变压器

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A coupled transformer has mutual inductance M=k√(L1L2); winding resistance and substrate paths reduce performance. The stored signals are RMS frequency-domain phasors.

耦合变压器互感M=k√(L1L2)，绕组电阻及衬底通路影响性能；保存信号是频域有效值相量。

[STL](../printing/stl/V2_N22.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P16](https://ieeexplore.ieee.org/document/720393/)

### V2_N23 — Through-silicon via

TSV硅通孔

Interconnect concept / 互连概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A TSV is an interconnect with resistance, inductance and substrate capacitance/leakage. A lumped RLCG network approximates its terminal response.

TSV是具有电阻、电感及衬底电容/漏电的互连，集总RLCG网络近似其端口响应。

[STL](../printing/stl/V2_N23.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P17](https://ieeexplore.ieee.org/document/5340655/)

### V2_N24 — Mach-Zehnder electro-optic modulator

MZI电光调制器

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An MZI converts relative optical phase to intensity by interference. Electrical drive terminals and optical input/output ports are different kinds of boundaries.

MZI通过干涉把相对光相位转换为强度，电驱端与光输入/输出是不同类型边界。

[STL](../printing/stl/V2_N24.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_N25 — Semiconductor laser diode

半导体激光二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A laser diode’s static L–I curve uses threshold current and slope efficiency. Its optical cavity distinguishes it from a simple spontaneous-emission LED.

激光二极管静态L–I曲线由阈值电流和斜率效率描述，光腔使其区别于单纯自发辐射LED。

[STL](../printing/stl/V2_N25.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_X01 — MOS gate charge and Miller coupling

MOS栅电荷与Miller耦合

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Miller coupling connects gate and drain dynamics through Cgd. The legacy bench solves two coupled voltages with fixed capacitances and a clamped load.

Miller耦合经Cgd连接栅漏动态；旧测试台以固定电容及钳位负载求解两个耦合电压。

[STL](../printing/stl/V2_X01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf)

### V2_X02 — PN diode reverse recovery

PN二极管反向恢复

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A prescribed triangular reverse pulse has area Qrr. Its peak and duration are constrained by charge and imposed current slope, not by a carrier transport solution.

预设三角反向脉冲面积为Qrr，峰值和持续时间由电荷及规定电流斜率约束，并非载流子输运解。

[STL](../printing/stl/V2_X02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_X03 — MOS conduction-loss thermal feedback

MOS导通损耗自热反馈

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Under constant current, I²R(T) couples to a thermal RC. Positive resistance temperature coefficient provides reinforcing electrothermal feedback.

恒流下I²R(T)与热RC耦合，电阻正温度系数形成增强的电热反馈。

[STL](../printing/stl/V2_X03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### V2_X04 — PMOS NBTI aging

PMOS NBTI老化

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

NBTI can increase the magnitude of PMOS threshold under negative gate bias and temperature stress. The example uses an empirical time/temperature power law.

负栅偏和温度应力下，NBTI可增大PMOS阈值绝对值；示例采用经验时间/温度幂律。

[STL](../printing/stl/V2_X04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P20](https://www.sciencedirect.com/science/article/pii/S0026271404001751)

### V2_X05 — MOS flicker and thermal noise

MOS 1/f与热噪声

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The MOS current-noise PSD is Kf/f+4kTγgm; integrating over a stated frequency band gives mean-square current noise.

MOS电流噪声谱为Kf/f+4kTγgm，在规定频带积分得到电流噪声均方值。

[STL](../printing/stl/V2_X05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P21](https://ieeexplore.ieee.org/document/34242/) · [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V2_X06 — MOS threshold and resistance statistics

MOS阈值及电阻统计分散

Parameter/statistical demonstration / 参数/统计演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

This Monte Carlo example samples Gaussian threshold and positive lognormal resistance, then solves each bias point. Parameter spread is not simulated random geometry.

蒙特卡洛例子抽取高斯阈值和正值对数正态电阻，再求各偏置点；参数分散不是随机几何仿真。

[STL](../printing/stl/V2_X06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P22](https://ieeexplore.ieee.org/document/1210771/) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_A01 — Four-terminal MOS interpolation

四端MOS连续插值

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Transconductance is the local sensitivity of drain current to gate voltage at fixed other terminal voltages.

跨导是其他端口电压固定时，漏电流对栅压的局部变化率。

[STL](../printing/stl/V33_A01.stl) · Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V33_A02 — Junction charge and varactor

结电荷与变容二极管

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Junction differential capacitance is dQ/dV. Nonlinear stored charge is an integral, not generally C(V)V.

结的微分电容为dQ/dV；非线性储存电荷应通过积分求得，通常不等于C(V)V。

[STL](../printing/stl/V33_A02.stl) · Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V33_A03 — Reciprocal NPN Ebers–Moll

满足互易关系的NPN Ebers–Moll

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

The Ebers–Moll model combines forward and reverse junction injection and enforces three-terminal current conservation.

Ebers–Moll模型叠加正、反向结注入，并满足三端电流守恒。

[STL](../printing/stl/V33_A03.stl) · Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V33_A04 — MOS pair mismatch and correlation

MOS配对失配与相关性

Parameter/statistical demonstration / 参数/统计演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Pair mismatch is a difference of two device parameters; shared variation can cancel, while local variation remains.

配对失配是两个器件参数之差；共同变化可相消，局部差异仍存在。

[STL](../printing/stl/V33_A04.stl) · Sources / 来源: [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_B01 — MOS differential pair

MOS差分对

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A MOS differential pair converts differential input voltage into a branch-current difference.

MOS差分对将差分输入电压转换为支路电流之差。

[STL](../printing/stl/V33_B01.stl) · Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V33_B02 — CTAT/PTAT reference sum

CTAT/PTAT基准合成

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

CTAT decreases with absolute temperature; PTAT is proportional to absolute temperature. Their weighted sum cancels first-order drift near a design point.

CTAT随绝对温度下降，PTAT与绝对温度成正比；加权合成可在设计温度附近抵消一阶温漂。

[STL](../printing/stl/V33_B02.stl) · Sources / 来源: [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf)

### V33_B03 — Input noise and sampled kT/C

输入噪声与采样kT/C

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Voltage PSD integrates to variance; amplitude spectral density is its square root. An equilibrated sampled capacitor has thermal variance kT/C.

电压功率谱密度积分得到方差，幅度谱密度是其平方根；达到热平衡的采样电容热噪声方差为kT/C。

[STL](../printing/stl/V33_B03.stl) · Sources / 来源: [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V33_B04 — Capacitor DAC and SAR ADC

电容DAC与SAR ADC

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A SAR ADC tests binary capacitor-DAC weights sequentially. DNL describes code-width error; INL describes transition deviation from a stated reference line.

SAR ADC逐次测试二进制电容DAC权重；DNL描述码宽误差，INL描述转换边界相对指定参考直线的偏离。

[STL](../printing/stl/V33_B04.stl) · Sources / 来源: [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_B05 — LDO loop and load step

LDO环路与负载阶跃

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

An LDO feedback loop adjusts pass current to oppose output-voltage disturbances. Here v and i_p are deviations from a biased operating point.

LDO反馈环调节通过电流以抵消输出电压扰动；此处v和i_p为偏置工作点附近的增量。

[STL](../printing/stl/V33_B05.stl) · Sources / 来源: [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf)

### V33_B06 — Phase loop and noise transfer

相位环路与噪声传递

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Phase is position within an oscillation cycle. A canonical second-order loop filters reference phase and complementary oscillator phase disturbances.

相位描述振荡周期中的位置；典型二阶环路滤波参考相位及互补的振荡器相位扰动。

[STL](../printing/stl/V33_B06.stl) · Sources / 来源: [base:B09](https://chic.caltech.edu/wp-content/uploads/2013/05/general.pdf)

### V33_B07 — 40–150 V synchronous buck

40–150V同步降压

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A synchronous buck alternates high- and low-side switches; in forced continuous conduction, inductor current follows piecewise circuit equations.

同步降压器交替控制高、低侧开关；强制连续导通时，电感电流遵循分段电路方程。

[STL](../printing/stl/V33_B07.stl) · Sources / 来源: [base:D01](../simulation/V3-3/MODEL_CARDS.md)

### V33_P01 — HV MOS gate charge and switching overlap

高压MOS栅电荷与开关交叠

Mechanism demonstration / 机制演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Miller charge is the gate-drain charge transferred during a drain-voltage transition; finite gate current sets its transition time.

Miller电荷是漏压变化期间转移的栅漏电荷；有限栅电流决定转换时间。

[STL](../printing/stl/V33_P01.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V33_P02 — Dead-time diode and reverse recovery

死区二极管与反向恢复

Mechanism demonstration / 机制演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Dead time prevents simultaneous switch commands but permits diode conduction. Reverse-recovery charge is the time integral of reverse recovery current.

死区避免上下管同时收到导通指令，但可产生二极管导通；反向恢复电荷为恢复电流的时间积分。

[STL](../printing/stl/V33_P02.stl) · Sources / 来源: [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

### V33_P03 — Floating bootstrap supply and UVLO margin

浮地自举供电与欠压裕量

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A bootstrap capacitor powers the floating high-side driver; its differential voltage V_BS=V_B−V_S must retain adequate supply margin.

自举电容为浮动高侧驱动供电；差分电压V_BS=V_B−V_S须保持足够的供电裕量。

[STL](../printing/stl/V33_P03.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V33_P04 — Level-shifter common-mode disturbance

电平移位接收端共模扰动

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Common-mode slew injects displacement current through parasitic capacitance; receiver impedance converts it into a differential disturbance.

共模电压变化通过寄生电容注入位移电流，接收端阻抗将其变为差模扰动。

[STL](../printing/stl/V33_P04.stl) · Sources / 来源: [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V33_P05 — Current-sense amplifier and delayed comparator

电流检测放大器与延迟比较器

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A shunt converts current into voltage; finite amplifier bandwidth and comparator delay determine detection timing.

分流电阻把电流转为电压，放大器有限带宽和比较器延迟决定检测时刻。

[STL](../printing/stl/V33_P05.stl) · Sources / 来源: [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

### V33_P06 — HV startup supply and hysteretic UVLO

高压启动供电与迟滞欠压锁定

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Startup current charges an auxiliary supply; UVLO hysteresis uses distinct enable and disable thresholds to avoid immediate toggling.

启动电流给辅助供电电容充电，UVLO迟滞采用不同开启和关闭阈值以避免立即反复翻转。

[STL](../printing/stl/V33_P06.stl) · Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V33_P07 — Switch-node parasitic ringing and damping

开关节点寄生振铃与阻尼

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A series RLC free response transfers energy between capacitor and inductor; resistance dissipates it.

串联RLC自由响应在电容与电感间交换能量，由电阻耗散。

[STL](../printing/stl/V33_P07.stl) · Sources / 来源: [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

### V33_P08 — DC/DC separated losses and thermal budget

DC/DC分项损耗与热预算

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A loss ledger sums distinct energy mechanisms; a thermal resistance/capacitance converts assumed loss into an effective temperature rise.

损耗账本对不同能量机制分别求和，热阻/热容把假设损耗换算为等效温升。

[STL](../printing/stl/V33_P08.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### V33_P09 — Averaged buck soft-start and current-reference limit

平均Buck软启动与电流参考限幅

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Soft-start ramps the reference; a PI voltage loop requests current through a finite-bandwidth inner loop, with a clipped current reference.

软启动使参考缓升，PI电压环经有限带宽内环请求电流，且电流参考被限幅。

[STL](../printing/stl/V33_P09.stl) · Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

## Evidence boundary

## 依据边界

Existing source provenance is preserved. Three primary URLs were reopened for focused teaching checks; other entries retain their earlier read scope. This is not a new comprehensive paper audit, and references do not calibrate the authored model coefficients.

保留既有来源追溯，另打开3个一手网址作定向教学核对；其余保留原阅读范围。这不是新一轮全面论文审计，引用也不能校准人为模型系数。

Equations are teaching relations, not normative standards or complete SPICE implementations. A simplified exercise may use illustrative values different from its GIF.

公式为教学关系式，不是规范性标准或完整SPICE实现；简化练习可使用与GIF不同的示意数值。
