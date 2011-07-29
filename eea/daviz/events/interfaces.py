# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

try:
    from zope.component.interfaces import IObjectEvent
    IObjectEvent #pyflakes
except ImportError:
    #BBB Plone 2.5
    from zope.app.event.interfaces import IObjectEvent

class IDavizEvent(IObjectEvent):
    """ All daviz events should inherit from this class
    """

class IDavizEnabledEvent(IDavizEvent):
    """ Daviz was enabled
    """

class IDavizFacetDeletedEvent(IDavizEvent):
    """ Daviz facet deleted
    """
