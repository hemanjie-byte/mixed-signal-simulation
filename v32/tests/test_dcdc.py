"""Independent integrals, boundary conditions, convergence and artifact checks."""
from pathlib import Path
import sys,json,unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'models'))
from dcdc_models import *

class ChargeSwitchTests(unittest.TestCase):
    def test_charge_and_energy_against_dense_integrals(self):
        for v in VINS:
            x=np.linspace(0,v,20001);c=capacitance(x)
            self.assertLess(abs(np.trapezoid(c,x)/capacitor_charge(v)-1),1e-7)
            self.assertLess(abs(np.trapezoid(x*c,x)/capacitor_energy(v)-1),1e-7)
    def test_capacitance_is_derivative_of_charge(self):
        for v in [0.1,1,40,150]:
            h=1e-4;numeric=(capacitor_charge(v+h)-capacitor_charge(v-h))/(2*h)
            self.assertLess(abs(numeric/capacitance(v)-1),1e-7)
    def test_energy_is_not_half_qv_for_nonlinear_cap(self):
        for v in VINS:self.assertLess(capacitor_energy(v),.5*capacitor_charge(v)*v)
    def test_gate_charge_and_endpoint_voltages(self):
        for v in VINS:
            for temp in TEMPS:
                d=gate_switch(v,temp);m=d['metrics']
                self.assertAlmostEqual(d['vd_on'][0],v)
                self.assertAlmostEqual(d['vd_on'][-1],resistance(temp))
                self.assertAlmostEqual(d['vd_off'][-1],v)
                self.assertLess(abs(np.trapezoid(d['ig_on'],d['t_on'])/m['gate_charge_C']-1),.005)
                self.assertGreater(m['channel_overlap_on_J'],0)
    def test_gate_overlap_sampling_convergence(self):
        for v in [40,150]:
            a=gate_switch(v,125,81)['metrics'];b=gate_switch(v,125,321)['metrics']
            for k in ['channel_overlap_on_J','channel_overlap_off_J']:
                self.assertLess(abs(a[k]/b[k]-1),.001)
    def test_recovery_charge_all_voltage_temperature_cases(self):
        for v in VINS:
            for temp in TEMPS:
                d=recovery_pulse(v,temp)
                self.assertAlmostEqual(np.trapezoid(d['irr'],d['t'])/d['qrr'],1,places=13)
                self.assertAlmostEqual(d['peak']*d['trr']/2,d['qrr'],places=20)
    def test_deadtime_volt_seconds_and_current_periodicity(self):
        for v in VINS:
            for temp in TEMPS:
                d=deadtime_buck(v,temp);m=d['metrics']
                self.assertLess(abs(m['volt_second_residual_Vs']),1e-18)
                self.assertLess(abs(m['periodic_current_residual_A']),1e-12)
                self.assertAlmostEqual(m['mean_IL_A'],1,places=13)
                self.assertGreater(m['minimum_IL_A'],0)
                self.assertTrue(np.all(d['state_HS_on']+d['state_LS_on']+d['state_deadtime']==1))
    def test_zero_deadtime_reduces_to_ideal_buck(self):
        d=deadtime_buck(100,25,dead_s=0)
        self.assertAlmostEqual(d['metrics']['duty_fraction'],.12)
        self.assertAlmostEqual(d['metrics']['diode_deadtime_loss_W'],0)
        self.assertAlmostEqual(d['metrics']['ripple_IL_A'],(100-12)*.12/(250e3*100e-6),places=12)

