
# Case _for_ the two class model

In an effort to break-apart the core functionality of this project, the `ABFcore` class was made to contain code for ABF _file reading_ while the `ABF` class houses code for ABF _data access and manipulation_.

Higher-level _analysis_ tasks are achieved by feeding ABF objects into methods and classes specific for the analysis to be performed (e.g., action potential event detection, or power spectral analysis).

## The `ABFcore` Class

This class aims to only contain code related to ABF file reading: 

* Storage of ABF header values
  * light messaging to improve readability (e.g., abfDateTime, abfVersion)
  * creation of new useful header values (e.g., protocolPath, sTelegraphInstrument)
* Preparation of ABF data as a useful numpy array
  * Data is scaled to its meaningful value at the time it is loaded
  * Multidimensional array (one row per channel)
  * Data is one continuous array per channel and is _not_ divided into sweeps
* Stimulus (DAC) information is determined but not processed
  * Epoch tables are read, but stimulus waveforms are synthesized only when accessed
  * Custom waveforms from files are identified, but read only when accessed
* Custom modules may be used for advanced functions
  * All modules must conform to the design goals elsewhere (e.g., no obscure libraries)
  * Conversion of headers to HTML and markdown files
  * Synthesis of DAC waveforms from Epoch tables
  * Reading of ABF or ATF data for custom stimulus waveforms

## The `ABF` Class

This class aims to expand the `ABFcore` class by providing sweep-level access to ABF data. Note that data in `ABFcore` class is only divided by channel (not by sweep), so all sweep-level access and operations are provided by the `ABF` class.

The creation of baseline-subtracted sweeps and sweep averages are two extremely common sweep-level operations, so those functions are included in the ABF class, as will any future operation which acts on the sweep level.

# Case _against_ the two class model
The original design goal made more sense when both classes were approximately the same size. Now the ABFcore class has ballooned to over 500 lines and includes advanced modules/classes for web page generation, the reading of ATF files, and the generation of epoch waveforms. With so much functionality and complexity in the ABFcore class, and so little (200 lines) in the ABF class, it makes sense to combine them into a single class.