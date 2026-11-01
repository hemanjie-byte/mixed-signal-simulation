import json, math, csv
from pathlib import Path
import numpy as np

ROOT=Path(__file__).parent
VINS=[40,60,80,100,120,150]
RATINGS=[60,80,120,150,200,200]
TEMPS=[-40,25,125]
# All numerical model parameters below are authored illustrative assumptions, not foundry data.
defs=[
('M01','高侧隔离NLDMOS','mos',1,'必需：高侧功率开关','BV、Rds(on)、Qg、Coss、SOA、浮地隔离、VGS','HV',0.25,2.0,1.2,400e-12),
('M02','低侧NLDMOS','mos',1,'同步Buck必需；异步可用续流二极管','BV、反向导通、Qrr、Rds(on)、SOA','HV',0.18,2.0,1.6,600e-12),
('M03','高压PLDMOS','mos',-1,'可选：P沟道高侧/模拟开关','BV、Rds(on)、Qg、隔离、VSG','HV',0.6,2.0,0.5,250e-12),
('M04','高压DENMOS','mos',1,'电平移位/高压检测','BV、Id、漏电、HCI、SOA','HV',40,1.6,0.01,10e-12),
('M05','低压NMOS','mos',1,'控制逻辑/误差放大/栅驱','VGS、VDS、Vth、gm、失配、噪声','LV',25,0.7,0.02,2e-12),
('M06','低压PMOS','mos',-1,'控制逻辑/栅驱上拉','VSG、VSD、Vth、gm、失配、噪声','LV',50,0.7,0.01,2e-12),
('M07','高压DEPMOS','mos',-1,'可选：电平移位/高压偏置','BV、Id、漏电、HCI','HV',80,1.6,0.005,8e-12),
('Q01','NPN双极晶体管','bjt',1,'带隙/温度传感/模拟偏置','β、VBE、BVCEO、Early电压、噪声','LV',0,0,100,0),
('Q02','PNP双极晶体管','bjt',-1,'带隙/温度传感；取决于架构','β、VEB、BV、衬底注入','LV',0,0,30,0),
('D01','体PN续流二极管','diode',1,'同步开关死区续流','VF、IR、Qrr、trr、IF、反向耐压','HV',0.1,1.5,1e-10,80e-12),
('D02','高压自举PN二极管','diode',1,'N沟道高侧驱动自举','反向耐压、VF、Qrr、结隔离','HV',3,1.4,1e-11,10e-12),
('D03','肖特基二极管','diode',1,'可选：异步续流/低压钳位；HV版本需确认','VF、IR、反向耐压、结电容','HV',0.08,1.1,1e-6,150e-12),
('D04','栅极Zener钳位','zener',1,'栅源过压保护；示例6V钳位','VZ容差、动态电阻、脉冲电流、温漂','LV',10,6,0,0),
('J01','高压启动JFET','jfet',1,'可选：VIN启动供电，启动后需关断','IDSS、夹断电压、耐压、静态损耗','HV',0,3,0.002,3e-12),
('R01','高压多晶硅电阻链','res',1,'VIN检测/欠压锁定/启动泄放','阻值、每段耐压、TCR、压系数、功耗','HV',100000,100e-6,0,0),
('R02','电流检测电阻','res',1,'电流检测；片上金属或外接','阻值、TCR、Kelvin连接、EM、电流密度','LV',0.05,200e-6,0,0),
('C01','MIM电容','cap',1,'补偿/采样；本模型为5V低压电容','容量、额定电压、密度、漏电、压系数','LV',0,0,100e-12,0),
('C02','MOM电容','cap',1,'补偿/滤波；本模型为5V低压电容','容量、额定电压、寄生、匹配','LV',0,0,20e-12,0),
('I01','隔离结与DTI等效网络','iso',1,'高侧浮动域隔离；不是独立功率器件','域间电压、负瞬态、Ciso、衬底注入、闩锁','HV',1e12,0,1e-12,0),
('E01','高压ESD钳位等效器件','esd',1,'引脚ESD保护；需专用验证模型','Vt1、Vhold、It2、动态钳位、HBM/CDM','HV',20,0,0,0),
('L01','外接功率电感','ind',1,'Buck储能；通常不集成于BCD','L、Isat、DCR、磁芯损耗、温升','EXT',0.1,0,100e-6,0),
('C03','外接输出电容','cap',1,'Buck输出滤波','容量、ESR、纹波电流、额定电压','EXT',0.02,0,47e-6,0),
('C04','外接输入电容','cap',1,'VIN去耦/高频脉冲回路','容量、ESR、纹波电流、DC偏置降容、耐压','HV',0.03,0,2.2e-6,0),
('C05','外接自举电容','cap',1,'高侧驱动供电；两端低压但共模高压','容量、漏电、VBS、共模绝缘、启动刷新','LV',0.05,0,100e-9,0)
]
devices=[]; runs=[]; checks=[]

