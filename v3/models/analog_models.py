"""Reduced analog models, SI units, positive terminal currents into the device.

Public equations with explicitly assumed parameters. No foundry model or fitted
measurement is used. See MODEL_CARDS.md for validity limits and references.
"""
from __future__ import annotations
import numpy as np

KB = 1.380649e-23
QE = 1.602176634e-19
T0 = 298.15


def thermal_voltage(temp_c):
    if np.any(np.asarray(temp_c) <= -273.15):
        raise ValueError('Temperature must exceed absolute zero')
    return KB * (np.asarray(temp_c) + 273.15) / QE


def mos_current(vg, vd, vs=0.0, vb=0.0, temp_c=25.0):
    """Symmetric, EKV-inspired DC interpolation; not the complete EKV model."""
    ut = thermal_voltage(temp_c)
    n = 1.5
    beta = 1e-3 * ((temp_c + 273.15) / T0) ** -1.5
    vth = .55 - .001 * (temp_c - 25)
    vp = (np.asarray(vg) - vb - vth) / n
    f = np.logaddexp(0, (vp - (np.asarray(vs) - vb)) / (2 * ut)) ** 2
    r = np.logaddexp(0, (vp - (np.asarray(vd) - vb)) / (2 * ut)) ** 2
    return 2 * n * beta * ut ** 2 * (f - r) * (1 + .03 * np.abs(np.asarray(vd) - vs))


def mos_small_signal(vg, vd, vs=0.0, vb=0.0, temp_c=25.0):
    """Centered numerical derivatives, each in A/V (S)."""
    h = 1e-5
    gm = (mos_current(np.asarray(vg)+h,vd,vs,vb,temp_c)-mos_current(np.asarray(vg)-h,vd,vs,vb,temp_c))/(2*h)
    gds = (mos_current(vg,np.asarray(vd)+h,vs,vb,temp_c)-mos_current(vg,np.asarray(vd)-h,vs,vb,temp_c))/(2*h)
    gmb = (mos_current(vg,vd,vs,np.asarray(vb)+h,temp_c)-mos_current(vg,vd,vs,np.asarray(vb)-h,temp_c))/(2*h)
    return gm, gds, gmb


def mos_charges(vg, vd, vs=0.0, vb=0.0):
    """Conservative fixed pair-capacitor network in G,D,S,B order.

    This deliberately excludes intrinsic inversion-charge partition. Q is not
    derived from the DC interpolation and is not a full charge-based EKV model.
    """
    vg,vd,vs,vb=np.broadcast_arrays(vg,vd,vs,vb)
    volts=[vg,vd,vs,vb];q=[np.zeros_like(vg,dtype=float) for _ in range(4)]
    for i,j,c in [(0,2,2e-12),(0,1,.2e-12),(0,3,.1e-12),(1,3,.3e-12),(2,3,.3e-12)]:
        z=c*(volts[i]-volts[j]);q[i]+=z;q[j]-=z
    return np.array(q)


def junction_qc(v, temp_c=25.0):
    """Depletion-only charge referenced to V=0; limited to V < 0.35 V."""
    v=np.asarray(v);phi=.7;c0=2e-12*(1+2e-4*(temp_c-25));m=.5
    if np.any(v>=.35) or np.any(v < -20):
        raise ValueError('Junction demonstration range is -20 <= V < 0.35 V')
    q=c0*phi/(1-m)*(1-(1-v/phi)**(1-m))
    c=c0/(1-v/phi)**m
    return q,c


def bjt_currents(vb, vc, ve=0.0, temp_c=25.0):
    """Reciprocal Ebers-Moll NPN; no Early effect or high injection."""
    t=temp_c+273.15;ut=thermal_voltage(temp_c)
    isat=1e-15*(t/T0)**3*np.exp(1.11*QE/KB*(1/T0-1/t))
    af=100/101;ar=2/3
    i_f=isat/af*np.expm1((np.asarray(vb)-ve)/ut)
    i_r=isat/ar*np.expm1((np.asarray(vb)-vc)/ut)
    ic=af*i_f-i_r;ib=(1-af)*i_f+(1-ar)*i_r;ie=-i_f+ar*i_r
    return ic,ib,ie


