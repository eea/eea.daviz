# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from eea.daviz.facets.interfaces import IExhibitFacet

class IExhibitListFacet(IExhibitFacet):
    """ Exhibit list facet
    """
    def get(key, default):
        """ Get data property
        """
