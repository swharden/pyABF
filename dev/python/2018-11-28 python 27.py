"""
test to see what can be imported in python 2.7
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

print("importing special pyabf2")
import pyabf2
abf = pyabf2.ABF(PATH_DATA+"/model_vc_step.abf")
print(abf.sweepY)

print("DONE")