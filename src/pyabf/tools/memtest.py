"""
Code here relates to the detection and management of cell membrane properties:
  * holding current (Ih)
  * access resistance (Ra)
  * membrane resistance (Rm)
  * membrane capacitance (Cm)

This modules provides two types of membrane capacitance values: ones derived
from step protocols and ones derived from ramp protocols.

This URL has useful discussion and code for calculating membrane properties:
https://swharden.com/blog/2020-10-11-model-neuron-ltspice
"""

import pyabf
import pyabf.tools.sweep
import pyabf.tools.memtestMath
import numpy as np
import warnings

warnings.warn("The pyabf package is designed for reading ABF files (not analyzing them). " +
              "This module is experimental, provided only for backwards compatibility, and its API may change in future releases. " +
              "Users are encouraged to write their own ABF analysis code.")


class Memtest:
    def __init__(self, abf: pyabf.ABF, channel: int = 0):
        """
        This object contains passive cell membrane properties calculated from 
        each sweep an episodic protocol containing a voltage-clamp step.

        WARNING: These calculations are not optimized for speed or accuracy. 
        This module is experimental and included only for backward compatibility
        purposes. Users are highly encouraged to write their own analysis code.
        """
        assert isinstance(abf, pyabf.ABF)

        self.sweepCount = abf.sweepCount
        self.TimeSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
        self.TimeMin = self.TimeSec / 60.0

        Result = pyabf.tools.sweep.SweepMeasurement
        self.Ih = Result(abf.sweepCount, "Holding Current", "Ih", "pA")
        self.Rm = Result(abf.sweepCount, "Membrane Resistance", "Rm", "MOhm")
        self.Ra = Result(abf.sweepCount, "Access Resistance", "Ra", "MOhm")
        self.CmStep = Result(abf.sweepCount, "Capacitance (Step)", "Cm", "pF")
        self.CmRamp = Result(abf.sweepCount, "Capacitance (Ramp)", "Cm", "pF")

        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber, channel)

            # square step memtest
            Ih, Rm, Ra, CmStep = pyabf.tools.memtestMath.currentSweepStep(abf)
            self.Ih.values[sweepNumber] = Ih
            self.Rm.values[sweepNumber] = Rm
            self.Ra.values[sweepNumber] = Ra
            self.CmStep.values[sweepNumber] = CmStep

            # ramp memtest
            CmRamp = pyabf.tools.memtestMath.currentSweepRamp(abf)
            self.CmRamp.values[sweepNumber] = CmRamp

    @property
    def summary(self):
        msg = ""
        for item in [self.Ih, self.Rm, self.Ra, self.CmStep, self.CmRamp]:
            msg += f"%s: %.03f +/- %.03f %s\n" % (
                item.name, item.mean, item.stdErr, item.units)
        return msg.strip()

    def __repr__(self):
        return(f"Memtest results for {self.sweepCount} sweeps")
