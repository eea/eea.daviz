# -*- coding: utf-8 -*-
""" Views exhibit thumbnail interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope import schema
from zope.interface import Interface
from eea.daviz.views.interfaces import IExhibitView

class IExhibitThumbnailView(IExhibitView):
    """ Exhibit thumbnail view
    """

class IExhibitThumbnailEdit(Interface):
    """ Exhibit thumbnail edit
    """
    thumbnail =  schema.Choice(
        title=u'Thumbnail',
        description=u"Specify which column should be used to get " \
                                                    "thumbnail url.",
        required=True,
        vocabulary="eea.daviz.vocabularies.FacetsVocabulary"
    )

    columns = schema.List(
        title=u'Columns',
        description=u'Select columns to be shown under thumbnail',
        required=False,
        value_type=schema.Choice(
            vocabulary="eea.daviz.vocabularies.FacetsVocabulary")
    )
