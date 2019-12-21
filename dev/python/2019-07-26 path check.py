import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf

if __name__ == "__main__":
    abf = pyabf.ABF(
        abfFilePath=PATH_DATA+"/H19_29_150_11_21_01_0011.abf",
        stimulusFileFolder="/somewhere/special"
    )
    print(abf.sweepC)
