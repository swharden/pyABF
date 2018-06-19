"""
Example code demonstrating how to interact with the pyabf.ABF object
"""

# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../src/")  # for your IDE
import pyabf
pyabf.info()
import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')  # alternative color scheme

# now you are free to import additional modules
import glob

if __name__ == "__main__":

    allFiles = sorted(glob.glob(PATH_DATA+"/*.abf"))

    fnames = []
    fnames.append(PATH_DATA+"/model_vc_step.abf")  # VC memtest
    fnames.append(PATH_DATA+"/17o05026_vc_stim.abf")  # VC opto
    fnames.append(PATH_DATA+"/14o08011_ic_pair.abf")  # IC pair
    fnames.append(PATH_DATA+"/171116sh_0012.abf")  # VC pair

    outFolder = R"C:\Users\scott\Documents\temp"

    for fname in fnames:
        abf = pyabf.ABF(fname)
        print(abf.abfID)

    print("DONE")
