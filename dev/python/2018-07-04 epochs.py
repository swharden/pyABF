"""

"""
from imports import *
#plt.style.use('bmh')

if __name__ == "__main__":
    abf = pyabf.ABF(PATH_DATA+"/18702001-step.abf")  # complex step
    abf.setSweep(1, 1)
    pointsStart = [0, 312,  1312,  5312, 15312]
    pointsEnd = [312, 1312, 5312, 15312,  20311]
    epochLabels = ["pre", "A", "B", "C", "post"]
    epochCount = len(pointsStart)
    for epoch in range(epochCount):
        i1, i2 = pointsStart[epoch], pointsEnd[epoch]
        plt.plot(abf.sweepX[i1:i2], abf.sweepY[i1:i2],
                 lw=5, alpha=.5, label=epochLabels[epoch])
    plt.legend()
    #plt.show()
    plt.savefig(PATH_HERE+"/dontsync.png")
    print("DONE")
