# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from eea.daviz.views.view import ViewForm
from interfaces import IExhibitThumbnailView

class View(ViewForm):
    """ Thumbnail view
    """
    label = 'Thumbnail View'
    implements(IExhibitThumbnailView)

    @property
    def thumbnail(self):
        """ Return thumbnail column
        """
        thumbnail = self.data.get('thumbnail', None)
        if thumbnail:
            return '.%s' % thumbnail
        return None

    @property
    def columns(self):
        """ Return columns
        """
        for column in self.data.get('columns', []):
            yield '.%s' % column
