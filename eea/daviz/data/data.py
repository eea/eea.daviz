""" Adapters to provide data
"""
import logging
from zope.interface import implements
from eea.app.visualization.interfaces import IVisualizationData

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
        field = self.context.getField('spreadsheet')
        return field.getAccessor(self.context)()
