"""Dimensionless conceptual geometry; no fabrication dimensions or TCAD fields."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'models/obj';OUT.mkdir(exist_ok=True)
def box(name,center,size,color,terminal=None,signal=None):
 return dict(name=name,center=center,size=size,color=color,terminal=terminal,signal=signal)
def substrate():return [box('Substrate / 衬底',[0,-.5,0],[6,.4,3.5],'#7b8fa6')]
def mos(offset=0,labels=('S','G','D'),prefix=''):
 return [box(prefix+'well / 阱',[offset,-.12,0],[2.7,.35,1.7],'#688baf'),box(prefix+'oxide / 氧化层',[offset,.12,0],[2.4,.08,1.5],'#93d6c3'),
 box(labels[0],[offset-1,.3,0],[.65,.3,1.3],'#c8a66b',labels[0]),box(labels[1],[offset,.4,0],[.65,.5,1.3],'#d9b570',labels[1]),box(labels[2],[offset+1,.3,0],[.65,.3,1.3],'#c8a66b',labels[2])]
def block(name,x,z=0,color='#6a9ec2',terminal=None,signal=None):return box(name,[x,.15,z],[1.2,.7,1.1],color,terminal,signal)
geo={}
geo['A01']=substrate()+mos()+[box('B',[0,-.82,0],[1.8,.2,1.4],'#b38c60','B')]
geo['A02']=substrate()+[box('p region / p区',[-1,0,0],[2,.5,1.8],'#c38394'),box('n region / n区',[1,0,0],[2,.5,1.8],'#6da2bd'),block('A',-1,0,'#dab570','A'),block('K',1,0,'#dab570','K')]
geo['A03']=substrate()+[box('Collector / 集电区',[0,-.05,0],[4,.5,2.5],'#6298b8'),box('Base / 基区',[0,.24,0],[2.5,.12,1.9],'#bf7b92'),box('Emitter / 发射区',[0,.42,0],[1,.2,1.1],'#6aa8ba'),block('C',-2.1,0,'#dab570','C'),block('B',1.7,0,'#dab570','B'),box('E',[0,.7,0],[.7,.2,.8],'#dab570','E')]
geo['A04']=substrate()+mos(-1.5,('M1 S','M1 G','M1 D'),'M1 ')+mos(1.5,('M2 S','M2 G','M2 D'),'M2 ')
geo['B01']=substrate()+mos(-1.5,('Tail','G1','D1'),'M1 ')+mos(1.5,('Tail','G2','D2'),'M2 ')
geo['B02']=substrate()+[block('Q1',-2,-.5),block('Q2 ×8',0,-.5),block('R1',-1,1,'#b2a08b'),block('PTAT sum / 合成',2,0,'#938bb8',signal='Vref / 基准')]
geo['B03']=substrate()+[block('Input / 输入',-2),block('Noise shaping / 整形',0),block('Amplifier / 放大器',2),box('Sample C / 采样电容',[0,.5,1.2],[1.2,.5,.5],'#bea774')]
geo['B04']=substrate()+[box(f'C{2**k}',[-2.4+k*.55,.25,-.6],[.32,.4+.08*k,.7],'#c4af74')for k in range(10)]+[block('Comparator / 比较器',-1,1),block('SAR logic / 逐次逻辑',1,1,'#938bb8')]
geo['B05']=substrate()+[block('IN',-2,-.7,'#dab570','IN'),block('Pass / 调整管',0,-.7),block('OUT',2,-.7,'#dab570','OUT'),block('Error amplifier / 误差放大',-.8,1),block('Cout',1.3,1,'#c4af74'),box('GND',[0,-.8,0],[1.5,.2,1.5],'#dab570','GND')]
geo['B06']=substrate()+[block('Phase input / 相位输入',-2),block('Loop response / 环路',0),block('Phase output / 相位输出',2)]
geo['B07']=substrate()+[block('IN',-2.3,-.8,'#dab570','IN'),block('High side / 高侧',-.8,-.8),block('Low side / 低侧',-.8,1),block('SW',.5,-.8,'#dab570',signal='Vsw / 开关节点'),block('L',1.8,-.8,'#a89f8b'),block('OUT',2.4,1,'#dab570','OUT'),block('Cout',.8,1,'#c4af74'),box('GND',[-1,-.8,0],[1.5,.2,1.5],'#dab570','GND')]
faces=[[0,1,3,2],[4,6,7,5],[0,4,5,1],[2,3,7,6],[0,2,6,4],[1,5,7,3]]
for mid,boxes in geo.items():
 lines=['# Dimensionless conceptual geometry; NOT process geometry / 归一化概念结构'];base=1
 for j,b in enumerate(boxes):
  lines.append(f'o {mid}_part_{j}')
  for sx in [-.5,.5]:
   for sy in [-.5,.5]:
    for sz in [-.5,.5]:lines.append('v '+' '.join(str(b['center'][k]+[sx,sy,sz][k]*b['size'][k])for k in range(3)))
  for f in faces:lines.append('f '+' '.join(str(base+i)for i in f))
  base+=8
 (OUT/f'{mid}.obj').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'models/geometry.json').write_text(json.dumps(geo,ensure_ascii=False),encoding='utf-8')
print('Exported 11 dimensionless OBJ models')
