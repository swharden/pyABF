
# Core pyABF API

This document is generated automatically by the test script [api.py](api.py)
which attempts to enforce the preservation of core API functionality. While
new features may be added to pyABF in the future, extreme efforts will be taken
to preserve these core API functions (evidenced by the passing of this test 
script).



## ABF object properties
_Extreme efforts are taken to prevent modification of these components._

* abfDateTime - the exact time (or best guess) for when the ABF was made
* abfDateTimeString - abfDateTime formatted as str
* abfFileComment - comment defined in the waveform editor
* abfFilePath - full path to the ABF file
* abfID - abf filename (basename) without extension
* abfVersion - dictionary containing 4 levels of version information
* abfVersionString - version string formatted as 'x.x.x.x'
* adcNames - list containing names of each ADC channel
* adcUnits - list containing units of each ADC channel
* channelCount - numer of ADC channels
* channelList - a list of ADC channels (range(channelCount))
* creatorVersion - dictionary containing 4 levels of version information
* creatorVersionString - creatorVersion string formatted as 'x.x.x.x'
* dataByteStart - location of first byte of data in the file
* dataPointByteSize - byte size of each data point
* dataPointCount - number of total data points
* dataPointsPerMs - rate / 1000
* dataRate - data points per second
* dataSecPerPoint - inverse of rate
* fileGUID - globally unique file identifier (string formatted)
* protocol - the filename (basename) of the protocol file without extension
* protocolPath - full path to the protocol file
* sweepCount - number of sweeps in the file
* sweepLengthSec - length of each sweep in seconds
* sweepList - a list of ADC channels (range(sweepCount))
* sweepPointCount - number of data points in each sweep

#### Unstable ABF properties:
_These components may change in the future..._

* holdingCommand - a list of holding values (one per DAC)
* stimulusByChannel - special class to work with epoch and custom stimuli




## Direct access to signal data

* Direct signal data exists in `abf.data`.
* Its rows are channels.
* It's one continuous array for the entire data.
* It is not divided into sweeps.



## Access to sweep data (with setSweep)

* abf.setSweep() pulls data from abf.data and populates:
    * abf.sweepX - time of the sweep 
    * abf.sweepY - values of the sweep
    * abf.sweepC - command waveform for this sweep
    * abf.sweepD(outChannel) - generate waveform a digital output

_Passing absoluteTime=True means abf.sweepX is returned in absolute time
units (the time position of the sweep in the recording), otherwise 
abf.sweepX always starts at zero._

* Extra values populated by setSweep() include:
    * abf.sweepChannel - channel of the set sweep
    * abf.sweepNumber - number of the set sweep
    * abf.sweepLabelX - time label (suitable for X axis label)
    * abf.sweepLabelC - command waveform label (suitable for Y axis label)
    * abf.sweepLabelY - signal label (suitable for Y axis label)
    * abf.sweepUnitsX - sweep time units (usually 's')
    * abf.sweepUnitsC - sweep command units (usually 'pA' or 'mV')
    * abf.sweepUnitsY - sweep signal units (usually 'pA' or 'mV')


