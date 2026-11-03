"""Export V3.2 extension cases. NumPy and Python standard library only."""
from pathlib import Path
import json,csv,platform
import numpy as np
from improved import *

ROOT=Path(__file__).resolve().parent;OUT=ROOT

def catalog():
    common={'input_classes_V':list(VINS),'device_temperature_cases_C':list(TEMPS),'all_coefficients':'Authored illustrative assumptions; same parameterized device across all Vin classes, no rated-voltage certification.'}
    rows=[
    ('P01','HV MOS gate charge and switching overlap','高压MOS栅电荷与开关交叠','device_extension','S01 S02 S10',
     'Cgd(v)=80pF/(1+v/20V)^0.5; Qgd=integral Cgd dv; plateau gate current=(Vdrive-Vplateau)/Rg; Vds is the inverse charge law. Eoverlap=integral max(Vds Ichannel-Ron Ichannel^2,0)dt. Qoss=integral Coss dv; Eoss=integral v Coss dv.',
     'Miller电荷由非线性Cgd积分，平台电流决定漏压转换时间；交叠损耗积分扣除瞬时导通基线；Qoss与Eoss分别积分Coss和vCoss。',
     dict(common,Vdrive_V=10,Cgs_F=800e-12,Cgd0_F=80e-12,Coss_per_device_C0_F=600e-12,capacitance_V0_V=20,capacitance_exponent=.5,Rg_on_ohm=8,Rg_off_ohm=5,gm_S=.5,Iload_A=1,Vth_25_V=2.2,Vth_TC_V_per_K=-.002,Ron_25_ohm=.18,Ron_TC_per_K=.004),
     'Prescribed staged commutation, not a coupled charge-conserving MOS compact model. Ichannel excludes Coss displacement and diode recovery. Fixed-C Miller appeared in V2 X01; this bench adds nonlinear charge, separate overlap/storage energies and temperature sweeps. No breakdown, avalanche, SOA, gate overshoot or layout extraction.',
     '人为规定阶段的换流模型，非完整电荷守恒MOS紧凑模型；沟道电流不含Coss位移和二极管恢复。V2 X01已有固定电容Miller，本版增强非线性电荷、分离交叠/储能及温度扫描；不含击穿、雪崩、SOA、栅过冲或版图提取。'),
    ('P02','Dead-time diode and reverse recovery','死区二极管与反向恢复','device_extension','S02',
     'D=(Vout+2 td fs Vf)/Vin; L dIL/dt=Vsw-Vout in HS/dead/LS/dead phases. Qrr=0.5 Ipk trr. Ecomm=Vin Qrr is a separate prescribed bus-energy estimate.',
     '按死区压降补偿占空比，四阶段积分电感电流；三角恢复电流满足Qrr=Ipk trr/2，另列VinQrr换流能量估算。',
     dict(common,Vout_V=12,Iout_A=1,L_H=100e-6,fs_Hz=FS,deadtime_each_s=40e-9,Vf_25_V=.8,Vf_TC_V_per_K=-.001,Qrr_25_C=12e-9,Qrr_TC_per_K=.005,trr_25_s=60e-9,trr_TC_per_K=.002,recovery_rise_fraction=.35),
     'Periodic ideal CCM waveform; recovery pulse is separate from IL and Vsw. Vin Qrr assumes full bus voltage and is not measured diode heat. No stored-charge transport solution, Coss commutation, gate overlap or ringing. V2 X02 already imposed triangular recovery; V3.2 relates it to dead-time sizing and bus-energy accounting.',
     '周期理想CCM波形；恢复脉冲与IL、Vsw分别计算。VinQrr假定全母线电压，不等同实测二极管热。无载流子输运、Coss换流、栅交叠或振铃。V2 X02已有三角恢复，本版关联死区选取和母线能量核算。'),
    ('P03','Floating bootstrap supply and UVLO margin','浮地自举供电与欠压裕量','circuit_benchmark','S01 S03',
     'Gate event: deltaVbs=-Qg/Cboot. On: dVbs/dt=-Iq/Cboot. Off: Cboot dVbs/dt=(Vsource-Vbs)/Rcharge-Iq. Exact exponential recharge and analytical periodic map.',
     '栅极事件消耗Qg使VBS下降，导通期间静态电流放电，关断期间经充电电阻指数恢复；解析周期映射计算最小电压。',
     dict(common,Cboot_cases_F=[100e-9,3.3e-9],driver_supply_V=10,bootstrap_diode_drop_V=.65,recharge_R_ohm=10,Iq_25_A=100e-6,Iq_TC_per_K=.003,driver_UVLO_V=6,cycles=12,fs_Hz=FS),
     'VBS is gate-driver supply relative to switching source, not absolute gate voltage. UVLO flags a sizing violation without disabling the prescribed gate-charge pulses. No negative-SW overcharge, diode leakage/recovery, startup recharge sequence, high-side common-mode isolation or high-duty operation qualification.',
     'VBS相对开关源极，非绝对栅压；欠压仅标记选值失败，不关闭规定栅电荷脉冲。不含负SW过充、二极管漏电/恢复、启动充电序列、高侧共模隔离或高占空比认证。'),
    ('P04','Level-shifter common-mode disturbance','电平移位接收端共模扰动','circuit_benchmark','S04 S10',
     '(Crx+Ccm) dVrx/dt+Vrx/Rrx=Ccm dVcm/dt. Compare weak and stronger receiver discharge paths at the same 10 V/ns edge.',
     '共模电容注入电流经接收端RC产生扰动；在相同10V/ns边沿下比较弱/强泄放路径。',
     dict(input_classes_V=list(VINS),Ccm_F=30e-15,Crx_F=200e-15,receiver_R_cases_ohm=[20000,500],common_mode_slew_V_per_s=10e9,threshold_V=.7,temperature_C=25),
     'Unclamped linear RC susceptibility only. Receiver excursions beyond a real logic rail signal model invalidity/risk; no receiver clamp or latch transistor network is modeled. This is not a level-shifter implementation, isolation test or CMTI certification.',
     '仅未钳位线性RC敏感性；超过实际逻辑电源的电压提示模型适用边界/风险，未建模输入钳位或锁存晶体管。不代表完整电平移位电路、隔离测试或CMTI认证。'),
    ('P05','Current-sense amplifier and delayed comparator','电流检测放大器与延迟比较器','circuit_benchmark','S05 S12',
     'Vsense=Rs I; Vtarget=Gain Vsense+Vos; tau dVamp/dt+Vamp=Vtarget. Comparator output asserts after threshold crossing plus 35 ns propagation delay.',
     '取样电阻电压经有限带宽放大器和确定性失调形成输出；比较器阈值 crossing 后加35ns传播延迟。',
     dict(device_temperature_cases_C=list(TEMPS),Rs_25_ohm=.05,Rs_TC_per_K=100e-6,gain=20,Vos_25_V=.001,Vos_TC_V_per_K=5e-6,tau_s=100e-9,comparator_threshold_V=2,propagation_delay_s=35e-9,step_time_s=100e-9,current_step_A=[.5,3]),
     'Low-voltage ground-referenced sensing bench. No HV input/common-mode rating, amplifier saturation, input clamp, blanking, random noise, metastability, shunt inductance or actual cycle-by-cycle turn-off. Delay is assumed, not a guaranteed device specification.',
     '低压地参考检测台；无高压共模额定、放大器饱和、输入钳位、消隐、随机噪声、亚稳态、取样寄生电感及实际逐周期关断。延迟为假设，非器件保证值。'),
    ('P06','HV startup supply and hysteretic UVLO','高压启动供电与迟滞欠压锁定','circuit_benchmark','S06 S11',
     'Caux dVaux/dt=Istart-Iload-Iclamp; current source has a simple compliance limit. Enable at 9 V, disable at 7 V; an 11 V ideal clamp limits Vaux.',
     '辅助电容由限流启动源充电，并供给状态相关负载；9V开启、7V关闭，11V理想钳位限制辅助电压。',
     dict(common,Caux_F=1e-6,start_current_25_A=.001,start_current_TC_per_K=.001,compliance_R_ohm=20000,UVLO_on_V=9,UVLO_off_V=7,clamp_V=11,disabled_load_A=40e-6,enabled_load_A=500e-6,source_interruption_s=[.014,.024],dt_s=2e-6,end_s=.040),
     'Behavioral startup current source, not a JFET transistor model. The source remains on except for an imposed interruption. No real auxiliary winding handover, high-voltage reliability, clamp SOA, leakage, power-on reset timing or guaranteed start-up range.',
     '启动限流源为行为模型，非JFET晶体管模型；除规定中断外保持开启。不含真实辅助绕组接管、高压可靠性、钳位SOA、漏电、上电复位时序或保证启动范围。'),
    ('P07','Switch-node parasitic ringing and damping','开关节点寄生振铃与阻尼','circuit_benchmark','S07',
     'Series RLC free response: C dv/dt=i; L di/dt=-v-Ri. Rcritical=2 sqrt(L/C), not the parallel-RLC critical resistance. E=0.5 Cv^2+0.5 Li^2; dE/dt=-Ri^2.',
     '串联RLC自由响应，临界电阻为2√(L/C)，与并联RLC不同；电场与磁场储能之和按Ri²耗散。',
     dict(input_classes_V=list(VINS),Lpar_H=15e-9,Clinearization='P01 Coss evaluated at Vin',Rweak_ohm=.8,Rdamped_fraction_of_series_critical=.8,initial_ring_amplitude_fraction_of_Vin=.15,initial_current_A=0,temperature_C=25),
     'Linearized series-RLC surrogate about a bus voltage, not a literal shunt RC snubber design. Initial disturbance amplitude is prescribed. No switching-edge excitation, EMI prediction, nonlinear Coss or snubber recurring power estimate. Do not copy its Rcritical into a real shunt snubber.',
     '母线附近线性化串联RLC替代模型，不是实际并联RC吸收器设计；初始扰动人为规定。无开关边沿激励、EMI预测、非线性Coss或吸收器周期功率；不得将临界电阻直接用于真实并联吸收器。'),
    ('P08','DC/DC separated losses and thermal budget','DC/DC分项损耗与热预算','circuit_benchmark','S01 S02 S08',
     'Matched Coss hard-turn-on energy: Eupper+(Vin Qlower-Elower)=Vin Qoss. Ploss=HS/LS conduction+L copper+channel overlap+Vin Qoss fs+Vin Qrr fs+two Qg Vdrive fs+dead-time diode+control. Solve Thot=Tamb+Rtheta Ploss(Thot). Fixed-loss transient: Thot(t)=Tamb+Ploss Rtheta (1-exp(-t/Rtheta Ctheta)).',
     '两管相同Coss：高侧放电储能加低侧充电耗散为Eupper+(VinQlower-Elower)=VinQoss；计一次硬导通/周期，另加导通、铜损、沟道交叠、恢复母线估算、两管栅驱、死区和控制损耗；求等效热节点反馈不动点，再计算恒损耗热瞬态。',
     dict(input_classes_V=list(VINS),ambient_temperature_cases_C=list(TEMPS),fs_Hz=FS,Vout_V=12,Iout_A=1,RL_25_ohm=.12,Rtheta_K_per_W=8,Ctheta_J_per_K=.025,control_loss_W=.01,assumed_coefficient_temperature_range_C=[-40,175],hard_Coss_commutations_per_cycle=1,gate_charge_events_per_cycle=2),
     'A ledger, not one self-consistent switched electrical/thermal simulation. Two matched Coss curves, one hard upper turn-on per cycle, opposite edge ideal energy redistribution; Coss subterm energies are explanatory and only their sum enters the loss ledger. Overlap includes load-channel current only; Qrr is separate, with no reused full Eon. Vin Qrr is conservative full-bus energy, not diode heat. All heat shares one effective node, not a MOS junction; the thermal transient holds converged loss constant. No core/ESR/reliability/layout loss or measured efficiency.',
     '此为预算表，非完整自洽开关电热仿真；两管Coss相同，每周期一次高侧硬导通，另一边沿假定理想能量再分配；Coss子项能量用于解释，仅其和计入损耗。交叠仅含负载沟道电流，Qrr单列，不重复使用完整Eon。VinQrr为全母线保守能量，非二极管热；所有热量共用一个等效节点，非MOS结温，热瞬态固定收敛损耗。不含磁芯、ESR、可靠性、版图损耗或实测效率。'),
    ('P09','Averaged buck soft-start and current-reference limit','平均Buck软启动与电流参考限幅','circuit_benchmark','S06 S09',
     'L di/dt=D Vin-R i-v; C dv/dt=i-v/Rload. PI voltage loop commands a finite-bandwidth current loop. Reference ramps to 12 V in 2 ms; current command clips at 1.6 A with conditional-integration anti-windup.',
     '平均功率级由电压PI环和有限带宽电流环控制；2ms参考斜坡、1.6A电流指令上限及条件积分抗饱和。',
     dict(common,L_H=100e-6,C_F=22e-6,total_R_25_ohm=.30,voltage_Kp_A_per_V=.25,voltage_Ki_A_per_V_s=350,current_loop_bandwidth_Hz=12000,current_reference_limit_A=1.6,max_duty=.90,softstart_s=.002,load_step_s=.004,Rload_before_ohm=12,Rload_after_ohm=6,dt_s=1e-6,end_s=.008,saved_stride_steps=10),
     'Continuous averaged duty, not PWM edges. A current-reference ceiling is not cycle-by-cycle peak protection; high-frequency overshoot, blanking and inductor saturation are absent. P08 switching losses are not inserted into this plant. Saved traces are decimated; energy metrics use every integration step. No sampled-cycle, slope-compensation, subharmonic or hardware-stability prediction.',
     '连续平均占空比，非PWM边沿；电流参考上限不是逐周期峰值保护，无高频过冲、消隐与电感饱和。未将P08开关损耗注入功率级；显示曲线抽取，能量指标使用全部积分步。不预测采样周期、斜坡补偿、次谐波或硬件稳定性。')]
    return [dict(id=i,name_en=en,name_zh=zh,kind=kind,source_ids=src.split(),equation_en=eq,equation_zh=eqzh,parameters=par,limits_en=lim,limits_zh=limzh,geometry='dcdc_block',parameter_origin_en='Authored illustrative coefficients; no paper parameter extraction or foundry calibration.',parameter_origin_zh='系数为人为示意假设；未提取论文参数或校准晶圆厂数据。')for i,en,zh,kind,src,eq,eqzh,par,lim,limzh in rows]

