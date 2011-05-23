# -*- coding: utf-8 -*-
""" Facets exhibit interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import Interface

class IExhibitFacet(Interface):
    """ Access / update one exhibit facet configuration
    """
