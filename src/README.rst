
pyabf: A portable Python library for reading files in Axon Binary Format (ABF)
==============================================================================

Homepage: `https://github.com/swharden/pyABF <https://github.com/swharden/pyABF>`_

Quickstart
----------

**Display ABF Information:**

.. code-block:: python

  import pyabf
  abf=pyabf.ABF("filename.abf")
  abf.info()

**Plot all sweeps with matplotlib:**

.. code-block:: python

  import pyabf
  import matplotlib.pyplot as plt
  abf=pyabf.ABF("filename.abf")
  plt.figure(figsize=(8,4))
  for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    plt.plot(abf.dataX,abf.dataY)
  plt.ylabel(abf.unitsLong)
  plt.xlabel(abf.unitsTimeLong)
  plt.title(abf.ID)
  plt.margins(0,.1)
  plt.show()
    

Documentation
-------------
Full pyabf API documentation, additional code examples, a pyabf cookbook, and low-level information about the ABF file format can be found at the pyABF project homepage: https://github.com/swharden/pyABF