"""
see if a simpler stimulus class can be designed
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob
import numpy as np
import matplotlib.pyplot as plt

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Epoch:
    def __init__(self, abf):
        """
        A simple wrapper for
        """
        assert isinstance(abf, pyabf.ABF)

        if abf.abfVersion["major"]==1:
            self._readV1()
        else:
            self._readV2()
            
    def _readV1(self):
        """ABF v1 does not support epoch waveforms."""
        self.points = []
        self.values = []
        self.digitalWaveform = []

    def _readV2(self):
        """Prepare epoch points and values from the epoch table."""

        points = pyabf.stimulus.epochPoints(abf)
        values = list(pyabf.stimulus.epochValues(abf)[abf.sweepNumber])

        # add an extra point for the beginning of the sweep
        points = [0]+points
        values = [abf.sweepC[0]]+values

        # add extra points for the end of the sweep
        points.append(abf.sweepPointCount)
        while (len(values)<len(points)):
            values.append(abf.sweepC[-1])

        self.points = points
        self.values = values

        # prepare digital waveform
        digitalWaveforms = pyabf.stimulus.digitalWaveformEpochs(abf)
        self.digital = digitalWaveforms[abf.sweepNumber]

if __name__ == "__main__":
    for fname in glob.glob(PATH_DATA+"/*.abf"):
        print(fname)
        abf = pyabf.ABF(fname)
        for sweep in range(min(3, abf.sweepCount)):
            abf.setSweep(sweep)
            epochs = Epoch(abf)
    print("DONE")
