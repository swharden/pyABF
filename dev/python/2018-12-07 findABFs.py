"""
Demonstrate how to rapidly search thousands of ABFs to find one with
some specific header values. Notice the use of preLoadData=False to
make the ABF reading header-only and therefore extremely highspeed.

A few benchmark tests over the network drive demonstrated ABFs load
at a rate of about 3.23 ms per ABF. ABF2 files are a little slower,
but this is still fantastic. Headers can be read at a rate of about
300 ABFs per second.
"""
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob
import time

def findABFsOnXdrive(rig="DIC3", year="2016"):
    abfFiles = []
    for folderMonth in glob.glob(R"X:\Data\%s\%s\*" % (rig, year)):
        if os.path.isfile(folderMonth):
            continue
        for folderDay in glob.glob(folderMonth+"/*"):
            if os.path.isfile(folderDay):
                continue
            for abfFilePath in glob.glob(folderDay+"/*.abf"):
                abfFiles.append(abfFilePath)
    print("rig %s year %s had %d ABFs" % (rig, year, len(abfFiles)))
    return abfFiles

abfFiles = []
abfFiles += findABFsOnXdrive("DIC3", "2015")
abfFiles += findABFsOnXdrive("DIC3", "2016")
abfFiles += findABFsOnXdrive("DIC3", "2017")
abfFiles += findABFsOnXdrive("DIC3", "2018")
print("found %d total ABFs" % len(abfFiles))

# find a multi-channel ABF with comments
for i, abfFilePath in enumerate(abfFiles):
    abf = pyabf.ABF(abfFilePath, False)    
    if abf.channelCount>1 and len(abf.tagComments)>0:
        print(abf.adcUnits, abf.abfFilePath, abf.tagComments)
