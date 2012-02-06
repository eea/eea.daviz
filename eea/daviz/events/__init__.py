""" Daviz/events init module with DavizEnabledEvent class
"""
from zope.interface import implements
from eea.daviz.events.interfaces import IDavizEnabledEvent
from eea.daviz.events.interfaces import IDavizFacetDeletedEvent
from eea.daviz.events.interfaces import IDavizRelationsChangedEvent

class DavizEnabledEvent(object):
    """ Sent if a document was converted to exhibit json
    """
    implements(IDavizEnabledEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.columns = kwargs.get('columns', [])
        self.cleanup = kwargs.get('cleanup', True)

class DavizFacetDeletedEvent(object):
    """ Sent if a daviz facet was deleted
    """
    implements(IDavizFacetDeletedEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.facet = kwargs.get('facet', '')

class DavizRelationsChanged(object):
    """ Sent if relations for a Daviz Presentation were changed
    """
    implements(IDavizRelationsChangedEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.relatedItems = kwargs.get('relatedItems', [])
