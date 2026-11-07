# V3.2 DC/DC model cards

# V3.2 DC/DC模型卡

All numerical coefficients are authored illustrative assumptions. See source IDs in [the evidence audit](SOURCES_AND_GAPS.md). No paper reproduction or PDK calibration.

全部数值系数为人为示意假设。来源编号见[依据审计](SOURCES_AND_GAPS.md)；未复现论文或校准PDK。

## P01 — HV MOS gate charge and switching overlap

## P01 — 高压MOS栅电荷与开关交叠

Cgd(v)=80pF/(1+v/20V)^0.5; Qgd=integral Cgd dv; plateau gate current=(Vdrive-Vplateau)/Rg; Vds is the inverse charge law. Eoverlap=integral max(Vds Ichannel-Ron Ichannel^2,0)dt. Qoss=integral Coss dv; Eoss=integral v Coss dv.

Miller电荷由非线性Cgd积分，平台电流决定漏压转换时间；交叠损耗积分扣除瞬时导通基线；Qoss与Eoss分别积分Coss和vCoss。

**Limits / 限制:** Prescribed staged commutation, not a coupled charge-conserving MOS compact model. Ichannel excludes Coss displacement and diode recovery. Fixed-C Miller appeared in V2 X01; this bench adds nonlinear charge, separate overlap/storage energies and temperature sweeps. No breakdown, avalanche, SOA, gate overshoot or layout extraction.

人为规定阶段的换流模型，非完整电荷守恒MOS紧凑模型；沟道电流不含Coss位移和二极管恢复。V2 X01已有固定电容Miller，本版增强非线性电荷、分离交叠/储能及温度扫描；不含击穿、雪崩、SOA、栅过冲或版图提取。

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

## P02 — Dead-time diode and reverse recovery

## P02 — 死区二极管与反向恢复

D=(Vout+2 td fs Vf)/Vin; L dIL/dt=Vsw-Vout in HS/dead/LS/dead phases. Qrr=0.5 Ipk trr. Ecomm=Vin Qrr is a separate prescribed bus-energy estimate.

按死区压降补偿占空比，四阶段积分电感电流；三角恢复电流满足Qrr=Ipk trr/2，另列VinQrr换流能量估算。

**Limits / 限制:** Periodic ideal CCM waveform; recovery pulse is separate from IL and Vsw. Vin Qrr assumes full bus voltage and is not measured diode heat. No stored-charge transport solution, Coss commutation, gate overlap or ringing. V2 X02 already imposed triangular recovery; V3.2 relates it to dead-time sizing and bus-energy accounting.

周期理想CCM波形；恢复脉冲与IL、Vsw分别计算。VinQrr假定全母线电压，不等同实测二极管热。无载流子输运、Coss换流、栅交叠或振铃。V2 X02已有三角恢复，本版关联死区选取和母线能量核算。

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

## P03 — Floating bootstrap supply and UVLO margin

## P03 — 浮地自举供电与欠压裕量

Gate event: deltaVbs=-Qg/Cboot. On: dVbs/dt=-Iq/Cboot. Off: Cboot dVbs/dt=(Vsource-Vbs)/Rcharge-Iq. Exact exponential recharge and analytical periodic map.

栅极事件消耗Qg使VBS下降，导通期间静态电流放电，关断期间经充电电阻指数恢复；解析周期映射计算最小电压。

**Limits / 限制:** VBS is gate-driver supply relative to switching source, not absolute gate voltage. UVLO flags a sizing violation without disabling the prescribed gate-charge pulses. No negative-SW overcharge, diode leakage/recovery, startup recharge sequence, high-side common-mode isolation or high-duty operation qualification.

VBS相对开关源极，非绝对栅压；欠压仅标记选值失败，不关闭规定栅电荷脉冲。不含负SW过充、二极管漏电/恢复、启动充电序列、高侧共模隔离或高占空比认证。

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

## P04 — Level-shifter common-mode disturbance

## P04 — 电平移位接收端共模扰动

(Crx+Ccm) dVrx/dt+Vrx/Rrx=Ccm dVcm/dt. Compare weak and stronger receiver discharge paths at the same 10 V/ns edge.

共模电容注入电流经接收端RC产生扰动；在相同10V/ns边沿下比较弱/强泄放路径。

**Limits / 限制:** Unclamped linear RC susceptibility only. Receiver excursions beyond a real logic rail signal model invalidity/risk; no receiver clamp or latch transistor network is modeled. This is not a level-shifter implementation, isolation test or CMTI certification.

仅未钳位线性RC敏感性；超过实际逻辑电源的电压提示模型适用边界/风险，未建模输入钳位或锁存晶体管。不代表完整电平移位电路、隔离测试或CMTI认证。

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

## P05 — Current-sense amplifier and delayed comparator

## P05 — 电流检测放大器与延迟比较器

Vsense=Rs I; Vtarget=Gain Vsense+Vos; tau dVamp/dt+Vamp=Vtarget. Comparator output asserts after threshold crossing plus 35 ns propagation delay.

取样电阻电压经有限带宽放大器和确定性失调形成输出；比较器阈值 crossing 后加35ns传播延迟。

**Limits / 限制:** Low-voltage ground-referenced sensing bench. No HV input/common-mode rating, amplifier saturation, input clamp, blanking, random noise, metastability, shunt inductance or actual cycle-by-cycle turn-off. Delay is assumed, not a guaranteed device specification.

