"""
demonstrate datetime objects
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
    abf=pyabf.ABF(PATH_DATA+"/05210017_vc_abf1.abf")
    print(type(abf.abfDateTime), abf.abfDateTime)
    print(type(abf.abfDateTimeString), abf.abfDateTimeString)

    print("DONE")