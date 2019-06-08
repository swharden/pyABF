# Low-Pass filtering to reduce noise

One of the most common reasons sweep data is low-pass filtered is to reduce the effects of noise. This document seeks to characterize common types of ABF noise and develop methods to optimally reduce it. Since voltage-clamp recordings are typically have more noise than current-clamp recordings, we will focus exclusively on voltage-clamp traces.

## Analyze Frequency Spectrum of Noise

What [color of noise](https://en.wikipedia.org/wiki/Colors_of_noise) makes up the "rig noise" which makes its way into ABF files? It's important to figure this out so we can best decide how to eliminate it with filtering.

Let's use `np.fft()` to measure the baseline noise in several ABFs from different sources. The [full code used](2019-06-07%20auto%20detect%20lowpass%20filter%201.py) to generate this image is available, but the important bits are here:

```python
# create a hanning-window-smoothed sweep of data to analyze
smoothedSweep = np.hanning(len(abf.sweepY)) * abf.sweepY

# convert time-domain data to frequency-domain data
fft = np.fft.fft(smoothedSweep)

# sum the absolute value of real and imaginary components
fftRight = fft[:int(len(fft)/2)]
fftLeft = fft[int(len(fft)/2):]
fft = fftRight + fftLeft[::-1]

# convert to decibels
fft = 20 * np.log10(fft)
```

![](2019-06-07%20auto%20detect%20lowpass%20filter%200.png)

The first thing you'll see is that the maximum measured frequency is different by ABF. The maximum frequency that can be measured with FFT is half the sampling frequency. ABFs here are sampled at 10 or 20 kHz, so maximum frequency we can measure is 5 kHz and 10 kHz, respectively. 

The shape of these curves look like [pink noise](https://en.wikipedia.org/wiki/Pink_noise).

There may be 60 Hz hum in there, but it seems most of the noise is stable around the 1kHz zone. Interestingly this may be because this is where hardware filers often begin to engage.

The [full code used](2019-06-07%20auto%20detect%20lowpass%20filter%201.py) to generate this image is available

## Filter Types
There are a _lot_ of filters I could apply to 1d data. A moving window method (with a Hanning window) and FFT/iFFT method seem like two strong options, and testing should determine which is computationally faster. Notice how both of these examples take in a _frequency_ cutoff. The fact that both outputs look similar means the conversions are accurate.

#### FFT / iFFT
The idea here is to convert the full sweep to the frequency domain (every value of the FFT list is a complex number with real and imaginary components), zero-out the values that correspond to frequencies outside the range we want to keep, then perform the iFFT to produce a sweep of the original length but spectrally filtered. This method is fast for long sweeps, but requires a good FFT/iFFT library (it's not trivial to implement this discretely).

```python
def lowPassIFFT(abf, kHz = .25):
    fft = np.fft.fft(abf.sweepY)
    freqs = np.fft.fftfreq(len(abf.sweepY), 1 / abf.dataRate)
    for i, freq in enumerate(freqs):
        if np.abs(freq) > kHz*1000:
            fft[i] = np.complex(0, 0)
    ifft = np.fft.ifft(fft)
    return ifft
```

#### Moving (Hanning) Window
The idea here is to create a small kernel using the Hanning function and create a moving window average (weighting by the shape of the kernel). This could be implemented discretely as a moving window function, but can be executed faster if it is converted to the frequency domain (convolution). This requires a good convolution library (it's probably slower to run if implemented discretely in the time domain because of all the floating-point multiplication).

```python
def smoothHanning(x, window_len=40):
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = np.hanning(window_len)
    f = np.convolve(w/w.sum(), s, mode='same')
    f = f[window_len-1:]
    f = f[:-window_len+1]
    return f

def lowPassHanning(abf, kHz = .25):
    windowSizePoints = int(abf.dataRate / (kHz * 1000.0))
    smooth = smoothHanning(abf.sweepY, windowSizePoints)
    return smooth
```

#### Comparison

![](2019-06-07%20auto%20detect%20lowpass%20filter%202.png)

![](2019-06-07%20auto%20detect%20lowpass%20filter%203.png)

**I prefer the window method with** the Hanning filter (or Gaussian, about the same) because the FFT/iFFT method causes ringing. It's visible on the capacitive transients of the membrane test but not in this example. I'd imagine for large (e.g., evoked) currents it could add artifacts which would interfere with analysis.

The [full code used](2019-06-07%20auto%20detect%20lowpass%20filter%201.py) to generate this image is available

## Deciding Cut-Off Frequency

Now that we have tools to low-pass filter ABFs by frequency, what frequency should the cutoff be? How should we detect this from ABF to ABF?

The ideal cutoff is whatever suppresses the most noise near the noise floor. First let's make sure we have the tools we need to calculate noise at the noise floor.

### Measuring Noise

AC noise is just random values centered at 0. In physics this is white noise (evenly distributed random values), but in practice this is mostly pink noise (which decreases with frequency) combined with white noise. To measure white noise take its standard deviation (the root of the sum of the differences from the mean squared, or "root mean squared", RMS). AC noise is commonly just reported as RMS.

A method used in QRSS to capture the noise floor is to divide a signal into small pieces, measure RMS for all of them, then choose a _percentile_ from that data which you expect to be near the noise floor. In QRSS 20% is commonly used. 

![](2019-06-07%20auto%20detect%20lowpass%20filter%201.png)

When we plot a bunch of different ABFs' percentile vs. RMS curves (1 curve per ABF), it seems anywhere between 20% and 40% is stable (mostly noise). Let's use 25% moving forward.

## Identifying Test ABFs
Initially I thought we should make a graph of RMS noise vs. different filter settings... but RMS noise is virtually entirely high frequency (way above 0.25 kHz), so I think using such a low filter frequency will kill noise regardless of how big it is. Let's test this theory on the quietest vs the noisiest ABFs. 

This is the RMS noise for every ABF on the [pyABF data](https://github.com/swharden/pyABF/tree/master/data) page, sorted by RMS noise, using the RMS value of the 25 percentile of 10 millisecond pieces from the first sweep. Understandably model cell recordings are the quietest, and recordings with continuously changing voltage are the ones with greatest RMS noise.

ABF File Name | RMS Noise (25%, 10ms)
---|---
2018_12_15_0000.abf | 0.1672 pA
pclamp11_4ch.abf | 0.171 pA
17o05024_vc_steps.abf | 1.0707 pA
17o05026_vc_stim.abf | 1.306 pA
vc_drug_memtest.abf | 1.3595 pA
18702001-pulseTrain.abf | 1.4227 pA
18702001-cosTrain.abf | 1.4459 pA
14o16001_vc_pair_step.abf | 1.4583 pA
18702001-ramp.abf | 1.459 pA
18702001-biphasicTrain.abf | 1.4591 pA
18702001-step.abf | 1.4719 pA
model_vc_step.abf | 1.4738 pA
18702001-triangleTrain.abf | 1.4755 pA
2018_11_16_sh_0006.abf | 1.5011 pA
18808025.abf | 1.7154 pA
171116sh_0011.abf | 1.769 pA
171116sh_0013.abf | 1.9147 pA
171116sh_0012.abf | 1.963 pA
model_vc_ramp.abf | 1.9696 pA
171116sh_0020.abf | 1.989 pA
171116sh_0020_saved.abf | 1.989 pA
2018_08_23_0009.abf | 2.2372 pA
16d05007_vc_tags.abf | 2.8605 pA
f1_saved.abf | 4.9329 pA

## Testing Noisy vs Quiet ABFs
Noise reduction using low-pass filtering should be ***amplitude-independent*** so it should work identically on clean and dirty ABFs. Let's put this theory to the test.

```python
plt.plot(abf.sweepX, abf.sweepY, alpha=.3)
plt.plot(abf.sweepX, lowPassHanning(abf, 1), color='k', lw=1)
```

In this graph both axes are the same span.

![](2019-06-07%20auto%20detect%20lowpass%20filter%204.png)

It looks like our expectation turned-out to be true. For sEPSCs in low noise (top) or high noise (bottom) environments, a 1ms moving window function (e.g., Hamming or Gaussian) produces output traces with similar noise while preserving the clean peaks of spontaneous EPSCs.

A note regarding event detection: A smoothed signal can be used for threshold detection (derivative detection) and calculation of peak amplitude, but it should _not_ be used for curve fitting to calculate the decay constant. The original noisy data should be retained for this purpose because data points near the peak are preserved for fitting, whereas the window method "smears" the rise phase over the peak and engages the decay phase.