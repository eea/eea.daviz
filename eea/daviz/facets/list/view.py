# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from interfaces import IExhibitListFacet
from Products.Five.browser import BrowserView

class View(BrowserView):
    implements(IExhibitListFacet)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._data = {}

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    data = property(get_data, set_data)

    def gett(self, key, default=None):
        return self.data.get(key, default)
