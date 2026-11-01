"""Normalized explanatory 3D geometry. No process dimensions, dopants or solved fields."""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'results/simulation_v2.json').read_text(encoding='utf-8'))
def box(label,x,y,z,dx,dy,dz,color,terminal=None):
    return dict(label=label,center=[x,y,z],size=[dx,dy,dz],color=color,terminal=terminal)
def geometry(d):
    sh=d['shape'];B=[]
    def add(*a,**k):B.append(box(*a,**k))
    add('substrate',0,0,-.7,5,3,.6,'#b7c4cc')
    if sh in ['vertical','igbt','superjunction','jbs']:
        add('drift',0,0,0,4,2.5,.8,'#77b1c7');add('back contact',0,0,-1.08,4.5,2.8,.12,'#4e6473',0)
        if sh=='superjunction':
            for i in range(7):add('P/N pillar',-1.65+i*.55,0,.15,.25,2.5,.9,'#d99c8b' if i%2 else '#6d9fce')
        if sh=='jbs':
            for i in [-1.3,0,1.3]:add('P shield',i,0,.43,.45,2,.16,'#d99c8b')
            add('Schottky contact',0,0,.6,4,2.2,.15,'#d1b35f',1)
        else:
            add('body',0,0,.52,3.6,2.1,.24,'#d99c8b');add('source/emitter',-1.2,0,.72,1,2,.14,'#4e6473',2)
            add('gate oxide',.2,0,.72,1.3,2,.10,'#e4d9bd');add('gate',.2,0,.84,1.3,2,.12,'#d1b35f',1)
    elif sh in ['fin','mos','tft','organic','2d','hemt','cnt','fefet']:
        add('insulator',0,0,-.28,4.7,2.8,.15,'#e4d9bd')
        if sh=='fin':
            for y in [-.8,0,.8]:add('Si fin',0,y,.22,3.6,.18,.9,'#77b1c7')
            add('multi-gate',0,0,.76,.8,2.6,.2,'#d1b35f',1)
        elif sh=='cnt':
            for y in [-.6,0,.6]:add('nanotube',0,y,.05,3.4,.10,.10,'#5a87a0')
            add('gate',0,0,-.03,1,2,.18,'#d1b35f',1)
        else:
            add('channel',0,0,-.08,3.5,2,.2 if sh not in ['2d','organic'] else .06,'#77b1c7')
            if sh=='hemt':add('AlGaN barrier',0,0,.07,3.5,2,.12,'#89c1ad')
            add('gate dielectric',0,0,.16,1,2,.14,'#dfd4b7')
            if sh=='fefet':add('ferroelectric',0,0,.32,1,2,.15,'#c693c3')
            add('gate',0,0,.51 if sh=='fefet' else .32,1.2,2.2,.15,'#d1b35f',1)
        add('drain',-1.8,0,.4,.7,2.2,.2,'#4e6473',0);add('source',1.8,0,.4,.7,2.2,.2,'#4e6473',2)
    elif sh in ['rram','pcm','mtj','fecap']:
        add('bottom electrode',0,0,-.1,3,2,.2,'#4e6473',1)
        if sh=='mtj':
            add('fixed magnet',0,0,.18,2.4,1.6,.3,'#6f9fc7');add('tunnel oxide',0,0,.4,2.4,1.6,.12,'#dfd4b7');add('free magnet',0,0,.62,2.4,1.6,.3,'#ce9397')
        else:
            add('active layer',0,0,.35,2.4,1.6,.65,'#c693c3' if sh=='fecap' else '#77b1c7')
            if sh=='rram':add('filament (schematic)',0,0,.35,.17,.17,.65,'#e3b354')
            if sh=='pcm':add('heater',0,0,.05,.6,.6,.35,'#d69971')
        add('top electrode',0,0,.95,3,2,.18,'#4e6473',0)
    elif sh in ['led','qdled','pin','pv','laser','diode']:
        add('N / bottom contact',0,0,-.12,4,2.5,.25,'#4e6473',1);add('N layer',0,0,.15,3.8,2.4,.3,'#6f9fc7')
        add('active / intrinsic',0,0,.4,3.8,2.4,.15,'#b28eb9');add('P layer',0,0,.66,3.8,2.4,.35,'#ce9397')
        add('P / top electrode',0,0,.91,3.8,.28,.15,'#d1b35f',0)
        if sh=='qdled':
            for x in [-1.2,0,1.2]:
                for y in [-.7,.7]:add('quantum dot',x,y,.48,.23,.23,.23,'#e3b354')
        if sh=='laser':
            for x in [-2,2]:add('cavity facet',x,0,.5,.08,2.4,.8,'#e4d9bd')
    elif sh=='teg':
        for x in [-1.5,-.5,.5,1.5]:add('P/N thermoleg',x,0,.25,.6,1,.9,'#d99c8b' if x<0 else '#6f9fc7')
        add('hot plate',0,0,.9,4,2,.18,'#d1b35f',0);add('cold plate',0,0,-.35,4,2,.18,'#4e6473',1)
    elif sh=='transformer':
        for z,col in [(.1,'#d1b35f'),(.5,'#77b1c7')]:
            for scale in [1.,.65,.3]:
                for y in [-scale,scale]:add('winding',0,y,z,3.8*scale,.12,.12,col)
                for x in [-1.9*scale,1.9*scale]:add('winding',x,0,z,.12,2*scale,.12,col)
        for j in range(4):add('pad',-2+j*1.3,-1.4,.7,.4,.4,.14,'#4e6473',j)
    elif sh=='tsv':
        add('oxide sleeve',0,0,.2,1.1,1.1,2.2,'#dfd4b7');add('Cu via',0,0,.2,.65,.65,2.5,'#d69971')
        add('IN pad',0,0,1.55,2,2,.15,'#d1b35f',0);add('OUT pad',0,0,-1.15,2,2,.15,'#4e6473',1);add('substrate tap',2,0,.2,.5,1,.2,'#4e6473',2)
    elif sh=='mzi':
        for y in [-.7,.7]:add('waveguide arm',0,y,.1,4,.16,.2,'#77b1c7')
        for x in [-2,2]:add('splitter / combiner',x,0,.1,.3,1.5,.2,'#77b1c7')
        add('phase electrode',0,-.7,.4,2.5,.5,.15,'#d1b35f',0);add('return',0,.7,.4,2.5,.5,.15,'#4e6473',1)
    return B

