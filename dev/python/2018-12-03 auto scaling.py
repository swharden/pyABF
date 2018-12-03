"""
Previously the ABF writer used fixed scaling factors.
Practice auto-scaling based on the ABF data.
"""

import sys
import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf

abf = pyabf.ABF(PATH_DATA+"/171116sh_0020.abf") 
abf.saveABF1(PATH_DATA+"/171116sh_0020_saved.abf")

abf = pyabf.ABF(PATH_DATA+"/f1.abf") 
abf.saveABF1(PATH_DATA+"/f1_saved.abf")