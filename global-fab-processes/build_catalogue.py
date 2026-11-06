"""Render the public catalogue from reviewed records; standard library only."""
from pathlib import Path
from collections import Counter
import csv, html, json, re

HERE=Path(__file__).resolve().parent
ROWS=json.loads((HERE/'data/processes.json').read_text(encoding='utf8'))
assert ROWS and len({r['id'] for r in ROWS})==len(ROWS)
REQUIRED=['id','company_en','company_zh','region_en','region_zh','business_type_en','business_type_zh','platform_en','platform_zh','node_en','node_zh','wafer_en','wafer_zh','voltage_en','voltage_zh','voltage_kind_en','voltage_kind_zh','devices_en','devices_zh','application_en','application_zh','dcdc_relevance_en','dcdc_relevance_zh','availability_en','availability_zh','limitations_en','limitations_zh','source_title','source_url','source_date','checked_date','reading_depth_en','reading_depth_zh']
for r in ROWS:
    assert all(k in r for k in REQUIRED),r['id']
    assert r['source_url'].startswith('https://'),r['id']
    assert r['checked_date']=='2026-11-06'
companies=sorted({r['company_en'] for r in ROWS})
process_count=sum(r['record_type_en']=='Process / platform' for r in ROWS)
REQUIRED+=['record_type_en','record_type_zh']
slug=lambda s: re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def md(s):return str(s if s is not None else 'Not disclosed / 未公开').replace('|','\\|').replace('\n','<br>')
def bi(r,k):return md(r.get(k+'_en'))+'<br>'+md(r.get(k+'_zh'))
with (HERE/'data/processes.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=REQUIRED,extrasaction='ignore');w.writeheader();w.writerows(ROWS)
(HERE/'companies').mkdir(exist_ok=True)
index=[]
for company in companies:
    group=[r for r in ROWS if r['company_en']==company]
    p=HERE/'companies'/f'{slug(company)}.md'
    text=f'# {company}\n\n# {group[0]["company_zh"]}\n\n[Catalogue](../README.md) · [工艺目录](../README.md)\n\n'
    for r in group:
        text+=f'## {r["id"]} · {r["platform_en"]}\n\n## {r["platform_zh"]}\n\n'
        text+='| Field / 字段 | Published context / 公开信息 |\n|---|---|\n'
        text+=f'| Record type / 记录类别 | {bi(r,"record_type")} |\n'
        for k,label in [('region','Geographic context / 地域背景'),('business_type','Business model / 业务类型'),('node','Node / 节点'),('wafer','Wafer / 晶圆尺寸'),('voltage','Published voltage / 公开电压'),('voltage_kind','Voltage meaning / 电压含义'),('devices','Devices / 器件'),('application','Applications / 应用'),('dcdc_relevance','40–150 V DC/DC relevance / 关联'),('availability','Availability wording / 可用性表述'),('limitations','Limits / 限制'),('reading_depth','Reading depth / 阅读深度')]:
            text+=f'| {label} | {bi(r,k)} |\n'
        text+=f'\nSource / 来源: [{md(r["source_title"])}]({r["source_url"]}). Source date / 来源日期: {md(r["source_date"])}. Checked / 核对: {r["checked_date"]}.\n\n'
        for extra in r.get('additional_sources',[]):
            if isinstance(extra,dict):text+=f'- [{md(extra.get("title",extra.get("source_title","Additional official source")))}]({extra.get("url",extra.get("source_url",""))})\n'
    p.write_text(text.rstrip()+'\n',encoding='utf8',newline='\n')
    index.append(f'| [{md(company)}](companies/{p.name})<br>{md(group[0]["company_zh"])} | {bi(group[0],"region")} | {len(group)} |')

intro=f'''# Global FAB public-process catalogue

# 全球FAB公开工艺目录

Reviewed on **2026-11-06**. This first catalogue covers **{len(companies)} manufacturers and {len(ROWS)} evidence records ({process_count} process/platform records and {len(ROWS)-process_count} corporate-history context record)** across mainland China, Taiwan, Korea, Japan, Europe and North America. It is a selected public-source collection, not an exhaustive list of all global fabs or every device option.

核对日期：**2026-11-06**。首批目录覆盖中国大陆、台湾、韩国、日本、欧洲及北美的 **{len(companies)} 家厂商、{len(ROWS)} 条公开资料（{process_count}条工艺/平台及{len(ROWS)-process_count}条业务沿革）**，属于有选择的公开资料集合，并非全球全部晶圆厂或全部器件选件清单。

- [Searchable offline catalogue](index.html) — 可搜索的离线目录
- [Filterable bilingual Excel](Global_FAB_Public_Processes_EN_ZH.xlsx) — 可筛选英中对照Excel
- [CSV](data/processes.csv) / [JSON](data/processes.json) — 结构化工艺资料
- [How to read process claims](METHOD.md) — 工艺信息阅读方法
- [Source-review scope and limitations](validation/SOURCE_REVIEW_EN_ZH.md) — 来源复核范围与限制
- [V3-3 sharing entry](../V3-3/README.md) — V3-3分享入口

Each record links the manufacturer's primary source and states node, wafer size, voltage meaning, disclosed device classes, analog/power relevance, commercial context, reading depth and unresolved details. Geographic labels describe the vendor/technology context; they are not a complete list of physical fab sites. Public process descriptions do not include licensed PDKs, production recipes or foundry sign-off models.

每条记录链接厂商一手来源，列出节点、晶圆尺寸、电压含义、公开器件类别、模拟/电源关联、商业背景、阅读深度与未确认内容。地域标签为厂商/技术背景，不是实体工厂的完整地址表。公开工艺介绍不包含授权PDK、生产配方或签核模型。

Device working voltage, breakdown voltage and converter maximum input are separate quantities. A platform family maximum cannot be assigned to every process node. Historical announcements and IDM internal processes are explicitly described; catalogue inclusion does not confirm present external orders.

器件工作电压、击穿电压和转换器最高输入是不同量；平台家族上限不能自动赋予每个节点。历史公告与IDM内部工艺分别说明；收录不代表确认目前对外接单。

| Manufacturer / 厂商 | Geographic context / 地域背景 | Evidence records / 资料记录 |
|---|---|---|
'''
(HERE/'README.md').write_text(intro+'\n'.join(index)+'\n',encoding='utf8',newline='\n')
payload=json.dumps(ROWS,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
template=(HERE/'viewer_template.html').read_text(encoding='utf8')
(HERE/'index.html').write_text(template.replace('__DATA__',payload).rstrip()+'\n',encoding='utf8',newline='\n')
(HERE/'coverage.json').write_text(json.dumps({'checked_date':'2026-11-06','manufacturers':len(companies),'records':len(ROWS),'process_records':process_count,'context_records':len(ROWS)-process_count,'companies':companies,'source_urls':len({r['source_url'] for r in ROWS}),'all_required_fields_present':True,'scope':'Selected official public process descriptions; no PDK or operating-rating certification.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'manufacturers':len(companies),'records':len(ROWS)},ensure_ascii=False))
