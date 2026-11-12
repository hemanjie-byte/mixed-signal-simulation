# V3-5 · Learn, inspect, reproduce

# V3-5 · 学习、查看与复现

Download the repository ZIP, extract it, and open **index.html** in Edge or Chrome. Choose **Beginner**, **Undergraduate** or **Graduate**, then a model. GitHub's file preview does not execute HTML; the Markdown lessons remain readable online.

下载仓库 ZIP 并解压，用 Edge 或 Chrome 打开 **index.html**。先选择**入门、本科、研究生**，再选择模型。GitHub 文件预览不运行 HTML；Markdown 课程可直接在线阅读。

| Entry / 入口 | Contents / 内容 |
|---|---|
| [Learning entry / 学习入口](index.html) | Three explanations of the same model, animations and questions / 同一模型的三级解释、动画与问题 |
| [Numerical laboratory / 数值实验室](simulation/index.html) | Voltage/current plots, parameters and case selection / 电压电流曲线、参数与工况选择 |
| [Print gallery / 打印图库](printing/index.html) | 75 enlarged STL teaching entries and three-level explanations / 75 项放大 STL 教学条目及三级解释 |
| [FAB catalogue / FAB 工艺目录](fab/index.html) | 119 public-source records; original review date 2026-11-06 / 119 条公开来源记录，保留 2026-11-06 核对日期 |
| [Compact Excel / 精简 Excel](Mixed_Signal_Simulation_V3-5_EN_ZH.xlsx) | Teaching, model validity, key cases, sources and indices / 教学、模型有效性、关键工况、来源及索引 |
| [Validity review / 有效性复核](evidence/VALIDITY.md) | Per-model limits and executed evidence / 逐项模型边界及执行证据 |

## Read the demonstrations correctly

## 正确理解演示

**40–150 V means maximum DC/DC input voltage**, not the breakdown rating of every device. The low-voltage MOS and junction examples have their own lower voltage domains. A circuit bench is not a qualified physical device. GIFs show sampled computations; 3D/STL geometry is an enlarged teaching concept, not a solved electric-field or current-density distribution. STL units must be interpreted as millimetres; models have a 60 × 42 mm footprint. No printer-specific slicing or physical printing is claimed.

**40～150 V 指 DC/DC 最高输入电压**，不是所有器件的击穿额定值。低压 MOS 和结模型有各自较低的电压适用域。电路测试台不等于经过认证的物理器件。GIF 展示计算采样；3D/STL 是放大教学概念，不是求解得到的电场或电流密度分布。STL 导入时单位选毫米，模型底面为 60 × 42 mm；尚无指定打印机切片或实物打印验证。

## Reproduce the retained equations

## 复现保留的方程

Run from the repository root with Python 3.12. The baseline inputs are retained only because the current models and independent numerical comparisons use them. Bulk CSV files are generated on demand and are omitted from the distributed tree.

在仓库根目录使用 Python 3.12 执行。基线输入仅因当前模型和独立数值比较仍需要而保留；批量 CSV 按需生成，交付目录不重复保存。

```bash
python -m pip install -r V3-5/requirements.txt
python V3-5/simulation/V3-3/numerics/analog/run.py
python V3-5/simulation/V3-3/numerics/dcdc/run.py
python V3-5/simulation/V3-3/numerics/analog/validate.py
python V3-5/simulation/V3-3/validation/run_legacy_checks.py
python V3-5/validate.py
```

Rebuild the numerical viewer with `python V3-5/simulation/V3-3/presentation/build_views.py`; rebuild the learning/printing pages with `python V3-5/build.py`. GIF rendering and mesh generation remain separate reproducible scripts in their respective folders. The original articles retain their own reading-depth records; the new review states which sources were revisited.

用 `python V3-5/simulation/V3-3/presentation/build_views.py` 重建数值演示页，用 `python V3-5/build.py` 重建学习及打印页面。GIF 渲染和网格生成脚本分别保留在相应目录。原始论文保留其实际阅读深度记录，本次复核单独注明重新查阅的来源。
