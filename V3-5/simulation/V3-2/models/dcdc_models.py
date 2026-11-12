"""Reduced DC/DC mechanisms. All device coefficients are illustrative assumptions.

No foundry PDK, extracted parasitics, measured-fit model or transistor-level signoff.
Each function states whether it solves an ODE, an analytical waveform or a ledger.
"""
import numpy as np

VINS=(40,60,80,100,120,150)
TEMPS=(-40,25,125)
FS=250e3

def resistance(temp_c,base=.18):
    return base*(1+.004*(temp_c-25))

def capacitance(v,c0=600e-12,v0=20.,m=.5):
    v=np.asarray(v,dtype=float)
    if np.any(v<0):raise ValueError('Capacitance law requires nonnegative reverse voltage')
    return c0/(1+v/v0)**m

def capacitor_charge(v,c0=600e-12,v0=20.,m=.5):
    v=np.asarray(v,dtype=float)
    if m==1:return c0*v0*np.log1p(v/v0)
    return c0*v0*((1+v/v0)**(1-m)-1)/(1-m)

def capacitor_energy(v,c0=600e-12,v0=20.,m=.5):
    if m in (1,2):raise ValueError('This analytical integral excludes m=1 or 2')
    u=1+np.asarray(v,dtype=float)/v0
    return c0*v0*v0*((u**(2-m)-1)/(2-m)-(u**(1-m)-1)/(1-m))

def _q_inverse(q,c0=80e-12,v0=20.):
    return v0*((1+np.asarray(q)/(2*c0*v0))**2-1)

def gate_switch(vin=100.,temp_c=25.,points=121):
    """Prescribed load-current commutation with nonlinear Miller charge.

    Channel current excludes Coss and diode-recovery current. The excess
    channel-overlap integral subtracts instantaneous I**2*Ron baseline.
    Gate and drain waveforms are reduced stages, not a coupled MOS solution.
    """
    vdrv=10.;cgs=800e-12;rgon=8.;rgoff=5.;gm=.5;iload=1.
    vth=2.2-.002*(temp_c-25);plateau=vth+iload/gm;ron=resistance(temp_c)
    von=iload*ron;tauon=rgon*cgs;tauoff=rgoff*cgs
    tpre=-tauon*np.log(1-plateau/vdrv)
    qlo=capacitor_charge(von,80e-12);qhi=capacitor_charge(vin,80e-12)
    qgd=qhi-qlo;igon=(vdrv-plateau)/rgon;igoff=plateau/rgoff
    ton=qgd/igon;toff=qgd/igoff
    # Each boundary is represented twice to preserve algebraic jumps.
    a=np.sort(np.r_[np.linspace(0,tpre,points),-tauon*np.log(1-vth/vdrv)])
    vg1=vdrv*(1-np.exp(-a/tauon));i1=np.clip(gm*(vg1-vth),0,iload)
    b=np.linspace(0,ton,points);vd2=_q_inverse(qhi-igon*b)
    c=np.linspace(0,5*tauon,points);vg3=vdrv-(vdrv-plateau)*np.exp(-c/tauon)
    t_on=np.r_[a,tpre+b,tpre+ton+c]
    vg_on=np.r_[vg1,np.full(points,plateau),vg3]
    vd_on=np.r_[np.full(len(a),vin),vd2,np.full(points,von)]
    id_on=np.r_[i1,np.full(2*points,iload)]
    ig_on=np.r_[(vdrv-vg1)/rgon,np.full(points,igon),(vdrv-vg3)/rgon]
    delay=tauoff*np.log(vdrv/plateau)
    a=np.linspace(0,delay,points);vg1=vdrv*np.exp(-a/tauoff)
    b=np.linspace(0,toff,points);vd2=_q_inverse(qlo+igoff*b)
    c=np.sort(np.r_[np.linspace(0,6*tauoff,points),tauoff*np.log(plateau/vth)])
    vg3=plateau*np.exp(-c/tauoff);i3=np.clip(gm*(vg3-vth),0,iload)
    t_off=np.r_[a,delay+b,delay+toff+c]
    vg_off=np.r_[vg1,np.full(points,plateau),vg3]
    vd_off=np.r_[np.full(points,von),vd2,np.full(len(c),vin)]
    id_off=np.r_[np.full(2*points,iload),i3]
    ig_off=np.r_[-vg1/rgoff,np.full(points,-igoff),-vg3/rgoff]
    p_on=np.maximum(vd_on*id_on-ron*id_on**2,0)
    p_off=np.maximum(vd_off*id_off-ron*id_off**2,0)
    return dict(t_on=t_on,vg_on=vg_on,vd_on=vd_on,id_on=id_on,ig_on=ig_on,p_on=p_on,
                t_off=t_off,vg_off=vg_off,vd_off=vd_off,id_off=id_off,ig_off=ig_off,p_off=p_off,
                metrics=dict(Miller_charge_C=float(qgd),Miller_on_duration_s=float(ton),Miller_off_duration_s=float(toff),
                plateau_V=float(plateau),channel_overlap_on_J=float(np.trapezoid(p_on,t_on)),channel_overlap_off_J=float(np.trapezoid(p_off,t_off)),
                gate_charge_C=float(cgs*vdrv+qgd),Qoss_C=float(capacitor_charge(vin)),Eoss_J=float(capacitor_energy(vin))))

