"""

                Ch1 EPOCH    pre      A      B      C   post
                     Type   Step   Step   Step   Step   Step
         First Level (mV)    -10    -20    -10     25     25
         Delta Level (mV)      0      0      0     10      0
 First Duration (samples)    312   1000   4000  10000      0
 Delta Duration (samples)      0      0      0      0      0
   Train Period (samples)      0      0      0      0      0
    Pulse Width (samples)      0      0      0      0      0
    Epoch Start (samples)      0    312   1312   5312  15312
      Epoch End (samples)    312   1312   5312  15312  20311

"""

from imports import *
plt.style.use('bmh')

COLORBLIND_COLORS = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf',
                     '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']


class Epochs:
    def __init__(self, abf, channel):
        """
        handles epoch values for a single sweep/channel
        """

        self.abf = abf
        self.channel = channel

        self._initEpochVars()

        if abf.abfFileFormat==1:
            self._updateForABFv1()
        elif abf.abfFileFormat==2:
            self._addPreEpoch()
            self._fillEpochsFromABF()
            self._addPostEpoch()
            
        self._createEpochLabels()
        self._updateEpochDetails()

    def __len__(self):
        return len(self.epochList)

    def __str__(self):
        msg = f"Channel {self.channel} epochs ({self.epochCount}): "
        msg += ", ".join(self.label)
        return msg

    def __repr__(self):
        return "ChannelEpochs(ABF, %s)" % (self.channel)

    def _initEpochVars(self):
        """
        Create empty lists for every field of the waveform editor
        """
        self.pointStart = []
        self.pointEnd = []
        self.label = []
        self.type = []
        self.level = []
        self.levelDelta = []
        self.duration = []
        self.durationDelta = []
        self.pulsePeriod = []
        self.pulseWidth = []
        self.digitalOutputs = []  # TODO: this never gets filled

    def _updateForABFv1(self):
        """
        Do our best to create an epoch from what we know about the ABFv1.
        Currently this makes it look like a single step epoch over the 
        entire sweep.
        """
        #TODO: support this better
        warnings.warn("ABFv1 epoch synthesis not fully supported")
        self.pointStart.append(0)
        self.pointEnd.append(self.abf.sweepPointCount)
        self.type.append(1)
        self.level.append(self.abf.holdingCommand[self.channel])
        self.levelDelta.append(0)
        self.duration.append(self.abf.sweepPointCount)
        self.durationDelta.append(0)
        self.pulsePeriod.append(0)
        self.pulseWidth.append(0)
        self.digitalOutputs.append(self.abf.sweepPointCount)

    def _addPreEpoch(self):
        """
        The pre-epoch period is 1/64th of the swep length (dear god why?!)
        so make a fake epoch to represent this pre-epoch
        """
        self._pointOffset = int(self.abf.sweepPointCount/64)

        self.pointStart.append(0)
        self.pointEnd.append(self._pointOffset)
        self.type.append(1)
        self.level.append(self.abf.holdingCommand[self.channel])
        self.levelDelta.append(0)
        self.duration.append(self._pointOffset)
        self.durationDelta.append(0)
        self.pulsePeriod.append(0)
        self.pulseWidth.append(0)
        self.digitalOutputs.append(self._pointOffset)

    def _fillEpochsFromABF(self):
        """
        Read the ABF header and append to the epoch lists
        """

        # load epoch values relevant to this channel
        for i, dacNum in enumerate(self.abf._epochPerDacSection.nDACNum):
            if dacNum != self.channel:
                continue
            epPerDac = self.abf._epochPerDacSection
            self.pointStart.append(self.pointStart[-1]+self.duration[-1])
            self.type.append(epPerDac.nEpochType[i])
            self.level.append(epPerDac.fEpochInitLevel[i])
            self.levelDelta.append(epPerDac.fEpochLevelInc[i])
            self.duration.append(epPerDac.lEpochInitDuration[i])
            self.durationDelta.append(epPerDac.lEpochDurationInc[i])
            self.pulsePeriod.append(epPerDac.lEpochPulsePeriod[i])
            self.pulseWidth.append(epPerDac.lEpochPulseWidth[i])
            self.pointEnd.append(self.pointStart[-1]+self.duration[-1])

    def _addPostEpoch(self):
        """
        There is ABF data after the last epoch is over. Create a fake epoch
        to represent this.
        """
        if self.abf._dacSection.nInterEpisodeLevel[self.channel]:
            # don't revert back to holding, sustain last epoch.
            # do this by extending the last epoch to the end of the sweep.
            self.pointEnd[-1] = self.abf.sweepPointCount-1 + self._pointOffset
        else:
            # revert back to holding
            self.pointStart.append(self.pointEnd[-1])  # TODO: +1?
            self.pointEnd.append(
                self.abf.sweepPointCount - 1 + self._pointOffset)
            self.type.append(1)
            self.level.append(self.level[-1])
            self.levelDelta.append(0)
            self.duration.append(0)
            self.durationDelta.append(0)
            self.pulsePeriod.append(0)
            self.pulseWidth.append(0)

    def _createEpochLabels(self):
        self.label = [chr(x+64) for x in range(len(self.type))]
        self.label[0] = "pre"
        if self.duration[-1] == 0:
            self.label[-1] = "post"

    def _prePulseDetermine(self):
        """
        What happens after the last epoch? Is it holding, or sustained?
        """
        if self.abf._dacSection.nInterEpisodeLevel[self.channel]:
            # if not, sustain the last epoch through to the end of the sweep
            self.pointEnd[-1] = self.abf.sweepPointCount-1 + self._pointOffset
        else:
            # if so, add a fake epoch (step) back to the holding values
            self.pointStart.append(self.pointEnd[-1])  # TODO: +1?
            self.pointEnd.append(
                self.abf.sweepPointCount - 1 + self._pointOffset)
            self.type.append(1)
            self.level.append(self.level[-1])
            self.levelDelta.append(0)
            self.duration.append(0)
            self.durationDelta.append(0)
            self.pulsePeriod.append(0)
            self.pulseWidth.append(0)

    def _updateEpochDetails(self):
        """
        After all epochs have been loaded, do some housekeeping
        """

        self.epochCount = len(self.type)
        self.epochList = range(self.epochCount)
        self.dacUnits = self.abf.dacUnits[self.channel]

    def _txtFmt(self, label, values):
        """
        Format a label and its values for text-block printing.
        """

        if label == "Type":
            for i, value in enumerate(values):
                if value == 0:
                    values[i] = "Off"
                elif value == 1:
                    values[i] = "Step"
                elif value == 2:
                    values[i] = "Ramp"
                else:
                    values[i] = "%d?" % value
                    msg = "UNSUPPORTED EPOCH TYPE: %d" % value
                    warnings.warn(msg)

        line = label.rjust(25, ' ')
        for val in values:
            if not isinstance(val, str):
                val = "%d" % val
            line += val.rjust(7, ' ')
        return line+"\n"

    @property
    def text(self):
        """
        Return all epoch levels as a text block, similar to how ClampFit does
        this when poking through the file properties dialog
        """
        out = "\n"
        out += self._txtFmt("Ch%d EPOCH" % self.channel, self.label)
        out += self._txtFmt("Type", self.type)
        out += self._txtFmt(f"First Level ({self.dacUnits})", self.level)
        out += self._txtFmt(f"Delta Level ({self.dacUnits})", self.levelDelta)
        out += self._txtFmt("First Duration (samples)", self.duration)
        out += self._txtFmt("Delta Duration (samples)", self.durationDelta)
        out += self._txtFmt("Train Period (samples)", self.pulsePeriod)
        out += self._txtFmt("Pulse Width (samples)", self.pulseWidth)
        out += self._txtFmt("Epoch Start (samples)", self.pointStart)
        out += self._txtFmt("Epoch End (samples)", self.pointEnd)
        out += "\n"
        return out


def testGraph():
    abf = pyabf.ABF(PATH_DATA+"/18702001-step.abf")  # complex step

    abf.setSweep(2, 1)

    epochs = Epochs(abf, abf.sweepChannel)
    for epochNumber in epochs.epochList:
        i1 = epochs.pointStart[epochNumber]
        i2 = epochs.pointEnd[epochNumber]
        plt.plot(abf.sweepX[i1:i2], abf.sweepY[i1:i2],
                 lw=5, alpha=.8, label=epochs.label[epochNumber],
                 color=COLORBLIND_COLORS[epochNumber])
    plt.legend()
    plt.title(time.time())
    plt.tight_layout()
    # plt.show()
    plt.savefig(PATH_HERE+"/dontsync.png")

def testCharting():
    for fname in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(fname)
        for channel in abf.channelList:
            epochs = Epochs(abf, channel)
            #print(abf.abfID, epochs)
            print(epochs.text)

if __name__ == "__main__":
    #testGraph()
    testCharting()

    print("DONE")
