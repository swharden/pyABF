"""
Code here relates to filering ABF data.
"""
import os
import sys
import warnings
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    warnings.warn("DO NOT RUN THIS FILE DIRECTLY!")
    sys.path.append(os.path.dirname(__file__)+"/../")
import pyabf


def kernelGaussian(size=100, sigma=None):
    """
    Return a 1d array shaped like a Gaussian curve with area of 1.
    Optionally provide a sigma (the larger, the wider the curve).
    """
    if not sigma:
        sigma = size/7
    points = np.arange(int(size))
    points = np.exp(-np.power(points-size/2, 2) / (2*np.power(sigma, 2)))
    points = points/sum(points)
    return points


def convolve(data, kernel):
    """
    Convolve the data with the kernel. The edges of the returned data (half the
    size of the kernel) will be nan. If you want a different convolution method,
    code it yourself!
    """
    smooth = np.convolve(data, kernel, mode='valid')
    nansNeeded = int((len(data)-len(smooth))/2)
    smooth = np.concatenate((np.full(nansNeeded, np.nan), smooth))
    nansNeeded = int(len(data)-len(smooth))
    smooth = np.concatenate((smooth, np.full(nansNeeded, np.nan)))
    return smooth


def remove(abf):
    """
    Revert to the original data in the ABF. This is accomplished by opening
    the original file and re-reading the data (into abf.data).
    """
    abf._fileOpen()
    abf._loadAndScaleData()
    abf._fileClose()


def gaussian(abf, sigmaMs=5, channel=0):
    """
    Perform a gaussian convolution on every sweep of the indicated channel.
    Note that this performs smoothing once (acting directly on abf.data), and
    subsequent calls will keep smoothing the smoothed trace.

    Set sigmaMs to 0 or False to remove the filter.
    """

    if not sigmaMs:
        remove(abf)
        return

    pointsPerMs = abf.dataRate/1000.0
    kernel = kernelGaussian(int(pointsPerMs*sigmaMs*7))
    abf.data[channel] = convolve(abf.data[channel], kernel)


if __name__ == "__main__":
    print("DEVELOPER TESTING ONLY")

    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")
    abf = pyabf.ABF(PATH_DATA+"/17o05026_vc_stim.abf")
    print(abf.abfID)
    plt.figure()
    abf.setSweep(3)
    plt.plot(abf.sweepX, abf.sweepY, alpha=.2, color='k', label="original")

    for sigma in [.5, 2, 10]:
        gaussian(abf, 0)  # remove old filter
        gaussian(abf, sigma)  # apply custom sigma
        abf.setSweep(3)  # reload sweep
        plt.plot(abf.sweepX, abf.sweepY, alpha=.8, label=f"sigma: {sigma}")

    plt.axis([8.20, 8.30, -45, -5])
    plt.legend()
    plt.show()
