

# Advanced pyABF Examples

* Review this page only after reviewing the 
[getting started](/docs/getting-started) guide.
* This page is a collection of advanced tasks performed by pyABF.
* Use these advanced features at your own risk!
  * Many of these examples are dirty hacks which may get cleaner with time
  * However, this means the syntax may change as the API improves
  * These examples will never be removed. Their code will always be updated.


## Accessing Digital Outputs

Epochs don't just control DAC clamp settings, they also control digital
outputs. Digital outputs are stored as an 8-bit byte with 0 representing
off and 1 representing on. Calling `abf.sweepD(digOutNum)` will return
a waveform (scaled 0 to 1) to show the high/low state of the digital
output number given (usually 0-7). Here a digital output controls an 
optogenetic stimulator, and a light-evoked EPSC is seen several 
milliseconds after the stimulus

**Code:**

```python
import pyabf
abf = pyabf.ABF("17o05026_vc_stim.abf")

fig = plt.figure(figsize=(8, 5))

ax1 = fig.add_subplot(211)
ax1.set_title("Digital Output 4")
ax1.set_ylabel("State")

# plot the digital output of the first sweep
ax1.plot(abf.sweepX, abf.sweepD(4), color='r')

ax2 = fig.add_subplot(212, sharex=ax1)
ax2.set_title("Recorded Waveform")
ax2.set_xlabel(abf.sweepLabelY)
ax2.set_ylabel(abf.sweepLabelC)

# plot the data from every sweep
for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    ax2.plot(abf.sweepX, abf.sweepY, color='C0', alpha=.8, lw=.5)

fig.subplots_adjust(hspace=.4)
ax2.axes.set_xlim(1.10, 1.25)
ax2.axes.set_ylim(-150, 50)

plt.show()
```

**Output:**

![source/advanced_09a_digital_outputs.jpg](source/advanced_09a_digital_outputs.jpg)

## Shading Epochs

In this ABF digital output 4 is high during epoch C. Let's highlight
this by plotting sweeps and shading that epoch.

`print(abf.epochPoints)` yields `[0, 3125, 7125, 23125, 23145, 200000]`
and I know the epoch I'm interested in is bound by index 3 and 4.

**Code:**

```python
import pyabf
abf = pyabf.ABF("17o05026_vc_stim.abf")

plt.figure(figsize=(8, 5))
for sweepNumber in abf.sweepList:
    abf.setSweep(sweepNumber)
    plt.plot(abf.sweepX, abf.sweepY, color='C0', alpha=.5, lw=.5)
plt.ylabel(abf.sweepLabelY)
plt.xlabel(abf.sweepLabelX)
plt.title("Shade a Specific Epoch")
plt.axis([1.10, 1.25, -150, 50])

t1 = abf.sweepX[abf.epochPoints[3]]
t2 = abf.sweepX[abf.epochPoints[4]]
plt.axvspan(t1, t2, color='r', alpha=.3, lw=0)

plt.show()
```

**Output:**

![source/advanced_10a_digital_output_shading.jpg](source/advanced_10a_digital_output_shading.jpg)

## Plotting Data from ATF Files

Although most of the effort in this project has gone into the ABF class,
there also exists an ATF class with much of the similar functionality.
This class can read Axon Text Format (ATF) files and has a setSweep()
with nearly identical sentax to the ABF class. 

Extra attention was invested into supporting muli-channel ATF data.
Note that this example plots only channel 2 from a multi-channel ATF 
file.

**Code:**

```python
import pyabf
atf = pyabf.ATF("18702001-step.atf")  # not ABF!

fig = plt.figure(figsize=(8, 5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

for channel, ax in enumerate([ax1, ax2]):
    ax.set_title(f"{atf.atfID} channel {channel}")
    ax.set_xlabel(atf.sweepLabelX)
    ax.set_ylabel(atf.sweepLabelY)
    for sweepNumber in atf.sweepList:
        atf.setSweep(sweepNumber, channel)
        ax.plot(atf.sweepX, atf.sweepY)

plt.show()
```

**Output:**

![source/advanced_17_atf_plotting.jpg](source/advanced_17_atf_plotting.jpg)