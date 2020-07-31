"""
This script tests files with external trigger tags
"""

import glob
import os
import sys
import matplotlib.pyplot as plt

try:
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
    PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
    DATA_FOLDER = os.path.join(PATH_SRC, "../data/abfs/")
    sys.path.insert(0, PATH_SRC)
    import pyabf
except:
    raise EnvironmentError()


if __name__ == "__main__":
    abf = pyabf.ABF(DATA_FOLDER+"/2020_07_29_0062.abf")

    plt.figure(figsize=(10, 4))
    plt.plot(abf.sweepX, abf.sweepY, lw=.5)

    for tagIndex, tagTimeSec in enumerate(abf.tagTimesSec):
        print(f"tag '{abf.tagComments[tagIndex]}' at {tagTimeSec} sec")
        plt.axvline(tagTimeSec, color='r', ls=':')

    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.title(abf.abfID)
    plt.margins(0, .05)
    plt.tight_layout()
    plt.show()
