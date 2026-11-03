"""Regenerate 58 analog cases and measured numerical audit, preserving V3 files.

Run from any directory: python /path/to/v33/numerics/analog/run.py
Requires only NumPy. The retained baseline exporter is redirected inside HERE;
historical v3/v32 files are never written by this entry point.
"""
from pathlib import Path
import csv
import hashlib
import importlib.util
import json
import sys
import numpy as np
import numerics as nm
import reference as ref

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "v3/models"))


def audit_rows(data):
    baseline = json.loads((REPO / "v3/results/simulation_v3.json").read_text(encoding="utf-8"))
    before = {x["id"]: x for x in baseline["cases"]}
    after = {x["id"]: x for x in data["cases"]}
    rows = []

    def add(mid, metric_en, metric_zh, unit, old_error, new_error, reference_en, reference_zh,
            limits_en, limits_zh, status="verified_numerical_improvement", **extra):
        improvement = 100 * (1 - new_error / old_error) if old_error > 0 and status in ("verified_numerical_improvement", "statistical_uncertainty") else None
        rows.append(dict(model_id=mid, metric_en=metric_en, metric_zh=metric_zh, unit=unit,
                         old_error=float(old_error), new_error=float(new_error),
                         improvement_pct=None if improvement is None else float(improvement), status=status,
                         reference_en=reference_en, reference_zh=reference_zh,
                         limits_en=limits_en, limits_zh=limits_zh, **extra))

    errors_old, errors_new = [], []
    derivative_details = {}
    for temp in (-40, 25, 125):
        case = before[f"A01_transfer_{temp}C"]
        probes = np.unique(np.r_[np.arange(0, len(case["x"]), 16), len(case["x"]) - 1])
        for k in probes:
            vg = case["x"][k]
            exact = ref.mos_derivative_decimal(vg, 1.2, temp)
            old_val = case["signals"][1]["y"][k]
            new_val = after[case["id"]]["signals"][1]["y"][k]
            errors_old.append(abs(old_val / exact - 1))
            errors_new.append(abs(new_val / exact - 1))
    add("A01", "Maximum relative gm error on 78 retained transfer-grid probes",
        "原转移曲线78个探针点的最大gm相对误差", "relative",
        max(errors_old), max(errors_new),
        "75-digit Decimal current with independent centered derivative h=1e-16 V; 26 gate points at each of -40/25/125 C.",
        "75位Decimal电流与独立中心差分h=1e-16V；三个温度各26个栅压点。",
        "Accuracy of the existing interpolation's derivative only; no device/PDK accuracy gain or added physics.",
        "仅提升既有插值公式的导数计算精度，不代表器件/PDK准确度或新增物理机制。")

    probes = np.r_[-np.geomspace(1e-18, 1e-6, 49), np.geomspace(1e-18, 1e-6, 49)]
    old_e, new_e = [], []
    for temp in (-40, 25, 125):
        for v in probes:
            exact = ref.junction_charge_decimal(v, temp)
            old_e.append(abs(float(nm.old.junction_qc(v, temp)[0]) / exact - 1))
            new_e.append(abs(float(nm.junction_qc(v, temp)[0]) / exact - 1))
    add("A02", "Maximum relative charge error in a near-zero numerical stress test",
        "近零电压数值压力测试的最大电荷相对误差", "relative", max(old_e), max(new_e),
        "70-digit Decimal evaluation of the original charge equation; 294 probes, |Vj|=1e-18 to 1e-6 V, both polarities and three temperatures.",
        "原电荷方程的70位Decimal参考；294个探针点，|Vj|=1e-18至1e-6V，正负两种极性及三个温度。",
        "Stress-test range is explicitly separate from the original plotted CV sweep; eliminates cancellation, not an across-the-board measured capacitance improvement.",
        "压力测试电压范围与原绘制的CV扫描明确分开；消除数值相消，不表示全部实测电容精度提高。",
        diagnostic_only=True)

    def kcl_error(mid, cases):
        errors = []
        for c in cases.values():
            if c["model_id"] == mid:
                currents = np.asarray([t["i"] for t in c["terminals"]])
                errors.append(float(np.max(np.abs(np.sum(currents, axis=0))) / max(np.max(np.abs(currents)), 1e-30)))
        return max(errors)
    add("A03", "Maximum normalized terminal KCL residual", "最大归一化端口KCL残差", "relative",
        kcl_error("A03", before), kcl_error("A03", after),
        "Exact Ebers-Moll terminal-current conservation: Ic+Ib+Ie=0.", "Ebers-Moll三端电流守恒精确关系：Ic+Ib+Ie=0。",
        "Existing closed-form expm1 evaluation is retained; residual is at floating-point scale. No numerical improvement percentage is assigned.",
        "保留既有expm1解析计算；残差已在浮点精度量级，不赋予数值提升百分比。", "not_applicable_roundoff_floor")

    nold, nnew = 20000, 80000
    add("A04", "Asymptotic relative sampling SE of estimated Gaussian pair sigma",
        "高斯配对标准差估计的渐近相对抽样标准误", "relative_SE",
        1 / np.sqrt(2 * (nold - 1)), 1 / np.sqrt(2 * (nnew - 1)),
        "Delta-method approximation SE(s)/sigma≈1/sqrt(2(N-1)); fourfold samples. This is a sampling-uncertainty estimate, not a deterministic error.",
        "Delta方法近似SE(s)/sigma≈1/sqrt(2(N-1))；样本量增至四倍。此为抽样不确定度估计，不是确定性误差。",
        "Reported separately from numerical accuracy. A single realized sigma estimate may move either direction; no foundry statistics or yield improvement.",
        "与数值准确度分开报告；单次标准差估计可能向任一方向变化，不代表工艺统计或良率改善。", "statistical_uncertainty",
        old_samples=nold, new_samples=nnew,
        observed_sigma_relative_error_old=abs(before["A04_area1um2"]["metrics"]["pair_sigma_observed_V"] / before["A04_area1um2"]["metrics"]["pair_sigma_prediction_V"] - 1),
        observed_sigma_relative_error_new=abs(after["A04_area1um2"]["metrics"]["pair_sigma_observed_V"] / after["A04_area1um2"]["metrics"]["pair_sigma_prediction_V"] - 1))

    add("B01", "Maximum relative ideal-tail current residual", "理想尾电流最大相对残差", "relative",
        kcl_error("B01", before), kcl_error("B01", after),
        "Exact tail condition I1+I2=100 uA on all 1203 saved bias points.", "1203个保存偏置点满足精确尾电流条件I1+I2=100μA。",
        "80 bisection steps already reach double-precision resolution; retained unchanged, no fabricated 10% gain.",
        "80次二分已达到双精度分辨率，保持不变，不虚构10%提升。", "not_applicable_roundoff_floor")

    cb, ca = before["B02_temperature"], after["B02_temperature"]
    idx = np.unique(np.r_[np.arange(0, len(cb["x"]), 20), len(cb["x"]) - 1])
    exact = np.array([ref.bandgap_decimal(cb["x"][k]) for k in idx])
    bo = max(abs(np.asarray(cb["signals"][0]["y"])[idx] - exact))
    bn = max(abs(np.asarray(ca["signals"][0]["y"])[idx] - exact))
    add("B02", "Maximum reference-voltage error against simplified analytic sum", "相对简化解析合成式的最大基准电压误差", "V", bo, bn,
        "70-digit Decimal identity Vref=Vg0+3(k/q)T[1-ln(T/T0)], 34 temperatures.",
        "70位Decimal恒等式Vref=Vg0+3(k/q)T[1-ln(T/T0)]，34个温度点。",
        "Existing analytic evaluation is already at floating-point floor; temperature curvature and physical assumptions are unchanged.",
        "原解析计算已处于浮点精度下限，温度曲率及物理假设不变。", "not_applicable_roundoff_floor")

    eo, en = [], []
    for temp in (-40, 25, 125):
        for key, suppressed in [("plain_integrated_Vrms", False), ("suppressed_integrated_Vrms", True)]:
            exact = ref.noise_rms_decimal(temp, suppressed)
            eo.append(abs(before[f"B03_{temp}C"]["metrics"][key] - exact))
            en.append(abs(after[f"B03_{temp}C"]["metrics"][key] - exact))
    add("B03", "Maximum RMS noise integration error across six band integrals", "六个带内积分的最大噪声均方根误差", "V_rms", max(eo), max(en),
        "70-digit evaluation of elementary PSD antiderivatives over 1 Hz–1 MHz; both spectra and all three temperatures.",
        "1Hz至1MHz PSD初等原函数的70位参考；两个频谱与三个温度。",
        "Saved PSD grid is unchanged; metric integration is analytic. No transistor noise, aliasing or measured amplifier calibration is added.",
        "保存的PSD网格不变，指标积分改为解析式；未增加晶体管噪声、混叠或实测放大器校准。")

    add("B04", "Maximum absolute DNL of the ideal SAR", "理想SAR的最大绝对DNL", "LSB",
        before["B04_ideal"]["metrics"]["DNL_max_abs_LSB"], after["B04_ideal"]["metrics"]["DNL_max_abs_LSB"],
        "Ideal binary CDAC transition widths equal one LSB, hence DNL=0.", "理想二进制CDAC转换码宽为一个LSB，因此DNL=0。",
        "Sequential-decision search and coherent FFT retained. Existing 60-step thresholds are at machine precision; no ENOB/physical accuracy gain is asserted.",
        "保留逐次判决搜索与相干FFT，原60次边界搜索已达机器精度；不声称ENOB或实物准确度提升。", "not_applicable_roundoff_floor")

    eo, en = [], []
    for temp in (-40, 25, 125):
        exact = ref.ldo_unity_decimal(temp)
        eo.append(abs(before[f"B05_{temp}C"]["metrics"]["unity_gain_frequency_Hz"] - exact))
        en.append(abs(after[f"B05_{temp}C"]["metrics"]["unity_gain_frequency_Hz"] - exact))
    add("B05", "Maximum unity-gain crossing-frequency error", "最大单位增益交越频率误差", "Hz", max(eo), max(en),
        "70-digit positive root of the exact |L(jw)|=1 quadratic; three temperatures. Transients separately use exact 2x2 propagation.",
        "精确|L(jw)|=1二次方程正根的70位参考，三个温度；瞬态另采用精确2×2传播。",
        "Removes interpolation/ODE discretization for the retained linear loop; no dropout, current limit, transistor network or measured phase-margin validation.",
        "消除既有线性环路的插值及ODE离散误差；未加入压差、限流、晶体管网络或实测相位裕度验证。")

    eo, en, jitter_checks = [], [], []
    for zeta in (.3, .7, 1.2):
        cb, ca = before[f"B06_zeta{zeta}"], after[f"B06_zeta{zeta}"]
        for k in range(0, len(cb["x"]), 20):
            exact = ref.pll_phase_decimal(zeta, cb["x"][k])
            eo.append(abs(cb["signals"][0]["y"][k] - exact))
            en.append(abs(ca["signals"][0]["y"][k] - exact))
        dense = np.sqrt(nm.pll_noise_variance(zeta, order=32, intervals=64)) / (2 * np.pi * 1e9)
        jitter_checks.append(dict(zeta=zeta, old_error_s=abs(cb["metrics"]["integrated_jitter_s"] - dense),
                                  new_error_s=abs(ca["metrics"]["integrated_jitter_s"] - dense), reference_jitter_s=float(dense)))
    add("B06", "Maximum sampled phase-step error over three damping ratios", "三种阻尼比的最大采样相位阶跃误差", "rad", max(eo), max(en),
        "75-digit matrix-exponential Taylor scaling/squaring, 101 times per damping ratio; independent of the new Cayley-Hamilton implementation.",
        "75位矩阵指数Taylor缩放平方法，每阻尼比101个时刻；独立于新版Cayley-Hamilton实现。",
        "Canonical phase-domain response only. PSD quadrature also refined without enlarging saved traces; no transistor VCO, cycle-slip or measured-jitter accuracy claim.",
        "仅典型相位域响应；PSD积分也细化且不扩大保存曲线，未增加晶体管VCO、周跳或实测抖动准确度。",
        jitter_quadrature_diagnostics=jitter_checks)

    bids = [k for k, c in before.items() if c["model_id"] == "B07"]
    eo = [abs(before[k]["metrics"]["mean_Vout_V"] - 12) for k in bids]
    en = [abs(after[k]["metrics"]["mean_Vout_V"] - 12) for k in bids]
    add("B07", "Maximum periodic mean-output-voltage error across 18 cases", "18个工况的最大周期平均输出电压误差", "V", max(eo), max(en),
        "Independent periodic volt-second/charge balance: <Vout>=Vin*D/(1+(Rsw+RL)/Rload)=12 V for the unchanged duty law.",
        "独立周期伏秒及电荷平衡：<Vout>=Vin*D/(1+(Rsw+RL)/Rload)=12V，沿用原占空比公式。",
        "Exact affine propagation and phasewise Gauss integration improve the reduced conduction-only solution. Saved ripple extrema remain sampled; no switching-loss/real-device accuracy improvement.",
        "精确仿射传播与分段Gauss积分改进仅含导通损耗的简化解；纹波极值仍按保存点取样，不代表开关损耗或实物精度提升。",
        max_energy_residual_old_J=max(abs(before[k]["metrics"]["energy_residual_J"]) for k in bids),
        max_energy_residual_new_J=max(abs(after[k]["metrics"]["energy_residual_J"]) for k in bids))
    # A conservative comparison guard, not a certified roundoff bound: 64 eps
    # allows for the short arithmetic/transcendental evaluation chain. Scales
    # come from the audited quantity, never from the desired improvement ratio.
    eps = float(np.finfo(float).eps)
    phase_scale = max(max(abs(np.asarray(c["signals"][0]["y"]))) for c in after.values() if c["model_id"] == "B06")
    scales = {"A01": 1., "A02": 1., "A03": 1., "B01": 1.,
              "B02": max(abs(np.asarray(after["B02_temperature"]["signals"][0]["y"]))),
              "B03": max(max(nm.noise_integrals(t)) for t in [-40, 25, 125]),
              "B04": 1024.,
              "B05": max(after[f"B05_{t}C"]["metrics"]["unity_gain_frequency_Hz"] for t in [-40, 25, 125]),
              "B06": phase_scale, "B07": 12.}
    scale_reasons = {
        "A01": ("Unit relative derivative scale; audited transfer probes avoid near-cancelling forward/reverse terms.", "单位相对导数尺度；审计的转移探针点不涉及正反项近相消。"),
        "A02": ("Unit relative charge scale; rationalized near-zero denominator remains approximately two.", "单位相对电荷尺度；有理化后近零分母约为2。"),
        "A03": ("Terminal-current conservation is normalized by the largest terminal current.", "端口电流守恒残差按最大端口电流归一化。"),
        "B01": ("Tail-current residual is normalized by the largest terminal current, 100 uA.", "尾电流残差按最大端口电流100μA归一化。"),
        "B02": ("Maximum saved reference voltage sets the voltage scale.", "以保存的最大基准电压作为电压尺度。"),
        "B03": ("Largest RMS value among the six positive band integrals sets the voltage scale.", "以六个正值带内积分中的最大均方根电压作为尺度。"),
        "B04": ("Full-scale binary64 voltage rounding converts to 1024 LSB units for a 10-bit ADC.", "10位ADC满量程双精度电压舍入换算为1024LSB尺度。"),
        "B05": ("Largest unity-crossing frequency sets the scale; the stable positive root is away from the DC-gain-one singular boundary.", "以最大交越频率作为尺度；稳定正根远离直流增益为1的奇异边界。"),
        "B06": ("Maximum saved phase magnitude covers step and overshoot.", "最大保存相位幅度覆盖阶跃与过冲。"),
        "B07": ("12 V output scale multiplied by maximum 2-norm condition number of I-exp(A*T), after scaling states as i/1 A and v/12 V.", "12V输出尺度乘以I-exp(A*T)的最大2范数条件数，状态先归一化为i/1A及v/12V。"),
    }
    conditions = {k: 1. for k in scales}
    scaling = np.diag([1., 12.])
    for temp in [-40, 25, 125]:
        a = np.array([[-.30 * (1 + .004 * (temp - 25)) / 1e-4, -1 / 1e-4],
                      [1 / 22e-6, -1 / (12 * 22e-6)]])
        normalized = np.linalg.solve(scaling, a @ scaling)
        conditions["B07"] = max(conditions["B07"], float(np.linalg.cond(np.eye(2) - nm.expm2(normalized, 4e-6))))
    for row in rows:
        mid = row["model_id"]
        if mid == "A04":
            row.update(comparison_floor=None, characteristic_scale=None, conditioning_factor=None,
                       improvement_above_floor_pct=None,
                       reference_resolution_en="Asymptotic Gaussian sampling-SE formula for the declared sample counts; no deterministic numerical-error floor applies. Not a confidence interval for the realized sample sigma.",
                       reference_resolution_zh="针对声明样本量的渐近高斯抽样标准误公式；不适用确定性数值误差下限，也不是实得样本标准差的置信区间。")
            continue
        floor = 64 * eps * float(scales[mid]) * conditions[mid]
        row.update(comparison_floor=float(floor), comparison_floor_unit=row["unit"],
                   machine_epsilon=eps, roundoff_guard_multiplier=64,
                   characteristic_scale=float(scales[mid]), conditioning_factor=conditions[mid],
                   reference_resolution_en="Practical binary64 comparison guard = 64*epsilon*characteristic_scale*conditioning_factor; not a rigorous error bound or physical tolerance. " + scale_reasons[mid][0],
                   reference_resolution_zh="实用双精度比较保护量=64×机器epsilon×特征尺度×条件因子；不是严格误差界或物理容差。" + scale_reasons[mid][1])
        if row["status"] == "verified_numerical_improvement":
            if row["old_error"] <= floor:
                row["status"] = "not_applicable_roundoff_floor"
                row["improvement_pct"] = None
                row["improvement_above_floor_pct"] = None
            else:
                row["improvement_above_floor_pct"] = 100 * (1 - max(row["new_error"], floor) / row["old_error"])
        else:
            row["improvement_above_floor_pct"] = None
        if row["status"] == "not_applicable_roundoff_floor":
            ids = [key for key, value in before.items() if value["model_id"] == mid]
            row["baseline_artifact_bitwise_equal_on_this_run"] = all(
                before[key]["signals"] == after[key]["signals"] and before[key]["metrics"] == after[key]["metrics"] for key in ids)
    return rows


