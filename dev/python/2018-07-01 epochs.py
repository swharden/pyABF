# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../../src/")  # for your IDE
import pyabf
import glob

import matplotlib.pyplot as plt
import numpy as np
import warnings


def populateEpochInfo(abf, sweep=0, channel=0):
    """
    Provide easy-to-use lists of command values, types, and times.
    """
    # TODO: support more epoch types

    # TODO: create epochs for ABF1 files
    if abf.abfFileFormat != 2:
        raise NotImplementedError

    # populate epoch arrays with values appropriate for pre-sweep
    epochPoints = [0]
    epochValues = [abf.holdingCommand[channel]]
    epochTypes = [1]

    # the epoch doesn't actually start at the start of the sweep
    position = int(abf.sweepPointCount/64)

    # epochs are in a flat list repeated by channel
    epochCount = len(abf._epochPerDacSection.nEpochType)
    epochsOfThisChannel = np.arange(epochCount/abf.channelCount)
    epochsOfThisChannel += epochCount*channel

    #epochsOfThisChannel = range(len(abf._epochPerDacSection.nEpochType))

    # step through each epoch and track the command value and time position
    for epoch in epochsOfThisChannel:
        epoch = int(epoch)
        epochType = abf._epochPerDacSection.nEpochType[epoch]
        thisT = abf._epochPerDacSection.lEpochInitDuration[epoch]
        dT = abf._epochPerDacSection.lEpochDurationInc[epoch] * sweep
        thisC = abf._epochPerDacSection.fEpochInitLevel[epoch]
        dC = abf._epochPerDacSection.fEpochLevelInc[epoch] * sweep
        dClast = abf._epochPerDacSection.fEpochLevelInc[epoch] * (sweep-1)
        position += thisT+dT

        # add this epoch to the list
        epochTypes.append(epochType)
        epochValues.append(thisC+dC)
        epochPoints.append(position)

        # determine if the pre-command is holding or holdover from last sweep
        if epoch == 0 and abf._dacSection.nInterEpisodeLevel[channel]:
            epochValues[0] = thisC+dClast

    # add an after-epoch value (holding command or command holdover)
    epochTypes.append(1)
    epochPoints.append(position)
    epochValues.append(abf.holdingCommand[channel])
    if abf._dacSection.nInterEpisodeLevel[channel]:
        epochValues[-1] = thisC+dC

    # add a point to simulate the end of the sweep
    epochTypes.append(1)
    epochPoints.append(abf.sweepPointCount-1)
    epochValues.append(epochValues[-1])

    for epochType in epochTypes:
        if not epochType in [0, 1]:
            msg = f"epoch type {epochType} unsupported"
            warnings.warn(msg)

    #print(epochTypes, epochPoints, epochValues)

    return [epochPoints, epochValues]


if __name__ == "__main__":
    # abf = pyabf.ABF(PATH_DATA+"/171116sh_0013.abf")  # ramp
    # abf = pyabf.ABF(PATH_DATA+"/2018_04_13_0016b_modified.abf") # delta t
    abf = pyabf.ABF(PATH_DATA+"/14o16001_vc_pair_step.abf")  # delta c

    fig, axs = plt.subplots(2, 1, sharex='all')

    for sweep in abf.sweepList:
        abf.setSweep(sweep, 0)
        epochPoints, epochValues = populateEpochInfo(abf, sweep)

        axs[0].plot(abf.sweepX, abf.sweepY, color='b', lw=.5, alpha=.5)
        axs[1].step(abf.sweepX[epochPoints], epochValues, color='r')

    plt.show()

    print("DONE")
