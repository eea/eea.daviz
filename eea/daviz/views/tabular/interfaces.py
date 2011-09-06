# -*- coding: utf-8 -*-
""" Tabular views interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope import schema
from zope.interface import Interface
from eea.daviz.views.interfaces import IExhibitView

class IExhibitTabularView(IExhibitView):
    """ Exhibit tabular view
    """

class IExhibitTabularEdit(Interface):
    """ Exhibit tabular edit
    """
    columns = schema.List(
        title=u'Columns',
        description=u'Select columns to be shown in table view',
        required=False, unique=True,
        value_type=schema.Choice(
            vocabulary="eea.daviz.vocabularies.FacetsVocabulary")
    )
    details = schema.Bool(
        title=u'Display details column',
        description=(u"Select this if you want to display a column with "
                     "a 'more' link to item details"),
        required=False
    )
