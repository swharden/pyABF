import sys
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

try:
    PATH_HERE = pathlib.Path(__file__).parent
    PATH_ABFS = PATH_HERE.joinpath("../../data/abfs/").resolve()
    PATH_SRC = PATH_HERE.joinpath("../../src/").resolve()
    print(PATH_SRC)
    sys.path.insert(0, str(PATH_SRC))
    import pyabf
except:
    raise EnvironmentError()


if __name__ == "__main__":
    abfPath = pathlib.Path(PATH_ABFS).joinpath("17o05027_ic_ramp.abf")
    abf = pyabf.ABF(abfPath)
    f, t, Sxx = signal.spectrogram(abf.getAllYs(), abf.sampleRate)
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.axis([None, None, 0, 500])
    plt.tight_layout()
    plt.show()
