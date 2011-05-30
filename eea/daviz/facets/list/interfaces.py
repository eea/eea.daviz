# -*- coding: utf-8 -*-
""" Facets list exhibit interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from eea.daviz.facets.interfaces import IExhibitFacet

class IExhibitListFacet(IExhibitFacet):
    """ Exhibit list facet
    """
    def gett(key, default):
        """ Get data property
        """
