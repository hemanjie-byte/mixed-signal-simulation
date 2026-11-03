"""Run the actual analog numerical-upgrade tests and record their outcomes."""
import json
from pathlib import Path
import platform
import sys
import time
import unittest
import numpy as np

HERE = Path(__file__).resolve().parent


class Recorder(unittest.TextTestResult):
    records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append(dict(test=test.id(), status="PASS"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append(dict(test=test.id(), status="FAIL", reason=self._exc_info_to_string(err, test)))

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append(dict(test=test.id(), status="ERROR", reason=self._exc_info_to_string(err, test)))


suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_*.py")
start = time.time()
result = unittest.TextTestRunner(verbosity=2, resultclass=Recorder).run(suite)
report = dict(date="2026-11-03", python=platform.python_version(), numpy=np.__version__,
              tests_run=result.testsRun, passed=result.wasSuccessful(), tests=result.records,
              elapsed_s=round(time.time() - start, 3),
              scope_en="Numerical evaluation of unchanged reduced equations, independent references, conserved quantities and export compatibility; no physical-model or silicon accuracy certification.",
              scope_zh="既有简化方程的数值计算、独立参考、守恒量与导出兼容性；不认证物理模型或硅片精度。")
(HERE / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sys.exit(0 if result.wasSuccessful() else 1)