def recovery_pulse(vin=100.,temp_c=25.,points=201):
    """Imposed triangular stored-charge recovery; no minority-carrier PDE."""
    qrr=12e-9*(1+.005*(temp_c-25));trr=60e-9*(1+.002*(temp_c-25));fraction=.35
    t=np.r_[np.linspace(0,fraction*trr,points),np.linspace(fraction*trr,trr,points)]
    peak=2*qrr/trr
    irr=np.where(t<=fraction*trr,peak*t/(fraction*trr),peak*(trr-t)/((1-fraction)*trr))
    irr=np.maximum(irr,0)
    return dict(t=t,irr=irr,qrr=qrr,trr=trr,peak=peak,commutation_estimate_J=vin*qrr)

def deadtime_buck(vin=100.,temp_c=25.,dead_s=40e-9,points_per_phase=101):
    """Exact periodic ideal CCM teaching waveform with two diode dead times.

    Recovery is a separate imposed pulse and is NOT added to inductor current.
    No ringing, finite gate transition or Coss commutation in this waveform.
    """
    period=1/FS;vout=12.;l=100e-6;vf=.8-.001*(temp_c-25);mean_i=1.
    duty=(vout+2*dead_s/period*vf)/vin
    durations=[duty*period,dead_s,(1-duty)*period-2*dead_s,dead_s]
    if min(durations)<0:raise ValueError('Dead time exceeds available off interval')
    switches=[vin,-vf,0.,-vf];t=[];raw=[];sw=[];states=[];now=0.;curr=0.
    for k,(duration,voltage)in enumerate(zip(durations,switches)):
        local=np.linspace(0,duration,points_per_phase)
        t.extend(now+local);raw.extend(curr+(voltage-vout)/l*local)
        sw.extend(np.full(points_per_phase,voltage));states.extend(np.full(points_per_phase,k))
        curr+=(voltage-vout)/l*duration;now+=duration
    t=np.array(t);raw=np.array(raw);sw=np.array(sw);states=np.array(states)
    il=raw+mean_i-np.trapezoid(raw,t)/period;hs=(states==0);ls=(states==2);dead=(states==1)|(states==3)
    id_forward=np.where(dead,il,0.);diode_power=vf*id_forward
    return dict(t_s=t,state_HS_on=hs.astype(float),state_LS_on=ls.astype(float),state_deadtime=dead.astype(float),
                Vsw_V=sw,Vout_V=np.full_like(t,vout),IL_A=il,Idiode_forward_A=id_forward,Pdiode_W=diode_power,
                parameters=dict(Vin_V=vin,Vout_V=vout,temperature_C=temp_c,fs_Hz=FS,period_s=period,L_H=l,Iout_A=mean_i,deadtime_s=dead_s,Vf_V=vf,duty_fraction=duty,edge_times_s=np.r_[0,np.cumsum(durations)].tolist()),
                metrics=dict(duty_fraction=duty,minimum_IL_A=float(min(il)),ripple_IL_A=float(np.ptp(il)),mean_IL_A=float(np.trapezoid(il,t)/period),
                             diode_deadtime_loss_W=float(np.trapezoid(diode_power,t)/period),volt_second_residual_Vs=float(np.trapezoid(sw-vout,t)),periodic_current_residual_A=float(curr)))

