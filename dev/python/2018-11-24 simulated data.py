"""
Collect code here which may be useful to simulate patch-clamp-like recordings
from scratch. This will be useful when generating data to practice exporting
into different formats (e.g., ABF1) or when performing/testing various event
detection or curve fitting routines.

This script was used to create the NPY file containing a few sweeps of simulated
data representing a cell in whole-cell patch-clamp configuration with a high
chloride internal looking at IPSCs (appearing as inward currents):
  * 10 Hz IPSCs (monoexponential) were stochastically placed in each sweep
  * The time constant of each is about 100ms, but randomly varies slightly
  * Event amplitude is random (not normally distributed though)
  * Gaussian noise was added to the trace to simulate amplifier noise
  * A slight wobble was added to the trace to reflect real recording conditions
  * The signal was low-pass filtered (due to Ra, not the hardware filter)
  * Extra tools are in this function to similarly generate EPSPs/IPSPs (alpha)
"""

import numpy as np
import matplotlib.pyplot as plt
import os
FOLDER_HERE = os.path.dirname(__file__)

# trace feature generation


def generate_alpha(pointCount=1000):
    """create a smooth rise/fall similar to an EPSP"""
    xs = np.arange(pointCount)
    alpha = 10/pointCount
    data = alpha**2*xs*np.exp(-alpha*xs)
    data /= np.max(data)
    return data


def generate_exp(tauMs=100, rate=20_000, fudgeTau=True):
    """create a sharp rise and exponential decay, like an IPSC."""
    tauPoints = tauMs * 20_000 / 1000
    xs = np.arange(tauPoints)
    if fudgeTau:
        fudgeFactor = tauMs/2
        tauMs += np.random.random()*fudgeFactor-fudgeFactor/2
    data = np.exp(-xs/tauMs)
    return data


def _demo_check_IPSC_tau():
    """visual check that IPSC time constants are accurate."""
    plt.figure()
    plt.grid(alpha=.2)
    plt.title("IPSC time constant assessment")
    taus = [10, 15, 25, 35, 50]
    plt.axhline(100/np.e, color='k', ls='--')
    for i, tau in enumerate(taus):
        data = generate_exp(tau)
        dataX = np.arange(0, len(data))/20_000
        plt.plot(data*100, color=f'C{i}', label=f"tau = {tau} ms")
        plt.axvline(tau, color=f'C{i}', ls=':', alpha=.5)
    plt.legend()
    plt.axis([0, 100, None, None])
    plt.xlabel("time (ms)")
    plt.ylabel("magnitude (%)")
    plt.show()


# addition of noise, filtering, and instability artifacts


def _kernel_gaussian(size=100, sigma=None):
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


def _convolve(data, kernel):
    """
    Convolve the data with the kernel. The edges of the returned data (half the
    size of the kernel) will be nan. If you want a different convolution method,
    code it yourself!
    """
    smooth = np.convolve(data, kernel, mode='same')  # use valid for strict
    nansNeeded = int((len(data)-len(smooth))/2)
    smooth = np.concatenate((np.full(nansNeeded, np.nan), smooth))
    nansNeeded = int(len(data)-len(smooth))
    smooth = np.concatenate((smooth, np.full(nansNeeded, np.nan)))
    return smooth


def smooth(data, kernelWidthDataFrac=.1):
    """simple gaussian convolution. Guesses most values."""
    kernelSize = int(len(data)*kernelWidthDataFrac)
    kernel = _kernel_gaussian(size=kernelSize)
    return _convolve(data, kernel)


def add_noise(data, magnitude=3):
    """Return the input signal with normal (gaussian) noise added."""
    noise = np.random.normal(0, magnitude/10, len(data))
    return data + noise * magnitude


def add_wobble(data, magnitude=3):
    """add slow wobbling to make the signal slowly drift in stability."""
    wobble = np.random.normal(0, magnitude/10, len(data))
    wobble = smooth(wobble)
    wobbleMax = np.nanmax(wobble)
    wobble /= wobbleMax
    return data + wobble * magnitude


# full sweep creation

def generate_sweep_IPSCs(rate_Hz=20000, length_sec=5, ipsc_freq_Hz=20,
                         offset=-123, plotToo=False):

    # start with a clean trace
    data = np.zeros(rate_Hz*length_sec, dtype=np.float)

    # add IPSCs at totally random times (allow compound events)
    eventTimes = np.random.random_sample(length_sec*ipsc_freq_Hz)*length_sec
    eventTimes = np.sort(eventTimes)
    eventMagnitudes = np.random.random_sample(len(eventTimes))*50.0
    polarity = -1  # make negative to reverse the direction of events
    for i in range(len(eventTimes)):
        eventIndex = int(rate_Hz*eventTimes[i])
        eventTrace = generate_exp() * eventMagnitudes[i]
        if (len(data)-eventIndex) < len(eventTrace):
            maxEventLength = len(data)-eventIndex
            eventTrace = eventTrace[:maxEventLength]
        traceBefore = data[eventIndex:eventIndex+len(eventTrace)]
        traceAfter = traceBefore + eventTrace * polarity
        data[eventIndex:eventIndex+len(eventTrace)] = traceAfter

    # low-pass filter the recording (to smooth the rising edge of IPSCs)
    lowPassFilterHz = 500  # be aggressive here to compensate for Ra*Cm
    lowPassFilterPoints = int(rate_Hz/lowPassFilterHz)
    data = _convolve(data, _kernel_gaussian(size=lowPassFilterPoints))

    # add recording artifacts
    data = add_noise(data)
    data = add_wobble(data, 2)

    # adjust offset
    data += offset

    if plotToo:
        dataX = np.arange(len(data))/rate_Hz
        plt.figure(figsize=(8, 4))
        plt.grid(alpha=.2)
        plt.plot(dataX*1000, data, lw=.5, color='r')
        plt.title("Simulated Voltage-Clamp Trace (sIPSCs)")
        plt.xlabel("time (ms)")
        plt.ylabel("current (pA)")
        plt.margins(0, .1)
        plt.tight_layout()
        plt.show()

    return data


def generate_sweeps_IPSCs(sweepCount=10, sweepLengthSec=5, rate_Hz=20_000):
    """save several sweeps of simulated data as a numpy array (NPY file)."""
    sweepPoints = rate_Hz * sweepLengthSec
    data = np.empty((sweepCount, sweepPoints), dtype=np.float16)
    for sweep in range(sweepCount):
        print(f"generating sweep {sweep+1} of {sweepCount} ...")
        data[sweep] = generate_sweep_IPSCs(rate_Hz, sweepLengthSec)
    np.save(FOLDER_HERE+"/2018-11-24 simulated data.npy", data)
    return data


def load_simulated_data():
    """load the NPY file and display it."""
    data = np.load(FOLDER_HERE+"/2018-11-24 simulated data.npy")
    sweepX = np.arange(len(data[0]))/20_000
    plt.figure(figsize=(8, 4))
    plt.plot(sweepX*1000, data[0], color='r', lw=.5)
    plt.margins(0, .1)
    plt.ylabel("current (pA)")
    plt.ylabel("time (ms)")
    plt.show()


if __name__ == "__main__":
    load_simulated_data()
    print("DONE")
