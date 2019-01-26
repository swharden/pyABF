"""
This file contains functions to demonstrate core functionality of the pyABF
module. Functions prefaced with "demo_" may be run automatically to generate 
a markdown document. In this case their docstrings will be included in the 
getting started guide and their code will be added to the 
readme along with any images saved with the same filename as the function.

This documentation generator doubles as a test suite, as a variety of ABF 
loading and plotting functions are executed while the documentation and 
supportive graphs are regnerated.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
sys.path.insert(0, PATH_PROJECT+"/src/")
import pyabf
import glob
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import glob
import inspect

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

MARKDOWN_STANDARD = """

# Getting Started with pyABF

**This page demonstrates how to use pyABF to perform many common tasks.**
Examples start out simple and increase in complexity. 
Browsing this page is the best way to get started with pyABF, as every core 
function is demonstrated in this document.
All ABFs used in these examples are provided in [the data folder](/data/), 
so you can practice recreating these examples in your own programming 
environment.

**Advanced examples:** experimental features (useful, but subject to syntax 
changes as the pyABF API matures) are demonstrated on the 
[advanced examples](advanced.md) page.

**Technical note:** this guide is generated automatically by
[gettingStarted.py](/tests/tests/gettingStarted.py)) and so this page doubles 
as a test suite (all these examples should produce identical graphs after all
code changes). 

## Prerequisite Imports

Although it's not explicitly shown in every example, it is assumed the following
lines are present at the top of your Python script:

```python
import pyabf
import numpy as np
import matplotlib.pyplot as plt
```
"""

MARKDOWN_ADVANCED = """

# Advanced pyABF Examples

* Review this page only after reviewing the 
[getting started](/docs/getting-started) guide.
* This page is a collection of advanced tasks performed by pyABF.
* Use these advanced features at your own risk!
  * Many of these examples are dirty hacks which may get cleaner with time
  * However, this means the syntax may change as the API improves
  * These examples will never be removed. Their code will always be updated.
