# -*- coding: utf-8 -*-
""" Views exhibit tile interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from eea.daviz.views.interfaces import IExhibitView

class IExhibitTilelView(IExhibitView):
    """ Exhibit tile view
    """
