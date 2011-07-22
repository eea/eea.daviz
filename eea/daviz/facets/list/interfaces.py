# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import Interface
from zope.schema import TextLine, Bool, List, Choice
from eea.daviz.facets.interfaces import IExhibitFacet

class IExhibitListFacet(IExhibitFacet):
    """ Exhibit list facet
    """
    def get(key, default):
        """ Get data property
        """

class IExhibitListFacetEdit(Interface):
    """ Exhibit list facet edit
    """
    label = TextLine(title=u'Friendly name',
                     description=u'Label for exhibit facet')
    show = Bool(title=u'Visible', description=u'Is this facet visible?',
            required=False)
