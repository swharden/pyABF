**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

## Notable Changes
* The header format is now an [ordered dictionary](https://docs.python.org/2/library/collections.html)
  * This retains the order of all the sections and variables rather than mashing them up into a huge crazy list which can only be organized alphabetically.
  * I add section names as header dictionary entries so we know down the road which variables go to which section. It also greatly helps the display of the header (or its formatting when saved as HTML or markdown)
* I started an `ABF` class which is the only thing the user will interact with
  * end users never interact with the `ABFheader` class.
  * the first line of the `ABF` class is just `self.header=ABFheader(abfFile).header`. This provides excellent separation between work related to the ABFheader (which is a work in progress) and work related to _using_ data from ABFs (graphing, measuring, etc).
  * abf header tools ([abfHeaderTools.py](abfHeaderTools.py)) can be used to display the header or save it as HTML ([demo.html](demo.html)) or markdown ([demo.md](demo.md))
  * this will contain functions like `getSweepData(sweepNumber)`