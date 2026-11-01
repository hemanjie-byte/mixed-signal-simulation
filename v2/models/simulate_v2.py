"""Public-evidence-inspired behavioral test benches, NOT foundry models or paper fits.
Run from any directory. Only NumPy is required. All parameters and signs are explicit.
"""
import json,csv,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
Q=1.602176634e-19; KB=1.380649e-23; H=6.62607015e-34
TEMPS=[-40,25,125]; VINS=[40,60,80,100,120,150]
MODELS=[]; CASES=[]; CHECKS=[]

def model(id,name,group,shape,papers,formula,params,scope,kind='new'):
    d=dict(id=id,name=name,group=group,shape=shape,paper_ids=papers.split(),formula=formula,parameters=params,scope=scope,kind=kind,
           parameter_origin='全部数值为人为演示假设，未拟合论文曲线，无工艺/产品耐压认证')
    MODELS.append(d); return d

def tr(name,unit,y):return dict(name=name,unit=unit,y=np.asarray(y,dtype=float).tolist())
def plot(title,x,xlabel,unit,series,xlog=False):return dict(title=title,x=np.asarray(x,dtype=float).tolist(),xlabel=xlabel,unit=unit,series=[tr(n,unit,y) for n,y in series],xlog=xlog)
def terminal(name,v,i,n):return dict(name=name,v=np.broadcast_to(v,(n,)).tolist(),i=np.broadcast_to(i,(n,)).tolist())
def case(d,T,x,xlabel,terminals,extra,metrics,vin=None,notes='',plots=None):
    x=np.asarray(x); n=len(x)
    assert all(len(t['v'])==n and len(t['i'])==n for t in terminals)
    v=np.array([t['v'] for t in terminals]);i=np.array([t['i'] for t in terminals]);p=(v*i).sum(axis=0)
    c=dict(id=d['id']+f'_T{T}'+(f'_VIN{vin}' if vin else ''),model_id=d['id'],temp_C=T,vin_V=vin,
           x=x.tolist(),xlabel=xlabel,terminals=terminals,port_power_W=p.tolist(),extra=extra,metrics=metrics,
           kcl_max_A=float(np.abs(i.sum(axis=0)).max()),notes=notes,plots=plots or [])
    CASES.append(c);return c

def integrate(y,x):return np.r_[0,np.cumsum((np.asarray(y)[1:]+np.asarray(y)[:-1])*.5*np.diff(x))]
def fet(vd,vg,vt,beta,rs=0,n=1.5,T=25):
    """Smooth weak/strong inversion + series resistance, scalar bisection."""
    ut=KB*(T+273.15)/Q; eff=2*n*ut*np.logaddexp(0,(vg-vt)/(2*n*ut))
    lo=0.;hi=max(vd,0.)
    for _ in range(55):
        vi=(lo+hi)/2;ii=beta*(eff*vi-.5*vi*vi) if vi<eff else .5*beta*eff*eff
        if vi+ii*rs>vd:hi=vi
        else:lo=vi
    vi=(lo+hi)/2
    return float(max(0,beta*(eff*vi-.5*vi*vi) if vi<eff else .5*beta*eff*eff))
def diode(v,Is,n,rs,T):
    ut=KB*(T+273.15)/Q
    if v<=0:return Is*np.expm1(max(-700,v/(n*ut)))
    lo=0.;hi=v/rs
    for _ in range(60):
        i=(lo+hi)/2
        if n*ut*np.log1p(i/Is)+i*rs>v:hi=i
        else:lo=i
    return (lo+hi)/2

