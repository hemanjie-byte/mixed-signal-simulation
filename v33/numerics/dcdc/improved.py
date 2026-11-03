"""Numerical refinements of preserved V3.2 equations; no calibrated physics.

The baseline module is imported read-only. Analytical trajectories stay
analytical; tighter numerical integration does not validate device parameters.
"""
from pathlib import Path
import importlib.util
import math
import numpy as np

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('preserved_v32_dcdc',REPO/'v32/models/dcdc_models.py')
baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
VINS=baseline.VINS;TEMPS=baseline.TEMPS;FS=baseline.FS
resistance=baseline.resistance
capacitance=baseline.capacitance
capacitor_charge=baseline.capacitor_charge
capacitor_energy=baseline.capacitor_energy
recovery_pulse=baseline.recovery_pulse
deadtime_buck=baseline.deadtime_buck
bootstrap=baseline.bootstrap
level_shift=baseline.level_shift
coss_hard_commutation=baseline.coss_hard_commutation
_GX,_GW=np.polynomial.legendre.leggauss(32)

def _gauss(f,a,b):
    return float((b-a)/2*np.dot(_GW,f((a+b)/2+(b-a)/2*_GX)))

def overlap_quadrature(vin,temp_c):
    """Integrate each smooth physical stage, independent of display samples."""
    vth=2.2-.002*(temp_c-25);vp=vth+2.;ron=resistance(temp_c)
    ton=8*800e-12;toff=5*800e-12
    ta=-ton*np.log1p(-vth/10);tb=-ton*np.log1p(-vp/10)
    def on_power(t):
        cur=.5*(10*(1-np.exp(-t/ton))-vth)
        return vin*cur-ron*cur**2
    tc=toff*np.log(vp/vth)
    def off_power(t):
        cur=.5*(vp*np.exp(-t/toff)-vth)
        return vin*cur-ron*cur**2
    weighted_charge=_gauss(lambda v:(v-ron)*80e-12/np.sqrt(1+v/20),ron,vin)
    return (_gauss(on_power,ta,tb)+weighted_charge/((10-vp)/8),
            _gauss(off_power,0,tc)+weighted_charge/(vp/5))

def gate_switch(vin=100.,temp_c=25.,points=121):
    d=baseline.gate_switch(vin,temp_c,points)
    a,b=overlap_quadrature(vin,temp_c)
    d['metrics'].update(channel_overlap_on_J=a,channel_overlap_off_J=b)
    return d

def current_sense(temp_c=25.,dt=2e-9,end=2e-6):
    """Insert left/right comparator event samples into the analytic waveform."""
    d=baseline.current_sense(temp_c,dt,end);m=d['metrics'];step=100e-9
    crossing=m['analog_crossing_time_s'];event=m['trip_time_s']
    rows=[(float(t),1)for t in d['t']if t!=step and t!=event]
    rows.extend([(step,0),(step,1),(crossing,1),(event,0),(event,1)])
    rows.sort();t=np.array([r[0]for r in rows]);side=np.array([r[1]for r in rows])
    rs=m['sense_resistance_ohm'];offset=m['amplifier_offset_V']
    cur=np.where((t<step)|((t==step)&(side==0)),.5,3.)
    y0=20*rs*.5+offset;y1=20*rs*3+offset
    out=y0+(y1-y0)*(-np.expm1(-np.maximum(t-step,0)/100e-9))
    trip=((t>event)|((t==event)&(side==1))).astype(float)
    sampled=float(t[np.flatnonzero(trip)[0]])
    m.update(sampled_trip_time_s=sampled,sampled_trip_timing_error_s=abs(sampled-event))
    return dict(t=t,load=cur,vsense=rs*cur,out=out,trip=trip,metrics=m)

