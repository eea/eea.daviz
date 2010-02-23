# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from interfaces import IExhibitTimelineView
from eea.daviz.interfaces import IDavizConfig

class View(BrowserView):
    """ Timeline view
    """
    label = 'Timeline View'
    implements(IExhibitTimelineView)
    _data = {}

    @property
    def data(self):
        if self._data:
            return self._data

        accessor = queryAdapter(self.context, IDavizConfig)
        self._data = accessor.view(self.__name__, {})
        return self._data

    @property
    def start(self):
        start = self.data.get('start', None)
        if start:
            return '.%s' % start
        return None

    @property
    def end(self):
        end = self.data.get('end', None)
        if end:
            return '.%s' % end
        return None
