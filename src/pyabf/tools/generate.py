"""
Code here relates to the from-scratch creation of data which simulates
electrical recordings of neurons. Creating data from scratch is useful 
because (1) you can generate your own ABFs to analyze without requiring
access to real recordings and, (2) generating data with known events allows you
to test your event detection code to ensure the results are what you expect.
Same goes for simulating membrane tests, then analyzing them.
"""

import numpy as np

def generate_exp(tauMs=100, rateHz=20000, filterHz=2000):
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


def generate_alpha(tauMs=100, rateHz=20000):
    """
    Create a signal similar to an EPSP or IPSP with a slow rise and decay. 
    """
    eventPoints = tauMs * rateHz / 2000
    xs = np.arange(eventPoints)
    alpha = 10/eventPoints
    data = alpha**2*xs*np.exp(-alpha*xs)
    data /= np.max(data)
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


class SynthSweep:

    def __init__(self, sampleRate=20000, sweepLengthSec=5, voltageClamp=True):
        self.sampleRate = int(sampleRate)
        pointCount = sampleRate*sweepLengthSec
        self.sweepY = np.zeros(pointCount)
        self.sweepX = np.arange(pointCount)/sampleRate
        if voltageClamp:
            self.clampMode = "Voltage Clamp"
            self.units = "pA"
            self.unitsLong = "Clamp Current (pA)"
        else:
            self.clampMode = "Current Clamp"
            self.unitsY = "mV"
            self.unitsLong = "Membrane Potential (mV)"

    def addOffset(self, offset):
        """Add a fixed offset (pA) to the trace."""
        self.sweepY += offset

    def addNoise(self, magnitude=3):
        """Add normal (gaussian) noise to the trace."""
        noise = np.random.normal(0, magnitude/10, len(self.sweepY))
        self.sweepY = self.sweepY + noise

    def addWobble(self, magnitude=3):
        """Add a random walk to simulate slight instability."""
        walk = np.cumsum(np.random.normal(0, 1, len(self.sweepY)))
        slope = np.arange(len(self.sweepY))/len(self.sweepY)
        walk = walk - slope * walk[-1]  # start and end at same point
        peak = max(np.abs(walk))
        walk = walk / (peak / magnitude)
        self.sweepY = self.sweepY + walk
        return

    def addEvent(self, timeSec=1.23, magnitude=20, tauMs=100, excitatory=True):
        """Add a single post-synaptic event at a given time point."""
        if self.clampMode == "Voltage Clamp":
            # in voltage clamp events are monoexponential shape
            eventOnly = generate_exp(tauMs) * magnitude
            if excitatory == True:
                eventOnly *= -1
        else:
            # in current-clamp events are alpha shape (~integrated alpha)
            eventOnly = generate_alpha(tauMs) * magnitude
            if excitatory == False:
                eventOnly *= -1
        eventSweep = np.zeros(len(self.sweepY))
        eventSweep[:len(eventOnly)] = eventOnly
        eventSweep = np.roll(eventSweep, int(timeSec*self.sampleRate))
        self.sweepY = self.sweepY + eventSweep

    def addEvents(self, frequencyHz, maxMagnitude=10, tauMs=100, excitatory=True, AP=False):
        """Add stochastic spontaneous post-synaptic currents or potentials."""

        # create list of event times
        sweepLengthSec = len(self.sweepY)/self.sampleRate
        eventCount = int(frequencyHz*sweepLengthSec)
        eventPositions = np.random.random_sample(eventCount)  # 0-1
        eventPositions *= len(self.sweepY)
        eventPositions = np.sort(eventPositions)
        lastEventPos = 0
        for eventPos in eventPositions:
            eventSec = eventPos / self.sampleRate
            eventMag = np.random.random() * maxMagnitude
            if AP:
                # add an action-potential (combination of several alphas)
                secSinceLastEvent = (eventPos-lastEventPos)/self.sampleRate
                if secSinceLastEvent<.1:
                    continue
                self.addEvent(eventSec, 100, 10, True)  # fast rise
                self.addEvent(eventSec, 10, 40, False)  # fast fall
                self.addEvent(eventSec, 2, 200, False)  # slow AHP
            else:
                # add a spontaneous synaptic event (an exponential or alpha)
                self.addEvent(eventSec, eventMag, tauMs=tauMs,
                              excitatory=excitatory)
            lastEventPos = eventPos
        return

    def addGlutamate(self, frequencyHz, maxMagnitude):
        """Add spontaneous excitatory post-synaptic currents or potentials."""
        tauMs = 50
        if self.clampMode != "Voltage Clamp":
            tauMs *= 4
        self.addEvents(frequencyHz, maxMagnitude, tauMs=tauMs, excitatory=True)
        return

    def addGABA(self, frequencyHz, maxMagnitude):
        """Add spontaneous inhibitory post-synaptic currents or potentials."""
        tauMs = 200
        if self.clampMode != "Voltage Clamp":
            tauMs *= 4
        self.addEvents(frequencyHz, maxMagnitude,
                       tauMs=tauMs, excitatory=False)
        return

    def addAPs(self, frequencyHz):
        """Add spontaneous action potentials (Poisson distributed)."""
        self.addEvents(frequencyHz, AP=True)

    def plot(self, show=False):
        """Display the current sweep."""
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 4))
        plt.grid(alpha=.2, ls='--')
        ax.plot(self.sweepX, self.sweepY, color='r', lw=.5)
        plt.margins(0, .1)
        plt.title("Simulated %s Sweep" % self.clampMode)
        plt.xlabel("Time (seconds)")
        plt.ylabel(self.unitsLong)
        plt.tight_layout()
        if show:
            plt.show()
        return


def _demo_EPSCs_IPSCs():
    """Create a lifelike sweep containing sEPSCs and sIPSCs."""
    sweep = SynthSweep()
    sweep.addOffset(-123)
    sweep.addWobble(2)
    sweep.addNoise(3)
    sweep.addGlutamate(frequencyHz=10, maxMagnitude=20)  # glutamate
    sweep.addGABA(frequencyHz=20, maxMagnitude=5)  # GABA
    sweep.plot()


def _demo_EPSPs_IPSPs():
    """Create a lifelike sweep containing sEPSPs and sIPSPs."""
    sweep = SynthSweep(voltageClamp=False)
    sweep.addOffset(-70)
    sweep.addWobble(1)
    sweep.addNoise(1)
    sweep.addGlutamate(frequencyHz=20, maxMagnitude=5)  # glutamate
    sweep.addGABA(frequencyHz=10, maxMagnitude=2)  # GABA
    sweep.plot()


def _demo_AP():
    sweep = SynthSweep(voltageClamp=False)
    sweep = SynthSweep(voltageClamp=False)
    sweep.addOffset(-70)
    sweep.addWobble(3)
    sweep.addNoise(1)
    sweep.addAPs(10)
    sweep.plot()


if __name__ == "__main__":
    print("DO NOT RUN THIS FILE DIRECTLY")
    import matplotlib.pyplot as plt
    _demo_EPSCs_IPSCs()
    _demo_EPSPs_IPSPs()
    _demo_AP()
    plt.show()