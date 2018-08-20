# pyABF Design Goals

**The core goal of pyABF is to simplify the process of reading data from ABF files in Python.** To this end, the following trends are followed:
* **pyABF should be so intuitive that documentation is unnecessary**
  * Glancing through the getting started guide should convey all the programmer needs to know to get started.
  * ABF class method names are intended to be intuitive without documentation.
  * Important information is stored in flat variables and class properties instead of dictionaries whenever possible (especially in the header), maximizing their accessibility when using a predictive IDE.
* **Nonstandard libraries are avoided** - to minimize liability and simplify portability to other languages.
  * The only requirement beyond the standard library is numpy.
  * Testing routines and the generation of documentation utilize matplotlib, but that module is not a requirement of the ABF class.
* **pyABF is for data access (not analysis or graphing)** - It is assumed the end user is a programmer, so they will be left to design their own data analysis routines. 
  * The core component of this project is the ABF object, which contains as little analysis code as possible.
  * Modules may be distributed with pyABF which take-in ABF objects and perform analytical tasks, but these modules lie outside the core ABF reading goals of this project.