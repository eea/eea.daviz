# -*- coding: utf-8 -*-
""" Subtypes exhibit interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.annotation.interfaces import IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope import schema
from zope.interface import Interface

class IPossibleExhibitJson(Interface):
    """ Objects which can have Exhibit Json exported data.
    """

class IExhibitJson(Interface):
    """ Objects which have Exhibit Json exported data.
    """

class IDavizSubtyper(Interface):
    """ Support for subtyping objects
    """

    can_enable = schema.Bool(u'Can enable exhibit view',
                             readonly=True)
    can_disable = schema.Bool(u'Can disable disable exhibit view',
                              readonly=True)
    is_exhibit = schema.Bool(u'Is current object exhibit enabled',
                             readonly=True)

    def enable():
        """ Enable exhibit view
        """

    def disable():
        """ Disable exhibit view
        """

__all__ = [
    IAnnotations,
    AttributeAnnotations
]


