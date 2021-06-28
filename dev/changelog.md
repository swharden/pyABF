# pyABF 2.3.0
* Improved support for user lists (#110) _Thanks @haganenoneko_
* ABFs with invalid dates no longer display a warning when they are loaded (#113)
* ABF and ATF now can also be instantiated with a `pathlib.Path` instead of just `str` (#112)
* Improved data scaling for ABF1 files with out-of-order ADC channels