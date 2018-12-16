"""
I moved around the info page module. Ensure it still works.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob

if __name__=="__main__":
    for abfFile in sorted(glob.glob(PATH_DATA+"/*.abf")):
        print(abfFile)
        abf=pyabf.ABF(abfFile)
        print(len(abf.headerHTML))