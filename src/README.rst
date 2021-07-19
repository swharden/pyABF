pyABF: a pure-Python ABF file reader
====================================

**pyABF** provides a Python interface to electrophysiology files in the Axon Binary Format (ABF).
pyABF supports Python versions 3.6 and newer and does not use obscure libraries
(just the standard libraries plus numpy and matplotlib). pyABF supports reading
of ABF1 and ABF2 files, and can write ABF1 files.

.. class:: no-web

    .. image:: http://swharden.com/pyabf/graphics/action-potentials-small.png
        :alt: pyABF electrophysiology data analysis with Python and Matplotlib
        :align: center

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
  abf.setSweep(sweepNumber=3, channel=0)
  print(abf.sweepY) # displays sweep data (ADC)
  print(abf.sweepX) # displays sweep times (seconds)
  print(abf.sweepC) # displays command waveform (DAC)

|

Plot a sweep with Matplotlib:

.. code-block:: python

  import pyabf
  import matplotlib.pyplot as plt
  abf = pyabf.ABF("demo.abf")
  abf.setSweep(14)
  plt.plot(abf.sweepX, abf.sweepY)
  plt.show()

.. class:: no-web

    .. image:: http://swharden.com/pyabf/graphics/pyabf-example-sweep.jpg
        :alt: pyABF Example
        :align: center

|


Additional Examples
===================
Full pyabf API documentation, additional code examples, a pyabf cookbook, 
and low-level information about the ABF file format can be found at the pyABF 
project homepage: http://swharden.com/pyabf/

.. class:: no-web

    .. image:: http://swharden.com/pyabf/graphics/pyabf-example-action-potentials.jpg
        :alt: pyABF Example
        :align: center

|
