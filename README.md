# Mixed-Signal Simulation

# 模拟与混合信号仿真

V3.1.0 · 2026-11-02. Re-audited analog-focused cohort: 200 researchers, 182 distinct representative papers, 22 countries/regions of affiliation context. English first, Chinese below. TOP200 is a curated research cohort, not an official ranking.

V3.1.0 · 2026-11-02。重新审计的模拟方向名单：200位研究人员、182篇不同代表论文、22个国家/地区机构背景。英文在前、中文在下。TOP200为研究名单，不是官方排名。

This revision replaces 16 people whose selected evidence was too broad and four retained authors’ representative papers. All current entries have a documented direct analog connection: 154 circuit/architecture papers, 14 design-method/model papers and 14 component/parasitic papers. It does not present all three types as complete analog IC designs.

本版替换16条旧代表证据范围过宽的人选，并更换4位保留人员的代表论文。当前条目均记录直接模拟关联：154篇电路/架构、14篇设计方法/模型、14篇元件/寄生；不将三类统称为完整模拟芯片设计。

The SAR ADC now searches actual code transitions, uses a specified internal-transition endpoint INL, and corrects one-sided FFT DC/Nyquist weighting. All 58 current cases were rerun; 36 checks pass. Historical reruns cover another 600 device/benchmark cases and six buck examples, matching their previous data exactly. Model parameters remain illustrative: no PDK, measured fit, TCAD fields or paper-circuit reproduction.

SAR ADC改为搜索实际码转换边界，明确内部转换点端点INL定义，并修正单边FFT直流/奈奎斯特功率计权。58个当前工况全部重跑，36项检查通过；另重跑历史600个器件/测试台工况及6个Buck示例，与旧数据完全一致。参数仍为示意假设：无PDK、实测拟合、TCAD场或论文电路复现。

## Open the release

## 查看本版

- [Excel workbook](Mixed_Signal_Simulation_V3_1_EN_ZH.xlsx)<br>
  英文/中文Excel汇总
- [Offline interactive 3D and curves](index.html)<br>
  离线交互3D与曲线
- [V3.1 delivery ZIP](mixed-signal-simulation_V3_1_20261102.zip)<br>
  V3.1交付包
- [200-person ledger](v3/research/people200.csv)<br>
  200人台账
- [182-paper bibliography](v3/research/papers.csv)<br>
  182篇论文题录
- [Analog relevance audit](v3/research/analog_scope_audit.csv)<br>
  逐人模拟相关性审计
- [Previous 200 reconciliation](v3/research/scope_reconciliation_v31.csv)<br>
  旧200人变更对照
- [Audit and rerun report](v3/AUDIT_V3_1.md)<br>
  审计与重跑说明
- [Method and reading depth](v3/METHODOLOGY.md)<br>
  方法与阅读层级
- [Reviewer guide](v3/REVIEWER_GUIDE.md)<br>
  审阅指南
- [Model equations and limits](v3/MODEL_CARDS.md)<br>
  方程与适用边界
- [Foundry context](v3/FOUNDRY_CONTEXT.md)<br>
  晶圆厂背景

Download index.html and open locally in Edge/Chrome, or extract the ZIP. GitHub file previews do not execute HTML. The standalone viewer works offline and shows 11 conceptual 3D models, 58 cases and 110 selectable plots, with terminal voltages/currents/power and CSV/OBJ/PNG export.

下载index.html用本地Edge/Chrome打开，或先解压ZIP。GitHub文件预览不执行HTML。独立演示页可离线查看11个概念3D模型、58个工况、110组曲线，以及端口电压/电流/功率并导出CSV/OBJ/PNG。

