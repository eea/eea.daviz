# -*- coding: utf-8 -*-
""" Basic layer for daviz views
"""

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig

class ViewForm(BrowserView):
    """ Basic layer for daviz views. For more details on how to use this,
    see implementation in eea.daviz.views.map.view.View.
    """
    label = ''
    section = 'Exhibit'
    _data = {}

    @property
    def data(self):
        """ Return saved configuration
        """
        if self._data:
            return self._data

        accessor = queryAdapter(self.context, IDavizConfig)
        self._data = accessor.view(self.__name__, {})
        return self._data
