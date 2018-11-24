"""
I got an email indicating this ABF wouldn't load properly.
It seems to be a gap-free protocol, but is being loaded as >1000 sweeps!
This ABF demonstrated the problem and the issue was fixed.
"""

import os
import sys
import glob
import time
import numpy as np
import matplotlib.pyplot as plt

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

if __name__=="__main__":
    abf = pyabf.ABF(PATH_DATA+"/sample trace_0054.abf")
    plt.plot(abf.sweepX, abf.sweepY)
    plt.show()
    print(abf)