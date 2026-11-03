# Analog numerical evaluation — V3.3

# 模拟模型数值计算 — V3.3

This module preserves the **11 V3 analog models, 58 case IDs, physical assumptions, source IDs, signal names, metric names and saved plot densities**. It improves how selected equations are evaluated. It does not establish a 10% improvement in silicon accuracy, process fidelity, noise prediction or device ratings.

本模块保留**V3的11类模拟模型、58个工况编号、物理假设、来源编号、信号名、指标名及保存曲线密度**，改进部分方程的数值计算方法。不证明硅片准确度、工艺保真度、噪声预测或器件额定值改善10%。

Six selected numerical-error metrics meet the requested ≥10% reduction. Four selected metrics are already at floating-point scale and receive no improvement percentage. A04 is separately classified as statistical uncertainty, not numerical or physical-model accuracy. Large percentage reductions often remove errors that were already tiny in practical units; consult both absolute errors and the stated reference before drawing an engineering conclusion.

六项指定数值误差指标达到至少10%的下降；四项已处于浮点精度量级，不赋予提升百分比。A04单列为抽样不确定度，不计入数值或物理模型准确度。较大的百分比下降通常对应实际单位下本来就很小的误差；作工程判断时应同时查看绝对误差和参考定义。

| Model / 模型 | Audited quantity / 审计量 | Old error / 旧误差 | New error / 新误差 |
|---|---|---:|---:|
| A01 | Relative gm error on 78 saved-grid probes / 78个原网格点的gm相对误差 | 1.8343e-8 | 5.3291e-15 |
| A02 | Relative charge error, near-zero stress test only / 仅近零压力测试的电荷相对误差 | 1.0 | 4.4409e-16 |
| B03 | Integrated noise RMS / 带内噪声均方根 | 2.5376e-13 V | 1.6941e-21 V |
| B05 | Unity-gain crossing / 单位增益交越频率 | 0.077676 Hz | 9.0949e-13 Hz |
| B06 | Sampled phase step / 采样相位阶跃 | 3.7433e-11 rad | 2.7756e-17 rad |
| B07 | Periodic mean output / 周期平均输出 | 1.3250e-8 V | 7.1054e-14 V |

The complete [audit JSON](accuracy_audit.json) and [CSV](accuracy_audit.csv) contain one row per model, units, independent references, old/new error, percentage, classification and bilingual limitations. A03, B01, B02 and B04 retain the original numerical outputs. Their N/A status applies to the selected audited metric; it does not prove that every observable or omitted physical effect is exact.

完整[JSON审计](accuracy_audit.json)及[CSV](accuracy_audit.csv)逐模型记录单位、独立参考、前后误差、百分比、分类与双语局限。A03、B01、B02、B04保留原数值输出。“不适用”仅针对选定审计指标，不证明所有可观测量或被省略物理效应精确。

Each deterministic row also declares a **practical numerical comparison floor**: `64 × binary64 epsilon × characteristic scale × conditioning factor`. The factor 64 is a conservative allowance for the short arithmetic/transcendental evaluation chain, not a calibrated accuracy or rigorous mathematical bound. Relative metrics use unit scale; dimensional metrics use their voltage, frequency or phase scale. Ideal ADC rounding is converted from full-scale voltage to 1024 LSB. B07 additionally uses the worst condition number of its period-map solve after nondimensionalizing current by 1 A and voltage by 12 V. The fields disclose every scale and factor. An old error at or below that floor is ineligible for a claimed gain. `improvement_above_floor_pct` substitutes the floor for a smaller measured new error; all six improvements still exceed 10% under this more cautious comparison. A04 has no deterministic numerical floor because its measure is sampling SE.

每个确定性指标还声明**实用数值比较下限**：`64×双精度epsilon×特征尺度×条件因子`。64为短算术及超越函数计算链预留的保守余量，不是校准精度或严格数学误差界。相对指标采用单位尺度，有量纲指标采用对应电压、频率、相位尺度；理想ADC将满量程电压舍入换算成1024LSB。B07另计周期映射求解的最大条件数，电流、电压先按1A、12V无量纲化，字段公开全部尺度和因子。旧误差不高于该下限时不具备宣称提升的资格。`improvement_above_floor_pct`用下限代替更小的新测得误差；六项在此保守比较下仍超过10%。A04为抽样标准误，因此没有确定性数值下限。

## What changes mathematically

## 数学计算如何改进

