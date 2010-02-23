# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.component import queryAdapter
from zope.interface import implements
from Products.Five.browser import BrowserView
from interfaces import IExhibitMapView
from eea.daviz.interfaces import IDavizConfig

class View(BrowserView):
    """ Thumbnail view
    """
    label = 'Map View'
    implements(IExhibitMapView)

    @property
    def latlng(self):
        accessor = queryAdapter(self.context, IDavizConfig)
        view = accessor.view(self.__name__, {})
        return view.get('latlng', '')
