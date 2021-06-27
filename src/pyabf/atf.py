"""
This file contains code simplifying access to data in ATF files.

One goal of this module is to produce an ATF class with virtually all the same
methods as the ABF class.

ATF file format description:
https://mdc.custhelp.com/app/answers/detail/a_id/18883/~/genepix%C2%AE-file-formats
"""
import numpy as np
import os
import sys
import glob

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


class ATF():
    """
    The ATF class provides simplistic access to the header and data which exist 
    in Axon Text Format (ATF) files. This class supports the reading of multi-
    channel data and has a setSweep() function similar to the ABF class.
    """

    def __init__(self, file_path):

        if file_path.lower().endswith(".abf"):
            raise Exception("use pyabf.ABF (not pyabf.ATF) for ABF files")

        # ensure the file exists and open it
        if not os.path.isfile(file_path):
            log.critical("file does not exist")
        self.atfFilePath = file_path
        self.atfID = os.path.basename(self.atfFilePath).replace(".atf", "")
        fh = open(file_path, 'r')

        # line 1 - contains "ATF" and a version number
        signature, file_version = fh.readline().rstrip().split()
        self.atfVersion = file_version
        if signature != 'ATF':
            log.critical("Unexpected file signature "+signature)

        # line 2 - contains "# #" (number of header and data items)
        elems = fh.readline().rstrip().split()
        nHeaderItems, nDataCols = [int(x) for x in elems]
        if nHeaderItems == 0 or nDataCols == 0:
            log.critical("improper header or data structure")
        if nHeaderItems == 0 or nDataCols == 0:
            log.critical("no sweeps found")

        # parse header items - one line per item
        self.header = {}
        for headerItemNumber in range(nHeaderItems):
            headerLine = fh.readline().strip()
            if headerLine.count('"') == 2:
                key, val = headerLine.strip('"').split("=")
                if val.isdigit():
                    val = int(val)
                elif val.replace(".", "").replace("-", "").isdigit():
                    val = float(val)
                elif "." in val and "," in val:
                    val = val.split(",")
                    val = [float(x) for x in val]
            else:
                items = headerLine.split("\t")
                key = items[0].strip().strip('"').strip('=')
                val = items[1:]
                val = [x.strip().strip('"') for x in val]
            self.header[key] = val

        # figure out about our number of channels from their names
        self.channelNames = list(set(self.header["Signals"]))
        self.channelCount = len(self.channelNames)
        self.channelList = list(range(self.channelCount))

        # calculate number of sweeps now that we know channel count
        self.sweepCount = int((nDataCols - 1)/self.channelCount)
        self.sweepList = list(range(self.sweepCount))

        # read one more line which is all our column names
        columnNames = fh.readline().split("\t")
        columnNames = [x.strip().strip('"') for x in columnNames]
        self.columnLabelX = columnNames[0]
        self.columnLabelsY = columnNames[1:]

        # now that we are done reading the header, close the file
        fh.close()

        # read data values as a numpy array
        self.data = np.genfromtxt(file_path, dtype=np.float32,
                                  skip_header=3 + nHeaderItems,
                                  invalid_raise=True,
                                  usecols=range(0, nDataCols))

        # adjust it so it is sweepCount rows and sweepPointCount columns
        self.data = np.rot90(self.data, -1)
        self.data = np.flip(self.data, 1)
        self.dataX = self.data[0]
        self.data = self.data[1:]

        # calculate more useful variables
        self.dataRate = int(1.0/self.dataX[1])
        self.sweepPointCount = len(self.dataX)
        self.sweepLengthSec = self.sweepPointCount/self.dataRate

        # always set the first sweep
        self.setSweep()

    def __str__(self):
        msg = "%s.atf (ATF %s)"%(self.atfID, self.atfVersion)
        msg += " has %d channel"%(self.channelCount)
        if self.channelCount>1:
            msg+="s"
        msg += " with %d sweeps"%(self.sweepCount)
        msg += " (%.02f seconds each)"%(self.sweepLengthSec)
        msg += " at a sample rate of %.02f kHz"%(self.dataRate/1000)
        return msg

    def setSweep(self, sweepNumber=0, channel=0):
        if not sweepNumber in self.sweepList:
            raise ValueError("invalid sweep number")
        columnNumber = sweepNumber*self.channelCount+channel
        self.sweepY = self.data[columnNumber]
        self.sweepX = self.dataX
        self.sweepLabelX = self.columnLabelX
        self.sweepLabelY = self.columnLabelsY[columnNumber]


if __name__ == "__main__":
    log.warn("DO NOT RUN THIS FILE DIRECTLY!")
    sys.path.append(os.path.dirname(__file__)+"/../")
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")

    import matplotlib.pyplot as plt
    for fname in glob.glob(PATH_DATA+"/*.atf"):
        atf = ATF(fname)
        print()
        print(atf)
        for channel in atf.channelList:
            plt.figure()
            plt.title("%s channel %d"%(atf.atfID, channel))
            plt.xlabel(atf.sweepLabelX)
            plt.ylabel(atf.sweepLabelY)
            for sweepNumber in atf.sweepList:
                atf.setSweep(sweepNumber, channel)
                plt.plot(atf.sweepX, atf.sweepY)
            
    plt.show()