- **A01:** differentiate the same MOS current interpolation analytically instead of using a fixed finite-difference step. Independent 75-digit current evaluations and centered differences check the derivatives.
- **A02:** rationalize the square-root subtraction for `m=0.5`: `Q=2 C0 V / (1+sqrt(1−V/phi))`. The headline stress test uses `|V|=10^-18…10^-6 V`, outside the saved CV sweep's near-zero sampling. It diagnoses cancellation in arithmetic, not a new physical operating capability.
- **A04:** increase independent Gaussian draws from 20,000 to 80,000. The asymptotic relative standard error of the estimated sigma decreases from about 0.5000% to 0.2500%. In this deterministic seed realization, the observed sigma error actually increases from 0.04017% to 0.38878%; no improvement in that realized estimate is claimed.
- **B03:** integrate the two assumed PSD laws analytically, keeping the original plotted frequency grid.
- **B05/B06:** use the real 2×2 Cayley–Hamilton exponential for the unchanged linear state equations. B05 solves the unity-gain quadratic directly. B06 uses composite Gauss integration in log frequency for the same noise PSD.
- **B07:** evaluate exact on/off affine states from the same periodic initial condition; integrate each smooth switching phase with 16-point Gauss quadrature. The plotted sample density stays unchanged, so displayed ripple extrema remain sampled estimates. A separate eigen-decomposition/Simpson reference checks the energy calculation.

- **A01：**对原MOS电流插值式求解析导数，替代固定步长差分；用独立75位电流计算及中心差分核对。
- **A02：**对`m=0.5`平方根相减有理化，采用`Q=2C0V/(1+sqrt(1−V/phi))`。主要压力测试采用`|V|=10^-18…10^-6V`，不同于原保存CV扫描的近零采样；诊断的是算术相消，不是新的器件工作能力。
- **A04：**独立高斯样本由2万增至8万，标准差估计的渐近相对标准误约由0.5000%降至0.2500%。当前确定性种子下，实得标准差误差反而从0.04017%增至0.38878%，不宣称该单次估计改善。
- **B03：**对两种假设PSD作解析积分，保留原频率显示网格。
- **B05/B06：**对不变的线性状态方程使用实数2×2 Cayley–Hamilton矩阵指数；B05直接求解单位增益二次方程，B06对原PSD在对数频率域作复合Gauss积分。
- **B07：**沿用相同周期初值，精确计算导通、关断仿射状态，各平滑相位采用16点Gauss积分。显示采样密度不变，纹波极值仍属采样估计；另用特征分解及Simpson积分核对能量。

## Reproduction and validation

## 复现与验证

Python and NumPy are sufficient; no SciPy or mpmath dependency is introduced. Run from the repository root:

仅需Python与NumPy，不增加SciPy或mpmath依赖。在仓库根目录执行：

```text
python v33/numerics/analog/run.py
python v33/numerics/analog/validate.py
```

`run.py` redirects the retained exporter inside this directory and generates data plus the accuracy audit. Run `validate.py` afterward to execute the tests against those outputs and replace `validation.json` with the actual results. Historical source/data files are hashed before and after generation; [baseline_inputs.json](baseline_inputs.json) records the unchanged inputs. [simulation.json](simulation.json) is approximately 15.82 MB. CSV traces retain the existing conventions. Original metric names are unchanged, so `metric_labels_zh.json` is an empty extension dictionary.

`run.py`将旧版导出器的写入位置重定向到本目录，生成数据及准确性审计；随后执行`validate.py`，对生成结果运行测试，并用实际结果更新`validation.json`。生成前后核对历史源文件及数据的哈希，[baseline_inputs.json](baseline_inputs.json)记录未改变的输入。[simulation.json](simulation.json)约15.82MB，CSV曲线沿用原约定。指标名称不变，因此`metric_labels_zh.json`为空扩展字典。

All **18 executed checks** pass in [validation.json](validation.json). They cover high-precision derivative/charge references, independent matrix exponentials, PSD quadrature refinement, periodic energy balance, export schema/density, finite values and historical-file preservation. Decimal calculations are independent numerical references, not measurement data. Results near double precision may vary slightly across platforms; they should be interpreted as reaching the numerical floor rather than achieving infinite accuracy.

[validation.json](validation.json)记录实际执行的**18项检查全部通过**，覆盖高精度导数、电荷参考、独立矩阵指数、PSD积分细化、周期能量平衡、导出结构与密度、有限值及历史文件保护。Decimal计算是独立数值参考，不是测量数据。接近双精度下限的结果可能随平台略变，应理解为达到数值下限，而非无限准确。

For the four retained floor models, the audit records whether this run exactly matches the preserved artifact. CI compares values with a declared `64×epsilon×quantity-scale` allowance, because operating-system math libraries can differ by a few last bits. Discrete code changes of one LSB are not hidden by that allowance.

四项保留模型的审计记录本次运行是否与历史文件逐数值完全相同。CI按声明的`64×epsilon×量值尺度`容差比较，以允许不同操作系统数学库的末位差异；该容差不能掩盖1LSB的离散输出码变化。
