""" Adapters to provide data
"""
import logging
from zope.interface import implements
from zope.component import queryUtility
from eea.app.visualization.interfaces import IVisualizationData
from eea.app.visualization.interfaces import IExternalData

logger = logging.getLogger('eea.daviz')

class DavizVisualization(object):
    """ Data adapter for eea.daviz.content.interfaces.IDavizVisualization
    """
    implements(IVisualizationData)

    def __init__(self, context):
        self.context = context

    @property
    def data(self):
        """ Data to be converted to JSON
        """
        external = self.context.getField('external')
        url = external.getAccessor(self.context)()
        if url:
            data = queryUtility(IExternalData)
            return data(url) if data else u''
        else:
            field = self.context.getField('spreadsheet')
            return field.getAccessor(self.context)()
