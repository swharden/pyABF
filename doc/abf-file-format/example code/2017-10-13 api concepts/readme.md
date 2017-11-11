**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

## Notable Changes
* added protocol waveform generator.
* figured out epoch shifting

---

### Epoch/Signal misalignment
For some reason I still don't understand, some data gets recorded _before_ epoch A begins in each sweep. More confusingly, it's not a fixed amount of pre-epoch time for each sweep. Instead, ***Exactly 1/64'th of the sweep length exists in the pre-epoch area at the beginning each sweep.*** This must be taken into account if you intend to synthesize the protocol waveform from just the epoch table. This is what I've done, and these are my results.