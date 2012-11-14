""" Module to enable or disable visualization
"""
from eea.app.visualization.subtypes.support import DavizPublicSupport

class DavizVisualizationSupport(DavizPublicSupport):
    """ Enable/Disable visualization
    """
    @property
    def is_visualization(self):
        """ Is visualization enabled?
        """
        return True
