"""Independent analytical limits and numerical convergence checks (unittest)."""
from pathlib import Path
import sys,unittest,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'models'))
from analog_models import *


class DeviceTests(unittest.TestCase):
    def test_mos_zero_and_source_drain_exchange(self):
        for t in [-40,25,125]:
            self.assertEqual(float(mos_current(.9,.2,.2,0,t)),0)
            self.assertAlmostEqual(float(mos_current(.9,1.2,.1,0,t)),-float(mos_current(.9,.1,1.2,0,t)),places=15)

    def test_mos_reference_potential_invariance(self):
        i=mos_current(.85,1.2,.1,-.2)
        self.assertAlmostEqual(float(i),float(mos_current(1.55,1.9,.8,.5)),places=15)

    def test_mos_weak_inversion_transconductance_limit(self):
        for t in [-40,25,125]:
            gm,_,gmb=mos_small_signal(-.3,1.2,temp_c=t);i=mos_current(-.3,1.2,temp_c=t)
            self.assertLess(abs(float(gm/i)*1.5*thermal_voltage(t)-1),.003)
            self.assertLess(abs(float(gmb/gm)-.5),1e-6)

    def test_mos_strong_inversion_limit(self):
        vov=1.8-.55
        expected=.001/(2*1.5)*vov**2*(1+.03*1.8)
        self.assertLess(abs(float(mos_current(1.8,1.8))/expected-1),1e-5)

    def test_capacitive_reciprocity_and_positive_energy(self):
        mat=np.column_stack([mos_charges(*np.eye(4)[j])for j in range(4)])
        self.assertLess(np.max(abs(mat-mat.T)),1e-25)
        self.assertLess(np.max(abs(mat.sum(axis=0))),1e-25)
        for v in np.random.default_rng(3).normal(size=(20,4)):
            self.assertGreaterEqual(float(v@mat@v),-1e-25)

    def test_junction_derivative_of_charge(self):
        v=np.linspace(-10,.3,100);h=1e-5
        derivative=(junction_qc(v+h)[0]-junction_qc(v-h)[0])/(2*h)
        self.assertLess(np.max(abs(derivative/junction_qc(v)[1]-1)),1e-8)

    def test_junction_transient_charge_balance(self):
        t=np.linspace(0,.37e-6,10001);v=-2+np.sin(2*np.pi*1e6*t);q,c=junction_qc(v)
        i=c*2*np.pi*1e6*np.cos(2*np.pi*1e6*t)
        self.assertLess(abs(np.trapezoid(i,t)-(q[-1]-q[0])),1e-19)
        with self.assertRaises(ValueError):junction_qc(.7)

    def test_bjt_zero_bias_and_forward_gain(self):
        self.assertEqual(tuple(float(i)for i in bjt_currents(0,0)),(0,0,0))
        for t in [-40,25,125]:
            ic,ib,ie=bjt_currents(.6,1.2,temp_c=t)
            # Finite reverse-junction leakage makes beta approach, not equal,
            # betaF. Bound that correction analytically at each temperature.
            forward=np.expm1(.6/thermal_voltage(t))
            bound=100*(1.5+100*.5)/forward
            self.assertLess(abs(float(ic/ib)-100),1.01*bound+1e-10)
            self.assertLess(abs(float(ic+ib+ie))/max(abs(float(ic)),1e-20),1e-12)

    def test_bjt_reciprocity_in_saturation(self):
        # At Vc=Ve, base injection partitions with reverse and forward beta.
        ic,ib,ie=bjt_currents(.6,0)
        self.assertAlmostEqual(float(ic/ie),100/2,places=8)

    def test_mismatch_pair_sigma_and_area(self):
        for area in [1,4,16,64]:
            _,_,dv,pred=mismatch_samples(area,samples=100000)
            self.assertLess(abs(np.std(dv,ddof=1)/pred-1),.01)
        _,_,dv,pred=mismatch_samples(4,samples=100000,rho=0)
        self.assertAlmostEqual(pred,.0015)
        self.assertLess(abs(np.std(dv,ddof=1)/.0015-1),.01)


