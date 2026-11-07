"""Execute tests and write actual outcomes to validation.json."""
from pathlib import Path
import unittest,json,sys,time,platform
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
class Recorder(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.records=[]
    def addSuccess(self,test):super().addSuccess(test);self.records.append(dict(test=test.id(),status='PASS'))
    def addFailure(self,test,err):super().addFailure(test,err);self.records.append(dict(test=test.id(),status='FAIL',reason=self._exc_info_to_string(err,test)))
    def addError(self,test,err):super().addError(test,err);self.records.append(dict(test=test.id(),status='FAIL',reason=self._exc_info_to_string(err,test)))
start=time.time();suite=unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent),pattern='test_*.py')
result=unittest.TextTestRunner(verbosity=2,resultclass=Recorder).run(suite)
report=dict(tests_run=result.testsRun,passed=result.wasSuccessful(),tests=result.records,python=platform.python_version(),numpy=np.__version__,elapsed_s=round(time.time()-start,3),scope='Selected numerical-error reductions, independent mathematical references, event timing, artifact integrity; not physical-model calibration.')
(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.exit(0 if result.wasSuccessful()else 1)
