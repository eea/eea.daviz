# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import Interface
from zope.schema import TextLine

class IExhibitView(Interface):
    """ Access / update exhibit view configuration
    """
    label = TextLine(title=u'Label for exhibit view')
