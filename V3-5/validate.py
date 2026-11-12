"""Check V3-5 coverage, preserved scientific assets, links and delivery claims.

This is numerical/teaching delivery validation, not measured device qualification.
The 96 scientific tests and full mesh validation run separately in CI.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import hashlib,json,re,subprocess,sys
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def read(p):return json.loads((HERE/p).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ['href','src'] and v:self.links.append(v)

def main():
    errors=[];counts={}
    def check(ok,message):
        if not ok:errors.append(message)
    for p in ROOT.iterdir():
        if p.is_dir() and not p.name.startswith('.'):
            check(p.name=='V3-5',f'Unexpected root directory: {p.name}')
    for p in HERE.rglob('*'):
        if p.is_dir() and re.fullmatch(r'(?i)v\d+(?:[._-]\d+)*',p.name):
            check(bool(re.fullmatch(r'V\d+-\d+',p.name)),f'Noncanonical version directory: {p}')
    check(not list(ROOT.glob('*.zip')),'Release ZIPs must not duplicate the working tree')
    books=list(ROOT.rglob('*.xlsx'));check(len(books)==1,'Expected one compact workbook')
    lessons=read('lessons/lessons.json')['lessons'];prints=read('lessons/print_lessons.json')
    prows=prints.get('print_lessons',prints.get('models',prints.get('entries',prints.get('lessons',[]))))
    audit=read('evidence/validity_audit.json')['models'];catalogue=read('printing/catalogue.json')
    models=[];cases=[]
    for f in ['analog','dcdc']:
        d=read(f'simulation/V3-3/numerics/{f}/simulation.json');models+=d['models'];cases+=d['cases']
    ids={m['id']for m in models}
    check(len(ids)==len(models)==20,'Twenty unique numerical entries are required')
    check(len(cases)==211,'Expected 211 recorded cases')
    check(len(lessons)==20 and {x['id']for x in lessons}==ids,'Lesson coverage differs from model coverage')
    check(len(audit)==20 and {x['model_id']for x in audit}==ids,'Validity coverage differs from model coverage')
    check(len(prows)==75 and {x.get('print_id',x.get('id'))for x in prows}=={x['print_id']for x in catalogue},'Printing lesson coverage is incomplete')
    check(Counter(x.get('numeric_status',{}).get('electrical_rerun_in_this_release')for x in prows)=={True:20,False:55},'Historical teaching structures must not imply a new electrical rerun')
    for row in prows:
        check(row.get('numeric_status',{}).get('physical_calibration_verified') is False,f"Unsupported printing calibration claim: {row.get('print_id')}")
    for lesson in lessons+prows:
        ident=lesson.get('id',lesson.get('print_id'))
        for level in ['beginner','undergraduate','graduate']:
            check(bool(lesson.get(level)),f'{ident}: missing {level}')
        check(len({json.dumps(lesson.get(l),ensure_ascii=False,sort_keys=True)for l in ['beginner','undergraduate','graduate']})==3,f'{ident}: learning levels are duplicates')
    check(Counter(x['kind']for x in lessons)=={'illustrative_device':3,'statistical_parameter_demo':1,'prescribed_mechanism_bench':2,'circuit_system_bench':14},'Misleading numerical-entry classification')
    for a in audit:
        check(a.get('physical_calibration_verified') is False and a.get('foundry_qualified') is False,f"Unsupported calibration claim: {a['model_id']}")
        check(a['observed_ranges_are_ratings'] is False,f"Observed ranges treated as ratings: {a['model_id']}")
    saved={x['id']:x for x in cases}
    for lesson in lessons:
        check(lesson['recorded_case']['metrics']==saved[lesson['recorded_case']['id']]['metrics'],f"Lesson case metrics changed: {lesson['id']}")
        for p in [lesson['assets']['gif_path'],*lesson['assets']['stl_paths']]:check((HERE/p).is_file(),f'Missing lesson asset: {p}')
    preserved=read('evidence/preservation.json')['files']
    for row in preserved:
        p=ROOT/row['path'];check(p.is_file() and sha(p)==row['sha256'],f"Scientific asset changed: {row['path']}")
    counts['preserved_scientific_files']=len(preserved)
    gallery=read('simulation/V3-3/education/manifest.json')
    for mid,g in gallery.items():
        for k,h in [('source','source_sha256'),('gif','gif_sha256'),('poster','poster_sha256')]:
            p=HERE/'simulation'/g[k];check(p.is_file() and sha(p)==g[h],f'{mid}: {k} hash differs')
        with Image.open(HERE/'simulation'/g['gif']) as image:
            check(image.n_frames==g['frames'],f'{mid}: frame count changed')
            for i in range(image.n_frames):image.seek(i);image.load()
    counts.update(models=20,cases=len(cases),levels=3,model_gifs=len(gallery),printing_entries=len(prows))
    candidates=[ROOT/'README.md',ROOT/'VERSIONS.md',ROOT/'index.html',*HERE.rglob('*.md'),*HERE.rglob('*.html')]
    checked=0
    for p in candidates:
        if p.name.endswith('_template.html'):continue
        s=p.read_text('utf8')
        if p.suffix=='.html':parser=Links();parser.feed(s);links=parser.links
        else:
            s=re.sub(r'```.*?```','',s,flags=re.S)
            links=re.findall(r'\]\(([^)\n]+)\)',s)
        for dest in links:
            dest=dest.strip().strip('<>');u=urlsplit(dest)
            if u.scheme or u.netloc or not u.path:continue
            q=(p.parent/unquote(u.path)).resolve();checked+=1
            check(q.is_relative_to(ROOT.resolve()) and q.exists(),f'{p.relative_to(ROOT)}: broken local link {dest}')
    counts['local_links']=checked
    for script in ['printing/validation/validate_delivery.py','fab/validate_catalogue.py']:
        result=subprocess.run([sys.executable,'-X','utf8',str(HERE/script)],capture_output=True,text=True,encoding='utf8')
        check(result.returncode==0,f'{script}: {result.stdout[-6000:]} {result.stderr[-2000:]}')
    report={'status':'PASS'if not errors else'FAIL',**counts,'errors':errors,'physical_accuracy_verified':False,'physical_print_tested':False}
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if not errors else 1
if __name__=='__main__':sys.exit(main())
