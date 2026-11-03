"""Numerical upgrades of the unchanged V3 reduced analog equations.

No PDK, parameter fitting, additional device physics or physical-accuracy claim.
Uses NumPy and the Python standard library only.
"""
from pathlib import Path
import importlib.util
import sys
import numpy as np

sys.dont_write_bytecode = True  # Import historical source without creating cache files there.

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
spec = importlib.util.spec_from_file_location("v33_baseline_analog", REPO / "v3/models/analog_models.py")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def mos_small_signal(vg, vd, vs=0., vb=0., temp_c=25.):
    """Analytic partial derivatives of exactly the retained DC interpolation."""
    ut = old.thermal_voltage(temp_c)
    n = 1.5
    beta = 1e-3 * ((temp_c + 273.15) / old.T0) ** -1.5
    vth = .55 - .001 * (temp_c - 25)
    vg, vd, vs, vb = np.broadcast_arrays(vg, vd, vs, vb)
    vp = (vg - vb - vth) / n
    xs = (vp - (vs - vb)) / (2 * ut)
    xd = (vp - (vd - vb)) / (2 * ut)
    sp_s = np.logaddexp(0, xs)
    sp_d = np.logaddexp(0, xd)
    ds = 2 * sp_s * np.exp(-np.logaddexp(0, -xs))
    dd = 2 * sp_d * np.exp(-np.logaddexp(0, -xd))
    pref = 2 * n * beta * ut ** 2
    shape = sp_s ** 2 - sp_d ** 2
    mult = 1 + .03 * np.abs(vd - vs)
    gm = pref * (ds - dd) / (2 * ut * n) * mult
    gds = pref * (dd / (2 * ut) * mult + shape * .03 * np.sign(vd - vs))
    gmb = pref * (ds - dd) * (1 - 1 / n) / (2 * ut) * mult
    return gm, gds, gmb


def junction_qc(v, temp_c=25.):
    """Rationalized m=1/2 depletion charge, avoiding 1-sqrt(1-small)."""
    v = np.asarray(v, dtype=float)
    if np.any(v >= .35) or np.any(v < -20):
        raise ValueError("Junction demonstration range is -20 <= V < 0.35 V")
    phi = .7
    c0 = 2e-12 * (1 + 2e-4 * (temp_c - 25))
    root = np.sqrt(1 - v / phi)
    return 2 * c0 * v / (1 + root), c0 / root


def mismatch_samples(area_um2, samples=80000, rho=.25, seed=20261101):
    """More independent Gaussian draws, not a new mismatch law or fitted yield."""
    return old.mismatch_samples(area_um2, samples, rho, seed)


def noise_integrals(temp_c=25., low=1., high=1e6):
    e2 = 1e-16 * (temp_c + 273.15) / old.T0
    plain = e2 * ((high - low) + 100 * np.log(high / low))
    suppressed = e2 * (2 * (high - low) + 100 * np.log((high + 20000) / (low + 20000)))
    return float(np.sqrt(plain)), float(np.sqrt(suppressed))


def expm2(matrix, time):
    """Real Cayley-Hamilton 2x2 exponential, including under/overdamped roots."""
    a = np.asarray(matrix, dtype=float)
    t = np.asarray(time, dtype=float)
    half_trace = (a[0, 0] + a[1, 1]) / 2
    b = a - half_trace * np.eye(2)
    delta2 = ((a[0, 0] - a[1, 1]) / 2) ** 2 + a[0, 1] * a[1, 0]
    if delta2 > 0:
        delta = np.sqrt(delta2)
        cf = np.cosh(delta * t)
        sf = np.sinh(delta * t) / delta
    elif delta2 < 0:
        delta = np.sqrt(-delta2)
        cf = np.cos(delta * t)
        sf = np.sin(delta * t) / delta
    else:
        cf = np.ones_like(t)
        sf = t
    return np.exp(half_trace * t)[..., None, None] * (cf[..., None, None] * np.eye(2) + sf[..., None, None] * b)


def affine_states(matrix, forcing, initial, time):
    steady = -np.linalg.solve(matrix, forcing)
    return steady + np.einsum("...ij,j->...i", expm2(matrix, time), np.asarray(initial) - steady)


def ldo_response(temp_c=25., dt=1e-7, end=300e-6):
    c = 10e-6
    r = 90.
    g = .5 * ((temp_c + 273.15) / old.T0) ** -1.2
    wa = 2 * np.pi * 20000
    matrix = np.array([[-1 / (r * c), 1 / c], [-wa * g, -wa]])
    forcing = np.array([-.01 / c, 0.])
    t = np.arange(int(round(end / dt)) + 1) * dt
    states = affine_states(matrix, forcing, [0., 0.], t)
    f = np.geomspace(10, 1e7, 600)
    s = 2j * np.pi * f
    loop = g / ((c * s + 1 / r) * (1 + s / wa))
    # |L(jw)|=1 gives a quadratic in w^2; stable positive-root evaluation.
    qa = c * c / wa ** 2
    qb = c * c + 1 / (r * r * wa ** 2)
    qc = 1 / r ** 2 - g * g
    w2 = -2 * qc / (qb + np.sqrt(qb * qb - 4 * qa * qc))
    unity = np.sqrt(w2) / (2 * np.pi)
    lu = g / ((c * 2j * np.pi * unity + 1 / r) * (1 + 2j * np.pi * unity / wa))
    return dict(t=t, vout=1.8 + states[:, 0], ipass=.02 + states[:, 1],
                iload=.03 + states[:, 0] / r, matrix=matrix, forcing=forcing,
                states=states, f=f, loop=loop, dc_deviation=-.01 / (g + 1 / r),
                unity_hz=unity, phase_margin=180 + np.angle(lu, deg=True))


