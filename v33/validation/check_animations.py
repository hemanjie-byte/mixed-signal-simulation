"""Validate published GIF bytes against their recorded simulation sources."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/'v33/education/manifest.json').read_text(encoding='utf8'))
expected={'A01','A02','A03','A04','B01','B02','B03','B04','B05','B06','B07',*[f'P{i:02d}'for i in range(1,10)]}
assert set(manifest)==expected
sources={};records=[]
for mid,row in manifest.items():
    source=ROOT/row['source'];assert row['source'].startswith('v33/numerics/')
    if row['source']not in sources:sources[row['source']]=(hashlib.sha256(source.read_bytes()).hexdigest(),json.loads(source.read_text(encoding='utf8')))
    digest,data=sources[row['source']];assert digest==row['source_sha256'],mid+' source changed'
    case=next(c for c in data['cases']if c['id']==row['case_id']);assert case['model_id']==mid
    gif=ROOT/row['gif'];poster=ROOT/row['poster']
    assert hashlib.sha256(gif.read_bytes()).hexdigest()==row['gif_sha256']
    assert hashlib.sha256(poster.read_bytes()).hexdigest()==row['poster_sha256']
    assert row['annotation_language']=='English only'
    with Image.open(gif)as im:
        assert im.n_frames==row['frames'] and im.size==(row['width'],row['height'])
        duration=0
        for k in range(im.n_frames):im.seek(k);im.load();duration+=im.info.get('duration',0)
        assert duration==row['duration_ms']
    with Image.open(poster)as im:im.verify()
    assert all(0<=i<len(case['x'])for i in row['sampled_indices'])
    records.append(dict(model_id=mid,case_id=row['case_id'],gif_bytes=gif.stat().st_size,frames=row['frames'],duration_ms=duration,source_hash_matches=True))
result=dict(date='2026-11-03',models=20,gifs=20,passed=True,total_gif_bytes=sum(r['gif_bytes']for r in records),records=records,note='Language metadata plus source render strings were reviewed; image decoding alone is not OCR or scientific validation.')
(ROOT/'v33/validation/animation_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in result.items()if k!='records'},indent=2))
