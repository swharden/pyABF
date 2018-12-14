"""
Ensure no ABFs have empty sweepC arrays
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

if __name__=="__main__":
    abf = pyabf.ABF(PATH_DATA+"/05210017_vc_abf1.abf")
    for abfFile in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf=pyabf.ABF(abfFile)
        print(abf.abfID, abf.sweepC)