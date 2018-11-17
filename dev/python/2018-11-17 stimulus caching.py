"""
Demonstrate how to load many ABFs and use a cached stimulus waveform
from an ATF file which only gets loaded once. Since the ATF file is kept
in memory, this is stimulus waveform caching.
"""

import os
import sys
import glob
import time
import numpy as np

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

if __name__=="__main__":

    # An ATF file can be loaded just like an ABF file.
    # Most methods of the ABF class are the same for the ATF class.
    stimulus = pyabf.ATF(PATH_DATA+"/sine sweep magnitude 20.atf")
    stimulus.setSweep(0)
    stimulusWaveform = stimulus.sweepY

    # abf.sweepC can be assigned to at any time.
    # Extra work (trimming or null-padding the stimulus) is done here to
    # ensure the stimulus waveform length matches the sweep length.
    for abfFileName in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFileName)
        print("processing", abf.abfID, "...")
        if len(abf.sweepC) == len(stimulusWaveform):
            abf.sweepC = stimulusWaveform
        elif len(abf.sweepC) < len(stimulusWaveform):
            abf.sweepC = stimulusWaveform[:len(abf.sweepC)]
        elif len(abf.sweepC) > len(stimulusWaveform):
            abf.sweepC.fill(np.nan)
            abf.sweepC[:len(stimulusWaveform)] = stimulusWaveform