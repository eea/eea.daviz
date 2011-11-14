# -*- coding: utf-8 -*-
""" Timeline View
"""
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
        """ Start property of timeline view
        """
        start = self.data.get('start', None)
        if start:
            return '.%s' % start
        return None

    @property
    def end(self):
        """ End property of timeline view
        """
        end = self.data.get('end', None)
        if end:
            return '.%s' % end
        return None
