"""Optional network audit of the published bibliography; does not overwrite it.

Usage: python v3/research/verify_bibliography.py --output doi_audit.json
Reads public Crossref metadata only, at a conservative rate. A name match is not
institutional authentication. Absence of update-to is not a retraction clearance.
"""
import argparse,json,urllib.request,urllib.parse,time,datetime
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
papers=json.loads((Path(__file__).parent/'papers.json').read_text(encoding='utf-8'));out=[]
for item in papers:
    url='https://api.crossref.org/works/'+urllib.parse.quote(item['doi'],safe='')
    record={'doi':item['doi'],'url':url,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'MixedSignalSimulation/3.0 (public-bibliography-check)'})
        with urllib.request.urlopen(request,timeout=40)as response:m=json.load(response)['message']
        record.update(ok=True,doi_matches=m.get('DOI','').lower()==item['doi'],title=m.get('title',[]),authors=m.get('author',[]),update_to=m.get('update-to',[]))
    except Exception as error:
        record.update(ok=False,error=str(error))
        if getattr(error,'code',None)==429:time.sleep(min(60,float(error.headers.get('Retry-After','10'))))
    out.append(record);time.sleep(2)
Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checked':len(out),'successful':sum(r['ok']for r in out),'output':args.output}))