class CircuitTests(unittest.TestCase):
    def test_sar_actual_transition_edges_with_missing_code(self):
        weights=np.array([.45,.30,.20])
        edges=sar_transition_levels(weights,1.)
        np.testing.assert_allclose(edges,[0,.2,.3,.45,.45,.65,.75,.95,1],atol=2e-16)
        self.assertEqual(np.count_nonzero(np.diff(edges)==0),1)
        self.assertAlmostEqual(np.diff(edges).sum(),1.)
        v=(np.arange(200000)+.5)/200000
        hist=np.bincount(sar_convert(v,weights,1.),minlength=8)/len(v)
        np.testing.assert_allclose(hist,np.diff(edges),atol=1/len(v))

    def test_fft_power_parseval_dc_nyquist_and_odd_length(self):
        for n in [1023,1024]:
            t=np.arange(n);x=1.7+.3*np.cos(2*np.pi*17*t/n)+.2*(-1.)**t
            self.assertAlmostEqual(one_sided_bin_power(x).sum(),np.mean(x*x),places=13)
        self.assertAlmostEqual(one_sided_bin_power((-1.)**np.arange(1024))[-1],1.)

    def test_adc_inl_endpoint_definition(self):
        d=adc_metrics(unit_sigma=.02)
        self.assertEqual(len(d['inl']),1023)
        self.assertAlmostEqual(d['inl'][0],0.,places=14)
        self.assertAlmostEqual(d['inl'][-1],0.,places=14)
        self.assertTrue(np.all(np.diff(d['transitions'])>=0))

    def test_ldo_unity_frequency_against_quadratic_solution(self):
        for temp in [-40,25,125]:
            d=ldo_response(temp);c=10e-6;r=90.;g=.5*((temp+273.15)/T0)**-1.2;wa=2*np.pi*20000
            # |L(jw)|=1 gives a quadratic in w**2, independently of log interpolation.
            a=c*c/wa**2;b=c*c+1/(r*r*wa**2);cc=1/r**2-g*g
            w2=2*(-cc)/(b+np.sqrt(b*b-4*a*cc));hz=np.sqrt(w2)/(2*np.pi)
            self.assertLess(abs(d['unity_hz']/hz-1),1e-4)

    def test_buck_all_voltage_temperature_grid_convergence(self):
        for vin in [40,60,80,100,120,150]:
            for temp in [-40,25,125]:
                a=buck_response(vin,temp,200);b=buck_response(vin,temp,400)
                self.assertLess(abs(a['metrics']['mean_Vout_V']-b['metrics']['mean_Vout_V']),1e-5)
                self.assertLess(abs(a['metrics']['conduction_only_efficiency']-b['metrics']['conduction_only_efficiency']),1e-5)
                self.assertLess(abs(a['metrics']['energy_residual_J']),2e-8)

    def test_differential_pair_symmetry_and_tail(self):
        x=np.linspace(-.3,.3,21)
        for t in [-40,25,125]:
            _,i1,i2=differential_pair(x,t)
            self.assertLess(np.max(abs(i1+i2-1e-4)),1e-15)
            self.assertLess(np.max(abs(i1-i2[::-1])),1e-15)
            self.assertAlmostEqual(float(i1[len(x)//2]),50e-6,places=14)

    def test_bandgap_first_order_cancellation(self):
        h=.001;d=(bandgap(25+h)[2]-bandgap(25-h)[2])/(2*h)
        self.assertLess(abs(float(d)),1e-10)
        self.assertAlmostEqual(float(bandgap(25)[2]),1.205+3*thermal_voltage(25),places=12)

    def test_bandgap_curvature_retained(self):
        ref=bandgap(np.array([-40,25,125]))[2]
        self.assertGreater(ref[1],ref[0]);self.assertGreater(ref[1],ref[2])
        self.assertGreater(float(np.ptp(ref)),1e-3)

    def test_noise_integral_against_analytic_reference(self):
        f=np.geomspace(1,1e6,1001);p,_=noise_psd(f)
        exact=1e-16*((1e6-1)+100*np.log(1e6))
        self.assertLess(abs(np.trapezoid(p,f)/exact-1),1e-6)

    def test_ideal_sar_codes_and_linearity(self):
        for bits in [8,10,12]:
            w=cdac_weights(bits,0);q=1.8/(2**bits);levels=dac_voltage(np.arange(2**bits),w)
            self.assertLess(np.max(abs(levels-np.arange(2**bits)*q)),1e-14)
            v=(np.arange(2**bits)+.25)*q
            np.testing.assert_array_equal(sar_convert(v,w),np.arange(2**bits))

    def test_adc_quantization_noise_limit(self):
        d=adc_metrics(unit_sigma=0)
        theory=6.020599913*10+1.76091259+20*np.log10(.98)
        self.assertLess(abs(d['metrics']['SNDR_dB']-theory),.15)
        self.assertLess(d['metrics']['DNL_max_abs_LSB'],1e-10)
        self.assertEqual(d['metrics']['missing_codes'],0)

    def test_adc_mismatch_changes_linearity(self):
        ideal=adc_metrics(unit_sigma=0);impaired=adc_metrics(unit_sigma=.02)
        self.assertGreater(impaired['metrics']['DNL_max_abs_LSB'],.1)
        self.assertLess(impaired['metrics']['SNDR_dB'],ideal['metrics']['SNDR_dB'])

    def test_ldo_against_matrix_exponential(self):
        d=ldo_response();a=d['matrix'];b=d['forcing'];steady=-np.linalg.solve(a,b)
        ev,vec=np.linalg.eig(a);inv=np.linalg.inv(vec)
        reference=np.array([steady-(vec@np.diag(np.exp(ev*t))@inv@steady).real for t in d['t']])
        self.assertLess(np.max(abs(d['states']-reference)),1e-9)
        self.assertLess(abs(d['vout'][-1]-1.8-d['dc_deviation']),1e-8)

    def test_ldo_step_convergence(self):
        a=ldo_response(dt=4e-7);b=ldo_response(dt=2e-7);c=ldo_response(dt=1e-7)
        coarse=np.max(abs(a['vout']-b['vout'][::2]));fine=np.max(abs(b['vout']-c['vout'][::2]))
        self.assertLess(fine,coarse/10)

    def test_ldo_energy_and_positive_phase_margin(self):
        d=ldo_response();v=d['vout'];p_cap=v*(d['ipass']-d['iload'])
        delta=.5*10e-6*(v[-1]**2-v[0]**2)
        self.assertLess(abs(np.trapezoid(p_cap,d['t'])-delta),1e-9)
        self.assertGreater(d['phase_margin'],30)

    def test_pll_step_against_closed_form(self):
        for z in [.3,.7]:
            d=pll_response(z);t=d['t'];wn=2*np.pi*1e5;wd=wn*np.sqrt(1-z*z)
            exact=.1*(1-np.exp(-z*wn*t)*(np.cos(wd*t)+z/np.sqrt(1-z*z)*np.sin(wd*t)))
            self.assertLess(np.max(abs(exact-d['phase'])),1e-9)

    def test_pll_jitter_psd_convention(self):
        d=pll_response();ssb=d['noise']/2
        jitter_from_ssb=np.sqrt(2*np.trapezoid(ssb,d['f']))/(2*np.pi*1e9)
        self.assertAlmostEqual(jitter_from_ssb,d['jitter_s'],places=20)

    def test_buck_event_alignment_and_convergence(self):
        a=buck_response(150,125,50);b=buck_response(150,125,100);c=buck_response(150,125,200)
        ea=abs(a['metrics']['mean_Vout_V']-c['metrics']['mean_Vout_V'])
        eb=abs(b['metrics']['mean_Vout_V']-c['metrics']['mean_Vout_V'])
        self.assertLess(eb,ea/5)
        self.assertLess(abs(c['metrics']['mean_Vout_V']-12),.02)
        self.assertTrue(np.any(np.diff(c['t'])==0)) # both sides of the discontinuity saved

    def test_buck_integrated_energy_balance(self):
        for vin in [40,100,150]:
            d=buck_response(vin)
            self.assertLess(abs(d['metrics']['energy_residual_J']),2e-8)
            self.assertTrue(0<d['metrics']['conduction_only_efficiency']<1)
            self.assertGreater(d['metrics']['max_high_side_Vds_V'],vin)


class ArtifactTests(unittest.TestCase):
    def test_published_cases_finite_complete_and_kcl(self):
        path=Path(__file__).resolve().parents[1]/'results/simulation_v3.json'
        d=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(len(d['models']),11);self.assertEqual(len(d['cases']),58)
        for c in d['cases']:
            n=len(c['x']);self.assertTrue(np.isfinite(c['x']).all())
            for s in c['signals']:
                self.assertEqual(len(s['y']),n);self.assertTrue(np.isfinite(s['y']).all())
            for p in c['plots']:
                self.assertTrue(np.isfinite(p['x']).all())
                for s in p['series']:
                    self.assertEqual(len(s['y']),len(p['x']))
                    self.assertTrue(np.isfinite(s['y']).all())
            if c['terminals']:
                for t in c['terminals']:
                    for k in ['v','i']:
                        self.assertEqual(len(t[k]),n);self.assertTrue(np.isfinite(t[k]).all())
                currents=np.array([t['i']for t in c['terminals']])
                voltages=np.array([t['v']for t in c['terminals']])
                self.assertLess(np.max(abs(currents.sum(axis=0))),1e-12)
                np.testing.assert_allclose(c['port_power_W'],(currents*voltages).sum(axis=0),atol=1e-14,rtol=1e-12)
                self.assertLess(c['metrics']['max_KCL_residual_A'],1e-12)
            else:self.assertIsNone(c['port_power_W'])


if __name__=='__main__':unittest.main(verbosity=2)