def signal(name,unit,y):return dict(name=name,unit=unit,y=np.asarray(y,dtype=float).tolist())
def plot(en,zh,x,signals,xlabel='Time (s)'):return dict(title_en=en,title_zh=zh,x=np.asarray(x,dtype=float).tolist(),xlabel=xlabel,series=signals,xlog=False)

def main():
    OUT.mkdir(exist_ok=True);(OUT/'csv').mkdir(exist_ok=True);models=catalog();cases=[]
    def add(mid,tag,x,sigs,metrics,temp=25,vin=None,plots=None,notes=''):
        cases.append(dict(id=mid+'_'+tag,model_id=mid,temp_C=temp,vin_V=vin,x=np.asarray(x,dtype=float).tolist(),xlabel='Time / 时间 (s)',signals=sigs,terminals=[],port_power_W=None,plots=plots or[plot(models[int(mid[1:])-1]['name_en'],models[int(mid[1:])-1]['name_zh'],x,sigs[:1])],metrics=metrics,notes_en=notes))
    for vin in VINS:
        for temp in TEMPS:
            tag=f'{vin}V_{temp}C'
            d=gate_switch(vin,temp);x=d['t_on'];s=[signal('Vgs on / 导通栅源电压','V',d['vg_on']),signal('Vds on / 导通漏源电压','V',d['vd_on']),signal('Ichannel on / 导通沟道电流','A',d['id_on']),signal('Igate on / 导通栅电流','A',d['ig_on']),signal('Overlap power / 交叠功率','W',d['p_on'])]
            v=np.linspace(0,vin,301)
            add('P01',tag,x,s,d['metrics'],temp,vin,[plot('Turn-on gate and drain voltages','导通栅漏电压',x,s[:2]),plot('Turn-on channel and gate currents','导通沟道与栅电流',x,s[2:4]),plot('Turn-on overlap power','导通交叠功率',x,s[4:]),plot('Turn-off voltages','关断电压',d['t_off'],[signal('Vgs / 栅源电压','V',d['vg_off']),signal('Vds / 漏源电压','V',d['vd_off'])]),plot('Turn-off channel and gate currents','关断沟道与栅电流',d['t_off'],[signal('Ichannel / 沟道电流','A',d['id_off']),signal('Igate / 栅电流','A',d['ig_off'])]),plot('Turn-off overlap power','关断交叠功率',d['t_off'],[signal('Overlap power / 交叠功率','W',d['p_off'])]),plot('Nonlinear output capacitance','非线性输出电容',v,[signal('Coss','F',capacitance(v))],'Reverse voltage (V)'),plot('Stored output energy','输出储能',v,[signal('Eoss','J',capacitor_energy(v))],'Reverse voltage (V)')])
            d=deadtime_buck(vin,temp);q=recovery_pulse(vin,temp);x=d['t_s'];s=[signal('Vsw / 开关节点','V',d['Vsw_V']),signal('IL / 电感电流','A',d['IL_A']),signal('Diode forward current / 二极管正向电流','A',d['Idiode_forward_A']),signal('HS state / 高侧状态','1',d['state_HS_on']),signal('LS state / 低侧状态','1',d['state_LS_on']),signal('Dead time / 死区','1',d['state_deadtime']),signal('Diode loss / 二极管损耗','W',d['Pdiode_W'])]
            metrics=dict(d['metrics'],Qrr_C=q['qrr'],peak_recovery_A=q['peak'],recovery_time_s=q['trr'],recovery_bus_energy_estimate_J=q['commutation_estimate_J'])
            add('P02',tag,x,s,metrics,temp,vin,[plot('Switch-node voltage','开关节点电压',x,s[:1]),plot('Inductor and forward diode current','电感与正向二极管电流',x,s[1:3]),plot('Gate states and dead time','栅状态与死区',x,s[3:6]),plot('Dead-time diode dissipation','死区二极管耗散',x,s[6:]),plot('Separate recovery pulse','单独恢复脉冲',q['t'],[signal('Reverse current magnitude / 反向电流幅值','A',q['irr'])])])
            for cb,label in [(100e-9,''),(3.3e-9,'_small_cap')]:
                d=bootstrap(vin,temp,cboot=cb);x=d['t'];s=[signal('VBS / 自举电压','V',d['vbs']),signal('Recharge current / 充电电流','A',d['icharge']),signal('Driver quiescent current / 驱动静态电流','A',d['idriver']),signal('UVLO flag / 欠压标记','1',d['uvlo'])]
                add('P03',tag+label,x,s,d['metrics'],temp,vin,[plot('Bootstrap voltage','自举电压',x,s[:1]),plot('Recharge and quiescent currents','充电与静态电流',x,s[1:3]),plot('UVLO sizing flag','欠压选值标记',x,s[3:])],notes='Gate charge is an impulse; zero instantaneous gate current in sampled arrays does not mean zero gate-charge consumption. See Qgate_C.')
            d=startup_uvlo(vin,temp);sel=np.unique(np.r_[np.arange(0,len(d['t']),20),d['event_indices'],len(d['t'])-1]);x=d['t'][sel];s=[signal('Vaux / 辅助电压','V',d['vaux'][sel]),signal('Enable / 使能','1',d['enabled'][sel]),signal('Startup current / 启动电流','A',d['isource'][sel]),signal('Auxiliary load / 辅助负载电流','A',d['iload'][sel]),signal('Clamp current / 钳位电流','A',d['iclamp'][sel]),signal('HV source dissipation / 高压启动源耗散','W',d['source_loss'][sel])]
            add('P06',tag,x,s,d['metrics'],temp,vin,[plot('Auxiliary supply voltage','辅助供电电压',x,s[:1]),plot('UVLO enable state','欠压锁定使能状态',x,s[1:2]),plot('Startup, load and clamp current','启动、负载与钳位电流',x,s[2:5]),plot('Startup-source dissipation','启动源耗散',x,s[5:])],notes='Exact event-aligned UVLO segments; a 2us display grid is decimated by 20, with event samples retained.')
            d=loss_budget(vin,temp);x=d['t'];s=[signal('Effective hot node / 等效热节点','degC',d['temperature'])];metrics=dict(d['metrics'],**d['parts']);loss_names=list(d['parts']);loss_values=list(d['parts'].values())
            add('P08',tag,x,s,metrics,temp,vin,[plot('Constant-loss thermal response','恒损耗热响应',x,s),plot('Separated loss components','分项损耗',np.arange(len(loss_names)),[signal('Loss / 损耗','W',loss_values)],'Component index (see metrics)')],notes='temp_C is AMBIENT here; steady_hot_node_C is an effective shared thermal node, not a semiconductor junction. Component plot indices follow metric order from high_side_conduction_W through assumed_control_supply_W.')
            cases[-1]['loss_components_W']=d['parts']
            d=controlled_buck(vin,temp);x=d['t'];s=[signal('Vout / 输出电压','V',d['voltage']),signal('Vreference / 参考电压','V',d['reference']),signal('IL / 电感电流','A',d['current']),signal('Icommand / 电流指令','A',d['current_reference']),signal('Iload / 负载电流','A',d['load_current']),signal('Iin averaged / 平均输入电流','A',d['input_power']/vin),signal('Duty / 占空比','1',d['duty']),signal('Input power / 输入功率','W',d['input_power']),signal('Output power / 输出功率','W',d['output_power']),signal('Conduction loss / 导通损耗','W',d['conduction_loss'])]
            add('P09',tag,x,s,d['metrics'],temp,vin,[plot('Soft-start and overload response','软启动与过载响应',x,s[:2]),plot('Current flow and reference limit','电流与参考限幅',x,s[2:6]),plot('Averaged duty','平均占空比',x,s[6:7]),plot('Averaged power flow','平均功率流',x,s[7:])])
        for r,label in [(20000,'weak'),(500,'strong')]:
            d=level_shift(vin,receiver_r=r);x=d['t'];s=[signal('Common mode / 共模电压','V',d['cm']),signal('Receiver disturbance / 接收端扰动','V',d['rx']),signal('Injected current / 注入电流','A',d['iinj']),signal('Receiver discharge / 接收端泄放','A',d['ir'])]
            add('P04',f'{vin}V_25C_{label}',x,s,d['metrics'],25,vin,[plot('Receiver disturbance','接收端扰动',x,s[1:2]),plot('Common-mode edge','共模边沿',x,s[:1]),plot('Coupled and discharge currents','耦合与泄放电流',x,s[2:])])
        for label in ['weak','damped']:
            d=ringing(vin,label);x=d['t'];s=[signal('Vsw / 开关节点','V',d['v']),signal('Parasitic loop current / 寄生环路电流','A',d['i']),signal('Stored ring energy / 振铃储能','J',d['energy']),signal('Damping loss / 阻尼耗散','W',d['loss'])]
            add('P07',f'{vin}V_{label}',x,s,d['metrics'],25,vin,[plot('Parasitic ringing','寄生振铃',x,s[:1]),plot('Loop current','环路电流',x,s[1:2]),plot('Stored energy','储存能量',x,s[2:3]),plot('Damping dissipation','阻尼耗散',x,s[3:])])
    for temp in TEMPS:
        d=current_sense(temp);x=d['t'];s=[signal('Load current / 负载电流','A',d['load']),signal('Shunt voltage / 取样电压','V',d['vsense']),signal('Amplifier output / 放大器输出','V',d['out']),signal('Comparator output / 比较器输出','1',d['trip'])]
        add('P05',f'{temp}C',x,s,d['metrics'],temp,None,[plot('Sense amplifier response','取样放大器响应',x,s[1:3]),plot('Comparator trip','比较器动作',x,s[3:]),plot('Input current step','输入电流阶跃',x,s[:1])])
    cases.sort(key=lambda c:(c['model_id'],c['id']))
    result=dict(version='3.3.0',date='2026-11-03',python=platform.python_version(),numpy=np.__version__,models=models,cases=cases,conventions=dict(current='Signal direction is named by function; electrical supply ports not solved are absent, never zero-filled.',power='Waveform-specific dissipation, stored energy and budget estimates are explicitly separated.',source='All numerical coefficients assumed. No PDK, calibrated process parameters or full paper reproduction.'))
    (OUT/'simulation.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf-8')
    (ROOT/'model_catalog.json').write_text(json.dumps(models,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for c in cases:
        with (OUT/'csv'/f"{c['id']}.csv").open('w',newline='',encoding='utf-8-sig')as f:
            w=csv.writer(f);w.writerow([c['xlabel']]+[s['name']+' ('+s['unit']+')'for s in c['signals']]);w.writerows([x]+[s['y'][i]for s in c['signals']]for i,x in enumerate(c['x']))
    with (OUT/'case_summary.csv').open('w',newline='',encoding='utf-8-sig')as f:
        w=csv.writer(f);w.writerow(['case_id','model_id','temperature_C','Vin_V','points','metrics_json']);w.writerows([c['id'],c['model_id'],c['temp_C'],c['vin_V'],len(c['x']),json.dumps(c['metrics'],ensure_ascii=False)]for c in cases)
    count={m['id']:sum(c['model_id']==m['id']for c in cases)for m in models}
    print(json.dumps(dict(models=len(models),cases=len(cases),per_model=count,json_bytes=(OUT/'simulation.json').stat().st_size),indent=2))

if __name__=='__main__':main()
