# V3-3 shared package

# V3-3分享包

The 2026-11-07 sharing package extracts into **V3-3** and adds `global-fab-processes`. The simulation content remains the v3.3.0 baseline. The older dated ZIP is preserved as the original release snapshot.

2026-11-07分享包解压后的目录为 **V3-3**，新增`global-fab-processes`工艺目录；仿真内容沿用v3.3.0基线。旧日期ZIP保留为原发布快照。

Extract all files together and open index.html. Keep the v33/education assets beside the viewer. Every model has an English GIF and a static poster; Excel links to the published GIFs and displays posters, native charts and formula-based error reduction. Numerical values remain authored examples, not measured or PDK-calibrated devices.

将全部文件一起解压后打开index.html，保留v33/education资源。每项模型有英文GIF与静态海报；Excel链接已发布GIF，并展示海报、原生图表及误差下降公式。数值仍为人为示例，不是实测或PDK校准器件。

The package includes current V3.3 data/code and preserved V3/V3.2 source/JSON needed to reproduce the comparisons. It omits historical CSV duplicates, older workbooks/ZIPs and V1/V2 trees. Old historical relative links may require the full repository. No paper PDFs or private research caches are included. Check V3-3/package_manifest.json for current SHA-256 hashes; v33/validation/release_manifest.json records the original dated simulation release.

包内含当前V3.3数据/源码及复现对比所需的V3/V3.2源码与JSON；省略历史CSV副本、旧工作簿/ZIP和V1/V2目录。历史相对链接可能需要完整仓库。不含论文PDF或私有研究缓存。当前SHA-256见V3-3/package_manifest.json；v33/validation/release_manifest.json记录原日期的仿真发布。

Catalogue revision **2.0** expands the original 25 entities / 49 records to **59 entities / 119 records**, retaining the original 49 records and adding 70. It includes 118 technical, manufacturing, research or context records and one corporate-history record. The offline catalogue supports eight filters, up to three records side by side, source links, bookmarks and CSV export. The process workbook contains Catalogue, Evidence, Gaps and Guide sheets. Published development, pilot, production and historical states remain distinct.

目录修订版 **2.0** 由原25个主体/49条记录扩展至 **59个主体/119条记录**，保留原49条并新增70条。其中118条属于技术、制造、研究或背景资料，1条属于企业沿革。离线目录支持8类筛选、最多3条并排对比、来源链接、书签与CSV导出；工艺Excel包含目录、依据、缺口、指南四表，并区分开发、试产、量产及历史阶段。

No exhaustive worldwide completeness rate is claimed. The 28 gap items document unresolved evidence, scope exclusions and candidates not reviewed in this edition. This research update does not change numerical models or assert new PDK/silicon calibration.

不声称覆盖全球全部工艺；28项缺口记录尚缺依据、范围排除及本版未核对候选。本次研究更新不修改数值模型，也不增加PDK或实测校准声明。

**Printing edition 1.0 (2026-11-07): [75 egg-size STL teaching models](printable-models/README.md).** Each file corresponds to a documented catalogue entry; devices, passive parts, isolation/interconnect structures, mechanisms and circuit benches remain distinct. Models have 60 × 42 mm footprints and enlarged tactile features. [Download the printing bundle](Semiconductor_Teaching_STL_20261107.zip).

**打印版1.0（2026-11-07）：[75份鸡蛋大小STL教学模型](printable-models/README.md)。** 每份对应明确目录条目，区分器件、无源、隔离/互连结构、机理及电路台；底面60×42毫米，细节为教学放大。[下载打印资料包](Semiconductor_Teaching_STL_20261107.zip)。

The printable source catalogue and referenced legacy geometry are included so the teaching mapping can be inspected. STL uses millimetres by interpretation; select mm and 100% scale in a slicer. These static models do not add semiconductor physics or change numerical accuracy claims.

包内包含打印源目录及引用的历史几何，便于检查教学映射。STL按毫米解释，请在切片软件选择mm与100%比例；静态模型不新增半导体物理机制或改变数值准确性声明。

The complete sharing edition uses two archives: extract the core package to create **V3-3**, then extract **Semiconductor_Teaching_STL_20261107.zip inside that V3-3 folder**. The printing archive also works independently for printing. Its source files overlap some core dependencies with identical bytes; merge folders and keep the matching versions. Both archives and all individual files are available in the repository.

完整分享版采用两个压缩包：先解压核心包得到 **V3-3**，再将 **Semiconductor_Teaching_STL_20261107.zip解压到该V3-3文件夹内部**。打印包也可独立用于打印；其部分源文件与核心依赖字节一致，合并目录并保留匹配版本即可。仓库同时保存两个压缩包及全部单独文件。