# Power devices: independent off-state C-V/leakage sweeps at each maximum input,
# plus low-VDS output characteristics. A 650 V assumption does NOT certify blocking.
powerdefs=[
 ('N01','SiC垂直MOSFET','vertical','P01 P02',dict(R25_ohm=.08,Vth_V=3,Beta_A_V2=2,gate_V=15,C0_F=400e-12,V0_V=20,m=.5,leak_25_A=1e-8)),
 ('N02','增强型GaN HEMT','hemt','P01 P25',dict(R25_ohm=.06,Vth_V=1.5,Beta_A_V2=3,gate_V=5,C0_F=180e-12,V0_V=15,m=.5,leak_25_A=2e-8,trap_amplitude=.5,trap_tau_s=4e-6)),
 ('N03','硅超结MOSFET','superjunction','P01',dict(R25_ohm=.10,Vth_V=3,Beta_A_V2=1.5,gate_V=10,C0_F=700e-12,V0_V=12,m=.65,leak_25_A=5e-9)),
 ('N04','IGBT','igbt','P02',dict(R25_ohm=.15,Vknee_V=.8,gate_V=15,C0_F=500e-12,V0_V=20,m=.5,leak_25_A=1e-8,tail_tau_s=.6e-6)),
 ('N05','SiC JBS整流二极管','jbs','P02',dict(Is25_A=1e-16,n=1.3,Rs_ohm=.15,C0_F=140e-12,V0_V=5,m=.5,leak_25_A=1e-8)),
]
for id,name,shape,papers,p in powerdefs:
    p['blocking_assumption_V']=650
    d=model(id,name,'功率器件',shape,papers,'C(V)=C0/(1+V/V0)^m；Q=∫C dV；Eoss=∫V C dV；关断漏电为线性假设',p,'外接功率器件研究对照；不能据此认定BCD平台支持。IGBT/650V器件并非40–150V的默认选型。')
    for T in TEMPS:
        for vin in VINS:
            v=np.linspace(0,vin,301);leak=p['leak_25_A']*2**((T-25)/25)*v/650
            cap=p['C0_F']/(1+v/p['V0_V'])**p['m'];q=integrate(cap,v);en=integrate(cap*v,v)
            ex=[tr('Coss/结电容','F',cap),tr('输出电荷','C',q),tr('电容储能','J',en)]
            met={'Vin_V':vin,'blocking_assumption_V':650,'blocking_ratio':vin/650,'Q_at_Vin_C':q[-1],'E_at_Vin_J':en[-1]}
            if id=='N05':
                vf=np.linspace(-1,2,301);If=np.array([diode(z,p['Is25_A']*2**((T-25)/12),p['n'],p['Rs_ohm']*(1+.003*(T-25)),T) for z in vf])
                plots=[plot('JBS正向特性（无少子存储模型）',vf,'VAK (V)','A',[('IA',If)])]
                terms=[terminal('K',v,leak,len(v)),terminal('A',0,-leak,len(v))]
            else:
                vf=np.linspace(0,3,301);r=p['R25_ohm']*(1+.004*(T-25))
                if id=='N04':If=np.maximum(vf-p['Vknee_V'],0)/r
                else:If=np.array([fet(z,p['gate_V'],p['Vth_V']-.0015*(T-25),p['Beta_A_V2']*(298.15/(T+273.15))**1.3,r,T=T) for z in vf])
                plots=[plot('低压导通特性（非SOA扫描）',vf,'VDS/VCE (V)','A',[('ID/IC',If)])]
                terms=[terminal('D' if id!='N04' else 'C',v,leak,len(v)),terminal('G',0,0,len(v)),terminal('S' if id!='N04' else 'E',0,-leak,len(v))]
                if id=='N02':
                    t=np.linspace(0,30e-6,301);rd=r*(1+p['trap_amplitude']*(vin/150)*(1-np.exp(-10e-6/2e-6))*np.exp(-t/p['trap_tau_s']))
                    plots += [plot('硬开关后动态Ron恢复（1A测试）',t*1e6,'t (us)','ohm',[('Rdyn',rd),('Rdc',np.full_like(t,r))]),plot('动态导通压降（ID=1A）',t*1e6,'t (us)','V',[('VDS',rd)])]
                    met['Rdyn_initial_ohm']=rd[0];met['Rdc_ohm']=r
                if id=='N04':
                    t=np.linspace(0,4e-6,401);tail=np.exp(-t/(p['tail_tau_s']*(1+.003*(T-25))))
                    plots += [plot('关断尾电流（外部VCE钳位）',t*1e6,'t (us)','A',[('IC_tail',tail)]),plot('关断尾部功率',t*1e6,'t (us)','W',[('P_tail',tail*vin)])]
                    met['tail_energy_J']=float(np.trapezoid(tail*vin,t))
            case(d,T,v,'关断电压 (V)',terms,ex,met,vin,notes='主图为关断扫描，门极为0V；附图独立施加导通门压。没有雪崩、破坏或SOA判断。',plots=plots)

fetdefs=[
 ('N06','FinFET','fin','P04',dict(vt=.35,beta=.003,rs=100,vgmax=1,vd=.7,n=1.1)),
 ('N07','a-IGZO TFT','tft','P05',dict(vt=1,beta=2e-5,rs=1000,vgmax=10,vd=1,n=2)),
 ('N08','有机聚合物TFT','organic','P06',dict(vt=2,beta=5e-6,rs=5000,vgmax=15,vd=1,n=2.5,strain=.3)),
 ('N09','MoS2接触受限FET','2d','P07',dict(vt=.6,beta=.001,rs=2000,vgmax=3,vd=.5,n=1.6)),
]
for id,name,shape,papers,p in fetdefs:
    d=model(id,name,'低压新型晶体管',shape,papers,'平滑有效过驱动u=2nUT·log(1+exp((VG−Vth)/2nUT))；沟道分段平方律＋串联接触电阻',p,'低压控制/传感研究；不接入40–150V开关节点；非BSIM/TCAD，FinFET只示意多栅器件端口。')
    for T in TEMPS:
        vg=np.linspace(-1,p['vgmax'],301);bt=p['beta']*(298.15/(T+273.15))**1.2; vt=p['vt']-.001*(T-25)
        if id=='N08':bt*=np.exp(-p['strain'])
        i=np.array([fet(p['vd'],g,vt,bt,p['rs'],p['n'],T) for g in vg]);gm=np.gradient(i,vg)
        ideal=np.array([fet(p['vd'],g,vt,bt,0,p['n'],T) for g in vg]); terms=[terminal('D',p['vd'],i,len(vg)),terminal('G',vg,0,len(vg)),terminal('S',0,-i,len(vg))]
        case(d,T,vg,'VG (V)',terms,[tr('gm','S',gm)],{'Imax_A':i[-1],'gmmax_S':max(gm),'Vth_V':vt},plots=[plot('接触电阻影响',vg,'VG (V)','A',[('含接触电阻',i),('零接触电阻参考',ideal)])])

d=model('N10','石墨烯双极性FET','低压新型晶体管','2d','P08','G=Gmin+k·sqrt((VG−VDirac)^2+Vs^2)；ID=G·VD',dict(Gmin_S=2e-5,k_S_V=8e-5,Vdirac_V=.4,Vs_V=.2,Vd_V=.1),'仅双极性电导示意；无带隙、量子霍尔和高场输运模型')
for T in TEMPS:
    g=np.linspace(-4,4,301);G=2e-5+8e-5*(298.15/(T+273.15))*np.sqrt((g-.4)**2+.2**2);i=G*.1
    case(d,T,g,'VG (V)',[terminal('D',.1,i,len(g)),terminal('G',g,0,len(g)),terminal('S',0,-i,len(g))],[tr('电导','S',G)],{'Imin_A':min(i),'on_off_ratio':max(i)/min(i)})

