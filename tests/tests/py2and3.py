"""
This script will test to ensure Python 2.7 and Python 3.6+ are supported.
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