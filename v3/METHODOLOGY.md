# Research and simulation methodology

# 研究与仿真方法

V3.1 scope requires a direct analog-circuit connection for each representative paper: analog/mixed-signal/RF/power-management circuits; methods explicitly serving analog design; or components and parasitic models with a stated analog circuit use. General semiconductor prestige, power-device physics or packaging alone is insufficient.

V3.1要求每篇代表论文与模拟电路存在直接关联：模拟/混合信号/射频/电源管理电路；明确服务模拟设计的方法；或有明确模拟应用的元件与寄生模型。仅有半导体领域声望、功率器件物理或封装研究不足以入选。

This is a curated 200-person cohort, not an official TOP200 ranking. The 22 countries/regions describe source-linked affiliation context, not citizenship. The sample remains uneven: 75 have United States affiliation context. It is not a global census. Most inherited profiles were not refreshed as an employment directory.

这是整理的200人名单，不是官方TOP200排名。22个国家/地区指来源关联的机构背景，不表示国籍。样本仍不均衡：75人有美国机构背景；不是全球普查。大多数沿用主页未按现职名录重新更新。

V3.0 began from a bounded 234-candidate search. This revision reviews all 200 selected title/byline/topic associations, removes 16 whose selected evidence lacks a sufficiently direct analog link, adds 16 with analog-focused evidence, and replaces four retained authors’ representative papers. The change ledger preserves all 200 prior decisions. Exclusion evaluates the selected evidence, not the researcher’s ability or entire career.

V3.0从有限的234人候选池检索。本轮复核200条入选题名、署名和主题关联，移出16条直接模拟证据不足的旧人选，补入16位有模拟方向证据的人员，并替换4位保留人员的代表论文。变更台账保留旧200条决定。移出针对所选证据，不评价研究者能力或全部职业成果。

The final 182 distinct DOI records were retrieved again on 2026-11-02. Coauthored papers count once. There are 154 circuit/architecture papers, 14 analog-design method/model papers and 14 directly related component/parasitic papers; the corresponding person counts are 165, 17 and 18. All have documented analog relevance, but these three types must not be presented as 182 complete analog IC designs.

最终182条不同DOI于2026-11-02重新获取；合著同一论文只计一次。154篇电路/架构、14篇模拟设计方法/模型、14篇直接相关元件/寄生；对应人员165、17和18人。各条均记录模拟相关性，但不能将三类合称为182篇完整模拟芯片设计。

Each current person links to a DOI byline, scope class, English/Chinese reason, evidence URL and actual scope-reading depth. DOI title, author list, venue and date checks are bibliographic checks. Five key model papers have targeted primary-source review; additional borderline/new entries use source abstracts, original bylines or official author pages as explicitly recorded. We did not read all full texts or all publications of these 200 people.

当前每人关联DOI署名、范围类别、中英文理由、证据链接与实际阅读层级。DOI题名、作者列表、期刊和日期属于题录核查。5篇关键模型论文有定向原始来源阅读；新增或边界条目另使用摘要、原文署名或官方作者主页，具体范围逐条记录。未通读全部正文，也未阅读200人的全部发表成果。

Names/initials and topics support bibliographic association; they do not independently certify institutional identity. A corrupted François character was normalized from the original EKV paper byline. HTML and selected mathematical notation are normalized for display; Chinese lines summarize topics and are not official translated titles. Crossref record SHA-256 digests identify the checked metadata. An empty update-to field is not a comprehensive retraction or fraud audit.

姓名/缩写及主题支持文献关联，不构成机构身份认证。François的损坏字符按EKV原文署名修复。展示题名清理HTML及部分数学记号，中文为主题概述而非官方译题；Crossref记录SHA-256标识本轮检查的数据。update-to为空不代表全面撤稿或学术不端审查。

Per-paper model mapping is conservative: eight papers have a restricted mechanism relationship, and no paper-specific circuit is reproduced. Category membership alone no longer assigns a model. The remaining gaps are explicit. All numerical coefficients, bias points and statistical distributions are illustrative assumptions except exact SI constants. Neither literature review nor test passage supplies missing process calibration.

