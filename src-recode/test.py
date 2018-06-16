import os
import glob
import numpy as np

import pyabf
pyabf.info()

thisFolder = os.path.abspath(os.path.dirname(__file__))
dataFolder = thisFolder+"/../data/*.abf"
dataFolder = os.path.abspath(dataFolder)

if __name__ == "__main__":
    for abfFileName in sorted(glob.glob(dataFolder)):
        abf = pyabf.ABF(abfFileName)
        print(os.path.basename(abfFileName), np.average(abf.data,axis=1))