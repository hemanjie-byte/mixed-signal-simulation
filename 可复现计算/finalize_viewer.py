from pathlib import Path
p=Path(__file__).parent
f=p/'viewer_template.html'
s=f.read_text(encoding='utf-8')
s=s.replace("['mos','jfet','esd'].includes(dev.type)","['mos','jfet'].includes(dev.type)")
s=s.replace('let dir=dev.sign;',"let dir=['mos','jfet','bjt'].includes(dev.type)?dev.sign:-1;")
s=s.replace("[['A',-2,0,.8],['B',2,0,.8]]","[[dev.type==='esd'?'PAD':dev.type==='zener'?'K':'A',-2,0,.8],[dev.type==='esd'?'RETURN':dev.type==='diode'?'K':dev.type==='zener'?'A':'B',2,0,.8]]")
s=s.replace('<div id="cursor"></div>','<div id="cursor"></div><svg id="drive" class="plot" viewBox="0 0 650 300" style="display:none"></svg>')
s=s.replace('sample();draw3d();surface();',"if(current.drive){$('drive').style.display='block';plot($('drive'),[{x:current.x,y:current.drive,name:'外加端口电压',color:'#4779ac'}],current.xlabel,'VAB (V)')}else $('drive').style.display='none';sample();draw3d();surface();")
(p.parent/'DC_DC_3D器件演示.html').write_text(s.replace('__DATA__',(p/'data.json').read_text(encoding='utf-8')).replace('__RESEARCH__',(p/'research.json').read_text(encoding='utf-8')),encoding='utf-8')
print('HTML finalized')
