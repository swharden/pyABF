from pyabf.abf2.section import Section

class DataSection(Section):

    def __init__(self, fb):
        Section.__init__(self, fb, 236)