# Numerical accuracy and remaining limits

# 数值准确性与尚存限制

The requested “10% improvement” is evaluated as `100 × (old benchmark error − new benchmark error) / old benchmark error` for each explicitly defined benchmark. This is relative error reduction, not an increase of ten percentage points in a physical accuracy score. Missing PDK/measured data prevent that latter claim for every model.

“提升10%”按每项明确定义的基准计算为`100×(旧基准误差−新基准误差)/旧基准误差`，含义是误差相对下降，并非物理准确率增加10个百分点。缺少PDK/实测数据，无法对所有模型证明后者。

Result: 12 numerical targets met, 7 numerical-floor cases, 1 separately classified sampling-uncertainty case. Numerical errors are calculated against independent high-precision formulas, conservation identities or convergence-checked reference integration. These references test the retained equations, not their fit to silicon.

结果：12项数值目标达标、7项数值精度下限、1项单列采样不确定度。误差对照独立高精度公式、守恒恒等式或经收敛检查的参考积分；这些基准检验保留方程，不检验其与硅片的拟合。

## Per-model comparison

## 逐模型比较

Columns contain the stated error metric (absolute, normalized or relative as shown by the unit); A04 contains asymptotic standard error instead. Full references, numerical floors, domains and case-level comparisons are in [the JSON audit](presentation/accuracy_audit.json) and the family audit files.

列中为注明的误差指标，按单位区分绝对、归一化或相对误差；A04为渐近标准误。完整基准、数值底限、适用域及工况级比较见[JSON审计](presentation/accuracy_audit.json)及各系列审计文件。

| Model | Benchmark / 基准 | Old / 旧 | New / 新 | Unit / 单位 | Reduction % / 下降比例 | Status / 状态 |
|---|---|---:|---:|---|---:|---|
| A01 | Maximum relative gm error on 78 retained transfer-grid probes<br>原转移曲线78个探针点的最大gm相对误差 | 1.8342937e-08 | 5.3290705e-15 | relative | 99.999971 | target_met |
| A02 | Maximum relative charge error in a near-zero numerical stress test<br>近零电压数值压力测试的最大电荷相对误差 | 1 | 4.4408921e-16 | relative | 100 | target_met |
| A03 | Maximum normalized terminal KCL residual<br>最大归一化端口KCL残差 | 1.3418344e-16 | 1.3418344e-16 | relative | N/A | numerical_floor |
| A04 | Asymptotic relative sampling SE of estimated Gaussian pair sigma<br>高斯配对标准差估计的渐近相对抽样标准误 | 0.005000125 | 0.0025000156 | relative_SE | 50.000938 | statistical_uncertainty |
| B01 | Maximum relative ideal-tail current residual<br>理想尾电流最大相对残差 | 6.7762636e-16 | 6.7762636e-16 | relative | N/A | numerical_floor |
| B02 | Maximum reference-voltage error against simplified analytic sum<br>相对简化解析合成式的最大基准电压误差 | 2.220446e-16 | 2.220446e-16 | V | N/A | numerical_floor |
| B03 | Maximum RMS noise integration error across six band integrals<br>六个带内积分的最大噪声均方根误差 | 2.5376405e-13 | 1.6940659e-21 | V_rms | 99.999999 | target_met |
| B04 | Maximum absolute DNL of the ideal SAR<br>理想SAR的最大绝对DNL | 1.010303e-13 | 1.010303e-13 | LSB | N/A | numerical_floor |
| B05 | Maximum unity-gain crossing-frequency error<br>最大单位增益交越频率误差 | 0.077675755 | 9.094947e-13 | Hz | 100 | target_met |
| B06 | Maximum sampled phase-step error over three damping ratios<br>三种阻尼比的最大采样相位阶跃误差 | 3.7433324e-11 | 2.7755576e-17 | rad | 99.999926 | target_met |
| B07 | Maximum periodic mean-output-voltage error across 18 cases<br>18个工况的最大周期平均输出电压误差 | 1.3249693e-08 | 7.1054274e-14 | V | 99.999464 | target_met |
| P01 | On/off overlap-energy quadrature error<br>导通/关断交叠能量积分误差 | 1.2966582e-10 | 7.4115383e-22 | J | 100 | target_met |
| P02 | Periodic inductor volt-second balance residual<br>周期电感伏秒平衡残差 | 2.7105054e-20 | 2.7105054e-20 | V s | N/A | numerical_floor |
| P03 | Periodic bootstrap minimum-voltage residual<br>周期自举最低电压残差 | 1.7763568e-15 | 1.7763568e-15 | V | N/A | numerical_floor |
| P04 | Analytical RC disturbance peak error<br>解析RC扰动峰值误差 | 8.8817842e-16 | 8.8817842e-16 | V | N/A | numerical_floor |
| P05 | Exported comparator transition timing error<br>导出比较器跳变时刻误差 | 1.4772991e-09 | 0 | s | 100 | target_met |
| P06 | First UVLO-enable timing error<br>首次欠压锁定使能时刻误差 | 1.4339623e-06 | 1.7347235e-18 | s | 100 | target_met |
| P07 | Integrated damping-energy error<br>阻尼耗散能量积分误差 | 1.1754713e-12 | 1.8409318e-14 | J | 98.433878 | target_met |
| P08 | Total loss numerical evaluation error<br>总损耗数值计算误差 | 9.2458955e-05 | 4.4408921e-16 | W | 100 | target_met |
| P09 | Maximum output-voltage trajectory error<br>输出电压轨迹最大误差 | 0.0029373093 | 5.7071582e-07 | V | 99.98057 | target_met |

