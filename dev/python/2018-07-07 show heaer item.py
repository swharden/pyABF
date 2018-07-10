
"""
Code here makes it easy to glance at a header item from every demo ABF file.
"""
from imports import *

if __name__=="__main__":
    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf = pyabf.ABF(fname)
        if abf.abfFileFormat==1:
            print(abf.abfID, abf._headerV1.nTelegraphEnable)
        else:
            print(abf.abfID, abf._adcSection.nTelegraphEnable)

        # if abf.abfFileFormat==1:
        #     plt.figure(figsize=(10,4))
        #     plt.plot(abf.sweepX, abf.sweepY)
        #     plt.title(abf.abfID)
        #     plt.ylabel(abf.sweepLabelY)
        #     plt.xlabel(abf.sweepLabelX)
        #     plt.tight_layout()
        #     plt.margins(0,.1)
    plt.show()