"""
Is there a way to determine the best lowpass filter based on measuring
the noise value? It would be great if lowpass filter settings could be
determined by the ABF, not by qualitative user input.

This also requires RMS measurement.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt
import numpy as np
import glob

import pyabf


def getIdealABFs():
    print("scanning ABFs...")
    idealAbfs = []
    for abfFilePath in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFilePath)
        if (abf.sweepUnitsY == "pA"
                and abf.sweepLengthSec <= 60
                and abf.dataRate <= 20000):
            idealAbfs.append(abf)
    print(f"Found {len(idealAbfs)} ideal ABFs to analyze")
    return idealAbfs


def getRmsNoise(abf, percentile=10, pieceSizeMsec=10):
    # Theory: break the sweep into many pieces, calculate RMS noise of each,
    #         then return the given percentile of those noise values.
    piecePointCount = int(abf.dataPointsPerMs * pieceSizeMsec)
    if piecePointCount == 0:
        return None
    pieceCount = int(len(abf.sweepY) / piecePointCount)
    rmsByPiece = np.empty(pieceCount)
    for pieceNumber in range(pieceCount):
        i1 = pieceNumber * piecePointCount
        i2 = i1 + piecePointCount
        piece = abf.sweepY[i1:i2]
        rmsByPiece[pieceNumber] = np.std(piece)
    return np.percentile(rmsByPiece, percentile)


def figure_rmsNoiseByPercentile():
    plt.figure(figsize=(8, 6))
    plt.grid(alpha=.5)
    for abfFilePath in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFilePath)
        if (abf.sweepUnitsY == "pA" and abf.sweepLengthSec < 60):
            print("ANALYZING", abf)
            xs = []
            ys = []
            for i in range(100):
                xs.append(i)
                ys.append(getRmsNoise(abf, i))
            plt.plot(xs, ys, alpha=.7)
        else:
            print("SKIPPING", abf)
    plt.ylabel("RMS Noise (pA)")
    plt.xlabel("Floor Percentile (%)")
    plt.title("Noise by ABF")
    plt.axis([None, None, 0.5, 10.5])
    plt.tight_layout()
    plt.savefig("2019-06-07 auto detect lowpass filter 1.png")
    plt.show()


def smoothFlat(x, window_len=40):
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = np.ones(window_len, 'd')
    f = np.convolve(w/w.sum(), s, mode='same')
    f = f[window_len-1:]
    f = f[:-window_len+1]
    return f


def smoothHanning(x, window_len=40):
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = np.hanning(window_len)
    f = np.convolve(w/w.sum(), s, mode='same')
    f = f[window_len-1:]
    f = f[:-window_len+1]
    return f


def figure_noiseSpectrum(abfs):
    plt.figure(figsize=(8, 6))
    plt.grid(alpha=.5, ls='--')
    plt.axhline(0, color='k')
    plt.ylabel("Power (dB)")
    plt.xlabel("Frequency (kHz)")
    plt.title("ABF Sweep Noise Frequency Analysis")

    for abf in abfs[::2]:
        print(abf)

        # create a hanning-window-smoothed sweep of data to analyze
        smoothedSweep = np.hanning(len(abf.sweepY)) * abf.sweepY
        fft = np.fft.fft(smoothedSweep)

        # sum the absolute value of real and imaginary components
        fft = np.abs(fft)
        fftRight = fft[:int(len(fft)/2)]
        fftLeft = fft[int(len(fft)/2):]
        if len(fftRight) != len(fftLeft):
            continue
        fft = fftRight + fftLeft[::-1]

        # convert to decibels
        fft = 20 * np.log10(fft)

        # smooth
        fft = smoothFlat(fft)

        # calculate frequency axis
        freqs = np.fft.fftfreq(len(abf.sweepY), 1 / abf.dataRate)
        freqs = freqs[:int(len(freqs)/2)]

        # silence FFT below 10Hz
        for i, freq in enumerate(freqs):
            fft[i] = None
            if freq > 10:
                break

        plt.plot(freqs/1000, fft, alpha=.7, label=abf.abfID)

    plt.tight_layout()
    plt.margins(0, 0.05)
    plt.axis([0, 10, None, None])
    plt.legend(fontsize=8)
    plt.savefig("2019-06-07 auto detect lowpass filter 0.png")
    plt.show()


def lowPassIFFT(abf, kHz=.25):
    fft = np.fft.fft(abf.sweepY)
    freqs = np.fft.fftfreq(len(abf.sweepY), 1 / abf.dataRate)
    for i, freq in enumerate(freqs):
        if np.abs(freq) > kHz*1000:
            fft[i] = np.complex(0, 0)
    ifft = np.fft.ifft(fft)
    return ifft


def lowPassHanning(abf, kHz=.25):
    windowSizePoints = int(abf.dataRate / (kHz * 1000.0))
    smooth = smoothHanning(abf.sweepY, windowSizePoints)
    return smooth


def figure_typicalTraceFiltered():
    abf = pyabf.ABF(PATH_DATA+"/171116sh_0020.abf")
    abf.setSweep(1)
    xsMs = abf.sweepX*1000
    plt.figure(figsize=(8, 4))
    plt.plot(xsMs, abf.sweepY, label="original", alpha=.5)
    plt.plot(xsMs, lowPassIFFT(abf), label="iFFT", color='k', lw=1)
    plt.plot(xsMs, lowPassHanning(abf), label="Hanning", color='r', lw=1)
    plt.axis([1500, 1750, -10, 95])
    plt.ylabel("Clamp Current (pA)")
    plt.xlabel("Sweep Time (milliseconds)")
    plt.title("250 Hz Low-Pass Filter")
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig("2019-06-07 auto detect lowpass filter 2.png")
    plt.show()


def figure_listNoiseForEveryAbf(idealAbfs):
    rmsAbfs = []
    rmsValues = []
    for abf in idealAbfs:
        rmsAbfs.append(abf.abfID)
        rms = getRmsNoise(abf, 25)
        if not rms:
            rms = 0
        rmsValues.append(rms)
    rmsValues, rmsAbfs = zip(*sorted(zip(rmsValues, rmsAbfs)))

    print("ABF File | RMS Noise (25%, 10ms)")
    print("---|---")
    for i, abfFile in enumerate(rmsAbfs):
        imgUrl = f"https://raw.githubusercontent.com/swharden/pyABF/master/data/headers/{abfFile}.png"
        #print(f"{abfFile}.abf | {round(rmsValues[i], 3)} pA | ![]({imgUrl})")
        print(f"{abfFile}.abf | {round(rmsValues[i], 4)} pA")


def figure_quietVsNoisy():

    plt.figure(figsize=(8, 6))

    plt.subplot(211)
    abf = pyabf.ABF(PATH_DATA+"/171116sh_0011.abf")  # noisy
    plt.title(f"171116sh_0011.abf (RMS noise: 1.769  pA)")
    plt.ylabel(abf.sweepLabelY)
    plt.plot(abf.sweepX, abf.sweepY, alpha=.3)
    plt.plot(abf.sweepX, lowPassHanning(abf, 1), color='k', lw=1)
    plt.axis([.30, .50, -225, -100])

    plt.subplot(212)
    abf = pyabf.ABF(PATH_DATA+"/f1_saved.abf")  # noisy
    plt.title(f"f1_saved.abf (RMS noise: 4.933 pA)")
    plt.plot(abf.sweepX, abf.sweepY, alpha=.3)
    plt.plot(abf.sweepX, lowPassHanning(abf, 1), color='k', lw=1)
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.axis([.68, .88, -125, 0])

    plt.tight_layout()
    plt.savefig("2019-06-07 auto detect lowpass filter 4.png")
    plt.show()


if __name__ == "__main__":
    idealAbfs = getIdealABFs()
    # figure_noiseSpectrum(idealAbfs)
    # figure_rmsNoiseByPercentile()
    # figure_typicalTraceFiltered()
    # figure_listNoiseForEveryAbf(idealAbfs)
    figure_quietVsNoisy()
