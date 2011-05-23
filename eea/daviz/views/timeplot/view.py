# -*- coding: utf-8 -*-
""" Timeplot view
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from eea.daviz.views.view import ViewForm
from eea.daviz.views.timeplot.interfaces import IExhibitTimeplotView

class View(ViewForm):
    """ Timeplot view
    """
    label = 'Timeplot View'
    implements(IExhibitTimeplotView)
