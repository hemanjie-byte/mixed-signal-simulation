# V3.3 model cards

# V3.3模型卡

Coefficients remain illustrative. Numerical changes preserve the stated physical equations unless explicitly noted in each audit.

系数仍为示意假设；数值改进保留所述物理方程，具体边界见各项审计。

## A01 Four-terminal MOS interpolation

## A01 四端MOS连续插值

Id = 2 n beta Ut^2 (softplus(xs)^2 - softplus(xd)^2) (1 + lambda |Vds|). Pair-capacitor charges sum to zero.

弱反型至强反型连续电流，另用守恒的固定互电容网络表示端口电荷。

0–1.8 V low-voltage demonstration. No avalanche, oxide leakage, DIBL, velocity saturation, intrinsic charge partition or measured fit. Not full EKV/BSIM.

仅0–1.8V低压示意；无雪崩、栅漏、DIBL、速度饱和、内禀电荷分配或实测拟合；不是完整EKV/BSIM。

Numerical scope: Accuracy of the existing interpolation's derivative only; no device/PDK accuracy gain or added physics.

数值范围：仅提升既有插值公式的导数计算精度，不代表器件/PDK准确度或新增物理机制。

[GIF](../v33/education/gifs/A01.gif) · Case / 工况: `A01_transfer_25C`

Sources / 来源: B01

```json
{
  "n": 1.5,
  "beta_25_A_per_V2": 0.001,
  "Vth_25_V": 0.55,
  "dVth_dT_V_per_K": -0.001,
  "mobility_T_exponent": -1.5,
  "lambda_per_V": 0.03,
  "Cgs_F": 2e-12,
  "Cgd_F": 2e-13,
  "Cgb_F": 1e-13,
  "Cdb_Csb_F": 3e-13,
  "small_signal_method": "Analytic derivatives of the same DC law"
}
```

## A02 Junction charge and varactor

## A02 结电荷与变容二极管

C(V)=C0(1-V/phi)^(-m); Q(V)=C0 phi [1-(1-V/phi)^(1-m)]/(1-m); Idisplacement=C(V)dV/dt.

从C(V)积分得到Q(V)，瞬态位移电流为C(V)dV/dt。

Depletion capacitance only, -20 <= V < 0.35 V. No forward diffusion charge, breakdown or series resistance. Reverse leakage is an assumed 1 pA.

仅耗尽电容，-20≤V<0.35V；不含正向扩散电荷、击穿和串联电阻；反向漏电假设为1pA。

Numerical scope: Stress-test range is explicitly separate from the original plotted CV sweep; eliminates cancellation, not an across-the-board measured capacitance improvement.

数值范围：压力测试电压范围与原绘制的CV扫描明确分开；消除数值相消，不表示全部实测电容精度提高。

[GIF](../v33/education/gifs/A02.gif) · Case / 工况: `A02_CV_25C`

Sources / 来源: B07

```json
{
  "C0_25_F": 2e-12,
  "C0_TC_per_K": 0.0002,
  "phi_V": 0.7,
  "m": 0.5,
  "transient_bias_V": -2,
  "transient_amplitude_V": 1,
  "frequency_Hz": 1000000.0,
  "charge_evaluation": "Rationalized m=0.5 expression, unchanged physics"
}
```

## A03 Reciprocal NPN Ebers–Moll

## A03 满足互易关系的NPN Ebers–Moll

Ic=alphaF IF-IR; Ib=(1-alphaF)IF+(1-alphaR)IR; Ie=-IF+alphaR IR; alphaF IES=alphaR ICS=IS.

分别求解正、反向结注入，三端电流满足KCL和互易关系。

Generic silicon NPN, not a SiGe HBT. Low-injection DC only; no Early effect, high injection, transit time, RF fT or breakdown.

通用硅NPN，不是SiGe HBT；仅低注入直流，不含Early效应、大注入、渡越时间、fT及击穿。

Numerical scope: Existing closed-form expm1 evaluation is retained; residual is at floating-point scale. No numerical improvement percentage is assigned.

数值范围：保留既有expm1解析计算；残差已在浮点精度量级，不赋予数值提升百分比。

[GIF](../v33/education/gifs/A03.gif) · Case / 工况: `A03_gummel_25C`

Sources / 来源: B07

