# Graduate — derive and validate

# 研究生版——推导与验证

Separate assumptions, numerical error and physical error; plan a falsifiable measurement or model extension.

区分假设、数值误差与物理误差，提出可检验的测量或模型扩展。

V3-5 teaching edition of the existing v3.3.0 numerical baseline: 20 views comprise 3 illustrative device models, 1 statistical demonstration, 2 prescribed mechanism benches and 14 circuit/system benches. The 75 printable entries include these 20 plus 55 legacy/background representations; they are not 75 independently calibrated devices. The release audit separately records reruns of the current numerical baseline. This teaching content adds no new physics, PDK, silicon fit or physical-accuracy gain.

V3-5是现有v3.3.0数值基线的教学版本：20个视图含3个示意器件、1个统计演示、2个预设机制测试台及14个电路/系统测试台。75个打印条目包含上述20项与55项旧版/背景表示，并非75种独立校准器件。发布审计另行记录现有数值基线重跑；本教学内容未新增物理机制、PDK、硅实测拟合或物理准确度提高。

## Before you begin

## 阅读前

Begin with a falsifiable question. First test the implemented equations and convergence; then compare independent measurements. A good fit on training cases alone is not validation.

从可检验的问题开始，先检验实现方程和收敛，再对比独立测量。仅在拟合工况表现好不等于验证通过。

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

**Assumptions / 模型假设**

The softplus current law bridges weak and strong inversion; an independent fixed pair-capacitance network conserves terminal charge.

softplus电流式连接弱、强反型；独立的固定互电容网络保证端口电荷守恒。

**Derivation / research question / 推导／研究问题**

Differentiate the same DC law analytically; test source/drain exchange symmetry and ΣQ = 0 separately. Why does charge conservation alone not prove correct intrinsic capacitances?

对同一直流式解析求导，分别检查源漏交换对称性及ΣQ=0。为什么电荷守恒本身不能证明内禀电容正确？

**Validity and error / 有效性与误差**

The revision improves derivatives of the authored equation. Missing DIBL, velocity saturation and intrinsic charge partition can dominate physical error.

本次基线改进的是人为方程的导数计算。未包含的DIBL、速度饱和及内禀电荷分配可能主导物理误差。

**Extension and required evidence / 扩展与所需证据**

Obtain multi-bias I–V and terminal C–V data over temperature; separate fitting and hold-out bias points before adding a calibrated compact model.

需要多偏置、多温度I–V与端口C–V数据；划分拟合与留出验证工况后，才能引入经校准的紧凑模型。

Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

## A02 — Junction charge and varactor

结电荷与变容二极管

[GIF: A02_CV_25C](../simulation/V3-3/education/gifs/A02.gif) · [STL: V33_A02](../printing/stl/V33_A02.stl)

**Assumptions / 模型假设**

A quasi-static depletion law and an assumed 1 pA reverse leakage represent two different mechanisms.

准静态耗尽规律与假设的1 pA反向漏电代表两种不同机制。

**Derivation / research question / 推导／研究问题**

For m=1/2, rationalize Q=2C0φ[1−√(1−V/φ)] as Q=2C0V/[1+√(1−V/φ)]. Verify dQ/dV=C.

m=1/2时，将Q=2C0φ[1−√(1−V/φ)]有理化为Q=2C0V/[1+√(1−V/φ)]，验证dQ/dV=C。

**Validity and error / 有效性与误差**

Rationalization removes cancellation near zero; a stress-test percentage does not describe accuracy of the entire plotted C–V range or measured junction.

有理化消除零附近的相消误差；压力测试的改善比例不能代表全部C–V区间或实测结的准确度。

**Extension and required evidence / 扩展与所需证据**

Measure bias- and frequency-dependent C–V plus I–V before adding series resistance, diffusion storage or breakdown.

补充偏置、频率相关C–V及I–V测量，再引入串联电阻、扩散储能或击穿。

Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

## A03 — Reciprocal NPN Ebers–Moll

满足互易关系的NPN Ebers–Moll

[GIF: A03_gummel_25C](../simulation/V3-3/education/gifs/A03.gif) · [STL: V33_A03](../printing/stl/V33_A03.stl)

**Assumptions / 模型假设**

Two exponential junction currents share the reciprocity-constrained saturation current; no transit-time charge is present.

两个指数结电流由互易约束关联饱和电流；没有渡越时间电荷。

**Derivation / research question / 推导／研究问题**

Substitute the three terminal equations to prove KCL for arbitrary I_F and I_R. Then examine the forward-active approximation and its failure in saturation.

代入三端方程，证明任意I_F、I_R下均满足KCL；再分析正向放大近似及其在饱和区的失效。

**Validity and error / 有效性与误差**

An expm1 implementation has floating-point-scale KCL residuals. That does not validate β versus current, Early effect or RF behavior.

expm1实现的KCL残差处于浮点量级；这不验证电流相关β、Early效应或射频行为。

**Extension and required evidence / 扩展与所需证据**

Collect Gummel plots and output curves across temperature; charge-storage or fT measurements are needed for dynamic extensions.

需收集不同温度的Gummel图及输出曲线；动态扩展还需电荷储存或fT测量。

Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

## A04 — MOS pair mismatch and correlation

MOS配对失配与相关性

[GIF: A04_area16um2](../simulation/V3-3/education/gifs/A04.gif) · [STL: V33_A04](../printing/stl/V33_A04.stl)

**Assumptions / 模型假设**

A common global shift is added to both members; the local joint distribution has specified variance and correlation.

两成员加入相同的全局偏移，局部联合分布具有规定的方差与相关系数。

**Derivation / research question / 推导／研究问题**

Derive Var(X−Y)=Var(X)+Var(Y)−2Cov(X,Y). Distinguish the spread of devices from uncertainty in the estimated spread.

推导Var(X−Y)=Var(X)+Var(Y)−2Cov(X,Y)，区分器件本身的分散与分散估计值的不确定度。

**Validity and error / 有效性与误差**

80,000 samples reduce sampling uncertainty; a particular sample standard deviation can still move farther from the analytic value. No yield gain follows.

80000个样本降低抽样不确定度；某次样本标准差仍可能更远离解析值，也不能据此宣称良率提高。

**Extension and required evidence / 扩展与所需证据**

Use measured pair arrays with area, separation, orientation and temperature metadata; fit spatial/systematic terms separately from local mismatch.

需要带面积、间距、方向和温度信息的实测配对阵列，分别拟合空间/系统性项与局部失配。