| ID | Model | 中文 | Cases / 工况 |
|---|---|---|---:|
| A01 | Four-terminal MOS interpolation | 四端MOS连续插值 | 9 |
| A02 | Junction charge and varactor | 结电荷与变容二极管 | 6 |
| A03 | Reciprocal NPN Ebers–Moll | 满足互易关系的NPN Ebers–Moll | 6 |
| A04 | MOS pair mismatch and correlation | MOS配对失配与相关性 | 4 |
| B01 | MOS differential pair | MOS差分对 | 3 |
| B02 | CTAT/PTAT reference sum | CTAT/PTAT基准合成 | 1 |
| B03 | Input noise and sampled kT/C | 输入噪声与采样kT/C | 3 |
| B04 | Capacitor DAC and SAR ADC | 电容DAC与SAR ADC | 2 |
| B05 | LDO loop and load step | LDO环路与负载阶跃 | 3 |
| B06 | Phase loop and noise transfer | 相位环路与噪声传递 | 3 |
| B07 | 40–150 V synchronous buck | 40–150V同步降压 | 18 |

All 182 DOI records were refreshed; this is not a claim to have read every full text. Five key model papers have targeted original-source reading, with additional scope/byline sources recorded per entry. Only eight papers have restricted mechanism links; zero papers are reproduced. Unmodeled work includes RF front ends, calibrated SiGe HBT, complete chopper/ADC/PLL implementations, start-up/protection, intrinsic MOS charge, reliability and process statistics. Counts are not a percentage of library completeness.

182条DOI全部更新核查，不表示通读全部正文。5篇关键模型论文有定向原始来源阅读，另逐条记录主题/署名补充来源。仅8篇有受限机理关联，论文复现数为零。未完成部分包括射频前端、校准SiGe HBT、完整斩波/ADC/PLL、启动保护、MOS内禀电荷、可靠性与工艺统计；数量不代表库完整度百分比。

## Reproduce

## 复现

```bash
python -m pip install -r v3/requirements.txt
python v3/models/run_simulations.py
python v3/tests/run_validation.py
python v3/models/build_geometry.py
python v3/models/build_viewer.py
```

Recorded environment: Python 3.12.14, NumPy 2.3.5. These commands regenerate calculations and the viewer, not the Excel/ZIP snapshots. Raw traces, tests and file checksums are included in the V3.1 package. Historical V1/V2 files remain in the full repository.

记录环境：Python 3.12.14、NumPy 2.3.5。命令重新生成计算和演示页，不生成Excel/ZIP快照。V3.1包包含原始曲线、测试和文件校验值；历史V1/V2仍在完整仓库。

[Numerical checks / 数值检查](v3/results/validation.json) · [Rerun comparison / 重跑对比](v3/validation/rerun_audit.json) · [Browser QA / 浏览器检查](v3/validation/viewer_validation.json) · [Workbook QA / 工作簿检查](v3/validation/workbook_validation.json)

40–150 V means maximum DC/DC input, not a low-voltage block rating. The V3 buck assumes 250 kHz, 100 uH and 22 uF; efficiency includes conduction loss only. Current is positive into modeled ports and ΣVI includes storage. Unmodeled supply currents remain absent. 3D geometry contains no physical process dimensions or local electric/current-density fields.

40～150V指DC/DC最高输入，不是低压模块额定。V3 Buck假设250kHz、100μH和22μF，效率只含导通损耗。电流流入模型端口为正，ΣVI包含储能；未建模供电电流留空。3D不包含实际工艺尺寸或局部电场/电流密度场。

## Historical releases

## 历史版本

V1/V2 and V3.0 remain historical snapshots with their original broader scope; current analog evidence is defined by V3.1. Legacy numerical reruns do not change literature classification. Third-party papers are linked, not redistributed. No author/foundry endorsement or peer-review approval is implied.

V1/V2和V3.0保留原宽范围历史快照，当前模拟证据以V3.1为准。历史数值重跑不改变文献分类。第三方论文仅提供链接，不分发全文；不暗示作者/晶圆厂背书或同行评审认可。

[V3.0 snapshot / V3.0历史快照](https://github.com/hemanjie-byte/mixed-signal-simulation/tree/v3.0.0) · [V2 viewer / V2演示](v2/legacy-viewer.html) · [Legacy TOP100 reconciliation / 旧100人对照](v3/research/legacy100_reconciliation.csv)
