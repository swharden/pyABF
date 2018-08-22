"""
Code here makes it easy to glance at a header item from every demo ABF file.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob


import logging
logging.basicConfig(level=logging.DEBUG)

pyabf.epochs.log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    for fname in glob.glob(PATH_DATA+"/*.abf"):
        if not "171116sh_0017" in fname:
            continue
        abf=pyabf.ABF(fname)
        print(abf.epochsByChannel[0].stimulusWaveform(0))
