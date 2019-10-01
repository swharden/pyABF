"""
Try to figure out how to read file creation date/time from ABF1 files.

19122043.abf according to ABFInfo:
    Created: Jan 22, 2019, at 22:22:10.750 [10:56:42]
    File GUID: {EA774D20-4346-4219-ACCF-DB3B6DD89ABD}
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
import datetime

if __name__=="__main__":
    abf = pyabf.ABF(PATH_DATA+"/19122043.abf")
    print(f"lFileStartTime: {abf._headerV1.lFileStartTime}")
    print(f"lFileStartDate: {abf._headerV1.lFileStartDate}")
    print(f"abfDateTime: {abf.abfDateTime}")
    print(f"fileGUID: {abf.fileGUID}")