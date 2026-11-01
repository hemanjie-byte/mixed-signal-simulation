import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'models/viewer_template.html').read_text(encoding='utf-8')
for key,path in [('DATA','results/simulation_v2.json'),('GEOMETRY','models/geometry.json'),('PAPERS','research/papers.json'),('PEOPLE','research/top100_screening.json')]:
    s=s.replace('__'+key+'__',json.dumps(json.loads((ROOT/path).read_text(encoding='utf-8')),ensure_ascii=False,separators=(',',':')).replace('</',r'<\/'))
(ROOT.parent/'index.html').write_text(s,encoding='utf-8')
print('Built offline index.html')
