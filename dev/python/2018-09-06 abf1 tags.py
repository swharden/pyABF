"""
Test ABF1 tags
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    abf = pyabf.ABF(PATH_DATA+"/abf1_with_tags.abf")
    lNumTagEntries = abf._headerV1.lNumTagEntries
    print(f"lNumTagEntries: {lNumTagEntries}")
    lTagSectionPtr = abf._headerV1.lTagSectionPtr
    print(f"lTagSectionPtr: {lTagSectionPtr}")
    # Go there then read lTagTime (i) and sComment (56s)
    # Then offset by 64 bytes for each tag
    print(abf.tagComments)
    print(np.array(abf.tagTimesSec)/60)