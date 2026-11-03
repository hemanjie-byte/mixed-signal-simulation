"""Render the P02 teaching trace as an English-only, reproducible GIF.

Requires NumPy and Pillow. No AI image generation, circuit solver or external
web resources are used by this renderer. Re-run the model suite first.
"""
from pathlib import Path
import argparse, csv, hashlib, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WIDTH, HEIGHT = 1160, 780
COLORS = {
    'bg': '#F1F5F8', 'paper': '#FFFFFF', 'navy': '#183247',
    'muted': '#536A7B', 'line': '#CAD6DF', 'wire': '#8D9DAA',
    'current': '#087F78', 'diode': '#B36112', 'blue': '#2368A2',
    'lightblue': '#E8F1F8', 'lightteal': '#E4F2EE',
    'lightamber': '#FFF0DC', 'red': '#B53D43', 'black': '#101D28'
}


def font(size, bold=False):
    names = [
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf',
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    raise RuntimeError('Install Arial or DejaVu Sans, or adapt the documented font paths.')


F = {n: font(n) for n in [13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 28, 32]}
FB = {n: font(n, True) for n in F}


def text(draw, xy, value, size=18, color='navy', bold=False, anchor=None):
    draw.text(xy, value, font=(FB if bold else F)[size], fill=COLORS.get(color, color), anchor=anchor)


def wrapped(draw, xy, value, width, size=18, color='navy', spacing=6):
    x, y = xy
    for paragraph in value.split('\n'):
        words = paragraph.split(); line = ''
        for word in words:
            trial = (line + ' ' + word).strip()
            if line and draw.textlength(trial, font=F[size]) > width:
                text(draw, (x, y), line, size, color); y += size + spacing; line = word
            else:
                line = trial
        if line:
            text(draw, (x, y), line, size, color); y += size + spacing
    return y


def line(draw, points, color='wire', width=3):
    draw.line(points, fill=COLORS.get(color, color), width=width, joint='curve')


def arrow(draw, start, end, color='current', width=3, head=8):
    line(draw, [start, end], color, width)
    dx, dy = end[0]-start[0], end[1]-start[1]
    length = math.hypot(dx, dy)
    if length == 0: return
    ux, uy = dx/length, dy/length
    a = (end[0]-head*ux+head*.55*uy, end[1]-head*uy-head*.55*ux)
    b = (end[0]-head*ux-head*.55*uy, end[1]-head*uy+head*.55*ux)
    draw.polygon([end, a, b], fill=COLORS[color])


def moving_arrows(draw, points, phase, color='current', count=9):
    points = np.array(points, dtype=float)
    lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
    cum = np.r_[0, np.cumsum(lengths)]; total = cum[-1]
    for k in range(count):
        distance = ((k/count + phase) % 1)*total
        j = min(np.searchsorted(cum, distance, side='right')-1, len(lengths)-1)
        if lengths[j] < 1e-9: continue
        ratio = (distance-cum[j])/lengths[j]
        tip = points[j] + ratio*(points[j+1]-points[j])
        direction = (points[j+1]-points[j])/lengths[j]
        arrow(draw, tuple(tip-11*direction), tuple(tip), color, width=3, head=7)


def coil_points():
    points = []
    for j in range(4):
        for theta in np.linspace(math.pi, 0, 20):
            points.append((442+24*j+12*math.cos(theta), 315-15*math.sin(theta)))
    return points


def resistor_points(x, ya, yb):
    return [(x, ya)] + [(x+(8 if i%2 else -8), ya+(yb-ya)*(i+1)/10) for i in range(9)] + [(x, yb)]


def switch(draw, x, ya, yb, active, name, current_color='current'):
    ink = current_color if active else 'wire'
    draw.ellipse((x-4, ya-4, x+4, ya+4), fill=COLORS[ink])
    draw.ellipse((x-4, yb-4, x+4, yb+4), fill=COLORS[ink])
    line(draw, [(x, yb), (x if active else x-22, ya+2)], ink, 5)
    text(draw, (x-58, (ya+yb)/2-12), name, 20, ink, True)


def base_image(title, subtitle):
    im = Image.new('RGB', (WIDTH, HEIGHT), COLORS['bg']); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, WIDTH, 100), fill=COLORS['navy'])
    text(d, (30, 20), title, 32, 'paper', True)
    text(d, (32, 65), subtitle, 18, '#D6E4EE')
    return im, d


