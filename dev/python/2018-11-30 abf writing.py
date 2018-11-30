"""
test the new ABF writer module by loading an ABF2 file (voltage clamp sweeps
with a membrane test and spontaneous events) and saving it as an ABF1 file
then loading it in MiniAnalysis.
"""

import sys
import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
abf = pyabf.ABF(PATH_DATA+"/171116sh_0020.abf") 
abf.saveABF1(PATH_DATA+"/171116sh_0020_ABF1.abf")