def bootstrap(vin=100.,temp_c=25.,cboot=100e-9,cycles=12,points=61):
    """Bootstrap capacitor with exact on-discharge/off-RC-recharge steps.

    Each gate event removes Qg impulsively, with duplicate-time samples.
    UVLO is reported, not coupled to PWM logic in this isolated sizing bench.
    """
    period=1/FS;duty=12/vin;ton=duty*period;toff=(1-duty)*period
    vs=10.-.65;rq=10.;iq=100e-6*(1+.003*(temp_c-25));qg=gate_switch(vin,temp_c)['metrics']['gate_charge_C']
    v=vs;t=[];vb=[];ich=[];idr=[];uv=[];now=0.
    for cycle in range(cycles):
        t.extend([now,now]);vb.extend([v,v-qg/cboot]);ich.extend([0,0]);idr.extend([0,0]);uv.extend([v<6,v-qg/cboot<6]);v-=qg/cboot
        x=np.linspace(0,ton,points);vals=v-iq*x/cboot
        t.extend(now+x);vb.extend(vals);ich.extend(np.zeros(points));idr.extend(np.full(points,iq));uv.extend(vals<6);v=vals[-1];now+=ton
        x=np.linspace(0,toff,points);veq=vs-iq*rq;vals=veq+(v-veq)*np.exp(-x/(rq*cboot));charge=(vs-vals)/rq
        t.extend(now+x);vb.extend(vals);ich.extend(charge);idr.extend(np.full(points,iq));uv.extend(vals<6);v=vals[-1];now+=toff
    # Exact steady-state map, independently useful for capacitor sizing.
    a=np.exp(-toff/(rq*cboot));drop=(qg+iq*ton)/cboot
    pre=(vs-iq*rq)-a*drop/(1-a);minimum=pre-drop
    return dict(t=np.array(t),vbs=np.array(vb),icharge=np.array(ich),idriver=np.array(idr),uvlo=np.array(uv,dtype=float),
                metrics=dict(Cboot_F=cboot,Qgate_C=qg,steady_pre_gate_V=float(pre),steady_min_V=float(minimum),minimum_simulated_V=float(min(vb)),
                             steady_droop_V=float(drop),UVLO_margin_V=float(minimum-6),last_cycle_min_V=float(min(vb[-(2+2*points):])),gate_impulse_charge_C=qg))

