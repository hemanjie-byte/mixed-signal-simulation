"""Check complete source-ID coverage and the distributed teaching artifacts."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys

H=Path(__file__).resolve().parents[1];R=H.parent
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    rows=read(H/'catalogue.json');manifest=read(H/'generated_manifest.json');items=manifest['records']
    expected={'V1_'+x['id'] for x in read(R/'可复现计算/data.json')['devices']}
    expected|={'V2_'+x['id'] for x in read(R/'v2/models/model_catalog.json')}
    for path in ['v33/numerics/analog/models/model_catalog.json','v33/numerics/dcdc/model_catalog.json']:
        expected|={'V33_'+x['id'] for x in read(R/path)}
    ids=[x['print_id'] for x in rows];assert len(ids)==len(set(ids))==75
    assert set(ids)==expected=={x['print_id'] for x in items}
    assert {p.stem for p in (H/'stl').glob('*.stl')}==expected
    assert {p.stem for p in (H/'heightfields').glob('*.npy')}==expected
    for row in rows:
        assert (R/row['source_catalogue']).is_file()
        for k in ['name_en','name_zh','limits_en','limits_zh']:assert row[k].strip()
        for path in [H/'stl'/f"{row['print_id']}.stl",H/'heightfields'/f"{row['print_id']}.npy",H/'previews'/f"{row['print_id']}.png",H/'cards'/f"{row['print_id']}.md"]:assert path.is_file(),path
    for item in items:
        report=item['geometry_report'];assert report['status']=='PASS'
        assert sha(H/item['stl'])==report['stl_sha256']
        assert sha(H/item['heightfield'])==report['heightfield_sha256']
        assert report['minimum_declared_main_feature_mm']>=1.2-1e-8
        assert report['minimum_declared_text_stroke_mm']>=0.8-1e-8
    preview=read(H/'preview_manifest.json');assert preview['catalogue_sha256']==sha(H/'catalogue.json')
    assert len(preview['previews'])==75 and len(preview['contact_sheets'])==6
    assert {p['print_id'] for p in preview['previews']}==expected
    for p in preview['previews']:
        assert sha(H/p['png'])==p['sha256']
        assert sha(H/p['top'])==p['top_sha256']
        assert sha(H/p['heightfield'])==p['heightfield_sha256']
    output={'status':'PASS','records':75,'source_id_coverage':'75/75','group_counts':dict(Counter(x.split('_')[0] for x in ids)),'kind_counts':dict(Counter(r['kind'] for r in rows)),'stl_npy_manifest_hashes':'PASS','per_record_cards_and_previews':'PASS','physical_print_tested':False}
    print(json.dumps(output,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:print(json.dumps({'status':'FAIL','error':str(exc)},ensure_ascii=False));sys.exit(1)