def mismatch_samples(area_um2, samples=20000, rho=0.25, seed=20261101):
    """A_VT denotes uncorrelated PAIR sigma * sqrt(area), not single-device sigma."""
    if area_um2<=0 or not 0<=rho<1:raise ValueError('Invalid mismatch area/correlation')
    rng=np.random.default_rng(seed);z=rng.standard_normal((3,samples))
    sigma_single=.003/np.sqrt(2*area_um2)
    v1=sigma_single*z[0];v2=sigma_single*(rho*z[0]+np.sqrt(1-rho*rho)*z[1])
    global_shift=.02*z[2]
    return v1+global_shift,v2+global_shift,v1-v2,.003*np.sqrt((1-rho)/area_um2)


def differential_pair(vdiff, temp_c=25.0, tail_a=100e-6):
    """Solve the shared source voltage with 80 bisection steps, fixed drain biases."""
    vdiff=np.asarray(vdiff);g1=.85+vdiff/2;g2=.85-vdiff/2
    lo=np.full_like(vdiff,-1.0);hi=np.full_like(vdiff,1.7)
    for _ in range(80):
        mid=(lo+hi)/2
        current=mos_current(g1,1.8,mid,0,temp_c)+mos_current(g2,1.8,mid,0,temp_c)
        lo=np.where(current>tail_a,mid,lo);hi=np.where(current>tail_a,hi,mid)
    source=(lo+hi)/2
    return source,mos_current(g1,1.8,source,0,temp_c),mos_current(g2,1.8,source,0,temp_c)


def bandgap(temp_c):
    """Ideal CTAT+PTAT sum, not a transistor-level reproduction of Brokaw's circuit."""
    t=np.asarray(temp_c)+273.15;ut=thermal_voltage(temp_c);ut0=thermal_voltage(25)
    vg0=1.205;vbe0=.68;eta=3.0;nratio=8.0
    vbe=vg0+(vbe0-vg0)*t/T0-eta*ut*np.log(t/T0)
    delta=ut*np.log(nratio)
    scale=(vg0-vbe0+eta*ut0)/(ut0*np.log(nratio))
    return vbe,delta,vbe+scale*delta,scale


def noise_psd(freq_hz,temp_c=25.0):
    f=np.asarray(freq_hz)
    if np.any(f<=0):raise ValueError('Frequency must be positive')
    e2=(10e-9)**2*(temp_c+273.15)/T0
    return e2*(1+100/f),e2*(2+100/(f+20000))


def cdac_weights(bits=10,unit_sigma=.02,seed=20261101):
    """Independent unit-cap errors aggregated into binary weights plus a dummy."""
    if bits<2 or bits>16 or unit_sigma<0:raise ValueError('Invalid ADC parameters')
    rng=np.random.default_rng(seed);units=2.0**np.arange(bits-1,-1,-1)
    caps=units+unit_sigma*np.sqrt(units)*rng.standard_normal(bits)
    dummy=1+unit_sigma*rng.standard_normal()
    if np.any(caps<=0) or dummy<=0:raise ValueError('Nonphysical capacitor sample')
    return caps/(sum(caps)+dummy)


def dac_voltage(codes,weights,vref=1.8):
    codes=np.asarray(codes,dtype=np.int64);out=np.zeros_like(codes,dtype=float)
    for j,w in enumerate(weights):out+=((codes>>(len(weights)-1-j))&1)*w*vref
    return out


def sar_convert(vin,weights,vref=1.8):
    vin=np.asarray(vin);codes=np.zeros_like(vin,dtype=np.int64)
    for bit in range(len(weights)-1,-1,-1):
        trial=codes|(1<<bit)
        codes=np.where(vin>=dac_voltage(trial,weights,vref),trial,codes)
    return codes


