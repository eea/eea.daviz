# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""
try:
    from zope.annotation.interfaces import IAnnotations
    IAnnotations #pyflakes
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.interfaces import IAnnotations
IAnnotations #pyflakes
try:
    from zope.annotation.attribute import AttributeAnnotations
    AttributeAnnotations #pyflakes
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.attribute import AttributeAnnotations
AttributeAnnotations #pyflakes
from zope.interface import Interface

class IPossibleExhibitJson(Interface):
    """ Objects which can have Exhibit Json exported data.
    """

class IExhibitJson(Interface):
    """ Objects which have Exhibit Json exported data.
    """
