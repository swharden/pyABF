# The pyabf Python Package
The pyabf package was created to ***facilitate exploratory analysis of electrophysiological data*** by providing a simple object model through which to interact with it (a model so intuitive that documentation is not required). The pyabf package was designed as a tool for neurophysiology data exploration, rather a product aimed at data presentation.
  
**Quick Start:** After installing with `pip install pyabf`, run the following code. If you use a predictive IDE (like [spyder](https://pypi.python.org/pypi/spyder) or the [IDLE editor](https://en.wikipedia.org/wiki/IDLE)) or python shell (like [IPython](https://ipython.org) or the [IDLE shell](https://en.wikipedia.org/wiki/IDLE)) you should immediately understand how access all features of this package without reading any additional documentation.

```python
import pyabf
abf=pyabf.ABF("filename.abf")
abf.info()
```


# Package Details

The pyabf package is a sub-component of [the pyABF project](https://github.com/swharden/pyABF). The pyABF project as a whole provides numerous additional resources, code examples, performance assessments, ABF file format information, and even notes for writing ABF-reading code in additional programming languages. If you just want to access some data from ABF files using python, the pyabf package is for you! If you are a developer interested in working with ABF files, review all folders in this project.

### Features
* Can be installed (and upgraded) with pip
* Use is so intuitive that documentation is not required
* Extreme effort has gone into maximizing performance
* Does not require niche libraries which frequently break (e.g., quantities)
* Written for Python 3 and works on 32-bit and 64-bit systems

### Limitations

* Basic Python experience is required, as no GUI is (or will ever) be provided
* This module was designed with single-channel ABF2 files in mind.
  * Additional modes are likely supported, but have not been tested
  * The ABFHeader class is easy to modify to implement these features
  * I have made an extensive [ABF File Format](https://github.com/swharden/pyABF/tree/master/doc/abf-file-format) guide to make expansion simple

## Using pyabf with pip

* Install: `pip install pyabf`
* Upgrade: `pip install pyabf --upgrade`
* Uninstall: `pip uninstall pyabf`
* Anaconda users: Run these commands in the _Anaconda Prompt_ (not the windows command prompt) too avoid permissions errors.

```python
import pyabf
pyabf.info() # display package version and location
```
  
## Using pyabf from a source code folder
This is typcailly what I do while developing this project.
```python
import sys
sys.path.append(R"path/to/pyABF/src/")
import pyabf
pyabf.info() # display package version and location
```

_If pyabf is installed with pip but you wish to manually import the version in this source folder, use `sys.path.insert(0,R"path/to/pyABF/src/")` so python imports the local one instead of the installed one._

# Additional pyabf Examples
  
#### Graph ABF Data with Matplotlib
```python
import pyabf
import matplotlib.pyplot as plt
abf=pyabf.ABF("filename.abf")
plt.figure(figsize=(8,4))
for sweepNumber in abf.sweepList:
	abf.setSweep(sweepNumber)
	plt.plot(abf.dataX,abf.dataY)
plt.ylabel(abf.unitsLong)
plt.xlabel(abf.unitsTimeLong)
plt.title(abf.ID)
plt.margins(0,.1)
plt.show()
```

![](/doc/graphics/2017-11-11-a.png)