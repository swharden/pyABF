"""
More thorough sweep value validator created in June 2020.
Checks EVERY value of EVERY sweep of EVERY channel of EVERY ABF
to ensure it matches what we expect and does not change.
"""

try:
    import sys
    import pytest
    import datetime
    import inspect
    import numpy as np
    import glob

    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
    
    from test_sweepHashes import knownAbfSweepValues

except:
    raise ImportError("couldn't import local pyABF")


def sweepKeyAndInfo(abf, sweepIndex, channelIndex):
    assert isinstance(abf, pyabf.ABF)
    abf.setSweep(sweepIndex, channelIndex)
    key = str(f"{abf.abfID}.abf " +
              f"SW{sweepIndex} " +
              f"CH{channelIndex}")
    info = str(f"{len(abf.sweepY)}, " +
               f"{abf.sweepY[0]:.08f}, " +
               f"{abf.sweepY[-1]:.08f}, " +
               f"{np.std(abf.sweepY):.08f}")
    return [key, info]


@pytest.mark.parametrize("abfPath", glob.glob("data/abfs/*.abf"))
def test_valuesMatch_firstValue(abfPath):
    abf = pyabf.ABF(abfPath)
    print(f"verifying sweep values for {abf.abfID}.abf...")
    for sweepIndex in range(abf.sweepCount):
        for channelIndex in range(abf.channelCount):
            key, actualInfo = sweepKeyAndInfo(abf, sweepIndex, channelIndex)
            expectedInfo = knownAbfSweepValues[key]
            assert(expectedInfo == actualInfo)
