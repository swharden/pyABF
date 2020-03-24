"""
Invent a better (truly unique) GUID system
"""

import glob
import os
import sys
import matplotlib.pyplot as plt
import uuid
import datetime
import time
import hashlib

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

    print("ABF | User List")
    print("----|----------")
    for abfFilePath in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFilePath)
        if (abf.userList):
            print(f"{abf.abfID}|`{abf.userList}`")
