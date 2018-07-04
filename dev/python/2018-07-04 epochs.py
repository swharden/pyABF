"""

                Ch1 EPOCH    pre      A      B      C   post
                     Type   Step   Step   Step   Step   Step
         First Level (mV)    -10    -20    -10     25     25
         Delta Level (mV)      0      0      0     10      0
 First Duration (samples)    312   1000   4000  10000      0
 Delta Duration (samples)      0      0      0      0      0
   Train Period (samples)      0      0      0      0      0
    Pulse Width (samples)      0      0      0      0      0
    Epoch Start (samples)      0    312   1312   5312  15312
      Epoch End (samples)    312   1312   5312  15312  20311

"""

from imports import *
plt.style.use('bmh')

COLORBLIND_COLORS = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf',
                     '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']


if __name__ == "__main__":

    abf = pyabf.ABF(PATH_DATA+"/18702001-step.abf")  # complex step
    sweep=2
    channel=1
    abf.setSweep(sweep, channel)
    epochs = abf.epochsByChannel[channel]

    for epochNumber in epochs.epochList:
        i1 = epochs.pointStart[epochNumber]
        i2 = epochs.pointEnd[epochNumber]
        plt.plot(abf.sweepX[i1:i2], abf.sweepY[i1:i2],
                 lw=5, alpha=.8, label=epochs.label[epochNumber],
                 color=COLORBLIND_COLORS[epochNumber])
    plt.legend()
    plt.title(time.time())
    plt.tight_layout()
    # plt.show()
    plt.savefig(PATH_HERE+"/dontsync.png")

    print("DONE")
