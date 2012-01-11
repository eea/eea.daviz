""" Daviz Events interfaces
"""

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

from zope.component.interfaces import IObjectEvent

class IDavizEvent(IObjectEvent):
    """ All daviz events should inherit from this class
    """

class IDavizEnabledEvent(IDavizEvent):
    """ Daviz was enabled
    """

class IDavizFacetDeletedEvent(IDavizEvent):
    """ Daviz facet deleted
    """

class IDavizRelationsChangedEvent(IDavizEvent):
    """ Daviz relations changed
    """

__all__ = [
    IDavizEvent,
    IDavizEnabledEvent,
    IDavizFacetDeletedEvent,
    IDavizRelationsChangedEvent,
]
