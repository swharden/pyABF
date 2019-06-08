abfFilePathsA=R"""
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_14_DIC1_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_14_DIC2_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_14_DIC2_0004.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_14_DIC2_0011.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_14_DIC2_0015.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_14_DIC2_0020.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_21_DIC2_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_21_DIC2_0004.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_21_DIC2_0007.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_23_DIC2_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_23_DIC2_0003.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_23_DIC2_0006.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_23_DIC2_0015.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_31_DIC1_0005.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_31_DIC1_0002.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_31_DIC1_0008.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_31_DIC1_0011.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_31_DIC2_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_31_DIC2_0003.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_31_DIC2_0006.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_21_DIC1_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_21_DIC1_0006.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_21_DIC1_0009.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_23_DIC1_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_23_DIC1_0003.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_23_DIC1_0006.abf
""".strip().split("\n")

abfFilePathsB=R"""
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_16_DIC2_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_16_DIC2_0003.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_16_DIC2_0006.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_16_DIC2_0009.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_17_DIC2_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_17_DIC2_0003.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_17_DIC2_0006.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_17_DIC1_0002.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_17_DIC2_0009.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_17_DIC1_0008.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_17_DIC2_0014.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_22_DIC2_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_22_DIC2_0003.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_22_DIC2_0006.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_22_DIC2_0009.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_22_DIC1_0000.abf
X:\Data\F344\Aging Hipp\E-I-balance\2019_05_22_DIC1_0003.abf
""".strip().split("\n")

abfFilePaths = sorted(abfFilePathsA + abfFilePathsB)


import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt
import numpy as np

import pyabf

if __name__=="__main__":
    plt.figure(figsize = (8, 6))
    plt.ylabel("RMS Noise (pA)")
    plt.xlabel("ABF ID")
    plt.title("RMS Noise (20 percentile of all sweeps)")
    for abfNumber, abfPath in enumerate(abfFilePaths):
        print(abfPath)
        abf = pyabf.ABF(abfPath)
        abfRmsBySweep = []
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            snip = abf.sweepY[:abf.sweepEpochs.p2s[0]] # pre-epoch
            abfRmsBySweep.append(np.std(snip))
        abfRms = np.percentile(abfRmsBySweep, 20)
        print("%s.abf RMS = %.04f pA" %(abf.abfID, abfRms))
        if "DIC1" in abf.abfID:
            color = "r"
        else:
            color = "b"
        plt.plot(abfNumber, abfRms, '.-', ms = 20, color = color)
    plt.axis([None, None, 0, None])
    plt.show()