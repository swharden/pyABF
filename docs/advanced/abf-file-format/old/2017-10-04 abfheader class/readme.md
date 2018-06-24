**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

# Standalone ABFheader class
The class in [abfHeader.py](abfHeader.py) contains everything needed to extract header information and
sweep data from an ABF file. [abfTools.py](abfTools.py) has functions to create pretty HTML files from
an ABFheader object. (Sample output HTML files are in [html-output/](html-output/))

# Usage
```python
import abfTools
import abfHeader
header=abfHeader.ABFheader(abfFileName)
abfTools.headerToHTML(header)
```