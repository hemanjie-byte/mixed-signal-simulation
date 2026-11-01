# High-voltage process context

# 高压工艺背景

40/60/80/100/120/150 V denotes maximum converter input. The public platform references below are inherited from the same-day V1 review; they do not establish individual PDK device ratings or current commercial availability.

40/60/80/100/120/150V均指转换器最高输入。下列公开平台资料沿用同日V1核对，不证明具体PDK器件额定值或当前商业可获得性。

## P01 Hua Hong — BCD family overview

华虹：BCD平台总览

0.35 um to 55 nm; 8/12 inch; 1.5–800 V family range. Family maximum is not a device option at every node. Obtain the exact 40–150 V-compatible option table.

0.35μm～55nm；8/12英寸；1.5～800V（家族范围）。不可把800V家族上限赋给任意0.18μm工艺；40～150V要逐器件确认

[Official source / 官方来源](https://www.huahonggrace.com/s/business_ap_management.php)

## P02 Hua Hong — Historical 700 V BCD

华虹：0.5μm 700V BCD

0.5 um; 700 V LDMOS; 200–700 V JFET application range. 2016 announcement of 2015 production. A 200 V start-up JFET is not evidence for a 200 V low-Ron power LDMOS.

0.5μm；700V LDMOS；200～700V是JFET应用范围。200V明确属于JFET，不能宣称有200V低Ron功率LDMOS；高压高频DC/DC适配待确认

[Official source / 官方来源](https://www.huahong.com.cn/?id=443&m=detail)

## P03 United Nova Technology / SMEC — Bulk/SOI BCD

芯联集成：Bulk/SOI BCD

0.35/0.18 um; 5–150 V and 250–650 V platform ranges. Legacy official English page; current availability and exact device options require confirmation. A 150 V input cannot use a nominal 150 V device without headroom.

0.35/0.18μm；5～150V；250～650V（平台区间）。150V输入需更高档；250V系列可询，但无公开具体LDMOS参数

[Official source / 官方来源](https://www.unt-c.com/html/pro5/)

## P04 United Nova Technology / SMEC — Analog IC platform

芯联集成：模拟IC技术平台

180/90/55 nm; No voltage stated on this page. The current platform page does not establish a 150 V option at 55 nm.

180/90/55nm；该新官网页未列电压。不可把旧版150V范围直接赋给55nm；需确切版本

[Official source / 官方来源](https://cn.unt-c.com/solution)

## P05 DB HiTek — 80 V BCDMOS

东部 DB HiTek：80V BCDMOS

0.18 um; NLDMOS/PLDMOS up to 80 V. Candidate for 40/60 V inputs under the example margin; not for 80 V maximum input with that margin.

0.18μm；NLDMOS/PLDMOS最高80V。适合40/60V输入候选；80V输入在本示例裕量下不足

[Official source / 官方来源](https://dbhitek.com/en/technology/portfolio/bcdmos)

## P06 DB HiTek — 120 V BCDMOS

东部 DB HiTek：120V BCDMOS

0.18 um; High-side NLDMOS/PLDMOS up to 120 V. Candidate for 80 V input under the example margin; 100 V input exceeds it.

0.18μm；HS NLDMOS/PLDMOS最高120V。适合80V输入候选；100V输入需检查尖峰；按本例裕量不满足

[Official source / 官方来源](https://dbhitek.com/en/technology/portfolio/bcdmos)

## P07 DB HiTek — 120 V BCDMOS with optional DTI

东部 DB HiTek：120V BCDMOS DTI可选

0.13 um; High-side NLDMOS/PLDMOS up to 120 V. Device/platform voltage is not a guarantee of equal maximum converter input.

0.13μm；HS NLDMOS/PLDMOS最高120V。120V是器件平台标称，不是120V输入保证

[Official source / 官方来源](https://dbhitek.com/en/technology/portfolio/bcdmos)

## P08 DB HiTek — UHV non-epitaxial BCD

东部 DB HiTek：UHV非外延BCD

0.35 um; 200–700 V LDMOS. A 200 V branch is a candidate inquiry for 100/120/150 V inputs. Ron, Qg, isolation and switching suitability are unknown.

0.35μm；LDMOS 200～700V。100/120/150V输入可询200V选件；Ron/Qg/频率/隔离兼容待证

[Official source / 官方来源](https://dbhitek.com/en/technology/portfolio/bcdmos)

## P09 DB HiTek — UHV epitaxial BCD

东部 DB HiTek：UHV外延BCD

0.35 um; 200–900 V LDMOS; page also discusses 900 V breakdown. Do not treat breakdown voltage as continuous operating rating; confirm the precise 200 V device option.

0.35μm；LDMOS 200～900V；页面另述900V击穿。不得把900V击穿当连续工作额定；200V支路待PDK确认

[Official source / 官方来源](https://dbhitek.com/en/technology/portfolio/bcdmos)

## P10 TSMC — Gen-2 100 V extension

台积电：Gen-2 100V扩展

0.18 um; 100 V, targeting 48 V systems. Official page says PDK released in 2025. Candidate for 60 V input under the example margin, not 80 V and above.

0.18μm；100V；面向48V系统。60V输入可候选；80V及以上在本例裕量下需更高档

[Official source / 官方来源](https://www.tsmc.com/japanese/dedicatedFoundry/technology/specialty/bcd)

## P11 UMC — BCD family

联电：BCD家族

0.5 um to 55 nm family; Up to 200 V operating voltage. The 200 V claim is not assigned to every node or polarity in the public overview.

0.5μm～55nm（总览表述）；最高200V工作电压。200V所属具体节点/隔离/极性未逐项公开，不能都归55nm

[Official source / 官方来源](https://www.umc.com/en/Product/technologies/Detail/bcd)

## P12 UMC — 55 nm EPI BCD

联电：55nm EPI BCD

55 nm; Up to 150 V operating voltage. 2025-10-22 release. The EPI claim supports at most 100 V input under the example margin; it does not qualify 150 V input.

55nm；最高150V工作电压。150V仅明确给EPI；本例只覆盖到100V输入，不能覆盖150V输入

[Official source / 官方来源](https://www.umc.com/en/News/press_release/Content/technology_related/20251022)

## P13 SK hynix system ic (Wuxi) — 60 V BCD Gen2

海力士 system ic（无锡）：60V BCD Gen2

0.18 um; DMOS up to 60 V. Candidate for 40 V input under the example margin. Distinct from SK hynix memory processes.

0.18μm；DMOS最高60V。40V输入候选；不能直接以60V档支持60V输入

[Official source / 官方来源](https://www.skhynixsystemic.cn/foundry/bcdmos?lang=en_US)

## P14 SK hynix system ic (Wuxi) — 120 V BCD

海力士 system ic（无锡）：120V BCD

0.18 um; DMOS up to 120 V. Candidate for 80 V input under the example margin. Junction/deep-trench isolation options require exact PDK confirmation.

0.18μm；DMOS最高120V。本例80V输入候选；不是SK Hynix存储工艺，也不与Key Foundry自动等同

[Official source / 官方来源](https://www.skhynixsystemic.cn/foundry/bcdmos?lang=en_US)

## P15 Magnachip (historical reference) — 200 V SOI BCD

美格纳（历史参考）：200V SOI BCD

0.18 um; 200 V operating voltage. 2018 historical announcement includes LDMOS, BJT, Zener, Schottky, high-R poly, MIM/MOM and memory options. Does not prove present order availability.

0.18μm；200V工作电压。历史技术对标，不证明美格纳当前仍接此工艺新单；代工业务2020售予Key Foundry

[Official source / 官方来源](https://investors.magnachip.com/node/10451/pdf)

## P16 Magnachip / Key Foundry history — Foundry group and Fab 4 sale

美格纳（主体变更）：Foundry Services Group和Fab4出售

Not applicable; Not applicable. Sale completed in 2020. Confirm current contracting entity, process lineage and available PDK before procurement.

不适用；不适用。引用历史美格纳能力时，当前合同主体、工艺沿革、可用PDK需重新确认

[Official source / 官方来源](https://www.magnachip.com/magnachip-completes-sale-of-foundry-services-group-and-fab-4/)

The illustrative minimum working-voltage screen is Vin,max × 1.15 / 0.90: 51.1, 76.7, 102.2, 127.8, 153.3 and 191.7 V. Candidate classes round up to 60, 80, 120, 150, 200 and 200 V. This is an engineering assumption, not a device qualification. A 150 V device does not qualify a 150 V input.

示例最低工作电压筛选为Vin,max×1.15/0.90，对应51.1、76.7、102.2、127.8、153.3、191.7V；向上选择60、80、120、150、200、200V档。这是工程假设，不是器件认证。150V器件不能直接证明支持150V输入。

High/low-side switches, high-voltage sensing and level shifting must meet bus stress. Logic MOS, precision BJT, reference and MIM/MOM capacitors stay in appropriate low-voltage domains. Bootstrap capacitance may have low differential voltage yet require high common-mode isolation. Start-up JFET, power LDMOS and Schottky options are not interchangeable.

高低侧开关、高压检测和电平转换需要承受总线应力；逻辑MOS、精密BJT、基准与MIM/MOM电容位于相应低压域。自举电容可能差模电压低而共模隔离要求高。启动JFET、功率LDMOS和肖特基选件不能混为一谈。
