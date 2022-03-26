"""
Code here relates to the creation of arbitrary waveforms to be used as
voltage-clamp or current-clamp stimulus waveforms.
"""

import numpy as np
import matplotlib.pyplot as plt

ATF_HEADER="""
ATF	1.0
8	2
"AcquisitionMode=Episodic Stimulation"
"Comment="
"YTop=2000"
"YBottom=-2000"
"SyncTimeUnits=20"
"SweepStartTimesMS=0.000"
"SignalsExported=IN 0"
"Signals="	"IN 0"
"Time (s)"	"Trace #1"
""".strip()

def create_atf(data, filename="output.atf", rate=20000):
    """Save a stimulus waveform array as an ATF 1.0 file."""
    out=ATF_HEADER
    for i,val in enumerate(data):
        out+="\n%.05f\t%.05f"%(i/rate,val)
    with open(filename,'w') as f:
        f.write(out)
        print("wrote",filename)
    return

def display(data, rate=20000):
    """Display a stimulus waveform array."""
    Xs=np.arange(len(data))/rate
    plt.figure(figsize=(8,2))
    plt.plot(Xs,data)
    plt.margins(0,.1)
    plt.title("Stimulus Waveform")
    plt.ylabel("mV or pA")
    plt.xlabel("Stimulus Time (seconds)")
    plt.savefig("stimulus-waveform.png",dpi=100)
    plt.tight_layout()
    plt.show()

def synth_sine_sweep(freq_max_hz=10, span_sec=10, rate=20000, display=True):
    """
    Returns an array (scaled -1 to 1) of a sine wave of increasing frequency.
    The frequency increases linearly. Zero-intercepts can also be calculated.
    """

    time_scale=freq_max_hz/span_sec/2
    Xs=np.arange(rate*span_sec)/rate
    zi=np.sqrt(np.arange(0,(Xs[-1]**2)*time_scale,1)/time_scale)
    cycle_freqs=np.concatenate(([0],1/np.diff(zi)))
    data=np.sin(2*np.pi*(Xs**2)*time_scale)

    if display:
        plt.figure(figsize=(8,4))
        ax1=plt.subplot(211)
        plt.title("Sine Sweep (0.00 - %.02f Hz)"%(freq_max_hz))
        plt.ylabel("mV or pA")
        plt.plot(Xs,data)
        plt.plot(zi,np.zeros(len(zi)),'rx')
        plt.axhline(0,color='r',alpha=.2,ls='--')
        plt.subplot(212,sharex=ax1)
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Stimulus Time (seconds)")
        plt.plot(zi,cycle_freqs,'.-')
        plt.tight_layout()
        plt.margins(0.02,.1)
        plt.savefig("sine-sweep.png",dpi=100)
        plt.show()

    # pad on both sides with 1 second of zeros
    data=np.concatenate((np.zeros(rate),data,np.zeros(rate)))

    return data

if __name__=="__main__":
    data=synth_sine_sweep(display=False)
    #display(data)
    create_atf(data)
    print("DONE")