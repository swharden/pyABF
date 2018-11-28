# pyABF for Python 2.7

**pyABF [release 2.0.27](https://github.com/swharden/pyABF/releases/tag/2.0.27) 
has been back-ported to support Python 2.**
This version of pyABF is not officially supported, can not be installed or 
upgraded with pip, and has not been extensively tested, but seems to work well
and required minimal modifications so little functionality is changed.

### Example Python 2.7 Usage
_[demo.py](demo.py) has additional lines to add the pyabf2 folder to the import path_

```python
import pyabf2
abf = pyabf2.ABF(PATH_DATA + "/171116sh_0011.abf")
for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    print "sweep %02d: %s"%(sweepNumber, abf.sweepY)
```

### Output

```
sweep 00: [-125.7324 -125.8545 -125.3662 ... -123.7793 -124.3896 -125.2441]
sweep 01: [-126.5869 -128.7842 -128.2959 ... -127.4414 -125.9766 -125.8545]
sweep 02: [-124.1455 -124.2676 -123.0469 ... -132.5683 -133.1787 -134.2773]
sweep 03: [-135.0098 -136.3525 -135.1318 ... -130.1269 -130.7373 -129.7607]
sweep 04: [-130.249  -130.3711 -130.8594 ... -128.54   -130.4931 -129.7607]
sweep 05: [-129.1504 -128.418  -128.7842 ... -128.7842 -130.249  -130.7373]
sweep 06: [-130.4931 -130.6152 -129.2724 ... -131.4697 -132.0801 -133.3008]
sweep 07: [-131.3476 -128.9062 -128.1738 ... -137.9394 -139.5264 -140.7471]
sweep 08: [-141.4795 -142.334  -141.6015 ... -129.3945 -130.1269 -130.1269]
sweep 09: [-130.9814 -130.1269 -128.7842 ... -131.2256 -131.3476 -130.9814]
sweep 10: [-129.8828 -129.2724 -128.0517 ... -127.4414 -126.4648 -126.2207]
sweep 11: [-126.709  -128.54   -128.418  ... -134.7656 -132.5683 -131.4697]
sweep 12: [-130.3711 -130.0049 -131.4697 ... -132.2021 -132.2021 -132.0801]
sweep 13: [-129.5166 -127.5635 -128.2959 ... -129.6387 -130.0049 -129.3945]
sweep 14: [-128.54   -129.0283 -128.9062 ... -131.3476 -131.5918 -130.9814]
sweep 15: [-130.9814 -132.6904 -132.9346 ... -128.9062 -128.9062 -129.0283]
sweep 16: [-128.2959 -129.5166 -130.249  ... -129.1504 -131.4697 -133.1787]
sweep 17: [-134.5215 -133.3008 -130.6152 ... -133.5449 -134.2773 -137.207 ]
sweep 18: [-138.3056 -137.9394 -137.8174 ... -130.9814 -131.2256 -130.1269]
sweep 19: [-130.4931 -131.7139 -130.3711 ... -126.0986 -126.3428 -127.4414]
```