"""Run all V3 cases and export deterministic JSON/CSV artifacts."""
from pathlib import Path
import json,csv,sys,platform
import numpy as np
from analog_models import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'


def catalog():
    # Numerical values are demonstration assumptions unless identified as constants.
    records=[
    ('A01','Four-terminal MOS interpolation','四端MOS连续插值','device_extension','B01',
     'Id = 2 n beta Ut^2 (softplus(xs)^2 - softplus(xd)^2) (1 + lambda |Vds|). Pair-capacitor charges sum to zero.',
     '弱反型至强反型连续电流，另用守恒的固定互电容网络表示端口电荷。',
     {'n':1.5,'beta_25_A_per_V2':.001,'Vth_25_V':.55,'dVth_dT_V_per_K':-.001,'mobility_T_exponent':-1.5,'lambda_per_V':.03,'Cgs_F':2e-12,'Cgd_F':.2e-12,'Cgb_F':.1e-12,'Cdb_Csb_F':.3e-12},
     '0–1.8 V low-voltage demonstration. No avalanche, oxide leakage, DIBL, velocity saturation, intrinsic charge partition or measured fit. Not full EKV/BSIM.',
     '仅0–1.8V低压示意；无雪崩、栅漏、DIBL、速度饱和、内禀电荷分配或实测拟合；不是完整EKV/BSIM。','mos'),
    ('A02','Junction charge and varactor','结电荷与变容二极管','device_extension','B07',
     'C(V)=C0(1-V/phi)^(-m); Q(V)=C0 phi [1-(1-V/phi)^(1-m)]/(1-m); Idisplacement=C(V)dV/dt.',
     '从C(V)积分得到Q(V)，瞬态位移电流为C(V)dV/dt。',
     {'C0_25_F':2e-12,'C0_TC_per_K':.0002,'phi_V':.7,'m':.5,'transient_bias_V':-2,'transient_amplitude_V':1,'frequency_Hz':1e6},
     'Depletion capacitance only, -20 <= V < 0.35 V. No forward diffusion charge, breakdown or series resistance. Reverse leakage is an assumed 1 pA.',
     '仅耗尽电容，-20≤V<0.35V；不含正向扩散电荷、击穿和串联电阻；反向漏电假设为1pA。','junction'),
    ('A03','Reciprocal NPN Ebers–Moll','满足互易关系的NPN Ebers–Moll','device_extension','B07',
     'Ic=alphaF IF-IR; Ib=(1-alphaF)IF+(1-alphaR)IR; Ie=-IF+alphaR IR; alphaF IES=alphaR ICS=IS.',
     '分别求解正、反向结注入，三端电流满足KCL和互易关系。',
     {'IS_25_A':1e-15,'betaF':100,'betaR':2,'Eg_eV':1.11,'IS_T_exponent':3},
     'Generic silicon NPN, not a SiGe HBT. Low-injection DC only; no Early effect, high injection, transit time, RF fT or breakdown.',
     '通用硅NPN，不是SiGe HBT；仅低注入直流，不含Early效应、大注入、渡越时间、fT及击穿。','bjt'),
    ('A04','MOS pair mismatch and correlation','MOS配对失配与相关性','parameter_extension','B02',
     'sigma(pair)=A_VT sqrt((1-rho)/(WL)); individual uncorrelated sigma=A_VT/sqrt(2WL).',
     '区分配对标准差和单管标准差，并演示共同偏移的抵消。',
     {'A_VT_pair_V_um':.003,'rho':.25,'samples':20000,'global_sigma_V':.02,'areas_um2':[1,4,16,64],'seed':20261101},
     'Assumed Gaussian local mismatch and correlation. No foundry statistics, spatial-gradient fit, yield certification or temperature-dependent mismatch law.',
     '高斯局部失配和相关系数为假设；无工艺统计、空间梯度拟合、良率认证或温度失配律。','pair'),
    ('B01','MOS differential pair','MOS差分对','circuit_benchmark','B01',
     'Solve Id1(Vs)+Id2(Vs)=Itail with bisection using A01; Vg1/2=Vcm +/- Vdiff/2.',
     '用A01求解共同源极电压，使两支路之和等于尾电流。',
     {'Vcm_V':.85,'Vd1_Vd2_V':1.8,'Itail_A':100e-6,'bisection_steps':80},
     'Fixed drain biases and ideal tail source. No amplifier load, common-mode feedback, frequency compensation or finite tail impedance.',
     '固定漏端偏置、理想尾电流源；不含放大器负载、共模反馈、频率补偿及尾源有限阻抗。','pair'),
    ('B02','CTAT/PTAT reference sum','CTAT/PTAT基准合成','circuit_benchmark','B03',
     'Vbe=Vg0+(Vbe0-Vg0)T/T0-eta Ut ln(T/T0); deltaVbe=Ut ln(N); Vref=Vbe+a deltaVbe; dVref/dT|T0=0.',
     '一阶温漂在25°C相消，并保留VBE曲率；输出PTAT电流为deltaVbe/R1。',
     {'Vg0_V':1.205,'Vbe0_V':.68,'eta':3,'area_ratio':8,'R1_ohm':10000,'T0_K':298.15},
     'Ideal voltage sum inspired by bandgap principles, not the 2.5 V Brokaw circuit reproduction. No start-up, PSRR, trimming, resistor TC, mismatch or output load.',
     '按带隙原理的理想电压合成，并非复现Brokaw的2.5V电路；不含启动、PSRR、修调、电阻温漂、失配及输出负载。','reference'),
    ('B03','Input noise and sampled kT/C','输入噪声与采样kT/C','circuit_benchmark','B08',
     'Splain=en^2(1+fc/f); Ssuppressed=en^2(2+fc/(f+fchop)); variance=integral S(f)df; sampled variance=kT/C.',
     '演示抑制低频噪声时的白噪声代价；另列采样热噪声。',
     {'en_25_V_per_sqrtHz':1e-8,'fc_Hz':100,'fchop_Hz':20000,'sample_C_F':1e-12,'integration_band_Hz':[1,1e6]},
     'Illustrative spectral shaping, not a switched chopper circuit or measured op amp. No current noise, source resistance, aliasing, ripple or charge injection.',
     '仅示意频谱整形，不是开关斩波电路或实测运放；不含电流噪声、源阻、混叠、纹波和电荷注入。','amplifier'),
    ('B04','Capacitor DAC and SAR ADC','电容DAC与SAR ADC','circuit_benchmark','B05 B02',
     'Binary CDAC plus dummy capacitor; sequential bit decisions; DNL from code widths; endpoint INL; coherent 16384-point FFT at bin 503.',
     '二进制电容阵列逐位比较，分别计算码宽DNL、端点INL及相干FFT动态指标。',
     {'bits':10,'Vref_V':1.8,'fs_Hz':2e6,'samples':16384,'tone_bin':503,'input_amplitude_fraction_of_Vref':.49,'unit_sigma_cases':[0,.02],'seed':20261101},
     'Ideal comparator and full settling. No aperture jitter, thermal/comparator noise, switch leakage, reference droop or supply-current prediction. Capacitor mismatch is assumed.',
     '比较器理想且完全建立；不含采样抖动、热噪声/比较器噪声、开关漏电、参考跌落及供电电流预测；电容失配为假设。','adc'),
    ('B05','LDO loop and load step','LDO环路与负载阶跃','circuit_benchmark','B06',
     'C dv/dt=ip-v/R-dIload; dip/dt=wa(-Gv-ip). L(s)=G/[(Cs+1/R)(1+s/wa)].',
     '二状态线性反馈模型，输出负载阶跃、环路增益和相位裕度。',
     {'Vin_V':3.3,'Vout_nom_V':1.8,'Iload_nom_A':.02,'delta_Iload_A':.01,'Cout_F':10e-6,'Rload_ohm':90,'G_25_A_per_V':.5,'G_T_exponent':-1.2,'amplifier_pole_Hz':20000,'Iq_A':30e-6,'dt_s':1e-7},
     'Small perturbation around a biased operating point; no dropout, current limit, start-up, ESR zero or transistor netlist. Not a reproduction of the cited measured LDO.',
     '围绕偏置点的小扰动模型；无压差极限、限流、启动、ESR零点或晶体管网表；并非复现引用论文的实测LDO。','ldo'),
    ('B06','Phase loop and noise transfer','相位环路与噪声传递','circuit_benchmark','B09',
     'H(s)=wn^2/(s^2+2 zeta wn s+wn^2); Sout=|H|^2 Sref+|1-H|^2 Svco; jitter=sqrt(integral Sout df)/(2 pi fcarrier).',
     '典型二阶相位响应与互补噪声传递，区分单边相位PSD和SSB噪声。',
     {'natural_frequency_Hz':1e5,'zeta_cases':[.3,.7,1.2],'phase_step_rad':.1,'carrier_Hz':1e9,'integration_band_Hz':[100,1e7],'Sref_rad2_per_Hz':1e-13,'Svco_floor_rad2_per_Hz':1e-16},
     'Canonical phase-domain abstraction without a loop zero. Not a transistor VCO, a full type-II PLL, ISF extraction, cycle-slip or acquisition simulation.',
     '无环路零点的典型相位域抽象；不是晶体管VCO、完整二型PLL、ISF提取、周跳或捕获仿真。','pll'),
    ('B07','40–150 V synchronous buck','40–150V同步降压','circuit_benchmark','D01',
     'L di/dt=u Vin-(Rsw+RL)i-v; C dv/dt=i-v/Rload. Exact period-map initialization; event-aligned RK4; input-output-loss-energy balance.',
     '用解析周期映射初始化，再在每个开关边沿精确分段，校核输入、输出、导通损耗和储能变化。',
     {'Vin_max_classes_V':[40,60,80,100,120,150],'Vout_target_V':12,'L_H':100e-6,'C_F':22e-6,'Rload_ohm':12,'Rsw_25_ohm':.18,'RL_25_ohm':.12,'resistance_TC_per_K':.004,'fs_Hz':250e3,'steps_per_cycle':200,'warmup_cycles':35,'saved_cycles':5},
     'Forced CCM with ideal instantaneous switches. Efficiency includes conduction loss only; no switching/gate/core loss, dead time, ringing, control-loop start-up, SOA or validated voltage rating.',
     '强制连续导通、理想瞬时开关；效率仅含导通损耗；无开关/栅极/磁芯损耗、死区、振铃、控制启动、SOA或已验证耐压。','buck')]
    return [dict(id=i,name_en=en,name_zh=zh,kind=kind,source_ids=refs.split(),equation_en=eq,equation_zh=eqzh,parameters=param,limits_en=lim,limits_zh=limzh,geometry=geo,parameter_origin_en='Demonstration assumptions; SI constants k and q are exact.',parameter_origin_zh='数值为演示假设；SI常数k与q采用精确定义。') for i,en,zh,kind,refs,eq,eqzh,param,lim,limzh,geo in records]