```json
{
  "IS_25_A": 1e-15,
  "betaF": 100,
  "betaR": 2,
  "Eg_eV": 1.11,
  "IS_T_exponent": 3
}
```

## A04 MOS pair mismatch and correlation

## A04 MOS配对失配与相关性

sigma(pair)=A_VT sqrt((1-rho)/(WL)); individual uncorrelated sigma=A_VT/sqrt(2WL).

区分配对标准差和单管标准差，并演示共同偏移的抵消。

Assumed Gaussian local mismatch and correlation. No foundry statistics, spatial-gradient fit, yield certification or temperature-dependent mismatch law.

高斯局部失配和相关系数为假设；无工艺统计、空间梯度拟合、良率认证或温度失配律。

Numerical scope: Reported separately from numerical accuracy. A single realized sigma estimate may move either direction; no foundry statistics or yield improvement.

数值范围：与数值准确度分开报告；单次标准差估计可能向任一方向变化，不代表工艺统计或良率改善。

[GIF](../v33/education/gifs/A04.gif) · Case / 工况: `A04_area16um2`

Sources / 来源: B02

```json
{
  "A_VT_pair_V_um": 0.003,
  "rho": 0.25,
  "samples": 80000,
  "global_sigma_V": 0.02,
  "areas_um2": [
    1,
    4,
    16,
    64
  ],
  "seed": 20261101
}
```

## B01 MOS differential pair

## B01 MOS差分对

Solve Id1(Vs)+Id2(Vs)=Itail with bisection using A01; Vg1/2=Vcm +/- Vdiff/2.

用A01求解共同源极电压，使两支路之和等于尾电流。

Fixed drain biases and ideal tail source. No amplifier load, common-mode feedback, frequency compensation or finite tail impedance.

固定漏端偏置、理想尾电流源；不含放大器负载、共模反馈、频率补偿及尾源有限阻抗。

Numerical scope: 80 bisection steps already reach double-precision resolution; retained unchanged, no fabricated 10% gain.

数值范围：80次二分已达到双精度分辨率，保持不变，不虚构10%提升。

[GIF](../v33/education/gifs/B01.gif) · Case / 工况: `B01_25C`

Sources / 来源: B01

```json
{
  "Vcm_V": 0.85,
  "Vd1_Vd2_V": 1.8,
  "Itail_A": 0.0001,
  "bisection_steps": 80
}
```

## B02 CTAT/PTAT reference sum

## B02 CTAT/PTAT基准合成

Vbe=Vg0+(Vbe0-Vg0)T/T0-eta Ut ln(T/T0); deltaVbe=Ut ln(N); Vref=Vbe+a deltaVbe; dVref/dT|T0=0.

一阶温漂在25°C相消，并保留VBE曲率；输出PTAT电流为deltaVbe/R1。

Ideal voltage sum inspired by bandgap principles, not the 2.5 V Brokaw circuit reproduction. No start-up, PSRR, trimming, resistor TC, mismatch or output load.

按带隙原理的理想电压合成，并非复现Brokaw的2.5V电路；不含启动、PSRR、修调、电阻温漂、失配及输出负载。

Numerical scope: Existing analytic evaluation is already at floating-point floor; temperature curvature and physical assumptions are unchanged.

数值范围：原解析计算已处于浮点精度下限，温度曲率及物理假设不变。

[GIF](../v33/education/gifs/B02.gif) · Case / 工况: `B02_temperature`

Sources / 来源: B03

```json
{
  "Vg0_V": 1.205,
  "Vbe0_V": 0.68,
  "eta": 3,
  "area_ratio": 8,
  "R1_ohm": 10000,
  "T0_K": 298.15
}
```

## B03 Input noise and sampled kT/C

## B03 输入噪声与采样kT/C

Splain=en^2(1+fc/f); Ssuppressed=en^2(2+fc/(f+fchop)); variance=integral S(f)df; sampled variance=kT/C.

演示抑制低频噪声时的白噪声代价；另列采样热噪声。

Illustrative spectral shaping, not a switched chopper circuit or measured op amp. No current noise, source resistance, aliasing, ripple or charge injection.

仅示意频谱整形，不是开关斩波电路或实测运放；不含电流噪声、源阻、混叠、纹波和电荷注入。

