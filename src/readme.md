# pyABF v2 Developer Notes

## Justification for a new Version
pyABF v1 was written in November 2017 in parallel with my reverse-engineering of
the ABF file format (which was well-documented). As my understanding of the ABF
header structure expanded (along with bugs, unexpected use cases, and sample 
ABFs emailed to me from people who found pyABF on the internet) I developed a
strategy to code the ABF reading core again with streamlined effeciency and
simplicity. Now (June 2018) these changes will be released as pyABF v2.

## Backwards Compatibility
Unfortunately some of these changes are "breaking" changes which
may impact people who have already incorporated pyABF into their projects, but
I am trying as hard as I can to make the transition as simple as possible.
I am highly motivated to prevent making any breaking changes moving forward. 
Re-writing documentation pages and test code is exhausting.

## Summary of Changes
As with pyABF version 1, the end user is only expected to instantiate the `ABF`
class (passing in the path to an ABF file). All ABF information and data can be
accessed by interacting with that ABF object.

* Every element in the ABF header is now a solid python object (not parsed strings stored in a dictionary), so header elements can be accessed via your predictive IDE.
* Enhanced multi-channel support for scaling, units, and protocol information
* The `ABF` class provides high level functions to work with ABF files. It is relatively light in code and easy to modify to change high-level interactivity behavior. End users only need to instantiate this class.
* The `ABFCore` class (inherited by `ABF`) provides abstract access to common ABF elements (data, channel units, comments) identically supporting ABF1 and ABF2 file formats.
* Analysis (event detection, membrane test, sweep averaging, baseline subtraction) have been moved into an analysis module

-------
# MISC THOUGHTS
-------

# Object Model
## ABF
* Objects
  * Sweep
  * Core
  * sweepCount
  * sweepList
* Methods
  * info()
  * help()

## Sweep
* Objects
  * timeStartSec
  * timeStartMin
  * sweepNumber
  * x
  * xUnits
  * xUnitsLong
  * y
  * yUnits
  * yUnitsLong
* Methods
  * setSweep(sweepNumber(s), channel)
  * setAverage(sweepNumbers, channel)
  

## Core
* Objects
  * header stuff
  * timeCreated
  * durationSeconds
  * sweepCount


# Thoughts
What use cases do we actually have?

* plotting sweeps
  * one sweep at a time (maybe overlap)
  * continuous series of sweeps
  * average of some sweeps
* plotting data
  * average of some range (baseline)
  * event detection
  * intrinsic properties measurement