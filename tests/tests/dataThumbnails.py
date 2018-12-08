"""
This code reads every ABF in the data folder and updates its header information.
This script outputs HTML files, markdown files, and generates the readme.md in
the root folder of the data directory. It also generates thumbnails for each ABF
"""

# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
sys.path.insert(0, PATH_PROJECT+"/src/")
import pyabf
import glob
import numpy as np

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

import datetime
import matplotlib.patches as patches
import matplotlib.pyplot as plt

# now you are free to import additional modules
import glob

sectionSizes = {'HeaderV1': 1678, 'HeaderV2': 76, 'SectionMap': 216,
                'ProtocolSection': 208, 'ADCSection': 82, 'DACSection': 132,
                'EpochPerDACSection': 30, 'EpochSection': 4, 'TagSection': 64,
                'StringsSection': 0, 'StringsIndexed': 0}


def sectionBytes(section):
    """return [firstByte, byteCount]"""
    assert len(section) == 3
    firstByte = section[0]*512
    byteCount = section[1]*section[2]
    return [firstByte, byteCount]


def plotHeader(abf):
    """create a figure showing where the header sections are."""

    byteMap = {}
    byteMap["file"] = [0, abf._fileSize-1]

    if abf.abfVersion["major"] == 1:
        byteMap["ABFheaderV1"] = [0, 4898+684]  # start byte and size
        byteMap["DataSection"] = [abf.dataByteStart,
                                  abf.dataPointByteSize*abf.dataPointCount]
    else:
        byteMap["ABFheaderV2"] = [0, 75]
        byteMap["SectionMap"] = [76, 348+16]
        byteMap["ProtocolSection"] = sectionBytes(
            abf._sectionMap.ProtocolSection)
        byteMap["ADCSection"] = sectionBytes(abf._sectionMap.ADCSection)
        byteMap["DACSection"] = sectionBytes(abf._sectionMap.DACSection)
        byteMap["EpochPerDACSection"] = sectionBytes(
            abf._sectionMap.EpochPerDACSection)
        byteMap["EpochSection"] = sectionBytes(
            abf._sectionMap.EpochSection)
        byteMap["TagSection"] = sectionBytes(abf._sectionMap.TagSection)
        byteMap["StringsSection"] = sectionBytes(
            abf._sectionMap.StringsSection)
        byteMap["DataSection"] = sectionBytes(
            abf._sectionMap.DataSection)

    fig = plt.figure(figsize=(12, 3))
    fig.patch.set_alpha(0)  # transparent background

    # LEFT SUBPLOT

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    for ax in [ax1, ax2]:

        ax.patch.set_facecolor('w')
        ax.patch.set_facecolor('w')

        for i, part in enumerate(byteMap.keys()):
            firstByte, byteCount = byteMap[part]
            #lastByte = firstByte + byteCount
            color = plt.get_cmap("jet")(i/len(byteMap))
            if part == "file":
                rect = patches.Rectangle((firstByte, -.5), byteCount, .5,
                                         linewidth=0, facecolor='.5',
                                         alpha=1, label=part)
            else:
                rect = patches.Rectangle((firstByte, 0), byteCount, 1,
                                         linewidth=0, facecolor=color,
                                         alpha=1, label=part)
            ax.add_patch(rect)

        # hide the box on the edges
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.text(0, -.25, "  "+abf.abfID, ha='left', va='center')
        plt.xlabel("Byte Position")
        plt.margins(.1, .1)
        ax.get_yaxis().set_visible(False)  # hide Y axis
        plt.tight_layout()
        ax1.set_title("ABF Byte Map for "+abf.abfID+".abf")
        if len(ax2.get_legend_handles_labels()[0]):
            ax2.legend(loc='upper right', fontsize=8, shadow=True, framealpha=1)

    ax1.axis([-100, abf.dataByteStart+1500, -.5, 1])

    x1 = abf.dataByteStart + abf.dataPointCount*2
    x2 = abf._fileSize
    ax2.axis([x1-1500, x2+1500, -.5, 1])

    #fnameOut = os.path.dirname(os.path.dirname(abf.abfFilePath))
    #fnameOut += "/headers/"+abf.abfID+"_map.png"
    # plt.savefig(fnameOut)
    fig.savefig(f"{PATH_PROJECT}/data/headers/{abf.abfID}_map.png")
    plt.close()


