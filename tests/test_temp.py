"""
A temperary test for a single abf file that fails for me.
"""
# %%
import pyabf
from pathlib import Path
__file__ = r"C:\Users\peter\scripts\pyABF\tests\test_temp.py"

def test_load():
    abf_path = Path(__file__).parents[1] / "data" / "abfs" / "test_0001.abf"
    abf = pyabf.ABF(abf_path)
    abf.setSweep(sweepNumber=0, channel=8)
# %%
