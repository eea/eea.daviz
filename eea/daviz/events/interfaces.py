""" Daviz Events interfaces
"""
#BBB
from eea.app.visualization.events.interfaces import \
     IVisualizationEvent as IDavizEvent
from eea.app.visualization.events.interfaces import \
     IVisualizationEnabledEvent as IDavizEnabledEvent
from eea.app.visualization.events.interfaces import \
     IVisualizationFacetDeletedEvent as IDavizFacetDeletedEvent

class IDavizRelationsChangedEvent(IDavizEvent):
    """ Daviz relations changed
    """

class IDavizSpreadSheetChanged(IDavizEvent):
    """ Daviz spreadsheet changed
    """

__all__ = [
    IDavizEvent,
    IDavizEnabledEvent,
    IDavizFacetDeletedEvent,
    IDavizRelationsChangedEvent,
    IDavizSpreadSheetChanged,
]
