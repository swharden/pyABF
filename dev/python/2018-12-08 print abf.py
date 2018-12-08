"""
See what happens if you print(abf) for every ABF in the data folder
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
    for abfFile in glob.glob(PATH_DATA+"/*.abf"):
        abf=pyabf.ABF(abfFile)
        print(abf)