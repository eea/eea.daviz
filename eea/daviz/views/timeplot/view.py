# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from Products.Five.browser import BrowserView
from interfaces import IExhibitTimeplotView

class View(BrowserView):
    """ Timeplot view
    """
    label = 'Timeplot View'
    implements(IExhibitTimeplotView)
