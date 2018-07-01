# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../../src/")  # for your IDE
import pyabf
import glob

import matplotlib.pyplot as plt

if __name__ == "__main__":
    abf = pyabf.ABF(PATH_DATA+"/171116sh_0013.abf")

    currents = pyabf.calc.averageValue(abf, .5, 1)
    voltages = abf.epochValues

    plt.figure(figsize = (8, 5))
    plt.grid(alpha=.5, ls='--')
    plt.plot(voltages, currents,'.-', ms=15)
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelC)
    plt.title(f"I/V Relationship of {abf.abfID}")
    plt.show()
    print("DONE")