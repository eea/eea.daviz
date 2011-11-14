# -*- coding: utf-8 -*-
""" Views exhibit timeline interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope import schema
from zope.interface import Interface
from eea.daviz.views.interfaces import IExhibitView

class IExhibitTimelineView(IExhibitView):
    """ Exhibit timeline view
    """

class IExhibitTimelineEdit(Interface):
    """ Exhibit timeline edit
    """
    start = schema.Choice(
        title=u'Start date',
        description=u"Specify date or starting date",
        required=False,
        vocabulary="eea.daviz.vocabularies.FacetsVocabulary"
    )

    end = schema.Choice(
        title=u'End date',
        description=u"Specify end date if it is the case",
        required=False,
        vocabulary="eea.daviz.vocabularies.FacetsVocabulary"
    )