逐篇模型映射从严：8篇论文仅关联受限机理，没有复现任何论文的专门电路。不再仅因属于同一类别而分配模型，剩余缺口明确列出。除SI精确定义常数外，数值系数、偏置和统计分布均为示意假设。文献核查和测试通过均不能补足工艺校准。

All 58 current cases were rerun, with 36 analytical/numerical/research tests passing. In isolated working copies, 432 V1 device cases plus six V1 buck examples and 168 V2 cases reproduce their previous JSON data exactly. That verifies computational reproducibility of the legacy artifacts, not their physical accuracy or current analog scope. The rerun audit records hashes and ADC metric changes.

58个当前工况全部重跑，36项解析、数值和研究数据测试通过。隔离工作副本中，V1的432个器件工况及6个Buck示例、V2的168个工况与原JSON数据完全一致；这验证历史计算复现性，不证明其物理精度或符合当前模拟范围。重跑审计记录哈希和ADC指标变化。

Terminal current is positive into the block. Port power ΣVI includes storage and dissipation. Unmodeled ports are absent, never treated as measured zero. Noise PSD is one-sided and SSB phase noise equals Sphi/2. ADC uses 16,384 coherent samples, bin 503, no window and 0.98 of full-scale sine amplitude. One-sided FFT power doubles positive interior bins but counts DC and an even-length Nyquist bin once. SNDR excludes DC/fundamental; the separately reported SNR also excludes harmonics 2–5.

端口电流流入模块为正，端口功率ΣVI包含储能和耗散。未建模端口留空，不当作实测零。噪声PSD为单边，SSB相噪为Sphi/2。ADC采用16384相干采样点、频点503、不加窗和满幅正弦的0.98倍振幅；单边FFT正频率内部点功率加倍，直流和偶数长度的奈奎斯特点只计一次。SNDR去掉直流和基波；另列SNR还去掉2至5次谐波。

SAR DNL uses actual sequential-decision transition levels found by monotone search, so a non-monotonic CDAC may produce missing codes. INL is evaluated at 1023 internal transitions after removing the line through the first and last internal transitions, normalized by nominal LSB. End-bin widths use the specified 0–Vref range. Independent dense-input code histograms, Parseval equality and endpoint checks test these conventions.

SAR的DNL由单调搜索实际逐次决策转换边界得到，非单调CDAC可能产生缺码。INL在1023个内部转换点上减去首末内部转换点连线，并以标称LSB归一化；端码宽采用给定0～Vref范围。独立密集输入码直方图、Parseval等式与端点检查验证这些定义。

Buck integration starts from the analytic periodic state and includes both sides of each switching event at equal timestamps. All six input classes and three temperatures are checked with halved steps. The LDO unity frequency is compared with an independently solved quadratic in frequency squared. These tests assess implementation consistency; buck efficiency is conduction-only, and temperature sweeps are not foundry process corners.

Buck从解析周期状态起算，开关边沿在同一时间戳保留前后值；六种输入和三种温度均进行步长减半检查。LDO单位增益频率与关于频率平方的独立二次方程解比较。这些测试检验实现一致性；Buck效率仅含导通损耗，温度扫描不是晶圆厂工艺角。

3D geometry is dimensionless conceptual visualization with terminal/state data. It solves no Poisson, drift-diffusion, doping, process layout, electric-field, local current-density or thermal-field problem. Excel and HTML contain calculated snapshots; nonlinear model parameters require Python reruns. No PDK, SPICE engine execution, measured fit or professor/peer-review approval is claimed.

3D为归一化概念结构，展示端口/状态数据，不求解Poisson、漂移扩散、掺杂、工艺版图、电场、局部电流密度或温度场。Excel与HTML为计算快照，非线性参数改变须重跑Python。本版无PDK、SPICE引擎运行、实测拟合，也不声称教授或同行评审认可。
