"""
ABF1 epoch holding levels seem broken. Fix them.
https://github.com/swharden/pyABF/issues/52
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
    print("Ch1 hold\tABF ID", )
    for abfFilePath in glob.glob(PATH_DATA+"/*.abf"):
        abf=pyabf.ABF(abfFilePath)
        print("%.02f\t\t%s"%(abf.holdingCommand[0],abf.abfID))