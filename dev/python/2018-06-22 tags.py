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

    fname = PATH_DATA+"/16d05007_vc_tags.abf"

    abf = pyabf.ABF(fname)
    print(abf.abfID)
    print(abf.tagComments)
    print(abf.tagSweeps)
    print(abf.tagTimesSec)
    print(abf.tagTimesMin)

    print("DONE")
