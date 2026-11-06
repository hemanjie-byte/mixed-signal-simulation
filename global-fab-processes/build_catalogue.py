"""Public stable entry point for rebuilding catalogue views."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('catalogue_v2.py')),run_name='__main__')
