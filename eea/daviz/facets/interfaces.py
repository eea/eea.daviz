# -*- coding: utf-8 -*-
""" Facets exhibit interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope import schema
from zope.interface import Interface

class IExhibitFacet(Interface):
    """ Access / update one exhibit facet configuration
    """

class IExhibitAddFacet(Interface):
    """ Add exhibit facet
    """
    name = schema.TextLine(
        title=u'Id',
        description=(u"Facet id. Same as the key id in your Exhibit JSON. "
                     "(e.g. publishDate)"))
    label = schema.TextLine(
        title=u'Friendly name',
        description=u"Label for exhibit facet (e.g. Effective Date)",
        required=False
    )
