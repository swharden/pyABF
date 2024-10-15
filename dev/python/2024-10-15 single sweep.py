import sys
import pathlib
import matplotlib.pyplot as plt
import numpy as np

try:
    PATH_HERE = pathlib.Path(__file__).parent
    PATH_ABFS = PATH_HERE.joinpath("../../data/abfs/").resolve()
    PATH_SRC = PATH_HERE.joinpath("../../src/").resolve()
    print(PATH_SRC)
    sys.path.insert(0, str(PATH_SRC))
    import pyabf
except:
    raise EnvironmentError()
1

if __name__ == "__main__":
    abfPath = pathlib.Path(PATH_ABFS).joinpath("14o08011_ic_pair.abf")

    abf = pyabf.ABF(abfPath, loadData=False)
    channelA = abf.getOnlySweep(sweepIndex=0, channelIndex=0)
    channelB = abf.getOnlySweep(sweepIndex=0, channelIndex=1)

    print(np.mean(channelA))
    print(np.mean(channelB))

    plt.plot(channelA)
    plt.plot(channelB)
    plt.show()
