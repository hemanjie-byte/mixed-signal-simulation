"""Independent references, physical identities and export compatibility checks."""
import hashlib
import json
from pathlib import Path
import unittest
import numpy as np
import numerics as nm
import reference as ref

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


class DeviceNumerics(unittest.TestCase):
    def test_analytic_mos_derivatives_against_decimal_difference(self):
        for temp in [-40, 25, 125]:
            for vg, vd, vb in [(.1, 1.2, 0.), (.9, .3, -.2), (1.5, 1.2, .2), (.9, 0., 0.)]:
                values = nm.mos_small_signal(vg, vd, vb=vb, temp_c=temp)
                for variable, actual in zip(["vg", "vd", "vb"], values):
                    expected = ref.mos_derivative_decimal(vg, vd, temp, variable, vb)
                    self.assertLess(abs(float(actual) - expected), 3e-13 * abs(expected) + 2e-28)

    def test_mos_reference_shift_invariance_of_derivatives(self):
        original = nm.mos_small_signal(.9, 1.2, .1, -.2, 25)
        shifted = nm.mos_small_signal(1.6, 1.9, .8, .5, 25)
        np.testing.assert_allclose(original, shifted, rtol=5e-14, atol=1e-20)

    def test_near_zero_charge_against_high_precision(self):
        for temp in [-40, 25, 125]:
            for v in [-1e-18, 1e-18, -1e-12, 1e-12, -.01, .3]:
                actual = float(nm.junction_qc(v, temp)[0])
                expected = ref.junction_charge_decimal(v, temp)
                self.assertLess(abs(actual / expected - 1), 1e-14)
        self.assertEqual(float(nm.junction_qc(0)[0]), 0.)

    def test_charge_capacitance_identity_and_validity_domain(self):
        v = np.linspace(-10, .3, 121)
        h = 1e-5
        dq = (nm.junction_qc(v + h)[0] - nm.junction_qc(v - h)[0]) / (2 * h)
        self.assertLess(np.max(abs(dq / nm.junction_qc(v)[1] - 1)), 3e-9)
        for vbad in [-21, .35, 1.]:
            with self.assertRaises(ValueError):
                nm.junction_qc(vbad)

    def test_sampling_size_and_gaussian_sigma_are_separate(self):
        for area in [1, 4, 16, 64]:
            a, b, delta, sigma = nm.mismatch_samples(area)
            self.assertEqual(len(delta), 80000)
            self.assertLess(abs(np.std(delta, ddof=1) / sigma - 1), .015)
            np.testing.assert_allclose(a - b, delta, atol=2e-17, rtol=1e-12)
        self.assertLess(1 / np.sqrt(2 * (80000 - 1)), 1 / np.sqrt(2 * (20000 - 1)))


