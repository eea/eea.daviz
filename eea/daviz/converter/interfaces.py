from zope.interface import Interface, Attribute

class IExhibitJsonConverter(Interface):
    """ Converts context data to Json and save the output under annotations.
    """
    exhibitjson = Attribute("Exhibit Json")

    def getCoordinates():
        """ Returns Json output after converting source data. """