def card(draw, box, fill='paper'):
    draw.rounded_rectangle(box, radius=12, fill=COLORS[fill], outline=COLORS['line'], width=1)


def normalized_trace(raw):
    """Adapt only field naming, never alter computed currents or voltages."""
    keys = {
        't': ['t_s', 't'], 'hs': ['state_HS_on', 'hs'],
        'ls': ['state_LS_on', 'ls'], 'dead': ['state_deadtime', 'dead'],
        'sw': ['Vsw_V', 'sw'], 'vo': ['Vout_V', 'vo'], 'il': ['IL_A', 'il']
    }
    trace = {}
    for name, alternatives in keys.items():
        found = next((key for key in alternatives if key in raw), None)
        if found is None: raise KeyError(f'Missing teaching trace field: {alternatives}')
        trace[name] = np.asarray(raw[found], dtype=float)
    n = len(trace['t'])
    for key, values in trace.items():
        if values.ndim == 0: trace[key] = np.full(n, values)
        if len(trace[key]) != n or not np.isfinite(trace[key]).all(): raise ValueError(key)
    if np.any(np.diff(trace['t']) < 0): raise ValueError('Times must be monotonic')
    if np.max(abs(trace['hs']+trace['ls']+trace['dead']-1)) > 1e-9: raise ValueError('State overlap or gap')
    if trace['il'].min() <= 0: raise ValueError('Animation explicitly assumes positive CCM current')
    return trace


def trace_at(trace, time, segment):
    # Restrict interpolation to the selected continuous state interval to avoid
    # interpolating ideal voltage jumps across duplicated event timestamps.
    key = ['hs', 'dead', 'ls', 'dead'][segment]
    mask = trace[key] > .5
    idx = np.where(mask)[0]
    if key == 'dead':
        split = np.where(np.diff(idx)>1)[0]
        parts = np.split(idx, split+1)
        idx = parts[0 if segment == 1 else -1]
    t = trace['t'][idx]
    return {k: float(np.interp(time, t, v[idx])) for k,v in trace.items()}


def plot_traces(draw, trace, time, selected=None):
    card(draw, (30, 530, 1130, 714))
    x0, x1 = 162, 1098; period = trace['t'][-1]-trace['t'][0]
    xt = x0 + (trace['t']-trace['t'][0])/period*(x1-x0)
    text(draw, (48, 540), 'REAL time axis', 15, 'muted', True)
    for label, values, lo, hi, top, bottom, color in [
        ('Gate commands', trace['hs'], 0, 1, 555, 576, 'blue'),
        ('VSW (V)', trace['sw'], -2, 105, 598, 622, 'blue'),
        ('iL (A)', trace['il'], .7, 1.3, 640, 679, 'current')]:
        text(draw, (48, top+1), label, 15, 'navy')
        line(draw, [(x0,bottom),(x1,bottom)], 'line', 1)
        ys = bottom-(values-lo)/(hi-lo)*(bottom-top)
        line(draw, list(zip(xt,ys)), color, 2)
        if label == 'Gate commands':
            ls_y = bottom-trace['ls']*(bottom-top)
            line(draw, list(zip(xt,ls_y)), 'diode', 2)
            text(draw, (950, 538), 'HS', 14, 'blue'); text(draw, (1003, 538), 'LS', 14, 'diode')
        if label == 'iL (A)':
            ymid = bottom-(1-lo)/(hi-lo)*(bottom-top)
            for x in range(x0, x1, 14): line(draw, [(x,ymid),(min(x+7,x1),ymid)], 'line', 1)
            text(draw, (1103, ymid-8), '1', 13, 'muted')
    if selected is not None:
        a,b = selected; xa=x0+a/period*(x1-x0); xb=x0+b/period*(x1-x0)
        draw.rectangle((xa,550,xb,684), outline=COLORS['diode'], width=2)
    xp = x0+time/period*(x1-x0)
    line(draw, [(xp,550),(xp,684)], 'red', 2)
    for us in range(5):
        xx=x0+us*1e-6/period*(x1-x0)
        text(draw, (xx,693), f'{us} us', 14, 'muted', anchor='mm')