def startup_uvlo(vin=100.,temp_c=25.,dt=2e-6,end=.040):
    """Exact event-aligned segments for the V3.2 matrix's constant-current regime.

    The original compliance law is inactive throughout 0 <= Vaux <= 11 V
    in the supported Vin/temperature domain. Reject an unsupported domain
    rather than silently replacing a compliance-limited exponential by a line.
    dt controls display sampling only; UVLO/clamp/source events are inserted.
    """
    c=1e-6;istart=1e-3*(1+.001*(temp_c-25));on=9.;off=7.;vmax=11.
    if istart>(vin-vmax)/20000 or istart<=500e-6:
        raise ValueError('Exact startup segments require inactive compliance and positive enabled charging current')
    now=0.;v=0.;enabled=False;segments=[];enable_times=[];disable_times=[]
    while now<end-1e-15:
        if not enabled and v>=on-1e-12:
            enabled=True;enable_times.append(now)
        elif enabled and v<=off+1e-12:
            enabled=False;disable_times.append(now)
        source=0. if .014<=now<.024 else istart
        load=500e-6 if enabled else 40e-6
        slope=(source-load)/c;clamp=0.
        if v>=vmax-1e-12 and slope>0:slope=0.;clamp=source-load;v=vmax
        if v<=0 and slope<0:raise ValueError('Outside nonnegative auxiliary-voltage bench domain')
        candidates=[(b,'source')for b in [.014,.024,end]if b>now+1e-15]
        if slope>0:
            threshold=on if not enabled else vmax
            if threshold>v+1e-12:candidates.append((now+(threshold-v)/slope,'voltage'))
        elif slope<0 and enabled:
            candidates.append((now+(off-v)/slope,'voltage'))
        finish,kind=min(candidates,key=lambda z:z[0]);finish=min(finish,end)
        segments.append((now,finish,v,slope,float(enabled),source,load,clamp))
        v+=slope*(finish-now);now=finish
    starts=np.array([s[0]for s in segments]);event_times=starts[1:]
    rows=[(float(t),1)for t in np.arange(round(end/dt)+1)*dt]
    for event in event_times:
        rows=[r for r in rows if r[0]!=event]
        rows.extend([(float(event),0),(float(event),1)])
    rows.sort();t=np.array([r[0]for r in rows]);side=np.array([r[1]for r in rows])
    idx=np.searchsorted(starts,t,side='right')-1
    left=np.isin(t,event_times)&(side==0);idx[left]-=1
    seg=np.asarray(segments)[idx]
    voltage=seg[:,2]+seg[:,3]*(t-seg[:,0]);voltage=np.minimum(voltage,vmax)
    return dict(t=t,vaux=voltage,enabled=seg[:,4],isource=seg[:,5],iload=seg[:,6],iclamp=seg[:,7],
                source_loss=(vin-voltage)*seg[:,5],event_indices=np.flatnonzero(np.isin(t,event_times)),
                metrics=dict(first_enable_s=float(enable_times[0]),enable_events=len(enable_times),brownout_events=len(disable_times),
                             peak_source_dissipation_W=float(np.max((vin-voltage)*seg[:,5])),peak_Vaux_V=float(np.max(voltage)),
                             start_current_limit_A=istart,source_compliance_resistance_ohm=20000.))

def _simpson_uniform(y,t):
    if len(y)%2!=1:raise ValueError('Composite Simpson needs an even interval count')
    h=(t[-1]-t[0])/(len(t)-1)
    return float(h/3*(y[0]+y[-1]+4*np.sum(y[1:-1:2])+2*np.sum(y[2:-1:2])))

def ringing(vin=100.,damping='damped',points=1501):
    d=baseline.ringing(vin,damping,points)
    # Keep display density; refine the integration grid by four. On this
    # p(0)=p'(0)=0 response, same-grid Simpson need not beat trapezoidal.
    dense=baseline.ringing(vin,damping,4*(points-1)+1)
    energy=_simpson_uniform(dense['loss'],dense['t'])
    d['metrics']['energy_residual_J']=energy-(d['energy'][0]-d['energy'][-1])
    d['metrics']['integrated_damping_energy_J']=energy
    return d

def _linear_square_integral(t,y):
    return float(np.sum(np.diff(t)*(y[:-1]**2+y[:-1]*y[1:]+y[1:]**2)/3))

def loss_budget(vin=100.,ambient_c=25.):
    """Same nine-term ledger, improved overlap/RMS numerical integration only."""
    rth=8.;cth=.025;coss=coss_hard_commutation(vin)
    def parts(temp):
        g=gate_switch(vin,temp,points=81)['metrics'];d=deadtime_buck(vin,temp,points_per_phase=31)
        irms2=_linear_square_integral(d['t_s'],d['IL_A'])*FS;duty=d['parameters']['duty_fraction']
        return dict(high_side_conduction_W=irms2*resistance(temp)*duty,
                    low_side_conduction_W=irms2*resistance(temp)*(1-duty-2*40e-9*FS),
                    inductor_copper_W=irms2*resistance(temp,.12),
                    channel_overlap_W=(g['channel_overlap_on_J']+g['channel_overlap_off_J'])*FS,
                    Coss_commutation_W=coss['Coss_hard_commutation_J']*FS,
                    recovery_bus_estimate_W=vin*recovery_pulse(vin,temp)['qrr']*FS,
                    gate_driver_supply_W=2*g['gate_charge_C']*10*FS,
                    deadtime_diode_W=d['metrics']['diode_deadtime_loss_W'],assumed_control_supply_W=.01)
    hot=ambient_c
    for _ in range(100):
        new=ambient_c+rth*sum(parts(hot).values())
        if abs(new-hot)<1e-13:break
        hot=.5*(hot+new)
    components=parts(hot);total=sum(components.values());t=np.linspace(0,1,801)
    return dict(t=t,temperature=ambient_c+total*rth*(-np.expm1(-t/(rth*cth))),parts=components,
                metrics=dict(total_loss_W=total,estimated_efficiency=12/(12+total),steady_hot_node_C=hot,
                             thermal_fixed_point_residual_K=hot-ambient_c-rth*total,Rtheta_K_per_W=rth,Ctheta_J_per_K=cth,
                             parameter_temperature_range_exceeded=int(hot>175 or hot<-40),**coss))

