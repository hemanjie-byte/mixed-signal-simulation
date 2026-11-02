# V3.1 analog relevance and rerun audit

# V3.1模拟相关性与重跑审计

Checked 2026-11-02. This report records corrections and falsifiable evidence; it is not a certification of scientific or silicon accuracy.

核查日期2026-11-02。本报告记录修正与可检验证据，不构成科学结论或硅片精度认证。

The final cohort contains 200 people, linked to 154 circuit papers, 14 analog-method papers and 14 analog-component/parasitic papers. Person counts are 165/17/18 because of coauthorship. Every entry has a source and a stated scope reason; title-only review remains labeled title-only.

最终200人关联154篇电路、14篇模拟方法、14篇模拟元件/寄生论文。因合著关系，人员数为165/17/18。每条列来源和范围理由；仅题名核查仍标注为仅题名核查。

## Changes in representative evidence

## 代表证据变更

| Previous person | Decision | Previous DOI | Current DOI |
|---|---|---|---|
| Alex Q. Huang | Excluded from current scope / 当前范围移出 | 10.1016/s0038-1101(99)00239-7 | — |
| Asen Asenov | Excluded from current scope / 当前范围移出 | 10.1109/ted.2010.2067732 | — |
| B. Jayant Baliga | Excluded from current scope / 当前范围移出 | 10.1109/tpel.2020.3043281 | — |
| Chenming Hu | Paper replaced / 更换论文 | 10.1109/t-ed.1983.21452 | 10.1109/cicc.2019.8780155 |
| Debdeep Jena | Excluded from current scope / 当前范围移出 | 10.1109/ted.2018.2829125 | — |
| Douglas C. Hopkins | Excluded from current scope / 当前范围移出 | 10.4071/001c.81980 | — |
| Grigory Simin | Excluded from current scope / 当前范围移出 | 10.4071/hitec-tp16 | — |
| John D Cressler | Paper replaced / 更换论文 | 10.1016/0011-2275(90)90204-p | 10.1109/lmwc.2014.2369992 |
| José Alexandre Diniz | Excluded from current scope / 当前范围移出 | 10.1116/1.5022160 | — |
| Joungho Kim | Excluded from current scope / 当前范围移出 | 10.1109/tcpmt.2010.2101890 | — |
| Kevin Jing CHEN | Excluded from current scope / 当前范围移出 | 10.1109/ted.2017.2657579 | — |
| Linda S Milor | Paper replaced / 更换论文 | 10.1109/tvlsi.2018.2861769 | 10.1109/43.21830 |
| Mark S. Lundstrom | Excluded from current scope / 当前范围移出 | 10.1109/ted.2015.2481886 | — |
| Mathieu Luisier | Excluded from current scope / 当前范围移出 | 10.1109/mcse.2009.210 | — |
| Raafat Mansour | Paper replaced / 更换论文 | 10.1109/tmtt.2017.2671359 | 10.1109/tmtt.2020.3018141 |
| Souvik Mahapatra | Excluded from current scope / 当前范围移出 | 10.1109/ted.2018.2842129 | — |
| Srabanti Chowdhury | Excluded from current scope / 当前范围移出 | 10.1109/led.2019.2914026 | — |
| Tsu-Jae King Liu | Excluded from current scope / 当前范围移出 | 10.1109/ted.2009.2030711 | — |
| Umesh Mishra | Excluded from current scope / 当前范围移出 | 10.1109/led.2015.2436922 | — |
| Xiaowu Gong | Excluded from current scope / 当前范围移出 | 10.1109/ted.2023.3314401 | — |

These decisions concern the selected evidence, not an assertion that an excluded person never worked on analog circuits. The 16 additions are identified by ANALOG-AUDIT IDs in the person ledger. Eight of the original broad TOP100 were removed in this revision, leaving 15 in the current cohort.

这些决定针对所选证据，不断言移出人员从未研究模拟电路。16位补入人员在台账中使用ANALOG-AUDIT编号。本轮移出原宽范围TOP100中的8人，当前保留15人。

## Numerical corrections and rerun

## 数值修正与重跑

B04 now computes actual SAR transition edges rather than assuming every CDAC output is a transition. A deliberately non-monotonic 3-bit CDAC test exposes missing-code behavior. Endpoint INL uses the first/last internal transition line. FFT one-sided bin power counts DC/Nyquist once; a Parseval test also covers odd sample lengths.

B04现计算真实SAR转换边界，不再假设每个CDAC输出都是转换点。刻意构造的非单调3位CDAC测试验证缺码行为；端点INL使用首末内部转换点连线。单边FFT功率对直流/奈奎斯特只计一次，Parseval测试还覆盖奇数采样长度。

For the published mismatch case, maximum absolute endpoint INL changes from 0.6285107646 to 0.6331895534 LSB. SNDR changes from 59.5752894218 to 59.5753314665 dB; this tiny difference reflects corrected FFT weighting, not improved silicon. Both ADC plot arrays are updated; the other 56 current cases remain identical.

已发布失配工况最大绝对端点INL从0.6285107646变为0.6331895534 LSB；SNDR从59.5752894218变为59.5753314665 dB，微小变化来自FFT计权修正，不是硅片性能改善。两组ADC曲线已更新，其余56个当前工况保持一致。

36 current tests pass: 30 numerical/model tests and six research-data tests. The five new numerical tests cover actual SAR missing-code transitions, FFT Parseval normalization, INL endpoints, independently solved LDO unity frequency and all 18 buck input/temperature convergence cases. V1/V2 reruns match the previous numerical data exactly. Total rerun coverage is 658 device/benchmark cases plus six V1 buck examples.

36项当前测试通过：30项数值/模型和6项研究数据检查。新增5项数值测试覆盖SAR缺码边界、FFT Parseval归一化、INL端点、LDO独立单位增益频率和全部18个Buck输入/温度收敛工况。V1/V2重跑数值与旧数据完全一致；合计覆盖658个器件/测试台工况，另有6个V1 Buck示例。

[Scope evidence / 范围证据](research/analog_scope_audit.csv) · [DOI checks / DOI检查](research/doi_audit.csv) · [Rerun data / 重跑数据](validation/rerun_audit.json) · [Test outcomes / 测试结果](results/validation.json)

Remaining physical/model uncertainty is unchanged: no authorized PDK, extracted process parameters, measured data, complete charge-based MOS, switched chopper/RF transistor circuits, full ADC/PLL implementation or foundry reliability qualification. Passing tests establish consistency against the stated simplified equations, not transistor-level prediction accuracy.

物理与模型不确定性仍在：没有授权PDK、工艺参数提取、实测数据、完整电荷型MOS、开关斩波/射频晶体管电路、完整ADC/PLL实现或晶圆厂可靠性认证。测试通过证明与所列简化方程一致，不证明晶体管级预测精度。