Numerical scope: Saved PSD grid is unchanged; metric integration is analytic. No transistor noise, aliasing or measured amplifier calibration is added.

数值范围：保存的PSD网格不变，指标积分改为解析式；未增加晶体管噪声、混叠或实测放大器校准。

[GIF](../v33/education/gifs/B03.gif) · Case / 工况: `B03_25C`

Sources / 来源: B08

```json
{
  "en_25_V_per_sqrtHz": 1e-08,
  "fc_Hz": 100,
  "fchop_Hz": 20000,
  "sample_C_F": 1e-12,
  "integration_band_Hz": [
    1,
    1000000.0
  ],
  "integration_method": "Analytic PSD antiderivatives; saved frequency grid unchanged"
}
```

## B04 Capacitor DAC and SAR ADC

## B04 电容DAC与SAR ADC

Binary CDAC with dummy; actual sequential-decision transition search; DNL from code widths; INL fitted to first/last internal transitions; coherent 16384-point FFT, bin 503, one-sided power with DC/Nyquist counted once.

含dummy的二进制CDAC逐位比较；搜索实际转换码边界计算DNL，首末内部转换点端点拟合计算INL；相干FFT单边功率对直流与奈奎斯特点只计一次。

Ideal comparator and full settling. No aperture jitter, thermal/comparator noise, switch leakage, reference droop or supply-current prediction. Capacitor mismatch is assumed.

比较器理想且完全建立；不含采样抖动、热噪声/比较器噪声、开关漏电、参考跌落及供电电流预测；电容失配为假设。

Numerical scope: Sequential-decision search and coherent FFT retained. Existing 60-step thresholds are at machine precision; no ENOB/physical accuracy gain is asserted.

数值范围：保留逐次判决搜索与相干FFT，原60次边界搜索已达机器精度；不声称ENOB或实物准确度提升。

[GIF](../v33/education/gifs/B04.gif) · Case / 工况: `B04_mismatch`

Sources / 来源: B05, B02

```json
{
  "bits": 10,
  "Vref_V": 1.8,
  "fs_Hz": 2000000.0,
  "samples": 16384,
  "tone_bin": 503,
  "input_amplitude_fraction_of_Vref": 0.49,
  "unit_sigma_cases": [
    0,
    0.02
  ],
  "seed": 20261101
}
```

## B05 LDO loop and load step

## B05 LDO环路与负载阶跃

C dv/dt=ip-v/R-dIload; dip/dt=wa(-Gv-ip). L(s)=G/[(Cs+1/R)(1+s/wa)].

二状态线性反馈模型，输出负载阶跃、环路增益和相位裕度。

Small perturbation around a biased operating point; no dropout, current limit, start-up, ESR zero or transistor netlist. Not a reproduction of the cited measured LDO.

围绕偏置点的小扰动模型；无压差极限、限流、启动、ESR零点或晶体管网表；并非复现引用论文的实测LDO。

Numerical scope: Removes interpolation/ODE discretization for the retained linear loop; no dropout, current limit, transistor network or measured phase-margin validation.

数值范围：消除既有线性环路的插值及ODE离散误差；未加入压差、限流、晶体管网络或实测相位裕度验证。

[GIF](../v33/education/gifs/B05.gif) · Case / 工况: `B05_25C`

Sources / 来源: B06

```json
{
  "Vin_V": 3.3,
  "Vout_nom_V": 1.8,
  "Iload_nom_A": 0.02,
  "delta_Iload_A": 0.01,
  "Cout_F": 1e-05,
  "Rload_ohm": 90,
  "G_25_A_per_V": 0.5,
  "G_T_exponent": -1.2,
  "amplifier_pole_Hz": 20000,
  "Iq_A": 3e-05,
  "dt_s": 1e-07,
  "state_propagation": "Exact real 2x2 matrix exponential",
  "unity_gain_method": "Stable analytic positive quadratic root"
}
```

## B06 Phase loop and noise transfer

## B06 相位环路与噪声传递

H(s)=wn^2/(s^2+2 zeta wn s+wn^2); Sout=|H|^2 Sref+|1-H|^2 Svco; jitter=sqrt(integral Sout df)/(2 pi fcarrier).

典型二阶相位响应与互补噪声传递，区分单边相位PSD和SSB噪声。

