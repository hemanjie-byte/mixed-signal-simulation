# V3.2 evidence, scope and remaining gaps

**Checked: 3 November 2026.** This upgrade adds nine focused DC/DC teaching experiments, P01–P09, to the V3.1.0 baseline. The six input levels—40, 60, 80, 100, 120 and 150 V—are **maximum converter input scenarios**, not qualified device breakdown ratings. All numerical coefficients are declared engineering assumptions. No model is a foundry PDK, extracted silicon model, TCAD result or reproduced paper measurement.

**核对日期：2026年11月3日。** 本次在V3.1.0基础上增加P01–P09九类DC/DC教学实验。40、60、80、100、120、150V六档指**转换器最高输入场景**，不是已认证的器件击穿额定值。所有数值系数均为明确声明的工程假设，未使用晶圆厂PDK、硅片提取模型或TCAD，也未复现论文实测结果。

## What was actually checked

The V3.1 cohort of **200 people / 182 papers is retained**. This focused pass checks **12 additional evidence sources: four research papers and eight manufacturer technical documents**. The four DOI records were checked against primary publisher/institutional records and live Crossref metadata, including complete author lists, venue, publication year and pagination. Two papers received targeted body reading; two received abstract-level review. This is not a claim that all 182 earlier papers were read again in full. The four new papers are supplemental references; the TOP200 roster is not silently expanded or reranked.

保留V3.1的**200人、182篇论文**。本次定向核对**12项补充依据：4篇研究论文与8份厂商技术文档**。4项DOI记录均与出版商、机构库和实时Crossref元数据核对完整作者名单、刊会、年份及页码；其中2篇定向阅读正文，2篇只核对摘要。不声称重新阅读全文182篇旧论文。4篇新论文作为补充依据，不暗中扩充或重排TOP200人员名单。

The research references concern semiconductor analog ICs or power-converter control: S04 and S10 are integrated level-shifter/gate-driver papers; S11 is an analog power-management IC paper for an **AC/DC** constant-current buck; S09 concerns current-programmed DC/DC control rather than a transistor-level IC implementation. S11 is deliberately labelled adjacent architectural evidence, not a DC/DC reproduction. Manufacturer application notes and datasheets are not counted as peer-reviewed papers.

研究文献涉及半导体模拟集成电路或电源转换控制：S04、S10是集成电平移位器、栅极驱动论文；S11是**AC/DC**恒流降压模拟电源管理芯片论文；S09讨论电流编程DC/DC控制，而不是晶体管级芯片实现。S11明确标为相邻架构依据，不标成DC/DC复现。厂商应用笔记与数据手册不计入同行评审论文。

