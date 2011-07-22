# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from eea.daviz.views.view import ViewForm
from interfaces import IExhibitTileView

class View(ViewForm):
    """ Tile view
    """
    label = 'Tile View'
    implements(IExhibitTileView)

    @property
    def lens(self):
        """ View custom lens
        """
        return self.data.get('lens', '')
