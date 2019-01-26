"""
The memtest tool broke in the transition from pyABF v1 to v2.
This script tries to bring back its functionality.

ABFs were recorded on a Patch-1U Model Cell (https://goo.gl/sCWEhT).
Note that recordings were made with a hardware Bessel filter enabled at 2kHz.

Values calculated from a square pulse (model_vc_step):
    Ih = -139.31 +/- 0.14 pA
    Rm = 511.62 +/- 3.13 MOhm (expected within 1% of 500 MOhm)
    Ra = 14.88 +/- 0.08 MOhm
    Cm = 23.34 +/- 0.05 pF (expected within 10% of 33 pF)

Values calculated from a ramp pulse (model_vc_ramp)"
    Cm = -30.88 +/- 0.20 pF (expected within 10% of 33 pF)
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt

import pyabf
import pyabf.tools.memtest

if __name__=="__main__":
    
    print("\nMODEL CELL: SQUARE PULSE")
    abfFilePath = os.path.join(PATH_DATA, "model_vc_step.abf")
    abf=pyabf.ABF(abfFilePath)
    print(pyabf.tools.memtest.step_summary(abf))

    print("\nMODEL CELL: VOLTAGE RAMP")
    abfFilePath = os.path.join(PATH_DATA, "model_vc_ramp.abf")
    abf=pyabf.ABF(abfFilePath)
    print(pyabf.tools.memtest.cm_ramp_summary(abf))