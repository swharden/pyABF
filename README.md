# <img src="dev/icon/icon.ico" height="24" width="24"> pyABF
[![CI](https://github.com/swharden/pyABF/actions/workflows/ci.yaml/badge.svg)](https://github.com/swharden/pyABF/actions/workflows/ci.yaml)
[![Website](https://github.com/swharden/pyABF/actions/workflows/website.yaml/badge.svg)](https://github.com/swharden/pyABF/actions/workflows/website.yaml)
[![](https://img.shields.io/pypi/v/pyabf?label=pyabf&logo=python&logoColor=white)](https://pypi.org/project/pyabf/)
[![Downloads](https://pepy.tech/badge/pyabf)](https://pepy.tech/project/pyabf)
[![Downloads](https://pepy.tech/badge/pyabf/month)](https://pepy.tech/project/pyabf)

**pyabf is a Python library for reading electrophysiology data from Axon Binary Format (ABF) files.** It was created with the goal of providing a Pythonic API to access the content of ABF files which is so intuitive to use (with a predictive IDE) that documentation is largely unnecessary. Flip through the **[pyabf Tutorial](https://swharden.com/pyabf/tutorial)** and you'll be analyzing data from your ABF files in minutes!

<p align="center">
<img src='dev/graphics/2017-11-06-aps.png'>
</p>

### Installation
```bash
pip install --upgrade pyabf
```

### Quickstart
```python
import pyabf
abf = pyabf.ABF("demo.abf")
abf.setSweep(3)
print(abf.sweepY) # displays sweep data (ADC)
print(abf.sweepX) # displays sweep times (seconds)
print(abf.sweepC) # displays command waveform (DAC)
```

### Resources
* [pyabf Website](http://swharden.com/pyabf/)
* [pyabf Tutorial](https://swharden.com/pyabf/tutorial)
* [Advanced Topics](https://swharden.com/pyabf/#resources)
* [ABF File Format](https://swharden.com/pyabf/abf2-file-format)
* [AbfSharp](https://github.com/swharden/ABFsharp) - a C#/.NET interface for ABF files

<p align="center">
<img src='dev/graphics/stacked-traces.jpg'>
</p>