低压地参考检测台；无高压共模额定、放大器饱和、输入钳位、消隐、随机噪声、亚稳态、取样寄生电感及实际逐周期关断。延迟为假设，非器件保证值。

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

## P06 — HV startup supply and hysteretic UVLO

## P06 — 高压启动供电与迟滞欠压锁定

Caux dVaux/dt=Istart-Iload-Iclamp; current source has a simple compliance limit. Enable at 9 V, disable at 7 V; an 11 V ideal clamp limits Vaux.

辅助电容由限流启动源充电，并供给状态相关负载；9V开启、7V关闭，11V理想钳位限制辅助电压。

**Limits / 限制:** Behavioral startup current source, not a JFET transistor model. The source remains on except for an imposed interruption. No real auxiliary winding handover, high-voltage reliability, clamp SOA, leakage, power-on reset timing or guaranteed start-up range.

启动限流源为行为模型，非JFET晶体管模型；除规定中断外保持开启。不含真实辅助绕组接管、高压可靠性、钳位SOA、漏电、上电复位时序或保证启动范围。

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

## P07 — Switch-node parasitic ringing and damping

## P07 — 开关节点寄生振铃与阻尼

Series RLC free response: C dv/dt=i; L di/dt=-v-Ri. Rcritical=2 sqrt(L/C), not the parallel-RLC critical resistance. E=0.5 Cv^2+0.5 Li^2; dE/dt=-Ri^2.

串联RLC自由响应，临界电阻为2√(L/C)，与并联RLC不同；电场与磁场储能之和按Ri²耗散。

**Limits / 限制:** Linearized series-RLC surrogate about a bus voltage, not a literal shunt RC snubber design. Initial disturbance amplitude is prescribed. No switching-edge excitation, EMI prediction, nonlinear Coss or snubber recurring power estimate. Do not copy its Rcritical into a real shunt snubber.

母线附近线性化串联RLC替代模型，不是实际并联RC吸收器设计；初始扰动人为规定。无开关边沿激励、EMI预测、非线性Coss或吸收器周期功率；不得将临界电阻直接用于真实并联吸收器。

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

## P08 — DC/DC separated losses and thermal budget

## P08 — DC/DC分项损耗与热预算

Matched Coss hard-turn-on energy: Eupper+(Vin Qlower-Elower)=Vin Qoss. Ploss=HS/LS conduction+L copper+channel overlap+Vin Qoss fs+Vin Qrr fs+two Qg Vdrive fs+dead-time diode+control. Solve Thot=Tamb+Rtheta Ploss(Thot). Fixed-loss transient: Thot(t)=Tamb+Ploss Rtheta (1-exp(-t/Rtheta Ctheta)).

两管相同Coss：高侧放电储能加低侧充电耗散为Eupper+(VinQlower-Elower)=VinQoss；计一次硬导通/周期，另加导通、铜损、沟道交叠、恢复母线估算、两管栅驱、死区和控制损耗；求等效热节点反馈不动点，再计算恒损耗热瞬态。

**Limits / 限制:** A ledger, not one self-consistent switched electrical/thermal simulation. Two matched Coss curves, one hard upper turn-on per cycle, opposite edge ideal energy redistribution; Coss subterm energies are explanatory and only their sum enters the loss ledger. Overlap includes load-channel current only; Qrr is separate, with no reused full Eon. Vin Qrr is conservative full-bus energy, not diode heat. All heat shares one effective node, not a MOS junction; the thermal transient holds converged loss constant. No core/ESR/reliability/layout loss or measured efficiency.

此为预算表，非完整自洽开关电热仿真；两管Coss相同，每周期一次高侧硬导通，另一边沿假定理想能量再分配；Coss子项能量用于解释，仅其和计入损耗。交叠仅含负载沟道电流，Qrr单列，不重复使用完整Eon。VinQrr为全母线保守能量，非二极管热；所有热量共用一个等效节点，非MOS结温，热瞬态固定收敛损耗。不含磁芯、ESR、可靠性、版图损耗或实测效率。

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

## P09 — Averaged buck soft-start and current-reference limit

## P09 — 平均Buck软启动与电流参考限幅

L di/dt=D Vin-R i-v; C dv/dt=i-v/Rload. PI voltage loop commands a finite-bandwidth current loop. Reference ramps to 12 V in 2 ms; current command clips at 1.6 A with conditional-integration anti-windup.

平均功率级由电压PI环和有限带宽电流环控制；2ms参考斜坡、1.6A电流指令上限及条件积分抗饱和。

**Limits / 限制:** Continuous averaged duty, not PWM edges. A current-reference ceiling is not cycle-by-cycle peak protection; high-frequency overshoot, blanking and inductor saturation are absent. P08 switching losses are not inserted into this plant. Saved traces are decimated; energy metrics use every integration step. No sampled-cycle, slope-compensation, subharmonic or hardware-stability prediction.

连续平均占空比，非PWM边沿；电流参考上限不是逐周期峰值保护，无高频过冲、消隐与电感饱和。未将P08开关损耗注入功率级；显示曲线抽取，能量指标使用全部积分步。不预测采样周期、斜坡补偿、次谐波或硬件稳定性。

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
  "dt_s": 1e-06,
  "end_s": 0.008,
  "saved_stride_steps": 10
}
```
