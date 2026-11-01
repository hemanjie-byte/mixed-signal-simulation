# Historical V2 documentation

# V2历史说明

This Chinese-language document records the earlier, broader release. Current analog-focused evidence is in [V3](../README.md).

本中文文档记录原来范围更宽的版本，当前模拟方向证据以[V3](../README.md)为准。

# mixed-signal simulation

## V2 更新 — 2026-11-01

**49类器件 + 6项机制扩展，600个测试工况，另含六档Buck。** 原版资料保留在下方。论文用于识别器件与机制；全部数值参数为演示假设，未进行论文曲线拟合，无晶圆厂PDK。

- [新版Excel](../40至150V_DC_DC工艺器件与仿真_V2.xlsx)：保留原版31页，加入TOP100对照、关键论文、模型假设、全部新增工况指标及31个独立模型页。
- [新版离线3D演示](legacy-viewer.html)：下载后用Edge/Chrome打开。支持旋转结构、选择模型/温度/适用Vin、播放扫描，查看端电压、电流、功率及状态量，导出CSV/图片。
- [V2完整交付包](../mixed-signal-simulation_V2_20261101.zip)：解压后打开index.html；包含两版Excel/HTML、代码、结果、OBJ与论文对照。
- [论文对照与模型缺口报告](论文对照与模型缺口.md) · [100人逐行台账](research/top100_screening.csv) · [24篇关键来源](research/papers.json) · [全部模型参数](models/model_catalog.json)。

### 补充范围

| 类别 | 新增模型 |
|---|---|
| N01–N05 功率器件 | SiC MOSFET、增强型GaN HEMT、硅超结MOSFET、IGBT、SiC JBS |
| N06–N11 新型晶体管 | FinFET、IGZO TFT、有机TFT、MoS2、石墨烯、CNT FET |
| N12–N16 存储与铁电 | FeFET、RRAM、PCM、MTJ、铁电电容 |
| N17–N21、N24–N25 光电与能量转换 | 氮化物LED、量子点LED、PIN光探测器、单结光伏、热电、MZI调制器、激光二极管 |
| N22–N23 无源与互连 | 片上耦合变压器、TSV |
| X01–X06 原器件机制扩展 | 栅电荷/Miller、PN反向恢复、自热、NBTI、噪声、参数统计分散 |

N01–N05：5×6输入×3温度=90工况；N06–N25：20×3=60；X01–X06：6×3=18。新增168；原版432已重新运行。

TOP100来自2026-10-11的内部证据分榜单，并非官方世界排名。逐人筛查代表论文，补齐原缺失4条，共95个不同代表DOI；本轮重点核对24篇原始来源。56人仅题录初筛、18人复用既有出版商摘要、26人关联本轮关键来源。**不等于通读100人全部论文或复现100篇论文。** 逐行记录实际证据层级。

低压、存储和光电器件不可直接连接40–150V功率节点。SiC/GaN/IGBT等是外接功率器件研究对照，不证明BCD平台已提供。650V阻断等级为假设，IGBT及650V器件不是针对40–150V DC/DC的选型建议。

### V2复现与验证

```bash
python -m pip install -r requirements.txt
python 可复现计算/simulate.py
python 可复现计算/finalize_viewer.py
python v2/models/simulate_v2.py
python v2/models/build_geometry.py
python v2/models/build_viewer.py
```

新增结果在`v2/results/`；结构在`v2/models/OBJ/`。Excel与ZIP是本次运行快照，命令不会自动重建。Excel各N/X页为25°C代表工况全采样，功率列有ΣVI公式；完整168工况在HTML/JSON中。修改Excel参数文本不会自动重算非线性模型。

[数值校核](results/validation.json) · [浏览器检查](validation/viewer_validation.json) · [工作簿检查](validation/workbook_validation.json) · [数据与模型约定](数据与模型约定.md)。3D只显示概念结构、电极电压和端电流方向，无局部电场/电流密度/真实尺寸。新增自热为集总模型，不是TCAD热场。校核说明内部一致性，不构成实测精度或工艺签核。

## 原版资料（V1）

40–150V DC/DC 工艺、器件与通用示意仿真资料。首批研究与计算日期：2026-11-01。

研究华虹、芯联集成、东部 DB HiTek，并参考台积电、联电、海力士 system ic 及美格纳历史工艺。40V、60V、80V、100V、120V、150V 均表示 DC/DC 最高输入电压。

## 查看结果

- [Excel 汇总](../40至150V_DC_DC工艺器件与仿真.xlsx)：31 个工作表、27 张可编辑图表、24 张 3D 预览；包含工艺证据、器件需求、计算假设、扫描数据和校核说明。
- [离线 3D 演示](../DC_DC_3D器件演示.html)：下载后用 Edge 或 Chrome 打开。支持旋转结构、选择器件/输入/温度、播放扫描、导出 CSV 和图片。GitHub 文件页面本身不会执行这个 HTML。
- [完整交付包](../DC_DC工艺器件_完整交付_20261101.zip)：原始交付快照，可下载解压使用。
- [使用说明](../使用说明.txt)：模型范围、数据更新与使用方法。
- [24 个独立 OBJ 模型](../3D模型_OBJ/)：归一化结构示意，可在支持 OBJ 的软件中查看。

## 已计算内容

24 类器件 × 6 档最高输入 × 3 个温度点（−40°C、25°C、125°C），共 432 个独立测试。

器件包括高侧/低侧 NLDMOS、PLDMOS、DE-NMOS/PMOS、低压 CMOS、NPN/PNP、PN/自举/肖特基/Zener 二极管、启动 JFET、电阻、MIM/MOM 电容、隔离网络、ESD 等效器件及外接电感/电容。

另含六档输入下的 12V/1A、200kHz 理想 CCM 同步 Buck 示例，展示开关节点、漏源/栅源电压、电感/开关/电容电流、输出纹波与独立损耗估算。

## 复现计算

需要 Python 3 和 NumPy 2.x。在仓库目录执行：

```bash
python -m pip install -r requirements.txt
python 可复现计算/simulate.py
python 可复现计算/finalize_viewer.py
```

第一个脚本更新 `可复现计算/data.json` 和 `device_runs.csv`；第二个脚本重建根目录的离线 HTML。Excel 和 ZIP 是本次已完成交付的快照，上述命令不会自动重建它们。

## 参数与模型边界

没有使用晶圆厂 PDK。所有器件 R、C、Vth、β、温度系数、热阻等数值均为通用演示假设，不代表任一晶圆厂实测性能。器件测试采用解析模型及数值求解，不能用于流片签核或厂商性能排名。

3D 几何无真实工艺尺寸或掺杂信息；色带是端电压线性插值，箭头表示常规电流方向。未求解 Poisson、载流子输运、局部电场、电流密度或自热，不能视为 TCAD 结果。

电压筛选示例采用 15% 尖峰和 90% 工作等级利用率，对应 60/80/120/150/200/200V 的模型等级。实际设计需按瞬态、逐端子可靠性限制、SOA、隔离、PVT 与版图寄生重新验证。公开的平台电压范围不等于完整器件型号表或当前可订购状态。

## 来源与校核

- 官方来源链接见 Excel 的“工艺证据”、HTML 的“工艺依据与边界”及 [research.json](../可复现计算/research.json)。
- [validation/](../validation/) 保存原交付的数值、公式及浏览器验证记录。`final_validation.json` 的压缩包文件数和 SHA-256 对应原始交付 ZIP，并非整个 Git 仓库的文件数。
- [SHA256SUMS.txt](../SHA256SUMS.txt) 用于检查主要交付文件与已有结果数据的一致性。
