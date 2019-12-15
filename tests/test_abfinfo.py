"""
abfinfo.exe was used to create a few text documents of header information.
These tests compare header values from pyABF vs those in the text documents.
"""

import sys
import pytest
import glob
import os

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
except:
    pass

DATA_PATH = os.path.abspath("data/abfs")


def abfInfoText():
    """Return a dictioinary of abfinfo text keyed by abfID"""
    abfinfos = {}
    dataFiles = os.listdir(DATA_PATH)
    abfinfoFiles = [x for x in dataFiles if x.endswith(".abfinfo")]
    for abfInfoFile in abfinfoFiles:
        abfFile = abfInfoFile.replace(".abfinfo", ".abf")
        abfID = os.path.basename(abfInfoFile.replace(".abfinfo", ""))
        if (abfFile in dataFiles):
            with open(os.path.join(DATA_PATH, abfInfoFile)) as f:
                abfinfos[abfID] = f.readlines()
    return abfinfos


ABFINFOS = abfInfoText()


@pytest.mark.parametrize("abfID", ABFINFOS.keys())
def test_abfinfo_GUID(abfID):

    # look up GUID from abfinfo text
    abfInfoLines = ABFINFOS[abfID]
    for line in abfInfoLines:
        if "GUID" in line:
            abfinfoGUID = line.split("{")[1].split("}")[0]
            abfinfoGUID = "{"+abfinfoGUID+"}"

    # read GUID using pyABF
    abfFilePath = os.path.join(DATA_PATH, abfID+".abf")
    abf = pyabf.ABF(abfFilePath)
    assert(abf.fileGUID == abfinfoGUID)
