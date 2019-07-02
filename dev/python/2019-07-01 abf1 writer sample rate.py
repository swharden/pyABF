"""
Allow custom sample rate when writing ABF1 files
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf

if __name__ == "__main__":
    abfFile = PATH_DATA + "/14o08011_ic_pair.abf"

    abf = pyabf.ABF(abfFile)
    print(abf)

    # demo saving at 5kHz
    abf.saveABF1(R"C:\Users\scott\Documents\temp\test.atf", 5000)
    print("DONE")
