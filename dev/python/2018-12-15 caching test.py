"""
Demonstrate how ABF and ATF stimulus files can be automatically cached.

This script will dobule as a test to ensure this functionality does not break
as the stimulus module is refactored. This test tests caching of both ABF and
ATF files as stimulus waveforms.

SAMPLE OUTPUT:
    sine sweep magnitude 20.abf loaded in 1.92 ms
    sine sweep magnitude 20.atf loaded in 259.86 ms
    sine sweep magnitude 20.abf loaded in 0.20 ms
    sine sweep magnitude 20.atf loaded in 0.21 ms
    sine sweep magnitude 20.abf loaded in 0.23 ms
    sine sweep magnitude 20.atf loaded in 0.22 ms
    sine sweep magnitude 20.abf loaded in 0.20 ms
    sine sweep magnitude 20.atf loaded in 0.21 ms
    sine sweep magnitude 20.abf loaded in 0.25 ms
    sine sweep magnitude 20.atf loaded in 0.20 ms
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

#import logging
#pyabf.stimulus.log.setLevel(logging.DEBUG)

import shutil
import glob
import time

testDirectory = R"C:\Users\scott\Documents\temp"
testDirectory = os.path.abspath(testDirectory)
assert os.path.exists(testDirectory)

def setup_test_directory():
    """Create many ABF files which use ABF and ATF waveforms."""
    print("deleting old ABFs...")
    for fname in glob.glob(os.path.join(testDirectory, "cool_*.abf")):
            os.remove(fname)
    print("copying ABFs...")
    for i in range(5):
        fnameABF = os.path.join(PATH_DATA, "171116sh_0015.abf")
        fnameATF = os.path.join(PATH_DATA, "171116sh_0015-ATFwaveform.abf")
        fname2ABF = os.path.join(testDirectory, "cool_%03d.abf"%(i*2+0))
        fname2ATF = os.path.join(testDirectory, "cool_%03d.abf"%(i*2+1))
        shutil.copy(fnameABF, fname2ABF)
        shutil.copy(fnameATF, fname2ATF)

def test_stimulus_cache(useCache=True):
    """Load ABFs which use an external ABF and ATF stimulus files"""
    abfFiles = sorted(glob.glob(testDirectory+"/cool_*.abf"))
    for i, filename in enumerate(abfFiles):
        #abf = pyabf.ABF(filename, cacheStimulusFiles=False)
        abf = pyabf.ABF(filename)
        abf.stimulusFileFolder = PATH_DATA # alternate path for stimulus files
        t1 = time.perf_counter()
        sweepC = abf.sweepC # stimulus file is only read if this is accessed
        t2 = time.perf_counter()
        stimFile = os.path.basename(abf._stringsIndexed.lDACFilePath[0])
        timeMs = (t2 - t1)*1000.0
        print('"%s" loaded in %.02f ms'%(stimFile, timeMs), sweepC)

def test_stimulus_cache_old():
        """Test warning if access using old methods"""
        abfFiles = sorted(glob.glob(testDirectory+"/cool_*.abf"))
        abf = pyabf.ABF(abfFiles[0])
        print(abf.stimulusByChannel[0].protocolStorageDir)
        abf.stimulusByChannel[0].protocolStorageDir = PATH_DATA

if __name__=="__main__":
    setup_test_directory()
    test_stimulus_cache_old()
    test_stimulus_cache()
    print("DONE")