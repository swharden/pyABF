"""
This code demonstrates how to perform measurements on small ranges of sweeps.
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

# now you are free to import additional modules
import glob


if __name__ == "__main__":

    allFiles = sorted(glob.glob(PATH_DATA+"/*.abf"))

    fnames = []
    # fnames.append(PATH_DATA+"/model_vc_step.abf")  # VC memtest
    fnames.append(PATH_DATA+"/17o05026_vc_stim.abf")  # VC opto
    # fnames.append(PATH_DATA+"/14o08011_ic_pair.abf")  # IC pair
    # fnames.append(PATH_DATA+"/171116sh_0012.abf")  # VC pair

    for fname in fnames:
        abf = pyabf.ABF(fname)
        print(abf.abfID)

        # define a baseline
        abf.baseline(1, 2)

        # define two marker regions
        m1a, m1b = 0.09, 0.12
        m2a, m2b = 0.30, 0.33

        # calculate the average of these regions
        avs1, ers1 = pyabf.calc.averageValue(abf, m1a, m1b, [0])
        avs2, ers2 = pyabf.calc.averageValue(abf, m2a, m2b, [0])

        # plot our analyzed data
        pyabf.plot.sweeps(abf, [0], color='k')
        plt.axvspan(m1a, m1b, color='b', alpha=.1)
        plt.axvspan(m2a, m2b, color='r', alpha=.1)
        plt.axhline(avs1[0], color='b', ls='--')
        plt.axhline(avs2[0], color='r', ls='--')
        plt.axis([0, .5, -80, 40])
        plt.show()

    print("DONE")
