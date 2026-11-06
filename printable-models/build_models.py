"""Build enlarged, monolithic teaching reliefs; coordinates are millimetres."""
from pathlib import Path
import argparse, hashlib, json, sys
import numpy as np
from mesh_engine import HeightModel

HERE=Path(__file__).resolve().parent

class Lesson:
    def __init__(self, row):
        self.row=row; self.m=HeightModel(); self.features=[]; self.labels=[]
        self.m.text(row['print_id'].replace('_',' '),2,2,pixel_mm=0.8,raise_mm=0.8)
    def rect(self,label,en,zh,box,h,mark=True):
        self.m.rect(*box,h)
        self.features.append(dict(label=label,name_en=en,name_zh=zh,bounds_xy_mm=list(box),nominal_top_mm=h))
        if mark and label:self.labels.append((len(self.features)-1,label,box,h))
    def finish_labels(self):
        # Place letters only on a surviving level patch after all layer geometry.
        # A hidden or undersized patch stays unlettered and is identified in the atlas.
        for index,label,box,h in self.labels:
            target=round(h/0.4)*0.4; w=(6*len(label)-1)*2; hh=14
            heights=self.m.heightfield; found=None
            for y in range(int(np.ceil((box[1]+0.8)/0.4)),int(np.floor((box[3]-0.8)/0.4))-hh+1):
                for x in range(int(np.ceil((box[0]+0.8)/0.4)),int(np.floor((box[2]-0.8)/0.4))-w+1):
                    patch=heights[y:y+hh,x:x+w]
                    if patch.shape==(hh,w) and np.all(np.abs(patch-target)<0.05):found=(x*0.4,y*0.4);break
                if found:break
            self.features[index]['label_embossed']=found is not None
            if found:
                self.m.text(label,*found,pixel_mm=0.8,raise_mm=0.8)
                self.features[index]['label_xy_mm']=list(found)
    def substrate(self):
        self.rect('SUB','Exposed substrate ledge','外露衬底台阶',(3,11,57,39),5.6)
    def path(self,label,en,zh,pts,width,h):
        self.m.line(pts,width,h);self.features.append(dict(label=label,name_en=en,name_zh=zh,path_xy_mm=pts,width_mm=width,nominal_top_mm=h))
    def band(self,label,en,zh,index,h):
        # Staircase intentionally exposes layers; not a real sidewall profile.
        self.rect(label,en,zh,(5+index*2,12+index*6,55-index*2,39),h)

def mos(s,p=False,hv=False,pair=False,isolated=False):
    s.substrate()
    if pair:
        for x,tag in [(5,'1'),(32,'2')]:
            s.rect('P','Body well '+tag,'体区/阱 '+tag,(x,19,x+23,38),7.2)
            s.rect('S','Source '+tag,'源极 '+tag,(x+1,28,x+7,37),10.4)
            s.rect('D','Drain '+tag,'漏极 '+tag,(x+16,28,x+22,37),10.4)
            s.rect('OX','Gate dielectric '+tag,'栅介质 '+tag,(x+8,25,x+15,38),11.2,False)
            s.rect('G','Gate '+tag,'栅极 '+tag,(x+9,28,x+14,37),13.6)
        return
    s.rect('N' if p else 'P','Body well','体区/阱',(5,19,55,38),7.2)
    if hv:s.rect('DR','Extended drift region','延伸漂移区',(31,21,49,38),8.4)
    s.rect('S','Source contact / implanted region','源极接触/注入区',(7,27,17,37),10.4)
    s.rect('D','Drain contact / implanted region','漏极接触/注入区',(45,27,54,37),10.4)
    s.rect('OX','Exposed gate dielectric ledge','外露栅介质台阶',(19,21,33,38),9.6)
    s.rect('G','Gate electrode','栅电极',(22,29,30,38),13.6)
    s.rect('B','Separate body contact, distinct from doping label','独立体接触，与掺杂标签区分',(7,18,15,26),10.4)
    if isolated:
        for b in [(3,18,4.2,40),(55.8,18,57,40),(3,39,57,40.2)]:s.rect('ISO','Exposed isolation-boundary marker','外露隔离边界标记',b,8.4,False)
        s.features.append(dict(label='ISO',name_en='U-shaped exposed isolation boundary; teaching cutaway, not a specified foundry isolation topology',name_zh='U形外露隔离边界，教学剖切示意，非指定晶圆厂隔离拓扑'))
    s.features.append(dict(label='POL',name_en='P-channel schematic' if p else 'N-channel schematic',name_zh='P沟道示意' if p else 'N沟道示意'))

