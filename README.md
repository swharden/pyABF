# pyABF
**pyABF is a project created to simplify the reading of data from files in the Axon Binary Format (ABF).** At the core of this project is an ABF file reading class (written in Python) which is fully portable (a single file which can be placed inside any project) or can be installed via pip. It has no dependencies outside the standard libraries, works on all Python 3 distributions, and was designed to be easily ported to other programming languages.

**Documentation and Resources:**
* My [Unofficial ABF File Format Guide](/doc/abf-file-format)
* The official [Axon Binary File (ABF) Format](https://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf) document
* [Axon pCLAMP ABF SDK](http://mdc.custhelp.com/app/answers/detail/a_id/18881/~/axon%E2%84%A2-pclamp%C2%AE-abf-file-support-pack-download-page)
* [Neo](https://github.com/NeuralEnsemble/python-neo)
* [StimFit](https://github.com/neurodroid/stimfit)
* [SWHLab](https://github.com/swharden/SWHLab)

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
