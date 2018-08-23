"""
Code here makes it easy to glance at a header item from every demo ABF file.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

import glob

if __name__ == "__main__":
    abf = pyabf.ABF(PATH_DATA+"/18711001.abf")
    print(pyabf.sweep.rangeMax(abf))
    print(pyabf.sweep.rangeMin(abf))
