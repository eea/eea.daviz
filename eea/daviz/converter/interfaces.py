# -*- coding: utf-8 -*-
""" Converter exhibit interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

from zope.interface import Interface #, Attribute

class IExhibitJsonConverter(Interface):
    """ Converts CSV to JSON
    """
