"""
See how fast just the protocol can be read from ABF files
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import time

demoAbf2File = R"X:\Data\C57\Tat project\abfs-intrinsics\2018_07_24_DIC1_0000.abf";
timeStart = time.time()
benchmarkRepeats = 1000
for i in range(benchmarkRepeats):
    abf = pyabf.ABF(demoAbf2File, loadData=False)
    protocol = abf.protocol
timeElapsed = time.time() - timeStart
print(f"Reading full header from {benchmarkRepeats} ABF files with pyABF took {timeElapsed} sec")