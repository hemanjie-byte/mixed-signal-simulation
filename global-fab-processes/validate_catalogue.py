"""Validate structure, generated coverage and local links; not device qualification."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import hashlib,json,re

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
rows=json.loads((HERE/'data/processes.json').read_text(encoding='utf8'))
coverage=json.loads((HERE/'coverage.json').read_text(encoding='utf8'))
assert len({r['id']for r in rows})==len(rows)
assert coverage['records']==len(rows)
assert coverage['process_records']==sum(r['record_type_en']=='Process / platform'for r in rows)
assert coverage['manufacturers']==len({r['company_en']for r in rows})
expected_pages={re.sub(r'[^a-z0-9]+','-',r['company_en'].lower()).strip('-')+'.md'for r in rows}
assert {p.name for p in (HERE/'companies').glob('*.md')}==expected_pages,'Stale or missing company page'
missing=[]
for r in rows:
    for k in ['company','region','business_type','platform','node','wafer','voltage','voltage_kind','devices','application','dcdc_relevance','availability','limitations','reading_depth']:
        for lang in ['en','zh']:
            value=r[k+'_'+lang]
            assert value is None or (isinstance(value,str) and value.strip()),(r['id'],k,lang)
    assert urlparse(r['source_url']).scheme=='https' and urlparse(r['source_url']).netloc
    assert r['source_title'] and r['checked_date']=='2026-11-06'
for p in [ROOT/'README.md',ROOT/'V3-3/README.md',*(HERE.rglob('*.md'))]:
    for dest in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
        dest=unquote(dest.split('#')[0])
        if not dest or urlparse(dest).scheme:continue
        if dest.endswith(('V3-3_20261106.zip','package_manifest.json')):continue
        if not (p.parent/dest).exists():missing.append([str(p.relative_to(ROOT)),dest])
assert not missing,missing
assert 'V3-3' in (ROOT/'V3-3/README.md').read_text(encoding='utf8')
assert 'global-fab-processes/index.html' in (ROOT/'index.html').read_text(encoding='utf8')
assert '<small>V3-3</small>' in (ROOT/'index.html').read_text(encoding='utf8')
result={'review_date':'2026-11-06','records':len(rows),'process_records':coverage['process_records'],'manufacturers':coverage['manufacturers'],'bilingual_schema_complete':True,'unknown_fields_retained_as_null':True,'unique_record_ids':True,'local_markdown_links_missing':missing,'sharing_display_version':'V3-3','catalogue_sha256':hashlib.sha256((HERE/'data/processes.json').read_bytes()).hexdigest(),'scope':'Structural and local-link checks. Source-reading depth is per record; no PDK qualification or automatic external-link availability guarantee.'}
print(json.dumps(result,indent=2))
