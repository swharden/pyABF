"""
Inspect command waveform synthesis for a trouble ABF.
https://github.com/swharden/pyABF/issues/81
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
import numpy as np
import glob

def assertNanIsNotInSweepC(abf):

    for sweep in range(abf.sweepCount):
        for channel in range(abf.channelCount):
            abf.setSweep(sweep, channel=channel)

            if not abf._dacSection.nWaveformEnable[channel]:
                continue

            print(F"sweep {abf.sweepC}")
            if np.isnan(abf.sweepC).any():
                raise ValueError(f"Found at least one 'Not a Number' "
                                 f"entry in stimulus channel {channel} of sweep {sweep} "
                                 f"in file {abf.abfFilePath} using protocol {abf.protocol}.")


if __name__ == "__main__":
    #abf = pyabf.ABF(PATH_DATA+"/H19_29_150_11_21_01_0011.abf")
    #print(abf.sweepC)
    #assertNanIsNotInSweepC(abf)
    for abfFilePath in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFilePath)
        print()
        print(abf)
        print(abf.sweepC)