def pll_psd(freq, zeta):
    wn = 2 * np.pi * 1e5
    s = 2j * np.pi * freq
    h = wn * wn / (s * s + 2 * zeta * wn * s + wn * wn)
    svco = 1e-16 * (1 + (1e5 / freq) ** 2 + (1e4 / freq) ** 3)
    return h, np.abs(h) ** 2 * 1e-13 + np.abs(1 - h) ** 2 * svco


def pll_noise_variance(zeta, order=16, intervals=32):
    """Composite Gauss-Legendre integral in log-frequency; plots stay 1000 points."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    edges = np.linspace(np.log(100), np.log(1e7), intervals + 1)
    half = np.diff(edges) / 2
    x = (edges[:-1] + edges[1:])[:, None] / 2 + half[:, None] * nodes
    freq = np.exp(x)
    _, psd = pll_psd(freq, zeta)
    return float(np.sum(half[:, None] * weights * psd * freq))


def pll_response(zeta=.7, dt=2e-8):
    wn = 2 * np.pi * 1e5
    t = np.arange(int(round(40e-6 / dt)) + 1) * dt
    matrix = np.array([[0., 1.], [-wn * wn, -2 * zeta * wn]])
    states = affine_states(matrix, np.array([0., wn * wn * .1]), [0., 0.], t)
    f = np.geomspace(100, 1e7, 1000)
    h, psd = pll_psd(f, zeta)
    return dict(t=t, phase=states[:, 0], frequency_error=states[:, 1] / (2 * np.pi),
                f=f, h=h, noise=psd, jitter_s=np.sqrt(pll_noise_variance(zeta)) / (2 * np.pi * 1e9))


def buck_response(vin=100., temp_c=25., steps_per_cycle=200, cycles=40, keep_cycles=5):
    """Exact periodic affine states; Gauss integration independent of saved density.

    Same forced-CCM/conduction-only equations and all original coefficients.
    Startup is not added: periodic initialization removes the need to numerically
    traverse the historical 35 identical warmup cycles.
    """
    if vin not in [40, 60, 80, 100, 120, 150]:
        raise ValueError("Vin must be a documented input class")
    if not 0 < keep_cycles <= cycles:
        raise ValueError("Require 0 < keep_cycles <= cycles")
    l, c, rload, period = 100e-6, 22e-6, 12., 1 / 250e3
    rs = .18 * (1 + .004 * (temp_c - 25))
    rl = .12 * (1 + .004 * (temp_c - 25))
    duty = (12 + rs + rl) / vin
    matrix = np.array([[-(rs + rl) / l, -1 / l], [1 / c, -1 / (rload * c)]])
    bon = np.array([vin / l, 0.])
    ton, toff = duty * period, (1 - duty) * period
    eon, eoff = expm2(matrix, ton), expm2(matrix, toff)
    increment = np.linalg.solve(matrix, (eon - np.eye(2)) @ bon)
    initial = np.linalg.solve(np.eye(2) - expm2(matrix, period), eoff @ increment)
    endon = affine_states(matrix, bon, initial, ton)
    tt, states, gates = [], [], []
    for cycle in range(keep_cycles):
        for on, duration, offset, start in [(1, ton, 0., initial), (0, toff, ton, endon)]:
            n = max(1, int(np.ceil(duration / (period / steps_per_cycle))))
            local = np.linspace(0., duration, n + 1)
            tt.extend(cycle * period + offset + local)
            states.extend(affine_states(matrix, on * bon, start, local))
            gates.extend(np.full(n + 1, on))
    t = np.asarray(tt)
    states = np.asarray(states)
    i, v, on = states[:, 0], states[:, 1], np.asarray(gates)
    pin, pout, loss = vin * i * on, v * v / rload, (rs + rl) * i * i
    energy = .5 * l * i * i + .5 * c * v * v
    # Integrate smooth on/off phases, never across the algebraic switching jump.
    nodes, weights = np.polynomial.legendre.leggauss(16)
    integral = np.zeros(4)
    for gate, duration, start in [(1, ton, initial), (0, toff, endon)]:
        local = (nodes + 1) * duration / 2
        y = affine_states(matrix, gate * bon, start, local)
        ci, cv = y[:, 0], y[:, 1]
        values = np.array([cv, gate * vin * ci, cv * cv / rload, (rs + rl) * ci * ci])
        integral += duration / 2 * (values @ weights)
    means = integral / period
    residual = keep_cycles * (integral[1] - integral[2] - integral[3]) - (energy[-1] - energy[0])
    sw = on * vin - rs * i
    return dict(t=t, i=i, v=v, on=on, sw=sw, pin=pin, pout=pout, loss=loss,
                energy=energy, duty=duty,
                metrics=dict(mean_Vout_V=float(means[0]), Vout_ripple_pp_V=float(np.ptp(v)),
                             inductor_ripple_pp_A=float(np.ptp(i)),
                             conduction_only_efficiency=float(means[2] / means[1]),
                             mean_conduction_loss_W=float(means[3]), energy_residual_J=float(residual),
                             max_high_side_Vds_V=float(np.max(vin - sw)),
                             max_low_side_Vds_V=float(np.max(sw)), duty_fraction=float(duty)))
