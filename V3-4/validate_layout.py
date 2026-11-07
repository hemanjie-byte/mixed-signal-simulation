"""Verify V3-4 naming, references and preserved scientific/artifact bytes.

Run from the repository root: python V3-4/validate_layout.py
Use --extracted for the merged two-package delivery: archived snapshots omitted
from that distribution are reported separately, never counted as verified.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse,hashlib,json,re,sys

ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
    return h.hexdigest()
class Links(HTMLParser):
    def __init__(self):super().__init__();self.paths=[]
    def handle_starttag(self,tag,attrs):
        for key,val in attrs:
            if key in {'href','src'} and val:self.paths.append(val)

def validate(extracted=False):
    errors=[];count=0;omitted=[]
    for name in ['V3-2','V3.3','V3-4']:
        if not(ROOT/name).is_dir():errors.append('Missing directory: '+name)
    for name in ['v32','v33','V3-3']:
        if(ROOT/name).exists():errors.append('Old active directory remains: '+name)
    data=json.loads((ROOT/'V3-4/current-release.json').read_text(encoding='utf8'))
    if(data['display_version'],data['simulation_version'],data['catalogue_version'],data['printing_version'])!=('V3-4','v3.3.0','2.0','1.0'):errors.append('Edition metadata mismatch')
    preserved=json.loads((ROOT/'V3-4/preservation_manifest.json').read_text(encoding='utf8'))
    fab_meta=json.loads((ROOT/'global-fab-processes/catalogue.json').read_text(encoding='utf8'))
    if fab_meta.pop('sharing_version')!='V3-4' or fab_meta!=preserved['fab_metadata_excluding_sharing_version']:errors.append('FAB metadata changed beyond sharing edition')
    for row in preserved['files']:
        p=ROOT/row['path']
        if not p.is_file() and extracted and (row['historical_snapshot'] or row['path'].startswith(('v2/','可复现计算/','3D模型_OBJ/'))):
            omitted.append(row['path']);continue
        if not p.is_file() or sha(p)!=row['sha256']:errors.append('Preservation mismatch: '+row['path'])
        else:count+=1
    docs=[ROOT/'README.md',ROOT/'PACKAGE_README_EN_ZH.md',ROOT/'V3-4/README.md',ROOT/'V3-4/VERSION_COMPARISON.md',ROOT/'V3-2/README.md',ROOT/'V3.3/README.md']
    link_count=0
    for p in docs+[ROOT/'index.html',ROOT/'V3-4/index.html',ROOT/'printable-models/index.html']:
        text=p.read_text(encoding='utf8')
        if p.suffix=='.html':
            parser=Links();parser.feed(text);targets=parser.paths
        else:targets=re.findall(r'\]\(([^\s)]+)\)',text)
        for target in targets:
            parsed=urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            path=unquote(parsed.path)
            if '${' in path:continue
            candidate=(p.parent/path).resolve()
            if not candidate.is_relative_to(ROOT):errors.append('Path escapes root: '+target)
            elif not candidate.exists():
                if extracted and candidate.suffix=='.zip':omitted.append(path);continue
                errors.append(f'{p.relative_to(ROOT)}: broken link {target}')
            link_count+=1
    gallery=json.loads((ROOT/'V3.3/education/manifest.json').read_text(encoding='utf8'))
    for mid,row in gallery.items():
        for field in ['source','gif','poster']:
            if not(ROOT/row[field]).is_file():errors.append(mid+': missing '+field)
    catalogue=json.loads((ROOT/'printable-models/catalogue.json').read_text(encoding='utf8'))
    for row in catalogue:
        for field in ['source_catalogue','source_geometry']:
            if row.get(field) and not(ROOT/row[field]).is_file():errors.append(row['print_id']+': missing '+field)
    if len(gallery)!=20 or len(catalogue)!=75:errors.append('Model/GIF coverage changed')
    return {'status':'PASS' if not errors else 'FAIL','sharing_version':'V3-4','simulation_version':'v3.3.0','preserved_files_verified':count,'historical_or_legacy_files_omitted_from_distribution':sorted(set(omitted)),'local_links_checked':link_count,'model_gifs':len(gallery),'printable_entries':len(catalogue),'errors':errors,'scope':'Directory and byte-preservation validation; no new physical calibration or literature audit.'}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--extracted',action='store_true');args=parser.parse_args()
    report=validate(args.extracted);print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(0 if report['status']=='PASS' else 1)
