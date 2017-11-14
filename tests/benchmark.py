"""
Code here relates to benchmarking how long certain ABF-reading/calculating processes take.

Example Output:
    
    Test file open/read/close speed (10000 repetitions) ...
     file signature: b'ABF2'
     completed in 651.305 ms (65.130 us each)
    
    Test loading all ABF data (100 repetitions) ...
     read 7480000 data points per repetition
     completed in 715.377 ms (7.154 ms each)
    
    Test loading all ABF data (100 repetitions) ...
     read 7480000 data points per repetition
     scaling was applied: 0.032768
     completed in 2004.033 ms (20.040 ms each)
    
    Test loading all ABF data (100 repetitions) ...
     read 7480000 data points per repetition
     scaling was applied: 0.032768
     average was calculated: 7.80652
     completed in 2516.918 ms (25.169 ms each)

"""

import time
import sys
sys.path.append('../src/')
import pyabf
import numpy as np

def fileOpenClose(abfFileName,repetitions=10000):
    """
    Time how long it takes to open the file, read the first 4 bytes, then close it.
    """
    print("\nTest file open/read/close speed (%d repetitions) ..."%repetitions)
    t1=time.perf_counter()
    for repetition in range(repetitions):
        f=open(abfFileName,'rb')
        signature=f.read(4)
        f.close()
    timeTotal=time.perf_counter()-t1
    timeEach=timeTotal/repetitions
    print(" file signature:",signature)
    print(" completed in %.03f ms (%.3f us each)"%(timeTotal*1e3,timeEach*1e6))
    return

def loadData(abfFileName,repetitions=100,scale=False,average=False):
    """
    Time how long it takes to just read all data from an ABF.
    Reading additional header information (i.e., scaling factor) is not timed in this test.
    Optionally applt scaling factor. Optionally average all data.
    """
    print("\nTest loading all ABF data (%d repetitions) ..."%repetitions)
    
    # get header data using the easy way (ABFheader class)
    abf = pyabf.header.ABFheader(abfFileName)
    byteStart = abf.header['dataByteStart']
    pointCount = abf.header['DataSection'][2]
    scaleFactor = abf.header['lADCResolution'] / 1e6
    
    # Use numpy directly (not the ABFheader class) to pull data right from the file and scale it
    f=open(abfFileName,'rb')
    t1=time.perf_counter()
    for repetition in range(repetitions):
        f.seek(byteStart)
        data = np.fromfile(f, dtype=np.int16, count=pointCount)
        if scale:
            data = np.multiply(data,scaleFactor,dtype='float32')
        if average:
            averageToo=np.mean(data)
    timeTotal=time.perf_counter()-t1
    timeEach=timeTotal/repetitions
    f.close()
    
    print(" read %d data points per repetition"%(len(data)))
    if scale:
        print(" scaling was applied:",scaleFactor)
    if average:
        print(" average was calculated:",averageToo)
    print(" completed in %.03f ms (%.3f ms each)"%(timeTotal*1e3,timeEach*1e3))
    return

if __name__=="__main__":
    abfFileName="../data/16d05007_vc_tags.abf"
    fileOpenClose(abfFileName)
    loadData(abfFileName)
    loadData(abfFileName,scale=True)
    loadData(abfFileName,scale=True,average=True)
    print("\nDONE")