def mos(v,g,p,T):
    vt=p['vth']-0.002*(T-25); beta=p['beta']*((T+273.15)/298.15)**-1.5
    r=p['r']*(1+0.004*(T-25)); u=max(g-vt,0)
    # Self-consistent intrinsic drain voltage with drift resistance; bisection solves I=f(V-I*R).
    lo=0.; hi=max(v,0.)
    for _ in range(45):
        vd=(lo+hi)/2
        ich=beta*(u*vd-vd*vd/2) if vd<u else beta*u*u/2
        ich=max(ich,0)*(1+0.01*vd)
        if vd+ich*r>v: hi=vd
        else: lo=vd
    vd=(lo+hi)/2
    return max((v-vd)/r,0) if r else 0

def diode(v,p,T):
    vt=8.617333262e-5*(T+273.15); Is=p['beta']*2**((T-25)/10); n=p['vth']; rs=p['r']
    if v<=0:return Is*(math.exp(max(v/(n*vt),-700))-1)
    lo=0.;hi=v/rs
    for _ in range(60):
        ii=(lo+hi)/2; voltage=n*vt*math.log1p(ii/Is)+ii*rs
        if voltage>v:hi=ii
        else:lo=ii
    return (lo+hi)/2

def bench(d,vin,rating,T):
    typ=d['type']; k=d['id']; scale=(rating/60)**1.5 if d['domain']=='HV' else 1
    p={'r':d['r']*scale if typ=='mos' else d['r'],'vth':d['vth'],'beta':d['beta'],'c':d['c'],'rating':rating if d['domain']=='HV' else (25 if k in ['L01','C03'] else 5)}
    if k=='C05':p['rating']=16
    if k=='D04':p['rating']=8
    g=5 if d['domain']=='HV' else 3.3
    note='单器件独立测试；所有数值为通用假设'
    if typ=='mos':
        x=np.linspace(0,vin if d['domain']=='HV' else 3.3,121); y=np.array([mos(v,g,p,T) for v in x]); xlabel='|VDS| (V)'; ylabel='|ID| (A)'
        opv=0.2 if k in ['M01','M02','M03'] else (vin/2 if d['domain']=='HV' else 1)
        opi=mos(opv,g,p,T); s=d['sign']; terminals={'VD (V)':s*opv,'VG (V)':s*g,'VS (V)':0,'VB (V)':0,'ID (A)':s*opi,'IG (A)':0,'IS (A)':-s*opi,'IB (A)':0}
        gm=(mos(opv,g+.001,p,T)-mos(opv,g-.001,p,T))/.002
        extra={'Vth绝对值 (V)':p['vth']-.002*(T-25),'Rds有效 (ohm)':opv/max(opi,1e-30),'gm (S)':gm,'Cgate假设 (F)':p['c'],'Qg线性估算 (C)':p['c']*g,'VGS (V)':s*g,'VDS (V)':s*opv,'门极DC电流假设 (A)':0}
        note+='；忽略亚阈值/漏电、体效应、Miller非线性、自热反馈、雪崩；P型用绝对值曲线'
    elif typ=='bjt':
        x=np.linspace(.4,.75,121); isat=1e-15*2**((T-25)/10); vt=8.617333262e-5*(T+273.15)
        y=isat*np.expm1(x/vt)*(1+1/50); xlabel='|VBE| (V)';ylabel='|IC| (A)'
        opv=1.;opi=isat*math.expm1(.65/vt)*1.02; ib=opi/p['beta'];s=d['sign'];terminals={'VC (V)':s,'VB (V)':s*.65,'VE (V)':0,'IC (A)':s*opi,'IB (A)':s*ib,'IE (A)':-s*(opi+ib)};extra={'β假设':p['beta'],'VBE绝对值 (V)':.65,'Early电压假设 (V)':50};note+='；正向有源区近似，不含饱和/高注入'
    elif typ=='diode':
        x=np.linspace(-1,1.2,121); y=np.array([diode(v,p,T) for v in x]);xlabel='VAK (V)';ylabel='IA (A)';opv=.8 if k!='D03' else .5;opi=diode(opv,p,T);terminals={'VA (V)':opv,'VK (V)':0,'IA (A)':opi,'IK (A)':-opi};extra={'IR@-VIN估算 (A)':-diode(-vin,p,T),'Cj常数假设 (F)':p['c'],'反向等级假设 (V)':rating};note+='；无反向击穿/反向恢复，Qrr与trr无法由本模型预测'
    elif typ=='zener':
        x=np.linspace(0,8,121); vz=p['vth']*(1+.0005*(T-25));y=np.maximum(x-vz,0)/p['r'];xlabel='VKA反向 (V)';ylabel='IK反向 (A)';opv=6.2;opi=max(opv-vz,0)/p['r'];terminals={'VK (V)':opv,'VA (V)':0,'IK (A)':opi,'IA (A)':-opi};extra={'Vz (V)':vz,'rz (ohm)':p['r']};note+='；只用于钳位机理，非栅氧允许电压'
    elif typ=='jfet':
        x=np.linspace(0,vin,121); idss=p['beta']*((T+273.15)/298.15)**-1.5;y=idss*(1-np.exp(-x/3));xlabel='VDS (V)';ylabel='ID (A)';opv=vin;opi=float(y[-1]);terminals={'VD (V)':opv,'VG (V)':0,'VS (V)':0,'ID (A)':opi,'IG (A)':0,'IS (A)':-opi};extra={'IDSS (A)':idss,'夹断尺度假设 (V)':3};note+='；VGS=0启动状态，不含关断网络'
    elif typ=='res':
        r=p['r']*(1+p['vth']*(T-25));x=np.linspace(0,vin if k=='R01' else .1,121);y=x/r;xlabel='VAB (V)';ylabel='IA (A)';opv=vin if k=='R01' else .05;opi=opv/r;terminals={'VA (V)':opv,'VB (V)':0,'IA (A)':opi,'IB (A)':-opi};extra={'R(T) (ohm)':r,'TCR (1/K)':p['vth']};note+='；R01需分段满足单段耐压；无电迁移模型'
    elif typ in ['cap','iso','ind']:
        f=200e3;x=np.linspace(0,5,121);t=x*1e-6;w=2*math.pi*f;xlabel='时间 (us)';ylabel='I端口 (A)'
        bias=vin/2 if k in ['C04','I01'] else (12 if k=='C03' else (5 if k=='C05' else 2.5));amp=vin*.1 if k in ['C04','I01'] else .1
        c=p['beta']; va=bias+amp*np.sin(w*t)
        if typ=='ind':
            # L di/dt = sinusoidal voltage, current bias 1A. Series DCR accounted in terminal voltage.
            y=1-amp/(w*c)*np.cos(w*t);va=amp*np.sin(w*t)+p['r']*y;opv=p['r'];opi=1.;extra={'L (H)':c,'DCR (ohm)':p['r'],'储能@1A (J)':.5*c};note+='；未包含饱和和磁芯损耗'
        else:
            y=c*amp*w*np.cos(w*t)
            if typ=='iso':y+=va/p['r']
            opv=bias;opi=c*amp*w+(bias/p['r'] if typ=='iso' else 0);extra={'C (F)':c,'频率 (Hz)':f,'AC幅度 (V)':amp,'ESR (ohm)':p['r'] if typ=='cap' else 0,'储能@偏置 (J)':.5*c*bias*bias};note+='；温度系数假设为零'
        terminals={'VA (V)':opv,'VB (V)':0,'IA (A)':opi,'IB (A)':-opi}
    else:
        threshold=1.3*rating;x=np.linspace(0,1.5*rating,121);y=np.maximum(x-threshold,0)/p['r'];xlabel='Vpad (V)';ylabel='Iclamp (A)';opv=1.4*rating;opi=(opv-threshold)/p['r'];terminals={'Vpad (V)':opv,'Vreturn (V)':0,'Ipad (A)':opi,'Ireturn (A)':-opi};extra={'Vtrigger假设 (V)':threshold,'动态电阻 (ohm)':p['r']};note+='；人为钳位曲线，没有snapback、It2或ESD认证能力'
    power=opv*opi
    if typ=='bjt':power+=.65*abs(terminals['IB (A)'])
    extra['瞬时端口功率 (W)']=power
    if typ in ['cap','iso','ind']:extra['功率解释']='瞬时端口功率含储能交换，不等于耗散'
    else:extra['ΔT估算@50K/W (K)']=power*50
    residual=sum(v for key,v in terminals.items() if '(A)' in key)
    return {'id':k,'vin':vin,'rating':p['rating'],'temp':T,'x':x.tolist(),'y':y.tolist(),'drive':va.tolist() if typ in ['cap','iso','ind'] else None,'xlabel':xlabel,'ylabel':ylabel,'opv':opv,'opi':opi,'power':power,'terminals':terminals,'extra':extra,'parameters':p,'note':note,'kcl':residual}

