"""
These tests ensure ABF comments work and stay working.
"""

import os
import sys
import pytest

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
PATH_HEADERS = os.path.abspath(PATH_PROJECT+"/data/headers/")

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
except:
    raise ImportError("couldn't import local pyABF")

COMMENT_TAGS = {}
COMMENT_TAGS['16d05007_vc_tags.abf'] = [['+TGOT', '-TGOT'], [173.9776, 294.8608], [86.9888, 147.4304]]
COMMENT_TAGS['19122043.abf'] = [['C9, L3,  RMP -66.8 mv'], [0.9], [0.17437805161590328]]
COMMENT_TAGS['2018_11_16_sh_0006.abf'] = [['+drug at 3min'], [180.3776], [1803.7759999999998]]
COMMENT_TAGS['abf1_with_tags.abf'] = [['APV+CGP+DNQX+ON@6'], [374.95000000000005], [0.41661111111111115]]
COMMENT_TAGS['File_axon_2.abf'] = [['Clampex start acquisition', 'C:\\Axon\\rsultats\\06-05\\11-06-05\\05611005.abf', 'Clampex end (1)', 'Clampex start acquisition'], [26.765, 426.701, 426.701, 625.373], [0.022304166666666667, 0.3555841666666667, 0.3555841666666667, 0.5211441666666667]]
COMMENT_TAGS['File_axon_4.abf'] = [['drogue on'], [0.0], [0.0]]
COMMENT_TAGS['multichannelAbf1WithTags.abf'] = [['+TGOT', '-TGOT'], [173.9776, 294.86080000000004], [2104.9921355111915, 3567.583787053842]]
COMMENT_TAGS['vc_drug_memtest.abf'] = [['+TGOT', '-TGOT'], [399.6672, 520.8576], [199.8336, 260.4288]]

EXTERNAL_TAGS = {}
EXTERNAL_TAGS['ch121219_1_0001.abf'] = [['<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>', '<External>'], [7.68694, 17.68726, 27.68758, 37.6879, 47.6882, 57.68852, 67.68884, 77.68914, 87.68946, 97.68978, 107.69008, 117.6904, 127.69072, 137.69104, 147.69134, 157.69166], [0.04658751515151515, 0.10719551515151514, 0.16780351515151515, 0.22841151515151514, 0.28901939393939396, 0.3496273939393939, 0.41023539393939396, 0.4708432727272727, 0.5314512727272727, 0.5920592727272728, 0.6526671515151515, 0.7132751515151515, 0.7738831515151515, 0.8344911515151514, 0.8950990303030303, 0.9557070303030304]]

def assertTagsMatch(fileName, expectedTag):
    abf = pyabf.ABF(os.path.join(PATH_DATA, fileName))
    expectedComments = expectedTag[0]
    expectedTimesSec = expectedTag[1]
    expectedSweeps = expectedTag[2]
    for i in range(len(abf.tagComments)):
        assert expectedComments[i] == abf.tagComments[i]
        assert expectedTimesSec[i] == abf.tagTimesSec[i]
        assert expectedSweeps[i] == abf.tagSweeps[i]

@pytest.mark.parametrize("fileName", COMMENT_TAGS.keys())
def test_commentTags_areCorrectValues(fileName):
    assertTagsMatch(fileName, COMMENT_TAGS[fileName])
        
@pytest.mark.parametrize("fileName", EXTERNAL_TAGS.keys())
def test_externalTags_areCorrectValues(fileName):
    assertTagsMatch(fileName, EXTERNAL_TAGS[fileName])