def adc_metrics(bits=10,unit_sigma=.02,samples=16384,tone_bin=503):
    weights=cdac_weights(bits,unit_sigma);vref=1.8;ncode=2**bits;lsb=vref/ncode
    levels=dac_voltage(np.arange(ncode),weights,vref)
    widths=np.diff(np.r_[levels,vref]);dnl=widths/lsb-1
    ideal_line=np.arange(ncode)*levels[-1]/(ncode-1)
    inl=(levels-ideal_line)/lsb
    t=np.arange(samples)/2e6;vin=vref*(.5+.49*np.sin(2*np.pi*tone_bin*np.arange(samples)/samples))
    codes=sar_convert(vin,weights,vref);vout=(codes+.5)*lsb
    spectrum=np.abs(np.fft.rfft(vout-vout.mean()))**2
    signal=spectrum[tone_bin];other=spectrum.copy();other[0]=0;other[tone_bin]=0
    sndr=10*np.log10(signal/other.sum());sfdr=10*np.log10(signal/other.max())
    no_harm=other.copy()
    for h in range(2,6):
        k=(h*tone_bin)%samples;k=min(k,samples-k);no_harm[k]=0
    snr=10*np.log10(signal/no_harm.sum())
    return dict(t=t,vin=vin,vout=vout,codes=codes,levels=levels,dnl=dnl,inl=inl,weights=weights,
                freq=np.fft.rfftfreq(samples,1/2e6),spectrum_dbc=10*np.log10(np.maximum(spectrum/signal,1e-20)),
                metrics={'SNDR_dB':float(sndr),'SNR_excluding_harmonics_2_to_5_dB':float(snr),'SFDR_dBc':float(sfdr),
                         'ENOB_bits':float((sndr-1.76)/6.02),'DNL_max_abs_LSB':float(np.max(np.abs(dnl))),
                         'endpoint_INL_max_abs_LSB':float(np.max(np.abs(inl))),'missing_codes':int(np.sum(widths<=0))})


def rk4_linear(matrix,forcing,initial,dt,steps):
    y=np.empty((steps+1,len(initial)));y[0]=initial
    for k in range(steps):
        z=y[k];a=matrix@z+forcing;b=matrix@(z+dt*a/2)+forcing
        c=matrix@(z+dt*b/2)+forcing;d=matrix@(z+dt*c)+forcing
        y[k+1]=z+dt*(a+2*b+2*c+d)/6
    return y


def ldo_response(temp_c=25.0,dt=1e-7,end=300e-6):
    c=10e-6;r=90.0;g=.5*((temp_c+273.15)/T0)**-1.2;wa=2*np.pi*20000
    matrix=np.array([[-1/(r*c),1/c],[-wa*g,-wa]])
    forcing=np.array([-.01/c,0.0]);steps=int(round(end/dt));t=np.arange(steps+1)*dt
    y=rk4_linear(matrix,forcing,[0.,0.],dt,steps)
    vout=1.8+y[:,0];ipass=.02+y[:,1];iload=.02+.01+y[:,0]/r
    f=np.geomspace(10,1e7,600);s=2j*np.pi*f;loop=g/((c*s+1/r)*(1+s/wa))
    idx=np.where(np.abs(loop)<1)[0][0]
    logf=np.interp(0,[np.log(abs(loop[idx])),np.log(abs(loop[idx-1]))],[np.log(f[idx]),np.log(f[idx-1])])
    ug=np.exp(logf);l=g/((c*2j*np.pi*ug+1/r)*(1+2j*np.pi*ug/wa))
    return dict(t=t,vout=vout,ipass=ipass,iload=iload,matrix=matrix,forcing=forcing,states=y,
                f=f,loop=loop,dc_deviation=-.01/(g+1/r),unity_hz=ug,phase_margin=180+np.angle(l,deg=True))