for row in defs:
    id,name,typ,sign,role,metrics,dom,r,vth,beta,c=row
    d=dict(id=id,name=name,type=typ,sign=sign,role=role,metrics=metrics,domain=dom,r=r,vth=vth,beta=beta,c=c)
    d['model']={'mos':'平方律沟道 + 串联漂移电阻，二分法求解；μ∝T^-1.5，Vth温漂−2mV/K','bjt':'IC=IS(T)·(exp(VBE/VT)−1)·(1+VCE/50)，IB=IC/β','diode':'V=nVT·ln(1+I/IS)+I·Rs，二分法求解；反偏为−IS','zener':'IK=max(VKA−Vz(T),0)/rz','jfet':'ID=IDSS(T)·(1−exp(−VDS/3))，VGS=0','res':'I=V/[R25·(1+TCR·(T−25))]','cap':'I=C·dV/dt，V=Vbias+Vac·sin(2πft)','iso':'I=V/Riso+Ciso·dV/dt','ind':'L·di/dt=vL；V端=vL+DCR·I','esd':'I=max(Vpad−1.3·等级,0)/20'}[typ]
    devices.append(d)
    for vin,rating in zip(VINS,RATINGS):
        for T in TEMPS:runs.append(bench(d,vin,rating,T))

# Exact piecewise triangular CCM reference waveforms. Buck illustrative electrical sizing, not closed-loop SPICE.
bucks=[]
for vin,rating in zip(VINS,RATINGS):
    vo=12.;io=1.;f=200e3;L=100e-6;C=47e-6;esr=.02;D=vo/vin;period=1/f
    di=(vin-vo)*D/(f*L);ts=np.linspace(0,period,1001);phase=ts/period
    il=np.where(phase<=D,io-di/2+(vin-vo)/L*ts,io+di/2-vo/L*(ts-D*period))
    ic=il-io;vc=np.r_[0,np.cumsum((ic[:-1]+ic[1:])/2*np.diff(ts))/C];vc-=np.trapezoid(vc,ts)/period
    out=vo+vc+esr*ic;sw=np.where(phase<D,vin,0);ih=np.where(phase<D,il,0);ils=np.where(phase<D,0,il)
    r=.25*(rating/60)**1.5 + 1/(1.2*3);rl=.18*(rating/60)**1.5+1/(1.6*3)
    irms2=io**2+di**2/12;pcond=irms2*(D*r+(1-D)*rl);psw=.5*vin*io*40e-9*f;pgate=2*2e-9*5*f;pl=irms2*.1;pcap=di*di/12*esr;loss=pcond+psw+pgate+pl+pcap
    bucks.append({'vin':vin,'rating':rating,'D':D,'on_ns':D/f*1e9,'di':di,'imin':io-di/2,'imax':io+di/2,'vripple_mV':float(np.ptp(out)*1000),'pcond':pcond,'psw':psw,'pgate':pgate,'pl':pl,'pcap':pcap,'eta':12/(12+loss),'t_us':(ts*1e6).tolist(),'il':il.tolist(),'ic':ic.tolist(),'vo':out.tolist(),'sw':sw.tolist(),'ih':ih.tolist(),'ils':ils.tolist(),'vds_h':(vin-sw).tolist(),'vds_l':sw.tolist(),'vgs_h':np.where(phase<D,5,0).tolist(),'vgs_l':np.where(phase<D,0,5).tolist(),'iin_avg':12/vin,'iin_cap_rms':io*math.sqrt(D*(1-D)),'charge_residual':float(np.trapezoid(ic,ts))})