def bipolar(s,pnp=False):
    s.substrate(); s.rect('C','Collector region','集电区',(5,19,55,39),8.0)
    s.rect('B','Base region','基区',(20,25,51,39),11.2)
    s.rect('E','Emitter region','发射区',(37,31,48,39),15.2)
    s.features.append(dict(label='DOP',name_en='P-N-P doping order' if pnp else 'N-P-N doping order',name_zh='P-N-P掺杂顺序' if pnp else 'N-P-N掺杂顺序'))

def junction(s,schottky=False,pin=False,jbs=False):
    s.substrate()
    if schottky:
        s.rect('N','Semiconductor drift region','半导体漂移区',(6,19,54,39),8.4)
        s.rect('M','Metal / semiconductor contact','金属/半导体接触',(7,28,30,38),12.0)
        s.rect('K','Cathode contact','阴极接触',(44,28,53,38),10.8)
    elif pin:
        for l,en,zh,x0,x1,h in [('P','P region','P区',6,19,10),('I','Intrinsic region','本征区',20.2,39.8,8.4),('N','N region','N区',41,54,10)]:s.rect(l,en,zh,(x0,20,x1,39),h)
    else:
        s.rect('P','P-type region / anode','P型区/阳极',(6,20,29.2,39),10)
        s.rect('N','N-type region / cathode','N型区/阴极',(30.8,20,54,39),8.4)
        s.rect('J','Exposed junction marker','外露结界面标记',(27.2,30,33.6,38),11.2)
    if jbs:
        for x in [10,23,36]:s.rect('P','Junction-barrier island','结势垒P型岛',(x,22,x+5,27),13.2,False)

def resistor(s,sense=False):
    s.substrate()
    if sense:
        s.path('R','Short, wide sense element','短而宽的检测电阻体',[(10,27),(50,27)],5.6,8.4)
        s.rect('1','Terminal 1 at first path end','第一路径端的端子1',(6,23,14,31),10.4)
        s.rect('2','Terminal 2 at second path end','第二路径端的端子2',(46,23,54,31),10.4)
    else:
        s.path('R','Serpentine resistive strip','蛇形电阻条',[(10,20),(50,20),(50,24),(10,24),(10,28),(50,28),(50,32),(10,32),(10,36)],1.6,8.4)
        s.rect('1','Terminal 1 at first path end','第一路径端的端子1',(6,13,14,21),10.4)
        s.rect('2','Terminal 2 at second path end','第二路径端的端子2',(6,33,14,41),10.4)

def capacitor(s,mom=False,ferro=False,external=False):
    s.substrate()
    if mom:
        s.path('1','First metal comb bus','第一金属梳形母线',[(8,20),(8,37)],2.4,8.4)
        s.path('2','Second metal comb bus','第二金属梳形母线',[(52,20),(52,37)],2.4,8.4)
        for y in [21,27,33]:s.path('1','First comb fingers','第一梳形指条',[(8,y),(45,y)],1.6,8.4)
        for y in [24,30,36]:s.path('2','Second comb fingers','第二梳形指条',[(15,y),(52,y)],1.6,8.4)
    else:
        s.rect('BE','Bottom electrode','下电极',(5,19,55,39),7.6)
        s.rect('FE' if ferro else 'DE','Ferroelectric dielectric' if ferro else 'Dielectric','铁电介质' if ferro else '介质',(22,23,53,39),10)
        s.rect('TE','Top electrode','上电极',(38,30,51,39),13.2)
    if external:s.features.append(dict(label='TYPE',name_en='Generic plate-capacitor concept, not an asserted MLCC/electrolytic construction',name_zh='通用平板电容概念，不认定具体MLCC/电解电容结构'))