def array(x,n):
    return np.broadcast_to(np.asarray(x,dtype=float),(n,)).tolist()


def terminal(name,v,i,n):return dict(name=name,v=array(v,n),i=array(i,n))
def signal(name,unit,y):return dict(name=name,unit=unit,y=np.asarray(y).tolist())
def plot(title,title_zh,x,xlabel,signals,xlog=False):return dict(title_en=title,title_zh=title_zh,x=np.asarray(x).tolist(),xlabel=xlabel,series=signals,xlog=xlog)


def main():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'csv').mkdir(exist_ok=True)
    models=catalog();cases=[]
    def add(mid,tag,x,xlabel,signals,terminals=None,plots=None,temp=25,vin=None,metrics=None,notes=''):
        terminals=terminals or [];power=np.sum([np.array(t['v'])*t['i']for t in terminals],axis=0).tolist() if terminals else None
        c=dict(id=f'{mid}_{tag}',model_id=mid,temp_C=temp,vin_V=vin,x=np.asarray(x).tolist(),xlabel=xlabel,
               signals=signals,terminals=terminals,port_power_W=power,plots=plots or [],metrics=metrics or {},notes_en=notes)
        if terminals:c['metrics']['max_KCL_residual_A']=float(np.max(np.abs(np.sum([t['i']for t in terminals],axis=0))))
        if not c['plots']:c['plots']=[plot(mid+' response','响应',x,xlabel,signals[:1])]
        cases.append(c)
    for temp in [-40,25,125]:
        for mode in ['transfer','output','body']:
            x=np.linspace(0,1.8,401) if mode!='body' else np.linspace(-.5,.3,321)
            vg=x if mode=='transfer' else .9;vd=x if mode=='output' else 1.2;vb=x if mode=='body' else 0
            ids=mos_current(vg,vd,0,vb,temp);gm,gds,gmb=mos_small_signal(vg,vd,0,vb,temp);n=len(x)
            qs=mos_charges(vg,vd,0,vb)
            sig=[signal('Id / 漏电流','A',ids),signal('gm / 跨导','S',gm),signal('gds / 输出电导','S',gds),signal('gmb / 体跨导','S',gmb)]
            if mode!='output':sig.append(signal('gm/Id / 跨导效率','1/V',gm/ids))
            sig += [signal('Q'+k+' / 端口电荷','C',array(q,n)) for k,q in zip(['G','D','S','B'],qs)]
            terms=[terminal('G',vg,0,n),terminal('D',vd,ids,n),terminal('S',0,-ids,n),terminal('B',vb,0,n)]
            add('A01',f'{mode}_{temp}C',x,{'transfer':'Vg (V)','output':'Vd (V)','body':'Vb (V)'}[mode],sig,terms,temp=temp,metrics={'charge_sum_max_C':float(np.max(np.abs(qs.sum(axis=0))))})
        v=np.linspace(-10,.3,401);q,c=junction_qc(v,temp);i=1e-12*np.expm1(v/thermal_voltage(temp));n=len(v)
        add('A02',f'CV_{temp}C',v,'Va-Vk (V)',[signal('Cj / 结电容','F',c),signal('Qj / 结电荷','C',q),signal('Idc / 直流电流','A',i)],[terminal('A',v,i,n),terminal('K',0,-i,n)],temp=temp)
        t=np.linspace(0,3e-6,1201);v=-2+np.sin(2*np.pi*1e6*t);q,c=junction_qc(v,temp);i=c*2*np.pi*1e6*np.cos(2*np.pi*1e6*t)-1e-12;n=len(t)
        add('A02',f'transient_{temp}C',t,'Time / 时间 (s)',[signal('Va / 阳极电压','V',v),signal('Ia / 阳极电流','A',i),signal('Qj / 结电荷','C',q)],[terminal('A',v,i,n),terminal('K',0,-i,n)],temp=temp)
        isat=1e-15*((temp+273.15)/T0)**3*np.exp(1.11*QE/KB*(1/T0-1/(temp+273.15)))
        for mode in ['gummel','saturation']:
            x=thermal_voltage(temp)*np.log1p(np.geomspace(1e-9,1e-3,401)/isat) if mode=='gummel' else np.linspace(0,1.2,401)
            vb=x if mode=='gummel' else float(thermal_voltage(temp)*np.log1p(1e-4/isat));vc=1.2 if mode=='gummel' else x
            ic,ib,ie=bjt_currents(vb,vc,0,temp);n=len(x)
            add('A03',f'{mode}_{temp}C',x,'Vbe (V)' if mode=='gummel' else 'Vce (V)',[signal('Ic / 集电流','A',ic),signal('Ib / 基电流','A',ib),signal('Ie / 发射极电流','A',ie)],[terminal('C',vc,ic,n),terminal('B',vb,ib,n),terminal('E',0,ie,n)],temp=temp)
        v=np.linspace(-.3,.3,401);src,i1,i2=differential_pair(v,temp);n=len(v)
        add('B01',f'{temp}C',v,'Differential input / 差分输入 (V)',[signal('I1 / 支路1','A',i1),signal('I2 / 支路2','A',i2),signal('Vs / 共源电压','V',src)],[terminal('D1',1.8,i1,n),terminal('D2',1.8,i2,n),terminal('G1',.85+v/2,0,n),terminal('G2',.85-v/2,0,n),terminal('Tail',src,-1e-4,n)],temp=temp,plots=[plot('Current steering','电流转向',v,'Vdiff (V)',[signal('I1','A',i1),signal('I2','A',i2)])])
        f=np.geomspace(1,1e6,1001);plain,supp=noise_psd(f,temp)
        add('B03',f'{temp}C',f,'Frequency / 频率 (Hz)',[signal('Plain input ASD / 未抑制噪声','V/sqrt(Hz)',np.sqrt(plain)),signal('Suppressed input ASD / 抑制后噪声','V/sqrt(Hz)',np.sqrt(supp))],temp=temp,plots=[plot('Input noise density','输入噪声密度',f,'Frequency (Hz)',[signal('Plain','V/sqrt(Hz)',np.sqrt(plain)),signal('Suppressed','V/sqrt(Hz)',np.sqrt(supp))],True)],metrics={'plain_integrated_Vrms':float(np.sqrt(np.trapezoid(plain,f))),'suppressed_integrated_Vrms':float(np.sqrt(np.trapezoid(supp,f))),'sample_kTC_Vrms':float(np.sqrt(KB*(temp+273.15)/1e-12))})
        d=ldo_response(temp);t=d['t'];n=len(t);terms=[terminal('IN',3.3,d['ipass']+30e-6,n),terminal('OUT',d['vout'],-d['iload'],n),terminal('GND',0,d['iload']-d['ipass']-30e-6,n)]
        add('B05',f'{temp}C',t,'Time after load step / 负载阶跃后时间 (s)',[signal('Vout / 输出','V',d['vout']),signal('Ipass / 调整管电流','A',d['ipass']),signal('Iload / 负载电流','A',d['iload'])],terms,temp=temp,metrics={'final_Vout_V':float(d['vout'][-1]),'minimum_Vout_V':float(d['vout'].min()),'phase_margin_deg':float(d['phase_margin']),'unity_gain_frequency_Hz':float(d['unity_hz'])},plots=[plot('Load transient','负载瞬态',t,'Time (s)',[signal('Vout','V',d['vout'])]),plot('Loop magnitude','环路幅频',d['f'],'Frequency (Hz)',[signal('|L|','dB',20*np.log10(abs(d['loop'])))],True),plot('Loop phase','环路相频',d['f'],'Frequency (Hz)',[signal('Phase','deg',np.angle(d['loop'],deg=True))],True)])
        for vin in [40,60,80,100,120,150]:
            d=buck_response(vin,temp);t=d['t'];n=len(t)
            terms=[terminal('IN',vin,d['i']*d['on'],n),terminal('OUT',d['v'],-d['v']/12,n),terminal('GND',0,d['v']/12-d['i']*d['on'],n)]
            sig=[signal('Vout / 输出','V',d['v']),signal('IL / 电感电流','A',d['i']),signal('Vsw / 开关节点','V',d['sw']),signal('Vds_HS / 高侧漏源电压','V',vin-d['sw']),signal('Vgs_HS / 理想高侧驱动','V',5*d['on']),signal('Pin / 输入功率','W',d['pin']),signal('Pout / 输出功率','W',d['pout']),signal('Pconduction / 导通损耗','W',d['loss']),signal('Stored energy / 储能','J',d['energy'])]
            add('B07',f'{vin}V_{temp}C',t,'Time / 时间 (s)',sig,terms,temp=temp,vin=vin,metrics=d['metrics'],plots=[plot('Output ripple','输出纹波',t,'Time (s)',sig[:1]),plot('Inductor current','电感电流',t,'Time (s)',sig[1:2]),plot('Switch voltage stress','开关电压应力',t,'Time (s)',sig[2:4])])
    for area in [1,4,16,64]:
        v1,v2,dv,pred=mismatch_samples(area);hist,edges=np.histogram(dv,bins=61,density=True);centers=(edges[1:]+edges[:-1])/2
        add('A04',f'area{area}um2',np.arange(512),'Sample index / 样本序号',[signal('Device1 deltaVth / 单管1偏移','V',v1[:512]),signal('Device2 deltaVth / 单管2偏移','V',v2[:512]),signal('Pair deltaVth / 配对差','V',dv[:512])],plots=[plot('Pair mismatch density','配对失配密度',centers,'Delta Vth (V)',[signal('Probability density / 概率密度','1/V',hist)])],metrics={'area_um2':area,'sample_count':20000,'pair_sigma_prediction_V':float(pred),'pair_sigma_observed_V':float(np.std(dv,ddof=1))},notes='Metrics and histogram use 20000 samples. Raw display retains the first 512 samples; regenerate with the documented seed for all draws.')
    temp=np.linspace(-40,125,661);vbe,dv,ref,scale=bandgap(temp)
    add('B02','temperature',temp,'Temperature / 温度 (degC)',[signal('Vref / 基准','V',ref),signal('Vbe / CTAT','V',vbe),signal('Scaled PTAT / 加权PTAT','V',scale*dv),signal('IPTAT / PTAT电流','A',dv/10000)],temp=None,metrics={'PTAT_scale':float(scale),'Vref_25_V':float(bandgap(25)[2]),'Vref_max_min_span_V':float(np.ptp(ref))},plots=[plot('Reference curvature','基准曲率',temp,'Temperature (degC)',[signal('Vref','V',ref)]),plot('CTAT and PTAT','CTAT与PTAT',temp,'Temperature (degC)',[signal('Vbe','V',vbe),signal('Scaled PTAT','V',scale*dv)])])
    for mismatch in [0,.02]:
        d=adc_metrics(unit_sigma=mismatch);label='ideal' if mismatch==0 else 'mismatch';x=d['t']
        add('B04',label,x,'Time / 时间 (s)',[signal('Vin / 输入','V',d['vin']),signal('Reconstructed / 重建','V',d['vout']),signal('Output code / 输出码','code',d['codes'])],metrics=d['metrics'],plots=[plot('Sampled sine','采样正弦',x[:256],'Time (s)',[signal('Input','V',d['vin'][:256]),signal('Reconstructed','V',d['vout'][:256])]),plot('DNL','微分非线性',np.arange(1024),'Code',[signal('DNL','LSB',d['dnl'])]),plot('Endpoint INL','端点积分非线性',np.arange(1024),'Code',[signal('INL','LSB',d['inl'])]),plot('Coherent FFT','相干FFT',d['freq'][1:],'Frequency (Hz)',[signal('Amplitude / 幅度','dBc',d['spectrum_dbc'][1:])])])
    for zeta in [.3,.7,1.2]:
        d=pll_response(zeta);t=d['t']
        add('B06',f'zeta{zeta}',t,'Time / 时间 (s)',[signal('Output phase / 输出相位','rad',d['phase']),signal('Frequency deviation / 频偏','Hz',d['frequency_error'])],metrics={'zeta':zeta,'integrated_jitter_s':float(d['jitter_s']),'final_phase_rad':float(d['phase'][-1])},plots=[plot('Phase step','相位阶跃',t,'Time (s)',[signal('Output phase','rad',d['phase'])]),plot('SSB phase noise','单边带相位噪声',d['f'],'Offset frequency (Hz)',[signal('L(f)','dBc/Hz',10*np.log10(d['noise']/2))],True)])
    cases.sort(key=lambda c:(c['model_id'],c['id']))
    result=dict(version='3.0.0',date='2026-11-01',python=platform.python_version(),numpy=np.__version__,models=models,cases=cases,
                conventions={'current':'Positive into the modeled device/block. Unmodeled electrical ports are absent, never silently zero.','power':'sum(Vterminal * Iterminal), W; includes storage and dissipation; not automatically heat.','source':'All numerical parameters assumed; no PDK, TCAD or measured-fit validation.'})
    (OUT/'simulation_v3.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf-8')
    (ROOT/'models/model_catalog.json').write_text(json.dumps(models,ensure_ascii=False,indent=2),encoding='utf-8')
    for c in cases:
        headers=[c['xlabel']]+[t['name']+s for t in c['terminals']for s in [' V',' A']]+(['Port power W']if c['terminals']else[])+[s['name']+' ('+s['unit']+')'for s in c['signals']]
        with (OUT/'csv'/f"{c['id']}.csv").open('w',newline='',encoding='utf-8-sig')as f:
            w=csv.writer(f);w.writerow(headers)
            for j,x in enumerate(c['x']):w.writerow([x]+[z for t in c['terminals']for z in [t['v'][j],t['i'][j]]]+([c['port_power_W'][j]]if c['terminals']else[])+[s['y'][j]for s in c['signals']])
    print(json.dumps({'models':len(models),'cases':len(cases),'bytes':(OUT/'simulation_v3.json').stat().st_size,'per_model':{m['id']:sum(c['model_id']==m['id']for c in cases)for m in models}},indent=2))


if __name__=='__main__':main()
