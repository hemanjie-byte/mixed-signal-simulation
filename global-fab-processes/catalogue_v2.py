"""Deterministic catalogue views from reviewed JSON; standard library only."""
from pathlib import Path
from collections import Counter
import csv,json,re
H=Path(__file__).resolve().parent
rows=json.loads((H/'data/processes.json').read_text(encoding='utf8'))
meta=json.loads((H/'catalogue.json').read_text(encoding='utf8'))
gaps=json.loads((H/'data/gaps.json').read_text(encoding='utf8'))
tax=json.loads((H/'data/taxonomy.json').read_text(encoding='utf8'))
BASE_KEYS=['company','region','business_type','platform','node','wafer','voltage','voltage_kind','devices','application','dcdc_relevance','availability','limitations','reading_depth','record_type']
FIELDS=['id']+[k+'_'+lang for k in BASE_KEYS for lang in ['en','zh']]+['process_family','material','scope_category','entity_role','parent_group','publication_state','evidence_kind','source_date_kind','source_title','source_url','source_date','checked_date','catalogue_revision_added']
assert rows and len({r['id']for r in rows})==len(rows)
for r in rows:
    assert all(k in r for k in FIELDS),r['id']
    assert r['source_url'].startswith('https://')
    for k in ['scope_category','entity_role','publication_state','evidence_kind','source_date_kind']:assert r[k]in tax[k],(r['id'],k,r[k])
slug=lambda s:re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
md=lambda s:str(s if s is not None else'Not disclosed / 未公开').replace('|','\\|').replace('\n','<br>')
bi=lambda r,k:md(r.get(k+'_en'))+'<br>'+md(r.get(k+'_zh'))
lab=lambda k,v:'<br>'.join(tax[k][v])
def write(name,s):
    p=H/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(s.rstrip()+'\n',encoding='utf8',newline='\n')
def jsave(name,data):write(name,json.dumps(data,ensure_ascii=False,indent=2))
companies=sorted({r['company_en']for r in rows})
pc=sum(r['scope_category']!='corporate_history'for r in rows)
with(H/'data/processes.csv').open('w',encoding='utf-8-sig',newline='')as f:
    w=csv.DictWriter(f,fieldnames=FIELDS+['additional_sources_json'],extrasaction='ignore');w.writeheader()
    for r in rows:w.writerow({**r,'additional_sources_json':json.dumps(r.get('additional_sources',[]),ensure_ascii=False)})
with(H/'data/gaps.csv').open('w',encoding='utf-8-sig',newline='')as f:
    w=csv.DictWriter(f,fieldnames=['name','status','reason_en','reason_zh','source_url'],extrasaction='ignore');w.writeheader();w.writerows(gaps)
labels=[('region','Geographic context / 地域背景'),('business_type','Business model / 业务类型'),('node','Node / 节点'),('wafer','Wafer / 晶圆尺寸'),('voltage','Published voltage / 公开电压'),('voltage_kind','Voltage meaning / 电压含义'),('devices','Devices / 器件'),('application','Applications / 应用'),('dcdc_relevance','40–150 V DC/DC relevance / 关联'),('availability','Availability / 可用性表述'),('limitations','Limits / 限制'),('reading_depth','Reading depth / 阅读深度')]
idx=[]
for c in companies:
    group=[r for r in rows if r['company_en']==c];name=slug(c)+'.md'
    s=f'# {c}\n\n# {group[0]["company_zh"]}\n\n[Catalogue](../README.md) · [工艺目录](../README.md)\n\n'
    for r in group:
        s+=f'## {r["id"]} · {r["platform_en"]}\n\n## {r["platform_zh"]}\n\n| Field / 字段 | Published context / 公开信息 |\n|---|---|\n'
        s+=f'| Record type / 记录类别 | {bi(r,"record_type")} |\n'
        for k,title in [('scope_category','Scope / 用途分类'),('entity_role','Entity role / 主体角色'),('publication_state','Published state / 公开状态'),('evidence_kind','Evidence read / 已读证据'),('source_date_kind','Date meaning / 日期含义')]:s+=f'| {title} | {lab(k,r[k])} |\n'
        s+=f'| Process family / 工艺家族 | {md(r["process_family"])} |\n| Material / 材料 | {lab("material",r["material"])} |\n'
        if r['parent_group']:s+=f'| Group relationship / 集团关系 | {md(r["parent_group"])} |\n'
        for k,title in labels:s+=f'| {title} | {bi(r,k)} |\n'
        s+=f'\nSource / 来源: [{md(r["source_title"])}]({r["source_url"]}). Source date / 来源日期: {md(r["source_date"])}. Checked / 核对: {r["checked_date"]}.\n\n'
        for extra in r.get('additional_sources',[]):
            if isinstance(extra,dict):s+=f'- [{md(extra.get("title",extra.get("source_title","Additional official source")))}]({extra.get("url",extra.get("source_url",""))})\n'
        s+='\n'
    write('companies/'+name,s)
    idx.append(f'| [{md(c)}](companies/{name})<br>{md(group[0]["company_zh"])} | {bi(group[0],"region")} | {len(group)} |')
