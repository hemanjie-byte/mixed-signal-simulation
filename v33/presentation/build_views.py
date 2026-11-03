"""Combine improved numerical data with the complete model-animation gallery."""
from pathlib import Path
import json,csv,collections,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf8'))
analog=load('v33/numerics/analog/simulation.json');power=load('v33/numerics/dcdc/simulation.json')
models=power['models']+analog['models'];cases=power['cases']+analog['cases']
gallery=load('v33/education/manifest.json')
if 'models'in gallery:gallery=gallery['models']
if isinstance(gallery,list):gallery={g['model_id']:g for g in gallery}
assert set(gallery)=={m['id']for m in models}
def resource(p):
    if p.startswith('v33/'):return p
    return 'v33/education/'+p
for mid,g in gallery.items():
    for key in ['gif','poster']:g[key]=resource(g[key]);assert(ROOT/g[key]).exists()
    assert any(c['id']==g['case_id'] and c['model_id']==mid for c in cases)
    assert g['source'].startswith('v33/numerics/'), 'GIF must use improved data: '+mid
    assert hashlib.sha256((ROOT/g['source']).read_bytes()).hexdigest()==g['source_sha256']
    assert hashlib.sha256((ROOT/g['gif']).read_bytes()).hexdigest()==g['gif_sha256']
rows=[]
for family in ['analog','dcdc']:
    a=load(f'v33/numerics/{family}/accuracy_audit.json')
    rows+=a if isinstance(a,list)else a['rows']
assert len(rows)==20 and {r['model_id']for r in rows}==set(gallery)
rows=sorted(rows,key=lambda r:r['model_id'])
for r in rows:
    r['source_status']=r['status']
    r['status']={'verified_numerical_improvement':'target_met','not_applicable_roundoff_floor':'numerical_floor'}.get(r['status'],r['status'])
    if r['status']=='target_met':
        assert r['old_error']>0 and r['new_error']>=0
        improvement=100*(r['old_error']-r['new_error'])/r['old_error']
        assert improvement>=10 and abs(improvement-r['improvement_pct'])<1e-7
counts=dict(collections.Counter(r['status']for r in rows))
aud=dict(date='2026-11-03',comparison='V3.2.0 to V3.3.0',relative_error_reduction_target_pct=10,physical_accuracy_improvement_verified=False,rows=rows,status_counts=counts,definition_en='100*(old benchmark error-new benchmark error)/old benchmark error on each stated benchmark. This is not a ten-percentage-point increase in physical accuracy.',definition_zh='对每项注明的基准，计算100×(旧基准误差−新基准误差)/旧基准误差；并非物理准确率增加10个百分点。')
(HERE/'accuracy_audit.json').write_text(json.dumps(aud,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
with(HERE/'accuracy_audit.csv').open('w',newline='',encoding='utf-8-sig')as f:
    keys=['model_id','metric_en','metric_zh','unit','old_error','new_error','improvement_pct','status','reference_en','reference_zh','limits_en','limits_zh']
    w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
checks=[load('v33/validation/legacy_checks.json')]+[load(f'v33/numerics/{f}/validation.json')for f in ['analog','dcdc']]
validation=dict(tests_run=sum(c['tests_run']for c in checks),passed=all(c['passed']for c in checks),tests=[t for c in checks for t in c['tests']],python=checks[0]['python'],numpy=checks[0]['numpy'])
geometry=load('v3/models/geometry.json')|load('v32/presentation/geometry.json')
sources=load('v3/research/key_sources.json')+load('v32/research/sources.json')
labels=load('v32/models/metric_labels_zh.json')
for f in ['analog','dcdc']:
    p=ROOT/f'v33/numerics/{f}/metric_labels_zh.json'
    if p.exists():labels.update(json.loads(p.read_text(encoding='utf8')))
d=dict(version='3.3.0',date='2026-11-03',models=models,cases=cases,geometry=geometry,sources=sources,people=load('v3/research/people200.json'),papers=load('v3/research/papers.json'),validation=validation,accuracy=aud,gallery=gallery)
summary=dict(version='3.3.0',date='2026-11-03',model_views=len(models),cases=len(cases),plots=sum(len(c['plots'])for c in cases),model_gifs=len(gallery),tests_run=validation['tests_run'],tests_passed=validation['passed'],numerical_target_met=counts.get('target_met',0),status_counts=counts,physical_accuracy_improvement_verified=False)
(HERE/'release_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
(HERE/'representatives.json').write_text(json.dumps({k:v['case_id']for k,v in gallery.items()},indent=2)+'\n',encoding='utf8')
(HERE/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf8')
(HERE/'metric_labels_zh.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'gallery.json').write_text(json.dumps(gallery,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
template=(HERE/'viewer_template.html').read_text(encoding='utf8')
template=template.replace('__NEW_METRIC_ZH__',json.dumps(labels,ensure_ascii=False)).replace('__DATA__',json.dumps(d,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('</','<\\/'))
(ROOT/'index.html').write_text(template,encoding='utf8')
print(json.dumps(summary,indent=2))
