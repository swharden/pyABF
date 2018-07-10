"""
test advanced stimulus waveform generation.
"""

from imports import *
plt.style.use('bmh')

COLORBLIND_COLORS = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf',
                     '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']


if __name__ == "__main__":

    abf = pyabf.ABF(PATH_DATA+"/18702001-biphasicTrain.abf")
    
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