d=model('N11','碳纳米管弹道FET','低压新型晶体管','cnt','P19 P24','I=(4q²/h)·UT·[log(1+exp(ηS))−log(1+exp(ηD))]；ηS=(αVG−ΦB)/UT',dict(alpha=.8,barrier_eV=.25,Vd_V=.5,tubes=1),'单子带理想弹道示意；没有散射、接触肖特基势垒求解和真实CNT直径分布')
for T in TEMPS:
    g=np.linspace(-.5,1,301);ut=KB*(T+273.15)/Q;eta=(.8*g-.25)/ut;i=4*Q*Q/H*ut*(np.logaddexp(0,eta)-np.logaddexp(0,eta-.5/ut))
    case(d,T,g,'VG (V)',[terminal('D',.5,i,len(g)),terminal('G',g,0,len(g)),terminal('S',0,-i,len(g))],[tr('gm','S',np.gradient(i,g))],{'Imax_A':max(i),'conductance_quantum_S':4*Q*Q/H})

def triangular(duration,n,amplitude):
    t=np.linspace(0,duration,n);u=t/duration;v=np.interp(u,[0,.25,.5,.75,1],[0,amplitude,0,-amplitude,0]);return t,v

def relay_polarization(v,T):
    # Ensemble of deterministic coercive thresholds; initialization all negative.
    thresholds=np.linspace(.65,1.2,81)*(1-.001*(T-25));states=-np.ones(81);out=[]
    for z in v:
        states[z>thresholds]=1;states[z<-thresholds]=-1;out.append(np.mean(states))
    return np.array(out)

d=model('N12','FeFET铁电存储晶体管','非易失存储','fefet','P09','Vth=Vth0−ΔV·p；p由分布矫顽电压双稳态继电单元给出；ID=FET(VG,Vth)',dict(Vth0_V=.5,window_half_V=.35,beta=.002,Vd_V=.1,coercive_V=[.65,1.2],Cgate_F=1e-12,Qpolar_C=1e-12),'低压存储；率无关极化滞回，无畴动力学、保持/疲劳或概率开关预测')
for T in TEMPS:
    t,g=triangular(40e-6,1201,2);pol=relay_polarization(g,T);vt=.5-.35*pol;i=np.array([fet(.1,a,b,.002,T=T) for a,b in zip(g,vt)])
    charge=1e-12*g+1e-12*pol;ig=np.gradient(charge,t);terms=[terminal('D',.1,i,len(t)),terminal('G',g,ig,len(t)),terminal('S',0,-i-ig,len(t))]
    case(d,T,t*1e6,'t (us)',terms,[tr('归一化极化','1',pol),tr('Vth','V',vt)],{'memory_window_V':.7,'Ig_peak_A':max(abs(ig))},plots=[plot('FeFET滞回转移',g,'VG (V)','A',[('ID',i)])])

d=model('N13','氧化物RRAM','非易失存储','rram','P10 P19','G=Goff+(Gon−Goff)w；正向超过阈值dw/dt=k(V−Vset)(1−w)，反向复位；精确单步指数更新',dict(Goff_S=1e-6,Gon_S=1e-3,Vset_V=.8,Vreset_V=-.8,k_per_Vs=2e5,w0=.05),'低压双极性行为模型；无随机细丝、成形和耐久性预测')
for T in TEMPS:
    t,v=triangular(80e-6,1601,1.5);dt=t[1]-t[0];w=.05;ws=[];rate=2e5*np.exp(.003*(T-25))
    for z in v:
        if z>.8:w=1-(1-w)*np.exp(-rate*(z-.8)*dt)
        elif z<-.8:w=w*np.exp(-rate*(-z-.8)*dt)
        ws.append(w)
    ws=np.array(ws);G=1e-6+(1e-3-1e-6)*ws;i=v*G
    case(d,T,t*1e6,'t (us)',[terminal('TE',v,i,len(t)),terminal('BE',0,-i,len(t))],[tr('细丝状态w','1',ws),tr('G','S',G)],{'w_min':min(ws),'w_max':max(ws),'energy_J':float(np.trapezoid(v*i,t))},plots=[plot('RRAM I–V滞回',v,'V (V)','A',[('I',i)])])

def pcm_run(T,dt=1e-9):
    t=np.arange(0,2.0e-6+dt/2,dt);I=[];th=T+273.15;x=.85
    tv=[];xx=[];vv=[];loss=[];rth=1e6;cth=3e-13
    for k,tt in enumerate(t):
        R=1000*x+10000*(1-x)
        ii=3/R if tt<.35e-6 else (.20e-3 if .8e-6<tt<1.65e-6 else 0)
        v=ii*R;I.append(ii);tv.append(th);xx.append(x);vv.append(v);loss.append((th-(T+273.15))/rth)
        if k+1<len(t):
            th=(T+273.15)+(th-(T+273.15))*np.exp(-dt/(rth*cth))+ii*ii*R*rth*(1-np.exp(-dt/(rth*cth)))
            if th>900:x=x*np.exp(-dt/5e-9)
            elif 450<th<800:x=1-(1-x)*np.exp(-dt/80e-9)
    return t,np.array(I),np.array(vv),np.array(tv),np.array(xx),np.array(loss)
