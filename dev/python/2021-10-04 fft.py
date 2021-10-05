import sys
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

try:
    PATH_HERE = pathlib.Path(__file__).parent
    PATH_ABFS = PATH_HERE.joinpath("../../data/abfs/").resolve()
    PATH_SRC = PATH_HERE.joinpath("../../src/").resolve()
    print(PATH_SRC)
    sys.path.insert(0, str(PATH_SRC))
    import pyabf
except:
    raise EnvironmentError()


def getFft(values: np.ndarray, sampleRate: int, dB: bool = False, zeroDC: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """Return FFT power and frequency for the given values

    Parameters:
        values: evenly-spaced values from the continuous signal
        sampleRate: number of signal values per second (Hz)
        dB: if True the output will be scaled to Decibel units
        zeroDC: if True the lowest frequency (0 Hz corresponding to DC offset) will be zeroed

    Returns:
        A tuple of power spectrum densities and their frequencies

    Note:
        Decibel conversion uses a power of 10 (suitable for power, not amplitude)
        https://dspillustrations.com/pages/posts/misc/decibel-conversion-factor-10-or-factor-20.html
    """

    fft = abs(np.fft.fft(values)/len(values))

    if dB:
        fft = 10 * np.log10(fft)

    if zeroDC:
        fft[0] = 0
    fftFreq = np.fft.fftfreq(len(fft), 1.0 / sampleRate)
    fft = fft[:len(fft)//2]
    fftFreq = fftFreq[:len(fftFreq)//2]
    return (fft, fftFreq)


if __name__ == "__main__":
    abfPath = pathlib.Path(PATH_ABFS).joinpath("17o05027_ic_ramp.abf")
    abf = pyabf.ABF(abfPath)
    fft, freqs = getFft(abf.getAllYs(), abf.sampleRate)

    plt.figure(figsize=(8, 4))
    plt.plot(abf.getAllXs(), abf.getAllYs())
    plt.title(f"Signal: {abf.abfID}.abf")
    plt.ylabel("Potential (mV)")
    plt.xlabel("Time (s)")
    plt.grid(alpha=.5, ls='--')
    plt.margins(0, .1)
    plt.tight_layout()

    plt.figure(figsize=(8, 4))
    plt.plot(freqs, fft)
    plt.title(f"Power Spectrum: {abf.abfID}.abf")
    plt.ylabel("Power (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.grid(alpha=.5, ls='--')
    plt.axis([0, 100, 0, None])
    plt.tight_layout()
    
    plt.show()
