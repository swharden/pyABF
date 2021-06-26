# TODO: move this logic into the strings section

class StringsIndexed:
    """
    This object provides easy access to strings which are scattered around
    the header files. The StringsSection contains strings, but various headers
    contain values which point to a certain string index. This class connects
    the two, and provides direct access to those strings by their indexed name.
    """

    def __init__(self, headerV2, protocolSection, adcSection, dacSection, stringsSection):

        indexedStrings = stringsSection.strings[0]
        indexedStrings = indexedStrings[indexedStrings.rfind(b'\x00\x00'):]
        indexedStrings = indexedStrings.replace(b'\xb5', b"\x75")  # make mu u
        indexedStrings = indexedStrings.split(b'\x00')[1:]
        indexedStrings = [x.decode("ascii", errors='replace').strip()
                          for x in indexedStrings]
        self.indexedStrings = indexedStrings

        # headerv2
        self.uCreatorName = indexedStrings[headerV2.uCreatorNameIndex]
        self.uModifierName = indexedStrings[headerV2.uModifierNameIndex]
        self.uProtocolPath = indexedStrings[headerV2.uProtocolPathIndex]

        # ProtocolSection
        self.lFileComment = indexedStrings[protocolSection.lFileCommentIndex]

        # ADCSection
        self.lADCChannelName = []
        self.lADCUnits = []
        for i in range(len(adcSection.lADCChannelNameIndex)):
            self.lADCChannelName.append(
                indexedStrings[adcSection.lADCChannelNameIndex[i]])
            self.lADCUnits.append(indexedStrings[adcSection.lADCUnitsIndex[i]])

        # DACSection
        self.lDACChannelName = []
        self.lDACChannelUnits = []
        self.lDACFilePath = []
        self.nLeakSubtractADC = []

        for i in range(len(dacSection.lDACChannelNameIndex)):
            self.lDACChannelName.append(
                indexedStrings[dacSection.lDACChannelNameIndex[i]])
            self.lDACChannelUnits.append(
                indexedStrings[dacSection.lDACChannelUnitsIndex[i]])
            self.lDACFilePath.append(
                indexedStrings[dacSection.lDACFilePathIndex[i]])
            self.nLeakSubtractADC.append(
                indexedStrings[dacSection.nLeakSubtractADCIndex[i]])
