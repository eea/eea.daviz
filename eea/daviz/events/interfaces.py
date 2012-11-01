""" Daviz Events interfaces
"""
from eea.app.visualization.events.interfaces import IVisualizationEvent

class IDavizRelationsChangedEvent(IVisualizationEvent):
    """ Daviz relations changed
    """

class IDavizSpreadSheetChanged(IVisualizationEvent):
    """ Daviz spreadsheet changed
    """

class IDavizExternalChanged(IVisualizationEvent):
    """ Daviz external URL changed
    """

__all__ = [
    IDavizRelationsChangedEvent.__name__,
    IDavizSpreadSheetChanged.__name__,
    IDavizExternalChanged.__name__,
]