def write_audit(data):
    rows = audit_rows(data)
    (HERE / "accuracy_audit.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (HERE / "accuracy_audit.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()})
    return rows


def main():
    input_paths = ["v3/models/analog_models.py", "v3/models/run_simulations.py", "v3/results/simulation_v3.json"]
    hashes = {name: hashlib.sha256((REPO / name).read_bytes()).hexdigest() for name in input_paths}
    (HERE / "models").mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("v33_redirected_baseline_export", REPO / "v3/models/run_simulations.py")
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    exporter.ROOT = HERE
    exporter.OUT = HERE
    for name in ["mos_small_signal", "junction_qc", "mismatch_samples", "ldo_response", "pll_response", "buck_response"]:
        setattr(exporter, name, getattr(nm, name))
    exporter.main()
    scratch = HERE / "simulation_v3.json"
    data = json.loads(scratch.read_text(encoding="utf-8"))
    data["version"] = "3.3.0"
    data["date"] = "2026-11-03"
    data["numerical_scope_en"] = "Numerical evaluation upgrades of unchanged reduced equations, not +10% physical-model accuracy. See accuracy_audit.json for metric-specific results and N/A cases."
    data["numerical_scope_zh"] = "提升既有简化方程的数值求解，不代表物理模型准确度提升10%；各指标结果及不适用项见accuracy_audit.json。"
    for model in data["models"]:
        mid = model["id"]
        if mid == "A01":
            model["parameters"]["small_signal_method"] = "Analytic derivatives of the same DC law"
        if mid == "A02":
            model["parameters"]["charge_evaluation"] = "Rationalized m=0.5 expression, unchanged physics"
        if mid == "A04":
            model["parameters"]["samples"] = 80000
        if mid == "B03":
            model["parameters"]["integration_method"] = "Analytic PSD antiderivatives; saved frequency grid unchanged"
        if mid in ["B05", "B06"]:
            model["parameters"]["state_propagation"] = "Exact real 2x2 matrix exponential"
        if mid == "B05":
            model["parameters"]["unity_gain_method"] = "Stable analytic positive quadratic root"
        if mid == "B06":
            model["parameters"]["PSD_integration"] = "16-point Gauss-Legendre per 32 log-frequency intervals"
        if mid == "B07":
            model["equation_en"] = model["equation_en"].replace("event-aligned RK4", "exact piecewise affine propagation and 16-point phasewise Gauss integration")
            model["equation_zh"] = "解析周期映射初始化、精确分段仿射传播及16点Gauss积分；校核输入、输出、导通损耗和储能。"
            model["parameters"]["state_propagation"] = "Exact affine exponential; periodic warmup traversal unnecessary"
            model["parameters"]["metric_integration"] = "16-point Gauss-Legendre separately on on/off intervals"
    for case in data["cases"]:
        if case["model_id"] == "B03":
            plain, suppressed = nm.noise_integrals(case["temp_C"])
            case["metrics"]["plain_integrated_Vrms"] = plain
            case["metrics"]["suppressed_integrated_Vrms"] = suppressed
            case["notes_en"] = "Integrated RMS uses the analytic PSD integral, independently of the unchanged saved 1001-point frequency grid."
            case["notes_zh"] = "均方根指标使用解析PSD积分，与保持不变的1001点频率显示网格独立。"
        elif case["model_id"] == "A04":
            case["metrics"]["sample_count"] = 80000
            case["notes_en"] = "Metrics/histogram use 80000 independent Gaussian draws; first512 displayed. More samples reduce sampling uncertainty, not physical-model error; one realized estimate need not improve."
            case["notes_zh"] = "指标及直方图使用80000个独立高斯样本，仅显示前512点；增加样本降低抽样不确定度，不降低物理模型误差，单次估计不一定更接近真值。"
        elif case["model_id"] in ["B05", "B06", "B07"]:
            case["notes_en"] = "State values use exact linear/affine propagation. Integrated metrics use analytic or phasewise quadrature; display density is preserved. Physical assumptions remain the historical ones."
            case["notes_zh"] = "状态量采用精确线性/仿射传播，积分指标采用解析或分段求积，显示密度保持不变，物理假设沿用历史版本。"
    final = HERE / "simulation.json"
    final.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False), encoding="utf-8")
    scratch.unlink()  # Only this run's redirected temporary JSON, inside HERE.
    (HERE / "models/model_catalog.json").write_text(json.dumps(data["models"], ensure_ascii=False, indent=2), encoding="utf-8")
    rows = write_audit(data)
    (HERE / "metric_labels_zh.json").write_text("{}\n", encoding="utf-8")
    assert all(hashlib.sha256((REPO / name).read_bytes()).hexdigest() == value for name, value in hashes.items())
    (HERE / "baseline_inputs.json").write_text(json.dumps(dict(unchanged_during_run=True, files=[dict(path=name, sha256=value) for name, value in hashes.items()]), indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"models": len(data["models"]), "cases": len(data["cases"]), "bytes": final.stat().st_size,
                      "audits": [{k: r[k] for k in ["model_id", "status", "old_error", "new_error", "improvement_pct"]} for r in rows]}, indent=2))


if __name__ == "__main__":
    if "--audit-only" in sys.argv:
        rows = write_audit(json.loads((HERE / "simulation.json").read_text(encoding="utf-8")))
        print(json.dumps([{k: r.get(k) for k in ["model_id", "status", "comparison_floor", "improvement_above_floor_pct"]} for r in rows], indent=2))
    else:
        main()
