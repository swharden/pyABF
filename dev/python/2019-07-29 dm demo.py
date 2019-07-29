import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
import matplotlib.pyplot as plt

if __name__ == "__main__":
    abf = pyabf.ABF(PATH_DATA+"/DM1_0002.abf")

    colormap = plt.get_cmap("viridis")
    fractions = [sweepNumber / abf.sweepCount for sweepNumber in abf.sweepList]
    sweepColors = [colormap(fraction) for fraction in fractions]

    pt1 = int(294.64 * abf.dataPointsPerMs)
    pt2 = int(895.82 * abf.dataPointsPerMs)

    plt.figure(figsize=(8, 5))
    plt.grid(alpha=.5, ls='--')

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        current = abf.sweepY[pt1:pt2]
        voltage = abf.sweepC[pt1:pt2]
        plt.plot(voltage, current, color=sweepColors[sweepNumber],
                 label=f"sweep {sweepNumber+1}", alpha=.5)

    plt.legend(loc = "lower right")
    plt.margins(0, .1)
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(f"Voltage (mV)")
    plt.title(f"Instaneous IV Relationship of {abf.abfID}")

    plt.show()
