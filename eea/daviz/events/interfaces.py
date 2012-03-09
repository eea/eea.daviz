""" Daviz Events interfaces
"""
from eea.app.visualization.events.interfaces import IVisualizationEvent

class IDavizRelationsChangedEvent(IVisualizationEvent):
    """ Daviz relations changed
    """

class IDavizSpreadSheetChanged(IVisualizationEvent):
    """ Daviz spreadsheet changed
    """

__all__ = [
    IDavizRelationsChangedEvent,
    IDavizSpreadSheetChanged,
]
