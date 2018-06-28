"""
Comparing version numbers
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

    assert pyabf.versionAtLeast('1.0.0')
    assert pyabf.versionAtLeast('1.0.1')
    assert pyabf.versionAtLeast('2.0.0')
    assert pyabf.versionAtLeast('2.0.1')
    assert pyabf.versionAtLeast('2.0.2')
    assert pyabf.versionAtLeast('3.0.0')
    assert pyabf.versionAtLeast('3.0.1')

    print("DONE")