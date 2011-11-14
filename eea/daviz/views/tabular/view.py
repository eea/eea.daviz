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
    def details(self):
        """ Show details column?
        """
        return self.data.get('details', False)

    @property
    def columns(self):
        """ Returns columns property for tabular view
        """
        columns = self.data.get('columns', [])
        for column in columns:
            yield '.%s' % column

        if self.details:
            yield '!label'

    @property
    def formats(self):
        """ Column formats
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        columns = self.data.get('columns', [])
        for column in columns:
            facet = accessor.facet(column, {})
            itype = facet.get('item_type', 'text')
            yield itype

        if self.details:
            yield "item {title: expression('more')}"

    @property
    def labels(self):
        """ Returns labels property for tabular view
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        columns = self.data.get('columns', [])

        for column in columns:
            facet = accessor.facet(column, {})
            label = facet.get('label', column)
            yield label

        if self.details:
            yield 'Details'
