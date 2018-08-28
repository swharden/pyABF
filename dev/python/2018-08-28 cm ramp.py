"""
show how to calculate Cm from a ramp protocol
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob
import numpy as np
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def cm_from_sweep(abf):
    """
    Calculate capacitance from a voltage clamp ramp on channel 0.
    """

    log.debug(f"calculating Cm from ramp on {abf.abfID}3abf")

    # ensure this is the right type of protocol
    if abf.sweepUnitsY != "pA":
        log.critical("must be in voltage clamp configuration")
        return
    
    log.debug(f"epoch types: {abf._epochPerDacSection.nEpochType}")

    # get the point indexes in the data where the ramps start and end
    epochPoints = pyabf.stimulus.epochPoints(abf)
    log.debug(f"epochs start at {epochPoints}")

    # inspect command voltages
    epochValues = pyabf.stimulus.epochValues(abf)
    log.debug(f"first sweep epoch values {epochValues[0]}")
    return

if __name__=="__main__":
    abfFilesToTest = []
    abfFilesToTest.append(PATH_DATA+"/171116sh_0014.abf")
    abfFilesToTest.append(PATH_DATA+"/model_vc_ramp.abf")
    for abfFile in abfFilesToTest:
        abf = pyabf.ABF(abfFile)
        cm_from_sweep(abf)