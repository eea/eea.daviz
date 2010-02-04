from eea.daviz.facets.interfaces import IExhibitFacet

class IExhibitListFacet(IExhibitFacet):
    """ Exhibit list facet
    """
    def get(key, default):
        """ Get data property
        """
