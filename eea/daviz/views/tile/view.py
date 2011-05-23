# -*- coding: utf-8 -*-
""" Tiles view module
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from eea.daviz.views.view import ViewForm
from eea.daviz.views.tile.interfaces import IExhibitTilelView

class View(ViewForm):
    """ Tile view
    """
    label = 'Tile View'
    implements(IExhibitTilelView)
