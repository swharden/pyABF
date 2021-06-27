from pyabf.abfReader import readStruct
import datetime


class HeaderV2:
    """
    The first several bytes of an ABF2 file contain variables
    located at specific byte positions from the start of the file.
    """

    def __init__(self, fb):
        fb.seek(0)
        self.sFileSignature = readStruct(fb, "4s")  # 0
        self.fFileVersionNumber = readStruct(fb, "4b")  # 4
        self.uFileInfoSize = readStruct(fb, "I")  # 8
        self.lActualEpisodes = readStruct(fb, "I")  # 12
        self.uFileStartDate = readStruct(fb, "I")  # 16
        self.uFileStartTimeMS = readStruct(fb, "I")  # 20
        self.uStopwatchTime = readStruct(fb, "I")  # 24
        self.nFileType = readStruct(fb, "H")  # 28
        self.nDataFormat = readStruct(fb, "H")  # 30
        self.nSimultaneousScan = readStruct(fb, "H")  # 32
        self.nCRCEnable = readStruct(fb, "H")  # 34
        self.uFileCRC = readStruct(fb, "I")  # 36
        self.uFileGUID = readStruct(fb, "16B")  # 40
        self.uCreatorVersion = readStruct(fb, "4B")  # 56
        self.uCreatorNameIndex = readStruct(fb, "I")  # 60
        self.uModifierVersion = readStruct(fb, "I")  # 64
        self.uModifierNameIndex = readStruct(fb, "I")  # 68
        self.uProtocolPathIndex = readStruct(fb, "I")  # 72

        # format version number
        versionPartsInt = self.fFileVersionNumber[::-1]
        versionParts = [str(x) for x in versionPartsInt]
        self.abfVersionString = ".".join(versionParts)
        self.abfVersionFloat = int("".join(versionParts))/1000.0
        self.abfVersionDict = {}
        self.abfVersionDict["major"] = versionPartsInt[0]
        self.abfVersionDict["minor"] = versionPartsInt[1]
        self.abfVersionDict["bugfix"] = versionPartsInt[2]
        self.abfVersionDict["build"] = versionPartsInt[3]

        # format creator version
        versionPartsInt = self.uCreatorVersion[::-1]
        versionParts = [str(x) for x in versionPartsInt]
        self.creatorVersionString = ".".join(versionParts)
        self.creatorVersionFloat = int("".join(versionParts))/1000.0
        self.creatorVersionDict = {}
        self.creatorVersionDict["major"] = versionPartsInt[0]
        self.creatorVersionDict["minor"] = versionPartsInt[1]
        self.creatorVersionDict["bugfix"] = versionPartsInt[2]
        self.creatorVersionDict["build"] = versionPartsInt[3]

        # format GUID
        guid = []
        for i in [3, 2, 1, 0, 5, 4, 7, 6, 8, 9, 10, 11, 12, 13, 14, 15]:
            guid.append("%.2X" % (self.uFileGUID[i]))
        for i in [4, 7, 10, 13]:
            guid.insert(i, "-")
        self.sFileGUID = "".join(guid)

        # format creation date from values found in the header
        startDate = str(self.uFileStartDate)
        startTime = self.uFileStartTimeMS / 1000
        try:
            startDate = datetime.datetime.strptime(startDate, "%Y%m%d")
        except:
            startDate = datetime.datetime.fromtimestamp(0)
        timeStamp = startDate + datetime.timedelta(seconds=startTime)
        self.abfDateTime = timeStamp
        try:
            self.abfDateTimeString = self.abfDateTime.strftime('%Y-%m-%dT%H:%M:%S.%f')
            self.abfDateTimeString = self.abfDateTimeString[:-3]
        except:
            self.abfDateTimeString = "ERROR"