def isolation(s):
    s.substrate();s.rect('SI','Silicon island','硅岛',(16,23,44,35),10.4)
    for b in [(12,19,48,21.4),(12,36.6,48,39),(12,19,14.4,39),(45.6,19,48,39)]:s.rect('DTI','Raised deep-trench boundary marker','深沟槽边界凸起标记',b,8.4,False)
    s.features.append(dict(label='DTI',name_en='Trench dielectric is raised for touch; it is not a conductive wall',name_zh='沟槽介质用凸起便于触摸，不表示导电墙'))

def jfet(s):
    s.substrate();s.rect('N','N-type conducting channel','N型导电沟道',(7,24,53,33),8.4)
    s.rect('G','P-type gate regions','P型栅区',(23,18,35,25),11.2)
    s.rect('G','P-type gate regions','P型栅区',(23,32,35,39),11.2)
    s.rect('S','Source','源极',(6,26,14,38),10.4);s.rect('D','Drain','漏极',(46,26,54,38),10.4)

def vertical(s,igbt=False,sj=False):
    s.substrate();s.rect('P' if igbt else 'D','P-type bottom collector / hole-injection layer' if igbt else 'Bottom drain','P型底部集电极/空穴注入层' if igbt else '底部漏极',(5,18,55,39),7.2)
    s.rect('DR','Vertical drift layer','垂直漂移层',(18,20,53,39),10.4)
    if sj:
        for i,x in enumerate(range(22,49,4)):s.rect('P' if i%2==0 else 'N','Alternating superjunction column','交替超结柱',(x,23,x+2.4,38),12+(i%2)*0.8,False)
    s.rect('P','Body region','体区',(28,27,52,39),13.6)
    s.rect('E' if igbt else 'S','Top emitter' if igbt else 'Top source','顶部发射极' if igbt else '顶部源极',(42,31,51,39),16.8)
    s.rect('G','Insulated gate','绝缘栅',(29,31,38,39),16)

def hemt(s):
    s.band('BUF','Buffer / substrate ledge','缓冲层/衬底台阶',0,5.6)
    s.band('GAN','GaN channel region','GaN沟道区',1,8)
    s.band('BAR','Barrier / interface marker','势垒/界面标记',2,10.4)
    for l,x,h in [('S',10,13.6),('G',26,16),('D',43,13.6)]:s.rect(l,'Electrode '+l,'电极 '+l,(x,30,x+7,38),h)
    s.features.append(dict(label='2DEG',name_en='The conductive interface is conceptual; no specific enhancement-mode gate technology is certified',name_zh='导电界面为概念示意；不认定特定增强型栅工艺'))

def fin(s):
    s.substrate()
    for x in [19,28,37]:s.rect('FIN','Semiconductor fin','半导体鳍',(x,20,x+2.4,38),12,False)
    s.rect('G','Gate crossing fin channels','跨越鳍沟道的栅',(10,27,48,30.2),14.4,False)
    s.rect('G','Exposed gate pad, joined to crossing gate','与横跨栅连接的外露栅垫',(5,25,11,34),14.4)
    s.rect('S','Source joining the first ends of all fins; lowered cutaway exposes fins','连接所有鳍第一端的源区；降低剖切面以露出鳍',(12,18,48,26),8.4,False)
    s.rect('D','Drain joining the opposite ends of all fins; lowered cutaway exposes fins','连接所有鳍另一端的漏区；降低剖切面以露出鳍',(12,32,48,40),8.4,False)
    s.rect('S','Exposed source contact pad','外露源接触垫',(41,18,49,26),10.4)
    s.rect('D','Exposed drain contact pad','外露漏接触垫',(41,32,49,40),10.4)

