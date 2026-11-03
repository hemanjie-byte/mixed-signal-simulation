"""Auditable before/after errors; numerical precision is not physical accuracy."""
from pathlib import Path
import json,csv
import numpy as np
import improved as new
from improved import baseline as old,VINS,TEMPS
from reference import gate_overlap_closed,loss_reference,buck_reference

HERE=Path(__file__).resolve().parent

def build_audit():
    rows=[];details=[]
    common_en='Same authored coefficients and reduced physics as V3.2; no PDK, silicon data or measured physical-accuracy claim.'
    common_zh='沿用V3.2人为系数与简化物理；无PDK、硅数据或实测物理准确度声明。'
    def add(mid,metric,metriczh,unit,values,reference,referencezh,floor,limits='',limitszh='',uncertainty=0.):
        before=max(v['old_error']for v in values);after=max(v['new_error']for v in values)
        if before<=floor:status='numerical_floor';gain=None
        else:
            gain=100*(before-after)/before;status='target_met'if gain>=10 else'target_not_met'
        gains=[100*(v['old_error']-v['new_error'])/v['old_error']for v in values if v['old_error']>floor]
        row=dict(model_id=mid,metric_en=metric,metric_zh=metriczh,unit=unit,old_error=before,new_error=after,
                 improvement_pct=gain,status=status,reference_en=reference,reference_zh=referencezh,
                 absolute_error_floor=floor,reference_uncertainty_estimate=uncertainty,case_count=len(values),
                 minimum_eligible_case_improvement_pct=min(gains)if gains else None,
                 aggregation_en='Maximum absolute error over all listed case/metric comparisons.',
                 aggregation_zh='所有列出工况及指标比较的最大绝对误差。',
                 limits_en=(limits+' '+common_en).strip(),limits_zh=(limitszh+' '+common_zh).strip())
        rows.append(row);details.extend(dict(model_id=mid,**v)for v in values)
    vals=[]
    for vin in VINS:
        for temp in TEMPS:
            a=old.gate_switch(vin,temp)['metrics'];b=new.gate_switch(vin,temp)['metrics'];ref=gate_overlap_closed(vin,temp)
            for key,r in zip(['channel_overlap_on_J','channel_overlap_off_J'],ref):
                vals.append(dict(case_id=f'P01_{vin}V_{temp}C',quantity=key,reference_value=r,old_value=a[key],new_value=b[key],old_error=abs(a[key]-r),new_error=abs(b[key]-r)))
    add('P01','On/off overlap-energy quadrature error','导通/关断交叠能量积分误差','J',vals,
        'Closed-form exponential current moments and nonlinear Miller charge/energy primitives; all 18 Vin/temperature cases, both edges.',
        '指数电流矩与非线性Miller电荷/能量原函数的闭式积分；18种电压/温度、两个边沿。',1e-18,
        'Display density is unchanged; improved metrics use stage-wise 32-point Gauss quadrature.','显示密度不变；改进指标按阶段使用32点Gauss积分。')
    vals=[]
    for vin in VINS:
        for temp in TEMPS:
            a=old.deadtime_buck(vin,temp)['metrics']['volt_second_residual_Vs'];b=new.deadtime_buck(vin,temp)['metrics']['volt_second_residual_Vs']
            vals.append(dict(case_id=f'P02_{vin}V_{temp}C',reference_value=0.,old_value=a,new_value=b,old_error=abs(a),new_error=abs(b)))
    add('P02','Periodic inductor volt-second balance residual','周期电感伏秒平衡残差','V s',vals,
        'Exact piecewise-constant voltage integral is zero by duty construction; all 18 cases.','占空比构造使分段常数电压积分精确为零；全部18工况。',1e-15,
        'Analytical trajectory already at floating-point floor; no meaningful 10% reduction claimed.','解析轨迹已达浮点误差底限，不宣称有意义的10%降低。')
    vals=[]
    for vin in VINS:
        for temp in TEMPS:
            for cap,label in [(100e-9,''),(3.3e-9,'_small_cap')]:
                a=old.bootstrap(vin,temp,cboot=cap)['metrics'];b=new.bootstrap(vin,temp,cboot=cap)['metrics'];r=a['steady_min_V']
                vals.append(dict(case_id=f'P03_{vin}V_{temp}C{label}',reference_value=r,old_value=a['last_cycle_min_V'],new_value=b['last_cycle_min_V'],old_error=abs(a['last_cycle_min_V']-r),new_error=abs(b['last_cycle_min_V']-r)))
    add('P03','Periodic bootstrap minimum-voltage residual','周期自举最低电压残差','V',vals,
        'Analytical affine cycle-map fixed point versus end-of-run minimum, including finite-cycle settling; all 36 cases.','解析仿射周期映射不动点与末周期最低值比较，包含有限周期建立残差；全部36工况。',1e-10,
        'Exact exponential updates already settle below the stated floor.','精确指数递推的建立残差已低于给定底限。')
    vals=[]
    for vin in VINS:
        for resistance,label in [(20000,'weak'),(500,'strong')]:
            ratio=vin/1e10/(resistance*230e-15);ref=30/230*vin*(-np.expm1(-ratio))/ratio
            a=old.level_shift(vin,receiver_r=resistance)['metrics']['peak_receiver_disturbance_V'];b=new.level_shift(vin,receiver_r=resistance)['metrics']['peak_receiver_disturbance_V']
            vals.append(dict(case_id=f'P04_{vin}V_25C_{label}',reference_value=ref,old_value=a,new_value=b,old_error=abs(a-ref),new_error=abs(b-ref)))
    add('P04','Analytical RC disturbance peak error','解析RC扰动峰值误差','V',vals,
        'Linear-RC ramp response evaluated with the stable expm1 expression; all 12 weak/strong-receiver cases.','采用数值稳定expm1表达式的线性RC斜坡响应；全部12种强/弱接收端工况。',1e-12,
        'The peak is analytic already; this does not validate real logic clamps or CMTI.','峰值已为解析值；这不验证实际逻辑钳位或CMTI。')
    vals=[]
    for temp in TEMPS:
        a=old.current_sense(temp);b=new.current_sense(temp);ref=a['metrics']['trip_time_s']
        at=float(a['t'][np.flatnonzero(a['trip'])[0]]);bt=float(b['t'][np.flatnonzero(b['trip'])[0]])
        vals.append(dict(case_id=f'P05_{temp}C',reference_value=ref,old_value=at,new_value=bt,old_error=abs(at-ref),new_error=abs(bt-ref)))
    add('P05','Exported comparator transition timing error','导出比较器跳变时刻误差','s',vals,
        'Closed-form one-pole threshold crossing plus the same 35ns assumed propagation delay; all three temperatures.','单极点阈值交越闭式解加相同35ns假定传播延迟；全部三个温度。',1e-15,
        'This improves sampled waveform event placement; the analytic trip_time_s metric was already exact.','改善采样波形的事件定位；原解析trip_time_s指标已精确。')
    vals=[]
    for vin in VINS:
        for temp in TEMPS:
            ref=9e-6/(.001*(1+.001*(temp-25))-40e-6)
            a=old.startup_uvlo(vin,temp)['metrics']['first_enable_s'];b=new.startup_uvlo(vin,temp)['metrics']['first_enable_s']
            vals.append(dict(case_id=f'P06_{vin}V_{temp}C',reference_value=ref,old_value=a,new_value=b,old_error=abs(a-ref),new_error=abs(b-ref)))
    add('P06','First UVLO-enable timing error','首次欠压锁定使能时刻误差','s',vals,
        'Capacitor ramp time Caux*9V/(Istart-Ioff), while original compliance remains inactive; all 18 cases.','原模型未进入顺从电压限制时，电容斜坡时间Caux×9V/(Istart−Ioff)；全部18工况。',1e-12,
        'Event-aligned segments are exact only in the explicitly checked constant-current domain.','仅在明确检查的恒流工作域内，事件对齐分段解是精确的。')
    vals=[]
    for vin in VINS:
        for label in ['weak','damped']:
            a=old.ringing(vin,label);b=new.ringing(vin,label);ref=float(a['energy'][0]-a['energy'][-1])
            av=ref+a['metrics']['energy_residual_J'];bv=b['metrics']['integrated_damping_energy_J']
            vals.append(dict(case_id=f'P07_{vin}V_{label}',reference_value=ref,old_value=av,new_value=bv,old_error=abs(av-ref),new_error=abs(bv-ref)))
    add('P07','Integrated damping-energy error','阻尼耗散能量积分误差','J',vals,
        'Initial minus final stored LC energy from the analytical free response; all 12 cases.','解析自由响应的初始与末时刻LC储能之差；全部12工况。',1e-18,
        'Energy uses Simpson quadrature on a 4x finer internal grid; saved waveform density and analytical physics are unchanged.','能量采用加密4倍内部网格上的Simpson积分；保存波形密度与解析物理不变。')
    vals=[]
    for vin in VINS:
        for temp in TEMPS:
            ref,hot=loss_reference(vin,temp);a=old.loss_budget(vin,temp)['metrics']['total_loss_W'];b=new.loss_budget(vin,temp)['metrics']['total_loss_W']
            vals.append(dict(case_id=f'P08_{vin}V_{temp}C',reference_value=ref,reference_hot_node_C=hot,old_value=a,new_value=b,old_error=abs(a-ref),new_error=abs(b-ref)))
    add('P08','Total loss numerical evaluation error','总损耗数值计算误差','W',vals,
        'Independent closed-form overlap, exact piecewise-linear RMS moments, same nine loss terms, and bracketed thermal-root bisection; all 18 cases.','独立闭式交叠能量、分段线性电流的精确均方矩、相同九项损耗及热根区间二分法；全部18工况。',1e-10,
        'No new physical loss term or altered Coss/Qrr accounting. The common thermal node is not a MOS junction.','未新增物理损耗或改变Coss/Qrr核算；共用热节点不是MOS结温。')
    vals=[];uncertainty=0.
    for vin in VINS:
        for temp in TEMPS:
            reference=buck_reference(vin,temp);tight=buck_reference(vin,temp,rtol=1e-11,atol=1e-13)
            bound=float(np.max(abs(reference['voltage']-tight['voltage'])));uncertainty=max(uncertainty,bound)
            a=old.controlled_buck(vin,temp);b=new.controlled_buck(vin,temp)
            av=np.interp(tight['t'],a['t'],a['voltage']);bv=np.interp(tight['t'],b['t'],b['voltage']);ref=tight['voltage']
            vals.append(dict(case_id=f'P09_{vin}V_{temp}C',old_error=float(np.max(abs(av-ref))),new_error=float(np.max(abs(bv-ref))),
                             reference_uncertainty=bound,reference_accepted_steps=tight['steps'],comparison_points=len(ref)))
    add('P09','Maximum output-voltage trajectory error','输出电压轨迹最大误差','V',vals,
        'Independent adaptive Dormand-Prince 5(4), tighter run rtol=1e-11/atol=1e-13, continuous ramp and aligned load event; common 10us times, all 18 cases.','独立自适应Dormand-Prince 5(4)，收紧至rtol=1e-11/atol=1e-13，连续斜坡与对齐负载事件；统一10µs时刻，全部18工况。',1e-7,
        'Reference uncertainty is the max difference from a 10x looser tolerance, an empirical convergence estimate, not a rigorous bound. New RK4 uses 0.5us steps and stage-time ramp evaluation; saved traces remain 10us.','参考不确定度为容差放宽10倍的最大差异，是经验收敛估计而非严格上界。新版RK4采用0.5µs步长并在子步时刻计算斜坡；保存间隔仍为10µs。',uncertainty)
    return dict(version='3.3.0',rows=rows,case_details=details,claim_en='Measured reduction of selected numerical errors only; physical accuracy is uncalibrated.',claim_zh='仅衡量指定数值误差的降低；物理准确度未经校准。')

def main():
    report=build_audit();(HERE/'accuracy_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    with (HERE/'accuracy_audit.csv').open('w',newline='',encoding='utf-8-sig')as f:
        w=csv.DictWriter(f,fieldnames=list(report['rows'][0]));w.writeheader();w.writerows(report['rows'])
    print(json.dumps([{k:r[k]for k in ['model_id','old_error','new_error','improvement_pct','status']}for r in report['rows']],indent=2))
    return report

if __name__=='__main__':main()
