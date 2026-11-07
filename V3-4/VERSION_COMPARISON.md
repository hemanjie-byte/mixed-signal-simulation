# Version comparison and migration to V3-4

# 版本比较与 V3-4 迁移

V3-4 is the consolidated sharing edition. Its numerical baseline remains **v3.3.0**. The directory migration makes the source generations easier to identify and brings the existing simulation, teaching, FAB research and printable-model materials under one current entry. It does not establish new device physics, measured accuracy or foundry qualification.

V3-4 是整合后的分享版本，数值仿真基线仍为 **v3.3.0**。本次目录迁移使各代源码更容易辨认，并将已有仿真、教学、FAB 研究及打印模型资料统一到当前入口；不因此增加器件物理、实测精度或晶圆厂认证声明。

## What each directory represents

## 各目录分别代表什么

| Directory before → after / 迁移前 → 迁移后 | Purpose / 用途 | Existing scope / 已有范围 | Existing recorded checks / 已记录检查 |
|---|---|---|---|
| `v32/` → `V3-2/` | V3.2.0 DC/DC equations, sources and teaching baseline.<br>V3.2.0 的 DC/DC 方程、资料及教学基线。 | Adds 9 DC/DC model views and 153 cases to the V3.1 baseline of 11 views and 58 cases: **20 views, 211 cases, 725 plots** in the combined presentation. Includes one dedicated buck teaching GIF.<br>在 V3.1 的 11 项视图、58 个工况基础上新增 9 项 DC/DC 视图、153 个工况；合计 **20 项视图、211 个工况、725 组曲线**，附一份 Buck 专题教学 GIF。 | **61** implementation checks: 36 baseline checks + 25 DC/DC checks.<br>**61** 项实现检查：36 项基线检查＋25 项 DC/DC 检查。 |
| `v33/` → `V3.3/` | V3.3.0 numerical refinements and a complete model-animation gallery, using preserved older equations as comparison inputs.<br>V3.3.0 数值改进及全模型动画库，以保留的旧方程作为比较输入。 | The same **20 views, 211 cases and 725 plots**; **20 model GIFs**, each linked to a representative case. Model count does not increase.<br>仍为 **20 项视图、211 个工况、725 组曲线**；**20 个模型 GIF** 分别绑定代表工况，模型数量未增加。 | **96** implementation checks: 61 preserved-baseline checks + 18 analog numerical checks + 17 DC/DC numerical checks.<br>**96** 项实现检查：61 项基线回归＋18 项模拟数值检查＋17 项 DC/DC 数值检查。 |
| `V3-3/` → `V3-4/` | The current sharing entry and package metadata, rather than another numerical engine.<br>当前分享入口及打包元数据，不是另一套数值引擎。 | Combines the v3.3.0 simulation baseline, FAB catalogue **2.0**, and printing edition **1.0**.<br>汇合 v3.3.0 仿真基线、FAB 目录 **2.0** 与打印版 **1.0**。 | [V3-4 validation](VALIDATION.md) checks migrated paths and preserved outputs; package inventories record current bytes. Historical numerical test counts remain separately identified.<br>[V3-4验证](VALIDATION.md)核对迁移路径与输出保留情况，打包清单记录当前字节；历史数值测试数量单独标明。 |

The directory spelling **`V3.3`** follows the requested name; it is distinct from the former hyphenated **`V3-3`** sharing entry. Do not add the two generations' model or case totals: they describe the same evolving catalogue. The 75 printing entries likewise must not be added to the 20 numerical model views as if all were new physical devices.

目录 **`V3.3`** 按指定名称使用小数点，与此前带连字符的分享入口 **`V3-3`** 不同。两代仿真的模型数和工况数不可相加，它们对应同一目录的演进版本；75 个打印条目也不能与 20 项数值模型视图相加并称为新增物理器件。

## What V3.3 changed relative to V3-2

## V3.3 相对 V3-2 改了什么

The V3.3 changes address numerical evaluation of retained simplified equations: selected analytic derivatives and state propagation, stable small-signal charge expressions, improved integration, and explicit event timing. All twenty model views received English-annotated GIFs with units and a recorded case. DC sweeps, physical-time transients and statistical samples remain distinct demonstrations.

V3.3 改进保留简化方程的数值计算，包括部分解析导数与状态传播、稳定的小量结电荷表达式、积分方法及显式事件时序。20 项模型视图均补齐带单位及工况记录的英文 GIF，并区分直流扫描、物理时间瞬态与统计抽样。

The recorded result is **12 numerical benchmarks meeting at least 10% relative error reduction, 7 numerical-floor cases, and 1 separately classified statistical-uncertainty case**. This is not a ten-percentage-point improvement in measured device accuracy. Missing PDK and measured data still prevent a universal physical-accuracy claim. Large relative reductions can concern very small absolute errors.