"""

class NoStdStreams(object):
    def __init__(self, stdout=None):
        self.devnull = open(os.devnull, 'w')
        self._stdout = stdout or self.devnull or sys.stdout

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stdout.flush()
        sys.stdout = self._stdout

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        sys.stdout = self.old_stdout
        self.devnull.close()


class UseCaseManager:
    def __init__(self):
        self.figsize = (8, 5)
        self.dpi = 75

    def saveAndClose(self):
        func = inspect.stack()[1][3]
        fname = f"{PATH_PROJECT}/docs/getting-started/source/{func}.jpg"
        fname = os.path.abspath(fname)
        log.debug(f"saving figure: {fname}")
        plt.savefig(fname, dpi=self.dpi)
        plt.close()

    def demo_00a_load_abf(self):
        """
        ## Load an ABF File

        Give an ABF file path to `pyabf.ABF()` to get started

        **Code:**
        ```python
        import pyabf
        abf = pyabf.ABF("demo.abf")
        print(abf)
        ```

        **Output:**
        ```
        ABF file (demo.abf) with 1 channel, 187 sweeps, and a total length of 6.23 min.
        ```
        """
        pass

    def demo_00b_abf_header(self):
        """
        ## Inspect the ABF header

        Sometimes it is useful to see all the data contained in the ABF header.
        While inspecting the header is not necessary to use pyabf, it is useful
        to know how to access this information.

        **Code:**
        ```python
        import pyabf
        abf = pyabf.ABF("demo.abf")
        print(abf.headerText) # display header information in the console
        abf.headerLaunch() # display header information in a web browser
        ```
        """
        pass

    def demo_01a_print_sweep_data(self):
        """
        ## Access Sweep Data

        ABF objects provide access to ABF data by sweep number. Sweep numbers
        start at zero, and after setting a sweep you can access that sweep's
        ADC data with `sweepY`, DAC simulus waveform / command signal with 
        `sweepC`, and the time units for the sweep with `sweepX`.
        
        **Code:**
        ```python
        import pyabf
        abf = pyabf.ABF("18808025.abf")
        abf.setSweep(14)
        print("sweep data (ADC):", abf.sweepY)
        print("sweep command (DAC):", abf.sweepC)
        print("sweep times (seconds):", abf.sweepX)
        ```

        **Output:**
        ```
        sweep data (ADC): [-13.6719 -12.9395 -12.207  ..., -15.8691 -15.8691 -16.7236]
        sweep command (DAC): [-70. -70. -70. ..., -70. -70. -70.]
        sweep times (seconds): [ 0.      0.0001  0.0001 ...,  0.5998  0.5999  0.5999]
        ```
        """
        pass

    def demo_02a_plot_matplotlib_sweep(self):
        """
        ## Plot a Sweep with Matplotlib

        Matplotlib is a fantastic plotting library for Python. This example
        shows how to plot an ABF sweep using matplotlib.
        ABF `setSweep()` is used to tell the ABF class what sweep to load
        into memory. After that you can just plot `sweepX` and `sweepY`.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05028_ic_steps.abf")
        abf.setSweep(14)
        plt.figure(figsize=self.figsize)
        plt.plot(abf.sweepX, abf.sweepY)
        plt.grid(alpha=.2) #ignore
        plt.margins(0,.1) #ignore
        plt.tight_layout() #ignore
        self.saveAndClose()

    def demo_03a_decorate_matplotlib_plot(self):
        """
        ## Decorate Plots with ABF Information

        The ABF class provides easy access to lots of information about the ABF.
        This example shows how to use these class methods to create a prettier
        plot of several sweeps from the same file.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05028_ic_steps.abf")
        plt.figure(figsize=self.figsize)
        plt.title("pyABF and Matplotlib are a great pair!")
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        for i in [0, 5, 10, 15]:
            abf.setSweep(i)
            plt.plot(abf.sweepX, abf.sweepY, alpha=.5, label="sweep %d"%(i))
        plt.margins(0, .1) #ignore
        plt.tight_layout() #ignore
        plt.grid(alpha=.2) #ignore
        plt.legend()
        self.saveAndClose()

    def demo_04a_plotting_multiple_channels(self):
        """
        ## Plot Multi-Channel ABFs

        Channel selection is achieved by defining a channel when calling
        `setSweep()`.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/14o08011_ic_pair.abf")
        fig = plt.figure(figsize=self.figsize)

        # plot the first channel
        abf.setSweep(sweepNumber=0, channel=0)
        plt.plot(abf.sweepX, abf.sweepY, label="Channel 1")

        # plot the second channel
        abf.setSweep(sweepNumber=0, channel=1)
        plt.plot(abf.sweepX, abf.sweepY, label="Channel 2")

        # decorate the plot
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.tight_layout() #ignore
        plt.grid(alpha=.2) #ignore
        plt.axis([25, 45, -70, 50])
        plt.legend()
        self.saveAndClose()

    def demo_05a_plotting_command_waveform(self):
        """
        ## Plot the Command Waveform

        Episodic ABF files can have complex protocols designed with in waveform
        editor. After calling `setSweep()` the command waveform can be accessed
        as `sweep.C`. 
        
        To get more information about the epoch table (such as the list of 
        levels for each epoch, specific time points epochs start and stop, etc.)
        check out properties of the `abf.sweepEpochs` object, which represents
        the currently loaded sweep/channel.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")
        abf.setSweep(14)
        fig = plt.figure(figsize=self.figsize)

        # plot the ADC (voltage recording)
        ax1 = fig.add_subplot(211)
        ax1.set_title("ADC (recorded waveform)")
        ax1.plot(abf.sweepX, abf.sweepY)

        # plot the DAC (clamp current)
        ax2 = fig.add_subplot(212)
        ax2.set_title("DAC (stimulus waveform)")
        ax2.plot(abf.sweepX, abf.sweepC, color='r')

        # decorate the plots
        ax1.set_ylabel(abf.sweepLabelY)
        ax2.set_xlabel(abf.sweepLabelX)
        ax2.set_ylabel(abf.sweepLabelC)
        ax1.grid(alpha=.2) #ignore
        ax2.grid(alpha=.2) #ignore
        ax1.margins(0,.1) #ignore
        ax2.margins(0,.1) #ignore
        fig.subplots_adjust(hspace=.4)  #ignore
        self.saveAndClose()

    def demo_06a_linking_subplots_and_zooming(self):
        """
        ## Axis-Linked Subplots

        Matplotlib allows you to create subplots with linked axes. This is
        convenient when plotting a waveform and its command stimulus at the
        same time, because zooming-in on one will zoom-in on the other. This
        is most useful when using interactive graphs, but works in all cases.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")
        abf.setSweep(14)
        fig = plt.figure(figsize=self.figsize)

        # plot the ADC (voltage recording)
        ax1 = fig.add_subplot(211)
        ax1.set_title("ADC (recorded waveform)")
        ax1.plot(abf.sweepX, abf.sweepY)

        # plot the DAC (clamp current)
        ax2 = fig.add_subplot(212, sharex=ax1)  # <-- this argument is new
        ax2.set_title("DAC (stimulus waveform)")
        ax2.plot(abf.sweepX, abf.sweepC, color='r')

        # decorate the plots
        ax1.set_ylabel(abf.sweepLabelY)
        ax2.set_xlabel(abf.sweepLabelX)
        ax2.set_ylabel(abf.sweepLabelC)
        ax1.grid(alpha=.2) #ignore
        ax2.grid(alpha=.2) #ignore
        fig.subplots_adjust(hspace=.4)  #ignore
        ax1.axes.set_xlim(1.25, 2.5)  # <-- adjust axis like this
        self.saveAndClose()

    def demo_07a_stacked_sweeps(self):
        """
        ## Plot Stacked Sweeps

        I often like to view sweeps stacked one on top of another. In ClampFit
        this is done with "distribute traces". Here we can add a bit of offset
        when plotting sweeps and achieve the same effect. This example makes
        use of `abf.sweepList`, which is the same as `range(abf.sweepCount)`
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")
        plt.figure(figsize=self.figsize)

        # plot every sweep (with vertical offset)
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            offset = 140*sweepNumber
            plt.plot(abf.sweepX, abf.sweepY+offset, color='C0')

        # decorate the plot
        plt.gca().get_yaxis().set_visible(False)  # hide Y axis
        plt.xlabel(abf.sweepLabelX)
        plt.margins(0, .02) #ignore
        plt.tight_layout() #ignore
        self.saveAndClose()

    def demo_08a_xy_offset(self):
        """
        ## Plot Sweeps in 3D

        The previous example how to plot stacked sweeps by adding a Y offset
        to each sweep. If you add an X and Y offset to each sweep, you can
        create a 3D effect.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")

        plt.figure(figsize=self.figsize)
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            i1, i2 = 0, int(abf.dataRate * 1) # plot part of the sweep
            dataX = abf.sweepX[i1:i2] + .025 * sweepNumber
            dataY = abf.sweepY[i1:i2] + 15 * sweepNumber
            plt.plot(dataX, dataY, color='C0', alpha=.5)

        plt.gca().axis('off') # hide axes to enhance floating effect
        plt.margins(.02, .02) #ignore
        plt.tight_layout() #ignore
        self.saveAndClose()

    def demo_08b_custom_colormap(self):
        """
        ## Custom Colormaps

        Matplotlib's colormap tools can be used to add an extra dimension to
        graphs. All matplotlib colormaps are [listed here](https://matplotlib.org/examples/color/colormaps_reference.html).
        For an interesting discussion on choosing ideal colormaps for scientific
        data visit [bids.github.io/colormap/](https://bids.github.io/colormap/).
        Good colors for e-phys are "winter", "rainbow", and "viridis".
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")

        # use a custom colormap to create a different color for every sweep
        cm = plt.get_cmap("winter")
        colors = [cm(x/abf.sweepCount) for x in abf.sweepList]
        #colors.reverse()

        plt.figure(figsize=self.figsize)
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            i1, i2 = 0, int(abf.dataRate * 1)
            dataX = abf.sweepX[i1:i2] + .025 * sweepNumber
            dataY = abf.sweepY[i1:i2] + 15 * sweepNumber
            plt.plot(dataX, dataY, color=colors[sweepNumber], alpha=.5)

        plt.gca().axis('off')
        plt.margins(.02, .02) #ignore
        plt.tight_layout() #ignore
        self.saveAndClose()

    def advanced_08b_using_plot_module(self):
        """
        ## Advanced Plotting with the `pyabf.plot` Module

        pyabf has a plot module which has been designed to simplify the act
        of creating matplotlib plots of electrophysiological data loaded with
        the ABF class. This module isn't fully developed yet (so don't rely
        on code you write today working with it tomorrow), but it's a strong
        start and has some interesting functionality that might be worth
        inspecting. 

        If you care a lot about how your graphs look, plot them yourself with
        matplotlib commands. If you want to save keystrokes, don't care how
        the graphs look, or don't know how to use matplotlib (and don't feel
        like learning), maybe some of the functions in `pyabf.plot` will be
        useful to you. You don't have to import it, just call its functions
        and pass-in the abf object you're currently working with.

        Notice in this example there is an L-shaped scalebar. Nice!
        """

        import pyabf
        import pyabf.plot
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")
        pyabf.plot.sweeps(abf, title=False, 
            offsetXsec=.1, offsetYunits=20, startAtSec=0, endAtSec=1.5)
        pyabf.plot.scalebar(abf, hideFrame=True)
        plt.tight_layout()
        self.saveAndClose()

    def advanced_09a_digital_outputs(self):
        """
        ## Accessing Digital Outputs

        Epochs don't just control DAC clamp settings, they also control digital
        outputs. Digital outputs are stored as an 8-bit byte with 0 representing
        off and 1 representing on. Calling `abf.sweepD(digOutNum)` will return
        a waveform (scaled 0 to 1) to show the high/low state of the digital
        output number given (usually 0-7). Here a digital output controls an 
        optogenetic stimulator, and a light-evoked EPSC is seen several 
        milliseconds after the stimulus
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")

        fig = plt.figure(figsize=self.figsize)

        ax1 = fig.add_subplot(211)
        ax1.grid(alpha=.2)
        ax1.set_title("Digital Output 4")
        ax1.set_ylabel("Digital Output")

        # plot the digital output of the first sweep
        ax1.plot(abf.sweepX, abf.sweepD(4), color='r')
        ax1.set_yticks([0, 1])
        ax1.set_yticklabels(["OFF", "ON"])
        ax1.axes.set_ylim(-.5, 1.5)

        ax2 = fig.add_subplot(212, sharex=ax1)
        ax2.grid(alpha=.2)
        ax2.set_title("Recorded Waveform")
        ax2.set_xlabel(abf.sweepLabelY)
        ax2.set_ylabel(abf.sweepLabelC)

        # plot the data from every sweep
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            ax2.plot(abf.sweepX, abf.sweepY, color='C0', alpha=.8, lw=.5)
        
        # zoom in on an interesting region
        ax2.axes.set_xlim(1.10, 1.25)
        ax2.axes.set_ylim(-150, 50)
        fig.subplots_adjust(hspace=.4) #ignore
        self.saveAndClose()

    def advanced_10a_digital_output_shading(self):
        """
        ## Shading Epochs

        In this ABF digital output 4 is high during epoch C. Let's highlight
        this by plotting sweeps and shading that epoch.

        `print(abf.epochPoints)` yields `[0, 3125, 7125, 23125, 23145, 200000]`
        and I know the epoch I'm interested in is bound by index 3 and 4.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")

        plt.figure(figsize=self.figsize)
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            plt.plot(abf.sweepX, abf.sweepY, color='C0', alpha=.5, lw=.5)
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.title("Shade a Specific Epoch")
        plt.axis([1.10, 1.25, -150, 50])

        epochNumber = 3
        t1 = abf.sweepEpochs.p1s[epochNumber] * abf.dataSecPerPoint
        t2 = abf.sweepEpochs.p2s[epochNumber] * abf.dataSecPerPoint
        plt.axvspan(t1, t2, color='r', alpha=.3, lw=0)
        plt.grid(alpha=.2)
        self.saveAndClose()

    def demo_11a_gap_free(self):
        """
        ## Plotting Gap-Free ABFs

        The pyABF treats every ABF like it's episodic (with sweeps). As such,
        gap free ABF files are loaded as if they were episodic files with
        a single sweep. When an ABF is loaded, `setSweep(0)` is called
        automatically, so the entire gap-free set of data is already available
        by plotting `sweepX` and `sweepY`.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/abf1_with_tags.abf")
        plt.figure(figsize=self.figsize)
        plt.plot(abf.sweepX, abf.sweepY, lw=.5)
        plt.axis([725, 825, -150, -15])
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.title("Example Gap Free File")
        plt.margins(0,.1) #ignore
        plt.grid(alpha=.2) #ignore
        self.saveAndClose()

    def demo_12a_tags(self):
        """
        ## Accessing Comments (Tags) in ABF Files

        While recording an ABF the user can insert a comment at a certain
        time point. pClamp calls these "tags", and they can be a useful
        way to mark when a drug was applied during an experiment. For this
        to work, `sweepX` needs to be a list of times in the ABF recording
        (not times which always start at 0 for every new sweep). Set this
        behavior by setting `absoluteTime=True` when calling `setSweep()`.

        A list of comments (the text of tags) is stored in a list 
        `abf.tagComments`. The sweep for each tag is in `abf.tagSweeps`, while
        the time of each tag is in `abf.tagTimesSec` and `abf.tagTimesMin`
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/16d05007_vc_tags.abf")

        # create a plot with time on the horizontal axis
        plt.figure(figsize=self.figsize)
        for sweep in abf.sweepList:
            abf.setSweep(sweep, absoluteTime=True) # <-- relates to sweepX
            abf.sweepY[:int(abf.dataRate*1.0)] = np.nan  # ignore
            plt.plot(abf.sweepX, abf.sweepY, lw=.5, alpha=.5, color='C0')
        plt.margins(0, .5)
        plt.grid(alpha=.2) #ignore
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)

        # now add the tags as vertical lines
        for i, tagTimeSec in enumerate(abf.tagTimesSec):
            posX = abf.tagTimesSec[i]
            comment = abf.tagComments[i]
            color = "C%d"%(i+1)
            plt.axvline(posX, label=comment, color=color, ls='--')
        plt.legend()

        plt.title("ABF File with Comments (Tags)")
        self.saveAndClose()

    def demo_13a_baseline(self):
        """
        ## Baseline Subtraction

        Sometimes it is worthwhile to center every sweep at 0. This can be done
        easily giving a time range to baseline subtract to when calling 
        setSweep().
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")
        plt.figure(figsize=self.figsize)

        # plot a sweep the regular way
        abf.setSweep(3)
        plt.plot(abf.sweepX, abf.sweepY, alpha=.8, label="original")

        # plot a sweep with baseline subtraction
        abf.setSweep(3, baseline=[2.1, 2.15])
        plt.plot(abf.sweepX, abf.sweepY, alpha=.8, label="subtracted")

        # decorate the plot
        plt.title("Sweep Baseline Subtraction")
        plt.axhline(0, color='k', ls='--')
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.legend()
        plt.axis([2, 2.5, -50, 20])
        plt.grid(alpha=.2) #ignore
        self.saveAndClose()

    def demo_14a_gaussian_filter(self):
        """
        ## Gaussian Filter (Lowpass Filter / Data Smoothing)

        Noisy data can be filtered in software. This is especially helpful
        for inspection of evoked or spontaneuos post-synaptic currents. To
        apply low-pass filtering on a specific channel, invoke the 
        `abf.filter.gaussian()` method before calling `setSweep()`.

        The degree of smoothing is defined by _sigma_ (milliseconds units), 
        passed as an argument: `abf.filter.gaussian(abf, sigma)`. 
        
        When an ABF file is loaded its entire data is loaded into memory. When
        the gaussian filter is called, the entire data is smoothed in memory.
        This means calling the filter several times with the same sigma will
        make it progressively smoother (although extremely processor-intensive).

        Set sigma to 0 to remove all filters. This will cause the original data
        to be re-read from the ABF file.
        """

        import pyabf
        import pyabf.filter

        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")
        plt.figure(figsize=self.figsize)

        # plot the original data
        abf.setSweep(3)
        plt.plot(abf.sweepX, abf.sweepY, alpha=.3, label="original")

        # show multiple degrees of smoothless
        for sigma in [.5, 2, 10]:
            pyabf.filter.gaussian(abf, 0) # remove old filter
            pyabf.filter.gaussian(abf, sigma) # apply custom sigma
            abf.setSweep(3) # reload sweep with new filter
            label = "sigma: %.02f" % (sigma)
            plt.plot(abf.sweepX, abf.sweepY, alpha=.8, label=label)

        # zoom in on an interesting region and decorate the plot
        plt.title("Gaussian Filtering of ABF Data")
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.axis([8.20, 8.30, -45, -5])
        plt.legend()
        plt.grid(alpha=.2) #ignore
        self.saveAndClose()

    def demo_15_epochs(self):
        """
        ## Accessing Epoch Information

        In some ABFs an epoch table is used to control the command level of the
        DAC to control voltage or current. While the epoch table can be
        confusing to access directly from the header (e.g., the first epoch
        does not start at time 0, but rather 1/64 of the sweep length), a
        simplified way to access epoch types and levels is provided with the
        `abf.sweepEpochs` object, which contains epoch points, levels, and types
        for the currently-loaded sweep.

        For example, the output of this script:
        ```python
        import pyabf
        abf = pyabf.ABF("2018_08_23_0009.abf")
        for i, p1 in enumerate(abf.sweepEpochs.p1s):
            epochLevel = abf.sweepEpochs.levels[i]
            epochType = abf.sweepEpochs.types[i]
            print(f"epoch index {i}: at point {p1} there is a {epochType} to level {epochLevel}")
        ```

        looks like this:
        ```
        epoch index 0: at point 0 there is a Step to level -70.0
        epoch index 1: at point 187 there is a Step to level -80.0
        epoch index 2: at point 4187 there is a Step to level -70.0
        epoch index 3: at point 8187 there is a Ramp to level -80.0
        epoch index 4: at point 9187 there is a Ramp to level -70.0
        epoch index 5: at point 10187 there is a Step to level -70.0
        ```
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/2018_08_23_0009.abf")

        fig = plt.figure(figsize=self.figsize)

        ax1 = fig.add_subplot(211)
        ax1.plot(abf.sweepY, color='b')
        ax1.set_ylabel("ADC (measurement)")
        ax1.set_xlabel("sweep point (index)")

        ax2 = fig.add_subplot(212)
        ax2.plot(abf.sweepC, color='r')
        ax2.set_ylabel("DAC (command)")
        ax2.set_xlabel("sweep point (index)")

        for p1 in abf.sweepEpochs.p1s:
            ax1.axvline(p1, color='k', ls='--', alpha=.5)
            ax2.axvline(p1, color='k', ls='--', alpha=.5)

        plt.tight_layout()
        self.saveAndClose()

    def advanced_15a_IV_curve(self):
        """
        ## Create an I/V Curve

        This example analyzes 171116sh_0013.abf (a voltage clamp ABF which 
        goes from -110 mV to -50 mV increasing the clamp voltage by 5 mV each
        sweep). To get the "I" the sweep is averaged between 500ms and 1s, and
        to get the "V" the second epoch is accessed.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0013.abf")
        pt1 = int(500 * abf.dataPointsPerMs)
        pt2 = int(1000 * abf.dataPointsPerMs)

        currents=[]
        voltages=[]
        for sweep in abf.sweepList:
            abf.setSweep(sweep)
            currents.append(np.average(abf.sweepY[pt1:pt2]))
            voltages.append(abf.sweepEpochs.levels[2])

        plt.figure(figsize=self.figsize)
        plt.grid(alpha=.5, ls='--')
        plt.plot(voltages, currents, '.-', ms=15)
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelC)
        plt.title(f"I/V Relationship of {abf.abfID}")

        self.saveAndClose()

    # def advanced_16_average_sweep(self):
    #     """
    #     ## Averaging Sweeps

    #     Sometimes you want to analyze a sweep which is the average of several
    #     sweeps. Often this is used in conjunction with baseline subtraction.

    #     This can be done using the sweep range average function.
    #     Although here it's given without arguments, it can take a list of
    #     specific sweep numbers.
    #     """

    #     import pyabf
    #     abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")
    #     #abf.sweepBaseline(1.10, 1.16)

    #     plt.figure(figsize=self.figsize)
    #     plt.grid(alpha=.5, ls='--')
    #     plt.axhline(0, color='k', ls=':')

    #     # plot all individual sweeps
    #     for sweep in abf.sweepList:
    #         abf.setSweep(sweep)
    #         plt.plot(abf.sweepX, abf.sweepY, color='C0', alpha=.1)

    #     # calculate and plot the average of all sweeps
    #     avgSweep = pyabf.sweep.averageTrace(abf)
    #     plt.plot(abf.sweepX, avgSweep, lw=2)

    #     # decorate the plot and zoom in on the interesting area
    #     plt.title("Average of %d sweeps"%(abf.sweepCount))
    #     plt.ylabel(abf.sweepLabelY)
    #     plt.xlabel(abf.sweepLabelX)
    #     plt.axis([1.10, 1.25, -110, 20])

    #    self.saveAndClose()

    def advanced_17_atf_plotting(self):
        """
        ## Plotting Data from ATF Files

        Although most of the effort in this project has gone into the ABF class,
        there also exists an ATF class with much of the similar functionality.
        This class can read Axon Text Format (ATF) files and has a setSweep()
        with nearly identical sentax to the ABF class. 

        Extra attention was invested into supporting muli-channel ATF data.
        Note that this example plots only channel 2 from a multi-channel ATF 
        file.
        """

        import pyabf
        atf = pyabf.ATF("data/abfs/18702001-step.atf")  # not ABF!

        fig = plt.figure(figsize=self.figsize)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        for channel, ax in enumerate([ax1, ax2]):
            ax.set_title("channel %d"%(channel))
            ax.set_xlabel(atf.sweepLabelX)
            ax.set_ylabel(atf.sweepLabelY)
            for sweepNumber in atf.sweepList:
                atf.setSweep(sweepNumber, channel)
                ax.plot(atf.sweepX, atf.sweepY)

        ax1.margins(0, .1)
        ax2.margins(0, .1)
        ax1.grid(alpha=.2)
        ax2.grid(alpha=.2)
        fig.subplots_adjust(wspace=.4)  #ignore
        self.saveAndClose()

    plt.show()

    def advanced_18_memtestOverTime(self):
        """
        ## Passive Membrane Properties

        The pyabf.tools.memtest module has methods which can determine passive
        membrane properties (holding current, membrane resistance, access
        resistance, whole-cell capacitance) from voltage-clamp traces containing
        a hyperpolarizing step. Theory and implimentation details are in the
        comments of the module. This example demonstrates how to graph passive
        membrane properties sweep-by-sweep, and indicate where comment tags
        were added.
        """

        import pyabf
        import pyabf.tools.memtest
        
        abf = pyabf.ABF("data/abfs/vc_drug_memtest.abf")
        Ihs, Rms, Ras, Cms = pyabf.tools.memtest.step_valuesBySweep(abf)

        # That's it! The rest of the code just plots these 4 numpy arrays.
        fig = plt.figure(figsize=self.figsize)

        ax1 = fig.add_subplot(221)
        ax1.grid(alpha=.2)
        ax1.plot(abf.sweepTimesMin, Ihs, ".", color='C0', alpha=.7, mew=0)
        ax1.set_title("Clamp Current")
        ax1.set_ylabel("Current (pA)")

        ax2 = fig.add_subplot(222)
        ax2.grid(alpha=.2)
        ax2.plot(abf.sweepTimesMin, Rms, ".", color='C3', alpha=.7, mew=0)
        ax2.set_title("Membrane Resistance")
        ax2.set_ylabel("Resistance (MOhm)")

        ax3 = fig.add_subplot(223)
        ax3.grid(alpha=.2)
        ax3.plot(abf.sweepTimesMin, Ras, ".", color='C1', alpha=.7, mew=0)
        ax3.set_title("Access Resistance")
        ax3.set_ylabel("Resistance (MOhm)")

        ax4 = fig.add_subplot(224)
        ax4.grid(alpha=.2)
        ax4.plot(abf.sweepTimesMin, Cms, ".", color='C2', alpha=.7, mew=0)
        ax4.set_title("Whole-Cell Capacitance")
        ax4.set_ylabel("Capacitance (pF)")

        for ax in [ax1, ax2, ax3, ax4]:
            ax.margins(0, .9)
            ax.set_xlabel("Experiment Time (minutes)")
            for tagTime in abf.tagTimesMin:
                ax.axvline(tagTime, color='k', ls='--')

        plt.tight_layout()
        self.saveAndClose()

