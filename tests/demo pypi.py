# This is the example used on the front page of pypi for pyABF
import sys
sys.path.insert(0,'../src/') # path to the pyabf folder (if not installed with pip)

import pyabf
import matplotlib.pyplot as plt
plt.style.use('seaborn')

abf=pyabf.ABF("../data/17o05028_ic_steps.abf") 
plt.figure(figsize=(8,4))
for sweepNumber in abf.sweepList:
    if (sweepNumber%2>0) or sweepNumber>7:
        continue
    abf.setSweep(sweepNumber)
    plt.plot(abf.dataX,abf.dataY)
	
plt.ylabel(abf.unitsLong)
plt.xlabel(abf.unitsTimeLong)
plt.margins(0,.1)
plt.savefig('../src/demo1.png')
plt.show()