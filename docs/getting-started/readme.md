

# Getting Started with pyABF

This page is a collection of common tasks performed by pyABF.
They start out simple and increase in complexity.

  * All ABFs used are provided in  [the data folder](/data/)
  * These tests (and this output) are automated by [generate.py](generate.py)
  * Examples `import matplotlib.pyplot as plt`
  * Examples `import numpy as np`
  * Alternate color scheme provided with `plt.style.use('bmh')`


## Access Sweep Data

Load an ABF and display data from a certain sweep. 
The output will look like: 
`[-60.08911 -60.08911 ..., -61.67602 -61.64550]`.
Note that sweeps start at 0, so calling `setSweep(14)` really loads
the 15th sweep.

**Code:**

```python
import pyabf
plt.figure(figsize=(8, 5))
abf = pyabf.ABF("17o05028_ic_steps.abf")
abf.setSweep(14)
print(abf.sweepY)
```

## Plot Sweep Data

Plot a sweep of ABF data using matplotlib.

**Code:**

```python
import pyabf
abf = pyabf.ABF("17o05028_ic_steps.abf")
abf.setSweep(14)
plt.figure(figsize=(8, 5))
plt.plot(abf.sweepX, abf.sweepY)
```

**Output:**

![source/demo_02a_plot_matplotlib_sweep.jpg](source/demo_02a_plot_matplotlib_sweep.jpg)

## Decorate Plots with ABF Information

Plot every 5th sweep and decorate the plot nicely.
Note that the _displayed_ sweep number starts at 1.

**Code:**

```python
import pyabf
abf = pyabf.ABF("17o05028_ic_steps.abf")

plt.figure(figsize=(8, 5))
for sweepNumber in range(abf.sweepCount)[::5]:
    abf.setSweep(sweepNumber)
    plt.plot(abf.sweepX, abf.sweepY, alpha=.5,
             label=f"sweep {sweepNumber+1}")

plt.margins(0, .1)
plt.legend()
plt.ylabel(abf.sweepLabelY)
plt.xlabel(abf.sweepLabelX)
plt.title(abf.abfID)
plt.tight_layout()
```

**Output:**

![source/demo_03a_decorate_matplotlib_plot.jpg](source/demo_03a_decorate_matplotlib_plot.jpg)

## Plot Multi-Channel ABFs

Channel selection is done by adding the `channel=` 
argument in `setSweep()`

**Code:**

```python
import pyabf
abf = pyabf.ABF("14o08011_ic_pair.abf")

fig = plt.figure(figsize=(8, 5))

abf.setSweep(sweepNumber=0, channel=0)
ax1 = fig.add_subplot(211)
ax1.set_title(f"Channel {abf.sweepChannel+1}")
ax1.plot(abf.sweepX, abf.sweepY)
ax1.set_ylabel(abf.sweepLabelY)

abf.setSweep(sweepNumber=0, channel=1)
ax2 = fig.add_subplot(212)
ax2.set_title(f"Channel {abf.sweepChannel+1}")
ax2.plot(abf.sweepX, abf.sweepY)
ax2.set_xlabel(abf.sweepLabelX)
ax2.set_ylabel(abf.sweepLabelY)

fig.subplots_adjust(hspace=.4)  # add more space between the subplots
```

**Output:**

![source/demo_04a_plotting_multiple_channels.jpg](source/demo_04a_plotting_multiple_channels.jpg)

## Plot the Stimulus Waveform

Episodic ABF files can have complex protocols designed with the waveform
editor. After calling `setSweep()` the command waveform can be accessed
as `sweep.C`.

**Code:**

```python
import pyabf
abf = pyabf.ABF("171116sh_0018.abf")
abf.setSweep(14)

fig = plt.figure(figsize=(8, 5))

ax1 = fig.add_subplot(211)
ax1.set_title("ADC (recorded waveform)")
ax1.plot(abf.sweepX, abf.sweepY)
ax1.set_ylabel(abf.sweepLabelY)

ax2 = fig.add_subplot(212)
ax2.set_title("DAC (stimulus waveform)")
ax2.plot(abf.sweepX, abf.sweepC, color='r')
ax2.set_xlabel(abf.sweepLabelX)
ax2.set_ylabel(abf.sweepLabelC)

fig.subplots_adjust(hspace=.4)  # add more space between the subplots
```

**Output:**

![source/demo_05a_plotting_command_waveform.jpg](source/demo_05a_plotting_command_waveform.jpg)

## Zooming Gracefully

While you can zoom in on data by setting its matplotlib axis, when
using subplots it helps to link them together horizontally.

**Code:**

```python
import pyabf
abf = pyabf.ABF("171116sh_0018.abf")
abf.setSweep(14)

fig = plt.figure(figsize=(8, 5))

ax1 = fig.add_subplot(211)
ax1.set_title("ADC (recorded waveform)")
ax1.plot(abf.sweepX, abf.sweepY)
ax1.set_ylabel(abf.sweepLabelY)

ax2 = fig.add_subplot(212, sharex=ax1)  # this links them together
ax2.set_title("DAC (stimulus waveform)")
ax2.plot(abf.sweepX, abf.sweepC, color='r')
ax2.set_xlabel(abf.sweepLabelX)
ax2.set_ylabel(abf.sweepLabelC)

fig.subplots_adjust(hspace=.4)  # add more space between the subplots

ax1.axes.set_xlim(0.1, 0.4)  # zoom between 100 and 200 ms
```

**Output:**

![source/demo_06a_linking_subplots_and_zooming.jpg](source/demo_06a_linking_subplots_and_zooming.jpg)

## Stacking Sweeps

I often like to view sweeps stacked one on top of another. In ClampFit
this is done with "distribute traces". Here we can add a bit of offset
when plotting sweeps.

Note also that `abf.sweepList` is the same as `range(abf.sweepCount)`

**Code:**

```python
import pyabf
abf = pyabf.ABF("171116sh_0018.abf")

plt.figure(figsize=(8, 5))

for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    plt.plot(abf.sweepX, abf.sweepY + 140*sweepNumber, color='C0')

plt.gca().get_yaxis().set_visible(False)  # hide Y axis
plt.xlabel(abf.sweepLabelX)
plt.margins(0, .02)
plt.tight_layout()
```

**Output:**

![source/demo_07a_stacked_sweeps.jpg](source/demo_07a_stacked_sweeps.jpg)

## XY Offset and Custom Colormap

Plotting every sweep with a slight X and Y offset produces a cool
3D effect. I often use this view to visually inspect drug effects.

I also assign a color by sweep from a matplotlib colormap.

**Code:**

```python
import pyabf
abf = pyabf.ABF("17o05026_vc_stim.abf")

# only plot data between this time range
i1=int(abf.dataRate*3.0)
i2=int(abf.dataRate*3.5)

# use a custom colormap
cm = plt.get_cmap("winter")
colors = [cm(x/abf.sweepCount) for x in abf.sweepList]

plt.figure(figsize=(8, 5))
for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    plt.plot(
        abf.sweepX[i1:i2] + .05 * sweepNumber,
        abf.sweepY[i1:i2] + 15*sweepNumber,
        color=colors[sweepNumber],
        lw=.5, alpha=.6)

# remove axes and use tight margins
plt.gca().get_yaxis().set_visible(False)  # hide Y axis
plt.gca().get_xaxis().set_visible(False)  # hide X axis
plt.margins(.02, .02)
plt.tight_layout()
```

**Output:**

![source/demo_08a_xy_offset.jpg](source/demo_08a_xy_offset.jpg)