def thinfilm(s,channel='ACT',ferro=False,cnt=False):
    s.substrate();s.rect('G','Exposed lower gate ledge','外露底栅台阶',(5,19,55,39),7.6)
    s.rect('FE' if ferro else 'OX','Ferroelectric gate stack' if ferro else 'Gate dielectric','铁电栅叠层' if ferro else '栅介质',(16,21,54,39),10)
    if not cnt:s.rect(channel,'Active film / channel joining both contacts','连接两接触的有源薄膜/沟道',(18,26,52,38),12.4)
    if cnt:
        for y in [28,32,36]:s.path('CNT','Enlarged nanotube channel ridge','放大纳米管沟道脊',[(22,y),(48,y)],1.2,13.6)
    s.rect('S','Source contacting one end of the active layer','接触有源层一端的源接触',(18,28,26,38),14.4);s.rect('D','Drain contacting the other end of the active layer','接触有源层另一端的漏接触',(44,28,52,38),14.4)

def memory(s,kind):
    if kind=='mtj':
        s.substrate();s.rect('REF','Reference magnetic layer / lower contact ledge','参考磁层/下接触台阶',(5,19,55,39),7.6)
        s.rect('TB','Tunnel-barrier dielectric','隧穿势垒介质',(21,23,53,39),10.4)
        s.rect('F','Free magnetic layer','自由磁层',(33,27,51,39),13.2)
        s.rect('T','Top contact above the free layer','自由层上方的顶接触',(40,31,50,39),16)
        return
    s.substrate();s.rect('BE','Bottom electrode','下电极',(5,19,55,39),7.6)
    label={'rram':'OX','pcm':'PCM','mtj':'REF'}[kind]
    s.rect(label,{'rram':'Switching oxide','pcm':'Phase-change region','mtj':'Reference magnetic layer'}[kind],{'rram':'阻变氧化层','pcm':'相变区域','mtj':'参考磁层'}[kind],(20,23,53,39),10.4)
    if kind=='mtj':s.rect('TB','Tunnel barrier and free-layer ledges','隧穿势垒与自由层台阶',(30,27,51,39),13.2)
    s.rect('TE','Top electrode','上电极',(40,31,50,39),16)
    if kind=='rram':s.path('FIL','Illustrative conductive-filament ridge','示意导电细丝脊',[(16,25),(19,28),(16,31),(19,34)],1.2,12)

def optical(s,kind):
    if kind in ['pin','pv']:junction(s,pin=kind=='pin')
    elif kind=='qdled':
        s.substrate();s.rect('HTL','Hole transport layer','空穴传输层',(5,19,55,39),7.6)
        s.rect('QD','Quantum-dot emissive layer','量子点发光层',(23,24,53,39),10.4)
        s.rect('ETL','Electron transport layer','电子传输层',(35,30,53,39),13.2)
    else:
        s.substrate();s.rect('N','Lower injection / cladding region','下部注入/包层区',(5,19,55,39),7.6)
        s.rect('QD' if kind=='qdled' else 'ACT','Active emission layer','有源发光层',(20,24,53,39),10.4)
        s.rect('P','Upper injection / cladding region','上部注入/包层区',(36,30,51,39),13.2)
    if kind=='laser':s.path('CAV','Optical cavity ridge','光学腔脊',[(8,36),(50,36)],1.6,15.2)

