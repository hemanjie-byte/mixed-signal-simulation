"""Independent high-precision references used only for numerical audit/tests."""
from decimal import Decimal, localcontext
import numpy as np


def dec(value):
    return Decimal(str(value))


def mos_current_decimal(vg, vd, vs=0., vb=0., temp_c=25.):
    with localcontext() as ctx:
        ctx.prec = 75
        vg, vd, vs, vb, tc = map(dec, (vg, vd, vs, vb, temp_c))
        t = tc + dec(273.15)
        ut = dec("1.380649e-23") * t / dec("1.602176634e-19")
        n = dec(1.5)
        beta = dec(.001) * ((t / dec(298.15)).ln() * dec(-1.5)).exp()
        vth = dec(.55) - dec(.001) * (tc - 25)
        vp = (vg - vb - vth) / n
        sf = (1 + ((vp - (vs - vb)) / (2 * ut)).exp()).ln()
        sr = (1 + ((vp - (vd - vb)) / (2 * ut)).exp()).ln()
        return +(2 * n * beta * ut * ut * (sf * sf - sr * sr) * (1 + dec(.03) * abs(vd - vs)))


def mos_derivative_decimal(vg, vd, temp_c, variable="vg", vb=0.):
    with localcontext() as ctx:
        ctx.prec = 70
        h = dec("1e-16")
        args = dict(vg=dec(vg), vd=dec(vd), vb=dec(vb), temp_c=temp_c)
        plus, minus = args.copy(), args.copy()
        plus[variable] += h
        minus[variable] -= h
        return float((mos_current_decimal(**plus) - mos_current_decimal(**minus)) / (2 * h))


def junction_charge_decimal(v, temp_c=25.):
    with localcontext() as ctx:
        ctx.prec = 70
        c0 = dec("2e-12") * (1 + dec("2e-4") * (dec(temp_c) - 25))
        return float(2 * c0 * dec(.7) * (1 - (1 - dec(v) / dec(.7)).sqrt()))


def noise_rms_decimal(temp_c, suppressed=False):
    with localcontext() as ctx:
        ctx.prec = 70
        e2 = dec("1e-16") * (dec(temp_c) + dec(273.15)) / dec(298.15)
        low, high, fc, shift = map(dec, (1, 1e6, 100, 20000))
        band = 2 * (high - low) + fc * ((high + shift) / (low + shift)).ln() if suppressed else high - low + fc * (high / low).ln()
        return float((e2 * band).sqrt())


def ldo_unity_decimal(temp_c):
    with localcontext() as ctx:
        ctx.prec = 70
        pi = dec("3.141592653589793238462643383279502884197169399375105820974944592307816")
        c, r = dec("1e-5"), dec(90)
        g = dec(.5) * (((dec(temp_c) + dec(273.15)) / dec(298.15)).ln() * dec(-1.2)).exp()
        wa = 2 * pi * 20000
        a, b, cc = c * c / (wa * wa), c * c + 1 / (r * r * wa * wa), 1 / (r * r) - g * g
        w2 = (-b + (b * b - 4 * a * cc).sqrt()) / (2 * a)
        return float(w2.sqrt() / (2 * pi))


def bandgap_decimal(temp_c):
    with localcontext() as ctx:
        ctx.prec = 70
        kbq = dec("1.380649e-23") / dec("1.602176634e-19")
        t, t0 = dec(temp_c) + dec(273.15), dec(298.15)
        # Independently simplified CTAT+PTAT sum, retaining the same curvature.
        return float(dec(1.205) + 3 * kbq * t * (1 - (t / t0).ln()))


def _mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def expm2_decimal(matrix, time):
    """75-digit Taylor scaling/squaring; independent of Cayley-Hamilton path."""
    with localcontext() as ctx:
        ctx.prec = 75
        z = [[dec(matrix[i][j]) * dec(time) for j in range(2)] for i in range(2)]
        norm = max(sum(abs(x) for x in row) for row in z)
        squarings = 0
        while norm > dec(.125):
            z = [[x / 2 for x in row] for row in z]
            norm /= 2
            squarings += 1
        total = [[Decimal(int(i == j)) for j in range(2)] for i in range(2)]
        term = [r[:] for r in total]
        for n in range(1, 160):
            term = [[x / n for x in row] for row in _mul(term, z)]
            total = [[total[i][j] + term[i][j] for j in range(2)] for i in range(2)]
            if max(abs(x) for row in term for x in row) < dec("1e-70"):
                break
        else:
            raise RuntimeError("Reference Taylor series did not converge")
        for _ in range(squarings):
            total = _mul(total, total)
        return total


def pll_phase_decimal(zeta, time):
    with localcontext() as ctx:
        ctx.prec = 75
        # Float coefficient conversion isolates equation-solving error from a
        # deliberate change of the retained machine-represented coefficients.
        wn = 2 * np.pi * 1e5
        matrix = [[0., 1.], [-wn * wn, -2 * zeta * wn]]
        e = expm2_decimal(matrix, time)
        return float(dec(.1) * (1 - e[0][0]))
