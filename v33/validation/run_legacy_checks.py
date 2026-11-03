"""Rerun both preserved suites without overwriting historical result files."""
from pathlib import Path
import unittest,sys,json,time,platform
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
class Recorder(unittest.TextTestResult):
    def __init__(self,*a,**k):super().__init__(*a,**k);self.records=[]
    def addSuccess(self,test):super().addSuccess(test);self.records.append(dict(test=test.id(),status='PASS'))
    def addFailure(self,test,err):super().addFailure(test,err);self.records.append(dict(test=test.id(),status='FAIL',reason=self._exc_info_to_string(err,test)))
    def addError(self,test,err):super().addError(test,err);self.records.append(dict(test=test.id(),status='ERROR',reason=self._exc_info_to_string(err,test)))
suite=unittest.TestSuite()
for folder in ['v3/tests','v32/tests']:
    path=str(ROOT/folder);sys.path.insert(0,path)
    suite.addTests(unittest.TestLoader().discover(path,pattern='test_*.py'))
start=time.time();result=unittest.TextTestRunner(verbosity=1,resultclass=Recorder).run(suite)
report=dict(date='2026-11-03',tests_run=result.testsRun,passed=result.wasSuccessful(),tests=result.records,python=platform.python_version(),numpy=np.__version__,elapsed_s=time.time()-start,scope='Preserved V3.1/V3.2 implementation regression, separate from V3.3 improvement tests.')
(ROOT/'v33/validation/legacy_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
sys.exit(0 if result.wasSuccessful()else 1)