def schematic(draw, state, values, arrow_phase):
    card(draw, (30, 174, 754, 515))
    active = 'diode' if state in (1,3) else 'current'
    # Source and the passive network always retain their circuit connections.
    line(draw, [(95,220),(300,220),(300,244)], 'current' if state==0 else 'wire', 4)
    line(draw, [(300,287),(300,315)], 'current' if state==0 else 'wire', 4)
    switch(draw,300,244,287,state==0,'QH')
    line(draw, [(300,315),(430,315)], active, 4)
    coils=coil_points();line(draw, coils, active, 4)
    line(draw, [(526,315),(680,315),(680,360)], active,4)
    res=resistor_points(680,360,425);line(draw,res,active,3)
    line(draw,[(680,425),(680,470)],active,4)
    line(draw,[(95,470),(680,470)],'wire',4)
    return_x=95 if state==0 else 300 if state==2 else 390
    line(draw,[(return_x,470),(680,470)],active,4)
    line(draw,[(95,220),(95,322)],'current'if state==0 else'wire',4)
    line(draw,[(95,378),(95,470)],'current'if state==0 else'wire',4)
    draw.ellipse((67,322,123,378),fill=COLORS['paper'],outline=COLORS['current']if state==0 else COLORS['wire'],width=3)
    text(draw,(95,332),'+',18,'navy',True,anchor='mm');text(draw,(95,366),'-',20,'navy',anchor='mm')
    # Synchronous low-side channel, whose positive CCM current is source-to-drain.
    line(draw,[(300,315),(300,352)],'current'if state==2 else'wire',4)
    switch(draw,300,352,414,state==2,'QL')
    line(draw,[(300,414),(300,470)],'current'if state==2 else'wire',4)
    # Low-side body diode: anode at ground, cathode at SW.
    dc='diode'if state in(1,3)else'wire'
    line(draw,[(300,315),(390,315),(390,348)],dc,3)
    line(draw,[(390,377),(390,470)],dc,3)
    draw.polygon([(378,377),(402,377),(390,352)],fill=COLORS['paper'],outline=COLORS[dc],width=3)
    line(draw,[(377,348),(403,348)],dc,3)
    text(draw,(405,357),'Body',15,dc);text(draw,(405,375),'diode',15,dc)
    # Output capacitor branch; its current direction follows KCL, not gate state.
    line(draw,[(600,315),(600,377)],'wire',3)
    line(draw,[(581,377),(619,377)],'blue',4);line(draw,[(581,389),(619,389)],'blue',4)
    line(draw,[(600,389),(600,470)],'wire',3)
    ic=values['il']-1.
    if abs(ic)>1e-6:
        arrow(draw,(633,350 if ic>0 else 424),(633,424 if ic>0 else 350),'blue',3,8)
    text(draw,(556,401),'Cout',16,'blue');text(draw,(579,449),f'iC {ic:+.2f} A',15,'blue',anchor='mm')
    for x,y in [(95,220),(300,315),(390,315),(600,315),(680,315),(300,470),(390,470),(600,470)]:
        draw.ellipse((x-4,y-4,x+4,y+4),fill=COLORS['navy'])
    text(draw,(70,190),'Vin = 100 V',18,'navy',True)
    text(draw,(630,190),'Vout = 12 V',18,'navy',True,anchor='mm')
    text(draw,(480,272),'L = 100 uH',18,'navy',True,anchor='mm')
    text(draw,(682,435),'1 A load',15,'navy',anchor='mm')
    text(draw,(302,322),'SW',16,'blue',True)
    text(draw,(95,492),'GND = 0 V',15,'muted',anchor='mm')
    text(draw,(470,492),'Low-side body diode shown; high-side diode omitted',14,'muted',anchor='mm')
    common=[(300,315),(430,315)]+coils+[(526,315),(680,315),(680,360)]+res+[(680,425),(680,470)]
    if state==0:
        path=[(95,220),(300,220),(300,315)]+common[1:]+[(95,470),(95,220)]
    elif state==2:
        path=[(300,470),(300,315)]+common[1:]+[(300,470)]
    else:
        path=[(390,470),(390,315),(300,315)]+common[1:]+[(390,470)]
    moving_arrows(draw,path,arrow_phase,active,count=11)


PHASES=[
    ('1  HIGH-SIDE ON', 'QH connects Vin to the inductor.', 'Positive inductor voltage raises current and magnetic energy.'),
    ('2  DEAD TIME', 'Both gate commands are OFF.', 'Current cannot stop instantly. The low-side diode carries it; SW falls below ground.'),
    ('3  LOW-SIDE ON', 'QL provides the freewheel path.', 'Current flows upward through QL. Inductor energy continues to supply the load.'),
    ('4  DEAD TIME', 'QL turns OFF before QH turns ON.', 'The diode carries current again. This gap prevents commanded shoot-through.')
]


