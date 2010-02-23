# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig
from interfaces import IExhibitTabularView

class View(BrowserView):
    """ Tabular view
    """
    label = 'Tabular View'
    implements(IExhibitTabularView)

    @property
    def columns(self):
        accessor = queryAdapter(self.context, IDavizConfig)
        name = self.__name__
        view = accessor.view(name, {})
        columns = view.get('columns', [])
        res = ['.%s' % item for item in columns]
        return ', '.join(res)

    @property
    def labels(self):
        accessor = queryAdapter(self.context, IDavizConfig)
        name = self.__name__
        view = accessor.view(name, {})
        columns = view.get('columns', [])

        labels = []
        for column in columns:
            facet = accessor.facet(column, {})
            label = facet.get('label', column)
            labels.append(label)
        return ', '.join(labels)
