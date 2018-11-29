"""
test to see if the same pyABF can be imported in Python 2.7 and 3.6
"""


import sys
import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

print("PYTHON %d.%d"%(sys.version_info.major, sys.version_info.minor))
import pyabf
abf = pyabf.ABF(PATH_DATA+"/model_vc_step.abf")
print(abf.sweepY)