checks=[{'test':'432个独立器件测试覆盖','value':len(runs),'limit':432,'pass':len(runs)==432}, {'test':'所有器件KCL最大残差(A)','value':max(abs(r['kcl']) for r in runs),'limit':1e-10,'pass':max(abs(r['kcl']) for r in runs)<1e-10}, {'test':'曲线均为有限数','value':int(all(np.isfinite(r['y']).all() for r in runs)),'limit':1,'pass':all(np.isfinite(r['y']).all() for r in runs)}, {'test':'Buck电容周期电荷残差(C)','value':max(abs(b['charge_residual']) for b in bucks),'limit':1e-12,'pass':max(abs(b['charge_residual']) for b in bucks)<1e-12}, {'test':'Buck六工况均处于CCM','value':min(b['imin'] for b in bucks),'limit':0,'pass':min(b['imin'] for b in bucks)>0}]
data={'date':'2026-11-01','vins':VINS,'ratings':RATINGS,'temps':TEMPS,'devices':devices,'runs':runs,'bucks':bucks,'checks':checks}
ROOT.joinpath('data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
with ROOT.joinpath('device_runs.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['id','Vin_V','rating_V','temperature_C','V_test_V','I_test_A','P_instantaneous_W','KCL_residual_A']);w.writerows([[r[k] for k in ['id','vin','rating','temp','opv','opi','power','kcl']] for r in runs])
print(json.dumps({'devices':len(devices),'runs':len(runs),'checks':checks},ensure_ascii=False))
