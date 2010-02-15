# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

from zope.interface import Interface, Attribute

class IExhibitJsonConverter(Interface):
    """ Converts context data to Json and save the output under annotations.
    """
    exhibitjson = Attribute("Exhibit Json")

    def getCoordinates():
        """ Returns Json output after converting source data. """
