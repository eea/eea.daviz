# -*- coding: utf-8 -*-
""" Exhibit map view interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope import schema
from zope.interface import Interface
from eea.daviz.views.interfaces import IExhibitView

class IExhibitMapView(IExhibitView):
    """ Exhibit map view
    """

class IExhibitMapEdit(Interface):
    """ Exhibit map edit
    """
    latlng = schema.Choice(
        title=u'Latitude and Longitude column',
        description=u"Specify which column should be used to get latitude " \
                                                            "and longitude.",
        required=False,
        vocabulary="eea.daviz.vocabularies.FacetsVocabulary"
    )