Canonical phase-domain abstraction without a loop zero. Not a transistor VCO, a full type-II PLL, ISF extraction, cycle-slip or acquisition simulation.

无环路零点的典型相位域抽象；不是晶体管VCO、完整二型PLL、ISF提取、周跳或捕获仿真。

Numerical scope: Canonical phase-domain response only. PSD quadrature also refined without enlarging saved traces; no transistor VCO, cycle-slip or measured-jitter accuracy claim.

数值范围：仅典型相位域响应；PSD积分也细化且不扩大保存曲线，未增加晶体管VCO、周跳或实测抖动准确度。

[GIF](../v33/education/gifs/B06.gif) · Case / 工况: `B06_zeta0.7`

Sources / 来源: B09

```json
{
  "natural_frequency_Hz": 100000.0,
  "zeta_cases": [
    0.3,
    0.7,
    1.2
  ],
  "phase_step_rad": 0.1,
  "carrier_Hz": 1000000000.0,
  "integration_band_Hz": [
    100,
    10000000.0
  ],
  "Sref_rad2_per_Hz": 1e-13,
  "Svco_floor_rad2_per_Hz": 1e-16,
  "state_propagation": "Exact real 2x2 matrix exponential",
  "PSD_integration": "16-point Gauss-Legendre per 32 log-frequency intervals"
}
```

## B07 40–150 V synchronous buck

## B07 40–150V同步降压

L di/dt=u Vin-(Rsw+RL)i-v; C dv/dt=i-v/Rload. Exact period-map initialization; exact piecewise affine propagation and 16-point phasewise Gauss integration; input-output-loss-energy balance.

解析周期映射初始化、精确分段仿射传播及16点Gauss积分；校核输入、输出、导通损耗和储能。

Forced CCM with ideal instantaneous switches. Efficiency includes conduction loss only; no switching/gate/core loss, dead time, ringing, control-loop start-up, SOA or validated voltage rating.

强制连续导通、理想瞬时开关；效率仅含导通损耗；无开关/栅极/磁芯损耗、死区、振铃、控制启动、SOA或已验证耐压。

Numerical scope: Exact affine propagation and phasewise Gauss integration improve the reduced conduction-only solution. Saved ripple extrema remain sampled; no switching-loss/real-device accuracy improvement.

数值范围：精确仿射传播与分段Gauss积分改进仅含导通损耗的简化解；纹波极值仍按保存点取样，不代表开关损耗或实物精度提升。

[GIF](../v33/education/gifs/B07.gif) · Case / 工况: `B07_100V_25C`

Sources / 来源: D01

```json
{
  "Vin_max_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "Vout_target_V": 12,
  "L_H": 0.0001,
  "C_F": 2.2e-05,
  "Rload_ohm": 12,
  "Rsw_25_ohm": 0.18,
  "RL_25_ohm": 0.12,
  "resistance_TC_per_K": 0.004,
  "fs_Hz": 250000.0,
  "steps_per_cycle": 200,
  "warmup_cycles": 35,
  "saved_cycles": 5,
  "state_propagation": "Exact affine exponential; periodic warmup traversal unnecessary",
  "metric_integration": "16-point Gauss-Legendre separately on on/off intervals"
}
```

## P01 HV MOS gate charge and switching overlap

## P01 高压MOS栅电荷与开关交叠

Cgd(v)=80pF/(1+v/20V)^0.5; Qgd=integral Cgd dv; plateau gate current=(Vdrive-Vplateau)/Rg; Vds is the inverse charge law. Eoverlap=integral max(Vds Ichannel-Ron Ichannel^2,0)dt. Qoss=integral Coss dv; Eoss=integral v Coss dv.

Miller电荷由非线性Cgd积分，平台电流决定漏压转换时间；交叠损耗积分扣除瞬时导通基线；Qoss与Eoss分别积分Coss和vCoss。

Prescribed staged commutation, not a coupled charge-conserving MOS compact model. Ichannel excludes Coss displacement and diode recovery. Fixed-C Miller appeared in V2 X01; this bench adds nonlinear charge, separate overlap/storage energies and temperature sweeps. No breakdown, avalanche, SOA, gate overshoot or layout extraction. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

