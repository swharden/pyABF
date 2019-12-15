"""
This script places .abfinfo files next to .abf files in the data folder.
Abfinfo dumps don't contain the filename so GUIDs are used to match them up.
"""

import glob
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf

DATA_FOLDER = os.path.abspath("../../data/abfs/")


ABF_GUIDS = {}
for abfPath in glob.glob(DATA_FOLDER+"/*.abf"):
    abf = pyabf.ABF(abfPath, loadData=False)
    guid = abf.fileGUID
    if (guid != "00000000-0000-0000-0000-000000000000"):
        ABF_GUIDS[guid] = os.path.abspath(abfPath)


def guidFromInfo(text):
    abfInfoLines = text.split("\n")
    for line in abfInfoLines:
        if "GUID" in line:
            if "Not set" in line:
                return None
            else:
                guid = line.split("{")[1].split("}")[0]
                return guid


with open("2019-12-16 all.abfinfo") as f:
    raw = f.read()
    infos2 = raw.split("Protocol:")
    infos2 = ["Protocol:"+x for x in infos2][1:]
    infos = []
    for info in infos2:
        if info.count("Data File:") == 1:
            infos.append(info)
        elif info.count("Data File:") == 2:
            infoAA, infoAB, infoB = info.split("Data File:")
            infoA = infoAA+"Data File:"+infoAB
            infoB = "Data File:"+infoB
            infos.append(infoA)
            infos.append(infoB)
        else:
            raise NotImplementedError()
    infos = [x.strip() for x in infos]

    for info in infos:
        guid = guidFromInfo(info)
        if guid in ABF_GUIDS.keys():
            fname = ABF_GUIDS[guid][:-4]+".abfinfo"
            print(guid, fname)
            with open(fname, 'w') as f:
                f.write(info)

print("DONE")
