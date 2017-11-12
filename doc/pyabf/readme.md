# The pyabf Python Package
The pyabf package was created to ***facilitate exploratory analysis of electrophysiological data*** by providing a simple object model through which to interact with it (a model so intuitive that documentation is not required). The pyabf package was designed as a tool for neurophysiology data exploration, rather a product aimed at data presentation.

The pyabf package is a sub-component of [the pyABF project](https://github.com/swharden/pyABF). The pyABF project as a whole provides numerous additional resources, code examples, performance assessments, ABF file format information, and even notes for writing ABF-reading code in additional programming languages. If you just want to access some data from ABF files using python, the pyabf package is for you! If you are a developer interested in working with ABF files, review all folders in this project.
  
**Install or Upgrade:**
```bash
pip install pyabf --upgrade
````


**Quickstart:**
```python
import pyabf
abf=pyabf.ABF("filename.abf")
abf.info()
```

_TIP: If you use a predictive python editor (like [Spyder](https://pypi.python.org/pypi/spyder), [IDLE](https://en.wikipedia.org/wiki/IDLE), [IPython](https://ipython.org), or [Jupyter](http://jupyter.org)) will immediately be able to use most of the features of this package without requiring any additional documentation._

![](/doc/graphics/2017-11-06-aps.png)

# Package Details

### Features
* Can be installed (and upgraded) with pip
* Use is so intuitive that documentation is not required
* Extreme effort has gone into maximizing performance
* Does not require niche libraries which frequently break (e.g., quantities)
* Written for Python 3 and works on 32-bit and 64-bit systems

### Limitations

* Basic Python experience is required to use pyabf
  * no GUI is (or will ever) be provided
* This module was designed with single-channel ABF2 files in mind.
  * Additional modes are likely supported, but have not been tested
  * The ABFHeader class is easy to modify to implement these features
  * I have made an extensive [ABF File Format](https://github.com/swharden/pyABF/tree/master/doc/abf-file-format) guide to make expansion simple
  * Support for additional features [can be requested](https://github.com/swharden/pyABF#feature-requests--unsupported-abf-files) from the author

### Comparison to Similar Software Projects
* **Clampex** - ABF viewer as part of Molecular Devices pCLAMP
  * Commercial, not free, closed source, Windows-only software
  * Point-and-click only, not scriptable
  * Widely adopted / trusted for basic analysis
  * See the pCLAMP 10 [brochure](http://www.aryoazma.biz/Upload/Modules/Contents/asset0/asset1567/Electrophysiologysoftware.pdf) and [user Guide](https://neurophysics.ucsd.edu/Manuals/Axon%20Instruments/pCLAMP10-User-Guide-RevA.pdf)
* **Official pClamp SDK** - abffio.dll
  * Freely available for any use on [their website](http://mdc.custhelp.com/app/answers/detail/a_id/18881/~/axon™-pclamp®-abf-file-support-pack-download-page)
  * Poorly-written [user guide](http://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf) with no ready-to-compile code examples
  * Source code for the DLL is not provided
  * DLL is 32-bit only
  * Documentation is limited to using the DLL, not reading ABF files directly
  * Structs are defined in ABFHEADR.H (which is a good read)
* **Stimfit** - free open-source program to view/analyze electrophysiological data
  * Uses Python, but is a compiled program which ships with a Python interpreter
  * ABF file parser written in C++ ([source code available](https://github.com/neurodroid/stimfit/tree/master/src/libstfio/abf/axon2))
  * GUI-based program (writtein in C++)
  * The python module [can be interfaced directly](https://neurodroid.github.io/stimfit/linux_install_guide/moduleonly.html) but only with Python 2.x
  * Python code is not available for Python 3, and is not listed in PyPi
  * Python access to ABF data only occurs through their compiled code
* **Neo** - A python package which can read many electrophysiology formats (including ABF)
  * [http://neo.readthedocs.io/en/latest/](http://neo.readthedocs.io/en/latest/)
  * Neo is a fantastic effort and one of the best currently-available methods to read ABF data in Python
  * The code to read ABF files [axonrawio.py](https://github.com/NeuralEnsemble/python-neo/blob/master/neo/rawio/axonrawio.py) is poorly documented, non-pythonic, and hard to understand.
  * Some features are absent (e.g., reading digital output signals)
  * ABF header is represented as a massive and complex python dictionary of dictionaries of dictionaries of dictionaries - 4 levels deep! I tried to make sense of it by converting the crazy python object to HTML and [rendering it as a PDF](/doc/graphics/neo-io-header.pdf). Compare this to the [pyabf header format](/doc/graphics/pyabf-header.pdf).
  * Since it was designed to support many formats (including things like EEG and tetrode recordings), the API was not created with ABF files specifically in mind. Therefore, the API is not intuitive to use for many python developers, and likely cannot be used to plot ABF data without first reading extensive documentation.
  * Neo uses [quantities](https://pypi.python.org/pypi/quantities) as a dependeny. Quantities was [broken](https://github.com/python-quantities/python-quantities/issues/122) for 16 months (April 2016 - August 2017) such that `pip install quantities` would fail. This automatically broke all of my projects which used neo (preventing me from being able to upgrade them with pip) for over a year. While I could overcome these issues by manually installing quantities and neo, not being able to use pip to upgrade my own software reminded me of the importance of standalone packages which do not require niche dependencies.  This is why the core ABFheader class of the pyabf package uses just the standard libraries and no dependencies.
  
_If you are aware of a similar project (especially a Python one) I have not listed, let me know about it!_
  
### Importing pyabf from a specific folder
To pyabf package residing in a specific folder (e.g., a GitHub download) rather than importing it from a folder pip may have installed on your system, add the local path to your system path list prior to its import. This is useful when working on development versions of the package.

**Add this to the top of your code:**
```python
import sys
sys.path.append(R"C:\Users\scott\Documents\GitHub\pyABF\src")
sys.path.insert(0,sys.path.pop()) # moves it to the top of the list
```

**Then import like normal:**
```
import pyabf
pyabf.info()
```

_Note: the append statement is recognized by most IDEs so auto-complete / predictive text can occur while working on the file. The insert statement removes that entry from the last posistion and re-inserts it at the top of the list. This causes python to preferentially import from the specificed path even if a pip-installed version is available system-wide._

# Additional pyabf Examples

***NOTE: A COOOKBOOK IS IN DEVELOPMENT***
  
## Graph ABF Data with Matplotlib
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