人为规定阶段的换流模型，非完整电荷守恒MOS紧凑模型；沟道电流不含Coss位移和二极管恢复。V2 X01已有固定电容Miller，本版增强非线性电荷、分离交叠/储能及温度扫描；不含击穿、雪崩、SOA、栅过冲或版图提取。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: Display density is unchanged; improved metrics use stage-wise 32-point Gauss quadrature. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：显示密度不变；改进指标按阶段使用32点Gauss积分。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P01.gif) · Case / 工况: `P01_100V_25C`

Sources / 来源: S01, S02, S10

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "device_temperature_cases_C": [
    -40,
    25,
    125
  ],
  "all_coefficients": "Authored illustrative assumptions; same parameterized device across all Vin classes, no rated-voltage certification.",
  "Vdrive_V": 10,
  "Cgs_F": 8e-10,
  "Cgd0_F": 8e-11,
  "Coss_per_device_C0_F": 6e-10,
  "capacitance_V0_V": 20,
  "capacitance_exponent": 0.5,
  "Rg_on_ohm": 8,
  "Rg_off_ohm": 5,
  "gm_S": 0.5,
  "Iload_A": 1,
  "Vth_25_V": 2.2,
  "Vth_TC_V_per_K": -0.002,
  "Ron_25_ohm": 0.18,
  "Ron_TC_per_K": 0.004
}
```

## P02 Dead-time diode and reverse recovery

## P02 死区二极管与反向恢复

D=(Vout+2 td fs Vf)/Vin; L dIL/dt=Vsw-Vout in HS/dead/LS/dead phases. Qrr=0.5 Ipk trr. Ecomm=Vin Qrr is a separate prescribed bus-energy estimate.

按死区压降补偿占空比，四阶段积分电感电流；三角恢复电流满足Qrr=Ipk trr/2，另列VinQrr换流能量估算。

Periodic ideal CCM waveform; recovery pulse is separate from IL and Vsw. Vin Qrr assumes full bus voltage and is not measured diode heat. No stored-charge transport solution, Coss commutation, gate overlap or ringing. V2 X02 already imposed triangular recovery; V3.2 relates it to dead-time sizing and bus-energy accounting. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

周期理想CCM波形；恢复脉冲与IL、Vsw分别计算。VinQrr假定全母线电压，不等同实测二极管热。无载流子输运、Coss换流、栅交叠或振铃。V2 X02已有三角恢复，本版关联死区选取和母线能量核算。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: Analytical trajectory already at floating-point floor; no meaningful 10% reduction claimed. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：解析轨迹已达浮点误差底限，不宣称有意义的10%降低。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P02.gif) · Case / 工况: `P02_100V_25C`

Sources / 来源: S02

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "device_temperature_cases_C": [
    -40,
    25,
    125
  ],
  "all_coefficients": "Authored illustrative assumptions; same parameterized device across all Vin classes, no rated-voltage certification.",
  "Vout_V": 12,
  "Iout_A": 1,
  "L_H": 0.0001,
  "fs_Hz": 250000.0,
  "deadtime_each_s": 4e-08,
  "Vf_25_V": 0.8,
  "Vf_TC_V_per_K": -0.001,
  "Qrr_25_C": 1.2e-08,
  "Qrr_TC_per_K": 0.005,
  "trr_25_s": 6e-08,
  "trr_TC_per_K": 0.002,
  "recovery_rise_fraction": 0.35
}
```

## P03 Floating bootstrap supply and UVLO margin

## P03 浮地自举供电与欠压裕量

Gate event: deltaVbs=-Qg/Cboot. On: dVbs/dt=-Iq/Cboot. Off: Cboot dVbs/dt=(Vsource-Vbs)/Rcharge-Iq. Exact exponential recharge and analytical periodic map.

栅极事件消耗Qg使VBS下降，导通期间静态电流放电，关断期间经充电电阻指数恢复；解析周期映射计算最小电压。

VBS is gate-driver supply relative to switching source, not absolute gate voltage. UVLO flags a sizing violation without disabling the prescribed gate-charge pulses. No negative-SW overcharge, diode leakage/recovery, startup recharge sequence, high-side common-mode isolation or high-duty operation qualification. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

VBS相对开关源极，非绝对栅压；欠压仅标记选值失败，不关闭规定栅电荷脉冲。不含负SW过充、二极管漏电/恢复、启动充电序列、高侧共模隔离或高占空比认证。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: Exact exponential updates already settle below the stated floor. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：精确指数递推的建立残差已低于给定底限。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P03.gif) · Case / 工况: `P03_100V_25C`

