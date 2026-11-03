"""Run extension tests and serialize executed results."""
from pathlib import Path
import unittest,json,sys,time,platform
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
class Recorder(unittest.TextTestResult):
    records=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.records.append({'test':test.id(),'status':'PASS'})
    def addFailure(self,test,err):
        super().addFailure(test,err);self.records.append({'test':test.id(),'status':'FAIL','reason':self._exc_info_to_string(err,test)})
    def addError(self,test,err):
        super().addError(test,err);self.records.append({'test':test.id(),'status':'ERROR','reason':self._exc_info_to_string(err,test)})
suite=unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent),pattern='test_*.py');start=time.time()
result=unittest.TextTestRunner(verbosity=2,resultclass=Recorder).run(suite)
report=dict(date='2026-11-03',python=platform.python_version(),numpy=np.__version__,tests_run=result.testsRun,passed=result.wasSuccessful(),elapsed_s=round(time.time()-start,3),tests=result.records,scope='Independent analytical limits, energy/charge balances, event conditions, step refinement and exported artifacts. No PDK/measurement accuracy certification.')
(ROOT/'results/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.exit(0 if result.wasSuccessful()else 1)