Sources / 来源: [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

## B01 — MOS differential pair

MOS差分对

[GIF: B01_25C](../simulation/V3-3/education/gifs/B01.gif) · [STL: V33_B01](../printing/stl/V33_B01.stl)

**Assumptions / 模型假设**

A scalar common-source voltage is solved by bisection; drain voltages and the current sum are imposed.

通过二分法求一个共源电压标量，漏极电压和总电流作为约束。

**Derivation / research question / 推导／研究问题**

Linearize both devices about balance to derive current-difference gain. Then replace the ideal tail with finite impedance and examine common-mode response.

在平衡点线性化两管以推导差分电流增益；再将理想尾源改为有限阻抗，考察共模响应。

**Validity and error / 有效性与误差**

The 80-step solution is already at double-precision resolution. A small KCL residual does not establish bandwidth, CMRR or input offset.

80步求解已达到双精度分辨率；很小的KCL残差不等于已验证带宽、共模抑制比或输入失调。

**Extension and required evidence / 扩展与所需证据**

Add load and tail models, body connections and measured mismatch; AC and transient measurements are needed for amplifier-level claims.

需补充负载、尾源、体端连接与实测失配；放大器级结论还需交流和瞬态验证。

Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

## B02 — CTAT/PTAT reference sum

CTAT/PTAT基准合成

[GIF: B02_temperature](../simulation/V3-3/education/gifs/B02.gif) · [STL: V33_B02](../printing/stl/V33_B02.stl)

**Assumptions / 模型假设**

An empirical V_BE curvature law is combined with ideal PTAT scaling, tuned so dV_ref/dT=0 at 25 °C.

将经验V_BE曲率式与理想PTAT项组合，使25 °C处dV_ref/dT=0。

**Derivation / research question / 推导／研究问题**

Differentiate V_ref to obtain a at T0, then calculate d²V_ref/dT². Explain why zero slope at one point leaves finite temperature span.

对V_ref求导得到T0处的a，再求二阶导数；解释为何一点斜率为零仍有全温区变化。

**Validity and error / 有效性与误差**

Analytic evaluation has negligible numerical residual; curvature and missing mismatch dominate the interpretation. It is not a reproduction of Brokaw’s measured circuit.

解析求值的数值残差很小，但曲率及未建模失配限制结论；它不复现Brokaw的实测电路。

**Extension and required evidence / 扩展与所需证据**

Use transistor/resistor temperature data, supply sweeps and startup trajectories; test trim strategy on independent process corners.

需晶体管/电阻温度数据、电源扫描和启动轨迹，并在独立工艺角验证修调策略。

Sources / 来源: [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf)

## B03 — Input noise and sampled kT/C

输入噪声与采样kT/C

[GIF: B03_25C](../simulation/V3-3/education/gifs/B03.gif) · [STL: V33_B03](../printing/stl/V33_B03.stl)

**Assumptions / 模型假设**

Authored spectra compare 1/f suppression with a higher white floor; no actual chopper switches or aliasing are simulated.

人为频谱比较1/f抑制与白噪声底上升的取舍；未模拟真实斩波开关或混叠。

**Derivation / research question / 推导／研究问题**

Integrate a white-plus-1/f PSD analytically; explain the logarithmic lower-frequency cutoff and why integrating ASD directly gives the wrong units.

解析积分白噪声加1/f谱，解释低频截止的对数依赖，以及直接积分ASD为何单位不对。

**Validity and error / 有效性与误差**

Analytic quadrature improves a metric of the chosen PSD. Unknown current noise, source impedance, aliasing and switching ripple remain physical gaps.

解析积分改进选定频谱的指标计算；电流噪声、源阻抗、混叠和开关纹波仍是物理缺项。

**Extension and required evidence / 扩展与所需证据**

Measure input-referred spectra with source impedances and anti-alias filters specified; add cyclostationary sampling only with a real switching topology.

需明确源阻抗和抗混叠滤波后测量输入参考噪声谱；只有给定真实开关拓扑，才可增加循环平稳采样分析。

Sources / 来源: [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

## B04 — Capacitor DAC and SAR ADC

电容DAC与SAR ADC

[GIF: B04_mismatch](../simulation/V3-3/education/gifs/B04.gif) · [STL: V33_B04](../printing/stl/V33_B04.stl)

**Assumptions / 模型假设**

Assumed capacitor mismatch changes sequential decisions; an ideal comparator still resolves immediately and without noise.

假设的电容失配改变逐次判决，理想比较器仍无噪声、即时判断。

**Derivation / research question / 推导／研究问题**

Find actual decision thresholds rather than sorting nominal DAC levels. Audit coherent FFT power counting, including DC and Nyquist bins only once.

寻找真实逐次判决边界，而非将标称DAC电平排序；审查相干FFT功率计数，直流及奈奎斯特点仅计一次。

**Validity and error / 有效性与误差**

A machine-precision threshold search does not improve physical ENOB. Ideal SNR formulas require their input and quantization assumptions; use SNDR for ENOB here.

机器精度的边界搜索并不提高实物ENOB；理想SNR公式有输入与量化假设，本例ENOB应由SNDR换算。

**Extension and required evidence / 扩展与所需证据**

Measure transition histograms, capacitor statistics, comparator noise, settling and reference droop; retain independent codes and tones for validation.

需要转换直方图、电容统计、比较器噪声、建立过程及参考跌落测量，并保留独立码段和频点验证。

Sources / 来源: [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

## B05 — LDO loop and load step

LDO环路与负载阶跃

[GIF: B05_25C](../simulation/V3-3/education/gifs/B05.gif) · [STL: V33_B05](../printing/stl/V33_B05.stl)

**Assumptions / 模型假设**

A finite-bandwidth transconductance feeds an output RC load; matrix coefficients are constant at each temperature.

有限带宽跨导驱动输出RC负载；各温度下矩阵系数保持常数。

**Derivation / research question / 推导／研究问题**

Derive the state matrix and loop gain; compare its poles, unity-gain crossing and final-value load regulation with the step response.

推导状态矩阵和环路增益，比较极点、单位增益交点、终值负载调整与阶跃响应。

**Validity and error / 有效性与误差**

Exact matrix propagation removes discretization of this linear system, not errors in assumed loop poles or measured phase margin.

精确矩阵传播消除该线性系统的离散误差，不能消除假设极点或实测相位裕度的不确定性。

**Extension and required evidence / 扩展与所需证据**

Acquire loop gain versus load, capacitor ESR and pass-device operating range; use nonlinear transistor behavior for dropout and startup.

需不同负载下的环路增益、电容ESR及通过管工作范围；压差极限和启动需要非线性晶体管模型。

Sources / 来源: [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf)

## B06 — Phase loop and noise transfer

相位环路与噪声传递

[GIF: B06_zeta0.7](../simulation/V3-3/education/gifs/B06.gif) · [STL: V33_B06](../printing/stl/V33_B06.stl)

**Assumptions / 模型假设**

Linear time-invariant phase dynamics mix independent noise via |H|² and |1−H|², using one-sided phase PSD.

线性时不变相位动态采用单边相位谱，以|H|²、|1−H|²组合独立噪声。

**Derivation / research question / 推导／研究问题**

Derive pole damping and integrated output phase variance. Explain why SSB phase-noise data need a defined convention before conversion to phase PSD.

推导极点阻尼及输出相位方差；解释单边带相噪数据为何必须明确约定才能转换为相位功率谱。

**Validity and error / 有效性与误差**

Exact state evolution and refined quadrature do not capture ISF, cyclostationary noise, cycle slips or acquisition.

精确状态演化和细化积分仍不包含ISF、循环平稳噪声、周跳或捕获过程。

**Extension and required evidence / 扩展与所需证据**

Require measured phase-noise spectra, carrier frequency and integration limits; transistor oscillator work additionally needs periodic steady-state/noise evidence.

需实测相噪谱、载波频率和积分界限；晶体管振荡器研究还需周期稳态及噪声依据。

Sources / 来源: [base:B09](https://chic.caltech.edu/wp-content/uploads/2013/05/general.pdf)

## B07 — 40–150 V synchronous buck

40–150V同步降压

[GIF: B07_100V_25C](../simulation/V3-3/education/gifs/B07.gif) · [STL: V33_B07](../printing/stl/V33_B07.stl)

**Assumptions / 模型假设**

The linear state matrix is constant within each switch phase; a period map supplies the periodic initial state.

每个开关阶段内线性状态矩阵恒定，利用周期映射求周期初始状态。

**Derivation / research question / 推导／研究问题**

Derive the on/off affine maps and periodic fixed point. Check input energy minus output energy, resistor loss and stored-energy change.

推导导通/关断仿射映射及周期不动点；检查输入能量减输出能量、电阻损耗与储能变化的平衡。

**Validity and error / 有效性与误差**

Exact propagation and phasewise quadrature reduce numerical error. Saved ripple extrema remain sampled; conduction-only efficiency excludes many real losses.

精确传播与分段积分降低数值误差；保存的纹波极值仍来自采样，只含导通损耗的效率遗漏多项真实损耗。

**Extension and required evidence / 扩展与所需证据**

Add independently calibrated gate/diode/Coss and magnetic losses; validate switching waveforms, parasitic extraction and device voltage/SOA margins separately.

需独立校准栅极、二极管、Coss及磁性损耗，并分别验证开关波形、寄生参数、器件耐压及SOA裕量。

Sources / 来源: [base:D01](../simulation/V3-3/MODEL_CARDS.md)

## P01 — HV MOS gate charge and switching overlap

高压MOS栅电荷与开关交叠

[GIF: P01_100V_25C](../simulation/V3-3/education/gifs/P01.gif) · [STL: V33_P01](../printing/stl/V33_P01.stl)

**Assumptions / 模型假设**

C_gd and C_oss follow authored nonlinear voltage laws; channel overlap, capacitance storage and diode recovery are distinct quantities.

C_gd、C_oss采用人为非线性电压规律，沟道交叠、电容储能及二极管恢复分开处理。

**Derivation / research question / 推导／研究问题**

Integrate the charge law and invert it for V_DS(t). Audit the subtraction of instantaneous R_on I² baseline from channel-overlap energy.

积分电荷式并反解V_DS(t)，审查从沟道交叠能量中扣除瞬时R_on I²导通基线的处理。

**Validity and error / 有效性与误差**

Stagewise quadrature refines the assumed trajectory; this is not a coupled charge-conserving compact MOS model or a SOA prediction.

分阶段积分细化假设轨迹；它不是耦合电荷守恒MOS紧凑模型，也不预测SOA。

**Extension and required evidence / 扩展与所需证据**

Need bias/temperature C–V, gate-charge and double-pulse traces with de-embedded current definitions; separate measured E_on contributions before fitting.

需偏置/温度C–V、栅电荷和去嵌入双脉冲波形，并明确电流定义；拟合前先分清实测E_on的组成。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

## P02 — Dead-time diode and reverse recovery

死区二极管与反向恢复

[GIF: P02_100V_25C](../simulation/V3-3/education/gifs/P02.gif) · [STL: V33_P02](../printing/stl/V33_P02.stl)

**Assumptions / 模型假设**

Four ideal phases set the inductor trajectory; a separately specified recovery pulse does not feed back into the switch node.

四个理想阶段决定电感轨迹，独立规定的恢复脉冲不反馈到开关节点。

**Derivation / research question / 推导／研究问题**

Integrate inductor volt-seconds across HS/dead/LS/dead intervals; derive the duty correction caused by two diode-drop intervals.

积分高侧/死区/低侧/死区各阶段的电感伏秒，推导两段二极管压降引起的占空比修正。

**Validity and error / 有效性与误差**

Closed-form trajectories already have negligible discretization error. Carrier transport, Coss commutation and gate overlap remain uncoupled.

闭式轨迹的离散误差已很小；载流子输运、Coss换流及栅交叠仍未耦合。

**Extension and required evidence / 扩展与所需证据**

Measure recovery versus current, temperature, di/dt and reverse voltage; couple those results to a validated commutation loop before optimizing dead time.

需测量电流、温度、di/dt及反压相关恢复特性；与经验证的换流环耦合后才能优化死区。

Sources / 来源: [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

## P03 — Floating bootstrap supply and UVLO margin

浮地自举供电与欠压裕量

[GIF: P03_100V_25C](../simulation/V3-3/education/gifs/P03.gif) · [STL: V33_P03](../printing/stl/V33_P03.stl)

**Assumptions / 模型假设**

An imposed switching schedule alternates depletion and exponential recharge relative to the moving source node.

规定的开关时序使电容相对移动源极交替放电和指数充电。

**Derivation / research question / 推导／研究问题**

Compose the per-cycle affine voltage map; solve its fixed point and minimum V_BS as duty approaches one.

组合每周期仿射电压映射，求不动点及占空比趋近1时的最小V_BS。

**Validity and error / 有效性与误差**

Exact recursion is numerically converged but excludes negative-SW overcharge, startup charging and real leakage/recovery. It cannot certify high-duty operation.

精确递推在数值上收敛，但遗漏负SW过充、启动充电和真实漏电/恢复，不能认证高占空比工作。

**Extension and required evidence / 扩展与所需证据**

Measure driver current, gate charge, diode behavior and bias-dependent capacitor value; validate startup and worst-case recharge windows.

需测量驱动电流、栅电荷、二极管特性及电容偏压特性，并验证启动和最差充电窗口。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

## P04 — Level-shifter common-mode disturbance

电平移位接收端共模扰动

[GIF: P04_100V_25C_strong](../simulation/V3-3/education/gifs/P04.gif) · [STL: V33_P04](../printing/stl/V33_P04.stl)

**Assumptions / 模型假设**

A prescribed linear edge drives a first-order RC network with no nonlinear rail limiting.

预设线性边沿驱动一阶RC网络，没有非线性电源轨限幅。

**Derivation / research question / 推导／研究问题**

For a constant slew S, derive V_peak=R_rx C_cm S[1−exp(−t_r/τ)] with τ=R_rx(C_rx+C_cm); compare short- and long-edge limits.

恒定变化率S下推导峰值R_rx C_cm S[1−exp(−t_r/τ)]，其中τ=R_rx(C_rx+C_cm)，比较短、长边沿极限。

**Validity and error / 有效性与误差**

An analytic peak only validates this RC reduction. The cited 20 V and 400 V circuits neither calibrate it nor prove any catalogued foundry rating.

解析峰值只验证此RC简化；所引20 V和400 V电路既未校准本模型，也不能证明目录中晶圆厂的耐压。

**Extension and required evidence / 扩展与所需证据**

Need extracted coupling, receiver clamp I–V, latch sensitivity and measured positive/negative common-mode transients before a CMTI claim.

作CMTI声明前，需要提取耦合参数、接收端钳位I–V、锁存敏感性以及正负共模瞬态实测。

Sources / 来源: [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

## P05 — Current-sense amplifier and delayed comparator

电流检测放大器与延迟比较器

[GIF: P05_25C](../simulation/V3-3/education/gifs/P05.gif) · [STL: V33_P05](../printing/stl/V33_P05.stl)

**Assumptions / 模型假设**

The input current is prescribed; a first-order amplifier and fixed 35 ns comparator delay are deterministic.

输入电流预设，一阶放大器及固定35 ns比较器延迟均为确定性假设。

**Derivation / research question / 推导／研究问题**

Solve the exponential crossing time before adding propagation delay. Explain why total alert delay is not equal to comparator-only delay.

先解指数响应的过阈值时间，再加传播延迟；解释完整告警链延迟为何不等于比较器本体延迟。

**Validity and error / 有效性与误差**

Event placement is refined, while the analytic trip-time metric was already exact. Offset is assumed; noise, blanking and common-mode recovery are absent.

改进的是事件定位，解析触发时刻指标原已精确；失调是假设，未含噪声、消隐及共模恢复。

**Extension and required evidence / 扩展与所需证据**

Measure step response, offset drift, threshold dispersion and delay versus overdrive; high-side sensing needs an additional verified common-mode design.

需测阶跃响应、失调漂移、阈值分散及过驱相关延迟；高侧检测还需要另行验证的共模设计。

Sources / 来源: [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

## P06 — HV startup supply and hysteretic UVLO

高压启动供电与迟滞欠压锁定

[GIF: P06_100V_25C](../simulation/V3-3/education/gifs/P06.gif) · [STL: V33_P06](../printing/stl/V33_P06.stl)

**Assumptions / 模型假设**

Piecewise load states, an imposed interruption and an ideal clamp replace a full bias-generator circuit.

分段负载状态、预设中断与理想钳位代替完整偏置发生电路。

**Derivation / research question / 推导／研究问题**

Derive threshold event times and integrate source dissipation (V_in−V_aux)I_start. Which domain changes invalidate a constant-current segment?

推导阈值事件时刻，积分源损耗(V_in−V_aux)I_start；哪些工作域变化会使恒流分段失效？

**Validity and error / 有效性与误差**

Event-aligned exactness holds only in the checked constant-current domain. No JFET transport, handover circuit, clamp SOA or startup-rating guarantee is modeled.

事件对齐的精确性仅限已检查的恒流域；未模拟JFET输运、接管电路、钳位SOA或保证启动范围。

**Extension and required evidence / 扩展与所需证据**

Require startup I–V/compliance, leakage, auxiliary handover and threshold distributions across input and temperature.

需不同输入和温度下的启动I–V/顺从范围、漏电、辅助供电接管及阈值分布。

Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

## P07 — Switch-node parasitic ringing and damping

开关节点寄生振铃与阻尼

[GIF: P07_100V_damped](../simulation/V3-3/education/gifs/P07.gif) · [STL: V33_P07](../printing/stl/V33_P07.stl)

**Assumptions / 模型假设**

A constant Coss linearization, fixed L and R, and an imposed voltage excess form an unforced second-order system.

恒定Coss线性化、固定L/R及预设过压构成无外驱二阶系统。

**Derivation / research question / 推导／研究问题**

Use the characteristic polynomial to derive critical damping, then prove energy decay from the two state equations.

由特征多项式推导临界阻尼，再由两条状态方程证明能量衰减。

**Validity and error / 有效性与误差**

Quadrature refinement improves the energy audit; the initial peak is imposed, not predicted from a switching edge. No EMI or repetitive snubber power follows.

细化积分改进能量核算；初始峰值是给定而非由开关边沿预测，不能据此推算EMI或周期吸收功率。

**Extension and required evidence / 扩展与所需证据**

Measure ringing frequency and decay, extract loop parasitics, then validate a separately specified snubber topology and its dissipation.

需测振铃频率与衰减、提取回路寄生，再验证另行指定的吸收器拓扑及损耗。

Sources / 来源: [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

## P08 — DC/DC separated losses and thermal budget

DC/DC分项损耗与热预算

[GIF: P08_100V_25C](../simulation/V3-3/education/gifs/P08.gif) · [STL: V33_P08](../printing/stl/V33_P08.stl)

**Assumptions / 模型假设**

Matched Coss curves and one hard upper turn-on per cycle yield E_upper+(V_in Q_lower−E_lower)=V_in Qoss; Qrr and load-channel overlap are separate.

匹配Coss、每周期一次高侧硬导通，使E_upper+(V_in Q_lower−E_lower)=V_in Qoss；Qrr与负载沟道交叠分列。

**Derivation / research question / 推导／研究问题**

Derive the matched-capacitance energy identity without assuming constant capacitance. For thermal fixed-point iteration, examine |R_θ dP/dT| near the solution.

不假设恒定电容，推导匹配双电容能量恒等式；对热不动点迭代，考察解附近|R_θ dP/dT|。

**Validity and error / 有效性与误差**

Tight residuals certify the ledger calculation only. Full E_on must not be added again to separately counted overlap/Coss/Qrr; no measured efficiency claim is made.

小残差只证明账本运算；已分别计入交叠/Coss/Qrr时不可再叠加完整E_on，不宣称实测效率。

**Extension and required evidence / 扩展与所需证据**

Need loss-resolved double-pulse data, magnetic/ESR loss and multi-node transient thermal measurements under a specified PCB/cooling condition.

需分项双脉冲损耗、磁性/ESR损耗及指定PCB和散热条件下的多节点瞬态热测量。

Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

## P09 — Averaged buck soft-start and current-reference limit

平均Buck软启动与电流参考限幅

[GIF: P09_100V_25C](../simulation/V3-3/education/gifs/P09.gif) · [STL: V33_P09](../printing/stl/V33_P09.stl)

**Assumptions / 模型假设**

Averaged states omit PWM ripple; PI saturation and anti-windup introduce piecewise control behavior. P08 losses are not injected into this plant.

平均状态不含PWM纹波，PI饱和及抗饱和引入分段控制行为；功率级未注入P08损耗。

**Derivation / research question / 推导／研究问题**

Derive the averaged plant and current-limited equilibrium; compare control saturation events under RK4 step refinement and an adaptive reference solver.

推导平均功率级和限流平衡点，比较RK4步长细化与自适应参考求解器的控制饱和事件。

**Validity and error / 有效性与误差**

The reference’s tolerance comparison is empirical, not a rigorous bound. A 10 µs saved trace cannot resolve sub-cycle spikes or subharmonics.

参考解的容差比较为经验估计，并非严格界限；10 µs保存间隔无法分辨周期内尖峰或次谐波。

**Extension and required evidence / 扩展与所需证据**

Add sampled-cycle control, slope compensation and magnetic saturation only with explicit timing and hardware data; validate load steps independently.

只有具备明确时序和硬件数据后，才可增加采样周期控制、斜坡补偿和磁饱和，并独立验证负载阶跃。

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

Check substrate coupling, body bias and floating-domain transients independently. The ISO boundary supplies no DTI dimensions, breakdown data or isolation qualification.

分别研究衬底耦合、体偏置和浮动域瞬态；ISO边界不提供DTI尺寸、击穿数据或隔离认证。

[STL](../printing/stl/V1_M01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M02 — Low-side NLDMOS

低侧NLDMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Measure R_on, Qoss and recovery in the actual body connection. A lateral drawing cannot predict avalanche SOA or reverse-recovery transport.

需按真实体端连接测R_on、Qoss及恢复；横向图形不能预测雪崩SOA或恢复输运。

[STL](../printing/stl/V1_M02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M03 — High-voltage PLDMOS

高压PLDMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Extract polarity-correct threshold, mobility and body-junction data; do not infer equal N/P on-resistance or identical isolation from a mirrored teaching geometry.

需提取正确极性的阈值、迁移率及体结数据；不能因教学外形镜像而假定N/P导通电阻和隔离相同。

[STL](../printing/stl/V1_M03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M04 — Drain-extended NMOS

高压DENMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A drain extension is a structural concept, not an extracted RESURF solution. Need doping, field plates, bias-dependent capacitance and breakdown measurements.

漏延伸是结构概念，不是已求解的RESURF；需掺杂、场板、偏置相关电容及击穿测量。

[STL](../printing/stl/V1_M04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_M05 — Low-voltage NMOS

低压NMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Study body effect and intrinsic terminal charge using low-voltage I–V/C–V data. This legacy shape and tied-body law do not qualify operation at a 150 V switch node.

可用低压I–V/C–V研究体效应与内禀端口电荷；旧外形及绑体模型不能证明可接150 V开关节点。

[STL](../printing/stl/V1_M05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M06 — Low-voltage PMOS

低压PMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Define terminal-current signs before comparing N/P data. Mobility, NBTI and well parasitics require separate calibration, not sign reversal of an NMOS fit.

比较N/P数据前先定义端口电流符号；迁移率、NBTI和阱寄生须独立校准，不能仅将NMOS拟合改符号。

[STL](../printing/stl/V1_M06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V1_M07 — Drain-extended PMOS

高压DEPMOS

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Distinguish DEPMOS from a power PLDMOS option using process documentation and safe-operating data; no specific foundry stack follows from this model.

应结合工艺文档与安全工作数据区分DEPMOS和功率PLDMOS选项；模型不能推导某晶圆厂的具体层次。

[STL](../printing/stl/V1_M07.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_Q01 — NPN bipolar transistor

NPN双极晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The legacy model is forward-active only. Use A03 to study reciprocal injection, but obtain Gummel/output data before claiming saturation, Early effect or transit-time prediction.

旧模型仅正向放大；可用A03学习互易注入，但须有Gummel/输出数据才能研究饱和、Early效应或渡越时间预测。

[STL](../printing/stl/V1_Q01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf) · [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V1_Q02 — PNP bipolar transistor

PNP双极晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A polarity analogy does not identify a lateral or vertical PNP process. Need gain, substrate injection and charge-storage measurements for the actual structure.

极性类比不能确定横向或纵向PNP工艺；需真实结构的增益、衬底注入及电荷储存测量。

[STL](../printing/stl/V1_Q02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf) · [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V1_D01 — MOS body PN freewheel diode

体PN续流二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The legacy static junction has no recovery dynamics. P02 adds a prescribed charge pulse; physical recovery needs minority-carrier or measured switching data.

旧静态结没有恢复动态；P02增加预设电荷脉冲，物理恢复仍需少子模型或开关实测。

[STL](../printing/stl/V1_D01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

### V1_D02 — High-voltage bootstrap PN diode

高压自举PN二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Need reverse leakage, recovery charge, transient reverse voltage and thermal data. The printed depletion region proves neither blocking capability nor isolation.

需反向漏电、恢复电荷、瞬态反压及热数据；打印耗尽区不能证明阻断能力或隔离。

[STL](../printing/stl/V1_D02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V1_D03 — Schottky diode

肖特基二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Measure barrier-dependent I–V, capacitance and temperature leakage; an ideal Schottky label cannot establish a voltage grade or zero switching loss.

需势垒相关I–V、电容及温度漏电测量；肖特基标签不能证明耐压等级或零开关损耗。

[STL](../printing/stl/V1_D03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_D04 — Gate Zener clamp

栅极Zener钳位

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A sharp ideal knee omits dynamic resistance, pulse energy and tunnelling/avalanche physics. Validate clamp I–V and gate stress together.

理想锐转折遗漏动态电阻、脉冲能量及隧穿/雪崩物理；须联合验证钳位I–V和栅应力。

[STL](../printing/stl/V1_D04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_J01 — High-voltage startup JFET

高压启动JFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Pinch-off geometry, gate leakage and high-voltage dissipation are uncalibrated. P06 is a separate behavioral source, not a validated JFET replacement.

夹断几何、栅漏和高压损耗均未校准；P06是另一个行为源，并非已验证的JFET替代模型。

[STL](../printing/stl/V1_J01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V1_R01 — High-voltage polysilicon resistor chain

高压多晶硅电阻链

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Need voltage coefficient, temperature coefficient, parasitic leakage and per-segment limits; the number of printed sections is not a high-voltage design rule.

需电压系数、温度系数、寄生漏电及每段限值；打印段数不是高压设计规则。

[STL](../printing/stl/V1_R01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V1_R02 — Current-sense resistor

电流检测电阻

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Separate contact/trace resistance and inductive pickup from the intended shunt. Kelvin sensing would be a circuit extension, not already validated by this print.

应将接触/走线电阻及感应干扰与目标分流电阻区分；开尔文检测属于电路扩展，并未被该打印件验证。

[STL](../printing/stl/V1_R02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

### V1_C01 — MIM capacitor

MIM电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Characterize dielectric leakage, breakdown, voltage/temperature coefficients and matching. The legacy 5 V example does not establish a high-voltage rating.

需介质漏电、击穿、电压/温度系数及匹配数据；旧5 V例子不能证明高压额定。

[STL](../printing/stl/V1_C01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf) · [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V1_C02 — MOM capacitor

MOM电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Use field extraction and matching data with the actual metal stack; exaggerated printed spacing cannot substitute for layout design rules or parasitic extraction.

需实际金属层次的场提取及匹配数据；放大的打印间距不能替代版图规则或寄生提取。

[STL](../printing/stl/V1_C02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf) · [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf)

### V1_I01 — Isolation junction and DTI equivalent network

隔离结与DTI等效网络

Isolation equivalent/structure concept / 隔离等效/结构概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The catalogue combines equivalent isolation concepts, not one qualified DTI stack. Need bias/frequency leakage-capacitance, latch-up and breakdown tests.

目录组合隔离等效概念，并非某个合格DTI层次；需偏置/频率相关漏电电容、闩锁及击穿测试。

[STL](../printing/stl/V1_I01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V1_E01 — High-voltage ESD clamp equivalent

高压ESD钳位等效器件

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

This is a functional board, not an SCR or ggNMOS cross-section. No snapback, second breakdown or HBM/CDM qualification can be inferred.

此为功能展示板，不是SCR或ggNMOS剖面，不能推断回滞、二次击穿或HBM/CDM认证。

[STL](../printing/stl/V1_E01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json)

### V1_L01 — External power inductor

外接功率电感

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Measure inductance versus bias/frequency, saturation, DCR and core loss. The teaching core does not solve a magnetic field or establish current rating.

需偏置/频率相关电感、饱和、直流电阻及磁芯损耗；教学磁芯不求解磁场，也不确定额定电流。

[STL](../printing/stl/V1_L01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

### V1_C03 — External output capacitor

外接输出电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Effective capacitance under DC bias, ESR/ESL, ripple current and control-loop interaction require characterization; no dielectric or package is reconstructed.

直流偏压下有效电容、ESR/ESL、纹波电流及环路相互作用需测量，未重建介质材料或封装。

[STL](../printing/stl/V1_C03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

### V1_C04 — External input capacitor

外接输入电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Check input ripple spectrum, RMS current, bias derating and layout inductance. High absolute bus voltage in a model is not a manufactured capacitor rating.

需检查输入纹波谱、有效值电流、偏压降额和布局电感；模型中的高母线电压不等于制造电容额定值。

[STL](../printing/stl/V1_C04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [base:D01](../simulation/V3-3/MODEL_CARDS.md) · [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

### V1_C05 — External bootstrap capacitor

外接自举电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Validate minimum local supply, recharge window, leakage and negative-node overcharge. The print does not specify package clearance or high-side isolation.

需验证最小局部供电、充电窗口、漏电及负节点过充；打印件不规定封装爬电间距或高侧隔离。

[STL](../printing/stl/V1_C05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V2_N01 — SiC vertical MOSFET

SiC垂直MOSFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The legacy law is an assumed terminal model, not a SiC interface-trap or polytype solution. Need gate reliability, temperature I–V/C–V and switching data.

旧式是端口假设模型，并非SiC界面陷阱或晶型求解；需栅可靠性、温度I–V/C–V及开关数据。

[STL](../printing/stl/V2_N01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N02 — Enhancement-mode GaN HEMT

增强型GaN HEMT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

An assumed trap state does not reconstruct trap energy or p-GaN/recessed/MIS fabrication. Validate dynamic R_on, gate limits and reverse-conduction behavior independently.

假设的陷阱状态不能重建能级或p-GaN/凹槽/MIS工艺；须分别验证动态R_on、栅限值及反向导通。

[STL](../printing/stl/V2_N02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/) · [legacy:P25](https://researchportal.hkust.edu.hk/en/publications/dynamic-performance-of-aln-passivated-algangan-mis-high-electron-/)

### V2_N03 — Silicon superjunction MOSFET

硅超结MOSFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

No pillar charge-balance or avalanche solution is implemented. Doping/profile tolerances, nonlinear Coss and body-diode behavior need separate data.

未实现柱电荷平衡或雪崩求解；掺杂/轮廓公差、非线性Coss与体二极管特性需另有数据。

[STL](../printing/stl/V2_N03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P01](https://ieeexplore.ieee.org/document/7862945/)

### V2_N04 — IGBT

IGBT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The authored tail constant is not a carrier-lifetime extraction. Need conductivity-modulation, switching and temperature data; IGBT is not a default 40–150 V buck choice.

人为尾电流时间常数不是提取的载流子寿命；需电导调制、开关及温度数据，IGBT并非40～150 V降压的默认选型。

[STL](../printing/stl/V2_N04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N05 — SiC JBS rectifier

SiC JBS整流二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The print shows topology, not a solved shielding field. Reverse leakage, surge behavior and capacitive switching charge need characterized SiC junction data.

打印显示拓扑而非已求解屏蔽电场；反向漏电、浪涌及电容开关电荷需SiC结表征数据。

[STL](../printing/stl/V2_N05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_N06 — FinFET

FinFET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The stored smooth terminal law is not BSIM-CMG or a quantum confinement solution. Need actual fin dimensions, contact resistance and calibrated multigate data.

保存的平滑端口式不是BSIM-CMG或量子限域解；需实际鳍尺寸、接触电阻及多栅校准数据。

[STL](../printing/stl/V2_N06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P04](https://arxiv.org/abs/2005.02580)

### V2_N07 — a-IGZO thin-film transistor

a-IGZO TFT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A square-law reduction omits distributed trap states and bias-stress kinetics. Need sweep-rate, illumination, temperature and contact-length dependence.

平方律简化遗漏分布陷阱及偏压应力动力学；需扫描速度、照明、温度及接触长度相关数据。

[STL](../printing/stl/V2_N07.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P05](https://www.nature.com/articles/nature03090)

### V2_N08 — Organic polymer TFT

有机聚合物TFT

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The illustrative strain coefficient is not a mechanical or hopping-transport model. Measure transfer curves under strain cycles, atmosphere and contact conditions.

示意应变系数不是力学或跳跃输运模型；需应变循环、环境和接触条件下的转移曲线。

[STL](../printing/stl/V2_N08.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P06](https://www.nature.com/articles/nature25494)

### V2_N09 — Contact-limited MoS2 FET

MoS2接触受限FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A fixed series resistance does not solve a Schottky barrier or thickness-dependent band structure. Use transfer-length or four-terminal data versus gate bias.

固定串联电阻不求解肖特基势垒或厚度相关能带；需栅偏相关传输长度法或四端数据。

[STL](../printing/stl/V2_N09.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P07](https://pubs.acs.org/doi/10.1021/nl303583v)

### V2_N10 — Ambipolar graphene FET

石墨烯双极性FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The conductance minimum and smoothing voltage are assumed. Need residual carrier density, contact doping and bias/temperature data before a transport interpretation.

最小电导及平滑电压是假设；输运解释需剩余载流子密度、接触掺杂及偏置/温度数据。

[STL](../printing/stl/V2_N10.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P08](https://www.science.org/doi/10.1126/science.1102896)

### V2_N11 — Ballistic carbon-nanotube FET

碳纳米管弹道FET

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The single-subband Landauer example omits scattering, contact-barrier self-consistency and tube diameter distribution. Need length/contact and temperature series.

单子带Landauer示例遗漏散射、接触势垒自洽和管径分布；需长度、接触和温度系列数据。

[STL](../printing/stl/V2_N11.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P19](https://www.nature.com/articles/nature22994) · [legacy:P24](https://ieeexplore.ieee.org/document/1224486/)

### V2_N12 — Ferroelectric FET memory cell

FeFET铁电存储晶体管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The rate-independent relay ensemble has no domain kinetics, retention or fatigue prediction. Pulse-width and read-disturb data are needed for memory reliability.

率无关继电单元集合不预测畴动力学、保持或疲劳；存储可靠性需脉宽及读干扰数据。

[STL](../printing/stl/V2_N12.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P09](https://www.nature.com/articles/s41928-020-00492-7)

### V2_N13 — Oxide RRAM cell

氧化物RRAM

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The filament is a symbol, not a predicted microscopic shape. Forming, stochastic switching, compliance and endurance require measured pulse distributions.

细丝仅为符号，不是预测的微观形状；成形、随机开关、限流及耐久需实测脉冲分布。

[STL](../printing/stl/V2_N13.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P10](https://www.nature.com/articles/s41928-018-0092-2) · [legacy:P19](https://www.nature.com/articles/nature22994)

### V2_N14 — Phase-change memory cell

PCM相变存储单元

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Threshold temperatures are illustrative, with no latent heat, nucleation or spatial melt solution. Use pulse-dependent resistance and transient thermal data.

阈值温度是示意值，未含潜热、成核或空间熔融求解；需脉冲相关电阻及瞬态热数据。

[STL](../printing/stl/V2_N14.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P10](https://www.nature.com/articles/s41928-018-0092-2)

### V2_N15 — Magnetic tunnel junction

MTJ磁隧道结

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The deterministic two-state law omits LLG dynamics and thermal switching probability. Need resistance-bias, write-error and retention statistics.

确定性双态式遗漏LLG动力学和热激活开关概率；需电阻—偏置、写入误码及保持统计。

[STL](../printing/stl/V2_N15.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P11](https://www.sciencedirect.com/science/article/pii/S1369702117304285)

### V2_N16 — Ferroelectric capacitor

铁电电容

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The threshold ensemble is not Landau–Khalatnikov dynamics or material fitting. Need area/thickness, rate-dependent loops, leakage and fatigue data.

阈值集合不是Landau–Khalatnikov动力学或材料拟合；需面积/厚度、速率相关回线、漏电及疲劳数据。

[STL](../printing/stl/V2_N16.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P09](https://www.nature.com/articles/s41928-020-00492-7) · [legacy:P23](https://www.science.org/doi/10.1126/science.1169678)

### V2_N17 — Nitride LED

氮化物LED

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The port law has an empirical droop term, not quantum-well recombination or optical extraction. Need calibrated optical power, spectra and junction-temperature data.

端口式含经验效率下降项，不求解量子阱复合或光提取；需校准光功率、光谱及结温数据。

[STL](../printing/stl/V2_N17.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P12](https://www.nature.com/articles/nphoton.2009.32)

### V2_N18 — Quantum-dot LED

量子点LED

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

A fixed wavelength and EQE curve do not model exciton balance, size distributions or degradation. Need spectrum, charge balance and time-dependent efficiency measurements.

固定波长及EQE曲线不模拟激子平衡、尺寸分布或退化；需光谱、电荷平衡及效率随时间测量。

[STL](../printing/stl/V2_N18.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P13](https://www.nature.com/articles/370354a0)

### V2_N19 — PIN photodetector

PIN光电探测器

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Fixed responsivity, constant capacitance and one time constant omit wavelength response, shot noise and transport. Need spectral responsivity, dark I–V and bandwidth.

固定响应度、固定电容及单时间常数遗漏光谱响应、散粒噪声和输运；需光谱响应度、暗态I–V及带宽。

[STL](../printing/stl/V2_N19.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_N20 — Single-junction photovoltaic cell

单结光伏电池

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

This generic law does not reproduce the cited perovskite architecture. Need illumination/temperature I–V, area, spectral response and calibrated incident power.

通用方程不复现引用的钙钛矿结构；需光照/温度I–V、面积、光谱响应和校准入射功率。

[STL](../printing/stl/V2_N20.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P14](https://www.science.org/doi/10.1126/science.1228604)

### V2_N21 — Thermoelectric generator cell

热电发电单元

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

For constant coefficients, check Q_hot−Q_cold=VI. Temperature-dependent material data and contact thermal resistances are needed beyond the lumped steady model.

恒系数下检查Q_hot−Q_cold=VI；扩展集总稳态模型需温度相关材料数据及接触热阻。

[STL](../printing/stl/V2_N21.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P15](https://www.nature.com/articles/nmat2090)

### V2_N22 — On-chip coupled transformer

片上耦合变压器

Passive component concept / 无源元件概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

No geometry-based electromagnetic extraction is performed. Validate S-parameters, self-resonance, Q and substrate dependence before RF layout claims.

未做基于几何的电磁提取；射频版图结论需要S参数、自谐振、Q及衬底相关验证。

[STL](../printing/stl/V2_N22.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P16](https://ieeexplore.ieee.org/document/720393/)

### V2_N23 — Through-silicon via

TSV硅通孔

Interconnect concept / 互连概念

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The example omits distributed propagation, multi-via coupling and stress. Need geometry/material extraction and calibrated high-frequency test structures.

示例遗漏分布传播、多孔耦合及应力；需几何/材料提取和校准高频测试结构。

[STL](../printing/stl/V2_N23.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P17](https://ieeexplore.ieee.org/document/5340655/)

### V2_N24 — Mach-Zehnder electro-optic modulator

MZI电光调制器

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The cosine transfer law omits waveguide modes, carrier dynamics and travelling-wave electrodes. Need Vπ, insertion loss, bias drift and electro-optic bandwidth data.

余弦传输式遗漏波导模式、载流子动态及行波电极；需Vπ、插损、偏置漂移及电光带宽数据。

[STL](../printing/stl/V2_N24.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_N25 — Semiconductor laser diode

半导体激光二极管

Illustrative physical-device structure / 示意实体器件结构

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The threshold law has no carrier/photon rate equations, linewidth or mode competition. Need temperature L–I–V, modulation and spectral measurements.

阈值式没有载流子/光子速率方程、线宽或模式竞争；需温度相关L–I–V、调制及光谱测量。

[STL](../printing/stl/V2_N25.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P18](https://www.nature.com/articles/s41467-024-44750-0)

### V2_X01 — MOS gate charge and Miller coupling

MOS栅电荷与Miller耦合

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Distinguish this coupled fixed-C system from P01’s prescribed nonlinear-charge stages. Neither represents a full calibrated charge-partition compact model.

应区分该固定C耦合系统与P01预设非线性电荷阶段；两者均非完整校准的电荷分配紧凑模型。

[STL](../printing/stl/V2_X01.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf)

### V2_X02 — PN diode reverse recovery

PN二极管反向恢复

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Qrr is an input assumption. Validate with double-pulse data over temperature and di/dt; do not interpret the printed markers as measured carrier density.

Qrr是输入假设；需不同温度及di/dt双脉冲验证，不能把打印标记当成实测载流子密度。

[STL](../printing/stl/V2_X02.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P02](https://ieeexplore.ieee.org/document/7815312/)

### V2_X03 — MOS conduction-loss thermal feedback

MOS导通损耗自热反馈

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Analyze stability of Cθ dθ/dt=I²R(T)−θ/Rθ, including I²R25αRθ. A single-node solution is not a 3D hotspot or lifetime model.

分析Cθ dθ/dt=I²R(T)−θ/Rθ及I²R25αRθ的稳定性；单节点解不是三维热点或寿命模型。

[STL](../printing/stl/V2_X03.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### V2_X04 — PMOS NBTI aging

PMOS NBTI老化

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

No recovery, reaction–diffusion or trap kinetics is solved. Stress/recovery timing, duty cycle and process-specific distributions are required for lifetime inference.

未求解恢复、反应—扩散或陷阱动力学；寿命推断需应力/恢复时序、占空比及工艺分布。

[STL](../printing/stl/V2_X04.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P20](https://www.sciencedirect.com/science/article/pii/S0026271404001751)

### V2_X05 — MOS flicker and thermal noise

MOS 1/f与热噪声

Mechanism demonstration / 机制演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

The PSD is not a generated time waveform or a trap-density extraction. Check one-sided conventions, bias dependence and input/output noise referral.

频谱不是生成的时间波形，也不是陷阱密度提取；须检查单边约定、偏置依赖及输入/输出噪声折算。

[STL](../printing/stl/V2_X05.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P21](https://ieeexplore.ieee.org/document/34242/) · [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V2_X06 — MOS threshold and resistance statistics

MOS阈值及电阻统计分散

Parameter/statistical demonstration / 参数/统计演示

Historical structure; electrical simulation not rerun this release

历史结构；本轮未重跑其电学仿真

Do not transfer A04’s pair-correlation interpretation automatically. Validate the joint parameter distribution and sample uncertainty with process measurements.

不能自动套用A04的配对相关解释；需工艺测量验证联合参数分布及抽样不确定度。

[STL](../printing/stl/V2_X06.stl) · Sources / 来源: [catalog:printing](../printing/catalogue.json) · [legacy:P22](https://ieeexplore.ieee.org/document/1210771/) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_A01 — Four-terminal MOS interpolation

四端MOS连续插值

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

The revision improves derivatives of the authored equation. Missing DIBL, velocity saturation and intrinsic charge partition can dominate physical error.

本次基线改进的是人为方程的导数计算。未包含的DIBL、速度饱和及内禀电荷分配可能主导物理误差。

[STL](../printing/stl/V33_A01.stl) · Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V33_A02 — Junction charge and varactor

结电荷与变容二极管

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Rationalization removes cancellation near zero; a stress-test percentage does not describe accuracy of the entire plotted C–V range or measured junction.

有理化消除零附近的相消误差；压力测试的改善比例不能代表全部C–V区间或实测结的准确度。

[STL](../printing/stl/V33_A02.stl) · Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V33_A03 — Reciprocal NPN Ebers–Moll

满足互易关系的NPN Ebers–Moll

Illustrative physical-device structure / 示意实体器件结构

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

An expm1 implementation has floating-point-scale KCL residuals. That does not validate β versus current, Early effect or RF behavior.

expm1实现的KCL残差处于浮点量级；这不验证电流相关β、Early效应或射频行为。

[STL](../printing/stl/V33_A03.stl) · Sources / 来源: [base:B07](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf)

### V33_A04 — MOS pair mismatch and correlation

MOS配对失配与相关性

Parameter/statistical demonstration / 参数/统计演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

80,000 samples reduce sampling uncertainty; a particular sample standard deviation can still move farther from the analytic value. No yield gain follows.

80000个样本降低抽样不确定度；某次样本标准差仍可能更远离解析值，也不能据此宣称良率提高。

[STL](../printing/stl/V33_A04.stl) · Sources / 来源: [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_B01 — MOS differential pair

MOS差分对

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

The 80-step solution is already at double-precision resolution. A small KCL residual does not establish bandwidth, CMRR or input offset.

80步求解已达到双精度分辨率；很小的KCL残差不等于已验证带宽、共模抑制比或输入失调。

[STL](../printing/stl/V33_B01.stl) · Sources / 来源: [base:B01](https://link.springer.com/article/10.1007/BF01239381)

### V33_B02 — CTAT/PTAT reference sum

CTAT/PTAT基准合成

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Analytic evaluation has negligible numerical residual; curvature and missing mismatch dominate the interpretation. It is not a reproduction of Brokaw’s measured circuit.

解析求值的数值残差很小，但曲率及未建模失配限制结论；它不复现Brokaw的实测电路。

[STL](../printing/stl/V33_B02.stl) · Sources / 来源: [base:B03](https://class.ece.iastate.edu/djchen/ee501/2013/bandgaprefpaperbypaulbrokawjssc1974.pdf)

### V33_B03 — Input noise and sampled kT/C

输入噪声与采样kT/C

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Analytic quadrature improves a metric of the chosen PSD. Unknown current noise, source impedance, aliasing and switching ripple remain physical gaps.

解析积分改进选定频谱的指标计算；电流噪声、源阻抗、混叠和开关纹波仍是物理缺项。

[STL](../printing/stl/V33_B03.stl) · Sources / 来源: [base:B08](https://www.analog.com/en/resources/technical-articles/2018/05/25/03/08/to-chop-or-auto-zero-that-is-the-question.html)

### V33_B04 — Capacitor DAC and SAR ADC

电容DAC与SAR ADC

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

A machine-precision threshold search does not improve physical ENOB. Ideal SNR formulas require their input and quantization assumptions; use SNDR for ENOB here.

机器精度的边界搜索并不提高实物ENOB；理想SNR公式有输入与量化假设，本例ENOB应由SNDR换算。

[STL](../printing/stl/V33_B04.stl) · Sources / 来源: [base:B05](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) · [base:B02](https://ewh.ieee.org/r5/denver/sscs/References/1989_10_Pelgrom.pdf)

### V33_B05 — LDO loop and load step

LDO环路与负载阶跃

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Exact matrix propagation removes discretization of this linear system, not errors in assumed loop poles or measured phase margin.

精确矩阵传播消除该线性系统的离散误差，不能消除假设极点或实测相位裕度的不确定性。

[STL](../printing/stl/V33_B05.stl) · Sources / 来源: [base:B06](https://rincon-mora.gatech.edu/publicat/jrnls/jssc98_lv_ldo.pdf)

### V33_B06 — Phase loop and noise transfer

相位环路与噪声传递

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Exact state evolution and refined quadrature do not capture ISF, cyclostationary noise, cycle slips or acquisition.

精确状态演化和细化积分仍不包含ISF、循环平稳噪声、周跳或捕获过程。

[STL](../printing/stl/V33_B06.stl) · Sources / 来源: [base:B09](https://chic.caltech.edu/wp-content/uploads/2013/05/general.pdf)

### V33_B07 — 40–150 V synchronous buck

40–150V同步降压

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Exact propagation and phasewise quadrature reduce numerical error. Saved ripple extrema remain sampled; conduction-only efficiency excludes many real losses.

精确传播与分段积分降低数值误差；保存的纹波极值仍来自采样，只含导通损耗的效率遗漏多项真实损耗。

[STL](../printing/stl/V33_B07.stl) · Sources / 来源: [base:D01](../simulation/V3-3/MODEL_CARDS.md)

### V33_P01 — HV MOS gate charge and switching overlap

高压MOS栅电荷与开关交叠

Mechanism demonstration / 机制演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Stagewise quadrature refines the assumed trajectory; this is not a coupled charge-conserving compact MOS model or a SOA prediction.

分阶段积分细化假设轨迹；它不是耦合电荷守恒MOS紧凑模型，也不预测SOA。

[STL](../printing/stl/V33_P01.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V33_P02 — Dead-time diode and reverse recovery

死区二极管与反向恢复

Mechanism demonstration / 机制演示

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Closed-form trajectories already have negligible discretization error. Carrier transport, Coss commutation and gate overlap remain uncoupled.

闭式轨迹的离散误差已很小；载流子输运、Coss换流及栅交叠仍未耦合。

[STL](../printing/stl/V33_P02.stl) · Sources / 来源: [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf)

### V33_P03 — Floating bootstrap supply and UVLO margin

浮地自举供电与欠压裕量

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Exact recursion is numerically converged but excludes negative-SW overcharge, startup charging and real leakage/recovery. It cannot certify high-duty operation.

精确递推在数值上收敛，但遗漏负SW过充、启动充电和真实漏电/恢复，不能认证高占空比工作。

[STL](../printing/stl/V33_P03.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S03](https://www.ti.com/lit/an/slua887a/slua887a.pdf)

### V33_P04 — Level-shifter common-mode disturbance

电平移位接收端共模扰动

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

An analytic peak only validates this RC reduction. The cited 20 V and 400 V circuits neither calibrate it nor prove any catalogued foundry rating.

解析峰值只验证此RC简化；所引20 V和400 V电路既未校准本模型，也不能证明目录中晶圆厂的耐压。

[STL](../printing/stl/V33_P04.stl) · Sources / 来源: [dcdc:S04](https://ieeexplore.ieee.org/abstract/document/10236598) · [dcdc:S10](https://ieeexplore.ieee.org/document/9724123/)

### V33_P05 — Current-sense amplifier and delayed comparator

电流检测放大器与延迟比较器

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Event placement is refined, while the analytic trip-time metric was already exact. Offset is assumed; noise, blanking and common-mode recovery are absent.

改进的是事件定位，解析触发时刻指标原已精确；失调是假设，未含噪声、消隐及共模恢复。

[STL](../printing/stl/V33_P05.stl) · Sources / 来源: [dcdc:S05](https://www.ti.com/lit/ds/symlink/ina381.pdf) · [dcdc:S12](https://www.analog.com/en/resources/app-notes/an-1308.html)

### V33_P06 — HV startup supply and hysteretic UVLO

高压启动供电与迟滞欠压锁定

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Event-aligned exactness holds only in the checked constant-current domain. No JFET transport, handover circuit, clamp SOA or startup-rating guarantee is modeled.

事件对齐的精确性仅限已检查的恒流域；未模拟JFET输运、接管电路、钳位SOA或保证启动范围。

[STL](../printing/stl/V33_P06.stl) · Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S11](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article)

### V33_P07 — Switch-node parasitic ringing and damping

开关节点寄生振铃与阻尼

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Quadrature refinement improves the energy audit; the initial peak is imposed, not predicted from a switching edge. No EMI or repetitive snubber power follows.

细化积分改进能量核算；初始峰值是给定而非由开关边沿预测，不能据此推算EMI或周期吸收功率。

[STL](../printing/stl/V33_P07.stl) · Sources / 来源: [dcdc:S07](https://www.ti.com/lit/an/slpa010/slpa010.pdf)

### V33_P08 — DC/DC separated losses and thermal budget

DC/DC分项损耗与热预算

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

Tight residuals certify the ledger calculation only. Full E_on must not be added again to separately counted overlap/Coss/Qrr; no measured efficiency claim is made.

小残差只证明账本运算；已分别计入交叠/Coss/Qrr时不可再叠加完整E_on，不宣称实测效率。

[STL](../printing/stl/V33_P08.stl) · Sources / 来源: [dcdc:S01](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) · [dcdc:S02](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) · [dcdc:S08](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### V33_P09 — Averaged buck soft-start and current-reference limit

平均Buck软启动与电流参考限幅

Functional circuit/system board / 电路/系统功能展示板

Current numerical baseline rerun; educational scope only

现有数值基线已重跑；仅限教学范围

The reference’s tolerance comparison is empirical, not a rigorous bound. A 10 µs saved trace cannot resolve sub-cycle spikes or subharmonics.

参考解的容差比较为经验估计，并非严格界限；10 µs保存间隔无法分辨周期内尖峰或次谐波。

[STL](../printing/stl/V33_P09.stl) · Sources / 来源: [dcdc:S06](https://www.ti.com/lit/ds/symlink/lm5116.pdf) · [dcdc:S09](https://authors.library.caltech.edu/records/ac87w-mn171)

## Evidence boundary

## 依据边界

Existing source provenance is preserved. Three primary URLs were reopened for focused teaching checks; other entries retain their earlier read scope. This is not a new comprehensive paper audit, and references do not calibrate the authored model coefficients.

保留既有来源追溯，另打开3个一手网址作定向教学核对；其余保留原阅读范围。这不是新一轮全面论文审计，引用也不能校准人为模型系数。

Equations are teaching relations, not normative standards or complete SPICE implementations. A simplified exercise may use illustrative values different from its GIF.

公式为教学关系式，不是规范性标准或完整SPICE实现；简化练习可使用与GIF不同的示意数值。
