"""Build the combined offline V3.2 viewer from preserved V3 and new DC/DC data."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
old=load('v3/results/simulation_v3.json');new=load('v32/results/simulation_v32.json')
oldcheck=load('v32/validation/baseline_rerun.json');newcheck=load('v32/results/validation.json')
sources=load('v3/research/key_sources.json')+load('v32/research/sources.json')
geometry=load('v3/models/geometry.json')
def box(name,center,size,color,terminal=None,signal=None):
    return dict(name=name,center=center,size=size,color=color,terminal=terminal,signal=signal)
parts={
 'P01':['Gate driver / 栅驱','Gate charge / 栅电荷','Miller coupling / 米勒耦合','Power switch / 功率开关'],
 'P02':['High-side switch / 高侧','Body diode / 体二极管','Low-side switch / 低侧','Inductor path / 电感回路'],
 'P03':['Bootstrap diode / 自举二极管','Cboot / 自举电容','Floating supply / 浮动供电','UVLO / 欠压锁定'],
 'P04':['Common-mode edge / 共模边沿','Coupling C / 耦合电容','Receiver R-C / 接收端RC','Threshold / 阈值'],
 'P05':['Sense resistor / 检测电阻','Amplifier / 放大器','Filter / 滤波器','Comparator / 比较器'],
 'P06':['Startup source / 启动源','Supply capacitor / 供电电容','Hysteresis / 回差','Enable / 使能'],
 'P07':['Parasitic L / 寄生电感','Switch-node C / 开关电容','Series damping R / 串联阻尼电阻','Energy loss / 能量耗散'],
 'P08':['Conduction / 导通','Switching / 开关','Driver + recovery / 驱动与恢复','Thermal path / 热路径'],
 'P09':['Error amplifier / 误差放大','PWM average / PWM平均','Power stage / 功率级','Current limit / 限流']}
out=HERE/'obj';out.mkdir(exist_ok=True)
faces=[[0,1,3,2],[4,6,7,5],[0,4,5,1],[2,3,7,6],[0,2,6,4],[1,5,7,3]]
representatives={}
for m in new['models']:
    candidates=[c for c in new['cases']if c['model_id']==m['id']]
    c=next((c for c in candidates if c.get('temp_C')==25 and c.get('vin_V')==100),next((c for c in candidates if c.get('temp_C')==25),candidates[0]))
    if m['id']=='P07': c=next(c for c in candidates if c['id']=='P07_100V_damped')
    representatives[m['id']]=c['id']
    boxes=[box('Functional concept / 功能概念',[0,-.5,0],[6,.3,3.5],'#7b8fa6')]
    for j,label in enumerate(parts[m['id']]):boxes.append(box(label,[-1.7+(j%2)*2.4,.12,-.7+(j//2)*1.6],[1.6,.7,1.1],['#4f8fbc','#c8ad71','#8e90b7','#799e95'][j]))
    for j,t in enumerate(c['terminals'][:5]):boxes.append(box(t['name'],[-2.6+j*1.3,.65,-1.4],[.55,.3,.4],'#c8ad71',terminal=t['name']))
    geometry[m['id']]=boxes
    lines=['# Dimensionless functional blocks; not process geometry, layout or electric fields.'];base=1
    for j,b in enumerate(boxes):
        lines.append(f'o {m["id"]}_part_{j}')
        for x in [-.5,.5]:
            for y in [-.5,.5]:
                for z in [-.5,.5]:lines.append('v '+' '.join(str(v+[x,y,z][k]*b['size'][k])for k,v in enumerate(b['center'])))
        for f in faces:lines.append('f '+' '.join(str(base+i)for i in f))
        base+=8
    (out/(m['id']+'.obj')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
(HERE/'geometry.json').write_text(json.dumps({m['id']:geometry[m['id']]for m in new['models']},ensure_ascii=False),encoding='utf-8')
(HERE/'representatives.json').write_text(json.dumps(representatives,indent=2),encoding='utf-8')
checks=dict(tests_run=oldcheck['tests_run']+newcheck['tests_run'],passed=oldcheck['passed']and newcheck['passed'],tests=oldcheck['tests']+newcheck['tests'])
d=dict(old,version='3.2.0',date='2026-11-03',models=new['models']+old['models'],cases=new['cases']+old['cases'],geometry=geometry,sources=sources,people=load('v3/research/people200.json'),papers=load('v3/research/papers.json'),validation=checks)
summary={'release':'3.2.0','date':'2026-11-03','baseline_models':len(old['models']),'baseline_cases':len(old['cases']),'new_models':len(new['models']),'new_cases':len(new['cases']),'total_model_views':len(d['models']),'total_cases':len(d['cases']),'total_plots':sum(len(c['plots'])for c in d['cases']),'tests_run':checks['tests_run'],'new_tests':newcheck['tests_run'],'tests_passed':checks['passed'],'baseline_cohort_people':200,'baseline_cohort_papers':182,'cohort_checked_date':'2026-11-02','new_source_records':len(sources)-len(load('v3/research/key_sources.json')),'note':'New DC/DC sources supplement the unchanged V3.1 cohort. Models are illustrative, not paper or PDK reproductions.'}
(HERE/'release_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
template=(HERE/'viewer_template.html').read_text(encoding='utf-8')
template=template.replace('__TOTAL_MODELS__',str(summary['total_model_views'])).replace('__NEW_CASES__',str(summary['new_cases'])).replace('__TOTAL_CASES__',str(summary['total_cases']))
template=template.replace('__NEW_METRIC_ZH__',json.dumps(load('v32/models/metric_labels_zh.json'),ensure_ascii=False))
template=template.replace('__DATA__',json.dumps(d,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('</','<\\/'))
(ROOT/'index.html').write_text(template,encoding='utf-8')
print(json.dumps(summary,indent=2))
