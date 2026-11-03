"""Independent references for the *same assumed equations*, not device truth.

P01 uses closed-form exponential/charge primitives instead of production
Gauss quadrature. P08 uses closed-form phase moments and bisection. P09 uses
adaptive Dormand-Prince 5(4), distinct from the production fixed-step RK4.
"""
import math
import numpy as np

def gate_overlap_closed(vin,temp):
    r=.18*(1+.004*(temp-25));vth=2.2-.002*(temp-25);vp=vth+2
    def current_integrals(a,b,tau,start,end):
        # I(t)=a+b*exp(-t/tau).
        e1=math.exp(-start/tau)-math.exp(-end/tau)
        e2=math.exp(-2*start/tau)-math.exp(-2*end/tau)
        return (a*(end-start)+b*tau*e1,
                a*a*(end-start)+2*a*b*tau*e1+b*b*tau/2*e2)
    tau=8*800e-12;start=-tau*math.log1p(-vth/10);end=-tau*math.log1p(-vp/10)
    ion,i2on=current_integrals(.5*(10-vth),-5,tau,start,end)
    tau=5*800e-12;ioff,i2off=current_integrals(-.5*vth,.5*vp,tau,0,tau*math.log(vp/vth))
    def charge_primitive(v):
        u=math.sqrt(1+v/20)
        return 2*80e-12*20*u
    def energy_primitive(v):
        u=math.sqrt(1+v/20)
        return 2*80e-12*20**2*(u**3/3-u)
    weighted=energy_primitive(vin)-energy_primitive(r)-r*(charge_primitive(vin)-charge_primitive(r))
    return vin*ion-r*i2on+weighted/((10-vp)/8),vin*ioff-r*i2off+weighted/(vp/5)

def phase_moments(vin,temp):
    period=4e-6;vf=.8-.001*(temp-25);dead=40e-9;duty=(12+2*dead/period*vf)/vin
    durations=[duty*period,dead,(1-duty)*period-2*dead,dead]
    switches=[vin,-vf,0,-vf];edges=[0.]
    for duration,voltage in zip(durations,switches):edges.append(edges[-1]+(voltage-12)/100e-6*duration)
    mean=sum(h*(a+b)/2 for h,a,b in zip(durations,edges[:-1],edges[1:]))/period
    edge_current=np.asarray(edges)+1-mean
    rms2=sum(h*(a*a+a*b+b*b)/3 for h,a,b in zip(durations,edge_current[:-1],edge_current[1:]))/period
    diode=vf/period*sum(durations[k]*(edge_current[k]+edge_current[k+1])/2 for k in [1,3])
    return duty,rms2,diode

def loss_reference(vin,ambient):
    def total(temp):
        duty,rms2,diode=phase_moments(vin,temp);r=.18*(1+.004*(temp-25));rl=.12*(1+.004*(temp-25))
        on,off=gate_overlap_closed(vin,temp)
        qoss=2*600e-12*20*(math.sqrt(1+vin/20)-1)
        qgd=2*80e-12*20*(math.sqrt(1+vin/20)-math.sqrt(1+r/20))
        qrr=12e-9*(1+.005*(temp-25));fs=250e3
        return (rms2*r*(1-2*40e-9*fs)+rms2*rl+(on+off)*fs+
                vin*qoss*fs+vin*qrr*fs+2*(800e-12*10+qgd)*10*fs+diode+.01)
    lo=ambient;hi=ambient+100
    if hi-ambient-8*total(hi)<=0:raise ValueError('Reference root is not bracketed')
    for _ in range(70):
        mid=(lo+hi)/2
        if mid-ambient-8*total(mid)>0:hi=mid
        else:lo=mid
    hot=(lo+hi)/2
    return total(hot),hot

def buck_reference(vin,temp,rtol=1e-10,atol=1e-12):
    """Adaptive fifth-order reference at 10us output times, with event bounds."""
    def rhs(time,z,load):
        il,vo,integ=z;err=min(12.,time*6000)-vo;raw=integ+.25*err
        cmd=max(0.,min(1.6,raw));r=.30*(1+.004*(temp-25))
        control=(vo+r*il+100e-6*(2*math.pi*12000)*(cmd-il))/vin
        duty=max(0.,min(.9,control))
        dz=350*err if ((0<raw<1.6)or(raw>=1.6 and err<0)or(raw<=0 and err>0))else 0.
        return np.array([(duty*vin-r*il-vo)/100e-6,(il-vo/load)/22e-6,dz])
    times=np.arange(801)*1e-5;output=np.zeros((801,3));now=0.;z=np.zeros(3);h=2e-6;steps=0;rejects=0
    # Dormand-Prince coefficients, the embedded fourth-order estimate controls steps.
    for idx,target in enumerate(times[1:],1):
        while now<target-1e-16:
            step=min(h,target-now);load=12. if now<.004-1e-15 else 6.
            k1=rhs(now,z,load)
            k2=rhs(now+step/5,z+step*k1/5,load)
            k3=rhs(now+3*step/10,z+step*(3*k1/40+9*k2/40),load)
            k4=rhs(now+4*step/5,z+step*(44*k1/45-56*k2/15+32*k3/9),load)
            k5=rhs(now+8*step/9,z+step*(19372*k1/6561-25360*k2/2187+64448*k3/6561-212*k4/729),load)
            k6=rhs(now+step,z+step*(9017*k1/3168-355*k2/33+46732*k3/5247+49*k4/176-5103*k5/18656),load)
            nxt=z+step*(35*k1/384+500*k3/1113+125*k4/192-2187*k5/6784+11*k6/84)
            k7=rhs(now+step,nxt,load)
            fourth=z+step*(5179*k1/57600+7571*k3/16695+393*k4/640-92097*k5/339200+187*k6/2100+k7/40)
            err=float(np.max(abs(nxt-fourth)/(atol+rtol*np.maximum(abs(z),abs(nxt)))))
            if err<=1:
                now+=step;z=nxt;steps+=1
            else:rejects+=1
            h=min(20e-6,step*(5 if err==0 else min(5,max(.1,.9*err**(-.2)))))
            if h<1e-14:raise RuntimeError('Reference integration failed to converge')
        output[idx]=z;now=target
    return dict(t=times,voltage=output[:,1],current=output[:,0],steps=steps,rejected=rejects,rtol=rtol,atol=atol)
