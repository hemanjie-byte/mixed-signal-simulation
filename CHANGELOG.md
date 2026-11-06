# V3-3 · Printable teaching edition 1.0 — 2026-11-07

**Printing edition 1.0 (2026-11-07): [75 egg-size STL teaching models](printable-models/README.md).** Each file corresponds to a documented catalogue entry; devices, passive parts, isolation/interconnect structures, mechanisms and circuit benches remain distinct. Models have 60 × 42 mm footprints and enlarged tactile features. [Download the printing bundle](Semiconductor_Teaching_STL_20261107.zip).

**打印版1.0（2026-11-07）：[75份鸡蛋大小STL教学模型](printable-models/README.md)。** 每份对应明确目录条目，区分器件、无源、隔离/互连结构、机理及电路台；底面60×42毫米，细节为教学放大。[下载打印资料包](Semiconductor_Teaching_STL_20261107.zip)。

Adds 75 individual binary STL files, final-geometry previews, an offline atlas and source/terminal mappings. Geometry is validated independently from STL; physical printing is not claimed. GitLab CI definitions cover the FAB catalogue and printable artifacts; GitHub workflows are retained. Simulation v3.3.0 and FAB catalogue 2.0 are preserved.

新增75份独立二进制STL、由最终几何生成的预览、离线图册及来源/端口映射。从STL独立核验几何，不声称已实物试打。新增GitLab目录与打印资料检查配置，保留GitHub工作流；仿真v3.3.0及FAB目录2.0保持不变。

# V3-3 · Global FAB catalogue revision 2.0 — 2026-11-06

Catalogue revision **2.0** expands the original 25 entities / 49 records to **59 entities / 119 records**, retaining the original 49 records and adding 70. It includes 118 technical, manufacturing, research or context records and one corporate-history record. The offline catalogue supports eight filters, up to three records side by side, source links, bookmarks and CSV export. The process workbook contains Catalogue, Evidence, Gaps and Guide sheets. Published development, pilot, production and historical states remain distinct.

目录修订版 **2.0** 由原25个主体/49条记录扩展至 **59个主体/119条记录**，保留原49条并新增70条。其中118条属于技术、制造、研究或背景资料，1条属于企业沿革。离线目录支持8类筛选、最多3条并排对比、来源链接、书签与CSV导出；工艺Excel包含目录、依据、缺口、指南四表，并区分开发、试产、量产及历史阶段。

No exhaustive worldwide completeness rate is claimed. The 28 gap items document unresolved evidence, scope exclusions and candidates not reviewed in this edition. This research update does not change numerical models or assert new PDK/silicon calibration.

不声称覆盖全球全部工艺；28项缺口记录尚缺依据、范围排除及本版未核对候选。本次研究更新不修改数值模型，也不增加PDK或实测校准声明。

# V3-3 sharing and global FAB catalogue — 2026-11-06

The current sharing entry and extracted package folder are named V3-3. A separately sourced global FAB public-process catalogue is added. Simulation equations, numerical data and the v3.3.0 tag are preserved.

当前分享入口与解压后的文件夹统一命名为V3-3，新增独立核对来源的全球FAB公开工艺目录。保留仿真方程、数值数据及v3.3.0标签。

# V3.3.0 — 2026-11-03

All 20 models gain individual English GIFs with diagrams and data plots. All 211 cases regenerated. 12 numerical-error benchmarks meet the 10% relative-reduction target; 7 roundoff/analytic-floor cases and 1 sampling-only case are separately reported. 96 checks pass. Workbook/viewer add per-model animation access and auditable before/after errors. Physical accuracy remains unverified.

20项模型均补齐英文GIF，包含图示与数据曲线；211工况重跑。12项数值误差基准满足相对下降10%的目标；7项解析/浮点下限及1项仅统计采样分别报告。96项检查通过。工作簿和演示页增加逐模型动画入口及前后误差核算。物理准确性仍未验证。

# V3.2.0 — 2026-11-03

Nine DC/DC mechanism benches add 153 cases; total 20 model views/211 cases. Nonlinear gate charge, matched-pair Coss commutation, recovery, bootstrap, level shift, low-side sensing, startup/UVLO, series-RLC damping, loss/thermal accounting and average-current-limited control are explicit. 61 implementation checks pass. New evidence: four papers/eight manufacturer documents; original TOP200/182-paper V3.1 audit is preserved. Added English-only GIF, bilingual undergraduate lesson, and upgraded Excel/offline viewer. No PDK, silicon fitting or physical 3D field claim.