class AuxiliaryTests(unittest.TestCase):
    def test_bootstrap_reaches_analytical_periodic_map(self):
        for v in VINS:
            for temp in TEMPS:
                for c in [100e-9,3.3e-9]:
                    d=bootstrap(v,temp,cboot=c)
                    self.assertLess(abs(d['metrics']['last_cycle_min_V']-d['metrics']['steady_min_V']),1e-10)
                    self.assertGreater(d['metrics']['minimum_simulated_V'],0)
    def test_bootstrap_gate_charge_jump(self):
        d=bootstrap(150,125,cboot=3.3e-9)
        self.assertAlmostEqual((d['vbs'][0]-d['vbs'][1])*3.3e-9,d['metrics']['Qgate_C'],places=20)
        self.assertLess(d['metrics']['UVLO_margin_V'],0)
        self.assertGreater(bootstrap(150,125)['metrics']['UVLO_margin_V'],0)
    def test_level_shift_charge_balance(self):
        for r in [500,20000]:
            d=level_shift(150,receiver_r=r,points=40001);c=230e-15
            injected=np.trapezoid(d['iinj'],d['t']);removed=np.trapezoid(d['ir'],d['t'])
            self.assertLess(abs(injected-removed-c*d['rx'][-1])/(30e-15*150),1e-7)
    def test_level_shift_limit_and_stronger_sink(self):
        for v in VINS:
            weak=level_shift(v);strong=level_shift(v,receiver_r=500)
            peak=weak['metrics']['peak_receiver_disturbance_V']
            self.assertLessEqual(peak,30/230*v)
            self.assertGreater(weak['metrics']['threshold_crossed'],0)
            self.assertEqual(strong['metrics']['threshold_crossed'],0)
    def test_sense_step_against_analytic_crossing(self):
        for temp in TEMPS:
            d=current_sense(temp);m=d['metrics'];cross=m['analog_crossing_time_s'];rs=m['sense_resistance_ohm'];offset=m['amplifier_offset_V']
            y0=20*rs*.5+offset;y1=20*rs*3+offset
            self.assertAlmostEqual(y1+(y0-y1)*np.exp(-(cross-100e-9)/100e-9),2,places=12)
            self.assertAlmostEqual(m['trip_time_s']-cross,35e-9,places=20)
            idx=np.flatnonzero(d['trip'])[0]
            self.assertLess(abs(d['t'][idx]-m['trip_time_s']),2e-9+1e-18)
    def test_startup_first_enable_against_capacitor_ramp(self):
        for v in VINS:
            for temp in TEMPS:
                d=startup_uvlo(v,temp);m=d['metrics'];ideal=9e-6/(m['start_current_limit_A']-40e-6)
                self.assertLess(abs(m['first_enable_s']-ideal),4e-6)
    def test_uvlo_brownout_restart_and_hysteresis(self):
        for v in VINS:
            for temp in TEMPS:
                d=startup_uvlo(v,temp);m=d['metrics'];self.assertGreaterEqual(m['enable_events'],2);self.assertGreaterEqual(m['brownout_events'],1)
                rise=np.flatnonzero(np.diff(d['enabled'])>0)+1;fall=np.flatnonzero(np.diff(d['enabled'])<0)+1
                self.assertTrue(np.all(d['vaux'][rise]>=9));self.assertTrue(np.all(d['vaux'][fall]<=7))
                self.assertLessEqual(m['peak_Vaux_V'],11.)
    def test_startup_time_step_refinement(self):
        a=startup_uvlo(150,125,dt=2e-6);b=startup_uvlo(150,125,dt=1e-6)
        self.assertLess(abs(a['metrics']['first_enable_s']-b['metrics']['first_enable_s']),3e-6)
        self.assertLess(np.max(abs(a['vaux']-b['vaux'][::2])),.003)

