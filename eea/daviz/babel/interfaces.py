""" Babel translators interfaces

http://simile.mit.edu/wiki/Babel/How_to_call_translator_using_HTTP_GET
"""
from zope.interface import Interface

class IBabelReader(Interface):
    """ Babel reader
    """

class IBabelWriter(Interface):
    """ Babel writer
    """