Sources / 来源: S01, S03

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "device_temperature_cases_C": [
    -40,
    25,
    125
  ],
  "all_coefficients": "Authored illustrative assumptions; same parameterized device across all Vin classes, no rated-voltage certification.",
  "Cboot_cases_F": [
    1e-07,
    3.3e-09
  ],
  "driver_supply_V": 10,
  "bootstrap_diode_drop_V": 0.65,
  "recharge_R_ohm": 10,
  "Iq_25_A": 0.0001,
  "Iq_TC_per_K": 0.003,
  "driver_UVLO_V": 6,
  "cycles": 12,
  "fs_Hz": 250000.0
}
```

## P04 Level-shifter common-mode disturbance

## P04 电平移位接收端共模扰动

(Crx+Ccm) dVrx/dt+Vrx/Rrx=Ccm dVcm/dt. Compare weak and stronger receiver discharge paths at the same 10 V/ns edge.

共模电容注入电流经接收端RC产生扰动；在相同10V/ns边沿下比较弱/强泄放路径。

Unclamped linear RC susceptibility only. Receiver excursions beyond a real logic rail signal model invalidity/risk; no receiver clamp or latch transistor network is modeled. This is not a level-shifter implementation, isolation test or CMTI certification. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

仅未钳位线性RC敏感性；超过实际逻辑电源的电压提示模型适用边界/风险，未建模输入钳位或锁存晶体管。不代表完整电平移位电路、隔离测试或CMTI认证。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: The peak is analytic already; this does not validate real logic clamps or CMTI. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：峰值已为解析值；这不验证实际逻辑钳位或CMTI。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P04.gif) · Case / 工况: `P04_100V_25C_strong`

Sources / 来源: S04, S10

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "Ccm_F": 3e-14,
  "Crx_F": 2e-13,
  "receiver_R_cases_ohm": [
    20000,
    500
  ],
  "common_mode_slew_V_per_s": 10000000000.0,
  "threshold_V": 0.7,
  "temperature_C": 25
}
```

## P05 Current-sense amplifier and delayed comparator

## P05 电流检测放大器与延迟比较器

Vsense=Rs I; Vtarget=Gain Vsense+Vos; tau dVamp/dt+Vamp=Vtarget. Comparator output asserts after threshold crossing plus 35 ns propagation delay.

取样电阻电压经有限带宽放大器和确定性失调形成输出；比较器阈值 crossing 后加35ns传播延迟。

Low-voltage ground-referenced sensing bench. No HV input/common-mode rating, amplifier saturation, input clamp, blanking, random noise, metastability, shunt inductance or actual cycle-by-cycle turn-off. Delay is assumed, not a guaranteed device specification. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

低压地参考检测台；无高压共模额定、放大器饱和、输入钳位、消隐、随机噪声、亚稳态、取样寄生电感及实际逐周期关断。延迟为假设，非器件保证值。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: This improves sampled waveform event placement; the analytic trip_time_s metric was already exact. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：改善采样波形的事件定位；原解析trip_time_s指标已精确。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P05.gif) · Case / 工况: `P05_25C`

Sources / 来源: S05, S12

```json
{
  "device_temperature_cases_C": [
    -40,
    25,
    125
  ],
  "Rs_25_ohm": 0.05,
  "Rs_TC_per_K": 0.0001,
  "gain": 20,
  "Vos_25_V": 0.001,
  "Vos_TC_V_per_K": 5e-06,
  "tau_s": 1e-07,
  "comparator_threshold_V": 2,
  "propagation_delay_s": 3.5e-08,
  "step_time_s": 1e-07,
  "current_step_A": [
    0.5,
    3
  ]
}
```

## P06 HV startup supply and hysteretic UVLO

## P06 高压启动供电与迟滞欠压锁定

Caux dVaux/dt=Istart-Iload-Iclamp; current source has a simple compliance limit. Enable at 9 V, disable at 7 V; an 11 V ideal clamp limits Vaux.

辅助电容由限流启动源充电，并供给状态相关负载；9V开启、7V关闭，11V理想钳位限制辅助电压。

