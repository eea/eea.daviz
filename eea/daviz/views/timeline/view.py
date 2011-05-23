# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from eea.daviz.views.timeline.interfaces import IExhibitTimelineView
from eea.daviz.views.view import ViewForm

class View(ViewForm):
    """ Timeline view
    """
    label = 'Timeline View'
    implements(IExhibitTimelineView)

    @property
    def start(self):
        start = self.data.get('start', None)
        if start:
            return '.%s' % start
        return None

    @property
    def end(self):
        end = self.data.get('end', None)
        if end:
            return '.%s' % end
        return None
