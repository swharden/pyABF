"""
Add a top level method to the ABF class to simplify access to the headers 
"""

import sys
import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
abf = pyabf.ABF(PATH_DATA+"/model_vc_step.abf")

# old way
#abf.getInfoPage().showText()

print(abf.headerText)
abf.headerLaunch()