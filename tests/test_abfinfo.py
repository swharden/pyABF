"""
abfinfo.exe was used to create a few text documents of header information.
These tests compare header values from pyABF vs those in the text documents.
"""

import sys
import pytest
import glob
import os
import datetime

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
def test_abfinfo_abfDateTime(abfID):

    # look up value from abfinfo text
    abfInfoLines = ABFINFOS[abfID]
    for line in abfInfoLines:
        if line.startswith("Created: "):
            # clampfit doesn't use a standard date format, so do this manually
            line = line.split(":", 1)[1]
            line = line.split("[")[0]
            line = line.strip()
            line = line.replace(",", " ")
            dateParts = line.split(" ")
            dateParts = [x for x in dateParts if len(x)]

            month = int(datetime.datetime.strptime(dateParts[0], '%b').month)
            day = int(dateParts[1])
            year = int(dateParts[2])

            # Notice that ABFFIO/ClampFit/ABFINFO has a bug that removes 
            # left-padded zeros after the decimal point seconds (DOH!)

            timestamp = dateParts[4].replace(".", ":")
            hours, minutes, seconds, milliseconds = timestamp.split(":")
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            milliseconds = int(milliseconds)
            microseconds = milliseconds * 1000
            
            abfinfoDateTime = datetime.datetime(
                year, month, day, hours,
                minutes, seconds, microseconds
            )

            break

    # compare to value from pyABF
    abfFilePath = os.path.join(DATA_PATH, abfID+".abf")
    abf = pyabf.ABF(abfFilePath, loadData=False)

    # ignore microseconds in Python2
    if sys.version_info[0] == 2:
        abfinfoDateTime.microsecond = 0

    assert(abf.abfDateTime == abfinfoDateTime)


# NEED TEST FOR: abfVersionString = 2.6.0.0
# NEED TEST FOR: channelCount = 2
# NEED TEST FOR: creatorVersionString = 10.7.0.3
# NEED TEST FOR: dataByteStart = 6656
# NEED TEST FOR: dataLengthMin = 0.06666666666666667
# NEED TEST FOR: dataLengthSec = 4.0
# NEED TEST FOR: dataPointByteSize = 2
# NEED TEST FOR: dataPointCount = 120000
# NEED TEST FOR: dataPointsPerMs = 20
# NEED TEST FOR: dataRate = 20000
# NEED TEST FOR: dataSecPerPoint = 5e-05

@pytest.mark.parametrize("abfID", ABFINFOS.keys())
def test_abfinfo_fileGUID(abfID):

    # look up value from abfinfo text
    abfInfoLines = ABFINFOS[abfID]
    for line in abfInfoLines:
        if "GUID" in line:
            abfinfoGUID = line.split("{")[1].split("}")[0]
            break

    # read GUID using pyABF
    abfFilePath = os.path.join(DATA_PATH, abfID+".abf")
    abf = pyabf.ABF(abfFilePath, loadData=False)
    assert(abf.fileGUID == abfinfoGUID)

# NEED TEST FOR: holdingCommand = [-70.0, -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# NEED TEST FOR: protocolPath = S:\Protocols\permanent\0112 steps dual -50 to 150 step 10.pro
# NEED TEST FOR: sweepIntervalSec = 1.0
# NEED TEST FOR: sweepLengthSec = 1.0
# NEED TEST FOR: sweepPointCount = 20000
