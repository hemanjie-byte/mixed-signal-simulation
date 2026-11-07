# V3-4 validation record

# V3-4 验证记录

The migrated layout passed **96 independent implementation/regression tests**: 36 V3.1 baseline + 25 V3.2 DC/DC + 18 analog numerical + 17 DC/DC numerical tests. The recorded numerical outputs and equation coefficients are retained. See [machine-readable outcomes](regression_validation.json).

迁移后通过 **96项独立实现/回归测试**：36项V3.1基线＋25项V3.2 DC/DC＋18项模拟数值＋17项DC/DC数值测试，保留已有数值输出和方程系数。参见[机器可读结果](regression_validation.json)。

- 20 model GIFs: numerical-source, GIF and poster SHA256 matched; every frame decoded.
- 75 print entries: all 2,025 independent STL geometry/manifest checks passed; source coverage, heightfield hashes and cards/previews matched.
- Offline browser: all 20 models, 211 cases, 40 poster/GIF loads, case/sample controls and 3D rotation worked; no JavaScript errors or horizontal overflow at 1440px/390px.
- Workbook: 36 original sheets, 5,754 formulas/cached results, scientific values, 40 hyperlinks and 21 images retained; one Version guide sheet added. Three original description/title cells changed. Native Excel recalculation was not tested.

- 20项模型GIF：数值来源、GIF和海报SHA256吻合，全部帧解码成功。
- 75项打印条目：2,025项独立STL几何/清单检查全部通过；来源覆盖、高度场哈希及模型卡/预览对应正确。
- 离线浏览器：20模型、211工况、40次海报/GIF加载、工况/采样控制和3D旋转可用；1440px/390px下无JavaScript错误或横向溢出。
- 工作簿：保留原36表、5,754公式/缓存结果、科学数值、40超链接及21图片；新增Version guide表，只改原有3个说明/标题单元格。未测试原生Excel重算。

`python V3-4/validate_layout.py` verifies directory names, current local links and **934** byte-preserved assets/snapshots against the pre-migration commit. FAB metadata is compared separately, permitting only the sharing-version field to change. Run with `--extracted` in a merged core+printing delivery; omitted historical files are reported and never counted as verified.

`python V3-4/validate_layout.py` 核验目录名、当前本地链接及相对于迁移前提交保留的 **934** 份资产/快照字节。FAB元数据单独比较，仅允许分享版本字段变化。合并核心包和打印包后运行时使用`--extracted`；省略的历史文件会单列，不能计入已核验数量。

Package CRCs, every member's bytes and SHA256 inventories are verified during packaging. Original release manifests still describe their original dated tags; [the current package manifest](package_manifest.json) describes this delivery. These checks do not establish silicon/PDK accuracy, new literature coverage or physical print quality.

打包时核验ZIP CRC、逐成员字节及SHA256清单。原发布清单仍对应原日期标签；[当前打包清单](package_manifest.json)对应本版。以上检查不证明硅片/PDK精度、新增文献覆盖或实物打印质量。
