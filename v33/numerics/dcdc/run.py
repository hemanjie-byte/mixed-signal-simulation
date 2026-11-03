"""Portable entry point: python v33/numerics/dcdc/run.py (NumPy only).

Imports preserved V3.2 equations without changing any V3.2 file, generates
the 153 cases, compares numerical errors, and executes validation.
"""
from pathlib import Path
import sys,json,hashlib,platform,subprocess,argparse
import numpy as np
import export
from improved import REPO

HERE=Path(__file__).resolve().parent
METHODS={
 'P01':('Stage-wise 32-point Gauss quadrature for overlap energies; display samples unchanged.','交叠能量按阶段采用32点Gauss积分；显示采样不变。'),
 'P02':('Retained exact periodic piecewise-linear CCM solution; numerical-floor audit.','保留精确周期分段线性CCM解；审核浮点误差底限。'),
 'P03':('Retained exact exponential recharge and affine periodic map; numerical-floor audit.','保留精确指数充电及仿射周期映射；审核浮点误差底限。'),
 'P04':('Retained analytical RC ramp response and event boundary; numerical-floor audit.','保留解析RC斜坡响应及事件边界；审核浮点误差底限。'),
 'P05':('Analytical comparator event times inserted as left/right waveform samples; no changed propagation delay.','解析比较器事件时刻插入左右极限波形样本；传播延迟不变。'),
 'P06':('Exact event-aligned constant-current segments, checked against original compliance; 2us display grid with all events retained.','精确事件对齐恒流分段，检查原顺从电压条件；2µs显示网格并保留全部事件。'),
 'P07':('Simpson energy integration on a 4x finer internal grid; analytical display waveform unchanged.','在加密4倍内部网格上用Simpson进行能量积分；解析显示波形不变。'),
 'P08':('Improved P01 quadrature, exact piecewise-linear squared-current moments, tighter thermal fixed point; same nine loss terms.','改进P01积分、分段线性电流的精确均方矩及更紧热不动点容差；仍为相同九项损耗。'),
 'P09':('0.5us RK4 with continuous ramp evaluated at intermediate stages; events align with steps; RK4 energy quadrature; 10us saved grid.','0.5µs RK4并在中间子步计算连续斜坡；事件与步长对齐；RK4能量积分；10µs保存网格。')}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--reuse-audit',action='store_true',help='Reuse an existing audit only when equations are unchanged.');args=parser.parse_args()
    preserved=[REPO/'v32/models/dcdc_models.py',REPO/'v32/models/run_simulations.py',REPO/'v32/results/simulation_v32.json']
    before={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in preserved}
    export.main()
    data=json.loads((HERE/'simulation.json').read_text(encoding='utf-8'))
    for model in data['models']:
        en,zh=METHODS[model['id']];model.update(numerical_method_en=en,numerical_method_zh=zh)
        model['limits_en']+=' Numerical refinement reduces selected discretization errors, not unknown physical modeling error.'
        model['limits_zh']+=' 数值改进降低指定离散误差，不代表未知物理建模误差降低。'
        if model['id']=='P09':model['parameters'].update(dt_s=.5e-6,saved_stride_steps=20)
    for case in data['cases']:
        en,zh=METHODS[case['model_id']]
        case['notes_en']=(case.get('notes_en','')+' '+en).strip();case['notes_zh']=zh
    data['conventions']['accuracy']='Numerical-error audit only; no PDK/silicon-calibrated physical accuracy claim.'
    (HERE/'simulation.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf-8')
    (HERE/'model_catalog.json').write_text(json.dumps(data['models'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    labels=json.loads((REPO/'v32/models/metric_labels_zh.json').read_text(encoding='utf-8'))
    labels.update(sampled_trip_time_s='导出波形比较器跳变时刻 s',sampled_trip_timing_error_s='导出波形跳变时刻误差 s',integrated_damping_energy_J='内部加密积分阻尼耗散能量 J')
    (HERE/'metric_labels_zh.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not args.reuse_audit:
        import audit
        audit.main()
    elif not(HERE/'accuracy_audit.json').exists():raise FileNotFoundError('No audit to reuse')
    after={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in preserved}
    if before!=after:raise RuntimeError('Preserved baseline changed during run')
    manifest=dict(python=platform.python_version(),numpy=np.__version__,baseline_sha256=after,baseline_unchanged=True,
                  equations='V3.2 retained',models=9,cases=153)
    (HERE/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return subprocess.call([sys.executable,'-X','utf8',str(HERE/'tests/run_validation.py')],cwd=REPO)

if __name__=='__main__':sys.exit(main())
