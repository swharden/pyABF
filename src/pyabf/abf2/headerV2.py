from pyabf.abf2.section import Section
import datetime


class HeaderV2(Section):
    """
    The first several bytes of an ABF2 file contain variables
    located at specific byte positions from the start of the file.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 0)
        self.seek(0)
        self.sFileSignature = self.readString(4)  # 0
        self.fFileVersionNumber = self.readBytes(4)  # 4
        self.uFileInfoSize = self.readUInt32()  # 8
        self.lActualEpisodes = self.readUInt32()  # 12
        self.uFileStartDate = self.readUInt32()  # 16
        self.uFileStartTimeMS = self.readUInt32()  # 20
        self.uStopwatchTime = self.readUInt32()  # 24
        self.nFileType = self.readUInt16()  # 28
        self.nDataFormat = self.readUInt16()  # 30
        self.nSimultaneousScan = self.readUInt16()  # 32
        self.nCRCEnable = self.readUInt16()  # 34
        self.uFileCRC = self.readUInt32()  # 36
        self.uFileGUID = self.readBytes(16)  # 40
        self.uCreatorVersion = self.readBytes(4)  # 56
        self.uCreatorNameIndex = self.readUInt32()  # 60
        self.uModifierVersion = self.readUInt32()  # 64
        self.uModifierNameIndex = self.readUInt32()  # 68
        self.uProtocolPathIndex = self.readUInt32()  # 72

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
        try:
            startDate = str(self.uFileStartDate)
            startDate = datetime.datetime.strptime(startDate, "%Y%m%d")
            startTime = self.uFileStartTimeMS / 1000
            timeStamp = startDate + datetime.timedelta(seconds=startTime)
            self.abfDateTime = timeStamp
            self.abfDateTimeString = timeStamp.strftime('%Y-%m-%dT%H:%M:%S.%f')
            self.abfDateTimeString = self.abfDateTimeString[:-3]
        except:
            self.abfDateTime = datetime.datetime(1, 1, 1)
            self.abfDateTimeString = "ERROR"
