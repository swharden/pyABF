import glob
from core import ABFcore
import matplotlib.pyplot as plt

class ABF(ABFcore):
    def __init__(self, abf, preLoadData=True):
        self._loadEverything(abf, preLoadData)
        self.setSweep(0)

    def setSweep(self, sweepNumber, channel=0):

        # ensure the sweep number is valid
        while sweepNumber<0:
            sweepNumber = self.sweepCount - sweepNumber
        if sweepNumber>=self.sweepCount:
            sweepNumber = self.sweepCount - 1

        # determine data bounds for that sweep
        pointStart = self.sweepPointCount*sweepNumber
        pointEnd = pointStart + self.sweepPointCount
        self.sweepY = self.data[channel,pointStart:pointEnd]


if __name__ == "__main__":
    dataFolder = R"C:\Users\scott\Documents\GitHub\pyABF\data"
    for fname in glob.glob(dataFolder+"/*.abf"):
        abf = ABF(fname)
        print(abf.abfID,abf.sweepCount)

    #     plt.figure()
    #     plt.title(abf.abfID)
    #     for sweep in range(abf.sweepCount):
    #         abf.setSweep(sweep,1)
    #         plt.plot(abf.sweepY)
    # plt.show()
    print("DONE")