"""
binary crap keeps ending up parsed as a string. fix this.
"""

import sys
import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
import glob

for abfFile in glob.glob(PATH_DATA+"/*.abf"):
    abf = pyabf.ABF(abfFile) 
    print(abf.abfID, abf.protocolPath)