from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
d=load('results/simulation_v3.json')
d.update(geometry=load('models/geometry.json'),people=load('research/people200.json'),papers=load('research/papers.json'),sources=load('research/key_sources.json'),validation=load('results/validation.json'))
data=json.dumps(d,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('</','<\\/')
template=(ROOT/'models/viewer_template.html').read_text(encoding='utf-8')
(ROOT.parent/'index.html').write_text(template.replace('__DATA__',data),encoding='utf-8')
print('Built standalone English-first / Chinese viewer')
