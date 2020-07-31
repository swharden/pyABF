"""
Code here inspects every sweep of every channel of every ABF
in the project and stores sweep information as a string in
a dictionary in a python file in the tests folder.
"""

try:
    import glob
    import os
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
    PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
    DATA_FOLDER = os.path.join(PATH_SRC, "../data/abfs/")
    sys.path.insert(0, PATH_SRC)
    import pyabf
except:
    raise EnvironmentError()


def sweepKeyAndInfo(abf, sweepIndex, channelIndex):
    assert isinstance(abf, pyabf.ABF)
    abf.setSweep(sweepIndex, channelIndex)
    key = str(f"{abf.abfID}.abf " +
              f"SW{sweepIndex} " +
              f"CH{channelIndex}")
    info = str(f"{len(abf.sweepY)}, " +
               f"{abf.sweepY[0]:.08f}, " +
               f"{abf.sweepY[-1]:.08f}, " +
               f"{np.std(abf.sweepY):.08f}")
    return [key, info]


if __name__ == "__main__":
    txt=""
    #txt = "\"\"\"ABF sweep hashes generated automatically by 2020-06-19 script in dev folder.\"\"\"\n\n"
    #txt += "# key = ABFID, sweep, and channel\n"
    #txt += "# value = sweep point count, first value, last value, and stdev\n"
    #txt += "knownAbfSweepValues = {}\n"
    for abfPath in glob.glob(DATA_FOLDER + "/*.abf"):
        if not "2020_07" in abfPath:
            continue
        abf = pyabf.ABF(abfPath)
        print(f"generating sweep hashes for {abf.abfID}.abf...")
        txt += "\n"
        for sweepIndex in range(abf.sweepCount):
            for channelIndex in range(abf.channelCount):
                key, info = sweepKeyAndInfo(abf, sweepIndex, channelIndex)
                txt += f'knownAbfSweepValues["{key}"] = "{info}"\n'

    #with open(PATH_SRC+"/../tests/test_sweepHashes.py", 'w') as f:
        #f.write(txt)
    print(txt)