def frame(trace, phase, time, step, interval):
    values=trace_at(trace,time,phase)
    im,d=base_image('A buck converter: follow current, then energy',
        '100 V to 12 V  |  1 A load  |  250 kHz  |  P02 idealized positive-CCM teaching trace')
    band='lightamber'if phase in(1,3)else'lightteal';ink='diode'if phase in(1,3)else'current'
    d.rounded_rectangle((30,110,1130,158),radius=8,fill=COLORS[band])
    text(d,(48,119),PHASES[phase][0],24,ink,True)
    duration=(interval[1]-interval[0])*1e9
    text(d,(1110,134),f'Actual phase: {duration:.1f} ns',18,'muted',anchor='rm')
    schematic(d,phase,values,step*.017)
    card(d,(774,174,1130,515))
    y=wrapped(d,(793,189),PHASES[phase][1],314,20,ink)
    rows=[('Switch node VSW',f"{values['sw']:.2f} V"),('Inductor current iL',f"{values['il']:.3f} A"),
          ('VGS,H / VGS,L','10 V / 0 V'if phase==0 else'0 V / 10 V'if phase==2 else'0 V / 0 V'),
          ('Stored inductor energy',f"{.5*100e-6*values['il']**2*1e6:.1f} uJ")]
    y=max(y+8,245)
    for label,value in rows:
        text(d,(793,y),label,16,'muted');text(d,(1110,y),value,18,'navy',True,anchor='ra');y+=31
    y=wrapped(d,(793,378),PHASES[phase][2],314,17,'navy',5)
    note=('Floating driver: VG,H is about 110 V while VGS,H is only 10 V.'if phase==0 else
          'Low SW allows bootstrap recharge. P03 models whether the recharge is sufficient.')
    wrapped(d,(793,max(y+9,452)),note,314,15,'blue',4)
    plot_traces(d,trace,time,interval)
    text(d,(32,733),'Time is stretched by phase. Arrows show conventional current; arrow speed is not to scale.',16,'muted')
    text(d,(32,758),'Assumed 0/10 V gates. Fixed 12 V output approximation; capacitor voltage ripple is not solved here.',15,'muted')
    return im


def intro_frame():
    im,d=base_image('A buck converter: three ideas to keep', 'A first lesson in 40-150 V DC/DC conversion')
    y=136
    for n,title,body in [
        ('1','Switches choose the current path.','High-side ON connects the input. Low-side ON provides a low-resistance return path.'),
        ('2','The inductor smooths current.','vL = L diL/dt. Current stays continuous when the switching path changes.'),
        ('3','The capacitor smooths voltage.','iC = iL - Iload. It charges only when iL exceeds the load current, in either switch state.')]:
        card(d,(40,y,1120,y+142));text(d,(65,y+22),n,32,'current',True)
        text(d,(126,y+23),title,28,'navy',True);wrapped(d,(126,y+70),body,940,22,'muted',7);y+=165
    text(d,(55,670),'Next: watch one 4 us cycle slowed down, including two short dead-time intervals.',22,'navy',True)
    text(d,(55,727),'Green = conducting path   Amber = body-diode path   Blue = voltage / capacitor current',18,'muted')
    return im


