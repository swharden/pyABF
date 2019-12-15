"""
Simulate creating old GUIDs from new onew
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf

def oldIncorrectGUID(GUID):
    """Simulate the old (broken) GUID from the current GUID."""
    print("NEW FORMAT (correct):    " + GUID)
    oldGUID = list(GUID)
    oldGUID[-4:-2] = oldGUID[-2:]
    oldGUID = "{" + "".join(oldGUID) + "}"
    print("OLD FORMAT (incorrect): " + oldGUID)

if __name__=="__main__":
    abf = pyabf.ABF(PATH_DATA+"/17o05028_ic_steps.abf")
    oldIncorrectGUID(abf.fileGUID)