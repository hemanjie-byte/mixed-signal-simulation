"""Render twenty English-only, data-driven teaching GIFs. No simulation is run here."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
W, H = 1080, 720
COL = dict(bg="#081321", panel="#112338", grid="#294258", text="#eff6ff",
           muted="#adc1d4", cyan="#56d8f5", orange="#ffbf69", green="#6ce0ad",
           red="#ff808c", purple="#b6a2ff", blue="#2f79a9", dark="#06101d")
PALETTE = [COL[k] for k in ("cyan", "orange", "green", "purple", "red")]

def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size=size)

F = {(n, b): font(n, b) for n in (12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 27, 30)
     for b in (False, True)}

def text(d, xy, s, size=16, color="text", bold=False, anchor=None):
    d.text(xy, str(s), font=F[size, bold], fill=COL.get(color, color), anchor=anchor)

def wrap(d, xy, s, width=290, size=16, color="muted", leading=23, max_lines=8):
    words = str(s).split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if d.textlength(test, font=F[size, False]) > width and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".") + "..."
    for i, line in enumerate(lines):
        text(d, (xy[0], xy[1] + i * leading), line, size, color)
    return len(lines) * leading

def box(d, rect, label="", color="cyan", fill="panel", size=16):
    d.rounded_rectangle(rect, radius=9, fill=COL.get(fill, fill), outline=COL.get(color, color), width=2)
    if label:
        text(d, ((rect[0]+rect[2])/2, (rect[1]+rect[3])/2), label, size, color, True, "mm")

def wire(d, pts, color="muted", width=3):
    d.line(pts, fill=COL.get(color, color), width=width, joint="curve")

def arrow(d, a, b, color="muted"):
    wire(d, [a,b], color, 2)
    ang = math.atan2(b[1]-a[1], b[0]-a[0])
    pts=[b, (b[0]-8*math.cos(ang-.5), b[1]-8*math.sin(ang-.5)),
         (b[0]-8*math.cos(ang+.5), b[1]-8*math.sin(ang+.5))]
    d.polygon(pts, fill=COL.get(color, color))

def fmt(v):
    if not math.isfinite(float(v)):
        return "N/A"
    return f"{v:.3g}"

def axisfmt(v, span):
    """Retain significant ripple rather than labeling three ticks '12 V'."""
    if not span or abs(v)>1e5 or (abs(v)>0 and abs(v)<1e-5):
        return fmt(v)
    decimals=max(0,min(8,int(math.ceil(-math.log10(abs(span))))+1))
    return f"{v:.{decimals}f}"

def eng(v, unit):
    a = abs(float(v))
    if unit in ("A", "V", "C", "F", "J", "S", "s", "W") and a > 0:
        for fac, pre in ((1e-12,"p"),(1e-9,"n"),(1e-6,"u"),(1e-3,"m"),(1,""),(1e3,"k")):
            if a < 1000*fac or fac == 1e3:
                return fmt(v/fac) + " " + pre + unit
    return fmt(v) + (" " + unit if unit not in ("1","code") else (" code" if unit=="code" else ""))

def en(s):
    return s.split(" / ")[0].replace("–","-").replace("Δ","Delta")

# All diagram arrows denote signal influence unless explicitly identified as a circuit wire.
SPECS = {
 "A01": dict(case="A01_transfer_25C", title="MOS control: gate voltage to drain current",
   zh="MOS控制：栅压如何改变漏电流", kind="DC SWEEP", groups=[[0],[1],[4]],
   teach="Raise the gate voltage and compare drain current, transconductance and gm/Id. A DC sweep is a sequence of bias points, not a switching event.",
   teach_zh="升高栅压，对照漏电流、跨导及gm/Id。直流扫描是不同偏置点，并不是开关瞬态。",
   equation="gm = dId/dVg; transconductance efficiency = gm/Id",
   scope="Low-voltage interpolation; no breakdown or physical field solution."),
 "A02": dict(case="A02_CV_25C", title="Junction capacitance and stored charge",
   zh="结电容与储存电荷", kind="DC SWEEP", groups=[[0],[1],[2]],
   teach="Reverse bias changes depletion capacitance. Charge is the integral of capacitance, not C(V) times V for a nonlinear junction.",
   teach_zh="反向偏置改变耗尽电容。对非线性结，电荷为电容的电压积分，不能直接用C(V)乘V。",
   equation="Cj = dQj/dV; Idisplacement = Cj dV/dt",
   scope="DC C-V/Q-V sweep; no moving depletion boundary or transient current is implied."),
 "A03": dict(case="A03_gummel_25C", title="NPN transistor: exponential bias response",
   zh="NPN晶体管：指数偏置响应", kind="DC SWEEP", groups=[[0,1],[2]], logy=[0],
   teach="A small Vbe increase gives a large current change. Collector and base currents use a log scale. Terminal currents follow the into-device convention.",
   teach_zh="Vbe稍微增加即可显著改变电流。集电流与基电流采用对数纵轴；端口电流按流入器件为正。",
   equation="Ic + Ib + Ie = 0",
   scope="Low-injection DC Ebers-Moll; no carrier transit animation or breakdown."),
 "A04": dict(case="A04_area16um2", title="Matched MOS pairs: common shift and difference",
   zh="MOS配对：共同偏移与差分失配", kind="STATISTICAL SAMPLES", groups=[[0,1],[2]],
   teach="Each cursor position is a different random sample. Common variation can cancel in the pair difference. Only 512 display samples are shown; summary statistics use 20,000.",
   teach_zh="每个光标位置对应不同随机样本；共同变化可在配对差中抵消。图上仅显示512个样本，汇总统计使用20000个样本。",
   equation="Delta Vth(pair) = delta Vth1 - delta Vth2",
   scope="Sample index is not time; symbols do not show physical motion."),
 "B01": dict(case="B01_25C", title="Differential pair: steering a fixed tail current",
   zh="差分对：分配固定尾电流", kind="DC SWEEP", groups=[[0,1],[2]],
   teach="The differential input redistributes current between two branches. The tail source fixes the sum, while the shared source voltage adjusts.",
   teach_zh="差分输入把电流重新分配到两个支路；尾电流源固定总电流，共源节点电压随之调整。",
   equation="I1 + I2 = Itail = 100 uA",
   scope="Static pair model; no high-frequency settling or offset extraction."),
 "B02": dict(case="B02_temperature", title="Reference design: combine opposite temperature slopes",
   zh="基准设计：组合相反的温度斜率", kind="TEMPERATURE SWEEP", groups=[[1,2],[0],[3]],
   teach="Vbe falls with temperature; the weighted PTAT term rises. Their sum is flatter, but curvature remains. The cursor changes temperature, not elapsed time.",
   teach_zh="Vbe随温度下降，加权PTAT项随温度上升，二者求和更平坦但仍有曲率。光标代表温度而不是时间。",
   equation="Vref = Vbe + K x Delta Vbe",
   scope="Algebraic reference sum; no startup circuit or thermal transient."),
 "B03": dict(case="B03_25C", title="Noise spectrum: density is not total noise",
   zh="噪声谱：噪声密度不等于总噪声", kind="FREQUENCY SWEEP", groups=[[0,1]], logx=True,
   teach="At each frequency, compare amplitude spectral density. Integrated noise uses the area under PSD, which is ASD squared. Low-frequency suppression can raise wideband noise.",
   teach_zh="逐频率比较幅度谱密度。积分噪声使用功率谱密度即ASD平方的面积；低频抑制可能伴随宽带噪声增加。",
   equation="Vrms = sqrt(integral ASD(f)^2 df)",
   scope="Analytic spectrum; no generated random time-domain noise trace."),
 "B04": dict(case="B04_mismatch", title="SAR ADC: sampled input, code and quantization error",
   zh="SAR ADC：采样输入、输出码与量化误差", kind="SAMPLED SIGNAL", groups=[[0,1],[2],["error"]], samples=66,
   teach="The cursor advances through saved input samples. The reconstruction uses the final conversion code; the error is reconstructed minus input voltage. Internal bit trials are not animated.",
   teach_zh="光标逐个经过保存的输入样本。重建电压由最终输出码得到；误差为重建值减输入值。动画没有模拟内部逐次比较时序。",
   equation="Error = Vreconstructed - Vin",
   scope="Mismatch case; no comparator dynamics, switch settling or timing solver."),
 "B05": dict(case="B05_25C", title="LDO load step: capacitor support and pass-current recovery",
   zh="LDO负载阶跃：电容支撑与调整管电流恢复", kind="TIME TRANSIENT", groups=[[0],[1,2]],
   teach="After the load changes, the pass current needs time to respond. The output capacitor supplies the current difference, causing a voltage dip and finite-gain steady error.",
   teach_zh="负载改变后，调整管电流需要时间响应；输出电容提供差额电流，因此产生跌落及有限增益导致的稳态误差。",
   equation="Cout dVout/dt = Ipass - Iload",
   scope="Reduced LDO model; no dropout, transistor SOA or package extraction."),
 "B06": dict(case="B06_zeta0.7", title="Phase loop: correction and damping",
   zh="锁相环：相位修正与阻尼", kind="TIME TRANSIENT", groups=[[0],[1]],
   teach="A phase step is corrected by changing oscillator frequency. Damping controls overshoot and settling. Phase is an angle; it is not the oscillator voltage waveform.",
   teach_zh="相位阶跃通过改变振荡频率得到修正；阻尼决定过冲与稳定时间。相位是角度，并非振荡器电压波形。",
   equation="Frequency deviation = (1/2pi) dPhase/dt",
   scope="Linear phase-domain model; no transistor VCO or cycle-slip simulation."),
 "B07": dict(case="B07_100V_25C", title="Buck power stage: voltage, current and output ripple",
   zh="Buck功率级：电压、电流与输出纹波", kind="SWITCHED TRANSIENT", groups=[[2],[1],[0]], time_max=4e-6,
   teach="The switching node drives inductor current up and down. The LC state is integrated, so output ripple is calculated here. This view shows the first saved switching cycle.",
   teach_zh="开关节点使电感电流上升或下降；该模型积分LC状态，因此这里计算了输出纹波。本图显示首个保存的开关周期。",
   equation="L dIL/dt = Vsw - Vout - R_L IL",
   scope="Ideal gate commands and conduction losses; no dead time, Qrr or gate dynamics."),
 "P01": dict(case="P01_100V_25C", title="MOS turn-on: gate charging and Miller plateau",
   zh="MOS导通：栅充电与Miller平台", kind="STAGED TRANSIENT", groups=[[0],[1],[2,3]],
   teach="During the Miller interval, gate charge changes drain voltage while Vgs stays near a plateau. The channel-current and gate-current traces are distinct quantities.",
   teach_zh="Miller阶段中，栅电荷改变漏压而Vgs停留在平台附近；沟道电流与栅电流是两个不同量。",
   equation="Ig = (Vdrive - Vgs)/Rg; Qgd = integral Cgd dV",
   scope="Prescribed commutation; not a fully coupled charge-conserving MOS solver."),
 "P02": dict(case="P02_100V_25C", title="Dead time: the positive inductor current keeps flowing",
   zh="死区：正向电感电流仍然续流", kind="PIECEWISE TRANSIENT", groups=[[0],[1,2],[3,4,5]],
   teach="During dead time both gate commands are OFF, but the low-side diode carries positive inductor current. Each interval is given display time so the short dead times remain visible.",
   teach_zh="死区内两个栅命令均关断，但低侧二极管仍承载正向电感电流。各区间分配显示时间，使很短的死区也能看清。",
   equation="During diode freewheel: Vsw = -VF",
   scope="Fixed 12 V output; separate prescribed reverse recovery is not added to this trace."),
 "P03": dict(case="P03_100V_25C", title="Bootstrap supply: consume charge, then recharge",
   zh="自举电源：消耗电荷后再补充", kind="TIME TRANSIENT", groups=[[0],[1,2],[3]], time_min=40e-6,
   teach="Gate-charge removal lowers VBS. When the recharge path is available, current restores it toward the supply-minus-diode limit. The final two cycles are shown.",
   teach_zh="栅电荷消耗降低VBS；补充通路开放时，电流把它恢复到电源减去二极管压降的上限。这里显示最后两个周期。",
   equation="Delta VBS = -Qgate/Cboot (gate-charge event)",
   scope="Lumped charge budget; local VBS is not the gate voltage relative to ground."),
 "P04": dict(case="P04_100V_25C_strong", title="Level shifter: common-mode edge injects current",
   zh="电平移位：共模边沿注入电流", kind="TIME TRANSIENT", groups=[[0],[1],[2,3]],
   teach="A changing common-mode voltage injects displacement current through a small coupling capacitance. The receiver resistance and capacitance determine its disturbance.",
   teach_zh="变化的共模电压经小耦合电容注入位移电流；接收端电阻和电容决定扰动幅度。",
   equation="Iinjected = Ccm dVcm/dt",
   scope="Linear disturbance model; no full latch logic or measured CMTI qualification."),
 "P05": dict(case="P05_25C", title="Current sensing: filtering and comparator delay",
   zh="电流检测：滤波与比较器延迟", kind="TIME TRANSIENT", groups=[[0],[2],[3]], time_max=.5e-6,
   teach="The shunt turns current into voltage. The amplifier responds with finite bandwidth, then a delayed comparator changes state. Detection does not stop the prescribed load current here.",
   teach_zh="取样电阻把电流变成电压；放大器具有有限带宽，比较器再经延迟改变状态。本模型检测后不会切断预设负载电流。",
   equation="Vsense = Iload Rsense",
   scope="Sensing bench only; comparator output is not a simulated shutdown loop."),
 "P06": dict(case="P06_100V_25C", title="Startup supply: charge storage and UVLO hysteresis",
   zh="启动供电：储能与欠压迟滞", kind="TIME TRANSIENT", groups=[[0],[1],[2,3,4]],
   teach="The startup source charges Caux before enable. Different ON/OFF thresholds prevent a single-threshold toggle. The prescribed supply interruption creates a brownout and restart.",
   teach_zh="启动源先给Caux充电再使能；不同开启与关闭阈值形成迟滞。预设供电中断导致掉电与重新启动。",
   equation="Caux dVaux/dt = Istart - Iload - Iclamp",
   scope="Lumped startup source and ideal clamp; no HV transistor stress solution."),
 "P07": dict(case="P07_100V_damped", title="Parasitic ringing: stored energy becomes damping loss",
   zh="寄生振铃：储能转化为阻尼损耗", kind="TIME TRANSIENT", groups=[[0],[1],[2]], time_max=60e-9,
   teach="An imposed initial voltage excess excites the parasitic LC loop. Series resistance removes its stored energy. The early 60 ns show the damped response.",
   teach_zh="预设初始过压激发寄生LC环路；串联电阻耗散储能。前60 ns展示阻尼响应。",
   equation="E = (1/2)L i^2 + (1/2)C v_excess^2",
   scope="Initial-condition RLC response; not a solved MOS switching edge or extracted layout."),
 "P08": dict(case="P08_100V_25C", title="Loss budget: power becomes temperature rise",
   zh="损耗预算：功率转化为温升", kind="THERMAL TRANSIENT", groups=[[0]],
   teach="The fixed-point loss ledger sets a thermal RC step response. The bars are the steady operating loss components, not instantaneous switching power.",
   teach_zh="固定点损耗账本驱动热RC阶跃响应。条形图是稳态工作点的损耗分项，并非瞬时开关功率。",
   equation="T(t) = Ta + P_loss Rtheta (1 - exp(-t/tau))",
   scope="One effective thermal node; no package heat map or independent device junction temperatures."),
 "P09": dict(case="P09_100V_25C", title="Averaged buck: soft-start and current-reference limiting",
   zh="平均Buck：软启动与电流参考限幅", kind="AVERAGED TRANSIENT", groups=[[0,1],[2,3,4],[6]],
   teach="The reference ramps up, then a load change asks for more current. The clipped current command limits the average current; output voltage can fall when demand is too high.",
   teach_zh="参考电压缓慢上升，负载改变后要求更高电流；电流指令限幅约束平均电流，需求过大时输出电压下降。",
   equation="L dIL/dt = D Vin - R IL - Vout",
   scope="Average control states; no PWM ripple, per-cycle current trip or transistor switching."),
}

def signal_value(case, idx, k):
    return float(case["signals"][idx]["y"][k])

def functional(d, nodes, lines, colors=None):
    for a,b in lines:
        ra,rb=nodes[a][0],nodes[b][0]
        if rb[0]>=ra[2]:
            arrow(d,(ra[2],(ra[1]+ra[3])/2),(rb[0],(rb[1]+rb[3])/2))
        elif rb[2]<=ra[0]:
            arrow(d,(ra[0],(ra[1]+ra[3])/2),(rb[2],(rb[1]+rb[3])/2))
        elif rb[3]<=ra[1]:
            arrow(d,((ra[0]+ra[2])/2,ra[1]),((rb[0]+rb[2])/2,rb[3]))
        else:
            arrow(d,((ra[0]+ra[2])/2,ra[3]),((rb[0]+rb[2])/2,rb[1]))
    for i,(r,l) in enumerate(nodes):
        box(d,r,l,(colors or {}).get(i,"cyan"),size=15)

def diagram(d, mid, c, k):
    """Model-specific simplified symbols. No inferred carrier trajectories."""
    val=lambda idx: signal_value(c,idx,k)
    x=float(c["x"][k])
    text(d,(36,137),"MECHANISM VIEW",14,"muted",True)
    if mid=="A01":
        box(d,(65,243,305,323),"Body", "purple",size=18)
        box(d,(75,226,120,265),"S", "green")
        box(d,(250,226,295,265),"D", "orange")
        wire(d,[(127,222),(244,222)],"cyan",7)
        wire(d,[(130,210),(240,210)],"muted",2)
        wire(d,[(185,194),(185,210)],"cyan")
        text(d,(185,180),"Gate",17,"cyan",True,"mm")
        text(d,(185,350),"Vg = "+eng(x,"V"),20,"cyan",True,"mm")
        text(d,(185,384),"Id = "+eng(val(0),"A"),20,"green",True,"mm")
        text(d,(185,414),"Schematic section; not to scale",13,"muted",anchor="mm")
    elif mid=="A02":
        box(d,(62,226,178,300),"P / anode","orange",size=18)
        box(d,(190,226,306,300),"N / cathode","cyan",size=18)
        wire(d,[(90,226),(90,200),(165,200)])
        wire(d,[(205,200),(278,200),(278,226)])
        d.ellipse((165,180,205,220),outline=COL["muted"],width=2)
        text(d,(185,200),"V",16,"text",True,"mm")
        text(d,(185,169),"Va - Vk = "+eng(x,"V"),16,"text",anchor="mm")
        text(d,(185,340),"Cj = "+eng(val(0),"F"),20,"cyan",True,"mm")
        text(d,(185,378),"Qj = "+eng(val(1),"C"),20,"orange",True,"mm")
        text(d,(185,414),"Fixed geometry; no field solver",13,"muted",anchor="mm")
    elif mid=="A03":
        box(d,(120,225,250,320),"NPN","cyan",size=24)
        wire(d,[(185,185),(185,225)]);wire(d,[(185,320),(185,350)])
        wire(d,[(68,272),(120,272)])
        text(d,(185,174),"C",18,"orange",True,"mm")
        text(d,(55,272),"B",18,"purple",True,"mm")
        text(d,(185,364),"E",18,"green",True,"mm")
        text(d,(185,397),"Vbe = "+eng(x,"V"),20,"cyan",True,"mm")
        text(d,(185,427),"Currents positive into device",13,"muted",anchor="mm")
    elif mid=="A04":
        box(d,(49,192,172,258),"Device 1","cyan")
        box(d,(196,192,319,258),"Device 2","orange")
        text(d,(110,282),eng(val(0),"V"),18,"cyan",True,"mm")
        text(d,(258,282),eng(val(1),"V"),18,"orange",True,"mm")
        arrow(d,(110,302),(166,339),"cyan");arrow(d,(258,302),(203,339),"orange")
        box(d,(93,342,277,397),"Difference "+eng(val(2),"V"),"green",size=15)
        text(d,(185,425),"Sample "+str(int(x))+" / not time",16,"muted",anchor="mm")
    elif mid=="B01":
        box(d,(55,208,155,265),"Q1","cyan");box(d,(215,208,315,265),"Q2","orange")
        wire(d,[(105,265),(105,312),(265,312),(265,265)])
        wire(d,[(185,312),(185,342)])
        box(d,(116,342,254,384),"Tail 100 uA","green",size=16)
        text(d,(105,187),eng(val(0),"A"),18,"cyan",True,"mm")
        text(d,(265,187),eng(val(1),"A"),18,"orange",True,"mm")
        text(d,(185,419),"Vdiff = "+eng(x,"V"),20,"text",True,"mm")
    elif mid=="B02":
        functional(d,[((45,183,158,240),"CTAT Vbe"),((45,284,158,341),"PTAT x K"),
                      ((220,232,318,293),"SUM")],[(0,2),(1,2)],{0:"cyan",1:"orange",2:"green"})
        text(d,(101,256),eng(val(1),"V"),16,"cyan",anchor="mm")
        text(d,(101,357),eng(val(2),"V"),16,"orange",anchor="mm")
        text(d,(185,403),"Vref = "+eng(val(0),"V"),20,"green",True,"mm")
        text(d,(185,432),"Temperature = "+fmt(x)+" degC",16,"muted",anchor="mm")
    elif mid=="B03":
        functional(d,[((45,189,160,245),"White noise"),((45,291,160,347),"1/f term"),
                      ((218,235,320,298),"PSD sum")],[(0,2),(1,2)])
        text(d,(185,385),"f = "+eng(x,"Hz"),22,"cyan",True,"mm")
        text(d,(185,423),"No random time waveform is shown",13,"muted",anchor="mm")
    elif mid=="B04":
        functional(d,[((42,190,144,245),"Sample"),((210,190,320,245),"Compare"),
                      ((210,310,320,365),"SAR code"),((42,310,144,365),"CDAC")],
                   [(0,1),(1,2),(2,3)],{1:"orange",2:"green"})
        wire(d,[(144,337),(177,337),(177,234)],"muted",2)
        arrow(d,(177,234),(210,234))
        text(d,(185,280),"Final code = "+str(int(val(2))),20,"orange",True,"mm")
        text(d,(185,412),"Vin = "+eng(val(0),"V"),20,"cyan",True,"mm")
        text(d,(185,439),"Block arrows show information flow",13,"muted",anchor="mm")
    elif mid=="B05":
        functional(d,[((45,198,158,254),"Error amp"),((218,198,320,254),"Pass FET"),
                      ((218,326,320,383),"Cout/load")],[(0,1),(1,2)],{2:"green"})
        wire(d,[(218,354),(94,354),(94,254)],"muted",2)
        text(d,(185,285),"Ipass = "+eng(val(1),"A"),18,"cyan",True,"mm")
        text(d,(185,418),"Iload = "+eng(val(2),"A"),18,"orange",True,"mm")
    elif mid=="B06":
        functional(d,[((45,195,158,253),"Phase error"),((216,195,320,253),"Filter"),
                      ((216,322,320,380),"VCO phase")],[(0,1),(1,2)])
        wire(d,[(216,351),(100,351),(100,253)],"muted",2)
        text(d,(185,282),"zeta = "+fmt(c["metrics"]["zeta"]),18,"orange",True,"mm")
        text(d,(185,418),"Phase = "+fmt(val(0))+" rad",20,"cyan",True,"mm")
    elif mid in ("B07","P02"):
        qh=val(4) if mid=="B07" else val(3)
        ql=(1.0 if not qh else 0.0) if mid=="B07" else val(4)
        il=val(1); vs=val(2) if mid=="B07" else val(0)
        wire(d,[(95,177),(95,205)])
        box(d,(61,205,129,250),"QH","green" if qh else "muted")
        wire(d,[(95,250),(95,291),(163,291)])
        box(d,(163,270,238,313),"L","cyan")
        wire(d,[(238,291),(297,291),(297,307)])
        box(d,(271,307,323,346),"Load","muted",size=12)
        wire(d,[(297,346),(297,367),(95,367)])
        box(d,(53,304,137,349),"QL / diode" if mid=="P02" else "QL",
            "green" if ql else ("orange" if mid=="P02" else "muted"),size=12 if mid=="P02" else 16)
        wire(d,[(95,291),(95,304)]);wire(d,[(95,349),(95,367)])
        text(d,(95,164),str(c["vin_V"])+" V",18,"orange",True,"mm")
        text(d,(185,398),"SW = "+eng(vs,"V"),18,"cyan",True,"mm")
        text(d,(185,428),"IL = "+eng(il,"A"),18,"green",True,"mm")
        if mid=="P02" and val(5):
            text(d,(185,465),"DEAD TIME: low-side body diode",14,"orange",True,"mm")
        else:
            text(d,(185,465),"QH ON" if qh else "QL ON",14,"green",True,"mm")
    elif mid=="P01":
        functional(d,[((42,184,143,239),"Driver"),((213,184,320,239),"Rg"),
                      ((213,310,320,367),"MOS gate")],[(0,1),(1,2)])
        box(d,(53,310,154,367),"Cgs / Cgd","orange",size=14)
        wire(d,[(154,339),(213,339)],"orange",2)
        text(d,(185,276),"Vgs = "+eng(val(0),"V"),20,"cyan",True,"mm")
        text(d,(185,412),"Vds = "+eng(val(1),"V"),20,"orange",True,"mm")
    elif mid=="P03":
        functional(d,[((45,184,159,241),"Supply"),((214,184,320,241),"D + R"),
                      ((214,314,320,371),"Cboot"),((45,314,159,371),"Driver")],
                   [(0,1),(1,2),(2,3)],{2:"green"})
        text(d,(185,276),"VBS = "+eng(val(0),"V"),20,"green",True,"mm")
        text(d,(185,418),"Irecharge = "+eng(val(1),"A"),18,"cyan",True,"mm")
        text(d,(185,446),"Floating local supply",14,"muted",anchor="mm")
    elif mid=="P04":
        functional(d,[((45,185,160,241),"Vcm edge"),((214,185,320,241),"Ccm"),
                      ((214,321,320,377),"Receiver"),
                      ((45,321,160,377),"R + C load")],[(0,1),(1,2),(2,3)])
        text(d,(185,278),"Vcm = "+eng(val(0),"V"),20,"orange",True,"mm")
        text(d,(185,421),"Disturbance = "+eng(val(1),"V"),18,"cyan",True,"mm")
    elif mid=="P05":
        functional(d,[((42,184,145,240),"Rsense"),((211,184,320,240),"Amplifier"),
                      ((211,319,320,375),"Comparator"),((42,319,145,375),"Logic flag")],
                   [(0,1),(1,2),(2,3)],{3:"red" if val(3) else "green"})
        text(d,(185,276),"Iload = "+eng(val(0),"A"),20,"cyan",True,"mm")
        text(d,(185,418),"TRIP FLAG = "+str(int(val(3))),20,"red" if val(3) else "green",True,"mm")
    elif mid=="P06":
        functional(d,[((44,184,155,240),"HV source"),((214,184,320,240),"Caux"),
                      ((214,320,320,376),"UVLO"),((44,320,155,376),"Aux load")],
                   [(0,1),(1,2),(2,3)],{1:"cyan",2:"green" if val(1) else "orange"})
        text(d,(185,277),"Vaux = "+eng(val(0),"V"),20,"cyan",True,"mm")
        text(d,(185,419),"ENABLE = "+str(int(val(1))),20,"green" if val(1) else "orange",True,"mm")
    elif mid=="P07":
        box(d,(45,202,127,258),"Lpar","cyan")
        box(d,(233,202,315,258),"Rseries","orange",size=14)
        box(d,(142,329,225,385),"Cpar","green")
        wire(d,[(127,230),(233,230)])
        wire(d,[(315,230),(332,230),(332,357),(225,357)])
        wire(d,[(142,357),(30,357),(30,230),(45,230)])
        text(d,(185,290),"Initial excess = 15% of Vin",15,"muted",anchor="mm")
        text(d,(185,417),"Vsw = "+eng(val(0),"V"),20,"cyan",True,"mm")
    elif mid=="P08":
        functional(d,[((45,183,161,241),"Loss ledger"),((211,183,320,241),"Thermal RC"),
                      ((211,321,320,380),"Hot node")],[(0,1),(1,2)],{0:"orange",2:"red"})
        text(d,(185,275),"Ptotal = "+eng(c["metrics"]["total_loss_W"],"W"),20,"orange",True,"mm")
        text(d,(185,417),"T = "+fmt(val(0))+" degC",22,"red",True,"mm")
        text(d,(185,447),"One effective thermal node",14,"muted",anchor="mm")
    elif mid=="P09":
        functional(d,[((43,184,151,240),"Soft-start"),((212,184,320,240),"Voltage PI"),
                      ((212,320,320,376),"Iref limit"),((43,320,151,376),"Buck average")],
                   [(0,1),(1,2),(2,3)],{2:"orange",3:"green"})
        text(d,(185,276),"Duty = "+fmt(100*val(6))+" %",20,"cyan",True,"mm")
        text(d,(185,418),"Vout = "+eng(val(0),"V"),20,"green",True,"mm")

def make_panels(c, spec):
    x=np.asarray(c["x"],dtype=float)
    mask=np.ones(len(x),dtype=bool)
    if "samples" in spec: mask[np.arange(len(x))>=spec["samples"]]=False
    if "time_max" in spec: mask &= x<=spec["time_max"]*(1+1e-10)
    if "time_min" in spec: mask &= x>=spec["time_min"]*(1-1e-10)
    indices=np.flatnonzero(mask)
    panels=[]
    for gi,group in enumerate(spec["groups"]):
        ys=[]
        for si in group:
            if si=="error":
                a=np.asarray(c["signals"][1]["y"])-np.asarray(c["signals"][0]["y"])
                ys.append(dict(name="Reconstruction error",unit="V",y=a[indices]))
            else:
                s=c["signals"][si]
                ys.append(dict(name=en(s["name"]),unit=s["unit"],y=np.asarray(s["y"])[indices]))
        unit=ys[0]["unit"]
        peak=max(float(np.max(np.abs(s["y"]))) for s in ys)
        factor,pre=1.0,""
        if unit in ("A","V","C","F","J","S","W"):
            for fac,prefix in ((1e-12,"p"),(1e-9,"n"),(1e-6,"u"),(1e-3,"m"),(1,""),(1e3,"k")):
                if peak<1000*fac:
                    factor,pre=fac,prefix;break
        if unit=="V/sqrt(Hz)": factor,pre=1e-9,"n"
        for s in ys: s["y"]=s["y"]/factor
        binary=unit=="1" and all(np.isin(s["y"],[0,1]).all() for s in ys)
        panels.append(dict(x=x[indices],ys=ys,unit=pre+unit if unit!="1" else "",scale=factor,binary=binary,
                           logx=spec.get("logx",False),logy=gi in spec.get("logy",[])))
    return panels, indices

def x_axis(c,spec,x):
    if spec["kind"] in ("DC SWEEP","TEMPERATURE SWEEP","STATISTICAL SAMPLES","FREQUENCY SWEEP"):
        labels={"A01":"Gate voltage (V)","A02":"Va - Vk (V)","A03":"Vbe (V)",
                "A04":"Sample index (not time)","B01":"Differential input (V)",
                "B02":"Temperature (degC)","B03":"Frequency (Hz)"}
        return 1.0, labels[c["model_id"]]
    mag=max(abs(float(x[0])),abs(float(x[-1])))
    if mag<1e-6:return 1e-9,"Physical time (ns)"
    if mag<1e-3:return 1e-6,"Physical time (us)"
    if mag<1:return 1e-3,"Physical time (ms)"
    return 1.0,"Physical time (s)"

def plot(d, panel, rect, cursor, c, spec):
    x0,y0,x1,y1=rect
    d.rounded_rectangle(rect,9,fill=COL["panel"])
    x=panel["x"]
    ys=panel["ys"]
    sf,xlabel=x_axis(c,spec,x)
    xp=x/sf
    xx=np.log10(xp) if panel["logx"] else xp
    yy=[np.log10(np.maximum(s["y"],1e-30)) if panel["logy"] else s["y"] for s in ys]
    ymin=min(float(np.min(y)) for y in yy);ymax=max(float(np.max(y)) for y in yy)
    span=ymax-ymin
    if span<1e-12: span=max(abs(ymax)*.1,.1)
    ymin-=span*.08;ymax+=span*.12
    if panel["binary"]: ymin,ymax=-.05,1.05
    pl,pr=x0+66,x1-18;pt,pb=y0+42,y1-40
    if len(ys)>2: pt+=18
    for j,s in enumerate(ys):
        label=s["name"]
        if len(label)>24:label=label[:22]+"..."
        row=j//2;col=j%2
        dynamic_span=float(np.max(s["y"])-np.min(s["y"]))
        value=axisfmt(s["y"][cursor],dynamic_span) if 0<dynamic_span<abs(s["y"][cursor])*.1 else fmt(s["y"][cursor])
        txt=label+" = "+value+" "+panel["unit"]
        text(d,(x0+14+col*288,y0+9+row*19),txt,13,PALETTE[j],True)
    def px(v):return pl+(v-xx[0])/(xx[-1]-xx[0])*(pr-pl)
    def py(v):return pb-(v-ymin)/(ymax-ymin)*(pb-pt)
    for f in (0,.5,1):
        y=ymin+f*(ymax-ymin)
        liney=py(y)
        wire(d,[(pl,liney),(pr,liney)],"grid",1)
        label=fmt(10**y) if panel["logy"] else axisfmt(y,ymax-ymin)
        text(d,(pl-7,liney),label,12,"muted",anchor="rm")
    for f in (0,.5,1):
        z=xx[0]+f*(xx[-1]-xx[0])
        xxp=px(z)
        wire(d,[(xxp,pt),(xxp,pb)],"grid",1)
        text(d,(xxp,pb+6),fmt(10**z if panel["logx"] else z),12,"muted",anchor="mt")
    for j,y in enumerate(yy):
        # All displayed samples, including duplicate switching-event times, remain in the trace.
        pts=[(px(a),py(b)) for a,b in zip(xx,y)]
        d.line(pts,fill=PALETTE[j],width=2)
        cy=py(y[cursor]);cx=px(xx[cursor])
        d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=PALETTE[j])
    cx=px(xx[cursor])
    wire(d,[(cx,pt),(cx,pb)],"text",1)
    text(d,((pl+pr)/2,y1-8),xlabel+(" | log x" if panel["logx"] else "")+(" | log y" if panel["logy"] else ""),12,"muted",anchor="ms")

def loss_bars(d,c,rect):
    x0,y0,x1,y1=rect
    d.rounded_rectangle(rect,9,fill=COL["panel"])
    text(d,(x0+14,y0+10),"Steady loss ledger (W) - static operating point",16,"text",True)
    data=c.get("loss_components_W",{})
    if isinstance(data,list):
        data={str(i+1):v for i,v in enumerate(data)}
    names={"high_side_conduction_W":"HS conduction","low_side_conduction_W":"LS conduction",
           "inductor_copper_W":"Inductor copper","channel_overlap_W":"Channel overlap",
           "Coss_commutation_W":"Coss commutation","recovery_bus_estimate_W":"Recovery estimate",
           "gate_driver_supply_W":"Gate supply","deadtime_diode_W":"Dead-time diode",
           "assumed_control_supply_W":"Assumed control"}
    data={k:float(v) for k,v in data.items()}
    if not data:
        data={k:float(c["metrics"][k]) for k in names if k in c["metrics"]}
    top=max(data.values())
    for i,(k,v) in enumerate(data.items()):
        y=y0+44+i*25
        text(d,(x0+14,y),names.get(k,k.replace("_"," ").removesuffix(" W"))[:25],14,"muted")
        bx=x0+220;bw=(x1-bx-75)*v/top
        d.rectangle((bx,y+2,bx+max(bw,1),y+15),fill=COL["orange"])
        text(d,(x1-14,y),fmt(v),14,"text",anchor="ra")

def frame(mid,c,spec,panels,indices,local_idx,number,total):
    im=Image.new("RGB",(W,H),COL["bg"]);d=ImageDraw.Draw(im)
    text(d,(28,22),mid,30,"cyan",True)
    title=spec["title"]
    size=27 if d.textlength(title,font=F[27,True])<920 else 24
    text(d,(110,24),title,size,"text",True)
    tag=spec["kind"]
    text(d,(30,68),tag,16,"orange",True)
    conditions=c["id"]+" | "
    conditions+=(str(c["vin_V"])+" V input | ") if c.get("vin_V") is not None else ""
    conditions+=(str(c["temp_C"])+" degC") if c.get("temp_C") is not None else "see swept axis"
    text(d,(380,70),conditions,14,"muted")
    d.rounded_rectangle((22,112,350,638),12,fill=COL["panel"])
    diagram(d,mid,c,int(indices[local_idx]))
    text(d,(36,487),"WHAT TO NOTICE",14,"orange",True)
    wrap(d,(36,512),spec["teach"],width=298,size=15,leading=20,max_lines=6)
    n=len(panels)
    if mid=="P08":
        plot(d,panels[0],(366,112,1058,327),local_idx,c,spec)
        loss_bars(d,c,(366,340,1058,638))
    else:
        gap=10
        h=(526-gap*(n-1))/n
        for j,p in enumerate(panels):
            y=112+j*(h+gap)
            plot(d,p,(366,int(y),1058,int(y+h)),local_idx,c,spec)
    text(d,(30,653),spec["equation"],17,"cyan",True)
    wrap(d,(30,679),spec["scope"],width=1000,size=13,leading=17,max_lines=1)
    text(d,(1048,709),str(number+1)+"/"+str(total)+" | cursor = saved sample",12,"muted",anchor="rs")
    text(d,(30,709),"Illustrative public-source model | Display speed is not physical elapsed time | No PDK calibration",12,"muted",anchor="ls")
    return im

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--analog",type=Path,default=REPO/"v33/numerics/analog/simulation.json")
    ap.add_argument("--dcdc",type=Path,default=REPO/"v33/numerics/dcdc/simulation.json")
    ap.add_argument("--out",type=Path,default=HERE)
    ap.add_argument("--inspection-dir",type=Path)
    ap.add_argument("--models",nargs="*")
    args=ap.parse_args()
    for p in (args.out/"gifs",args.out/"posters"):p.mkdir(parents=True,exist_ok=True)
    datasets=[(args.analog,json.loads(args.analog.read_text(encoding="utf-8"))),
              (args.dcdc,json.loads(args.dcdc.read_text(encoding="utf-8")))]
    cases={c["id"]:(p,c) for p,data in datasets for c in data["cases"]}
    models={m["id"]:m for _,data in datasets for m in data["models"]}
    manifest_path=args.out/"manifest.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8")) if args.models and manifest_path.is_file() else {}
    for mid,spec in SPECS.items():
        if args.models and mid not in args.models: continue
        source,c=cases[spec["case"]]
        spec=dict(spec)
        if mid=="A04":
            sample_count=int(c["metrics"]["sample_count"])
            spec["teach"]=spec["teach"].replace("20,000",f"{sample_count:,}")
            spec["teach_zh"]=spec["teach_zh"].replace("20000",str(sample_count))
        panels,indices=make_panels(c,spec)
        count=48
        cursor_indices=np.rint(np.linspace(0,len(indices)-1,count)).astype(int)
        frames=[frame(mid,c,spec,panels,indices,k,j,count) for j,k in enumerate(cursor_indices)]
        # Include every state color; a common palette and disposal=1 enable sparse deltas.
        rgb=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))
        colors=[rgb(h) for h in COL.values()]
        for fg in tuple(colors):
            for bg in (rgb(COL["bg"]),rgb(COL["panel"])):
                for alpha in (.25,.5,.75):
                    colors.append(tuple(round(alpha*a+(1-alpha)*b) for a,b in zip(fg,bg)))
        raw=[v for c in colors for v in c]
        raw=(raw+[0]*768)[:768]
        pal=Image.new("P",(1,1));pal.putpalette(raw)
        frames_p=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
        durations=[150]*count;durations[0]=600;durations[-1]=900
        gp=args.out/"gifs"/(mid+".gif")
        pp=args.out/"posters"/(mid+".png")
        frames_p[0].save(gp,save_all=True,append_images=frames_p[1:],duration=durations,loop=0,optimize=True,disposal=1)
        poster_index=count//2 if mid not in ("P05","P07") else count//3
        frames[poster_index].save(pp)
        with Image.open(gp) as g:
            actual_frames=g.n_frames
            duration=0
            for j in range(g.n_frames):g.seek(j);duration+=g.info["duration"];g.load()
            assert g.size==(W,H)
        with Image.open(pp) as p:p.verify()
        def rel(p):
            try:return p.resolve().relative_to(REPO).as_posix()
            except ValueError:return p.name
        manifest[mid]=dict(model_id=mid,gif=rel(gp),poster=rel(pp),case_id=c["id"],
            title_en=spec["title"],title_zh=spec["zh"],explanation_en=spec["teach"],
            explanation_zh=spec["teach_zh"],animation_kind=spec["kind"],
            animation_type_en=spec["kind"].capitalize(),
            animation_type_zh={"DC SWEEP":"直流偏置扫描","TEMPERATURE SWEEP":"温度扫描",
                "STATISTICAL SAMPLES":"随机样本统计","FREQUENCY SWEEP":"频率扫描",
                "SAMPLED SIGNAL":"采样信号","TIME TRANSIENT":"时间瞬态",
                "SWITCHED TRANSIENT":"开关瞬态","STAGED TRANSIENT":"分阶段瞬态",
                "PIECEWISE TRANSIENT":"分段瞬态","THERMAL TRANSIENT":"热瞬态",
                "AVERAGED TRANSIENT":"平均模型瞬态"}[spec["kind"]],
            axis_en=x_axis(c,spec,panels[0]["x"])[1],
            axis_zh={"DC SWEEP":"直流偏置扫描（非时间）","TEMPERATURE SWEEP":"温度扫描（非时间）",
                     "STATISTICAL SAMPLES":"随机样本序号（非时间）","FREQUENCY SWEEP":"频率扫描（非时间）"}.get(spec["kind"],"物理时间（播放速度经过调整）"),
            equation=spec["equation"],scope_en=spec["scope"],scope_zh=models[mid].get("limits_zh",""),
            limits_en=models[mid].get("limits_en",""),limits_zh=models[mid].get("limits_zh",""),
            source=rel(source),source_sha256=digest(source),source_ids=models[mid].get("source_ids",[]),
            x_display_min=float(panels[0]["x"][0]),x_display_max=float(panels[0]["x"][-1]),
            frames=actual_frames,duration_ms=duration,width=W,height=H,
            bytes=gp.stat().st_size,gif_sha256=digest(gp),poster_sha256=digest(pp),
            annotation_language="English only",validation="decoded all frames; dimensions, timing and hashes checked",
            sampled_indices=[int(indices[i]) for i in cursor_indices],plot_signal_names=[[s["name"] for s in p["ys"]] for p in panels])
        if mid=="A04":manifest[mid]["statistical_sample_count"]=sample_count
        if args.inspection_dir:
            args.inspection_dir.mkdir(parents=True,exist_ok=True)
            for j in (0,poster_index,count-1):
                frames[j].save(args.inspection_dir/f"{mid}_{j:02}.png")
        print(mid,c["id"],actual_frames,duration,gp.stat().st_size,flush=True)
    # Enrich preserved records as well when a selected asset is refreshed.
    for mid,record in manifest.items():
        record["scope_zh"]=models[mid].get("limits_zh","")
        record["source_ids"]=models[mid].get("source_ids",[])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    gallery=["# Animated model gallery","","# 模型动画总览","",
             "Each GIF uses actual V3.3 case samples. Read the animation type before interpreting motion.",
             "","每个GIF使用V3.3实际案例样本。理解运动之前，请先查看动画类型。","",
             "| Model | Lesson / 课程 | Animation type / 动画类型 | Files / 文件 |",
             "|---|---|---|---|"]
    for mid,r in manifest.items():
        gallery.append(f"| {mid} | {r['title_en']}<br>{r['title_zh']} | {r['animation_type_en']}<br>{r['animation_type_zh']} | [GIF](gifs/{mid}.gif) · [PNG](posters/{mid}.png) |")
    gallery.extend(["","See [usage and limitations](README.md) and [the complete provenance manifest](manifest.json).","",
                    "使用方法与边界见[说明](README.md)，完整来源记录见[清单](manifest.json)。",""])
    (args.out/"GALLERY.md").write_text("\n".join(gallery),encoding="utf-8")
    if args.inspection_dir and manifest:
        entries=list(manifest)
        thumb_w,thumb_h=432,288
        for batch in range(0,len(entries),10):
            subset=entries[batch:batch+10]
            sheet=Image.new("RGB",(thumb_w*2,thumb_h*5),COL["bg"])
            for i,mid in enumerate(subset):
                p=Image.open(args.out/"posters"/(mid+".png"))
                p.thumbnail((thumb_w,thumb_h))
                sheet.paste(p,((i%2)*thumb_w,(i//2)*thumb_h))
            sheet.save(args.inspection_dir/f"contact_sheet_{batch//10+1}.png")
    print("Manifest models:",len(manifest),flush=True)

if __name__=="__main__":
    main()