def level_shift(vin=100.,dvdt=10e9,points=1001,receiver_r=20e3):
    """RC receiver disturbance from Ccm*dVcm/dt; no latch topology invented."""
    ccm=30e-15;crx=200e-15;r=receiver_r;tau=r*(ccm+crx);rise=vin/dvdt
    npre=max(3,points//3);npost=max(3,points-npre)
    t=np.r_[np.linspace(0,rise,npre),np.linspace(rise,10*tau+rise,npost)]
    during=np.r_[np.ones(npre,dtype=bool),np.zeros(npost,dtype=bool)];vinj=ccm*dvdt*r
    peak=vinj*(1-np.exp(-rise/tau))
    rx=np.where(during,vinj*(1-np.exp(-t/tau)),peak*np.exp(-(t-rise)/tau))
    cm=np.minimum(dvdt*t,vin);iin=np.where(during,ccm*dvdt,0.)
    return dict(t=t,cm=cm,rx=rx,iinj=iin,ir=rx/r,
                metrics=dict(common_mode_slew_V_per_s=dvdt,rise_time_s=rise,peak_receiver_disturbance_V=float(peak),
                             comparator_noise_margin_V=float(.7-peak),threshold_crossed=int(peak>=.7),Ccm_F=ccm,receiver_tau_s=tau,receiver_R_ohm=r))

def current_sense(temp_c=25.,dt=2e-9,end=2e-6):
    """One-pole current-sense amplifier, deterministic offset and delay comparator."""
    t=np.arange(round(end/dt)+1)*dt;step=100e-9;rs=.05*(1+100e-6*(temp_c-25));gain=20.;tau=100e-9;offset=1e-3+5e-6*(temp_c-25)
    cur=np.where(t<step,.5,3.);x=gain*rs*cur+offset
    out=x[0]+(x[-1]-x[0])*(1-np.exp(-np.maximum(t-step,0)/tau));threshold=2.;delay=35e-9
    crossing=step-tau*np.log((x[-1]-threshold)/(x[-1]-x[0]));trip=(t>=crossing+delay)
    return dict(t=t,load=cur,vsense=rs*cur,out=out,trip=trip.astype(float),
                metrics=dict(sense_resistance_ohm=rs,amplifier_offset_V=offset,nominal_trip_current_A=float((threshold-offset)/(gain*rs)),
                             analog_crossing_time_s=float(crossing),trip_time_s=float(crossing+delay),response_delay_s=float(crossing+delay-step),sense_loss_at_1A_W=rs))

def startup_uvlo(vin=100.,temp_c=25.,dt=2e-6,end=.040):
    """Current-limited HV startup source feeding Caux with hysteretic UVLO.

    Source stays on; loads differ in UVLO states. A short imposed loss of
    auxiliary support demonstrates brownout/restart, not an IC startup circuit.
    """
    t=np.arange(round(end/dt)+1)*dt;c=1e-6;limit=11.;on=9.;off=7.
    istart=1e-3*(1+.001*(temp_c-25));ioff=40e-6;irun=500e-6
    v=np.zeros_like(t);enabled=np.zeros_like(t);src=np.zeros_like(t);load=np.zeros_like(t);clamp=np.zeros_like(t);state=False
    for k in range(len(t)-1):
        if not state and v[k]>=on:state=True
        elif state and v[k]<=off:state=False
        enabled[k]=state
        source=0. if .014<=t[k]<.024 else istart
        source=min(source,max(vin-v[k],0)/20000) # simple source compliance
        demand=irun if state else ioff
        next_v=max(0,min(limit,v[k]+(source-demand)*dt/c))
        src[k]=source;load[k]=demand;clamp[k]=max(0,source-demand-c*(next_v-v[k])/dt)
        v[k+1]=next_v
    enabled[-1]=enabled[-2];src[-1]=src[-2];load[-1]=load[-2];clamp[-1]=clamp[-2]
    p_source=(vin-v)*src;pin=vin*src;p_load=v*load;p_clamp=v*clamp
    edges=np.flatnonzero(np.diff(enabled)>0);fall=np.flatnonzero(np.diff(enabled)<0)
    return dict(t=t,vaux=v,enabled=enabled,isource=src,iload=load,iclamp=clamp,source_loss=p_source,
                metrics=dict(first_enable_s=float(t[edges[0]+1])if len(edges)else-1,enable_events=int(len(edges)),brownout_events=int(len(fall)),
                             peak_source_dissipation_W=float(max(p_source)),peak_Vaux_V=float(max(v)),start_current_limit_A=istart,
                             source_compliance_resistance_ohm=20000.))

def ringing(vin=100.,damping='damped',points=1501):
    """Free response of a SERIES RLC parasitic surrogate around a DC bus.

    Rcritical=2*sqrt(L/C); this is not a literal shunt RC snubber network.
    Stored-energy decay is exact. No driven switching loss is inferred.
    """
    if damping not in ['weak','damped']:raise ValueError('Choose weak or damped series resistance')
    l=15e-9;c=float(capacitance(vin));critical=2*np.sqrt(l/c);r=.8 if damping=='weak'else .8*critical
    wn=1/np.sqrt(l*c);alpha=r/(2*l);wd=np.sqrt(wn*wn-alpha*alpha)
    t=np.linspace(0,400e-9,points);v0=.15*vin
    v=v0*np.exp(-alpha*t)*(np.cos(wd*t)+alpha/wd*np.sin(wd*t))
    # State convention: C dv/dt = i; L di/dt = -v-Ri.
    i=-v0*np.exp(-alpha*t)*wn*wn/wd*np.sin(wd*t)*c
    e=.5*c*v*v+.5*l*i*i;p=r*i*i
    return dict(t=t,v=vin+v,i=i,energy=e,loss=p,
                metrics=dict(Lpar_H=l,Clinearized_F=c,Rseries_ohm=r,Rcritical_series_ohm=float(critical),damping_ratio=float(alpha/wn),
                             peak_Vsw_V=float(max(v+vin)),initial_ring_energy_J=float(e[0]),energy_residual_J=float(np.trapezoid(p,t)-(e[0]-e[-1]))))

def coss_hard_commutation(vin):
    """Matched half-bridge capacitances, one hard upper turn-on.

    Upper Coss releases its stored energy. The bus supplies Vin*Qoss to
    charge lower Coss; subtract its final stored energy for charging loss.
    The opposite edge is assumed to redistribute charge without dissipation.
    No diode recovery, load-current overlap or ringing is embedded here.
    """
    stored=float(capacitor_energy(vin));source=vin*float(capacitor_charge(vin))
    return dict(Coss_upper_discharge_J=stored,Coss_lower_charging_loss_J=source-stored,
                Coss_hard_commutation_J=source)

def loss_budget(vin=100.,ambient_c=25.):
    """Separated loss estimates, with a self-consistent effective hot node.

    Two matched MOS Coss curves give Eupper+(Vin*Qlower-Elower)=Vin*Qoss
    loss at one hard upper turn-on per cycle; the other edge is ideal.
    Channel overlap excludes displacement/recovery currents. Vin*Qrr is a
    prescribed conservative bus-energy estimate, not diode heat extraction.
    All heat shares ONE illustrative node; it is not any device's junction.
    """
    fs=FS;rth=8.;cth=.025;iout=1.;vout=12.;coss=coss_hard_commutation(vin)
    def parts(tj):
        gate=gate_switch(vin,tj,points=81)['metrics'];dead=deadtime_buck(vin,tj,points_per_phase=31)
        irms2=float(np.trapezoid(dead['IL_A']**2,dead['t_s'])*fs)
        duty=dead['parameters']['duty_fraction'];qrr=recovery_pulse(vin,tj)['qrr']
        return dict(high_side_conduction_W=irms2*resistance(tj)*duty,
                    low_side_conduction_W=irms2*resistance(tj)*(1-duty-2*40e-9*fs),
                    inductor_copper_W=irms2*resistance(tj,.12),
                    channel_overlap_W=(gate['channel_overlap_on_J']+gate['channel_overlap_off_J'])*fs,
                    Coss_commutation_W=coss['Coss_hard_commutation_J']*fs,
                    recovery_bus_estimate_W=vin*qrr*fs,
                    gate_driver_supply_W=2*gate['gate_charge_C']*10*fs,
                    deadtime_diode_W=dead['metrics']['diode_deadtime_loss_W'],
                    assumed_control_supply_W=.01)
    tj=ambient_c
    for _ in range(80):
        losses=parts(tj);new=ambient_c+rth*sum(losses.values())
        if abs(new-tj)<1e-10:break
        tj=.5*(tj+new)
    total=sum(parts(tj).values());t=np.linspace(0,1.,801);temperature=ambient_c+total*rth*(1-np.exp(-t/(rth*cth)))
    # Transient uses the converged constant loss, not fully coupled P(T(t)).
    return dict(t=t,temperature=temperature,parts=parts(tj),
                metrics=dict(total_loss_W=float(total),estimated_efficiency=float(vout*iout/(vout*iout+total)),steady_hot_node_C=float(tj),
                             thermal_fixed_point_residual_K=float(tj-ambient_c-rth*total),Rtheta_K_per_W=rth,Ctheta_J_per_K=cth,
                             parameter_temperature_range_exceeded=int(tj>175 or tj<-40),**coss))

def controlled_buck(vin=100.,temp_c=25.,dt=1e-6,end=.008,save_stride=10):
    """Averaged 2-state buck with PI outer loop and finite-bandwidth current command.

    Duty is a continuous averaged control variable. A current-reference ceiling
    is not cycle-by-cycle peak current protection. No switching waveforms or
    P08 switching-loss terms are injected into this controller simulation.
    """
    n=round(end/dt);t=np.arange(n+1)*dt;state=np.zeros((n+1,3));duty=np.zeros(n+1);iref=np.zeros(n+1)
    l=100e-6;c=22e-6;rtot=resistance(temp_c,.30);kp=.25;ki=350.;wcurrent=2*np.pi*12000;limit=1.6
    ref=np.minimum(12.,12*t/.002);rload=np.where(t<.004,12.,6.)
    def derivative(z,vr,r):
        current,vout,integ=z;error=vr-vout;raw=kp*error+integ;icmd=np.clip(raw,0,limit)
        d=np.clip((vout+rtot*current+l*wcurrent*(icmd-current))/vin,0,.90)
        di=(d*vin-rtot*current-vout)/l;dv=(current-vout/r)/c
        # Conditional integration anti-windup is frozen when saturation worsens.
        dint=ki*error if (0<raw<limit) or (raw>=limit and error<0) or (raw<=0 and error>0) else 0.
        return np.array([di,dv,dint]),d,icmd
    for k in range(n):
        z=state[k];a,duty[k],iref[k]=derivative(z,ref[k],rload[k]);b,*_=derivative(z+dt*a/2,ref[k],rload[k]);cc,*_=derivative(z+dt*b/2,ref[k],rload[k]);dd,*_=derivative(z+dt*cc,ref[k],rload[k]);state[k+1]=z+dt*(a+2*b+2*cc+dd)/6
    _,duty[-1],iref[-1]=derivative(state[-1],ref[-1],rload[-1]);i=state[:,0];v=state[:,1];pin=duty*vin*i;pout=v*v/rload;ploss=rtot*i*i;energy=.5*l*i*i+.5*c*v*v
    residual=np.trapezoid(pin-pout-ploss,t)-(energy[-1]-energy[0])
    sel=np.unique(np.r_[np.arange(0,n+1,save_stride),n,round(.002/dt),round(.004/dt)])
    return dict(t=t[sel],current=i[sel],voltage=v[sel],reference=ref[sel],duty=duty[sel],current_reference=iref[sel],load_current=(v/rload)[sel],input_power=pin[sel],output_power=pout[sel],conduction_loss=ploss[sel],
                metrics=dict(peak_output_V=float(max(v)),maximum_IL_A=float(max(i)),current_reference_limit_A=limit,
                             final_output_V=float(v[-1]),final_load_current_A=float(v[-1]/rload[-1]),
                             pre_step_output_V=float(v[round(.0039/dt)]),minimum_post_step_output_V=float(min(v[t>=.004])),
                             maximum_duty=float(max(duty)),integrated_energy_residual_J=float(residual),internal_step_s=dt,saved_stride_steps=save_stride))
