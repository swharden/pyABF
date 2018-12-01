pyABF: a pure-Python ABF file reader
====================================

**pyABF** provides a Python interface to files in the Axon Binary Format (ABF)

* `pyABF Homepage (GitHub) <https://github.com/swharden/pyABF>`_
* `Getting Started with pyABF <https://github.com/swharden/pyABF/tree/master/docs/getting-started>`_
* `Unofficial Guide to the ABF File Format <https://github.com/swharden/pyABF/tree/master/docs/advanced/abf-file-format>`_






Quickstart
----------

**Access Sweep Data:**

.. code-block:: python

  import pyabf
  abf = pyabf.ABF("demo.abf")
  abf.setSweep(3)
  print(abf.sweepY) # sweep data (ADC)
  print(abf.sweepC) # sweep command (DAC)
  print(abf.sweepX) # sweep times (seconds)

**Plot a Single Sweep:**

.. code-block:: python

  import matplotlib.pyplot as plt
  import pyabf
  abf = pyabf.ABF("17o05028_ic_steps.abf")
  abf.setSweep(14)
  plt.plot(abf.sweepX, abf.sweepY)
  plt.show()

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/swharden/pyABF/master/docs/getting-started/source/demo_02a_plot_matplotlib_sweep.jpg
        :alt: pyABF Example
        :align: center


**Create Fancy Plots with Matplotlib:**

.. code-block:: python

  import matplotlib.pyplot as plt
  import pyabf
  abf = pyabf.ABF("17o05028_ic_steps.abf")

  plt.figure(figsize=(8, 5))
  for sweepNumber in range(abf.sweepCount)[::5]:
      abf.setSweep(sweepNumber)
      plt.plot(abf.sweepX,abf.sweepY,alpha=.5,label="sweep %d"%(sweepNumber))

  plt.margins(0, .1)
  plt.legend()
  plt.ylabel(abf.sweepLabelY)
  plt.xlabel(abf.sweepLabelX)
  plt.title(abf.abfID)
  plt.tight_layout()
  plt.show()

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/swharden/pyABF/master/docs/getting-started/source/demo_03a_decorate_matplotlib_plot.jpg
        :alt: pyABF Example
        :align: center


Additional Examples
-------------------

**Full pyabf API documentation**, additional code examples, a pyabf cookbook, 
and low-level information about the ABF file format can be found at the pyABF 
project homepage: https://github.com/swharden/pyABF