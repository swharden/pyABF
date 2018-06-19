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