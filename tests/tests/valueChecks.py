"""
This script records some known values of the first data point of the first
sweep from each channel of ABFs in the demo data folder.

It then uses pyABF to compare the first value to the known first value.
If the ABF reading class gets broken somehow and starts returning bad values,
this script will let you know about it.
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

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

FIRSTVALUES = {}
FIRSTVALUES['05210017_vc_abf1'] = ['-136.29149', '11625.36621']
FIRSTVALUES['14o08011_ic_pair'] = ['-65.52124', '-56.12183']
FIRSTVALUES['14o16001_vc_pair_step'] = ['-25.87890', '-31.49414']
FIRSTVALUES['16d05007_vc_tags'] = ['0.85449']
FIRSTVALUES['16d22006_kim_gapfree'] = ['0.01007', '0.13641']
FIRSTVALUES['171116sh_0011'] = ['-125.73241']
FIRSTVALUES['171116sh_0012'] = ['-120.23925']
FIRSTVALUES['171116sh_0013'] = ['-103.51562']
FIRSTVALUES['171116sh_0014'] = ['-109.98534']
FIRSTVALUES['171116sh_0015'] = ['-119.38476']
FIRSTVALUES['171116sh_0016'] = ['-61.43188']
FIRSTVALUES['171116sh_0017'] = ['-61.70654']
FIRSTVALUES['171116sh_0018'] = ['-62.46948']
FIRSTVALUES['171116sh_0019'] = ['-62.43896']
FIRSTVALUES['171116sh_0020'] = ['72.75390']
FIRSTVALUES['171117_HFMixFRET'] = ['-0.43945', '-94.87915', '0.06989', '0.07080']
FIRSTVALUES['17o05024_vc_steps'] = ['-21.36230']
FIRSTVALUES['17o05026_vc_stim'] = ['-16.11328']
FIRSTVALUES['17o05027_ic_ramp'] = ['-48.00415']
FIRSTVALUES['17o05028_ic_steps'] = ['-47.08862']
FIRSTVALUES['180415_aaron_temp'] = ['-0.35187', '25.02339']
FIRSTVALUES['2018_04_13_0016a_original'] = ['-115.96679', '-15.25879']
FIRSTVALUES['2018_04_13_0016b_modified'] = ['-115.96679', '-7.44399']
FIRSTVALUES['model_vc_ramp'] = ['-138.42772']
FIRSTVALUES['model_vc_step'] = ['-140.13670']
FIRSTVALUES['18702001-biphasicTrain'] = ['-10.74219', '-1.03607']
FIRSTVALUES['18702001-cosTrain'] = ['-8.05664', '-1.03638']
FIRSTVALUES['18702001-pulseTrain'] = ['-11.71875', '-1.03607']
FIRSTVALUES['18702001-ramp'] = ['-12.20703', '-1.03638']
FIRSTVALUES['18702001-step'] = ['-10.49805', '-1.03546']
FIRSTVALUES['18702001-triangleTrain'] = ['-9.88769', '-1.03577']
FIRSTVALUES['130618-1-12'] = ['-188.33015']
FIRSTVALUES['18711001'] = ['-66.66565']
FIRSTVALUES['18713001'] = ['-64.27002']
FIRSTVALUES['sine sweep magnitude 20'] = ['0.00000']
FIRSTVALUES['171116sh_0015-ATFwaveform'] = ['-119.38476']
FIRSTVALUES['2018_08_23_0009'] = ['-138.42772']
FIRSTVALUES['18807005'] = ['506.59180']
FIRSTVALUES['18808025'] = ['-14.77051']
FIRSTVALUES['File_axon_2'] = ['-55.28870']
FIRSTVALUES['File_axon_3'] = ['-15.50000', '-22000.00000']
# ABFFIO.DLL TELLS ME File_axon_3 SHOULD BE: ['-0.15500', '-55.00000']
FIRSTVALUES['File_axon_4'] = ['-0.00610']
FIRSTVALUES['File_axon_5'] = ['-71.05103']
FIRSTVALUES['File_axon_6'] = ['-56.47583', '-0.03357']
FIRSTVALUES['File_axon_7'] = ['-1.48067']
FIRSTVALUES['File_axon_1'] = ['2.18811']
FIRSTVALUES['abf1_with_tags'] = ['-34.54589']
FIRSTVALUES['2018_11_16_sh_0006'] = ['-119.14062']
FIRSTVALUES['sample trace_0054'] = ['0.00931']
FIRSTVALUES['f1'] = ['-30.51758', '-4.27246', '3100.58594', '3445.43457']
FIRSTVALUES['171116sh_0020_saved'] = ['72.72339']
FIRSTVALUES['f1_saved'] = ['-30.51758']
FIRSTVALUES['2018_12_09_pCLAMP11_0001'] = ['-3.65051']
FIRSTVALUES['18425108'] = ['0.07935', '-71.35010']
FIRSTVALUES['2018_05_08_0028-IC-VC-pair'] = ['-68.57300', '-153.32030']
FIRSTVALUES['18425108_abf1'] = ['0.07935', '-71.31958']
FIRSTVALUES['pclamp11_4ch'] = ['-0.24017', '-0.08545', '-0.00793', '0.27313']
FIRSTVALUES['pclamp11_4ch_abf1'] = ['-0.23987', '-0.08514', '-0.00763', '0.27313']
FIRSTVALUES['2018_12_15_0000'] = ['-0.16541', '0.26764', '0.04761', '-0.28351']
FIRSTVALUES['vc_drug_memtest'] = ['-7.20215']

def go():
    print("Checking first values ", end="")
    valuesNeedUpdating = False
    for fname in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(fname)
        firstValues = []  # one per channel
        for channel in abf.channelList:
            abf.setSweep(0, channel)
            firstValues.append("%.05f" % (abf.sweepY[0]))
        if abf.abfID in FIRSTVALUES.keys():
            if not firstValues == FIRSTVALUES[abf.abfID]:
                print("\n\nERROR WITH", abf.abfID)
                print("  expected:", FIRSTVALUES[abf.abfID])
                print("  actual:", firstValues)
                #raise ValueError
            #print("Verified first values of", abf.abfID)
            print(".", end="")
            sys.stdout.flush()
        else:
            valuesNeedUpdating = True
            print("FIRSTVALUES['%s'] = %s" % (abf.abfID, firstValues))
    if valuesNeedUpdating:
        print()
        print("UPDATE FIRSTVALUES TO INCLUDE NEW DATA!")
        raise NotImplementedError
    print(" OK")


if __name__ == "__main__":
    go()
    print("DONE")
