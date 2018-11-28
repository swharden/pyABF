"""
pyabf2 is a pyABF module which supports Python 2.7
  * It is not officially supported, but most features work.
  * It is a modified version of pyABF 2.0.27.
  * This script demonstrates how to use it
"""

import sys
assert sys.version_info.major == 2 and sys.version_info.minor == 7
import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
sys.path.insert(0, PATH_HERE)

import pyabf2
abf = pyabf2.ABF(PATH_DATA + "/171116sh_0011.abf")
for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    print "sweep %02d: %s"%(sweepNumber, abf.sweepY)