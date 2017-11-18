# The pyABF Project
The pyABF project was created to simplify the process of reading data from files in the Axon Binary Format (ABF). This project contains pip-installable Python package ([pyabf](/doc/pyabf/)) which provides a simplistic front-end to directly read values and data from ABF files in Python, as well as [extensive documentation on the ABF file format](/doc/abf-file-format/) including how to read data directly from ABF files which can be applied to any programming language.

![](/doc/graphics/2017-11-06-aps.png)

# The pyabf Python Package
**The pyabf Python package** was created to provide an intuitive pythonic API front-end to access the content of ABF files. Users who are interested in working with data from ABF files in a python environment (rather than learning the byte structure of ABF headers) can simply install pyabf and interact with it directly. The pyabf Python package can be installed with pip. To see all it can do, check out the **[pyabf Python package documentation page](https://github.com/swharden/pyABF/tree/master/doc/pyabf)**

**Install or Upgrade:**
```bash
pip install pyabf --upgrade
```

**Quickstart:**
```python
import pyabf
abf=pyabf.ABF("filename.abf")
abf.info() # shows what is available
```

**Access Sweep Data:**
```python
abf.setSweep(3)
print(abf.dataY) # recorded signal
print(abf.dataX) # time points
print(abf.dataC) # command waveform
```

# Direct Extraction of Data from ABF Files
**Direct reading of ABF files** was acheived in a set of maximally-simplistic, dependency-free, standalone python files intended for functional and education use. These were created by blending information available from existing open-source code (C, C++, MatLab, and Python) with my own efforts (including a few days staring at ABF files in a hex editor). In addition to serving as the core for the pyabf package, the ABF-reading classes developed for this project were written easy portability to other lanaguges in mind (with personal interest in PHP and C#). [Extensive documentation of the ABF file format](/doc/abf-file-format) reveals how to directly extract data from ABF files, discusses strategies for maximizing performance during analysis, and is aimed at simplifying the process of extending, customizing, or porting this functionality to meet evolving use cases in the future.

* **ABF2 File Format:** [SWHarden's Unofficial ABF File Format Guide](/doc/abf-file-format)
* **Python code to read ABF data:** in the [/src/pyabf/](/src/pyabf/) folder
* **C# code to read ABF data:** in the [/dev/](/dev/) folder

---

# About the Author
As a cellular neurophysiologist / electrophysiologist, I have a lot of experience analyzing electrophysiology data with many of the currently-available software options (both free and commercial). None of these options have proven flexible enough for my style of ***exploratory data analysis*** where I pursue scientific discoveries by analyzing data in new and creative ways (necessitating the rapid creation of custom experimental software). I was motivated to create the type of library I wish I had all along, and will be happy if these efforts chip away at the ABF-reading barrier which separates creative scientists from the ability to analyze their own data. I am a strong proponent of open source software, and hope that the sharing of this project will inspire future scientists and coders as well as promote the collaborative development of software to facilitate scientific discovery and ultimately improve the lives of those who will benefit from medical and scientific advancement.

![](/doc/graphics/spacer_paired_patch.jpg)

### Feature Requests / Unsupported ABF Files
If you have ABF files which are unsupported (or read incorrectly) by this software, chances are it is simply due to a use case I have not run across yet, so I would like to know about it! I can only develop and test this software against ABF files I have access to, so if you're interested in having your ABF file supported send me an email (and the ABF file you are trying to analyze) and I will investigate it. If I come up with a solution I will update the pyabf package so everyone will benefit from the change!

### Scott W Harden
* [SWHarden.com](http://www.SWHarden.com)
* SWHarden@gmail.com
* [About Scott](https://www.swharden.com/wp/about-scott/)