已有结果为 **12 项数值基准达到至少 10% 的相对误差下降、7 项处于数值精度下限、1 项单列统计不确定度**。这不是实测器件准确率增加 10 个百分点。缺少 PDK 和实测数据，仍不能对所有器件作物理准确率声明；很大的相对下降也可能仅对应极小的绝对误差。

The detailed model-by-model limits remain in [Numerical accuracy and limits](../V3.3/ACCURACY_AND_LIMITS.md). The input range **40–150 V means maximum DC/DC input voltage**, not a device breakdown or safe-operating-area rating.

逐模型边界保留在[数值准确性与限制](../V3.3/ACCURACY_AND_LIMITS.md)。**40～150 V 指 DC/DC 最高输入电压**，不是器件击穿额定值或安全工作区额定值。

## What the former V3-3 sharing entry added

## 此前 V3-3 分享入口增加了什么

The former V3-3 entry combined these existing materials without adding another simulation generation:

此前 V3-3 入口汇合以下已有资料，没有另增一代仿真：

- **FAB catalogue 2.0:** 59 catalogue entities, 119 records and 28 documented gap/exclusion/follow-up items, reviewed on 2026-11-06. Entities include subsidiaries and research institutes and are not equivalent to independent corporate groups or physical fabs. No exhaustive worldwide completeness claim is made.<br>**FAB 目录 2.0：**59 个目录主体、119 条记录、28 项缺口/排除/后续核实项，核对日期为 2026-11-06。主体含子公司与研究机构，不等于独立集团或实体晶圆厂数量，不宣称覆盖全球全部工艺。
- **Printing edition 1.0:** 75 binary STL teaching files with 60 × 42 mm footprints, enlarged tactile cutaways/reliefs, model cards and previews. The catalogue distinguishes physical devices, passive components, isolation/interconnect structures, mechanisms and circuit benches. Physical printing and printer-specific slicing have not been demonstrated.<br>**打印版 1.0：**75 份二进制 STL 教学文件，底面 60 × 42 毫米，采用教学放大的可触摸剖面/浮雕，并附模型卡和预览；区分物理器件、无源元件、隔离/互连、机理及电路台，尚未进行实物打印及特定打印机切片验证。
- **Literature and research history:** the V3.1 cohort audit and V3.2 supplementary source records retain their stated dates and reading depths. Renaming directories does not constitute a new full-text literature review.<br>**论文及研究历史：**V3.1 名单审计与 V3.2 补充来源记录保留各自日期及阅读深度。目录更名不等于重新阅读全文或完成新一轮文献核查。

## Reproducibility after migration

## 迁移后的可复现性

`V3.3` still depends on the preserved analog baseline in `v3/` and the DC/DC baseline now located in `V3-2/`. Source paths, CI commands, generated gallery metadata and printable catalogue references must follow the renamed directories together. Scientific model IDs such as `P01` and printing IDs such as `V33_P01` remain stable so that result, animation and printing records retain their joins.

`V3.3` 仍依赖 `v3/` 中的模拟基线及现位于 `V3-2/` 的 DC/DC 基线。源码路径、CI 命令、动画元数据和打印目录来源引用需要同步迁移。`P01` 等科学模型编号及 `V33_P01` 等打印编号保持稳定，保证计算结果、动画与打印记录仍能对应。

Original release manifests and tag-pinned links are historical evidence. Their original paths refer to the release at that tag; they should not be silently rewritten and then presented as original checksums. The V3-4 package requires its own manifest for current paths and bytes, with the previous release identities retained for traceability.

原发布清单及固定标签链接属于历史证据，其路径指向对应标签中的发布内容，不应静默改写后仍称为原校验值。V3-4 应使用自己的清单核对当前路径及字节，同时保留旧发布身份以便追溯。

## Repository evidence

## 仓库依据

- [V3.2 recorded release summary](../V3-2/presentation/release_summary.json) and [validation limits](../V3-2/VALIDATION_AND_LIMITS.md) — V3.2 已记录发布摘要及校核边界。
- [V3.3 recorded release summary](../V3.3/presentation/release_summary.json), [baseline regression](../V3.3/validation/legacy_checks.json), [analog checks](../V3.3/numerics/analog/validation.json), and [DC/DC checks](../V3.3/numerics/dcdc/validation.json) — V3.3 已记录摘要、基线回归及两类数值检查。
- [Original V3-3 sharing metadata at the printing release](https://github.com/hemanjie-byte/mixed-signal-simulation/blob/v3-3-print1-20261107/V3-3/current-release.json) — 打印发布标签下的原 V3-3 分享元数据。
- [FAB methodology](../global-fab-processes/METHOD.md) and [printing guide](../printable-models/PRINT_GUIDE_EN_ZH.md) — 工艺目录方法与打印说明。