9项DC/DC机理测试台增加153工况，合计20项模型视图/211工况。明确非线性栅电荷、双管Coss换流、恢复、自举、移位、低侧检测、启动/欠压、串联RLC阻尼、损耗/热节点及平均限流控制。61项实现检查通过。新核对4篇论文/8份厂商文档；保留TOP200/182篇的V3.1审计。新增英文GIF、双语大学生课程，升级Excel及离线演示。无PDK、实测拟合或三维物理场认证。

# Changelog

# 更新记录

## V3.1.0 — 2026-11-02

Re-audited all 200 representative associations; replaced 16 people and four papers. Current evidence: 182 distinct analog-related papers, 22 affiliation regions, explicit circuit/method/component scope, reading depth and conservative model links.

重新审计200条代表关联；替换16位人员和4篇论文。当前182篇模拟相关论文、22个机构背景地区；明确电路/方法/元件范围、阅读层级及从严模型关联。

Corrected SAR transition/endpoint INL and FFT DC/Nyquist power. Reran 58 current cases with 36 passing tests, plus 600 historical cases and six V1 buck examples. Updated bilingual viewer, model cards, Excel and audit records.

修正SAR转换边界/端点INL及FFT直流/奈奎斯特功率；重跑58个当前工况并通过36项测试，另重跑历史600工况及6个V1 Buck示例。同步双语演示、模型卡、Excel与审计记录。

## V3.0.0 — 2026-11-01

- Refocused the cohort on semiconductor and analog IC research: 200 people, 184 distinct DOI papers, 20 affiliation countries/regions. Added explicit selection decisions and reconciliation with the former TOP100; 23 former entries remain.
- Checked all 184 DOI bibliographic records. Five key papers received targeted primary-source reading; reading depth, identity limitations and unmodeled mechanisms are recorded separately.
- Added four device/parameter extensions and seven circuit benchmarks, with 58 computed cases, 110 selectable plots and 11 conceptual 3D views. All 29 recorded analytical, numerical and research-data checks passed.
- Added an English-first / Chinese-below interface, methods, model cards, reviewer guide, bibliography, raw CSV data and a 22-sheet Excel workbook with 12 editable charts.
- Preserved V1/V2 as historical artifacts. No PDK, measured-device calibration, TCAD field solution or paper-circuit reproduction is claimed.

- 名单围绕半导体与模拟芯片重新筛选，形成200人、184篇不同DOI论文、20个国家/地区机构背景；增加筛选决定和旧TOP100对照，旧名单保留23人。
- 核对全部184条DOI题录；5篇关键论文定向阅读原始来源，分别记录阅读层级、身份关联局限和未建模机制。
- 增加4项器件/参数增强和7个电路测试台，包含58个工况、110组可选曲线、11个概念3D视图；记录的29项解析、数值和研究数据检查通过。
- 新增英文在前、中文在下的界面、方法、模型卡、审阅指南、参考文献、原始CSV，以及含12张可编辑图表的22表Excel。
- V1/V2作为历史交付保留。本版不声称PDK、实测器件校准、TCAD场求解或论文电路复现。

The entries below are retained historical notes in their original language.

以下为按原语言保留的历史记录。

## V2 — 2026-11-01

- 找回既有TOP100，逐人筛查代表论文，补齐4条缺失，形成100行可追溯台账。
- 重点核对24篇原始来源，标明实际阅读范围。
- 新增25类器件、6项机制及168工况；重新执行原版432工况。
- 新增31个3D结构、端口V/I/功率与状态演示、CSV导出、模型代码和完整结果。
- 更新Excel并保留原版内容；增加数值、收敛、浏览器及工作簿校核记录。

## V1 — 2026-11-01

公开工艺资料、24类器件、432工况、六档理想Buck与离线3D演示。

The complete sharing edition uses two archives: extract the core package to create **V3-3**, then extract **Semiconductor_Teaching_STL_20261107.zip inside that V3-3 folder**. The printing archive also works independently for printing. Its source files overlap some core dependencies with identical bytes; merge folders and keep the matching versions. Both archives and all individual files are available in the repository.

完整分享版采用两个压缩包：先解压核心包得到 **V3-3**，再将 **Semiconductor_Teaching_STL_20261107.zip解压到该V3-3文件夹内部**。打印包也可独立用于打印；其部分源文件与核心依赖字节一致，合并目录并保留匹配版本即可。仓库同时保存两个压缩包及全部单独文件。
