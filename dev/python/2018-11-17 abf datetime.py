"""
See how the datetime string looks for every ABF file
"""

import os
import sys
import glob
import time
import numpy as np

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

if __name__=="__main__":
    for abfFileName in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFileName)
        print(abf.abfDateTimeString)