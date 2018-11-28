"""
Code here relates to the from-scratch creation of data which simulates
electrical recordings of neurons. Creating data from scratch is useful 
because (1) you can generate your own ABFs to analyze without requiring
access to real recordings and, (2) generating data with known events allows you
to test your event detection code to ensure the results are what you expect.
Same goes for simulating membrane tests, then analyzing them.
"""

import numpy as np
import matplotlib.pyplot as plt


def generate_exp(tauMs=100, rateHz=20_000, filterHz=4_000):
    """
    Create a signal similar to an EPSC or IPSC with a sharp rise and 
    exponential decay. Apply a Gaussian convolution (to simulate the low-pass
    effect of Cm/Ra) to take the sharp edge off the rising slope.
    """
    eventPoints = tauMs * rateHz / 2000
    xs = np.arange(eventPoints)
    data = np.exp(-xs/tauMs)
    smoothPoints = rateHz / filterHz
    data = np.convolve(data, _kernel_gaussian(smoothPoints*10, smoothPoints))
    return data

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

class SweepVC:

    def __init__(self, sampleRate=20000, sweepLengthSec=5):
        self.sampleRate = int(sampleRate)
        pointCount = sampleRate*sweepLengthSec
        self.sweepY = np.zeros(pointCount)
        self.sweepX = np.arange(pointCount)/sampleRate

    def addOffset(self, offset):
        """Add a fixed offset (pA) to the trace."""
        self.sweepY += offset

    def addNoise(self, magnitude=3):
        """Add normal (gaussian) noise to the trace."""
        noise = np.random.normal(0, magnitude/10, len(self.sweepY))
        self.sweepY = self.sweepY + noise

    def addPSC(self, timeSec=1.23, magnitude=20, positive=False):
        """Add a single post-synaptic current at a given time point."""
        eventOnly = generate_exp() * magnitude
        if not positive:
            eventOnly *= -1
        eventSweep = np.zeros(len(self.sweepY))
        eventSweep[:len(eventOnly)] = eventOnly
        eventSweep = np.roll(eventSweep, int(timeSec*self.sampleRate))
        self.sweepY = self.sweepY + eventSweep

    def addWobble(self, magnitude = 3):
        """Add a random walk to simulate slight instability."""
        walk = np.cumsum(np.random.normal(0, 1, len(self.sweepY)))
        slope = np.arange(len(self.sweepY))/len(self.sweepY)
        walk = walk - slope * walk[-1] # start and end at same point
        peak = max(np.abs(walk))
        walk = walk / (peak / magnitude)
        self.sweepY = self.sweepY + walk
        return

    def addIPSCs(self, frequencyHz=10, maxMagnitude=20):
        """Add stochastic random spontaneous IPSCs."""
        sweepLengthSec = len(self.sweepY)/self.sampleRate
        eventCount = int(frequencyHz*sweepLengthSec)
        for eventNumber in range(eventCount):
            eventPos = np.random.random() * len(self.sweepY)
            eventSec = eventPos / self.sampleRate
            eventMag = np.random.random() * maxMagnitude
            self.addPSC(eventSec, eventMag)
        return

    def plot(self):
        """Display the current sweep."""
        fig, ax = plt.subplots(figsize=(10, 4))
        plt.grid(alpha=.2, ls='--')
        ax.plot(self.sweepX, self.sweepY, color='r', lw=.5)
        plt.margins(0, .1)
        plt.title("Simulated Voltage-Clamp Sweep")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Clamp Current (pA)")
        plt.tight_layout()
        plt.show()
        return


if __name__ == "__main__":
    print("DO NOT RUN THIS FILE DIRECTLY")

    sweep = SweepVC()
    sweep.addOffset(-123)
    sweep.addWobble(2)
    sweep.addNoise(3)
    sweep.addIPSCs()
    print(sweep.sweepY)
    sweep.plot()