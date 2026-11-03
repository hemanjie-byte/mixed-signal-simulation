"""Independent references, before/after measurements, and output integrity."""
from pathlib import Path
import sys,json,hashlib,unittest
import numpy as np
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE))
import improved as m
from reference import gate_overlap_closed,loss_reference

class NumericalTests(unittest.TestCase):
    def test_overlap_closed_form_all_edges_and_temperatures(self):
        for vin in m.VINS:
            for temp in m.TEMPS:
                a=m.gate_switch(vin,temp);ref=gate_overlap_closed(vin,temp)
                for key,value in zip(['channel_overlap_on_J','channel_overlap_off_J'],ref):
                    self.assertLess(abs(a['metrics'][key]-value),1e-18)
                self.assertEqual(len(a['t_on']),len(m.baseline.gate_switch(vin,temp)['t_on']))
    def test_comparator_event_is_exported_without_quantization(self):
        for temp in m.TEMPS:
            d=m.current_sense(temp);event=d['metrics']['trip_time_s'];at=np.flatnonzero(d['t']==event)
            self.assertEqual(len(at),2);np.testing.assert_array_equal(d['trip'][at],[0,1])
            self.assertEqual(d['metrics']['sampled_trip_timing_error_s'],0)
    def test_startup_all_hysteresis_events_and_charge_balance(self):
        for vin in m.VINS:
            for temp in m.TEMPS:
                d=m.startup_uvlo(vin,temp);p=d['metrics'];rise=np.flatnonzero(np.diff(d['enabled'])>0)+1;fall=np.flatnonzero(np.diff(d['enabled'])<0)+1
                np.testing.assert_allclose(d['vaux'][rise],9,atol=2e-12,rtol=0)
                np.testing.assert_allclose(d['vaux'][fall],7,atol=2e-12,rtol=0)
                self.assertEqual(p['enable_events'],2);self.assertEqual(p['brownout_events'],1)
                charge=np.trapezoid(d['isource']-d['iload']-d['iclamp'],d['t'])
                self.assertLess(abs(charge-1e-6*(d['vaux'][-1]-d['vaux'][0])),1e-15)
    def test_startup_domain_rejects_unmodeled_compliance(self):
        with self.assertRaises(ValueError):m.startup_uvlo(12,25)
    def test_startup_solution_independent_of_display_grid(self):
        a=m.startup_uvlo(40,-40,dt=2e-6);b=m.startup_uvlo(40,-40,dt=1e-6)
        self.assertEqual(a['metrics'],b['metrics'])
    def test_ringing_energy_quadrature_refines(self):
        for vin in m.VINS:
            for label in ['weak','damped']:
                a=m.ringing(vin,label);b=m.ringing(vin,label,points=3001)
                self.assertLess(abs(b['metrics']['energy_residual_J']),abs(a['metrics']['energy_residual_J'])*.2+1e-20)
    def test_loss_reference_and_same_coss_ledger_all_cases(self):
        for vin in m.VINS:
            for temp in m.TEMPS:
                d=m.loss_budget(vin,temp);ref,_=loss_reference(vin,temp);p=d['parts'];metrics=d['metrics']
                self.assertEqual(len(p),9);self.assertAlmostEqual(sum(p.values()),metrics['total_loss_W'],places=13)
                self.assertLess(abs(metrics['total_loss_W']-ref),1e-10)
                self.assertAlmostEqual(p['Coss_commutation_W'],vin*m.capacitor_charge(vin)*m.FS,places=12)
                self.assertLess(abs(metrics['thermal_fixed_point_residual_K']),1e-10)
    def test_controller_refinement_and_energy_consistency(self):
        for temp in m.TEMPS:
            a=m.controlled_buck(150,temp);b=m.controlled_buck(150,temp,dt=.25e-6,save_stride=40)
            self.assertEqual(len(a['t']),801);self.assertEqual(len(b['t']),801)
            self.assertLess(np.max(abs(a['voltage']-b['voltage'])),5e-6)
            self.assertLess(abs(a['metrics']['integrated_energy_residual_J']),1e-10)
            self.assertLessEqual(a['metrics']['maximum_IL_A'],1.600001)
            self.assertAlmostEqual(a['metrics']['final_output_V'],9.6,places=6)