class PowerControlTests(unittest.TestCase):
    def test_series_rlc_critical_resistance_and_decay(self):
        for v in VINS:
            for label in ['weak','damped']:
                d=ringing(v,label);m=d['metrics']
                self.assertAlmostEqual(m['Rcritical_series_ohm'],2*np.sqrt(m['Lpar_H']/m['Clinearized_F']))
                self.assertTrue(np.all(np.diff(d['energy'])<=1e-20))
                self.assertLess(abs(m['energy_residual_J']),1e-10)
    def test_rlc_damping_removes_energy_faster(self):
        a=ringing(150,'weak');b=ringing(150,'damped')
        self.assertLess(b['energy'][-1],a['energy'][-1]*1e-8)
    def test_loss_budget_sum_and_no_reused_full_switch_energy(self):
        d=loss_budget();m=d['metrics'];p=d['parts']
        self.assertEqual(set(p),{'high_side_conduction_W','low_side_conduction_W','inductor_copper_W','channel_overlap_W','Coss_commutation_W','recovery_bus_estimate_W','gate_driver_supply_W','deadtime_diode_W','assumed_control_supply_W'})
        self.assertAlmostEqual(sum(p.values()),m['total_loss_W'],places=12)
        self.assertAlmostEqual(p['Coss_commutation_W'],m['Coss_hard_commutation_J']*FS,places=12)
        self.assertAlmostEqual(m['Coss_upper_discharge_J']+m['Coss_lower_charging_loss_J'],m['Coss_hard_commutation_J'],places=15)
        q=recovery_pulse(100,m['steady_hot_node_C'])['qrr']
        self.assertAlmostEqual(p['recovery_bus_estimate_W'],100*q*FS,places=12)
        self.assertAlmostEqual(m['estimated_efficiency'],12/(12+sum(p.values())),places=12)
    def test_matched_half_bridge_coss_source_minus_storage(self):
        for vin in VINS:
            v=np.linspace(0,vin,100001);c=capacitance(v)
            stored=np.trapezoid(v*c,v);bus_energy=vin*np.trapezoid(c,v)
            m=coss_hard_commutation(vin)
            self.assertAlmostEqual(m['Coss_upper_discharge_J']/stored,1,places=8)
            self.assertAlmostEqual(m['Coss_lower_charging_loss_J']/(bus_energy-stored),1,places=8)
            self.assertAlmostEqual(m['Coss_hard_commutation_J']/bus_energy,1,places=8)
            self.assertGreater(m['Coss_lower_charging_loss_J'],0)
    def test_thermal_fixed_point_and_constant_loss_solution(self):
        for v in VINS:
            for temp in TEMPS:
                d=loss_budget(v,temp);m=d['metrics']
                self.assertLess(abs(m['thermal_fixed_point_residual_K']),1e-8)
                self.assertGreater(m['steady_hot_node_C'],temp)
                np.testing.assert_allclose(d['temperature'],temp+m['total_loss_W']*8*(1-np.exp(-d['t']/.2)),rtol=1e-13)
                self.assertEqual(m['parameter_temperature_range_exceeded'],0)
    def test_controlled_buck_all_voltage_temperature_cases(self):
        for v in VINS:
            for temp in TEMPS:
                d=controlled_buck(v,temp);m=d['metrics']
                self.assertGreater(m['pre_step_output_V'],11.7)
                self.assertLess(m['peak_output_V'],12.1)
                self.assertLessEqual(m['maximum_IL_A'],1.60001)
                self.assertAlmostEqual(m['final_output_V'],1.6*6,places=5)
                self.assertLess(m['maximum_duty'],.9)
                self.assertLess(abs(m['integrated_energy_residual_J']),2e-7)
    def test_averaged_control_step_refinement_and_energy(self):
        a=controlled_buck(150,125,dt=1e-6,save_stride=1);b=controlled_buck(150,125,dt=.5e-6,save_stride=1)
        self.assertLess(np.max(abs(a['voltage']-b['voltage'][::2])),.006)
        self.assertLess(abs(b['metrics']['integrated_energy_residual_J']),abs(a['metrics']['integrated_energy_residual_J']))

class ArtifactTests(unittest.TestCase):
    def test_case_counts_finiteness_and_plot_lengths(self):
        d=json.loads((ROOT/'results/simulation_v32.json').read_text(encoding='utf-8'));self.assertEqual(len(d['models']),9);self.assertEqual(len(d['cases']),153)
        self.assertEqual(len(set(c['id']for c in d['cases'])),153)
        for c in d['cases']:
            self.assertTrue(np.isfinite(c['x']).all());self.assertTrue(np.isfinite(list(c['metrics'].values())).all())
            self.assertIsNone(c['port_power_W']);self.assertEqual(c['terminals'],[])
            for s in c['signals']:self.assertEqual(len(s['y']),len(c['x']));self.assertTrue(np.isfinite(s['y']).all())
            for p in c['plots']:
                self.assertEqual(len({s['unit']for s in p['series']}),1,'Single-axis plots must not mix units: '+c['id'])
                for s in p['series']:self.assertEqual(len(s['y']),len(p['x']));self.assertTrue(np.isfinite(s['y']).all())
    def test_bilingual_metadata_and_metric_dictionary(self):
        d=json.loads((ROOT/'results/simulation_v32.json').read_text(encoding='utf-8'));labels=json.loads((ROOT/'models/metric_labels_zh.json').read_text(encoding='utf-8'))
        for m in d['models']:
            for k in ['name_en','name_zh','equation_en','equation_zh','limits_en','limits_zh']:self.assertTrue(m[k])
            self.assertTrue(m['source_ids']);self.assertTrue(m['parameters'])
        for c in d['cases']:
            for k in c['metrics']:self.assertIn(k,labels);self.assertTrue(labels[k])

if __name__=='__main__':unittest.main(verbosity=2)
