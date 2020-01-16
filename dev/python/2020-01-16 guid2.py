"""
Invent a better (truly unique) GUID system
"""

import glob
import os
import sys
import matplotlib.pyplot as plt

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
    guids = []
    guidAndIDs = []
    for abfFilePath in glob.glob(DATA_FOLDER + "/*.abf"):
        abf = pyabf.ABF(abfFilePath)
        guidAndIDs.append([abf.fileGUID, abf.abfID])
        guids.append(abf.fileGUID)

    duplicates = 0
    for guid, abfID in sorted(guidAndIDs):
        if guids.count(guid) > 1:
            print(f"{guid} DUPLICATE! {abfID}.abf")
            duplicates += 1
        else:
            print(f"{guid}  (unique)  {abfID}.abf")

    print(f"Found {duplicates} duplicates out of {len(guidAndIDs)} ABFs")
