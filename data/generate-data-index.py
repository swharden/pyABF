"""
This code reads every ABF in the data folder and updates its header information.
This script outputs HTML files, markdown files, and generates the readme.md in
the root folder of the data directory. It also generates thumbnails for each ABF.
"""

# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../src/")  # for your IDE
import pyabf
pyabf.info()
import datetime
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
plt.style.use('bmh')  # alternative color scheme

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

    print("generating header map for", abf.abfID, "...")

    byteMap = {}
    byteMap["file"] = [0, abf._fileSize-1]

    if abf.abfFileFormat == 1:
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

    for subplot in [121, 122]:
        plt.subplot(subplot)

        #plt.gca().patch.set_alpha(0)
        plt.gca().patch.set_facecolor('w')
        plt.gca().patch.set_facecolor('w')

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
            plt.gca().add_patch(rect)

        # hide the box on the edges
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)

        plt.text(0, -.25, "  "+abf.abfID, ha='left', va='center')
        plt.xlabel("Byte Position")
        plt.margins(.1, .1)
        plt.gca().get_yaxis().set_visible(False)  # hide Y axis
        plt.tight_layout()
        if subplot == 121:
            plt.title("ABF Byte Map for "+abf.abfID+".abf")
        else:
            plt.legend(loc='upper right', fontsize=8,
                       shadow=True, framealpha=1)

    plt.subplot(121)
    plt.axis([-100, abf.dataByteStart+1500, -.5, 1])

    plt.subplot(122)
    x1 = abf.dataByteStart + abf.dataPointCount*2
    x2 = abf._fileSize
    plt.axis([x1-1500, x2+1500, -.5, 1])

    fnameOut = os.path.dirname(os.path.dirname(abf.abfFilePath))
    fnameOut += "/headers/"+abf.abfID+"_map.png"
    plt.savefig(fnameOut)
    plt.close()


def infoPage(abf):
    """
    Create markdown and HTML file containing header details.
    """
    print("generating info for", abf.abfID, "...")
    page = abf.getInfoPage()
    headerPath = os.path.abspath(PATH_HERE+"/../data/headers/")
    with open(headerPath+"/%s.md" % (abf.abfID), 'w') as f:
        f.write(page.generateMarkdown())
    with open(headerPath+"/%s.html" % (abf.abfID), 'w') as f:
        f.write(page.generateHTML())


def plotThumbnail(abf):
    """
    Create a graph some the DAC (command) and ADC (measure) data
    """
    print("generating data preview for", abf.abfID, "...")

    # create figure and subplots
    fig = plt.figure(figsize=(8, 6))
    fig.patch.set_alpha(0)  # transparent background
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
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

    # plot the data sweep by sweep
    for sweep in abf.sweepList:
        abf.setSweep(sweep, absoluteTime=absoluteTime)
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
    fig.savefig(PATH_HERE+"/../data/headers/%s.png" % abf.abfID)
    plt.close()


def go():

    md = "# Sample ABFs\n\n"
    md += "This is a small collection of various ABFs I practice developing with. "
    md += "Many of them were emailed to me by contributors. If you have a unique type "
    md += "of ABF file, email it to me and I will include it here. Note that this page "
    md += "is generated automatically by [generate-data-index](generate-data-index).\n\n"

    md += "ABF (version) | channels | sweeps | protocol | thumbnail\n"
    md += "---|---|---|---|---\n"

    # clear everything that used to be in the headers folder
    for fname in glob.glob(PATH_DATA.replace("abfs", "headers")+'/*.*'):
        #print("deleting", fname, "...")
        os.remove(fname)

    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):

        # load the ABF
        abf = pyabf.ABF(fname)

        # create the graphs
        infoPage(abf)
        plotThumbnail(abf)
        plotHeader(abf)

        # update main readme
        md += "[%s.abf](headers/%s.md) (%s)|" % (abf.abfID,
                                                 abf.abfID, abf.abfVersion)
        md += "%s (%s)|" % (abf.channelCount, ", ".join(abf.adcUnits))
        md += "%s|" % (abf.sweepCount)
        md += "%s|" % (abf.protocol)
        md += "![headers/%s.png](headers/%s.png)" % (abf.abfID, abf.abfID)
        md += "![headers/%s_map.png](headers/%s_map.png)\n" % (
            abf.abfID, abf.abfID)

    # write main readme
    with open(PATH_HERE+"/../data/readme.md", 'w') as f:
        f.write(md)

    print("DATA INDEX GENERATION COMPLETE")


if __name__ == "__main__":
    go()