def vertices(b):
    x,y,z=b['center'];a,c,e=[v/2 for v in b['size']]
    return [[x+u*a,y+v*c,z+w*e] for u,v,w in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
FACES=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
geos={d['id']:geometry(d) for d in data['models']}
(ROOT/'models/geometry.json').write_text(json.dumps(geos,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
objdir=ROOT/'models/OBJ';objdir.mkdir(exist_ok=True)
for id,bs in geos.items():
    out=['# Normalized explanatory geometry only. No process dimensions or simulation fields.'];offset=1
    for j,b in enumerate(bs):
        out.append('g region_'+str(j));out+=['v '+' '.join(map(str,v)) for v in vertices(b)]
        out+=['f '+' '.join(str(offset+k) for k in f) for f in FACES];offset+=8
    (objdir/(id+'.obj')).write_text('\n'.join(out)+'\n',encoding='utf-8')
if __name__=='__main__':
    from PIL import Image,ImageDraw,ImageFont
    preview=ROOT/'models/previews';preview.mkdir(exist_ok=True)
    for id,bs in geos.items():
        im=Image.new('RGB',(720,456),'#f5f7f9');dr=ImageDraw.Draw(im);faces=[]
        def project(v):
            x,y,z=v;az=-.65;el=.55;u=x*math.cos(az)-y*math.sin(az);q=x*math.sin(az)+y*math.cos(az);w=z*math.cos(el)-q*math.sin(el);dep=q*math.cos(el)+z*math.sin(el)
            return (360+u*95,255-w*95,dep)
        for b in bs:
            vs=[project(v) for v in vertices(b)]
            for f in FACES:faces.append((sum(vs[k][2] for k in f)/4,[(vs[k][0],vs[k][1]) for k in f],b['color']))
        for depth,pts,col in sorted(faces,key=lambda v:v[0]):dr.polygon(pts,fill=col,outline='#516370')
        dr.text((18,18),id+' | normalized structure; no solved field',fill='#243e50',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20))
        im.save(preview/(id+'.png'))
    print('Generated',len(geos),'geometries, OBJ files and previews')
