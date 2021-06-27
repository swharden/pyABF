"""
Tests related to locating and reading command waveforms from stimulus waveform 
files. If the stimulus waveforms aren't found you can provide a search path
as an argument when instantiating pyabf.ABF()
"""

import sys
import pytest
import os
import numpy as np
import time
import warnings

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
except:
    raise ImportError("couldn't import local pyABF")

ABF_PATH = os.path.abspath("data/abfs/H19_29_150_11_21_01_0011.abf")
STIM_FOLDER = os.path.abspath("data/stimulusFiles")


def test_findStimulusFile_NansIfNotFound():
    """When the stimulus file isn't found the waveform should be all NANs."""

    warnings.simplefilter("ignore")
    abf = pyabf.ABF(ABF_PATH)
    stimulus = abf.stimulusByChannel[0]
    waveform = stimulus.stimulusWaveform(stimulusSweep=0)

    assert isinstance(waveform, np.ndarray)
    assert len(waveform) == len(abf.sweepY)
    assert np.isnan(waveform).all()


def test_findStimulusFile_foundIfPathGiven():
    """The user can tell pyABF where to look for stimulus files."""

    abf = pyabf.ABF(ABF_PATH, stimulusFileFolder=STIM_FOLDER)
    stimulus = abf.stimulusByChannel[0]
    waveform = stimulus.stimulusWaveform(stimulusSweep=0)

    assert isinstance(waveform, np.ndarray)
    assert not np.isnan(waveform).any()
    assert pytest.approx(waveform[100000], 76.261)


def cachedStimulusSpeedBoost(useCaching):
    """Open an ABF/stimulus twice and return the times (in sec)"""

    times = [None, None]
    useCaching = [False, useCaching]
    for i in range(2):
        t1 = time.perf_counter()
        abf = pyabf.ABF(
            ABF_PATH,
            stimulusFileFolder=STIM_FOLDER,
            cacheStimulusFiles=useCaching[i]
        )
        stimulus = abf.stimulusByChannel[0]
        waveform = stimulus.stimulusWaveform(stimulusSweep=0)
        assert pytest.approx(waveform[100000], 76.261)
        times[i] = time.perf_counter() - t1

    speedBoost = times[0]/times[1]
    print(f"Caching: {useCaching[1]}, speed boost: {speedBoost}x")
    return speedBoost


@pytest.mark.slow
def test_stimulus_caching():

    # first try without caching
    assert (cachedStimulusSpeedBoost(False) < 2)

    # now use caching for a >10x speed boost
    assert (cachedStimulusSpeedBoost(True) > 10)

    # confirm not using caching is still slow
    assert (cachedStimulusSpeedBoost(False) < 2)
