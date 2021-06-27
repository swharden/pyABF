"""
This file contains code simplifying access to data in ATF files.

One goal of this module is to produce an ATF class with virtually all the same
methods as the ABF class.

ATF file format description:
https://mdc.custhelp.com/app/answers/detail/a_id/18883/~/genepix%C2%AE-file-formats
"""
import numpy as np
import os
import pathlib
from typing import Union


class ATF():
    """
    The ATF class provides simplistic access to the header and data which exist 
    in Axon Text Format (ATF) files. This class supports the reading of multi-
    channel data and has a setSweep() function similar to the ABF class.
    """

    def __init__(self, atfFilePath: Union[str, pathlib.Path], loadData: bool = True):
        """
        Load header and sweep data from an ATF file.
        
        ### Parameters
        1. atfFilePath -- path to the ATF file
        2. loadData -- whether or not to parse sweep data values on instantiation
        """

        if (isinstance(atfFilePath, pathlib.Path)):
            atfFilePath = str(atfFilePath)

        if atfFilePath.lower().endswith(".abf"):
            raise Exception("use pyabf.ABF (not pyabf.ATF) for ABF files")

        if (os.path.isdir(atfFilePath)):
            raise Exception("path must be a path to a FILE not a FOLDER.")

        # ensure the file exists and open it
        if not os.path.isfile(atfFilePath):
            raise Exception("file does not exist")
        self.atfFilePath = atfFilePath
        self.atfID = os.path.basename(self.atfFilePath).replace(".atf", "")
        fh = open(atfFilePath, 'r')

        # line 1 - contains "ATF" and a version number
        signature, file_version = fh.readline().rstrip().split()
        self.atfVersion = file_version
        if signature != 'ATF':
            raise Exception("Unexpected file signature "+signature)

        # line 2 - contains "# #" (number of header and data items)
        elems = fh.readline().rstrip().split()
        nHeaderItems, nDataCols = [int(x) for x in elems]
        if nHeaderItems == 0 or nDataCols == 0:
            raise Exception("improper header or data structure")
        if nHeaderItems == 0 or nDataCols == 0:
            raise Exception("no sweeps found")

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

        if (loadData == False):
            return

        # read data values as a numpy array
        self.data = np.genfromtxt(atfFilePath, dtype=np.float32,
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
        msg = "%s.atf (ATF %s)" % (self.atfID, self.atfVersion)
        msg += " has %d channel" % (self.channelCount)
        if self.channelCount > 1:
            msg += "s"
        msg += " with %d sweeps" % (self.sweepCount)
        msg += " (%.02f seconds each)" % (self.sweepLengthSec)
        msg += " at a sample rate of %.02f kHz" % (self.dataRate/1000)
        return msg

    def setSweep(self, sweepNumber=0, channel=0):
        """
        Update the ATF class to hold data, labels, and units for the given sweep.
        
        ### Parameters
        1. sweepNumber -- zero-indexed sweep number
        2. channel -- zero-indexed channel number
        """

        if not sweepNumber in self.sweepList:
            raise ValueError("invalid sweep number")
        columnNumber = sweepNumber*self.channelCount+channel
        self.sweepY = self.data[columnNumber]
        self.sweepX = self.dataX
        self.sweepLabelX = self.columnLabelX
        self.sweepLabelY = self.columnLabelsY[columnNumber]