d=model('N14','PCM相变存储单元','非易失存储','pcm','P10','Cth dT/dt=I²R−(T−Ta)/Rth；晶态比例x决定R；热阈值控制结晶/熔融状态更新',dict(Rcrystal_ohm=1000,Ramorphous_ohm=10000,Rth_K_W=1e6,Cth_J_K=3e-13,Tmelt_K=900,Tcrystal_range_K=[450,800],reset_V=3,set_A=.0002),'RESET施加3V、SET施加0.2mA；低压电热相变行为；无潜热、成核或空间温度求解，热阈值不代表特定合金')
for T in TEMPS:
    t,i,v,th,x,loss=pcm_run(T)
    case(d,T,t*1e6,'t (us)',[terminal('TE',v,i,len(t)),terminal('BE',0,-i,len(t))],[tr('Tcell','K',th),tr('晶态比例x','1',x),tr('散热','W',loss)],{'Tmax_K':max(th),'final_crystalline_fraction':x[-1],'energy_J':float(np.trapezoid(v*i,t))})

d=model('N15','MTJ磁隧道结','非易失存储','mtj','P11','R=RP[1+TMR(1−m)/2]；超过正/负写入阈值时m切换；V=IR',dict(Rp_ohm=1000,TMR=1.0,Iwrite_A=.00015),'确定性双态读写；不实现LLG、热噪声、写入误码率和磁化空间纹理')
for T in TEMPS:
    t=np.linspace(0,1e-6,501);i=np.where(t<.2e-6,2e-5,np.where(t<.4e-6,2e-4,np.where(t<.6e-6,2e-5,np.where(t<.8e-6,-2e-4,2e-5))))
    m=-1.;ms=[];crit=.00015*(1-.001*(T-25))
    for z in i:
        if z>crit:m=1
        elif z<-crit:m=-1
        ms.append(m)
    ms=np.array(ms);r=1000*(1+.002*(T-25))*(1+(1-ms)/2);v=i*r
    case(d,T,t*1e9,'t (ns)',[terminal('TE',v,i,len(t)),terminal('BE',0,-i,len(t))],[tr('磁态m','1',ms),tr('R','ohm',r)],{'Rp_ohm':min(r),'Rap_ohm':max(r),'energy_J':float(np.trapezoid(v*i,t))})

d=model('N16','铁电电容','非易失存储','fecap','P09 P23','Q=Clinear·V+Qsat·p；I=dQ/dt，p由矫顽阈值分布给出',dict(Clinear_F=5e-12,Qsat_C=20e-12,coercive_V=[.65,1.2]),'双稳态极化示意；不是Landau–Khalatnikov或真实SrTiO3参数拟合')
for T in TEMPS:
    t,v=triangular(40e-6,1201,2);p=relay_polarization(v,T);q=5e-12*v+20e-12*p;i=np.gradient(q,t)
    c=case(d,T,t*1e6,'t (us)',[terminal('TE',v,i,len(t)),terminal('BE',0,-i,len(t))],[tr('Q','C',q),tr('归一化极化','1',p)],{'charge_change_C':q[-1]-q[0],'current_integral_C':float(np.trapezoid(i,t))},plots=[plot('极化滞回',v,'V (V)','C',[('Q',q)])])

for id,name,shape,paper,wl,Is,rs,eqe in [('N17','氮化物LED','led','P12',450e-9,1e-24,3,.35),('N18','量子点LED','qdled','P13',620e-9,1e-28,20,.1)]:
    d=model(id,name,'光电与能量转换',shape,paper,'V=nUT ln(1+I/Is)+I Rs；Popt=EQE(I)·I·hc/(qλ)，EQE带经验高注入衰减',dict(wavelength_m=wl,Is_A=Is,n=2,Rs_ohm=rs,EQE0=eqe,Idroop_A=.05),'仅电光端口模型；不模拟能带/光谱/激子或论文器件效率。')
    for T in TEMPS:
        i=np.linspace(0,.1,301);ut=KB*(T+273.15)/Q;v=2*ut*np.log1p(i/(Is*2**((T-25)/12)))+i*rs
        eff=eqe/(1+i/.05)*np.exp(-.002*(T-25));opt=eff*i*H*299792458/(Q*wl);p=v*i
        case(d,T,i*1e3,'驱动电流 (mA)',[terminal('A',v,i,len(i)),terminal('K',0,-i,len(i))],[tr('光功率','W',opt),tr('热耗散','W',p-opt),tr('EQE','1',eff)],{'Poptmax_W':max(opt),'energy_balance_min_W':min(p-opt)})

d=model('N19','PIN光电探测器','光电与能量转换','pin','P18','IA=−Idark−Responsivity·Popt；阶跃光流的一阶低通响应；反偏电容为常数',dict(responsivity_A_W=.7,dark_A=1e-9,tau_s=3e-9,bias_V=-3,Cj_F=.5e-12),'光输入到电流输出；不含倍增、量子噪声和波长依赖')
for T in TEMPS:
    t=np.linspace(0,100e-9,501);opt=np.where(t>=20e-9,1e-3,0.);resp=.7*(1-.0003*(T-25));iph=np.where(t>=20e-9,resp*1e-3*(1-np.exp(-np.maximum(t-20e-9,0)/3e-9)),0);i=-1e-9*2**((T-25)/15)-iph
    case(d,T,t*1e9,'t (ns)',[terminal('A',-3,i,len(t)),terminal('K',0,-i,len(t))],[tr('入射光功率','W',opt),tr('光生电流幅值','A',iph)],{'Iphoto_final_A':iph[-1],'bandwidth_Hz':1/(2*np.pi*3e-9)})

