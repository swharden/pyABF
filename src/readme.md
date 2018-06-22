# pyABF source code

README.rst is the index page for pypi: https://pypi.org/project/pyabf/

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

## Documenation
* [Getting started with pyABF](../docs/getting-started)
* [Additional documentation](../docs/)