class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.audit=json.loads((HERE/'accuracy_audit.json').read_text(encoding='utf-8'));cls.rows={r['model_id']:r for r in cls.audit['rows']}
    def test_six_reducible_numerical_errors_meet_target(self):
        for mid in ['P01','P05','P06','P07','P08','P09']:
            r=self.rows[mid];self.assertEqual(r['status'],'target_met',mid);self.assertGreaterEqual(r['improvement_pct'],10)
            self.assertGreaterEqual(r['minimum_eligible_case_improvement_pct'],10)
            self.assertGreater(r['old_error'],r['absolute_error_floor'])
    def test_analytic_floor_is_not_reported_as_percentage_gain(self):
        for mid in ['P02','P03','P04']:
            r=self.rows[mid];self.assertEqual(r['status'],'numerical_floor');self.assertIsNone(r['improvement_pct'])
            self.assertLessEqual(r['old_error'],r['absolute_error_floor'])
    def test_controller_reference_tolerance_convergence(self):
        r=self.rows['P09'];self.assertLess(r['reference_uncertainty_estimate'],r['absolute_error_floor'])
        self.assertLess(r['reference_uncertainty_estimate'],r['old_error']*.001)
    def test_full_case_coverage(self):
        expected={'P01':18,'P02':18,'P03':36,'P04':12,'P05':3,'P06':18,'P07':12,'P08':18,'P09':18}
        for mid,count in expected.items():
            cases={d['case_id']for d in self.audit['case_details']if d['model_id']==mid}
            self.assertEqual(len(cases),count,mid)
    def test_references_and_scope_are_bilingual(self):
        for r in self.rows.values():
            for key in ['metric_en','metric_zh','reference_en','reference_zh','limits_en','limits_zh']:self.assertTrue(r[key])

class ExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((HERE/'simulation.json').read_text(encoding='utf-8'))
        cls.old=json.loads((m.REPO/'v32/results/simulation_v32.json').read_text(encoding='utf-8'))
    def test_ids_and_schema_preserved(self):
        self.assertEqual(self.data['version'],'3.3.0');self.assertEqual(len(self.data['models']),9)
        self.assertEqual({x['id']for x in self.data['cases']},{x['id']for x in self.old['cases']});self.assertEqual(len(self.data['cases']),153)
        for c in self.data['cases']:
            self.assertIsNone(c['port_power_W']);self.assertEqual(c['terminals'],[])
            self.assertTrue(np.isfinite(list(c['metrics'].values())).all())
            for s in c['signals']:self.assertEqual(len(s['y']),len(c['x']));self.assertTrue(np.isfinite(s['y']).all())
            for p in c['plots']:
                self.assertEqual(len({s['unit']for s in p['series']}),1)
                for s in p['series']:self.assertEqual(len(s['y']),len(p['x']));self.assertTrue(np.isfinite(s['y']).all())
    def test_source_ids_and_physical_parameters_preserved(self):
        old={x['id']:x for x in self.old['models']}
        for model in self.data['models']:
            previous=old[model['id']];self.assertEqual(model['source_ids'],previous['source_ids'])
            for key,value in previous['parameters'].items():
                if model['id']=='P09'and key in ['dt_s','saved_stride_steps']:continue
                self.assertEqual(model['parameters'][key],value)
    def test_complete_metric_dictionary(self):
        labels=json.loads((HERE/'metric_labels_zh.json').read_text(encoding='utf-8'))
        for c in self.data['cases']:
            for key in c['metrics']:self.assertIn(key,labels);self.assertTrue(labels[key])
    def test_preserved_baseline_hashes(self):
        manifest=json.loads((HERE/'run_manifest.json').read_text(encoding='utf-8'));self.assertTrue(manifest['baseline_unchanged'])
        for path,expected in manifest['baseline_sha256'].items():self.assertEqual(hashlib.sha256((m.REPO/path).read_bytes()).hexdigest(),expected)

if __name__=='__main__':unittest.main(verbosity=2)
