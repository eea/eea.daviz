# -*- coding: utf-8 -*-
""" Edit thumbnail views
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.formlib.form import Fields
from eea.daviz.views.thumbnail.interfaces import IExhibitThumbnailEdit
from eea.daviz.views.edit import EditForm

class Edit(EditForm):
    """ Edit thumbnail view
    """
    label = u"Thumbnail view settings"
    form_fields = Fields(IExhibitThumbnailEdit)
