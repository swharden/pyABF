# The pyABF Project

**The pyABF project simplifies the process of reading data from Axon Binary Format (ABF) files.** It was created with the goal of providing a Pythonic API to access the content of ABF files which is so intuitive to use (with a predictive IDE) that documentation is largely unnecessary. Flip through the [quickstart guide](https://github.com/swharden/pyABF/tree/master/docs/getting-started) and you'll be analyzing and graphing ABFs in minutes!

![](/docs/graphics/2017-11-06-aps.png)

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

## Documenation
* **[Getting Started with pyABF](/docs/getting-started)**
* [Advanced examples - typical use cases](/docs/getting-started/advanced.md)
* [Advanced examples - automated analysis with pyABFauto](https://github.com/swharden/pyABFauto)
* [Additional documentation and resources](/docs/)
* [Unofficial Guide to the ABF File Format](/docs/advanced/abf-file-format/)
* [pyABF listing on PyPI](https://pypi.org/project/pyabf/)

## Porting to Other Programming Languages
This GitHub project tracks the pyABF Python module as well as serve as a central site to aggregate ABF file format and analysis information and strategies. Code is written to be intentionally readable and efforts are taken to write and maintain documentation, making pyABF easy to port to other programming lanaguges. Some efforts to this end have already begin:

* [vsABF](https://github.com/swharden/vsABF) - A .NET library to interface to files in the Axon Binary Format (ABF)
* [phpABF](https://github.com/swharden/phpABF) - A PHP interface to files in the Axon Binary Format (ABF)

## Features
* To see some of what pyABF can do, review the [simple](/docs/getting-started) and [advanced](/docs/getting-started/advanced.md) example pages
* No obscure dependencies (just matplotlib and numpy)
* Actively developed (as of 2018)
* Pythonic API (methods and data are easy to locate with a predictive IDE)
* Cross-platform, open-source, 100% Python
* Supports 32-bit and 64-bit architectures
* Runs on Python 2.7 and Python 3.6+
* Supports ABF export (including conversion from ABF2 to ABF1 format compatible with [MiniAnalysis](http://www.synaptosoft.com/MiniAnalysis/))

![](/docs/graphics/spacer_paired_patch.jpg)
![](/docs/graphics/2017-11-18-multichannel.png)

## Citing pyABF
If the pyABF module facilitated your research, consider citing this project by name so it can benefit others too:

> _"Computational analysis of electrophysiological recordings was performed with custom software 
> written for this project using Python 3.6 and the pyABF module."_

## Feature Requests / Unsupported ABF Files
If you have ABF files which are unsupported (or read incorrectly) by this software, it is likely due to a use case we have not run across yet, so let us know about it! We can only develop and test this software against ABF files we have access to, so if you're interested in having your ABF file supported send the primary author an email (and the ABF file you are trying to analyze) and we will investigate it. If a solution is reached the pyabf package will be updated so everyone can benefit from the change. We can only develop for (and test against) ABFs we have access to, so we really appreciate your contributions!

**Scott W Harden, DMD, PhD**\
[Harden Technologies, LLC](http://tech.SWHarden.com)\
[www.SWHarden.com](http://www.SWHarden.com)\
[SWHarden@gmail.com](mailto:swharden@gmail.com)
