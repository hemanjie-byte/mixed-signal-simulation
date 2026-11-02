"""Run tests and serialize actual outcomes; exits nonzero on any failure."""
import unittest,json,sys,platform,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))

class Recorder(unittest.TextTestResult):
    records=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.records.append({'test':test.id(),'status':'PASS'})
    def addFailure(self,test,err):
        super().addFailure(test,err);self.records.append({'test':test.id(),'status':'FAIL','reason':self._exc_info_to_string(err,test)})
    def addError(self,test,err):
        super().addError(test,err);self.records.append({'test':test.id(),'status':'ERROR','reason':self._exc_info_to_string(err,test)})

suite=unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent),pattern='test_*.py')
start=time.time();result=unittest.TextTestRunner(verbosity=2,resultclass=Recorder).run(suite)
report={'date':'2026-11-02','python':platform.python_version(),'numpy':np.__version__,'tests_run':result.testsRun,'passed':result.wasSuccessful(),'elapsed_s':round(time.time()-start,3),'tests':result.records,'scope':'Analytical limits, conservation, numerical convergence and artifacts. No measured/PDK accuracy certification.'}
(ROOT/'results/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
sys.exit(0 if result.wasSuccessful()else 1)
