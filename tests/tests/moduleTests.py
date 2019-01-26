"""
Test misc things like epoch generation, statistics, membrane tests, etc.
Tests here focus mostly on challenging add-on modules.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
sys.path.insert(0, PATH_PROJECT+"/src/")
import pyabf
import pyabf.tools.memtest
import glob
import numpy as np

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def closeEnough(val1, val2, percentErrorAllowed=0.1):
    """
    Return True if the two values are within a certain percent of each other
    """
    avg = (val1+val2)/2
    diff = abs(val1-val2)
    err = abs(100*diff/avg)
    if err <= percentErrorAllowed:
        log.debug("%s == %s (error: %.02f%%)" % (val1, val2, err))
        return True
    else:
        log.debug("%s != %s (error: %.02f%%)" % (val1, val2, err))
        return False

def test_cm_ramp_withmemtest(abf):
    """Measure Cm (using step/ramp protocol) of a small cell."""
    abf = pyabf.ABF(PATH_DATA+"/2018_08_23_0009.abf")
    cms = pyabf.tools.memtest.cm_ramp_valuesBySweep(abf)
    assert closeEnough(np.mean(cms), 170.899298429)


def test_memtest_step_withramp(abf):
    """Measure memtest (using step/ramp 2018_08_23_0009) of a small cell."""
    abf = pyabf.ABF(PATH_DATA+"/2018_08_23_0009.abf")
    Ihs, Rms, Ras, Cms = pyabf.tools.memtest.step_valuesBySweep(abf)
    assert closeEnough(np.mean(Ihs), -134.723966408)
    assert closeEnough(np.mean(Rms), 135.459113043)
    assert closeEnough(np.mean(Ras), 17.9413483457)
    assert closeEnough(np.mean(Cms), 129.949702022)


def test_cm_ramp_isolated(abf):
    """Measure Cm (using ramp protocol) of the 33pF model cell."""
    abf = pyabf.ABF(PATH_DATA+"/model_vc_ramp.abf")
    cms = pyabf.tools.memtest.cm_ramp_valuesBySweep(abf)
    assert closeEnough(np.mean(cms), 30.8847047329)


def test_memtest_step_isolated(abf):
    """Measure memtest (using step protocol) of the 33pF model cell."""
    abf = pyabf.ABF(PATH_DATA+"/model_vc_step.abf")
    Ihs, Rms, Ras, Cms = pyabf.tools.memtest.step_valuesBySweep(abf)
    assert closeEnough(np.mean(Ihs), -139.308895874)
    assert closeEnough(np.mean(Rms), 511.624412725)
    assert closeEnough(np.mean(Ras), 14.8798838785)
    assert closeEnough(np.mean(Cms), 23.3401051935)

def go():
    print("Testing add-on modules", end=" ")

    fname = os.path.abspath(PATH_DATA+"/14o08011_ic_pair.abf")
    abf = pyabf.ABF(fname)
    abf.setSweep(sweepNumber=1, channel=1)

    for functionName in sorted(globals()):
        if not functionName.startswith("test_"):
            continue
        log.debug("Running %s" % functionName)
        globals()[functionName](abf)
        print(".", end="")
        sys.stdout.flush()

    print(" OK")

if __name__ == "__main__":
    go()
