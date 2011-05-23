# -*- coding: utf-8 -*-
""" View tabular views
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from zope.component import queryAdapter
from eea.daviz.interfaces import IDavizConfig
from eea.daviz.views.view import ViewForm
from eea.daviz.views.tabular.interfaces import IExhibitTabularView

class View(ViewForm):
    """ Tabular view
    """
    label = 'Tabular View'
    implements(IExhibitTabularView)

    @property
    def columns(self):
        """ Returns columns property for tabular view
        """
        columns = self.data.get('columns', [])
        res = ['.%s' % item for item in columns]
        return ', '.join(res)

    @property
    def labels(self):
        """ Returns labels property for tabular view
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        columns = self.data.get('columns', [])

        labels = []
        for column in columns:
            facet = accessor.facet(column, {})
            label = facet.get('label', column)
            labels.append(label)
        return ', '.join(labels)
