# V3.1 package instructions

# V3.1交付包说明

Extract this ZIP before use. Open `index.html` in a local Edge or Chrome browser and open `Mixed_Signal_Simulation_V3_1_EN_ZH.xlsx` in Excel. The interactive viewer works offline. Raw calculations, CSV traces, conceptual OBJ geometry, research records and validation evidence are under `v3/`.

请先解压ZIP。用本地Edge或Chrome打开`index.html`，用Excel打开`Mixed_Signal_Simulation_V3_1_EN_ZH.xlsx`。交互演示可以离线使用。`v3/`下包含计算代码、CSV曲线、概念OBJ几何、研究台账与校核证据。

To rerun the V3 calculations, follow the Python commands in README. The Excel and ZIP are delivery snapshots; those commands regenerate numerical results and the viewer, not the workbook or ZIP. Compare snapshot file hashes with `v3/validation/release_manifest.json`. The manifest excludes itself and this ZIP to avoid circular hashes.

重跑V3计算请遵循README中的Python命令。Excel和ZIP为交付快照；上述命令重新生成数值结果和演示页，不生成工作簿或ZIP。文件快照可与`v3/validation/release_manifest.json`中的校验值比较；清单排除其自身与ZIP，避免循环校验。

V1/V2 files and historical links are available in the [full GitHub repository](https://github.com/hemanjie-byte/mixed-signal-simulation). The ZIP's README includes historical links that require that full checkout. No third-party paper full texts or private research caches are distributed.

V1/V2文件和历史链接见[完整GitHub仓库](https://github.com/hemanjie-byte/mixed-signal-simulation)。包内README中的历史相对链接需要完整仓库。交付包不分发第三方论文全文或私有研究缓存。

Models are illustrative and use assumed parameters. Five key papers received targeted primary-source reading; all 182 papers received DOI bibliographic checks, not full-text replication. Conceptual 3D views do not solve physical fields. Read the model cards and reviewer guide before interpreting numerical accuracy or library coverage.

模型为使用假设参数的示意模型。5篇关键论文定向阅读原始来源；全部182篇核对DOI题录，不代表全文复现。概念3D视图不求解物理场。解释数值精度或器件库覆盖情况前，请阅读模型卡与审阅指南。

V3.1 adds a per-entry analog relevance audit and a full rerun comparison. Read v3/AUDIT_V3_1.md for the 16 person changes, four paper substitutions and SAR/FFT corrections.

V3.1增加逐条模拟相关性审计及完整重跑对比；16位人员变更、4篇论文替换和SAR/FFT修正见v3/AUDIT_V3_1.md。