d=model('N20','单结光伏电池','光电与能量转换','pv','P14','Iout=Iph−I0[exp((V+Iout Rs)/(nUT))−1]−(V+Iout Rs)/Rsh；二分法求解',dict(Iph25_A=.025,I025_A=1e-12,n=1.4,Rs_ohm=1,Rsh_ohm=1000,Pin_W=.1),'电流进入器件为负表示发电；单二极管参数为假设，非特定钙钛矿/有机电池拟合')
for T in TEMPS:
    ut=KB*(T+273.15)/Q;i0=1e-12*2**((T-25)/8);iph=.025*(1+.0005*(T-25));v=np.linspace(0,1.3,401);out=[]
    for z in v:
        lo=-2.;hi=iph
        for _ in range(65):
            a=(lo+hi)/2;u=z+a;f=a-iph+i0*np.expm1(min(700,u/(1.4*ut)))+u/1000
            if f>0:hi=a
            else:lo=a
        out.append((lo+hi)/2)
    out=np.array(out);power=v*out;idx=int(np.argmax(power));ia=-out
    case(d,T,v,'输出端电压 (V)',[terminal('P',v,ia,len(v)),terminal('N',0,-ia,len(v))],[tr('输出电流','A',out),tr('输出功率','W',power)],{'Vmpp_V':v[idx],'Impp_A':out[idx],'Pmax_W':power[idx],'efficiency_assumed':power[idx]/.1})

d=model('N21','热电发电单元','光电与能量转换','teg','P15','V=α(Th−Tc)−IR；Qh=αTh I−I²R/2+KΔT；Qc=αTc I+I²R/2+KΔT',dict(alpha_V_K=.02,R_ohm=4,K_W_K=.02,deltaT_K=30),'定常集总热电转换；不含温度依赖材料系数或汤姆孙效应')
for T in TEMPS:
    tc=T+273.15;th=tc+30;i=np.linspace(0,.15,301);v=.6-4*i;qh=.02*th*i-2*i*i+.02*30;qc=.02*tc*i+2*i*i+.02*30;p=v*i
    case(d,T,i*1e3,'负载电流 (mA)',[terminal('P',v,-i,len(i)),terminal('N',0,i,len(i))],[tr('热端流入Qh','W',qh),tr('冷端流出Qc','W',qc),tr('输出功率','W',p)],{'Pmax_W':max(p),'heat_balance_max_W':max(abs(qh-qc-p))})

d=model('N22','片上耦合变压器','片上无源与互连','transformer','P16','Z1=R1+jωL1；Z2=R2+RL+jωL2；I1=V1/(Z1+ω²M²/Z2)；I2=−jωM I1/Z2',dict(L1_H=5e-9,L2_H=5e-9,k=.7,R1_ohm=2,R2_ohm=2,RL_ohm=50,Rsub_ohm=1000,Csub_F=100e-15,Vin_rms_V=1),'频域RMS相量；含基底并联RC；不是实际金属版图电磁提取')
for T in TEMPS:
    f=np.logspace(6,10,401);w=2*np.pi*f;r=2*(1+.0039*(T-25));M=.7*5e-9;z2=r+50+1j*w*5e-9;i1=1/(r+1j*w*5e-9+w*w*M*M/z2);i2=-1j*w*M*i1/z2;isub=1/1000+1j*w*100e-15;it=i1+isub;vo=-i2*50
    pin=np.real(it);pout=abs(i2)**2*50;loss=r*(abs(i1)**2+abs(i2)**2)+1/1000
    # Terminal arrays are real instantaneous values at phasor angle 0, not RMS magnitudes.
    terms=[terminal('P+',1,it.real,len(f)),terminal('P-',0,-it.real,len(f)),terminal('S+',vo.real,i2.real,len(f)),terminal('S-',0,-i2.real,len(f))]
    case(d,T,f,'频率 (Hz)',terms,[tr('Vout_rms','V',abs(vo)),tr('Iin_rms','A',abs(it)),tr('平均输入有功','W',pin),tr('平均输出有功','W',pout),tr('损耗','W',loss)],{'power_balance_max_W':max(abs(pin-pout-loss))},notes='端口表为相位0的实部瞬时值；RMS幅值和平均有功另列，勿把相量幅值相乘当有功。',plots=[plot('电压传递幅值',f,'f (Hz)','1',[('|Vout/Vin|',abs(vo))],True)])

d=model('N23','TSV硅通孔','片上无源与互连','tsv','P17','Vout=Vin/[1+(R+jωL)(G+jωC+1/RL)]；Iin=(Vin−Vout)/(R+jωL)',dict(R_ohm=.1,L_H=50e-12,C_F=50e-15,G_S=1e-6,RL_ohm=50,Vin_rms_V=1),'集总RLCG幅频模型；不做多TSV耦合、电磁传播和真实几何提取')
for T in TEMPS:
    f=np.logspace(6,11,401);w=2*np.pi*f;r=.1*(1+.0039*(T-25));z=r+1j*w*50e-12;y=1e-6+1j*w*50e-15+1/50;vo=1/(1+z*y);ii=vo*y;il=vo/50;isub=vo*(1e-6+1j*w*50e-15)
    pin=ii.real;pout=abs(vo)**2/50;loss=abs(ii)**2*r+abs(vo)**2*1e-6
    case(d,T,f,'频率 (Hz)',[terminal('IN',1,ii.real,len(f)),terminal('OUT',vo.real,-il.real,len(f)),terminal('SUB',0,-isub.real,len(f))],[tr('Vout_rms','V',abs(vo)),tr('Iin_rms','A',abs(ii)),tr('相移','deg',np.angle(vo,deg=True)),tr('平均输入有功','W',pin),tr('平均输出有功','W',pout)],{'power_balance_max_W':max(abs(pin-pout-loss))},notes='端口表取相位0瞬时实部；输出和基底支路同时纳入KCL。',plots=[plot('TSV传输',f,'f (Hz)','1',[('|H|',abs(vo))],True)])

