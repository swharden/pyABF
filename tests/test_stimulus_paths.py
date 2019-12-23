"""
Tests related to locating and reading command waveforms from stimulus waveform 
files. If the stimulus waveforms aren't found you can provide a search path
as an argument when instantiating pyabf.ABF()
"""

import sys
import pytest
import os
import numpy as np

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
