---
title: pyABF - A Simple Python Library for Working with ABF Files
description: pyABF is a simple Python interface for Axon Binary Format (ABF) files
---

# pyABF

**pyABF is a Python package which simplifies the process of reading electrophysiology data from Axon Binary Format (ABF) files.** It was created with the goal of providing a Pythonic API to access the content of ABF files which is so intuitive to use (with a predictive IDE) that documentation is largely unnecessary. Flip through the [quickstart tutorial](tutorial) and you'll be analyzing and graphing ABFs in minutes!

<div class="text-center">

![](graphics/action-potentials-small.png)

</div>

## Installation

pyABF supports Python 3.6+ and is available on [PyPi](https://pypi.org/project/pyabf/):

```
pip install --upgrade pyabf
```

## Quickstart
```python
import pyabf
abf = pyabf.ABF("demo.abf")
abf.setSweep(sweepNumber: 3, channel: 0)
print(abf.sweepY) # displays sweep data (ADC)
print(abf.sweepX) # displays sweep times (seconds)
print(abf.sweepC) # displays command waveform (DAC)
```

## Plot Sweeps with Matplotlib
```python
import matplotlib.pyplot as plt
import pyabf
abf = pyabf.ABF("demo.abf")
abf.setSweep(14)
plt.plot(abf.sweepX, abf.sweepY)
plt.show()
```

## Tutorial
* The [pyABF tutorial](tutorial) demonstrates how to use the common features of pyABF
* Advanced topics reviewed on the [advanced page](advanced) include:
  * access data from multiple channels
  * generate command stimulus waveform
  * measure access resistance
  * calculate whole-cell capacitance
  * work with digital output waveforms

## Features
* No obscure dependencies (just matplotlib and numpy)
* Actively maintained (as of 2020)
* Pythonic API (methods and data are easy to locate with a predictive IDE)
* Cross-platform, open-source, 100% Python
* Supports 32-bit and 64-bit architectures
* Supports Python 3.6+ (pyabf 2.1.10 supports Python 2.7 and 3.5)
* Can read ABF1 and ABF2 files (including ABF 2.9 files created by pCLAMP 11)
* Can write ABF files (including ABF2 to ABF1 conversion for [MiniAnalysis](http://www.synaptosoft.com/MiniAnalysis/))
* Stimulus waveform generation from epoch information
* Access to digital output settings and waveforms
* Can load waveforms from external ABF and ATF stimulus files (with caching)

<div class="text-center">

![](graphics/pyabf-example-action-potentials.jpg)

</div>

## Citing pyABF
If the pyABF module facilitated your research, consider citing this project by name so it can benefit others too:

> "Analysis of electrophysiological recordings was performed with custom software written for this project using Python 3.7 and the pyABF module¹."<br><br>[1] Harden, SW (2020). pyABF 2.2.3. [Online]. Available: https://pypi.org/project/pyabf/, Accessed on: Sep. 24, 2019.

## Author
pyABF was created by [Scott W Harden](https://www.swharden.com/about) ([Harden Technologies, LLC](http://tech.swharden.com/)) with many contributions from the open-source community