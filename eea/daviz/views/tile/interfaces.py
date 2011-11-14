# -*- coding: utf-8 -*-
""" Views exhibit tile interfaces
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope import schema
from zope.interface import Interface
from eea.daviz.views.interfaces import IExhibitView

class IExhibitTileView(IExhibitView):
    """ Exhibit tile view
    """

class IExhibitTileEdit(Interface):
    """ Edit tile view
    """
    lens = schema.Text(
        title=u"Lens template",
        description=(u""
            "Edit custom exhibit lens. Leave it blank to use the default one. "
            "See more details "
            "http://www.simile-widgets.org/wiki/Exhibit/Lens_Templates"),
        required=False
    )
