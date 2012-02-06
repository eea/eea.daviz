# -*- coding: utf-8 -*-
""" Views exhibit configuration interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import Interface
from zope.schema import TextLine

class IExhibitView(Interface):
    """ Access / update exhibit view configuration
    """
    label = TextLine(title=u'Label for exhibit view')
    section = TextLine(title=u"Section of this view, e.g. Exhibit, Google, etc")

class IViewDirective(Interface):
    """
    Register a daviz view
    """
    name = TextLine(
        title=u"The name of the view.",
        description=u"The name shows up in URLs/paths. For example 'daviz.map'",
        required=True,
        default=u'',
        )

class IDavizViews(Interface):
    """ Utility to get available daviz views
    """
