"""Create English-first/Chinese teaching notes and an offline STL index."""
from pathlib import Path
from collections import Counter
import csv,html,json,hashlib

H=Path(__file__).resolve().parent
def esc(x):return html.escape(str(x))
def pair(a,b):return esc(a)+'<br><span class="zh">'+esc(b)+'</span>'

def main():
    rows=json.loads((H/'catalogue.json').read_text(encoding='utf8'))
    generated=json.loads((H/'generated_manifest.json').read_text(encoding='utf8'))
    models={m['print_id']:m for m in generated['records']}
    assert len(rows)==75 and set(models)=={r['print_id'] for r in rows}
    kinds=Counter(r['kind'] for r in rows)
    (H/'cards').mkdir(exist_ok=True)
    md=['# Egg-size printable semiconductor teaching models','', '# 鸡蛋大小的半导体教学打印模型','',
        '**Print edition 1.0 · 2026-11-07 · 75 binary STL files.** Each model has a 60 × 42 mm flat footprint and stays below 25 mm high. These are tactile, enlarged cutaway/relief concepts. Sizes, layer thicknesses and doping boundaries are deliberately exaggerated for teaching, not manufacturing drawings.','',
        '**打印版1.0 · 2026-11-07 · 75份二进制STL。** 每件底面60×42毫米，高度低于25毫米，接近鸡蛋大小。模型为便于观察和触摸的放大剖面/浮雕概念；尺寸、薄层及掺杂边界为教学刻意放大，不是制造图纸。','',
        'Coverage: all 24 V1 entries, 31 V2 entries and 20 current V3.3 entries. Historical copies of the same A/B/P model are not counted again. **75 catalogue entries do not mean 75 distinct physical devices.** Circuit benches, parameter demonstrations and broader historical devices are explicitly classified.','',
        '覆盖V1全部24项、V2全部31项及当前V3.3全部20项，相同A/B/P模型的历史副本不重复统计。**75项目录条目不等于75种独立物理器件。** 电路台、参数演示及历史广义器件分别标注。','',
        '- [Offline illustrated atlas](index.html) — 离线图册，可筛选、看图并下载单件STL',
        '- [All STL files](stl/) — 全部单件STL',
        '- [Current V3.3 overview](contact_sheets/V33.png) · [V1](contact_sheets/V1.png) · [V2](contact_sheets/V2.png) — 分组总览',
        '- [Printing and interpretation guide](PRINT_GUIDE_EN_ZH.md) — 打印及教学阅读说明',
        '- [Geometry validation](validation/mesh_validation.json) — 从STL回读的几何检查',
        '- [Structured catalogue](catalogue.json) · [Printable file list](print_index.csv) — 来源、端口及文件映射',
        '- [Portable printing bundle](../Semiconductor_Teaching_STL_20261107.zip) — 打印资料包','',
        'STL coordinates must be interpreted as **millimetres**; STL does not embed a unit setting. Import at 100% scale. The preview colours encode height for readability, not material, doping concentration, voltage or current. Printed raised labels are English abbreviations; detailed notes are bilingual.','',
        'STL坐标须按**毫米**导入，STL自身不保存单位设置，导入比例为100%。预览颜色仅用高度辅助辨认，不代表材料、掺杂浓度、电压或电流。实物凸字为英文缩写，详细说明英中对照。','',
        'Geometry checks address closed meshes and the documented heightfield construction. No physical print, printer-specific slicing or semiconductor-process validation is claimed. The original electrical simulations and their accuracy limits are unchanged.','',
        '几何检查针对封闭网格及所记录的高度场构造；尚未进行实物试打、针对具体打印机的切片或半导体工艺验证。原电气仿真及准确性边界保持不变。','',
        '| ID | Model / 模型 | Class / 分类 | Files / 文件 |','|---|---|---|---|']
    cards=[]; export=[]
    for row in rows:
        pid=row['print_id'];m=models[pid]
        md.append(f"| {pid} | {row['name_en']}<br>{row['name_zh']} | {row['kind']} · {row['status']} | [STL](stl/{pid}.stl) · [Preview](previews/{pid}.png) · [Notes](cards/{pid}.md) |")
        notes=[f"# {pid} · {row['name_en']}",f"# {row['name_zh']}",'',f"Classification / 分类: `{row['kind']}` · `{row['status']}`",'',f"[STL](../stl/{pid}.stl) · [Preview](../previews/{pid}.png) · [Top view](../previews/{pid}_top.png)",'',f"![{pid}](../previews/{pid}.png)",'',
            '60 × 42 mm footprint; flat face on the bed, Z up. Dimensions are teaching choices; they have no process-scale mapping.','60×42毫米底面；平底朝打印平台，Z朝上。尺寸属于教学选择，不对应工艺比例。','',
            'This monolithic tactile relief is intentionally supported down to its base. Plastic continuity does not imply an electrical short or a particular material. Only printed surfaces and exposed ledges are visible; hidden interfaces are interpreted using the key.','本单体触觉浮雕刻意向底座填实支撑，塑料相连不代表电气短路或同一种材料。实物仅呈现表面及外露台阶，隐藏界面须配合图例理解。','',
            '## Visible feature key / 可见结构说明','', '| Mark | English | 中文 |','|---|---|---|']
        for f in m['features']:
            notes.append(f"| {f['label']} | {f['name_en']} | {f['name_zh']} |")
        notes+=['','Some small/hidden ledges have no raised lettering; the illustrated atlas and feature list identify them. Numbers on functional displays refer to the numbered source-parts list below.','部分小型或遮挡台阶不刻字，由图册和结构表辨认。功能展示件上的数字对应下方源部件列表。','','## Source concepts / 来源概念','']
        for i,p in enumerate(row['parts'],1):notes+=[f"{i}. {p.get('label_en',p['label'])}: {p['description_en']}<br>{p['description_zh']}"]
        notes+=['','## Terminals and boundaries / 端口与边界','']
        for p in row['terminals']:notes+=[f"- {p['label']} ({p['port_kind']}): {p['role_en']}<br>{p['role_zh']}"]
        notes+=['','## Interpretation limits / 解释边界','',row['limits_en'],'',row['limits_zh'],'',
            'Source-model limitations are retained below; STL generation does not add physics or establish process qualification.','下方保留源模型限制；生成STL不增加物理机制或工艺认证。','',row.get('source_limits_en',''),'',row.get('source_limits_zh',''),'',
            f"[Source catalogue / 源目录](../../{row['source_catalogue']}) · ID `{row['source_id']}`",'']
        (H/'cards'/f'{pid}.md').write_text('\n'.join(x for x in notes if x is not None).rstrip()+'\n',encoding='utf8',newline='\n')
        cards.append(f'''<article data-search="{esc((pid+' '+row['name_en']+' '+row['name_zh']).lower())}" data-group="{pid.split('_')[0]}" data-kind="{row['kind']}"><h2>{pair(pid+' · '+row['name_en'],row['name_zh'])}</h2><p class="tag">{esc(row['kind'])} · {esc(row['status'])}</p><a href="previews/{pid}.png"><img loading="lazy" src="previews/{pid}.png" alt="{esc(row['name_en'])}"></a><p><a class="button" href="stl/{pid}.stl" download>Download STL / 下载</a> <a href="previews/{pid}_top.png">Top view / 俯视</a></p><details><summary>Printed features / 实物结构</summary><ul>{''.join('<li><strong>'+esc(f['label'])+'</strong>: '+pair(f['name_en'],f['name_zh'])+'</li>' for f in m['features'])}</ul><a href="cards/{pid}.md">Full source notes / 完整来源说明</a></details><details><summary>Teaching scope / 教学范围</summary><p>{pair(row['limits_en'],row['limits_zh'])}</p><p>{pair(row.get('parts_scope_en',''),row.get('parts_scope_zh',''))}</p><ol>{''.join('<li>'+pair(p['description_en'],p['description_zh'])+'</li>' for p in row['parts'])}</ol></details></article>''')
        export.append(dict(print_id=pid,name_en=row['name_en'],name_zh=row['name_zh'],classification=row['kind'],status=row['status'],stl=f'stl/{pid}.stl',preview=f'previews/{pid}.png',footprint_mm='60 x 42',interpret_units='mm',stl_sha256=m['geometry_report']['stl_sha256'],source_catalogue=row['source_catalogue'],source_id=row['source_id']))
    md+=['','The complete sharing edition uses two archives: extract the core package to create **V3-3**, then extract **Semiconductor_Teaching_STL_20261107.zip inside that V3-3 folder**. The printing archive also works independently for printing. Its source files overlap some core dependencies with identical bytes; merge folders and keep the matching versions. Both archives and all individual files are available in the repository.','','完整分享版采用两个压缩包：先解压核心包得到 **V3-3**，再将 **Semiconductor_Teaching_STL_20261107.zip解压到该V3-3文件夹内部**。打印包也可独立用于打印；其部分源文件与核心依赖字节一致，合并目录并保留匹配版本即可。仓库同时保存两个压缩包及全部单独文件。']
    (H/'README.md').write_text('\n'.join(md).rstrip()+'\n',encoding='utf8',newline='\n')
    with (H/'print_index.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(export[0]));w.writeheader();w.writerows(export)
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Egg-size semiconductor teaching models</title><style>
body{font:16px/1.55 system-ui,sans-serif;margin:0;color:#17344a;background:#f1f5f8}header,main{max-width:1260px;margin:auto;padding:24px}header{background:#12364f;color:white}h1{font-size:28px;margin:0}.zh{font-size:.87em;opacity:.83;display:inline-block}a{color:#08659a}header a{color:#bfe7ff}.tools{position:sticky;top:0;background:#e4eef5;padding:16px;display:flex;gap:12px;flex-wrap:wrap;z-index:2}input,select{padding:10px;border:1px solid #adc1ce;border-radius:5px;font:inherit}input{flex:1;min-width:180px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}article{background:white;border:1px solid #cfdae2;border-radius:8px;padding:16px}h2{font-size:18px;margin:0}img{width:100%;height:auto}.tag{font-size:13px;color:#47647a}.button{background:#00658e;color:white;padding:8px;border-radius:5px;text-decoration:none}details{margin-top:18px}#count{font-weight:bold}article[hidden]{display:none}@media(max-width:390px){main,header{padding:12px}.grid{grid-template-columns:1fr}}
</style><header><h1>Egg-size semiconductor teaching models<br><span class="zh">鸡蛋大小的半导体教学打印模型</span></h1><p>75 catalogue entries · 60 × 42 mm footprints · binary STL interpreted in millimetres.<br>75项目录条目；60×42毫米底面；二进制STL按毫米导入。</p><p>Enlarged tactile reliefs, not to scale. Circuit displays are functional abstractions. Preview colour means height, not material or electrical data.<br>放大触觉浮雕，不按真实比例；电路展示是功能抽象。预览颜色表示高度，不表示材料或电气数据。</p><a href="PRINT_GUIDE_EN_ZH.md">Printing guide / 打印指南</a> · <a href="../Semiconductor_Teaching_STL_20261107.zip">Download all / 全部下载</a></header><main><div class="tools"><input id="search" placeholder="Search ID, device / 搜索编号、器件"><select id="group"><option value="">All editions / 全版本</option><option>V1</option><option>V2</option><option>V33</option></select><select id="kind"><option value="">All types / 全类型</option>OPTIONS</select></div><p id="count" role="status"></p><section class="grid">CARDS</section></main><script>
const q=document.querySelector('#search'),g=document.querySelector('#group'),k=document.querySelector('#kind'),a=[...document.querySelectorAll('article')];function filter(){let n=0;for(const x of a){x.hidden=!(x.dataset.search.includes(q.value.trim().toLowerCase())&&(!g.value||x.dataset.group===g.value)&&(!k.value||x.dataset.kind===k.value));if(!x.hidden)n++}document.querySelector('#count').textContent=n+' / 75 models · 模型'}for(const e of [q,g,k])e.addEventListener('input',filter);filter();</script></html>'''.replace('OPTIONS',''.join(f'<option>{esc(k)}</option>' for k in sorted(kinds))).replace('CARDS','\n'.join(cards))
    (H/'index.html').write_text(page+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'cards':len(cards),'types':kinds},ensure_ascii=False))

if __name__=='__main__':main()