intro=f'''# Global FAB public-process catalogue {meta['version']}

# 全球FAB公开工艺目录 {meta['version']}

Reviewed on **{meta['review_date']}**. **{len(companies)} catalogue entities; {len(rows)} evidence records ({pc} technical/manufacturing/research records and {len(rows)-pc} corporate-history record)**. Coverage expands mature silicon, high-voltage BCD/SOI, RF/SiGe, compound semiconductors and selected research platforms. Counts include disclosed subsidiaries and research institutes; they are not counts of independent ownership groups or physical fab sites.

核对日期：**{meta['review_date']}**。收录 **{len(companies)}个目录主体、{len(rows)}条资料（{pc}条技术／制造／研究资料、{len(rows)-pc}条业务沿革）**，扩展成熟硅、高压BCD/SOI、RF/SiGe、化合物半导体及部分研究平台。主体数包含明确标注的子公司和研究机构，不等于独立控股集团数或实体工厂数。

- [Searchable offline catalogue](index.html) — 可搜索、筛选及对比的离线目录
- [Bilingual Excel](Global_FAB_Public_Processes_EN_ZH.xlsx) — 英中对照Excel
- [Process CSV](data/processes.csv) / [JSON](data/processes.json) — 结构化工艺资料，保留补充来源
- [Coverage and remaining gaps](GAPS.md) — 覆盖情况与尚待核实的缺口
- [Revision changes](CHANGES.md) — 本轮新增与保留条目
- [Reading method](METHOD.md) — 电压、状态与分类阅读方法
- [Source-review notes](validation/SOURCE_REVIEW_EN_ZH.md) — 来源复核说明
- [V3-3 sharing entry](../V3-3/README.md) — V3-3分享入口

This is a documented public-source coverage review, not an exhaustive census of all fabs or process options worldwide. RF bias, breakdown voltage and maximum converter input are different quantities. Development, pilot, historical and IDM-internal offerings remain separately labelled. No PDK, proprietary production recipe or process-qualified simulation model is redistributed.

本目录是可追溯的公开资料覆盖审查，并非全球所有FAB或工艺选件的穷尽普查。RF偏置、击穿电压与转换器最高输入各有含义；开发、试产、历史与IDM内部工艺分别标注。不分发PDK、专有生产配方或工艺签核模型。

| Entity / 主体 | Geographic context / 地域背景 | Records / 资料记录 |
|---|---|---|
'''
write('README.md',intro+'\n'.join(idx))
payload=json.dumps({'rows':rows,'taxonomy':tax,'meta':meta,'gaps':gaps},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
write('index.html',(H/'viewer_template.html').read_text(encoding='utf8').replace('__DATA__',payload))
sources={}
for r in rows:
    for x in [{'title':r['source_title'],'url':r['source_url']},*r.get('additional_sources',[])]:
        if not isinstance(x,dict):continue
        u=x.get('url',x.get('source_url'));t=x.get('title',x.get('source_title'))
        if u:sources.setdefault(u,{'url':u,'title':t,'record_ids':[]})['record_ids'].append(r['id'])
jsave('data/source_index.json',list(sources.values()))
coverage={'version':meta['version'],'checked_date':meta['review_date'],'entities':len(companies),'records':len(rows),'technical_records':pc,'corporate_history_records':len(rows)-pc,'record_type_counts':dict(Counter(r['record_type_en']for r in rows)),'companies':companies,'source_urls':len(sources),'primary_source_urls':len({r['source_url']for r in rows}),'scope_counts':dict(Counter(r['scope_category']for r in rows)),'state_counts':dict(Counter(r['publication_state']for r in rows)),'evidence_counts':dict(Counter(r['evidence_kind']for r in rows)),'gap_candidates':len(gaps),'baseline_records_preserved':sum(r['catalogue_revision_added']=='1.0'for r in rows),'all_required_fields_present':True,'scope':'Catalogue entities, not physical sites or unique ownership groups; no PDK or converter qualification.'}
jsave('coverage.json',coverage)
s='# Coverage gaps and follow-up\n\n# 覆盖缺口与后续核对\n\nThe table separates candidates not reviewed in this pass, incomplete evidence and announcements retained outside the process table. No inclusion percentage is claimed because a complete global process denominator is unavailable. These are research dispositions, not assessments of supplier capability.\n\n下表区分本轮未核对候选、证据不足及未纳入工艺表的公告。缺少完整全球工艺分母，不计算覆盖率；这些状态描述研究进度，不评价供应商能力。\n\n| Candidate / 候选 | Disposition / 处理 | Reason / 原因 | Source / 来源 |\n|---|---|---|---|\n'
for g in gaps:s+=f'| {md(g["name"])} | {lab("gap_status",g["status"])} | {md(g["reason_en"])}<br>{md(g["reason_zh"])} | '+(f'[Official / 官方]({g["source_url"]})'if g.get('source_url')else'Not verified / 未核实')+' |\n'
write('GAPS.md',s)
new=[r for r in rows if r['catalogue_revision_added']!='1.0']
s=f'# Catalogue {meta["version"]} changes\n\n# 目录{meta["version"]}变更\n\nPreserves FAB001–FAB049 and their technical claims. Adds {len(new)} records, structured classifications, published-state and evidence filters, side-by-side comparison and filtered CSV export. Simulation release remains v3.3.0.\n\n保留FAB001～FAB049及其技术表述，新增{len(new)}条资料、结构化分类、公开状态与证据筛选、并排对比及筛选CSV导出。仿真版本仍为v3.3.0。\n\n| New ID / 新编号 | Entity / 主体 | Platform / 平台 |\n|---|---|---|\n'
for r in new:s+=f'| {r["id"]} | {md(r["company_en"])} | {bi(r,"platform")} |\n'
write('CHANGES.md',s)
print(json.dumps({k:coverage[k]for k in ['entities','records','gap_candidates']}))
