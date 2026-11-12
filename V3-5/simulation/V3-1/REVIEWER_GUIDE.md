# Reviewer guide

# 审阅指南

This release is a reproducible illustrative research collection. It has not been peer reviewed and does not claim professor approval, measured accuracy or foundry qualification. Start with the falsifiable claims below.

本版是可复现的示意研究资料，未经同行评审，不声称获得教授认可、实测精度或晶圆厂认证。可从以下可核查事项审阅。

1. Inspect the people–paper join and original DOI bylines. Challenge homonyms, scope and affiliation context. See people200.csv, papers.csv, analog_scope_audit.csv and scope_reconciliation_v31.csv.

1. 核对人员与论文关联、DOI原始署名，检查同名、主题范围及机构背景。参见人员、论文、模拟相关性审计与旧200人变更CSV。

2. Read the actual source-depth columns. Five key model papers have targeted original-source review; additional scope sources are recorded per entry. Metadata checks are not full-text replication.

2. 查看实际阅读层级。5篇关键模型论文定向阅读原始来源，另逐条记录范围补充来源；题录核对不等于正文复现。

3. Inspect model equations and excluded terms. A01 uses a separate fixed capacitor network; A03 is a silicon NPN, not a SiGe HBT; B03 is spectral shaping, not a switched chopper; B06 is not a full type-II PLL.

3. 检查方程与缺项。A01另用固定电容网络；A03为硅NPN而非SiGe HBT；B03为频谱整形而非开关斩波；B06不是完整二型PLL。

4. Recompute numerical checks with the commands in README. The fixed seed verifies reproducibility, not foundry yield. The checks are designed to expose sign, normalization, factor-of-two and integration errors.

4. 按README重跑数值检查。固定种子支持复现，不证明工艺良率。检查用于发现符号、归一化、二倍因子和积分错误。

5. For 40–150 V input, distinguish operating rating, breakdown, gate oxide limits and common-mode isolation. The 15% overshoot and 90% utilization are editable screening assumptions, not standards.

5. 对40–150V输入，区分工作额定、击穿、栅氧限制与共模隔离。15%过冲和90%利用率是可修改的筛选假设，不是标准。

6. To claim a paper reproduction, add its exact topology, extracted parameters with units/provenance, figure/data references, quantitative residuals and uncertainty. To claim a foundry result, use the authorized PDK and permitted disclosure scope.

6. 若声称复现论文，需要补上准确拓扑、含单位和出处的提取参数、图表/数据定位、定量残差与不确定度。若声称工艺结果，需要授权PDK及其允许披露范围。

Open priorities: intrinsic charge-based MOS modeling; calibrated SiGe HBT; LNA/mixer/PA/TIA; switched chopper aliasing; delta-sigma/pipeline ADCs; LDO dropout and start-up; transistor VCO phase noise; gate-charge, reverse recovery and magnetic loss in the buck; layout parasitics, device reliability and statistical process data.

待完善重点：内禀电荷型MOS模型、校准SiGe HBT、LNA/混频器/功放/TIA、开关斩波混叠、Delta-Sigma/流水线ADC、LDO压差极限与启动、晶体管VCO相噪、Buck栅电荷/反向恢复/磁损、版图寄生、器件可靠性和工艺统计。

V3.1 review targets: challenge each scope judgment; inspect actual SAR transition levels and the missing-code histogram test; verify FFT Parseval/DC/Nyquist normalization; compare LDO unity frequency against the independent quadratic solution; inspect all 18 buck refinement cases and the rerun audit.

V3.1审阅重点：逐条挑战范围判断；核对实际SAR转换边界及缺码直方图测试；验证FFT的Parseval/直流/奈奎斯特归一化；比较LDO单位增益频率与独立二次方程解；检查全部18个Buck细化工况及重跑审计。
