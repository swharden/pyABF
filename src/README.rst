pyABF: a pure-Python ABF file reader
====================================

**pyABF** provides a Python interface to electrophysiology files in the Axon Binary Format (ABF).
pyABF supports Python 2.7 and Python 3.6+ and does not use obscure libraries
(just the standard libraries plus numpy and matplotlib). pyABF supports reading
of ABF1 and ABF2 files, and can write ABF1 files.

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/swharden/pyABF/master/docs/graphics/2017-11-06-aps.png
        :alt: pyABF electrophysiology data analysis with Python and Matplotlib
        :align: center


Links
=====
* `pyABF Homepage (GitHub) <https://github.com/swharden/pyABF>`_
* `Getting Started with pyABF <https://github.com/swharden/pyABF/tree/master/docs/getting-started>`_
* `Unofficial Guide to the ABF File Format <https://github.com/swharden/pyABF/tree/master/docs/advanced/abf-file-format>`_

Quickstart
==========

Install or upgrade pyABF:

.. code-block:: bash

    pip install --upgrade pyabf

|

Access ABF sweep data:

.. code-block:: python

  import pyabf
  abf = pyabf.ABF("demo.abf")
  abf.setSweep(3)
  print(abf.sweepY) # sweep data (ADC)
  print(abf.sweepC) # sweep command (DAC)
  print(abf.sweepX) # sweep times (seconds)

|

Plot a sweep with Matplotlib:

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

|

Get fancy with Matplotlib:

.. code-block:: python

  import matplotlib.pyplot as plt
  import pyabf
  abf = pyabf.ABF("sample.abf")

  plt.figure(figsize=(8, 5))
  for sweepNumber in range(abf.sweepCount)[::5]:
      abf.setSweep(sweepNumber)
      plt.plot(abf.sweepX,abf.sweepY,alpha=.5,label="sweep %d"%(sweepNumber))

  plt.legend()
  plt.ylabel(abf.sweepLabelY)
  plt.xlabel(abf.sweepLabelX)
  plt.title("pyABF and Matplotlib are a great pair!")
  plt.show()

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/swharden/pyABF/master/docs/getting-started/source/demo_03a_decorate_matplotlib_plot.jpg
        :alt: pyABF Example
        :align: center

|

Additional Examples
===================
Full pyabf API documentation, additional code examples, a pyabf cookbook, 
and low-level information about the ABF file format can be found at the pyABF 
project homepage: https://github.com/swharden/pyABF

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/swharden/pyABF/master/docs/getting-started/source/advanced_08b_using_plot_module.jpg
        :alt: pyABF Example
        :align: center

|

Citing pyABF
============

If the pyABF module facilitated your research, consider citing this project by name so it can benefit others too:

    *"Computational analysis of electrophysiological recordings was performed with custom software written for this project using Python 3.6 and the pyABF module."*

|

Feature Requests / Unsupported ABF Files
========================================
If you have ABF files which are unsupported (or read incorrectly) 
by this software, it is likely due to a use case we have not run 
across yet, so let us know about it! We can only develop and test 
this software against ABF files we have access to, so if you're 
interested in having your ABF file supported send the primary author 
an email (and the ABF file you are trying to analyze) and we will 
investigate it. If a solution is reached the pyabf package will be 
updated so everyone can benefit from the change. 
We can only develop for (and test against) ABFs we have access to, 
so we really appreciate your contributions!

|

Author
======

| **Scott W Harden, DMD, PhD**
| `Harden Technologies, LLC <http://tech.SWHarden.com>`_
| `www.SWHarden.com <http://www.SWHarden.com>`_
| SWHarden@gmail.com