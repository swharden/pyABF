"""
This file tests retrieval of values from the user list.

The user list replaces one cell in the waveform editor for episodic files.
Instead of using a value and a delta, the user can provide a list of values to apply by sweep.
"""

import sys
import pytest
import numpy as np

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
except:
    raise ImportError("couldn't import local pyABF")


@pytest.mark.parametrize("abfPath, listValues", [

    ("data/abfs/171117_HFMixFRET.abf",
     [-100.0, 180.0, 160.0, 140.0, 120.0, 100.0, 80.0, 60.0, 40.0, 20.0, 0.0, -20.0, -60.0]),

    ("data/abfs/19212027.abf",
     [-50.0, -55.0, -60.0, -65.0, -70.0, -75.0, -80.0, -85.0, -90.0, -95.0, -100.0, -105.0, -110.0, -115.0, -120.0]),

    ("data/abfs/user-list-durations.abf",
     [4000, 6000, 6000, 10000, 20000, 30000, 30000, 30000, 30000]),

    ("data/abfs/2020_03_02_0000.abf",
     [-200.0, -150.0, -100.0, -50.0, 0.0, 25.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0]),

])
def test_userList_values(abfPath, listValues):
    abf = pyabf.ABF(abfPath)
    assert listValues == abf.userList


@pytest.mark.parametrize("abfPath, firstType", [
    ("data/abfs/171117_HFMixFRET.abf", 22),
    ("data/abfs/19212027.abf", 24),
    ("data/abfs/user-list-durations.abf", 35),
    ("data/abfs/2020_03_02_0000.abf", 62),

])
def test_userList_types(abfPath, firstType):
    abf = pyabf.ABF(abfPath)
    assert firstType == abf.userListParamToVary[0]
