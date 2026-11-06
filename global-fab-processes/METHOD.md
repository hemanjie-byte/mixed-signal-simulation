# Reading public process information

# 如何阅读公开工艺信息

This catalogue records what manufacturers publish. A row can describe a process family, a named platform, an announcement or a historical technology. It does not promise that every node, device polarity or isolation option shares the same voltage range. The source date may be a publication date, document revision or explicitly labelled page-metadata modification date; the review date is when the source was checked. Unknown dates remain unknown.

目录记录厂商公开的信息。一行可能对应工艺家族、具名平台、技术公告或历史技术，不保证每个节点、器件极性和隔离选件都具有相同耐压。来源日期可能为公开发布日期、文件修订日期或明确标注的页面元数据更新时间；核对日期为本次检查时间，未知日期保留未知。

| Term / 术语 | Meaning / 含义 |
|---|---|
| BCD | Bipolar, CMOS and DMOS integration; exact devices depend on the platform.<br>双极、CMOS与DMOS集成；具体器件依平台而定。 |
| SOI / DTI | Silicon-on-insulator / deep-trench isolation; neither alone establishes a voltage rating.<br>绝缘体上硅/深沟槽隔离；仅凭名称不能确定器件额定电压。 |
| Operating voltage | The source explicitly describes a working condition; limits still depend on terminals, lifetime and bias.<br>来源明确描述工作条件；仍受端口、寿命及偏置限制。 |
| Breakdown voltage | An electrical breakdown criterion, often with a stated test current; not a continuous operating rating.<br>电击穿判据，通常关联测试电流；不等于连续工作额定。 |
| Platform voltage | A vendor's family/platform label whose precise device-level meaning may be unspecified.<br>厂商对家族/平台的电压标记，器件层面的定义可能未公开。 |
| External foundry | A manufacturer advertises fabrication services; this does not confirm a particular customer's access.<br>厂商宣传制造代工服务，不等于确认某个客户能够获得指定工艺。 |
| IDM internal process | A manufacturer describes technology used in its own products; external wafer services require separate evidence.<br>厂商描述自有产品使用的工艺；对外晶圆服务须另有依据。 |
| Historical announcement | A dated technology statement retained for comparison; current entity and availability need confirmation.<br>保留用于对比的旧技术公告；当前主体及可用性须确认。 |
| Not disclosed | The reviewed source does not establish this field; it is not zero or proof of absence.<br>所核对来源未证明该字段；不代表数值为零或不存在此能力。 |

For a 40/60/80/100/120/150 V maximum-input converter, a technology inquiry must identify the exact high-side and low-side device options, working and breakdown limits, transient overshoot, isolation, gate-drive constraints, RDS(on), Qg, Coss, diode recovery, SOA and lifetime models. The existing simulation voltage-screen assumptions are teaching examples, not qualification rules. This catalogue therefore does not automatically assign a “supported input voltage” to each public process label.

针对40/60/80/100/120/150V最高输入的转换器，应向厂商确认准确的高低侧器件选件、工作及击穿限制、瞬态过冲、隔离、栅驱动约束、导通电阻、栅电荷、输出电容、二极管恢复、安全工作区及寿命模型。原仿真的电压筛选假设属于教学示例，不是认证规则。因此目录不根据公开工艺名称自动推定“可支持输入电压”。

Official source pages are linked, with concise summaries. The collection does not redistribute proprietary PDKs or full third-party brochures. Platform context and published evidence are separate from the authored V3.3 illustrative models; no process calibration was performed in this catalogue update.

目录提供官方来源链接与简要归纳，不分发专有PDK或第三方完整手册。公开工艺背景与V3.3人为示意模型分别记录；本次目录更新未进行工艺参数标定。