def cleanDocstrings(s):
    s = s.strip()
    s = s.replace("\n        ", "\n")
    return s


def cleanCode(s):
    """
    Given a block of code as a string (probably pulled from a function in this
    script), return that code block with certain fixes so it displays well
    online.
    """
    s = s.replace("\n        ", "\n")
    s = s.replace("data/abfs/", "")
    s = s.replace("self.saveAndClose()", "plt.show()")
    s = s.replace("self.figsize", str(UseCaseManager().figsize))
    s = s.split('"""', 2)[2].strip()
    newLines = []
    for line in s.split("\n"):
        if line.strip().endswith("#ignore"):
            continue
        if line.strip().endswith("# ignore"):
            continue
        newLines.append(line)
    return "\n".join(newLines)

def generate_demos(match="demo_"):
    """
    Load the use case manager and run every function inside it which contains
    a match to the string given in the argument of this function.

    The function docstrings get rendered as a markdown page. If images are
    generated and saved as a result, those are added to the markdown page too.

    Code is also pulled from the function and displayed in the markdown format.
    """

    if match == "demo_":
        print("Running standard demos ", end="")
        md = MARKDOWN_STANDARD
        fname = "readme.md"
    elif match == "advanced_":
        print("Running advanced demos ", end="")
        md = MARKDOWN_ADVANCED
        fname = "advanced.md"
    else:
        raise NotImplementedError("unsupported match string")

    uses = UseCaseManager()
    for functionName in sorted(dir(uses)):
        if not functionName.startswith(match):
            continue
        func = getattr(uses, functionName)
        if True:
        #with NoStdStreams():  # silence print statements
            log.debug("Running %s" % functionName)
            func()
        print(".", end="")
        sys.stdout.flush()
        md += "\n\n"+cleanDocstrings(func.__doc__)
        code = inspect.getsource(func)
        if not code.strip().endswith("pass"):
            md += "\n\n**Code:**\n\n```python\n"
            md += cleanCode(code)
            md += "\n```"
        imgName = functionName+".jpg"
        imgPath = f"{PATH_PROJECT}/docs/getting-started/source/{imgName}"
        if os.path.exists(imgPath):
            md += f"\n\n**Output:**\n\n![source/{imgName}](source/{imgName})"
    fname = os.path.abspath(f"{PATH_PROJECT}/docs/getting-started/{fname}")
    log.debug(f"saving markdown file: {fname}")
    with open(fname, 'w') as f:
        f.write(md)

    print(" OK")


def go():
    """Regenerate all use case examples and figures (simple and advanced)"""
    for fname in glob.glob(os.path.dirname(__file__)+"/source/*.*"):
        os.remove(fname)
    generate_demos("demo_")
    generate_demos("advanced_")

if __name__ == "__main__":
    go()
