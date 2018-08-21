

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../")
PATH_SRC = os.path.abspath(PATH_PROJECT+"/src/")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
import logging
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)
sys.path.insert(0, PATH_SRC)
import pyabf

def closeEnough(val1,val2,percentErrorAllowed=0.1):
    """
    Return True if the two values are within a certain percent of each other
    """
    avg = (val1+val2)/2
    diff = abs(val1-val2)
    err = abs(100*diff/avg)
    if err<=percentErrorAllowed:
        log.debug("%s == %s (error: %.02f%%)" %(val1, val2, err))
        return True
    else:
        log.debug("%s != %s (error: %.02f%%)" %(val1, val2, err))
        return False

def test_sweepStats_measureAverage(abf): 
    """Verified using statistics tab in ClampFit."""
    m1, m2 = 1, 2   
    assert closeEnough(abf.measureAverage(m1, m2), -52.2538)
    
def test_sweepStats_measureStdev(abf): 
    """Verified using statistics tab in ClampFit."""
    m1, m2 = 1, 2   
    assert closeEnough(abf.measureStdev(m1, m2), 0.559542)
    
def test_sweepStats_measureStdErr(abf): 
    """Verified using statistics tab in ClampFit."""
    m1, m2 = 1, 2   
    assert closeEnough(abf.measureStdErr(m1, m2), 0.005595)
    
def test_sweepStats_measureArea(abf): 
    """Verified using statistics tab in ClampFit."""
    m1, m2 = 1, 2   
    assert closeEnough(abf.measureArea(m1, m2), -52259.2)

def go():
    print("Testing statistics module ", end="")

    fname = os.path.abspath(PATH_DATA+"/14o08011_ic_pair.abf")
    abf = pyabf.ABF(fname)
    abf.setSweep(sweepNumber=1, channel=1)
    
    for functionName in sorted(globals()):
        if not functionName.startswith("test_"):
            continue
        log.debug("Running %s"%functionName)
        globals()[functionName](abf)
        print(".", end="")
        sys.stdout.flush()
    
    print(" OK")

if __name__ == "__main__":
    go()