def comparison_frame():
    im,d=base_image('Why a higher input voltage is harder', 'The 12 V output does not reveal every internal voltage stress')
    card(d,(40,127,1120,429))
    headings=['Input','Ideal duty D = 12/Vin','ON time at 250 kHz','Off-state switch stress']
    xs=[65,248,570,837]
    for x,h in zip(xs,headings):wrapped(d,(x,148),h,255 if x<800 else 250,18,'muted')
    for row,vin in enumerate([40,100,150]):
        y=220+66*row
        for x,value in zip(xs,[f'{vin} V',f'{12/vin*100:.0f}%',f'{12/vin/250e3*1e9:.0f} ns',f'About {vin} V + ringing']):
            text(d,(x,y),value,24,'navy',True)
    text(d,(65,400),'Ideal estimates above ignore diode drops, resistance and timing delays.',16,'muted')
    y=460
    for title,body in [
        ('Shorter pulses make delays matter.','Gate charge, driver delay and dead time take a larger share of the ON interval.'),
        ('VGS and VDS are different limits.','A floating driver can move far above ground while keeping local VGS near 10 V.'),
        ('A voltage class is not a safe operating guarantee.','Check overshoot, isolation, SOA, temperature and real device models before hardware.')]:
        text(d,(58,y),title,22,'current',True);wrapped(d,(58,y+31),body,1040,19,'navy',6);y+=87
    text(d,(58,748),'Explore P01-P09 for gate drive, diode recovery, bootstrap, sensing, protection, losses and control.',16,'muted')
    return im


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trace',type=Path,default=ROOT/'results/teaching_buck_100V_25C.json');ap.add_argument('--out',type=Path,default=HERE);ap.add_argument('--inspection-dir',type=Path)
    args=ap.parse_args();raw=json.loads(args.trace.read_text(encoding='utf-8'));trace=normalized_trace(raw)
    args.out.mkdir(parents=True,exist_ok=True)
    keys=np.where(trace['hs']>.5,0,np.where(trace['ls']>.5,2,1))
    intervals=[]
    for state in [0,1,2,3]:
        k=['hs','dead','ls','dead'][state];ids=np.where(trace[k]>.5)[0]
        if k=='dead':ids=np.split(ids,np.where(np.diff(ids)>1)[0]+1)[0 if state==1 else-1]
        intervals.append((float(trace['t'][ids[0]]),float(trace['t'][ids[-1]])))
    frames=[intro_frame()];durations=[1800]
    examples={}
    for phase,(count,duration)in enumerate([(26,140),(16,110),(38,140),(16,110)]):
        a,b=intervals[phase]
        for step,f in enumerate(np.linspace(.015,.985,count)):
            rendered=frame(trace,phase,a+(b-a)*f,step,(a,b));frames.append(rendered);durations.append(duration)
            if step==count//2:examples[f'phase_{phase+1}']=rendered
    frames.append(comparison_frame());durations.append(4000)
    # One common palette avoids per-frame color flicker; all phase colors are included.
    pal=[]
    for value in [COLORS[k]for k in ['navy','muted','current','diode','blue','red','wire','line']]:
        rgb=tuple(int(value[j:j+2],16)for j in [1,3,5])
        for f in np.linspace(0,1,30):pal.extend(round(c+(255-c)*f)for c in rgb)
    for value in COLORS.values():pal.extend(int(value[j:j+2],16)for j in [1,3,5])
    pal=(pal+[255]*768)[:768];palette=Image.new('P',(1,1));palette.putpalette(pal)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE)for im in frames]
    gif=args.out/'buck_energy_flow.gif'
    indexed[0].save(gif,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True,disposal=1)
    examples['phase_1'].save(args.out/'buck_energy_flow_poster.png')
    if args.inspection_dir:
        inspection=args.inspection_dir;inspection.mkdir(parents=True,exist_ok=True)
        for name,im in examples.items():im.save(inspection/(name+'.png'))
        frames[0].save(inspection/'intro.png');frames[-1].save(inspection/'comparison.png')
    with Image.open(gif)as im:
        actual_durations=[]
        for j in range(im.n_frames):im.seek(j);actual_durations.append(im.info.get('duration',0))
        report={'date':'2026-11-03','gif':gif.name,'width':im.width,'height':im.height,'frames':im.n_frames,'duration_ms':sum(actual_durations),'loop':im.info.get('loop'),'bytes':gif.stat().st_size,'sha256':hashlib.sha256(gif.read_bytes()).hexdigest(),'annotation_language':'English only','data_source':args.trace.relative_to(ROOT.parent).as_posix(),'data_sha256':hashlib.sha256(args.trace.read_bytes()).hexdigest(),'physical_cycle_s':float(trace['t'][-1]-trace['t'][0]),'phase_intervals_s':intervals,'min_IL_A':float(trace['il'].min()),'max_IL_A':float(trace['il'].max()),'min_VSW_V':float(trace['sw'].min()),'max_VSW_V':float(trace['sw'].max()),'gate_command_annotation_assumption_V':[0,10],'interpolation':'Within each exported continuous-state interval; discontinuous voltages are not interpolated across state boundaries.','timing':'Different phases deliberately stretched for visibility; plot horizontal axis is physical time.','limitation':'Piecewise-linear positive-CCM teaching trace with assumed parameters and fixed output voltage. Capacitor current follows KCL but output voltage ripple is not solved. Motion is not an electron-velocity, field or transistor-level animation.'}
    assert report['frames']>=80 and 15000<=report['duration_ms']<=25000
    assert report['bytes']<8_000_000
    assert all(c.isascii()for c in PHASES[0][0])
    (args.out/'gif_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
