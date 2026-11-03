"""Rebuild the hand-reviewed V3.2 source registry and evidence map (no network).

All numerical model parameters remain assumptions. This script stores citations,
short audit notes, and model relationships; it does not redistribute papers.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKED = "2026-11-03"
SOURCES = []


def source(sid, title, chinese, authors, year, venue, kind, url, doi,
           read_en, read_zh, locator, use_en, use_zh, limits_en, limits_zh,
           models, **extra):
    SOURCES.append(dict(
        id=sid, title_en=title, title_zh=chinese, authors=authors,
        year=year, venue=venue, kind=kind, url=url, doi=doi,
        read_level_en=read_en, read_level_zh=read_zh,
        equation_locator=locator, use_en=use_en, use_zh=use_zh,
        limitations_en=limits_en, limitations_zh=limits_zh,
        model_ids=models, retrieved_date=CHECKED, checked_date=CHECKED,
        parameter_provenance_en="No numerical model coefficient extracted or fitted from this source.",
        parameter_provenance_zh="未从本来源提取或拟合任何模型数值系数。", **extra))


source("S01", "Fundamentals of MOSFET and IGBT Gate Driver Circuits",
       "MOSFET与IGBT栅极驱动电路基础", ["Laszlo Balogh"], 2018,
       "Texas Instruments, SLUA618A; March 2017, revised October 2018",
       "manufacturer_application_note", "https://www.ti.com/lit/ml/slua618a/slua618a.pdf", "",
       "Targeted PDF body: switching intervals, gate loss and bootstrap sizing.",
       "定向阅读PDF正文：开关区间、栅极损耗与自举电容选取。",
       "Sections 2.5–2.7, printed pp. 10–13, Eq. (9); section 5.2.2, p. 34, Eq. (31).",
       "Supports gate-charge/Miller intervals and gate-drive energy bookkeeping.",
       "支持栅电荷、米勒区间及驱动能量核算。",
       "P01 is a reduced charge-domain example, not the complete gate-driver circuits or a calibrated MOSFET.",
       "P01为简化电荷域示例，未复现完整驱动电路或校准MOSFET。",
       ["P01", "P03", "P08"], document_date="2018-10")

source("S02", "Power Loss Calculation With Common Source Inductance Consideration for Synchronous Buck Converters",
       "考虑共源电感的同步降压转换器功率损耗计算", ["David Jauregui", "Bo Wang", "Rengang Chen"], 2011,
       "Texas Instruments, SLPA009A; June 2011, revised July 2011",
       "manufacturer_application_note", "https://www.ti.com/lit/an/slpa009a/slpa009a.pdf", "",
       "Targeted PDF body: diode losses, output capacitance and CCM assumptions.",
       "定向阅读PDF正文：二极管损耗、输出电容和CCM假设。",
       "Section 3.3, p. 7, Eqs. (32)–(33); section 3.4, p. 8, Eqs. (34)–(35); section 4, p. 8.",
       "Supports dead-time body-diode conduction and a VIN×Qrr commutation-energy estimate.",
       "支持死区体二极管导通与VIN×Qrr换流能量估算。",
       "Its 0.5×Qoss×VIN approximation is not a nonlinear-energy identity. P01 integrates Eoss; P08 independently derives matched-pair hard-turn-on energy VIN×Qoss. No common-source-inductance circuit is reproduced.",
       "文中的0.5×Qoss×VIN近似并非非线性能量恒等式；P01积分Eoss，P08独立推导匹配双管硬开通能量VIN×Qoss；未复现共源电感电路。",
       ["P01", "P02", "P08"], document_date="2011-07")

source("S03", "Bootstrap Circuitry Selection for Half-Bridge Configurations",
       "半桥结构的自举电路选型", ["Mamadou Diallo"], 2023,
       "Texas Instruments, SLUA887A; August 2018, revised September 2023",
       "manufacturer_application_note", "https://www.ti.com/lit/an/slua887a/slua887a.pdf", "",
       "Targeted PDF body: operating paths and capacitor/diode selection.",
       "定向阅读PDF正文：工作电流路径与电容、二极管选取。",
       "Section 2, p. 2, Figs. 2-1/2-2; section 3.1, p. 3, Eq. (3); section 3.3, pp. 4–5.",
       "Relates stored bootstrap charge, leakage, high-side on-time and UVLO headroom.",
       "关联自举储存电荷、漏电、高侧导通时间与欠压锁定余量。",
       "P03 uses an assumed RC recharge path. It does not reproduce UCC27710, bootstrap-diode recovery or layout ringing.",
       "P03采用假设RC充电路径，未复现UCC27710、自举二极管反向恢复或布局振铃。",
       ["P03"], document_date="2023-09")

source("S04", "A Level Shifter With Almost Full Immunity to Positive dv/dt for Buck Converters",
       "用于降压转换器、几乎完全抑制正向dv/dt干扰的电平移位器",
       ["Yunzhe Yang", "Mo Huang", "Sijun Du", "Rui P. Martins", "Yan Lu"], 2023,
       "IEEE Transactions on Circuits and Systems I: Regular Papers 70(11), 4595–4604",
       "peer_reviewed_journal", "https://ieeexplore.ieee.org/abstract/document/10236598", "10.1109/TCSI.2023.3307869",
       "Publisher abstract; TU Delft author/title record; Crossref metadata. Full body not retrieved.",
       "出版商摘要、代尔夫特理工大学作者题录及Crossref元数据；未获取全文正文。",
       "Abstract only; no equation-level reproduction claimed.",
       "Analog-IC evidence that dv/dt-induced noise current can upset high-side level shifting.",
       "提供模拟集成电路依据：dv/dt噪声电流可能扰乱高侧电平移位。",
       "The reported circuit is a 20-V buck in 180-nm BCD. P04 is only an RC disturbance surrogate, not the paper's cancellation scheme or a 150-V rating.",
       "原文为180nm BCD的20V降压芯片。P04仅为RC干扰替代模型，不复现抑制方案，也不证明150V耐压。",
       ["P04"], published_online="2023-08-31", published_issue="2023-11",
       metadata_url="https://api.crossref.org/works/10.1109/TCSI.2023.3307869",
       author_repository_url="https://repository.tudelft.nl/record/uuid%3Ad3912f8c-8e44-4c97-ace2-6974b8c570bb")

source("S05", "INA381 26-V, High-Speed, Current Sense Amplifier With Integrated Comparator",
       "INA381：26V高速电流检测放大器及集成比较器", ["Texas Instruments"], 2019,
       "Texas Instruments, SBOS848B; December 2017, revised October 2019",
       "manufacturer_datasheet", "https://www.ti.com/lit/ds/symlink/ina381.pdf", "",
       "Targeted PDF body: timing specifications, low-side sensing and comparator hysteresis.",
       "定向阅读PDF正文：时序指标、低侧检测与比较器迟滞。",
       "Section 6.5, p. 5; section 7.3, pp. 14–16; section 8.2.2, pp. 27–29.",
       "Separates amplifier bandwidth, comparator-only delay and complete alert delay.",
       "区分放大器带宽、比较器本体延迟及完整告警链延迟。",
       "26-V common-mode capability does not permit direct 150-V high-side sensing. P05 uses an assumed low-side signal chain and is not an INA381 model.",
       "26V共模能力不支持直接150V高侧检测；P05是假设低侧信号链，并非INA381模型。",
       ["P05"], document_date="2019-10")

source("S06", "LM5116 Wide Range Synchronous Buck Controller",
       "LM5116宽输入范围同步降压控制器", ["Texas Instruments"], 2023,
       "Texas Instruments, SNVS499I; February 2007, revised November 2023",
       "manufacturer_datasheet", "https://www.ti.com/lit/ds/symlink/lm5116.pdf", "",
       "Targeted PDF body: startup regulator, UVLO, current limiting and soft start.",
       "定向阅读PDF正文：启动稳压器、欠压锁定、电流限制与软启动。",
       "Startup regulator, p. 14; section 6.3.3, p. 15; section 6.4.1, p. 19; section 7.2.2.10, p. 26, Eqs. (22)–(23).",
       "Provides analog-controller architecture context for bias startup, UVLO hysteresis and soft start.",
       "提供偏置启动、欠压锁定迟滞与软启动的模拟控制器结构依据。",
       "LM5116 operates up to 100 V, not 150 V. P06/P09 do not reproduce its internal emulated ramp, hiccup logic or transistor circuits.",
       "LM5116工作输入上限为100V，并非150V。P06/P09不复现其内部仿真斜坡、打嗝逻辑或晶体管电路。",
       ["P06", "P09"], document_date="2023-11")

source("S07", "Ringing Reduction Techniques for NexFET High Performance MOSFETs",
       "NexFET高性能MOSFET的振铃抑制方法", ["Texas Instruments"], 2011,
       "Texas Instruments, SLPA010, November 2011", "manufacturer_application_note",
       "https://www.ti.com/lit/an/slpa010/slpa010.pdf", "",
       "Targeted PDF body: edge-rate tradeoff and switch-node RC snubber.",
       "定向阅读PDF正文：边沿速度权衡与开关节点RC吸收电路。",
       "Optimized Boot Resistance, p. 9; Optimized Switch-Node Snubber, pp. 11–13, Fig. 17.",
       "Supports parasitic-L/C ringing and the damping-versus-dissipation tradeoff.",
       "支持寄生电感、电容振铃及阻尼与损耗之间的权衡。",
       "The source approximates a parallel RLC. P07 is a series-RLC surrogate: its critical resistance is 2√(L/C), not the source's 0.5√(L/C). It is not a PCB snubber-design validation.",
       "来源近似为并联RLC；P07为串联RLC替代模型，临界电阻应为2√(L/C)，不是原文的0.5√(L/C)。不构成PCB吸收电路设计验证。",
       ["P07"], document_date="2011-11")

source("S08", "Use Thermal Analysis to Predict an IC's Transient Behavior and Avoid Overheating",
       "运用热分析预测集成电路瞬态行为并避免过热", ["Analog Devices / Maxim Integrated (corporate publication; no individual byline displayed)"], 2010,
       "Analog Devices / Maxim Integrated technical article, 25 February 2010",
       "manufacturer_technical_article", "https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html", "",
       "Targeted HTML body: heat-flow laws, RC analogy and measurement-based fitting.",
       "定向阅读网页正文：热流定律、RC类比与测量拟合要求。",
       "Laws of Thermal Dynamics; RC Network Models Thermal-Transient Differential Equations; Fig. 4 and discussion after Eq. (25).",
       "Supports the heat-capacity/resistance analogy and requirement for transient thermal characterization.",
       "支持热容、热阻电路类比，以及瞬态热特性实测要求。",
       "P08 reduces heat flow to one assumed node; it does not reproduce the article's fitted three-body network, hotspots or board-dependent package behavior.",
       "P08将热流简化为单个假设节点；不复现原文拟合的三体网络、热点或与PCB有关的封装热行为。",
       ["P08"], document_date="2010-02-25")

source("S09", "Modelling and analysis of switching DC-to-DC converters in constant-frequency current-programmed mode",
       "恒频电流编程模式开关DC/DC转换器的建模与分析",
       ["Shi-Ping Hsu", "Art Brown", "Loman Rensink", "R. D. Middlebrook"], 1979,
       "1979 IEEE Power Electronics Specialists Conference, pp. 284–301; San Diego, 18–22 June 1979",
       "peer_reviewed_conference", "https://authors.library.caltech.edu/records/ac87w-mn171", "10.1109/PESC.1979.7081037",
       "Repository abstract; PDF pp. 284–285 (introduction and start of section 2); Crossref metadata.",
       "机构库摘要、PDF第284–285页（引言及第2节开头）与Crossref元数据。",
       "Printed pp. 284–285, Fig. 1, section 2 and Eqs. (1)–(4).",
       "Supports current-programmed control, command-current limiting and the distinction between averaged and cycle-to-cycle dynamics.",
       "支持电流编程控制、指令电流限制，以及平均动态与逐周期动态的区别。",
       "P09 is a simplified averaged teaching plant. It omits sampled-cycle dynamics, slope compensation and subharmonic instability; it does not reproduce this paper's full model.",
       "P09为简化平均教学对象；未建模采样周期动态、斜坡补偿及次谐波失稳，未复现论文完整模型。",
       ["P09"], published_issue="1979-06",
       metadata_url="https://api.crossref.org/works/10.1109/PESC.1979.7081037")

source("S10", "A 400-V Half Bridge Gate Driver for Normally-Off GaN HEMTs With Effective Dv/Dt Control and High Dv/Dt Immunity",
       "适用于常关型GaN HEMT、具有有效dv/dt控制与高抗扰度的400V半桥栅极驱动器",
       ["Siyuan Yu", "Qi Zhou", "Gang Shi", "Tianyang Wu", "Jing Zhu", "Long Zhang", "Weifeng Sun", "Sen Zhang", "Nailong He", "Ye Li"], 2023,
       "IEEE Transactions on Industrial Electronics 70(1), 741–751",
       "peer_reviewed_journal", "https://ieeexplore.ieee.org/document/9724123/", "10.1109/TIE.2022.3153808",
       "Publisher-indexed abstract and Crossref bibliographic metadata; full text not accessed.",
       "出版商索引摘要与Crossref题录元数据；未访问全文。",
       "Abstract only; no equation-level reproduction claimed.",
       "Analog-IC evidence for active gate-drive strength control and level-shifter common-mode-current compensation.",
       "为有源栅极驱动强度控制、电平移位器共模电流补偿提供模拟集成电路依据。",
       "P01/P04 reproduce neither proposed circuit nor measured performance. The paper's 400-V SOI BCD driver does not qualify any named foundry process in this repository.",
       "P01/P04均未复现该电路或实测性能；论文400V SOI BCD驱动器不能证明本库所列晶圆厂工艺具备相同能力。",
       ["P01", "P04"], published_online="2022-03-01", published_issue="2023-01",
       metadata_url="https://api.crossref.org/works/10.1109/TIE.2022.3153808")

source("S11", "An integrated high-voltage self-powered buck converter with reduced heat generation",
       "降低发热的集成高压自供电降压转换器", ["Bin Wang", "Zhiqiang Li", "Xin Liu"], 2026,
       "IEICE Electronics Express 23(9), article 20250401, pp. 1–6",
       "peer_reviewed_journal", "https://www.jstage.jst.go.jp/article/elex/23/9/23_22.20250401/_article", "10.1587/elex.22.20250401",
       "Publisher abstract and PDF pp. 1–3 (sections 1–2.3); Crossref metadata.",
       "出版商摘要与PDF第1–3页（第1至2.3节）；Crossref元数据。",
       "Section 1, p. 1, Eq. (1); sections 2.2–2.3, pp. 2–3, Figs. 5–7 and Eqs. (4)–(7).",
       "Supports HV JFET bias-supply loss (VIN−VDD)×I and voltage-divider/comparator supply supervision.",
       "支持高压JFET偏置供电损耗(VIN−VDD)×I，以及分压器、比较器电源监测。",
       "This is an AC-DC constant-current buck IC. P06 does not implement its rectified-line valley-supply method or complete 700-V JFET circuit.",
       "原文为AC/DC恒流降压芯片；P06不实现其整流输入谷底供电方法，也不复现完整700V JFET电路。",
       ["P06"], published_online="2025-08-19", published_issue="2026-05-10",
       metadata_url="https://api.crossref.org/works/10.1587/elex.22.20250401")

source("S12", "AN-1308: Common-Mode Step Response of Current Sense Amplifiers",
       "AN-1308：电流检测放大器的共模阶跃响应", ["Paul Blanchard", "Anna Fe Briones"], 2015,
       "Analog Devices, AN-1308 Rev. A; June 2014, revised October 2015",
       "manufacturer_application_note", "https://www.analog.com/en/resources/app-notes/an-1308.html", "",
       "HTML body and PDF revision record; targeted common-mode response discussion.",
       "网页正文及PDF修订记录；定向阅读共模响应讨论。",
       "Common-Mode Step Response, PDF p. 3; measurement results, pp. 4–5, Fig. 3; revision history p. 2.",
       "Shows why DC CMRR alone is insufficient for switching-node current sensing.",
       "说明为何仅有直流共模抑制比不足以评价开关节点电流检测。",
       "P05 is low-side and does not model high-side common-mode-step recovery, input protection or isolation.",
       "P05为低侧模型，未模拟高侧共模阶跃恢复、输入保护或隔离。",
       ["P05"], document_date="2015-10",
       pdf_url="https://www.analog.com/media/en/technical-documentation/app-notes/an-1308.pdf")

EVIDENCE_MAP = [
    dict(id="P01", source_ids=["S01", "S02", "S10"],
         change_en="Extends V2 X01's fixed-capacitance Miller example with charge-domain switching and nonlinear Qoss/Eoss bookkeeping.",
         change_zh="在V2 X01固定电容米勒示例基础上，扩展电荷域开关及非线性Qoss/Eoss核算。",
         remaining_en="No measured charge curves, charge-conserving terminal compact model, avalanche or SOA validation.",
         remaining_zh="无实测电荷曲线、电荷守恒端口紧凑模型、雪崩或安全工作区验证。"),
    dict(id="P02", source_ids=["S02"],
         change_en="Adds an explicit CCM buck dead-time trace; V2 X02 already contained an imposed triangular recovery pulse.",
         change_zh="增加明确的CCM降压死区波形；V2 X02已含外部指定的三角形恢复电流。",
         remaining_en="Qrr is imposed, not predicted by carrier transport; diode recovery and buck trajectory are separate teaching experiments.",
         remaining_zh="Qrr为指定值，不由载流子输运预测；恢复电流与降压轨迹属于分开的教学实验。"),
    dict(id="P03", source_ids=["S01", "S03"],
         change_en="Adds finite bootstrap recharge, charge depletion and UVLO headroom.",
         change_zh="增加有限自举充电、电荷消耗及欠压余量。",
         remaining_en="No actual driver, leakage corners, diode recovery or full startup/100%-duty strategy.",
         remaining_zh="无真实驱动器、漏电工艺角、二极管恢复或完整启动及100%占空比方案。"),
    dict(id="P04", source_ids=["S04", "S10"],
         change_en="Adds capacitive common-mode current injection into an RC receiver node.",
         change_zh="增加共模电容注入电流及RC接收节点响应。",
         remaining_en="No transistor latch, differential mismatch, regeneration or cited noise-cancellation circuits.",
         remaining_zh="无晶体管锁存器、差分失配、再生或文献中的噪声抵消电路。"),
    dict(id="P05", source_ids=["S05", "S12"],
         change_en="Adds a low-side sense amplifier/filter and delayed comparator signal chain.",
         change_zh="增加低侧检测放大器、滤波器与延迟比较器信号链。",
         remaining_en="No high-voltage common-mode input, transistor noise, saturation recovery or actual protection timing qualification.",
         remaining_zh="无高压共模输入、晶体管噪声、饱和恢复或实际保护时序认证。"),
    dict(id="P06", source_ids=["S06", "S11"],
         change_en="Adds current-limited bias startup with source compliance and UVLO hysteresis.",
         change_zh="增加带输出顺从范围的限流偏置启动及欠压迟滞。",
         remaining_en="Current-source branch is a JFET functional surrogate; no physical JFET extraction, self-bias zero-state or rectified-line valley control.",
         remaining_zh="恒流源支路仅为JFET功能替代，无物理JFET参数提取、自偏置零状态或整流谷底控制。"),
    dict(id="P07", source_ids=["S07"],
         change_en="Adds passive series-RLC damping sweeps and energy accounting.",
         change_zh="增加无源串联RLC阻尼扫描及能量核算。",
         remaining_en="Series surrogate is not a switch-node shunt-RC snubber; PCB parasitics and EMI require separate validation.",
         remaining_zh="串联替代模型并非开关节点并接RC吸收电路；PCB寄生与EMI需单独验证。"),
    dict(id="P08", source_ids=["S01", "S02", "S08"],
         change_en="Extends V2 X03 thermal RC with separate conduction, overlap, gate, matched-pair Coss hard-turn-on and recovery loss terms.",
         change_zh="在V2 X03热RC基础上，增加独立的导通、交叠、栅极、匹配双管Coss硬开通及恢复损耗项。",
         remaining_en="One thermal node and an assumed loss ledger are not measured efficiency, multi-die thermal prediction or calorimetric validation.",
         remaining_zh="单热节点和假设损耗表不能替代效率实测、多芯片热预测或量热验证。"),
    dict(id="P09", source_ids=["S06", "S09"],
         change_en="Extends V3 B07's fixed-duty steady-state buck with an averaged closed-loop teaching experiment.",
         change_zh="在V3 B07固定占空比稳态降压模型基础上，增加平均闭环教学实验。",
         remaining_en="No sampled-data current-mode instability, switching ripple, slope compensation, DCM or coupled transistor-level protection.",
         remaining_zh="无采样电流模式失稳、开关纹波、斜坡补偿、DCM或晶体管级耦合保护。"),
]


def dump_json(name, rows):
    (HERE / name).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dump_csv(name, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (HERE / name).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "; ".join(v) if isinstance(v, list) else v for k, v in row.items()})


if __name__ == "__main__":
    assert len(SOURCES) == 12 and len({s["id"] for s in SOURCES}) == 12
    source_ids = {s["id"] for s in SOURCES}
    assert all(set(row["source_ids"]) <= source_ids for row in EVIDENCE_MAP)
    assert all(s["retrieved_date"] == CHECKED for s in SOURCES)
    papers = [s for s in SOURCES if s["kind"].startswith("peer_reviewed")]
    assert len(papers) == 4 and all(p["doi"] for p in papers)
    dump_json("sources.json", SOURCES)
    dump_csv("sources.csv", SOURCES)
    dump_json("model_evidence_map.json", EVIDENCE_MAP)
    dump_csv("model_evidence_map.csv", EVIDENCE_MAP)
    dump_json("audit_summary.json", dict(
        checked_date=CHECKED, source_count=12, peer_reviewed_journal_count=3,
        peer_reviewed_conference_count=1, manufacturer_document_count=8,
        new_research_papers_with_targeted_pdf_body_read=2,
        new_research_papers_abstract_only=2,
        source_reported_numeric_parameters_used_in_models=0,
        baseline_people_count=200, baseline_papers_count=182,
        baseline_reaudit_en="V3.1 cohort retained; this targeted audit does not claim a new full-text review of all 182 baseline papers.",
        baseline_reaudit_zh="保留V3.1人员与论文集；此次定向核对不表示重新阅读全文182篇旧论文。",
        metadata_verification_en="All four paper DOIs, author lists, venue, year and pagination checked against publisher/repository records and live Crossref metadata on the checked date.",
        metadata_verification_zh="4篇论文DOI、作者名单、刊会、年份及页码均在核对日期与出版商、机构库及实时Crossref元数据核对。"))
    bib = []
    for s in papers:
        entry = "inproceedings" if s["kind"] == "peer_reviewed_conference" else "article"
        bib.append("@" + entry + "{" + s["id"] + ",\n" +
                   "  title = {" + s["title_en"] + "},\n" +
                   "  author = {" + " and ".join(s["authors"]) + "},\n" +
                   "  year = {" + str(s["year"]) + "},\n" +
                   "  note = {" + s["venue"] + "},\n" +
                   "  doi = {" + s["doi"] + "},\n" +
                   "  url = {" + s["url"] + "}\n}")
    (HERE / "references.bib").write_text("\n\n".join(bib) + "\n", encoding="utf-8")
    print("Wrote 12 reviewed source records, 9 evidence mappings and 4 research-paper citations.")
