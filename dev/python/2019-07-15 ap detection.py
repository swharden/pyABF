"""
Refactor the AP detection module to provide a clean interface.
You can always refactor the core later.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import matplotlib.pyplot as plt
import pyabf
import pyabf.tools

abf = pyabf.ABF(PATH_DATA+"/171116sh_0018.abf")

# display AP count per sweep
for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    points = pyabf.tools.ap.ap_points_currentSweep(abf)
    msg = f"Sweep %d has %d APs" % (sweepNumber, len(points))
    if (len(points)):
        msg += (f" (first AP at %.02f sec)" % (abf.sweepX[points[0]]))
    print(msg)

# plot the first AP
plt.plot(pyabf.tools.ap.extract_first_ap(abf))
plt.show()
