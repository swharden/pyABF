**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

## Notable Changes
* All ABF header code (structures and display functions too) are in a single header.py file. This file is kept intentionally simple (and well documented) to make it easy to port this class to other languages. It has *NO* dependencies, even though other parts of the pyABF project do (i.e., numpy and matplotlib). This file has minimal data access functions (for getting sweeps or getting data between arbitrarily time points) but it is left to the end user to multiply it by the scale factor. If vector math is availale, that's the way to go.
* ***I LEFT THIS CODE AS A FUNCTIONING FILE OPEN/CLOSE STRESS TEST!!!***

---

## Thoughts on file access and storing data in memory
Every ABF reading API probably has something like a `getSweepData(sweepNumber)` function which returns the data for that sweep. My goal is to design an ABF class which provides access to sweep data in the best way. I there are a few ways I can think of to go about this, each with different pros and cons.

* *ClampFit uses option 1.* - Pain in the butt becausae you can't view an ABF on a network drive if it's open on someone elses's computer.
* *abffio.dll uses option 2* - but I'm not 100% on this
* *I'm leaning toward option 3* - because I hate file blocking and I hate initiating the reading bytes over network drives

**OPTION 1 - Keep the ABF file open:** Open the ABF file for buffered reading when the header reading class is instantiated and leave it open. It's already open when we request a sweep's data, so just seek() to that position and return the file's contents.
  * **PRO:** opening the file takes a little bit of time (more on network drives) and so we save time by calling it once.
  * **CON:** The file is locked open until the user manually destroys the class or calls file.close(). Open ABF files can not be viewed by ClampFit or abffio.dll (orly?)

**OPTION 2 - Open the ABF when reading a sweep:** The goal here is to only have the ABF open when it's needed (once to read the header, then every time a sweep is requested). 
  * **PRO:** only blocks file when sweeps are requested
  * **PRO:** the user never has to manually close the file
  * **CON:** the small amount of time it takes to open/close a file is multiplied by the number of times a a sweep is requested. This becomes much slower on network drives.
  
**OPTION 3 - Load all sweep data in memory:** We could open the file just once to read the header then load ALL the signal data into memory and close the file forever. It isn't _that_ much memory. A 16-bit 20khz signal only takes up 40kB/sec (2.4 MB/min). A whole hour of recording is 144 MB. ***Attention should be paid to the format of storage!*** The data loaded from the ABF is `int16`, so mindlessly converting it to floats could easily double (`float16` half precision) or quadruple (`float32` single precision) memory requirements. However, since we know data will be converted to a float eventually (when multiplied by its scaling factor), maybe we can save time by doing the conversion when the data is loaded. Doubling the memory requirement (288 MB / hr of recording) would prevent the need for integer-to-float conversion and data scaling (float multiplication) later, improving performance.

  * **PRO:** no file blocking
  * **PRO:** file opening/closing time is eliminated (big pro for network drives)
  * **PRO:** on-demand file _reading_ time is eliminated (big pro for network drives)
  * **CON:** class instantiation time is increased, but this could be disabled with an argument
  
  