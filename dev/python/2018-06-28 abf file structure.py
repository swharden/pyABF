# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../../src/")  # for your IDE
import pyabf
import glob

BLOCKSIZE = 512

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

sectionSizes = {'HeaderV1': 1678, 'HeaderV2': 76, 'SectionMap': 216,
                'ProtocolSection': 208, 'ADCSection': 82, 'DACSection': 132,
                'EpochPerDACSection': 30, 'EpochSection': 4, 'TagSection': 64,
                'StringsSection': 0, 'StringsIndexed': 0}


def sectionBytes(section):
    """return [firstByte, byteCount]"""
    assert len(section) == 3
    firstByte = section[0]*BLOCKSIZE
    byteCount = section[1]*section[2]
    return [firstByte, byteCount]


def plotHeader(abfFileName):
    """create a figure showing where the header sections are."""

    abf = pyabf.ABF(fname)

    fileParts = {}
    fileParts["file"] = [0, os.path.getsize(fname)-1]

    if abf.abfFileFormat == 1:
        fileParts["ABFheaderV1"] = [0, 4898+684]  # start byte and size
        fileParts["DataSection"] = [
            abf._headerV1.lDataSectionPtr*BLOCKSIZE, abf.dataPointCount]
    else:
        fileParts["ABFheaderV2"] = [0, 75]
        fileParts["SectionMap"] = [76, 348+16]
        fileParts["ProtocolSection"] = sectionBytes(
            abf._sectionMap.ProtocolSection)
        fileParts["ADCSection"] = sectionBytes(abf._sectionMap.ADCSection)
        fileParts["DACSection"] = sectionBytes(abf._sectionMap.DACSection)
        fileParts["EpochPerDACSection"] = sectionBytes(
            abf._sectionMap.EpochPerDACSection)
        fileParts["EpochSection"] = sectionBytes(
            abf._sectionMap.EpochSection)
        fileParts["TagSection"] = sectionBytes(abf._sectionMap.TagSection)
        fileParts["StringsSection"] = sectionBytes(
            abf._sectionMap.StringsSection)
        fileParts["DataSection"] = sectionBytes(
            abf._sectionMap.DataSection)

    plt.figure(figsize=(12, 3))

    # LEFT SUBPLOT

    for subplot in [121, 122]:
        plt.subplot(subplot)

        for i, part in enumerate(fileParts.keys()):
            firstByte, byteCount = fileParts[part]
            #lastByte = firstByte + byteCount
            color = plt.get_cmap("jet")(i/len(fileParts))
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
    x1 = abf.dataByteStart + abf.dataByteStart*abf.dataPointCount*2
    x2 = os.path.getsize(fname)
    plt.axis([x1-1500, x2+1500, -.5, 1])

    fnameOut = os.path.dirname(os.path.dirname(abfFileName))
    fnameOut +="/headers/"+abf.abfID+"_header.png"
    plt.savefig(fnameOut)
    plt.close()


if __name__ == "__main__":
    for fname in glob.glob(PATH_DATA+"/*.abf"):
        print("generating header map for", os.path.basename(fname))
        plotHeader(fname)

    plt.show()

    print("DONE")