d=model('N24','MZI电光调制器','光电与能量转换','mzi','P18','Pout=Pin·loss·[1+cos(πV/Vπ)]/2；Ig=C·dV/dt+V/Rleak',dict(Pin_W=.001,transmission=.5,Vpi_V=3,C_F=1e-12,Rleak_ohm=1e9,f_Hz=1e6),'集总相移/干涉模型；不求解波导光场、pn载流子或行波电极')
for T in TEMPS:
    t=np.linspace(0,2e-6,1001);v=1.5+1.5*np.sin(2*np.pi*1e6*t);i=1e-12*1.5*2*np.pi*1e6*np.cos(2*np.pi*1e6*t)+v/1e9;vpi=3*(1+.001*(T-25));po=.001*.5*(1+np.cos(np.pi*v/vpi))/2
    case(d,T,t*1e6,'t (us)',[terminal('G',v,i,len(t)),terminal('RET',0,-i,len(t))],[tr('光输出','W',po)],{'optical_min_W':min(po),'optical_max_W':max(po)},plots=[plot('MZI静态传输',v,'V (V)','W',[('Pout',po)])])

d=model('N25','半导体激光二极管','光电与能量转换','laser','P18','Pout=ηs·max(I−Ith(T),0)；Ith=Ith25·exp((T−25)/T0)；V=V0+IRs',dict(Ith25_A=.02,T0_K=100,slope_W_A=.5,V0_V=1.2,Rs_ohm=3),'静态L-I-V阈值模型；无速率方程、模式竞争、线宽或腔内场')
for T in TEMPS:
    i=np.linspace(0,.1,301);v=1.2+3*i;th=.02*np.exp((T-25)/100);opt=.5*np.maximum(i-th,0)
    case(d,T,i*1e3,'驱动电流 (mA)',[terminal('A',v,i,len(i)),terminal('K',0,-i,len(i))],[tr('光输出','W',opt),tr('热耗散','W',v*i-opt)],{'Ith_A':th,'Poptmax_W':max(opt)})

# Existing-device mechanism extensions, counted separately from the new families.
d=model('X01','MOS栅电荷与Miller耦合','已有器件扩展','mos','P04','[Cgs+Cgd,−Cgd;−Cgd,Cds+Cgd]·d[VG,VD]/dt=[(Vdrv−VG)/Rg, Iload−Ich]；后向欧拉＋Newton',dict(Cgs_F=1e-9,Cgd_F=.2e-9,Cds_F=.3e-9,Rg_ohm=10,Vdrv_V=5,Vbus_V=100,Iload_A=1,Vth_V=2,beta_A_V2=.5),'固定电容、1A钳位电感等效测试台；含Miller反馈但无栅电容非线性/封装寄生',kind='extension')
def gate_run(T,dt=1e-9):
    t=np.arange(0,1.2e-6+dt/2,dt);C=np.array([[1.2e-9,-.2e-9],[-.2e-9,.5e-9]]);z=np.array([0.,100.]);out=[];igs=[];ics=[];clamps=[];vt=2-.002*(T-25);b=.5*(298.15/(T+273.15))**1.5
    for k,tt in enumerate(t):
        vg,vd=z;drv=5 if .1e-6<=tt<.7e-6 else 0
        def channel(a,bv):
            u=max(a-vt,0);vv=max(bv,0);return b*(u*vv-.5*vv*vv) if vv<u else .5*b*u*u
        if k:
            prev=z.copy();z=prev.copy()
            for _ in range(30):
                vg,vd=z;u=max(vg-vt,0);vv=max(vd,0);ich=channel(vg,vd)
                dg=b*min(vv,u) if u>0 else 0;dd=b*max(u-vv,0) if vd>0 else 0
                F=C@(z-prev)/dt-np.array([(drv-vg)/10,1-ich]);J=C/dt+np.array([[.1,0],[dg,dd]])
                delta=np.linalg.solve(J,F);z-=delta
                if np.max(abs(delta))<1e-10:break
            if z[1]>100: # Ideal freewheel clamp; solve gate equation with VD fixed.
                z[1]=100;z[0]=(drv/10+(1.2e-9*prev[0]+.2e-9*(100-prev[1]))/dt)/(.1+1.2e-9/dt)
            deriv=(z-prev)/dt;caps=C@deriv;ig=(drv-z[0])/10;ic=channel(*z);clamp=1-ic-caps[1]
        else:ig=0;ic=0;clamp=1
        out.append(z.copy());igs.append(ig);ics.append(ic);clamps.append(clamp)
    return t,np.array(out),np.array(igs),np.array(ics),np.array(clamps)
