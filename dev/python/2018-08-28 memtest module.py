"""
demonstrate how to use the new pyabf.memtest module
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

if __name__=="__main__":
    modelRamp = PATH_DATA+"/model_vc_ramp.abf"
    modelStep = PATH_DATA+"/model_vc_step.abf"

    abf=pyabf.ABF(modelRamp)
    print(pyabf.memtest.cm_ramp_summary(abf))

    abf=pyabf.ABF(modelStep)
    print(pyabf.memtest.step_summary(abf))

    print("DONE")