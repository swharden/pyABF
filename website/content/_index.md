---
title: pyABF - A Simple Python Library for Working with ABF Files
description: pyABF is a Python package for reading electrophysiology data from Axon Binary Format (ABF) files
---

**pyABF is a Python package for reading electrophysiology data from Axon Binary Format (ABF) files.** In contrast to the official interface (a 32-bit Windows-only DLL), pyABF is written in pure Python and runs on all operating systems (including 64-bit environments). PyABF's API aims to be intuitive enough that when used with a predictive IDE, documentation is largely unnecessary.

<img src="graphics/action-potentials-small.png" class="d-block mx-auto my-4">

## Installation

[pyABF is available on PyPi](https://pypi.org/project/pyabf/) and can be installed with pip:

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

## Documentation
* The [**pyABF tutorial**](tutorial) demonstrates how to use the common features of pyABF

## Resources
* [Unofficial Guide to the ABF File Format](abf2-file-format)
* [Notes about the legacy ABF1 File Format](abf1-file-format)
* [Create stimulus waveforms with Python](https://github.com/swharden/pyABF/tree/main/dev/docs-old/advanced/creating-waveforms)
* [Electrophysiology traces plotted with all matplotlib colormaps](graphics/colormaps.pdf)
* [Membrane Test Theory and Analaysis Techniques](https://swharden.com/blog/2020-10-11-model-neuron-ltspice/)
* [Alternative capacitance calculation method: the "vee" protocol](https://swharden.com/blog/2020-10-11-model-neuron-ltspice/#use-a-voltage-clamp-ramp-to-measure-cm)
* [ABFsharp](https://github.com/swharden/ABFsharp) - A C# interface for ABF files

## Features
* No obscure dependencies (just matplotlib and numpy)
* Battle-tested and actively maintained (2017 - present)
* Pythonic API (methods and data are easy to locate with a predictive IDE)
* Pure python package with full cross-platform support (32-bit and 64-bit)
* Can read ABF1 and ABF2 files (including ABF 2.9 files created by pCLAMP 11)
* Can convert ABF2 to ABF1 format to allow analysis with legacy software
* Epoch table stimulus waveforms can be generated
* Automatically integrates with external ABF and ATF stimulus files
* Digital output waveforms can be accessed

<img src="graphics/pyabf-example-action-potentials.jpg" class="d-block mx-auto my-5">

## How to Cite pyABF

If pyABF facilitated your research, consider citing this project so it can benefit others too:

> "Analysis of electrophysiological recordings was performed with custom software written for this project using Python 3.10 and the pyABF package¹."
> <br><br>
> [1] Harden, SW (2022). pyABF 2.3.5. [Online]. Available: https://pypi.org/project/pyabf