def control_rhs(time,z,vin,temp_c,load_r):
    """The same continuous averaged ODE, with its ramp evaluated at stage time."""
    current,vout,integ=z;ref=min(12.,6000*time);error=ref-vout;raw=.25*error+integ
    cmd=min(1.6,max(0.,raw));r=resistance(temp_c,.30);l=100e-6
    duty=min(.90,max(0.,(vout+r*current+l*(2*math.pi*12000)*(cmd-current))/vin))
    dint=350*error if (0<raw<1.6)or(raw>=1.6 and error<0)or(raw<=0 and error>0)else 0.
    derivative=np.array([(duty*vin-r*current-vout)/l,(current-vout/load_r)/22e-6,dint])
    power=duty*vin*current-vout*vout/load_r-r*current*current
    return derivative,duty,cmd,power

def controlled_buck(vin=100.,temp_c=25.,dt=.5e-6,end=.008,save_stride=20):
    """RK4 evaluates continuous ramp at all stages; load events bound steps.

    Same averaged plant and limits as V3.2. Finer steps address numerical
    time discretization, not PWM/slope-compensation or device-model accuracy.
    """
    n=round(end/dt)
    for event in [.002,.004,end]:
        if abs(event/dt-round(event/dt))>1e-7:raise ValueError('Step must align with ramp/load/end events')
    t=np.arange(n+1)*dt;state=np.zeros((n+1,3));duty=np.zeros(n+1);iref=np.zeros(n+1);net_energy=0.
    for k in range(n):
        tk=t[k];z=state[k];rload=12. if k<round(.004/dt)else 6.
        a,duty[k],iref[k],pa=control_rhs(tk,z,vin,temp_c,rload)
        b,_,_,pb=control_rhs(tk+dt/2,z+dt*a/2,vin,temp_c,rload)
        c,_,_,pc=control_rhs(tk+dt/2,z+dt*b/2,vin,temp_c,rload)
        d,_,_,pd=control_rhs(tk+dt,z+dt*c,vin,temp_c,rload)
        state[k+1]=z+dt*(a+2*b+2*c+d)/6;net_energy+=dt*(pa+2*pb+2*pc+pd)/6
    _,duty[-1],iref[-1],_=control_rhs(t[-1],state[-1],vin,temp_c,6.)
    i=state[:,0];v=state[:,1];rload=np.where(np.arange(n+1)<round(.004/dt),12.,6.);r=resistance(temp_c,.30)
    pin=duty*vin*i;pout=v*v/rload;loss=r*i*i;stored=.5*100e-6*i*i+.5*22e-6*v*v
    sel=np.unique(np.r_[np.arange(0,n+1,save_stride),n,round(.002/dt),round(.004/dt)])
    return dict(t=t[sel],current=i[sel],voltage=v[sel],reference=np.minimum(12.,6000*t[sel]),duty=duty[sel],
                current_reference=iref[sel],load_current=(v/rload)[sel],input_power=pin[sel],output_power=pout[sel],conduction_loss=loss[sel],
                metrics=dict(peak_output_V=float(max(v)),maximum_IL_A=float(max(i)),current_reference_limit_A=1.6,
                             final_output_V=float(v[-1]),final_load_current_A=float(v[-1]/6),pre_step_output_V=float(v[round(.0039/dt)]),
                             minimum_post_step_output_V=float(min(v[t>=.004])),maximum_duty=float(max(duty)),
                             integrated_energy_residual_J=float(net_energy-(stored[-1]-stored[0])),internal_step_s=dt,saved_stride_steps=save_stride))
