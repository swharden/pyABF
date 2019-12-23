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
    raise ImportError("couldn't import local pyABF")

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
        # break # only read one ABF
    return abfinfos


ABFINFOS = abfInfoText()


def getFirstLineContaining(lines, keyLineStart):
    """
    Given a split abfinfo text, return a stripped value for the given key.
    """
    for line in lines:
        if line.startswith(keyLineStart):
            line = line.replace(keyLineStart, "")
            line = line.strip()
            return line
    return None


def datetimeFromABFtime(line):
    """
    Convert the abfinfo created string to a python datetime.
    """

    # clampfit doesn't use a standard date format, so do this manually
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
    us = int(milliseconds) * 1000

    return datetime.datetime(year, month, day, hours, minutes, seconds, us)


@pytest.mark.parametrize("abfID", ABFINFOS.keys())
def test_abfinfo_abfDateTime(abfID):

    # read the ABF header into memory
    abfFilePath = os.path.join(DATA_PATH, abfID+".abf")
    abf = pyabf.ABF(abfFilePath, loadData=False)

    # read the ABFINFO text into memory
    infoLines = ABFINFOS[abfID]

    # abfDateTime
    abfInfoDateTime = getFirstLineContaining(infoLines, "Created:")
    if abfInfoDateTime:
        abfInfoDateTime = datetimeFromABFtime(abfInfoDateTime)
        assert(abf.abfDateTime.year == abfInfoDateTime.year)
        assert(abf.abfDateTime.month == abfInfoDateTime.month)
        assert(abf.abfDateTime.day == abfInfoDateTime.day)
        assert(abf.abfDateTime.hour == abfInfoDateTime.hour)
        assert(abf.abfDateTime.minute == abfInfoDateTime.minute)
        assert(abf.abfDateTime.second == abfInfoDateTime.second)

    # abfFileComment
    abfInfoComment = getFirstLineContaining(infoLines, "Comment:")
    if abfInfoComment == 'n/a':
        abfInfoComment = ''
    if abfInfoComment:
        assert(abf.abfFileComment == abfInfoComment)

    # abfVersion
    infoVersion = getFirstLineContaining(infoLines, "File format: ABF V")

    if abf.abfVersion["major"] == 1:
        version = "%d.%d%d" % (
            abf.abfVersion["major"],
            abf.abfVersion["minor"],
            abf.abfVersion["bugfix"]
        )
        assert(infoVersion == version)

    elif abf.abfVersion["major"] == 2:
        version = "%d.%02d" % (
            abf.abfVersion["major"],
            abf.abfVersion["minor"]
        )
        assert(infoVersion == version)

    else:
        raise NotImplementedError()

    # channel count (verify this two ways)
    channelCount = getFirstLineContaining(infoLines, "nADCNumChannels =")
    channelCount = int(channelCount)
    assert (channelCount == abf.channelCount)

    channelMap = getFirstLineContaining(infoLines, "nADCChannel")
    channelMap = channelMap.split(" ")
    channelMap = [x for x in channelMap if x]
    assert (len(channelMap) == abf.channelCount)

    # creator version
    creator = getFirstLineContaining(infoLines, "Created by:")
    if creator != "clampex pre-9.0":
        assert (creator in abf.creator)

    # data dimensions
    for line in infoLines:
        if "samples in this file" in line:
            sampleCount = int(line.split(" ")[0])
    assert(sampleCount == abf.dataPointCount)

    # GUID
    abfInfoGUID = getFirstLineContaining(infoLines, "File GUID:")
    if abfInfoGUID:
        abfInfoGUID = abfInfoGUID[1:-2]
    assert(abf.fileGUID == abfInfoGUID)

    # protocol
    protocol = getFirstLineContaining(infoLines, "Protocol:")
    if protocol == "(untitled)":
        protocol = None
    if protocol:
        assert(protocol == abf.protocolPath)

    # tags
    tagCount = getFirstLineContaining(infoLines, "lNumTagEntries =")
    if tagCount:
        tagCount = int(tagCount)
        assert(tagCount == len(abf.tagTimesMin))