for T in TEMPS:
    t,z,ig,ic,cl=gate_run(T); # Device total drain current = channel + displacement = Iload - external clamp.
    it=1-cl;terms=[terminal('D',z[:,1],it,len(t)),terminal('G',z[:,0],ig,len(t)),terminal('S',0,-it-ig,len(t))]
    case(d,T,t*1e9,'t (ns)',terms,[tr('沟道电流','A',ic),tr('外部钳位电流','A',cl)],{'Vgsmax_V':max(z[:,0]),'Vdsmax_V':max(z[:,1]),'channel_energy_J':float(np.trapezoid(z[:,1]*ic,t))},notes='端口电流含位移电流。钳位支路位于外部测试台，单独显示。')

d=model('X02','PN二极管反向恢复','已有器件扩展','diode','P02','外部规定dI/dt；三角形恢复电流满足Qrr=Irr·trr/2，trr=2sqrt(Qrr/a)',dict(Qrr25_C=50e-9,di_dt_A_s=5e7,Vreverse_V=100),'电荷约束行为模型；Qrr为输入假设，无少子连续性方程或实测恢复数据',kind='extension')
for T in TEMPS:
    qr=50e-9*(1+.003*(T-25));a=5e7;ta=np.sqrt(qr/a);t=np.linspace(-ta,3*ta,801);i=np.where(t<0,-a*t,np.where(t<ta,-a*t,np.where(t<2*ta,-a*(2*ta-t),0)));v=np.where(t<ta,.8,-100)
    case(d,T,t*1e9,'t (ns)',[terminal('A',v,i,len(t)),terminal('K',0,-i,len(t))],[],{'Qrr_assumed_C':qr,'Qrr_integrated_C':float(-np.trapezoid(np.minimum(i,0),t)),'Irr_A':a*ta,'trr_s':2*ta})

d=model('X03','MOS导通损耗自热反馈','已有器件扩展','vertical','P02 P19','Cth dθ/dt=I²R25[1+α(Ta+θ−25)]−θ/Rth；恒流一阶闭式解',dict(I_A=2,R25_ohm=.2,alpha_K_inv=.004,Rth_K_W=40,Cth_J_K=.02),'单节点热RC与电阻反馈；不是器件内部三维温度场或热失效寿命',kind='extension')
for T in TEMPS:
    t=np.linspace(0,4,801);p0=4*.2*(1+.004*(T-25));k=1/40-4*.2*.004;theta=p0/k*(1-np.exp(-k*t/.02));v=2*.2*(1+.004*(T+theta-25));i=np.full_like(t,2.)
    deriv=p0/.02*np.exp(-k*t/.02);res=.02*deriv+theta/40-v*i
    case(d,T,t,'t (s)',[terminal('D',v,i,len(t)),terminal('G',5,0,len(t)),terminal('S',0,-i,len(t))],[tr('Tj','°C',T+theta),tr('流向环境热功率','W',theta/40)],{'Tj_final_C':T+theta[-1],'thermal_balance_max_W':max(abs(res)),'stable_feedback':k>0})

d=model('X04','PMOS NBTI老化','已有器件扩展','mos','P20','Δ|Vth|=A·exp[(Ea/k)(1/Tref−1/T)]·(t/tref)^n；|ID|∝max(VSG−|Vth|,0)^2',dict(A_V=.02,Ea_eV=.1,Tref_K=398.15,tref_s=1000,n=.2,Vsg_V=3.3,Vth0_V=.7,beta_A_V2=.01),'经验幂律定压应力；不解反应扩散，不含恢复/工艺标定，不作寿命预测',kind='extension')
for T in TEMPS:
    t=np.logspace(-3,6,301);dv=.02*np.exp(.1/(KB/Q)*(1/398.15-1/(T+273.15)))*(t/1000)**.2;i=.5*.01*np.maximum(3.3-.7-dv,0)**2
    case(d,T,t,'应力时间 (s)',[terminal('D',-1,-i,len(t)),terminal('G',-3.3,0,len(t)),terminal('S',0,i,len(t))],[tr('阈值退化','V',dv)],{'deltaVth_final_V':dv[-1],'Id_retention':i[-1]/(.5*.01*2.6**2)})

d=model('X05','MOS 1/f与热噪声','已有器件扩展','mos','P21','Si(f)=Kf/f+4kTγgm；irms²=Kf ln(f2/f1)+4kTγgm(f2−f1)',dict(Kf_A2=1e-18,gm_S=.001,gamma=2/3,fmin_Hz=1,fmax_Hz=1e6),'频域PSD与积分；不伪造时间随机波形或陷阱密度；端口为DC偏置',kind='extension')
for T in TEMPS:
    f=np.logspace(0,6,601);white=4*KB*(T+273.15)*(2/3)*.001;psd=1e-18/f+white;integ=1e-18*np.log(1e6)+white*(1e6-1)
    case(d,T,f,'频率 (Hz)',[terminal('D',1,.001,len(f)),terminal('G',1,0,len(f)),terminal('S',0,-.001,len(f))],[tr('Si','A²/Hz',psd),tr('电流噪声幅谱','A/√Hz',np.sqrt(psd))],{'integrated_noise_A_rms':np.sqrt(integ),'numerical_noise_A_rms':np.sqrt(np.trapezoid(psd,f))},plots=[plot('电流噪声幅谱',f,'f (Hz)','A/√Hz',[('sqrt(Si)',np.sqrt(psd))],True)])

