# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from zope.component import queryAdapter
from eea.daviz.interfaces import IDavizConfig
from eea.daviz.views.view import ViewForm
from interfaces import IExhibitTabularView

class View(ViewForm):
    """ Tabular view
    """
    label = 'Tabular View'
    implements(IExhibitTabularView)

    @property
    def columns(self):
        columns = self.data.get('columns', [])
        columns = ['.%s' % item for item in columns]
        if self.details:
            columns.append('!label')
        return columns

    @property
    def labels(self):
        accessor = queryAdapter(self.context, IDavizConfig)
        columns = self.data.get('columns', [])

        labels = []
        for column in columns:
            facet = accessor.facet(column, {})
            label = facet.get('label', column)
            labels.append(label)

        if self.details:
            labels.append('Details')
        return labels

    @property
    def details(self):
        """ Show details column?
        """
        return self.data.get('details', False)