def inductor(s,transformer=False):
    s.substrate()
    if transformer:
        for idx,dx in [(1,0),(2,27)]:
            pts=[(5+dx,21),(23+dx,21),(23+dx,37),(7+dx,37),(7+dx,24),(20+dx,24),(20+dx,34),(11+dx,34),(11+dx,28),(16+dx,28)]
            s.path('PRI' if idx==1 else 'SEC','Primary open spiral' if idx==1 else 'Secondary open spiral','初级开口螺旋' if idx==1 else '次级开口螺旋',pts,1.2,9.2)
            s.rect(str(idx*2-1),'Winding outer terminal','绕组外端',(3+dx,17,7+dx,23),11.2,False)
            s.rect(str(idx*2),'Winding inner terminal','绕组内端',(15+dx,26,19+dx,30),11.2,False)
        s.features.append(dict(label='COUP',name_en='Two electrically separate open windings shown side by side for clarity; no coupling magnitude or actual winding layout asserted',name_zh='两组电气独立的开口绕组并列展示；不据此认定耦合量或实际绕组版图'))
        return
    pts=[(8,20),(52,20),(52,37),(10,37),(10,23),(48,23),(48,34),(14,34),(14,26),(44,26),(44,31),(18,31)]
    s.path('L1','Planar winding concept','平面绕组概念',pts,1.6,9.2)
    if transformer:
        s.path('L2','Second winding, offset for visibility','第二绕组，错位便于观察',[(20,28),(40,28),(40,30)],1.2,12)
        s.features.append(dict(label='L2',name_en='Offset demonstrator; not a manufacturable winding crossover layout',name_zh='错位展示，不是可制造的绕组跨接版图'))

def tsv(s):
    s.substrate();s.rect('SI','Silicon cross-section','硅剖面',(8,19,52,39),10.4)
    s.m.ellipse(30,28,10,8,12);s.features.append(dict(label='LIN',name_en='Via liner ring ledge',name_zh='通孔衬层环形台阶'))
    s.m.ellipse(30,28,7.2,5.2,16);s.m.text('CU',26,26,pixel_mm=0.8,raise_mm=0.8)
    s.features.append(dict(label='CU',name_en='Via conductor; enlarged exposed end',name_zh='通孔导体；放大外露端面'))

def teg(s):
    s.substrate();s.rect('COLD','Cold-side thermal plate','冷端热边界板',(5,19,55,39),6.8)
    s.rect('N','N-type thermoelectric leg','N型热电腿',(12,27,24,38),14.4);s.rect('P','P-type thermoelectric leg','P型热电腿',(36,27,48,38),14.4)
    s.rect('EN','Electrical terminal N (not the doping label)','电端N（不是掺杂标签）',(12,19,24,28),10.4)
    s.rect('EP','Electrical terminal P (not the doping label)','电端P（不是掺杂标签）',(36,19,48,28),10.4)
    s.path('HOT','Raised hot-side boundary marker','凸起热端边界标记',[(12,38),(48,38)],1.6,16)
    s.features.append(dict(label='PORT',name_en='HOT/COLD are thermal boundaries; electrical P/N ports are distinct from doping labels and are documented in the source mapping',name_zh='HOT/COLD为热边界；电气P/N端口与掺杂标记分开，详见源目录映射'))

def mzi(s):
    s.substrate()
    for sign in [-1,1]:s.path('WG','Interferometer waveguide arm','干涉仪波导臂',[(6,28),(15,28),(22,28+sign*7),(40,28+sign*7),(47,28),(54,28)],1.6,8.8)
    s.rect('RF','Electrode region beside one arm','一条臂旁的电极区',(25,29,36,36),11.2)