| ID | Primary record / 一手记录 | Type and actual reading / 类型与实际阅读范围 |
|---|---|---|
| S01 | [TI SLUA618A](https://www.ti.com/lit/ml/slua618a/slua618a.pdf) | Application note; selected switching/bootstrap sections. / 应用笔记；选读开关、自举章节。 |
| S02 | [TI SLPA009A](https://www.ti.com/lit/an/slpa009a/slpa009a.pdf) | Application note; diode/Coss losses and CCM assumptions. / 应用笔记；二极管、Coss损耗与CCM条件。 |
| S03 | [TI SLUA887A](https://www.ti.com/lit/an/slua887a/slua887a.pdf) | Application note; bootstrap charge paths and sizing. / 应用笔记；自举电荷路径与选型。 |
| S04 | [Yang et al., TCAS-I 2023](https://doi.org/10.1109/TCSI.2023.3307869) | Journal paper; publisher abstract, institutional metadata; body unavailable. / 期刊论文；出版商摘要、机构题录，正文未取得。 |
| S05 | [INA381 datasheet, Rev. B](https://www.ti.com/lit/ds/symlink/ina381.pdf) | Datasheet; timing and low-side sensing sections. / 数据手册；时序与低侧检测章节。 |
| S06 | [LM5116 datasheet, Rev. I](https://www.ti.com/lit/ds/symlink/lm5116.pdf) | Datasheet; bias startup, UVLO, limiting and soft start. / 数据手册；偏置启动、欠压、限流与软启动。 |
| S07 | [TI SLPA010](https://www.ti.com/lit/an/slpa010/slpa010.pdf) | Application note; ringing and RC-snubber sections. / 应用笔记；振铃与RC吸收章节。 |
| S08 | [ADI thermal-transient article](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html) | Technical article; heat-flow/RC analogy and fitting requirements. / 技术文章；热流、RC类比与拟合要求。 |
| S09 | [Hsu et al., PESC 1979](https://authors.library.caltech.edu/records/ac87w-mn171) | Conference paper; abstract and PDF pp. 284–285. / 会议论文；摘要及PDF第284–285页。 |
| S10 | [Yu et al., TIE 2023](https://doi.org/10.1109/TIE.2022.3153808) | Journal paper; publisher-indexed abstract and metadata; full text unavailable. / 期刊论文；出版商索引摘要与题录，未取得全文。 |
| S11 | [Wang et al., IEICE Electronics Express 2026](https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article) | Journal paper; abstract and PDF pp. 1–3, §§1–2.3. / 期刊论文；摘要与PDF第1–3页、第1至2.3节。 |
| S12 | [ADI AN-1308, Rev. A](https://www.analog.com/en/resources/app-notes/an-1308.html) | Application note; common-mode-step response and PDF revision history. / 应用笔记；共模阶跃响应及PDF修订记录。 |

Complete English/Chinese titles, authors, dates, locators and limitations are in [the source registry](research/sources.json), [CSV](research/sources.csv) and [four-paper BibTeX](research/references.bib). The registry distinguishes issue year from first-online date: S10 first appeared online in 2022 but belongs to the January 2023 issue; S11 first appeared online in 2025 but belongs to the May 2026 issue. Its DOI includes `22.20250401` while the final volume is 23; these are the publisher's actual identifiers.

完整英中题名、作者、日期、定位及限制见[来源登记表](research/sources.json)、[CSV](research/sources.csv)及[4篇论文BibTeX](research/references.bib)。登记表区分正式刊期与首次上线日期：S10于2022年上线，正式刊期为2023年1月；S11于2025年上线，正式刊期为2026年5月。S11的DOI含`22.20250401`而正式卷号为23，均按出版商实际标识保留。

## Coverage added, without overstating novelty

V2 already had fixed-capacitance Miller injection (X01), an imposed triangular reverse-recovery pulse (X02), and a thermal RC example (X03). V3 already had a simplified steady-state buck (B07). V3.2 connects those ideas to a clearer high-input-voltage curriculum and adds the missing bias, sensing, disturbance and averaged-control experiments. It does not newly discover those device effects or close every analog modelling gap.

V2已有固定电容米勒注入（X01）、外部指定三角形反向恢复脉冲（X02）、热RC示例（X03）；V3已有简化稳态降压模型（B07）。V3.2将这些概念组织为更清晰的高输入电压课程，并增加偏置、检测、干扰和平均控制实验。不把已有物理效应宣称为首次新增，也不声称补齐全部模拟建模缺口。

| Model / 模型 | Focus / 本次重点 | Evidence / 依据 | Important open gap / 主要未闭合项 |
|---|---|---|---|
| P01 | Gate charge and nonlinear output-capacitance energy. / 栅电荷与非线性输出电容能量。 | S01, S02, S10 | Measured charge curves and terminal compact model. / 实测电荷曲线与端口紧凑模型。 |
| P02 | Explicit dead-time CCM trace and separate recovery pulse. / 明确死区CCM轨迹及独立恢复脉冲。 | S02 | Self-consistent carrier-storage/commutation model. / 自洽载流子存储与换流模型。 |
| P03 | Bootstrap recharge, depletion and UVLO margin. / 自举充电、消耗与欠压余量。 | S01, S03 | Actual floating driver and bootstrap-diode parasitics. / 实际浮地驱动器与自举二极管寄生。 |
| P04 | dv/dt current injection and receiver-node disturbance. / dv/dt电流注入及接收节点干扰。 | S04, S10 | Transistor-level latch and active cancellation. / 晶体管级锁存器与有源抵消。 |
| P05 | Low-side sensing/filtering/comparator delay. / 低侧检测、滤波与比较延迟。 | S05, S12 | High-side common-mode recovery and protection. / 高侧共模恢复与保护。 |
| P06 | Current-limited bias startup and UVLO hysteresis. / 限流偏置启动与欠压迟滞。 | S06, S11 | Physical JFET and complete auxiliary-power handover. / 物理JFET与完整辅助供电切换。 |
| P07 | Series-RLC damping and stored-energy decay. / 串联RLC阻尼与储能衰减。 | S07 | Real switch-node RC snubber and PCB extraction. / 实际开关节点RC吸收与PCB提取。 |
| P08 | Separate loss terms and one effective thermal node. / 独立损耗项及单个等效热节点。 | S01, S02, S08 | Measured loss attribution and thermal impedance. / 实测损耗归属与热阻抗。 |
| P09 | Averaged PI/current-command loop, soft start and load step. / 平均PI、电流指令环、软启动与负载阶跃。 | S06, S09 | Switching-cycle stability and real peak-current protection. / 开关周期稳定性与真实峰值电流保护。 |

Machine-readable mappings, baseline comparisons and remaining gaps are in [model_evidence_map.json](research/model_evidence_map.json). These nine experiments operate at different abstraction levels. Their independent test results must not be described as one coupled transistor-level converter simulation.

机器可读的依据映射、旧版对照及剩余缺口见[model_evidence_map.json](research/model_evidence_map.json)。九项实验的抽象层级不同，独立测试结果不能合称为一套耦合晶体管级转换器仿真。

## Reading the equations critically

**Charge is not energy.** For an assumed nonlinear capacitance, `Qoss(V) = integral C(v) dv` and `Eoss(V) = integral v C(v) dv`. The integrals are direct definitions used by this repository. A constant-capacitance approximation must not be promoted to an exact nonlinear identity. Likewise, `VIN × Qrr` is a bus-energy estimate; it does not say which semiconductor dissipates that energy. Count a mechanism once when assembling a loss ledger.

**电荷不等于能量。** 对假设的非线性电容，`Qoss(V)=积分C(v)dv`，`Eoss(V)=积分vC(v)dv`，本库按定义积分。不能把常电容近似提升为非线性精确恒等式。`VIN×Qrr`是母线能量估算，并不能直接确定哪颗半导体耗散这些能量；汇总损耗时，同一机制只能计一次。

**Three quantities, three meanings.** `Qoss` tells us how much charge moves. `Eoss` tells us how much energy remains stored in a charged output capacitor. `VIN × Qoss` is the work supplied by an ideal constant-voltage bus when it charges that capacitance from zero to VIN. Some supplied energy remains stored; the rest is dissipated in the resistive charging path. A single MOSFET's stored `Eoss` is therefore not automatically the half-bridge's complete commutation loss.

**三个量，三个含义。** `Qoss`说明转移多少电荷；`Eoss`说明充电后输出电容中储存多少能量；`VIN×Qoss`说明理想恒压母线把电容从零充至VIN时提供多少功。供给能量的一部分留在电容中，其余耗散在电阻性充电路径上。因此，单颗MOSFET的储能`Eoss`不能自动当成整个半桥的换流损耗。

P08 uses an explicit matched-device hard-turn-on assumption. The upper MOSFET's initially charged output capacitance discharges dissipatively, while the lower MOSFET's initially uncharged output capacitance charges from the bus. With both devices assigned the same assumed Coss curve:

P08采用明确的匹配双管硬开通假设：上管初始已充电的输出电容经耗散路径放电，下管初始未充电的输出电容从母线充电。上下管采用相同的假设Coss曲线：

```text
Upper-capacitance discharge loss = Eoss_upper
Lower-capacitance charging loss  = VIN * Qoss_lower - Eoss_lower
Total hard-turn-on Coss loss     = Eoss_upper + VIN * Qoss_lower - Eoss_lower
Matched Coss curves              => Total = VIN * Qoss
Power contribution              = Total * switching_frequency
```

This is an independently derived energy balance for the stated idealized commutation, not a coefficient extracted from S02 or a measured half-bridge loss. It treats the opposite transition as ideal redistribution, excludes recovery and channel overlap from these capacitance terms, and counts the two terms only once. Real asymmetric devices, resonant energy recovery, package inductance and measured switching trajectories require a coupled model.

这是针对所述理想化换流条件独立推导的能量平衡，不是从S02提取的系数，也不是实测半桥损耗。对向转换采用理想能量转移假设；上述电容项不含反向恢复或沟道交叠，两项均只计一次。实际非对称器件、谐振能量回收、封装电感及实测开关轨迹仍需耦合模型。

**Topology changes the damping formula.** P07 independently solves a series RLC and uses `Rcritical = 2 sqrt(L/C)`. S07 discusses a different, approximately parallel topology for a switch-node snubber. The P07 damping sweep explains energy decay; it is not a ready-to-use snubber component prescription.

**拓扑决定阻尼公式。** P07独立求解串联RLC，采用`Rcritical=2sqrt(L/C)`；S07讨论开关节点吸收电路的近似并联拓扑，两者不同。P07阻尼扫描用于解释能量衰减，不是可直接投产的吸收器件选值方案。

**Average current limiting is not cycle-by-cycle protection.** P09 limits a continuous current command. It cannot establish peak-current comparator timing, slope-compensation adequacy or subharmonic stability. A converged numerical waveform is evidence about the equations implemented, not evidence that omitted physics is safe.

**平均电流限制不等于逐周期保护。** P09限制的是连续电流指令，不能证明峰值比较器时序、斜坡补偿充分性或次谐波稳定性。数值波形收敛只验证已实现的方程，不能证明被省略的物理机制安全。

## Boundaries before a real 40–150 V IC design

1. **Use the correct voltage domain.** INA381's cited signal-chain architecture is useful for low-side sensing; its 26-V common-mode range does not support direct 150-V high-side connection. LM5116's cited architecture does not extend its 100-V input rating. The S04 20-V experiment and S10 400-V driver are literature contexts, not voltage qualifications of this library.
2. **Obtain process evidence.** A qualified high-voltage power switch needs appropriate off-state rating, transient margin, isolation, gate-oxide constraints, safe operating area and reliability characterization. Foundry marketing voltage alone cannot supply these. This upgrade makes no new capability claim for Hua Hong, United Nova, DB HiTek, TSMC, UMC, SK hynix or Magnachip.
3. **Calibrate and couple the model.** Needed next are authorized PDK corners, terminal charge/noise models, measured switching/recovery data, package/PCB parasitics, thermal impedance and protection timing. Magnetic saturation, core loss, leakage-induced startup failures, ESD/latch-up and production reliability remain outside the present examples.
4. **Keep the teaching visuals honest.** The GIF illustrates current paths and simulated circuit quantities. Structural 3D illustrations are not solved electric-field, carrier-density or thermal-field maps. Neither a GIF nor a single thermal node proves physical 3D device behaviour.

1. **正确使用电压域。** INA381所示信号链结构适用于低侧检测，其26V共模范围不支持直接接150V高侧；引用LM5116结构不改变其100V输入额定值。S04的20V实验及S10的400V驱动器属于文献背景，不是本库的耐压认证。
2. **取得工艺证据。** 合格高压功率开关需要关断耐压、瞬态裕量、隔离、栅氧限制、安全工作区和可靠性表征；晶圆厂宣传电压不能替代这些数据。本次不增加对华虹、芯联集成、DB HiTek、台积电、联电、SK海力士或美格纳的工艺能力断言。
3. **校准并耦合模型。** 下一步需要授权PDK工艺角、端口电荷与噪声模型、实测开关和恢复数据、封装/PCB寄生、热阻抗及保护时序。磁性饱和、磁芯损耗、漏电导致启动失败、ESD/闩锁和量产可靠性仍在当前示例之外。
4. **准确理解教学图。** GIF展示电流路径及模拟电路量；结构性3D图不是已求解的电场、载流子密度或温度场。GIF和单热节点都不能证明真实三维器件行为。

## Reproducible source inventory

Run `python v32/research/build_source_audit.py` to regenerate the source registry, CSV, four-paper BibTeX and evidence map from reviewed entries. This script has no network dependence and does not download or redistribute paper PDFs. Source reading depth and limitations are part of the deliverable, rather than hidden behind a citation count.

执行`python v32/research/build_source_audit.py`可由已核对记录再生成来源表、CSV、4篇论文BibTeX及依据映射。脚本不依赖网络，不下载或分发论文PDF。阅读深度与局限属于正式交付内容，不以引文数量掩盖。
