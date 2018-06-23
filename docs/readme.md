# pyABF Documentation
pyABF was written to be so intuitive to use (with a predictive IDE) that extensive documentation is not necessary.
The best way to learn how to interact with pyABF is to check out the [examples](getting-started), then just start using it!

## Installation

```bash
pip install --upgrade pyabf
```

## Quickstart
```python
import pyabf
abf = pyabf.ABF("demo.abf")
abf.setSweep(3) # sweeps start at 0
print(abf.sweepY) # sweep data (ADC)
print(abf.sweepC) # sweep command (DAC)
print(abf.sweepX) # sweep times (seconds)
```

## Getting Started
* [Getting Started with pyABF](getting-started) - reading ABFs and plotting sweeps with matplotlib

## Advanced Topics
* [Unofficial ABF File Format Guide](advanced/abf-file-format) - details the file structure of ABF files
* [Creating Arbitrary Stimulus Waveforms](advanced/creating-waveforms/) - creating custom stimulus waveforms from scratch with Python
* [Gaussian Filtering with Numpy](advanced/python/gaussian-filter-with-numpy.ipynb)
* [Demo data plotted with common colormaps](advanced/v1%20cookbook/2017-11-12%20colormaps/colormaps.pdf)
* [Membrane Test Theory and Analaysis Techniques](advanced/v1%20cookbook/memtest-simulation.ipynb) - including how to measure cell capacitance from voltage-clamp steps
* [pyABF V1 cookbook](advanced/cookbook) - the syntax is outdated, but some code and theory is useful