def pll_response(zeta=.7,dt=2e-8):
    wn=2*np.pi*1e5;step=.1;end=40e-6;steps=int(round(end/dt));t=np.arange(steps+1)*dt
    matrix=np.array([[0.,1.],[-wn*wn,-2*zeta*wn]])
    y=rk4_linear(matrix,[0,wn*wn*step],[0.,0.],dt,steps)
    f=np.geomspace(100,1e7,1000);s=2j*np.pi*f;h=wn*wn/(s*s+2*zeta*wn*s+wn*wn)
    sref=np.full_like(f,1e-13);svco=1e-16*(1+(1e5/f)**2+(1e4/f)**3)
    sout=abs(h)**2*sref+abs(1-h)**2*svco
    jitter=np.sqrt(np.trapezoid(sout,f))/(2*np.pi*1e9)
    return dict(t=t,phase=y[:,0],frequency_error=y[:,1]/(2*np.pi),f=f,h=h,noise=sout,jitter_s=jitter)


def buck_response(vin=100.,temp_c=25.,steps_per_cycle=200,cycles=40,keep_cycles=5):
    """Event-aligned RK4, synchronous forced CCM, conduction losses only."""
    if vin not in [40,60,80,100,120,150]:raise ValueError('Vin must be a documented input class')
    l=100e-6;c=22e-6;rload=12.;fs=250e3;period=1/fs
    factor=1+.004*(temp_c-25);rs=.18*factor;rl=.12*factor
    duty=(12+rs+rl)/vin
    matrix=np.array([[-(rs+rl)/l,-1/l],[1/c,-1/(rload*c)]])
    # Solve the exact linear period map for the periodic initial condition.
    # Starting at the averaged DC point can leave stored-energy transients that
    # make a short-window Pout/Pin ratio exceed unity without violating physics.
    ev,vec=np.linalg.eig(matrix);inv=np.linalg.inv(vec)
    transition=lambda duration:(vec@np.diag(np.exp(ev*duration))@inv).real
    eon=transition(duty*period);eoff=transition((1-duty)*period)
    forcing_on=np.array([vin/l,0.])
    increment=np.linalg.solve(matrix,(eon-np.eye(2))@forcing_on)
    state=np.linalg.solve(np.eye(2)-eoff@eon,eoff@increment)
    tt=[];ii=[];vv=[];gg=[];time=0.
    # Save both sides of switching events: same state, different algebraic voltages.
    for cycle in range(cycles):
        for on,duration in [(1,duty*period),(0,(1-duty)*period)]:
            n=max(1,int(np.ceil(duration/(period/steps_per_cycle))));h=duration/n
            forcing=np.array([on*vin/l,0.])
            for k in range(n+1):
                if cycle>=cycles-keep_cycles:tt.append(time);ii.append(state[0]);vv.append(state[1]);gg.append(on)
                if k==n:continue
                a=matrix@state+forcing;b=matrix@(state+h*a/2)+forcing
                cc=matrix@(state+h*b/2)+forcing;d=matrix@(state+h*cc)+forcing
                state=state+h*(a+2*b+2*cc+d)/6;time+=h
    t=np.array(tt);i=np.array(ii);v=np.array(vv);on=np.array(gg)
    t-=t[0];sw=on*vin-rs*i;pin=vin*i*on;pout=v*v/rload;loss=(rs+rl)*i*i
    energy=.5*l*i*i+.5*c*v*v;duration=t[-1]-t[0]
    avg=lambda x:float(np.trapezoid(x,t)/duration)
    residual=float(np.trapezoid(pin-pout-loss,t)-(energy[-1]-energy[0]))
    return dict(t=t,i=i,v=v,on=on,sw=sw,pin=pin,pout=pout,loss=loss,energy=energy,duty=duty,
                metrics={'mean_Vout_V':avg(v),'Vout_ripple_pp_V':float(np.ptp(v)),
                         'inductor_ripple_pp_A':float(np.ptp(i)),'conduction_only_efficiency':avg(pout)/avg(pin),
                         'mean_conduction_loss_W':avg(loss),'energy_residual_J':residual,
                         'max_high_side_Vds_V':float(np.max(vin-sw)),'max_low_side_Vds_V':float(np.max(sw)),
                         'duty_fraction':duty})
