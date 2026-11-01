# Research and simulation methodology

# 研究与仿真方法

Scope: semiconductor devices and integrated-circuit research, with analog, mixed-signal, RF and power-management design as the priority. Biomedical papers are included only when the subject is a semiconductor sensor/readout/front-end circuit. Pure clinical studies, general machine learning, batteries, PCB-only antennas and editorial introductions were not selected.

范围为半导体器件与集成电路研究，优先模拟、混合信号、射频和电源管理。生物医学主题仅纳入半导体传感器、读出或前端电路；不选纯临床、通用机器学习、电池、纯PCB天线及编辑前言。

The TOP200 label identifies a curated research cohort, not an official ranking or a claim to identify the world’s objectively best 200 researchers. IDs and alphabetical display order are retrieval aids. Coverage spans 20 countries/regions of affiliation context, not citizenship. The sample remains uneven (76 United States affiliations) and is not a census of global analog research.

TOP200表示整理的研究名单，不是官方排名，也不声称客观找到了全球最优的200人。编号和英文姓名排序便于检索。20个国家/地区指机构背景，不表示国籍。样本仍不均衡（美国机构背景76人），不是全球模拟研究普查。

Selection started with the previous 1,000-candidate professional directory and 41 additional established analog researchers. A bounded pool of 234 was queried against Crossref (up to 25 journal-article results per author, with analog/CMOS or device terms). 200 were retained after title/byline screening. This search can miss relevant work and is not exhaustive. Only 23 members of the broader old TOP100 remain in the focused cohort; the reconciliation file records all 100 decisions without changing historical releases.

从原1000人专业目录和另外41位模拟研究人员形成234人候选池，在Crossref按每位作者最多25条期刊论文结果检索，并加入模拟/CMOS或器件关键词。按题名和署名筛选后保留200人。检索有限，可能漏检，不是穷尽研究。原来范围较广的TOP100中有23人进入本版重点名单，100条对照记录保留全部变更，旧版本保持历史状态。

The final cohort links to 184 distinct DOI records checked on 2026-11-01. Duplicate coauthored articles count once. Titles, full author names, venues and publication dates were checked against DOI records. The five primary model papers were inspected through publisher or author-hosted sources, supporting nine people. Other records have bibliographic-level review only. Manufacturer tutorials and the ngspice manual are labeled technical documentation, not peer-reviewed papers. No result implies that all publications of 200 authors were read.

最终关联184条不同DOI，于2026-11-01核对；合著同一论文只计一次。核对题名、完整署名、期刊与出版日期。5篇关键模型论文通过出版商或作者公开来源定向阅读，关联9位人员；其余仅做题录核对。厂家教程和ngspice手册标为技术文档，不算同行评审论文。本结果不表示通读了200人全部论文。

A full-name match plus a relevant topic reduces false matches but does not prove institutional identity. Most institutional profiles were inherited from 2026-10-11; added affiliation context is historical and not asserted as current employment. No-update entries mean only that this DOI record contains no update-to item; we did not perform a comprehensive retraction or fraud audit. These limitations are retained in the data rather than replaced with confidence scores.

完整姓名与相关主题匹配能够降低误匹配，但不等于机构身份认证。多数机构主页沿用2026-10-11快照，新增机构背景为历史信息，不声称现职。未发现update-to仅表示当前DOI记录未列更新项；未进行全面撤稿或学术不端审计。这些限制直接保留在数据中，不用主观置信度分数掩盖。

English titles are the cleaned publisher metadata. HTML markup and repeated whitespace were removed; Greek symbols were normalized for readability. Chinese topic lines are concise editorial summaries, not official translated titles. The list includes supporting semiconductor-device papers; it does not claim that all 184 are analog circuit design papers. All are assigned an explicit semiconductor/IC topic.

英文题名来自清理后的出版题录，去除HTML标记与重复空白并规范希腊符号。中文为简要主题说明，不是官方译题。名单含支撑半导体器件论文，不声称184篇全部是模拟电路设计论文；每篇均列明半导体/芯片主题。

Literature identifies missing mechanisms. It does not provide numerical extraction here. All model coefficients, operating points and stochastic distributions are demonstration assumptions, except exact SI constants. Four model/parameter extensions and seven circuit benchmarks are counted separately. No new fabricated device class or reproduced publication is claimed. V1/V2 contain broader historical models; V3 does not revalidate those legacy models.

文献用于识别缺失机理，本版未从文献做数值参数提取。除SI精确定义常数外，模型系数、偏置与随机分布均为演示假设。4项模型/参数增强与7个电路测试台分开计数，不宣称新增实际工艺器件类别或复现论文。V1/V2保留更宽范围的历史模型，V3未重新验证全部历史模型。

Positive terminal current enters the device/block. Port power is ΣVI and may include storage as well as dissipation. Missing electrical ports are marked unmodeled, never treated as measured zero. Noise PSD is one-sided; SSB phase noise is Sphi/2. ADC FFT uses 16,384 samples, coherent bin 503, no window and 0.98 of full-scale sine amplitude. SNDR includes all non-DC, non-fundamental bins; the separate SNR excludes harmonics 2–5.

端口电流以流入器件/模块为正。端口功率ΣVI可能同时包含储能和损耗。没有建模的电气端口标为未建模，不把缺项当成测得的零。噪声PSD为单边定义，SSB相位噪声为Sphi/2。ADC用16384点、相干频点503、不加窗、满幅正弦的0.98倍振幅。SNDR包含除直流和基波外所有频点，另列SNR去掉2至5次谐波。

The 58 cases use explicit SI units and deterministic seeds. Tests cover limiting formulas, gauge and source/drain symmetry, charge derivatives, mismatch variance, analytic matrix-exponential/step solutions, time-step refinement and energy balance. The buck starts from the analytic periodic state; switching events have both pre/post values at equal timestamps. Trapezoidal integration handles these zero-duration edges. Efficiency is conduction-only and is not a hardware prediction.

58个工况使用明确SI单位和固定随机种子。检查覆盖极限公式、参考电位与源漏对称性、电荷导数、失配方差、矩阵指数/阶跃解析解、步长细化和能量守恒。Buck从解析周期状态起算，开关边沿以相同时间戳保留前后数值，梯形积分处理零时长边沿。效率仅含导通损耗，不预测实际硬件效率。

The 3D view uses dimensionless boxes and terminal labels. It does not solve Poisson, drift-diffusion, local current density, electric field, fabrication geometry, doping or thermal fields. Circuit block arrangements are illustrations, not layouts. Excel and the viewer are saved numerical snapshots; changing text parameters does not rerun nonlinear models.

3D采用归一化图块和端口标签，不求解Poisson、漂移扩散、局部电流密度、电场、工艺几何、掺杂或热场。电路图块排列为示意而非版图。Excel与演示页是计算快照，修改参数文本不会重新运行非线性模型。