def plotThumbnail(abf):
    """
    Create a graph some the DAC (command) and ADC (measure) data
    """
    # create figure and subplots
    fig = plt.figure(figsize=(8, 6))
    fig.patch.set_alpha(0)  # transparent background
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.grid(alpha=.4, ls='--')
    ax2.grid(alpha=.4, ls='--')
    ax1.patch.set_facecolor('w')
    ax2.patch.set_facecolor('w')
    ax1.set_xmargin(0)
    ax2.set_xmargin(0)

    # overlap or continuous view depends on protocol
    absoluteTime = False
    if "0111" in abf.protocol:
        absoluteTime = True
    if "loose" in abf.protocol:
        absoluteTime = True

    # usually we plot channel 0, but sometimes manually override
    channel = 0
    if "18702001" in abf.abfID:
        channel = 1

    # plot the data sweep by sweep
    maxSweepsToPlot = min(abf.sweepCount,20)
    for sweep in range(maxSweepsToPlot):
        abf.setSweep(sweep, channel=channel, absoluteTime=absoluteTime)
        ax1.plot(abf.sweepX, abf.sweepY, alpha=.5, color='b', lw=.5)
        ax2.plot(abf.sweepX, abf.sweepC, color='r')

    # decorate plot and save it
    ax1.set_title("{}.abf [channel: {}/{}] [sweeps: {}]".format(
        abf.abfID, abf.sweepChannel+1, abf.channelCount, abf.sweepNumber+1))
    ax1.set_ylabel(abf.sweepLabelY)
    ax1.set_xlabel(abf.sweepLabelX)
    ax2.set_ylabel(abf.sweepLabelC)
    ax2.set_xlabel(abf.sweepLabelX)
    fig.tight_layout()
    ax1.margins(0,.1)
    ax2.margins(0,.1)
    fig.savefig(f"{PATH_PROJECT}/data/headers/{abf.abfID}.png")
    plt.close()


def deleteImages():
    """Delete all markdown and HTML files from the data folder."""
    for fname in glob.glob(f"{PATH_PROJECT}/data/headers/*.png"):
        log.debug(f"Deleting {fname}")
        os.remove(fname)


def go(processData=True):

    print("Generating data thumbnails", end=" ")
    if processData:
        deleteImages()

    md = "# Sample ABFs\n\n"
    md += "This is a small collection of various ABFs I practice developing with. "
    md += "Many of them were emailed to me by contributors. If you have a unique type "
    md += "of ABF file, email it to me and I will include it here. Note that this page "
    md += "is generated automatically by [dataThumbnails.py](/tests/tests/dataThumbnails.py).\n\n"

    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):

        # load the ABF
        abf = pyabf.ABF(fname)
        abfIDsafe = abf.abfID.replace(" ", "%20")

        # indicate which ABF is being challenged
        log.debug("creating thumbnail for %s" % abf.abfID)

        # create the graphs
        if processData:
            plotThumbnail(abf)
            #plotHeader(abf)

        # update the console
        print(".", end="")
        sys.stdout.flush()

        # update main readme
        md += "## %s.abf\n"%(abf.abfID)
        md += "ABF (version %s) "%(abf.abfVersionString)
        if abf.channelCount==1:
            md += "with 1 channel "
        else:
            md += "with %d channels " % (abf.channelCount)
        md += "(%s), "%(", ".join(abf.adcUnits))
        md += "%d sweeps, "%(abf.sweepCount)
        md += "recorded using protocol _%s_.<br> "%(abf.protocol)
        md += "\n[View the full header](headers/%s.md)" % (abfIDsafe)
        md += "<a href='headers/%s.png'><img src='headers/%s.png'></a>"%(abfIDsafe, abfIDsafe)
        md += "\n\n"

    # write main readme
    with open(PATH_PROJECT+"/data/readme.md", 'w') as f:
        f.write(md)

    print(" OK")


if __name__ == "__main__":
    print("DO NOT RUN THIS DIRECTLY")
    go(True)