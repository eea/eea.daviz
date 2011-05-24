# -*- coding: utf-8 -*-
""" Subtypes exhibit interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.annotation.interfaces import IAnnotations
from zope.annotation.attribute import AttributeAnnotations

from zope.interface import Interface

class IPossibleExhibitJson(Interface):
    """ Objects which can have Exhibit Json exported data.
    """

class IExhibitJson(Interface):
    """ Objects which have Exhibit Json exported data.
    """

__all__ = [
    IAnnotations,
    AttributeAnnotations
]
