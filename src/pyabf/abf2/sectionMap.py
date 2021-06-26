from pyabf.abfReader import readStruct


class SectionMap:
    """
    Reading three numbers (int, int, long) at specific byte locations
    yields the block position, byte size, and item count of specific
    data stored in sections. Note that a block is 512 bytes. Some of
    these sections are not read by this class because they are either
    not useful for my applications, typically unused, or have an
    unknown memory structure.
    """

    def __init__(self, fb):
        self.ProtocolSection = readStruct(fb, "IIi", 76)
        self.ADCSection = readStruct(fb, "IIi", 92)
        self.DACSection = readStruct(fb, "IIi", 108)
        self.EpochSection = readStruct(fb, "IIi", 124)
        self.ADCPerDACSection = readStruct(fb, "IIi", 140)
        self.EpochPerDACSection = readStruct(fb, "IIi", 156)
        self.UserListSection = readStruct(fb, "IIi", 172)
        self.StatsRegionSection = readStruct(fb, "IIi", 188)
        self.MathSection = readStruct(fb, "IIi", 204)
        self.StringsSection = readStruct(fb, "IIi", 220)
        self.DataSection = readStruct(fb, "IIi", 236)
        self.TagSection = readStruct(fb, "IIi", 252)
        self.ScopeSection = readStruct(fb, "IIi", 268)
        self.DeltaSection = readStruct(fb, "IIi", 284)
        self.VoiceTagSection = readStruct(fb, "IIi", 300)
        self.SynchArraySection = readStruct(fb, "IIi", 316)
        self.AnnotationSection = readStruct(fb, "IIi", 332)
        self.StatsSection = readStruct(fb, "IIi", 348)
