import sys
import pytest
import datetime
import inspect
import numpy as np
import glob

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
except:
    raise ImportError("couldn't import local pyABF")


@pytest.mark.parametrize("atfPath", glob.glob("data/abfs/*.atf"))
def test_ATF_hasSweeps(atfPath):
    atf = pyabf.ATF(atfPath)
    assert atf.sweepCount > 0
    assert len(atf.sweepY) > 0
    
@pytest.mark.parametrize("atfPath", glob.glob("data/abfs/*.atf"))
def test_ATF_setSweep(atfPath):
    atf = pyabf.ATF(atfPath)
    if (atf.sweepCount > 1):
        sweep0 = np.array(atf.sweepY)
        atf.setSweep(1)
        sweep1 = np.array(atf.sweepY)
        assert not np.array_equiv(sweep0, sweep1)