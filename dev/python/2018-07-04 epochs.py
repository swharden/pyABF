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

    #abf = pyabf.ABF(PATH_DATA+"/171116sh_0013.abf")  # ramp
    #abf = pyabf.ABF(PATH_DATA+"/2018_04_13_0016a_original.abf") # delta t
    #abf = pyabf.ABF(PATH_DATA+"/14o16001_vc_pair_step.abf")  # delta level
    #abf = pyabf.ABF(PATH_DATA+"/18702001-step.abf")  # complex step
    #abf = pyabf.ABF(PATH_DATA+"/18702001-ramp.abf")  # complex ramp
    #abf = pyabf.ABF(PATH_DATA+"/05210017_vc_abf1.abf")  # abf1 step
    #abf = pyabf.ABF(PATH_DATA+"/171116sh_0013.abf")  # ramps held
    #abf = pyabf.ABF(PATH_DATA+"/17o05027_ic_ramp.abf")  # weird
    #abf = pyabf.ABF(PATH_DATA+"/171116sh_0014.abf")  # weird

    abf = pyabf.ABF(PATH_DATA+"/130618-1-12.abf")  # weird
    
    channel=abf.channelCount-1
    
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, channel)
        epochs = abf.epochsByChannel[channel]
      
        ax1.plot(abf.sweepX, abf.sweepY, alpha=.6)
        ax2.plot(abf.sweepX, abf.sweepC, alpha=.6)

    # decorate the plot
    ax1.set_title("ADC Signal")
    ax1.set_ylabel(abf.sweepLabelY)
    ax2.set_title("DAC Command")
    ax2.set_ylabel(abf.sweepLabelC)
    ax2.set_xlabel(abf.sweepLabelX)

    fig.tight_layout()
    plt.show()
    #fig.savefig(PATH_HERE+"/dontsync.png")

    #import webbrowser
    #webbrowser.open(PATH_HERE+"/dontsync.png")

    print("DONE")