d=model('X06','MOS阈值及电阻统计分散','已有器件扩展','fin','P22','固定随机种子；Vth~N(μ,σ)，R为正值对数正态；每样本求解独立FET偏置点',dict(seed=20261101,samples=1000,sigma_Vth_V=.03,R_median_ohm=100,R_log_sigma=.1,Vd_V=.7,Vg_V=1),'参数Monte Carlo；不复现论文LER/离散掺杂的3D随机几何，不给制造良率',kind='extension')
for T in TEMPS:
    rng=np.random.default_rng(20261101);vt=rng.normal(.35-.001*(T-25),.03,1000);r=rng.lognormal(np.log(100),.1,1000);i=np.array([fet(.7,1,a,.003*(298.15/(T+273.15))**1.2,b,T=T) for a,b in zip(vt,r)]);x=np.arange(1,1001)
    case(d,T,x,'样本编号',[terminal('D',.7,i,len(x)),terminal('G',1,0,len(x)),terminal('S',0,-i,len(x))],[tr('Vth','V',vt),tr('Rseries','ohm',r)],{'I_mean_A':np.mean(i),'I_std_A':np.std(i,ddof=1),'I_p05_A':np.quantile(i,.05),'I_p95_A':np.quantile(i,.95),'samples':1000})

# Independent physical invariants and discretization checks, not just finite-output assertions.
def check(name,value,limit,ok):CHECKS.append(dict(test=name,value=float(value),limit=float(limit),pass_=bool(ok)))
check('新增模型数',sum(m['kind']=='new' for m in MODELS),25,sum(m['kind']=='new' for m in MODELS)==25)
check('扩展效应数',sum(m['kind']=='extension' for m in MODELS),6,sum(m['kind']=='extension' for m in MODELS)==6)
check('新增测试台工况数',len(CASES),168,len(CASES)==168)
check('端口KCL最大残差(A)',max(c['kcl_max_A'] for c in CASES),1e-12,max(c['kcl_max_A'] for c in CASES)<1e-12)
bad=0
for c in CASES:
    arrays=[c['x'],c['port_power_W']]+[t[k] for t in c['terminals'] for k in ['v','i']]+[a['y'] for a in c['extra']]
    arrays += [a['x'] for a in c['plots']]+[s['y'] for a in c['plots'] for s in a['series']]
    bad+=sum(not np.isfinite(a).all() for a in arrays)
check('非有限数组数',bad,0,bad==0)
for id,key,limit in [('N21','heat_balance_max_W',1e-12),('N22','power_balance_max_W',1e-12),('N23','power_balance_max_W',1e-12),('X03','thermal_balance_max_W',1e-12)]:
    val=max(c['metrics'][key] for c in CASES if c['model_id']==id);check(id+'能量平衡残差(W)',val,limit,val<limit)
qrerr=max(abs(c['metrics']['Qrr_integrated_C']/c['metrics']['Qrr_assumed_C']-1) for c in CASES if c['model_id']=='X02');check('恢复电荷积分相对误差',qrerr,1e-5,qrerr<1e-5)
qerr=max(abs(c['metrics']['charge_change_C']-c['metrics']['current_integral_C']) for c in CASES if c['model_id']=='N16');check('铁电电荷守恒残差(C)',qerr,1e-18,qerr<1e-18)
noiseerr=max(abs(c['metrics']['numerical_noise_A_rms']/c['metrics']['integrated_noise_A_rms']-1) for c in CASES if c['model_id']=='X05');check('噪声积分相对误差',noiseerr,.001,noiseerr<.001)
t1,z1,*_=gate_run(25,1e-9);t2,z2,*_=gate_run(25,.5e-9);gateerr=max(abs(z1[:,1]-z2[::2,1]));check('门极瞬态dt减半最大VDS差(V)',gateerr,1,gateerr<1)
_,_,_,th1,xx1,_=pcm_run(25,1e-9);_,_,_,th2,xx2,_=pcm_run(25,.5e-9);pcmerr=abs(th1.max()-th2.max())/th2.max();check('PCM dt减半峰温相对差',pcmerr,.03,pcmerr<.03)
states=[a['y'] for c in CASES if c['model_id'] in ['N13','N14'] for a in c['extra'] if a['name'] in ['细丝状态w','晶态比例x']];check('状态变量[0,1]越界数',sum(min(a)<0 or max(a)>1 for a in states),0,all(min(a)>=0 and max(a)<=1 for a in states))

data=dict(version='2.0',date='2026-11-01',models=MODELS,cases=CASES,checks=CHECKS,
          convention='所有电流定义为流入器件为正；端口功率ΣVI为吸收功率，储能/光/热/负载功率单独列示。',
          limitation='论文识别器件与机制；全部参数为示意假设。未执行SPICE/TCAD、PDK签核或论文曲线拟合。')
(OUT/'simulation_v2.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf-8')
(OUT/'validation.json').write_text(json.dumps(CHECKS,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'models/model_catalog.json').write_text(json.dumps(MODELS,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'case_summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['case_id','model_id','temperature_C','Vin_V','points','max_abs_V','max_abs_I_A','max_abs_port_power_W','KCL_residual_A','metrics_json'])
    for c in CASES:w.writerow([c['id'],c['model_id'],c['temp_C'],c['vin_V'],len(c['x']),max(abs(v) for t in c['terminals'] for v in t['v']),max(abs(i) for t in c['terminals'] for i in t['i']),max(abs(p) for p in c['port_power_W']),c['kcl_max_A'],json.dumps(c['metrics'],ensure_ascii=False)])
print(json.dumps({'models':len(MODELS),'cases':len(CASES),'checks':CHECKS},ensure_ascii=False))
if not all(c['pass_'] for c in CHECKS):raise SystemExit('Validation failed; inspect results/validation.json')