`target_met` means the stated numerical benchmark meets the 10% criterion. `numerical_floor` means no meaningful percentage is assigned to an already analytic/roundoff-limited calculation. `statistical_uncertainty` is not counted as improved deterministic or physical accuracy.

`target_met`表示注明的数值基准满足10%标准；`numerical_floor`表示既有解析/浮点受限计算不赋予有意义提升比例；`statistical_uncertainty`不计入确定性或物理准确度改善。

## Audit cautions that change interpretation

## 影响解读的审计要点

- A02: the near-zero charge stress domain is separate from the original CV plot. Eliminating cancellation is numerical robustness, not a measured capacitance upgrade.

  A02：近零电荷压力测试范围与原CV曲线分开；消除相消属于数值稳健性，不是实测电容升级。
- A04: four times as many Gaussian draws reduce asymptotic sigma-estimator standard error by about 50%. The realized relative sigma error changes from about 0.040% to 0.389% in this fixed-seed run. It is explicitly not claimed to be a 10% accuracy improvement.

  A04：高斯样本量增加四倍，使标准差估计渐近标准误下降约50%；固定种子本次实现的标准差相对误差由约0.040%变为0.389%。明确不声称其准确度提升10%。
- P05: the exported sampled transition improves; the old analytic delay metric was already exact. P06 exact segments are limited to the verified constant-current compliance range. P09 is an averaged current-reference limiter, not transistor switching or cycle-by-cycle protection.

  P05：改进的是导出采样跳变时刻，旧解析延迟指标原已精确；P06精确分段仅适用于已验证恒流顺从范围；P09为平均电流参考限幅，不是晶体管开关或逐周期保护。
- P08: the same nine-part loss budget remains. Matched-pair Coss hard commutation is Vin·Qoss; all losses feed one effective shared hot node, not an individual MOS junction. Better quadrature does not validate the assumed component values or efficiency.

  P08：保留九项损耗预算；匹配双管Coss硬换流为Vin·Qoss。全部损耗归入一个共享等效热节点，不是单管结温。更精确积分不证明假定器件值或效率正确。
- Large percentages can correspond to tiny absolute changes. Consult units and the old error before interpreting a 99.999% numerical reduction.

  大比例可能对应极小绝对变化；解读99.999%数值下降前须查看单位与旧误差量级。

## Reproducibility evidence

## 可复现证据

- [Analog implementation and audit](numerics/analog/README.md), [executed tests](numerics/analog/validation.json)
- [DC/DC implementation and audit](numerics/dcdc/README.md), [executed tests](numerics/dcdc/validation.json)
- [Preserved-model regression](validation/legacy_checks.json)
- [GIF manifest with source hashes](education/manifest.json)

Numerical background: cancellation-aware exponential differences are documented by [NumPy expm1](https://numpy.org/doc/2.0/reference/generated/numpy.expm1.html); matrix-exponential methods are discussed in the [SciPy linear-algebra documentation](https://docs.scipy.org/doc/scipy/tutorial/linalg.html). These are numerical-method references, not semiconductor calibration sources, and SciPy is not required by this release.

数值背景：[NumPy expm1](https://numpy.org/doc/2.0/reference/generated/numpy.expm1.html)说明小量指数差的精度问题；[SciPy线性代数文档](https://docs.scipy.org/doc/scipy/tutorial/linalg.html)讨论矩阵指数方法。这些是数值方法参考，不是半导体校准来源，本版运行不依赖SciPy。

To establish physical accuracy, obtain authorized models or measured I–V/C–V/gate-charge/recovery/thermal/transient data with uncertainty, fit on one set and validate on a separate set over voltage/current/temperature. A single percentage cannot replace the per-quantity error budget. Conceptual diagrams and English GIFs do not solve process-scale electric fields or current density.

要建立物理准确性，需要授权模型或带不确定度的I–V/C–V/栅电荷/恢复/热及瞬态实测数据，分别用于拟合与独立验证，并覆盖电压、电流、温度。单一百分比不能替代逐量误差预算；概念图与英文GIF不求解工艺尺度电场或电流密度。
