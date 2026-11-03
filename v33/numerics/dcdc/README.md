# V3.3 DC/DC numerical audit / V3.3 DC/DC 数值审核

Run from the repository root with Python and NumPy:

在仓库根目录使用 Python 与 NumPy 运行：

```text
python -X utf8 v33/numerics/dcdc/run.py
```

This reproduces 153 cases, a nine-row accuracy audit, CSV exports, and executed validation results. The preserved V3.2 files are imported read-only and their hashes are checked. `--reuse-audit` is only for rebuilding presentation data when a matching audit already exists and equations have not changed.

该命令复现153个工况、九行精度审核、CSV导出与实际执行的验证结果。V3.2文件以只读方式导入，并检查其哈希。`--reuse-audit`仅用于已有匹配审核、且方程未改变时重新生成呈现数据。

The quantified target means at least a 10% reduction in a named numerical error, using the same assumed physics and coefficients. It does **not** mean a 10% gain in physical accuracy. No PDK, silicon calibration, measured device data, or hardware efficiency measurement is available.

量化目标指在相同假定物理和系数下，明确指定的数值误差至少降低10%。它**不代表**物理准确度提高10%。本项目无PDK、硅校准、实测器件数据或硬件效率测量。

| Model / 模型 | Compared numerical quantity / 比较的数值量 | Reference / 参考 |
|---|---|---|
| P01 | On/off overlap energy / 导通、关断交叠能量 | Closed-form exponential moments and Miller integrals / 指数矩与Miller积分闭式解 |
| P02 | Periodic volt-second residual / 周期伏秒残差 | Exact zero by the periodic duty equation / 周期占空比方程的精确零值 |
| P03 | Final-cycle minimum versus periodic fixed point / 末周期最低电压与周期不动点 | Analytical affine map, including settling residual / 解析仿射映射，含建立残差 |
| P04 | RC disturbance peak / RC扰动峰值 | Stable analytical ramp response / 数值稳定的解析斜坡响应 |
| P05 | Exported comparator event time / 导出比较器事件时刻 | Analytical threshold crossing plus fixed delay / 解析阈值交越加固定延迟 |
| P06 | First UVLO-enable time / 首次欠压锁定使能时刻 | Capacitor charging time in checked constant-current domain / 经检查恒流工作域的电容充电时间 |
| P07 | Integrated damping energy / 阻尼能量积分 | Initial minus final analytical stored energy / 解析初始与末时刻储能之差 |
| P08 | Total loss evaluation / 总损耗计算 | Closed-form moments and bracketed thermal-root bisection / 闭式矩及有界热根二分求解 |
| P09 | Output-voltage trajectory / 输出电压轨迹 | Independent adaptive Dormand–Prince integration / 独立自适应Dormand–Prince积分 |

`accuracy_audit.json` contains all per-case comparisons, the maximum absolute error, the minimum percentage improvement among comparisons above the declared numerical floor, and reference limitations. P01 has two comparisons per physical case, one for each edge. P09 is compared at the same 801 saved times for all six input voltages and three temperatures; its reference uncertainty is an empirical tighter-tolerance convergence difference, not a rigorous mathematical bound.

`accuracy_audit.json`包含全部逐工况比较、最大绝对误差、超过规定数值底限的比较中最小改善百分比，以及参考方法边界。P01每个物理工况比较两个开关边沿。P09在六种输入电压、三个温度的相同801个保存时刻进行比较；其参考不确定度为收紧容差后的经验收敛差异，并非严格数学上界。

Analytical or roundoff-floor quantities are labeled `numerical_floor`, with `improvement_pct: null`. They are not counted as 10% improvements. A 100% reduction of comparator waveform quantization means an exact event sample was inserted; the originally analytical propagation-delay metric was already exact under the assumed model.

解析值或已达浮点底限的量标记为`numerical_floor`，其`improvement_pct`为空，不计为10%改善。比较器波形量化误差降低100%表示插入了精确事件样本；原本的解析传播延迟指标在假定模型下已精确。

Display density stays near V3.2. P01 overlap, P07 damping energy, and P09 energy balance use internal quadrature rather than trapezoidal integration of the reduced display trace. Recovering the published metric therefore requires rerunning the code, not reintegrating a decimated CSV. Coss, Qrr, overlap, and the nine-term thermal ledger retain their V3.2 separation. The thermal result is one effective shared hot node, never a MOS junction-temperature prediction.

显示密度保持接近V3.2。P01交叠、P07阻尼能量与P09能量平衡使用内部积分，而非对抽取后的显示曲线作梯形积分。因此复现指标应重新运行代码，不能只对抽取CSV重新积分。Coss、Qrr、交叠和九项热预算保持V3.2的分离方式。热结果是共用的等效热节点，不是MOS结温预测。