class CircuitNumerics(unittest.TestCase):
    def test_noise_integrals_against_decimal_antiderivatives(self):
        for temp in [-40, 25, 125]:
            for suppressed, actual in enumerate(nm.noise_integrals(temp)):
                expected = ref.noise_rms_decimal(temp, bool(suppressed))
                self.assertLess(abs(actual / expected - 1), 5e-15)

    def test_matrix_exponential_against_decimal_taylor(self):
        matrices = [nm.ldo_response(25)["matrix"], np.array([[0., 1.], [-4e11, -4e5]]),
                    np.array([[0., 1.], [-4e11, -2e6]]), np.array([[-2., 1.], [0., -2.]])]
        for matrix in matrices:
            for time in [0., 1e-8, 1e-6, 1e-5]:
                expected = np.array([[float(x) for x in row] for row in ref.expm2_decimal(matrix, time)])
                actual = nm.expm2(matrix, time)
                np.testing.assert_allclose(actual, expected, rtol=3e-13, atol=2e-13)

    def test_ldo_crossing_and_affine_state_initial_condition(self):
        for temp in [-40, 25, 125]:
            d = nm.ldo_response(temp)
            self.assertLess(abs(d["unity_hz"] - ref.ldo_unity_decimal(temp)), 3e-11)
            np.testing.assert_allclose(d["states"][0], [0., 0.], atol=1e-17)
            g = .5 * ((temp + 273.15) / nm.old.T0) ** -1.2
            w = 2 * np.pi * d["unity_hz"]
            gain = g / ((10e-6 * 1j * w + 1 / 90) * (1 + 1j * w / (2 * np.pi * 20000)))
            self.assertLess(abs(abs(gain) - 1), 2e-15)

    def test_pll_phase_against_independent_decimal_exponential(self):
        for z in [.3, .7, 1.2]:
            d = nm.pll_response(z)
            for k in [0, 1, 20, 100, 333, 1000, 2000]:
                expected = ref.pll_phase_decimal(z, d["t"][k])
                self.assertLess(abs(d["phase"][k] - expected), 1e-15)

    def test_pll_quadrature_refinement_and_positive_variance(self):
        for z in [.3, .7, 1.2]:
            base = nm.pll_noise_variance(z)
            fine = nm.pll_noise_variance(z, order=32, intervals=64)
            self.assertGreater(base, 0)
            self.assertLess(abs(base / fine - 1), 3e-14)

    def test_buck_periodicity_and_average_balance_all_cases(self):
        for vin in [40, 60, 80, 100, 120, 150]:
            for temp in [-40, 25, 125]:
                d = nm.buck_response(vin, temp)
                self.assertLess(abs(d["metrics"]["mean_Vout_V"] - 12), 2e-11)
                self.assertLess(abs(d["metrics"]["energy_residual_J"]), 1e-16)
                self.assertLess(abs(d["i"][-1] - d["i"][0]), 1e-11)
                self.assertLess(abs(d["v"][-1] - d["v"][0]), 1e-11)
                self.assertTrue(np.any(np.diff(d["t"]) == 0))
                self.assertTrue(0 < d["metrics"]["conduction_only_efficiency"] < 1)

    def test_buck_integrated_metrics_independent_of_display_density(self):
        coarse = nm.buck_response(150, 125, steps_per_cycle=50)
        normal = nm.buck_response(150, 125, steps_per_cycle=200)
        for metric in ["mean_Vout_V", "conduction_only_efficiency", "mean_conduction_loss_W", "energy_residual_J"]:
            self.assertAlmostEqual(coarse["metrics"][metric], normal["metrics"][metric], places=14)

    def test_buck_energy_against_independent_eigen_simpson_reference(self):
        for vin, temp in [(40, -40), (150, 125)]:
            l, c, rload, period = 100e-6, 22e-6, 12., 4e-6
            total_r = .30 * (1 + .004 * (temp - 25))
            duty = (12 + total_r) / vin
            a = np.array([[-total_r / l, -1 / l], [1 / c, -1 / (rload * c)]])
            vals, vectors = np.linalg.eig(a)
            inverse = np.linalg.inv(vectors)
            def ev(t):
                t = np.asarray(t)
                return np.einsum("ij,...j,jk->...ik", vectors, np.exp(t[..., None] * vals), inverse).real
            bon = np.array([vin / l, 0.])
            ton, toff = duty * period, (1 - duty) * period
            en, ef = ev(ton), ev(toff)
            inc = np.linalg.solve(a, (en - np.eye(2)) @ bon)
            initial = np.linalg.solve(np.eye(2) - ef @ en, ef @ inc)
            end_on = en @ initial + inc
            integrals = np.zeros(3)
            for gate, duration, start in [(1, ton, initial), (0, toff, end_on)]:
                t = np.linspace(0, duration, 4097)
                steady = -np.linalg.solve(a, gate * bon)
                state = steady + np.einsum("...ij,j->...i", ev(t), start - steady)
                i, v = state[:, 0], state[:, 1]
                values = np.array([gate * vin * i, v * v / rload, total_r * i * i])
                integrals += duration / 4096 / 3 * (values[:, 0] + values[:, -1] + 4 * values[:, 1:-1:2].sum(axis=1) + 2 * values[:, 2:-1:2].sum(axis=1))
            actual = nm.buck_response(vin, temp)["metrics"]
            self.assertLess(abs(actual["conduction_only_efficiency"] - integrals[1] / integrals[0]), 3e-13)
            self.assertLess(abs(actual["mean_conduction_loss_W"] - integrals[2] / period), 3e-12)


class ArtifactAndAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = json.loads((HERE / "simulation.json").read_text(encoding="utf-8"))
        cls.old = json.loads((REPO / "v3/results/simulation_v3.json").read_text(encoding="utf-8"))
        cls.audit = json.loads((HERE / "accuracy_audit.json").read_text(encoding="utf-8"))

    def test_case_identity_schema_and_saved_density(self):
        self.assertEqual(len(self.new["models"]), 11)
        self.assertEqual(len(self.new["cases"]), 58)
        before = {x["id"]: x for x in self.old["cases"]}
        self.assertEqual(set(before), {x["id"] for x in self.new["cases"]})
        for case in self.new["cases"]:
            base = before[case["id"]]
            self.assertEqual(set(case["metrics"]), set(base["metrics"]))
            self.assertEqual(len(case["x"]), len(base["x"]))
            self.assertEqual(len(case["plots"]), len(base["plots"]))
            for p, b in zip(case["plots"], base["plots"]):
                self.assertEqual(len(p["x"]), len(b["x"]))
            self.assertEqual([s["name"] for s in case["signals"]], [s["name"] for s in base["signals"]])
        self.assertLess((HERE / "simulation.json").stat().st_size, 20_000_000)

    def test_all_exported_values_finite_and_port_power_consistent(self):
        for c in self.new["cases"]:
            self.assertTrue(np.isfinite(c["x"]).all())
            self.assertTrue(np.isfinite(list(c["metrics"].values())).all())
            for s in c["signals"]:
                self.assertEqual(len(s["y"]), len(c["x"]))
                self.assertTrue(np.isfinite(s["y"]).all())
            for p in c["plots"]:
                self.assertTrue(np.isfinite(p["x"]).all())
                for s in p["series"]:
                    self.assertEqual(len(s["y"]), len(p["x"]))
                    self.assertTrue(np.isfinite(s["y"]).all())
            if c["terminals"]:
                current = np.asarray([t["i"] for t in c["terminals"]])
                voltage = np.asarray([t["v"] for t in c["terminals"]])
                self.assertLess(np.max(abs(current.sum(axis=0))), 1e-12)
                np.testing.assert_allclose(c["port_power_W"], (current * voltage).sum(axis=0), rtol=1e-12, atol=1e-14)

    def test_closed_form_floor_models_are_unchanged_within_roundoff(self):
        before = {x["id"]: x for x in self.old["cases"]}
        epsilon_guard = 64 * np.finfo(float).eps
        for c in self.new["cases"]:
            if c["model_id"] in ["A03", "B01", "B02", "B04"]:
                b = before[c["id"]]
                for actual, prior in zip(c["signals"], b["signals"]):
                    self.assertEqual((actual["name"], actual["unit"]), (prior["name"], prior["unit"]))
                    scale = max(np.max(abs(np.asarray(prior["y"]))), 1e-30)
                    np.testing.assert_allclose(actual["y"], prior["y"], rtol=0., atol=epsilon_guard * scale)
                for key, actual in c["metrics"].items():
                    if key == "max_KCL_residual_A":
                        scale = max(np.max(abs(np.asarray(t["i"]))) for t in b["terminals"])
                    elif "LSB" in key:
                        scale = 1024.  # Full-scale voltage rounding expressed in LSB.
                    else:
                        scale = max(1., abs(b["metrics"][key]))
                    self.assertLessEqual(abs(actual - b["metrics"][key]), epsilon_guard * scale)

    def test_audit_statuses_and_claim_boundaries(self):
        self.assertEqual(len(self.audit), 11)
        improvements = [x for x in self.audit if x["status"] == "verified_numerical_improvement"]
        floor = [x for x in self.audit if x["status"] == "not_applicable_roundoff_floor"]
        statistical = [x for x in self.audit if x["status"] == "statistical_uncertainty"]
        self.assertEqual((len(improvements), len(floor), len(statistical)), (6, 4, 1))
        for row in improvements:
            self.assertGreater(row["old_error"], row["new_error"])
            self.assertGreater(row["old_error"], row["comparison_floor"])
            self.assertGreaterEqual(row["improvement_pct"], 10.)
            self.assertGreaterEqual(row["improvement_above_floor_pct"], 10.)
        for row in floor:
            self.assertIsNone(row["improvement_pct"])
        self.assertEqual(statistical[0]["model_id"], "A04")
        self.assertTrue(next(x for x in self.audit if x["model_id"] == "A02")["diagnostic_only"])
        for row in self.audit:
            for name in ["metric_en", "metric_zh", "reference_en", "reference_zh", "limits_en", "limits_zh"]:
                self.assertTrue(row[name])
            self.assertTrue(row["reference_resolution_en"])
            self.assertTrue(row["reference_resolution_zh"])

    def test_historical_inputs_unchanged_since_generation(self):
        manifest = json.loads((HERE / "baseline_inputs.json").read_text(encoding="utf-8"))
        for row in manifest["files"]:
            self.assertEqual(hashlib.sha256((REPO / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        self.assertTrue(manifest["unchanged_during_run"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