Behavioral startup current source, not a JFET transistor model. The source remains on except for an imposed interruption. No real auxiliary winding handover, high-voltage reliability, clamp SOA, leakage, power-on reset timing or guaranteed start-up range. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

启动限流源为行为模型，非JFET晶体管模型；除规定中断外保持开启。不含真实辅助绕组接管、高压可靠性、钳位SOA、漏电、上电复位时序或保证启动范围。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: Event-aligned segments are exact only in the explicitly checked constant-current domain. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：仅在明确检查的恒流工作域内，事件对齐分段解是精确的。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P06.gif) · Case / 工况: `P06_100V_25C`

Sources / 来源: S06, S11

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "device_temperature_cases_C": [
    -40,
    25,
    125
  ],
  "all_coefficients": "Authored illustrative assumptions; same parameterized device across all Vin classes, no rated-voltage certification.",
  "Caux_F": 1e-06,
  "start_current_25_A": 0.001,
  "start_current_TC_per_K": 0.001,
  "compliance_R_ohm": 20000,
  "UVLO_on_V": 9,
  "UVLO_off_V": 7,
  "clamp_V": 11,
  "disabled_load_A": 4e-05,
  "enabled_load_A": 0.0005,
  "source_interruption_s": [
    0.014,
    0.024
  ],
  "dt_s": 2e-06,
  "end_s": 0.04
}
```

## P07 Switch-node parasitic ringing and damping

## P07 开关节点寄生振铃与阻尼

Series RLC free response: C dv/dt=i; L di/dt=-v-Ri. Rcritical=2 sqrt(L/C), not the parallel-RLC critical resistance. E=0.5 Cv^2+0.5 Li^2; dE/dt=-Ri^2.

串联RLC自由响应，临界电阻为2√(L/C)，与并联RLC不同；电场与磁场储能之和按Ri²耗散。

Linearized series-RLC surrogate about a bus voltage, not a literal shunt RC snubber design. Initial disturbance amplitude is prescribed. No switching-edge excitation, EMI prediction, nonlinear Coss or snubber recurring power estimate. Do not copy its Rcritical into a real shunt snubber. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

母线附近线性化串联RLC替代模型，不是实际并联RC吸收器设计；初始扰动人为规定。无开关边沿激励、EMI预测、非线性Coss或吸收器周期功率；不得将临界电阻直接用于真实并联吸收器。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: Energy uses Simpson quadrature on a 4x finer internal grid; saved waveform density and analytical physics are unchanged. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：能量采用加密4倍内部网格上的Simpson积分；保存波形密度与解析物理不变。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P07.gif) · Case / 工况: `P07_100V_damped`

Sources / 来源: S07

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "Lpar_H": 1.5e-08,
  "Clinearization": "P01 Coss evaluated at Vin",
  "Rweak_ohm": 0.8,
  "Rdamped_fraction_of_series_critical": 0.8,
  "initial_ring_amplitude_fraction_of_Vin": 0.15,
  "initial_current_A": 0,
  "temperature_C": 25
}
```

## P08 DC/DC separated losses and thermal budget

## P08 DC/DC分项损耗与热预算

Matched Coss hard-turn-on energy: Eupper+(Vin Qlower-Elower)=Vin Qoss. Ploss=HS/LS conduction+L copper+channel overlap+Vin Qoss fs+Vin Qrr fs+two Qg Vdrive fs+dead-time diode+control. Solve Thot=Tamb+Rtheta Ploss(Thot). Fixed-loss transient: Thot(t)=Tamb+Ploss Rtheta (1-exp(-t/Rtheta Ctheta)).

两管相同Coss：高侧放电储能加低侧充电耗散为Eupper+(VinQlower-Elower)=VinQoss；计一次硬导通/周期，另加导通、铜损、沟道交叠、恢复母线估算、两管栅驱、死区和控制损耗；求等效热节点反馈不动点，再计算恒损耗热瞬态。

A ledger, not one self-consistent switched electrical/thermal simulation. Two matched Coss curves, one hard upper turn-on per cycle, opposite edge ideal energy redistribution; Coss subterm energies are explanatory and only their sum enters the loss ledger. Overlap includes load-channel current only; Qrr is separate, with no reused full Eon. Vin Qrr is conservative full-bus energy, not diode heat. All heat shares one effective node, not a MOS junction; the thermal transient holds converged loss constant. No core/ESR/reliability/layout loss or measured efficiency. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

