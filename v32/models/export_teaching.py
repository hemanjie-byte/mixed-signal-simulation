from pathlib import Path
import json
import numpy as np
from dcdc_models import deadtime_buck,recovery_pulse
R=Path(__file__).resolve().parents[1]/'results';R.mkdir(exist_ok=True)
d=deadtime_buck();q=recovery_pulse()
d={k:v.tolist()if isinstance(v,np.ndarray)else v for k,v in d.items()}
d['recovery']={'t_s':q['t'].tolist(),'Ireverse_A':q['irr'].tolist(),'Qrr_C':q['qrr'],'model_note':'Prescribed charge pulse, separate from inductor current and switching-node waveform.'}
d['model_note']='P02 ideal periodic CCM teaching trace with diode dead time. Not a transistor-level switching simulation. No finite-gate/Coss/ringing solution. Conventional inductor current remains positive.'
(R/'teaching_buck_100V_25C.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Exported teaching_buck_100V_25C.json')
