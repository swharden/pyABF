# pyABF
**pyABF is a project created to simplify the reading of data from files in the Axon Binary Format (ABF).** At the core of this project is an ABF file reading class (written in Python) which is fully portable (a single file which can be placed inside any project) or can be installed via pip. It has no dependencies outside the standard libraries, works on all Python 3 distributions, and was designed to be easily ported to other programming languages.

![](/doc/graphics/2017-11-06-aps.png)

## Python Package (pyabf)
The pyabf package is listed in the Python Package Index: https://pypi.python.org/pypi/pyabf/

**Installation:**
```bash
pip install pyabf
```

**Upgrade:**
```
pip install pyabf --upgrade
```

**Testing your installation:**
```python
import pyabf
pyabf.info()
```

## Documentation
* **[SWHarden's Unofficial ABF File Format Guide](/doc/abf-file-format)** is a work in progress, but very handy.

## Sample Code
I strive to invest at least as much effort into the documentation as I do the code itself. If you are a developer interested in accessing header and signal data from ABF files, you will find many standalone scripts and notes in the [example code folder](/doc/abf-file-format/example%20code). If I make a proof-of-concept script to test an idea, I give it its own folder and write my conclusions alongside the original code (whether the original idea worked or not).

## Additional Resources
* The official [Axon Binary File (ABF) Format](https://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf) document
* [Axon pCLAMP ABF SDK](http://mdc.custhelp.com/app/answers/detail/a_id/18881/~/axon%E2%84%A2-pclamp%C2%AE-abf-file-support-pack-download-page)
* [Neo](https://github.com/NeuralEnsemble/python-neo)
* [StimFit](https://github.com/neurodroid/stimfit)
* [SWHLab](https://github.com/swharden/SWHLab)