def bench(s):
    s.substrate(); parts=s.row.get('parts',[])[:4]
    for i,p in enumerate(parts):
        x=5+(i%2)*27;y=19+(i//2)*11
        s.rect(str(i+1),p.get('description_en',p.get('label','Block')),p.get('description_zh','功能块'),(x,y,x+23,y+9),8.4+(i%2)*1.6)
    s.features.append(dict(label='KEY',name_en='Numbered functional blocks, not silicon layout or solved 3D fields. See numbered key in the atlas.',name_zh='编号功能块，不是硅版图或求解的三维场，编号说明见图册'))

def choose(s):
    pid=s.row['print_id']; k=s.row['source_id']; prefix=pid.split('_')[0]
    if prefix=='V1':
        if k.startswith('M'):return mos(s,p=k in ['M03','M06','M07'],hv=k not in ['M05','M06'],isolated=k=='M01')
        if k.startswith('Q'):return bipolar(s,pnp=k=='Q02')
        if k.startswith('D'):return junction(s,schottky=k=='D03')
        if k.startswith('R'):return resistor(s,sense=k=='R02')
        if k.startswith('C'):return capacitor(s,mom=k=='C02',external=k in ['C03','C04','C05'])
        if k=='J01':return jfet(s)
        if k=='I01':return isolation(s)
        if k=='L01':return inductor(s)
        return bench(s)
    if prefix=='V2':
        if k in ['N01','N03','N04','X03']:return vertical(s,igbt=k=='N04',sj=k=='N03')
        if k=='N02':return hemt(s)
        if k=='N05':return junction(s,schottky=True,jbs=True)
        if k in ['N06','X06']:return fin(s) if k=='N06' else mos(s,pair=True)
        if k in ['N07','N08','N09','N10','N11','N12']:return thinfilm(s,channel={'N07':'IGZO','N08':'ORG','N09':'MOS2','N10':'GR','N11':'CNT','N12':'CH'}[k],ferro=k=='N12',cnt=k=='N11')
        if k in ['N13','N14','N15']:return memory(s,{'N13':'rram','N14':'pcm','N15':'mtj'}[k])
        if k=='N16':return capacitor(s,ferro=True)
        if k in ['N17','N18','N19','N20','N25']:return optical(s,{'N17':'led','N18':'qdled','N19':'pin','N20':'pv','N25':'laser'}[k])
        if k=='N21':return teg(s)
        if k=='N22':return inductor(s,True)
        if k=='N23':return tsv(s)
        if k=='N24':return mzi(s)
        if k=='X02':return junction(s)
        return mos(s,p=k=='X04')
    if k in ['A01','P01']:return mos(s,hv=k=='P01')
    if k in ['A02','P02']:return junction(s)
    if k=='A03':return bipolar(s)
    if k in ['A04','B01']:return mos(s,pair=True)
    return bench(s)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--ids',nargs='*');args=parser.parse_args()
    rows=json.loads((HERE/'catalogue.json').read_text(encoding='utf8'))
    if args.ids:rows=[r for r in rows if r['print_id'] in args.ids]
    out=[]
    for folder in ['stl','heightfields','validation']: (HERE/folder).mkdir(exist_ok=True)
    for row in rows:
        lesson=Lesson(row);choose(lesson);lesson.finish_labels()
        pid=row['print_id']; report=lesson.m.export(HERE/'stl'/f'{pid}.stl',HERE/'heightfields'/f'{pid}.npy')
        report['stl_path']=f'stl/{pid}.stl';report['heightfield_path']=f'heightfields/{pid}.npy'
        out.append(dict(print_id=pid,stl=f'stl/{pid}.stl',heightfield=f'heightfields/{pid}.npy',features=lesson.features,geometry_report=report))
        print(pid,flush=True)
    if not args.ids:
        (HERE/'generated_manifest.json').write_text(json.dumps({'format':'binary STL','units_interpretation':'millimetres; STL has no embedded units','size_xy_mm':[60,42],'base_mm':2.4,'grid_pitch_mm':0.4,'embossed_stroke_design_mm':0.8,'structural_feature_design_min_mm':1.2,'not_to_scale':True,'physical_print_tested':False,'records':out},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'generated':len(out)},ensure_ascii=False))

if __name__=='__main__':main()