此为预算表，非完整自洽开关电热仿真；两管Coss相同，每周期一次高侧硬导通，另一边沿假定理想能量再分配；Coss子项能量用于解释，仅其和计入损耗。交叠仅含负载沟道电流，Qrr单列，不重复使用完整Eon。VinQrr为全母线保守能量，非二极管热；所有热量共用一个等效节点，非MOS结温，热瞬态固定收敛损耗。不含磁芯、ESR、可靠性、版图损耗或实测效率。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: No new physical loss term or altered Coss/Qrr accounting. The common thermal node is not a MOS junction. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：未新增物理损耗或改变Coss/Qrr核算；共用热节点不是MOS结温。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P08.gif) · Case / 工况: `P08_100V_25C`

Sources / 来源: S01, S02, S08

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "ambient_temperature_cases_C": [
    -40,
    25,
    125
  ],
  "fs_Hz": 250000.0,
  "Vout_V": 12,
  "Iout_A": 1,
  "RL_25_ohm": 0.12,
  "Rtheta_K_per_W": 8,
  "Ctheta_J_per_K": 0.025,
  "control_loss_W": 0.01,
  "assumed_coefficient_temperature_range_C": [
    -40,
    175
  ],
  "hard_Coss_commutations_per_cycle": 1,
  "gate_charge_events_per_cycle": 2
}
```

## P09 Averaged buck soft-start and current-reference limit

## P09 平均Buck软启动与电流参考限幅

L di/dt=D Vin-R i-v; C dv/dt=i-v/Rload. PI voltage loop commands a finite-bandwidth current loop. Reference ramps to 12 V in 2 ms; current command clips at 1.6 A with conditional-integration anti-windup.

平均功率级由电压PI环和有限带宽电流环控制；2ms参考斜坡、1.6A电流指令上限及条件积分抗饱和。

Continuous averaged duty, not PWM edges. A current-reference ceiling is not cycle-by-cycle peak protection; high-frequency overshoot, blanking and inductor saturation are absent. P08 switching losses are not inserted into this plant. Saved traces are decimated; energy metrics use every integration step. No sampled-cycle, slope-compensation, subharmonic or hardware-stability prediction. Numerical refinement reduces selected discretization errors, not unknown physical modeling error.

连续平均占空比，非PWM边沿；电流参考上限不是逐周期峰值保护，无高频过冲、消隐与电感饱和。未将P08开关损耗注入功率级；显示曲线抽取，能量指标使用全部积分步。不预测采样周期、斜坡补偿、次谐波或硬件稳定性。 数值改进降低指定离散误差，不代表未知物理建模误差降低。

Numerical scope: Reference uncertainty is the max difference from a 10x looser tolerance, an empirical convergence estimate, not a rigorous bound. New RK4 uses 0.5us steps and stage-time ramp evaluation; saved traces remain 10us. Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.

数值范围：参考不确定度为容差放宽10倍的最大差异，是经验收敛估计而非严格上界。新版RK4采用0.5µs步长并在子步时刻计算斜坡；保存间隔仍为10µs。 沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。

[GIF](../v33/education/gifs/P09.gif) · Case / 工况: `P09_100V_25C`

Sources / 来源: S06, S09

```json
{
  "input_classes_V": [
    40,
    60,
    80,
    100,
    120,
    150
  ],
  "device_temperature_cases_C": [
    -40,
    25,
    125
  ],
  "all_coefficients": "Authored illustrative assumptions; same parameterized device across all Vin classes, no rated-voltage certification.",
  "L_H": 0.0001,
  "C_F": 2.2e-05,
  "total_R_25_ohm": 0.3,
  "voltage_Kp_A_per_V": 0.25,
  "voltage_Ki_A_per_V_s": 350,
  "current_loop_bandwidth_Hz": 12000,
  "current_reference_limit_A": 1.6,
  "max_duty": 0.9,
  "softstart_s": 0.002,
  "load_step_s": 0.004,
  "Rload_before_ohm": 12,
  "Rload_after_ohm": 6,
  "dt_s": 5e-07,
  "end_s": 0.008,
  "saved_stride_steps": 20
}
```
