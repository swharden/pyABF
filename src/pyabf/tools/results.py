"""
This data transfer object represents a single metric measured once per sweep.
This is intended to be used for by-sweep means for memtest and event detection.
"""

import numpy as np


class SweepMeasurement:
    def __init__(self, sweepCount, name, abbreviation, units):
        self.values = np.empty(sweepCount)
        self.name = name
        self.abbreviation = abbreviation
        self.units = units

    @property
    def valuesReal(self):
        return self.values[~np.isnan(self.values)]

    @property
    def mean(self):
        if len(self.valuesReal):
            return np.mean(self.valuesReal)
        else:
            return np.nan

    @property
    def stdev(self):
        if len(self.valuesReal):
            return np.std(self.valuesReal)
        else:
            return np.nan

    @property
    def stdErr(self):
        if len(self.valuesReal):
            return np.std(self.valuesReal)/np.sqrt(len(self.valuesReal))
        else:
            return np.nan

    def __repr__(self):
        return "mean %s (%s) of %f %s" % (
            self.name, self.abbreviation, self.mean, self.units)
