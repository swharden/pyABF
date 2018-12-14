"""
Try to support abf.headerText in Python 2
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
    abf=pyabf.ABF(PATH_DATA+"/18425108.abf")
    print(abf)
    print(abf.headerText)
    abf.headerLaunch()