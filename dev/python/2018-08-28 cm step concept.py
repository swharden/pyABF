"""
Demonstrate how to calculate Cm from a ramp protocol.

INPUT:
    model_vc_ramp.abf is from Patch-1U Model Cell (33 pF +/- 10%)

OUTPUT:
    model_vc_ramp as a capacitance of 30.88 +/- 0.20 pF
    171116sh_0014 as a capacitance of 202.32 +/- 11.49 pF
    2018_08_23_0009 as a capacitance of 170.90 +/- 13.54 pF
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
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def cm_step_valuesBySweep(abf):
    """
    return an array of membrane capacitance values calculated from the step 
    found in every sweep in the abf.
    """
    assert isinstance(abf, pyabf.ABF)
    cms = np.full(abf.sweepCount, np.nan)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        cms[sweepNumber] = _cm_step_fromThisSweep(abf)
    log.info(f"%s has a capacitance of %.02f +/- %.02f pF" %
             (abf.abfID, np.mean(cms), np.std(cms)))
    return cms


def _cm_step_fromThisSweep(abf):
    assert isinstance(abf, pyabf.ABF)
    return


if __name__ == "__main__":
    abfFilesToTest = []
    abfFilesToTest.append(PATH_DATA+"/model_vc_step.abf")
    abfFilesToTest.append(PATH_DATA+"/171116sh_0011.abf")
    abfFilesToTest.append(PATH_DATA+"/18808025.abf")
    abfFilesToTest.append(PATH_DATA+"/2018_08_23_0009.abf")
    for abfFile in abfFilesToTest:
        abf = pyabf.ABF(abfFile)
        cm_step_valuesBySweep(abf)
        break
