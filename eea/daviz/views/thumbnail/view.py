# -*- coding: utf-8 -*-
""" Edit tile views
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from eea.daviz.views.view import ViewForm
from eea.daviz.views.thumbnail.interfaces import IExhibitThumbnailView

class View(ViewForm):
    """ Thumbnail view
    """
    label = 'Thumbnail View'
    implements(IExhibitThumbnailView)

    @property
    def thumbnail(self):
        """ Returns thumbnail column
        """
        thumbnail = self.data.get('thumbnail', None)
        if thumbnail:
            return '.%s' % thumbnail
        return None

    @property
    def columns(self):
        """ Returns columns
        """
        for column in self.data.get('columns', []):
            yield '.%s' % column
