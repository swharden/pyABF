"""
This code demonstrates how to access tags in ABF files
"""

# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../src/")  # for your IDE
import pyabf
pyabf.info()
import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')  # alternative color scheme

if __name__ == "__main__":

    # plot the first file
    abf = pyabf.ABF(PATH_DATA+"/2018_04_13_0016a_original.abf")
    abf.setSweep(sweepNumber=0, channel=1)
    plt.plot(abf.sweepX, abf.sweepY, label="original ABF")

    # plot the second file on top of it
    abf = pyabf.ABF(PATH_DATA+"/2018_04_13_0016b_modified.abf")
    abf.setSweep(sweepNumber=0, channel=1)
    mult = -(1/3)
    plt.plot(abf.sweepX, abf.sweepY * mult, label="modified ABF")

    # decorate the plot and zoom to an interesting area
    plt.title("2018_04_13_0016 inspection (pyABF v2)")
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.legend()
    plt.axis([.005,.015,-150,350])
    plt.show()

    print("DONE")
