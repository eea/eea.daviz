# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.formlib.form import Fields
from interfaces import IExhibitTimelineEdit
from eea.daviz.views.edit import EditForm

class Edit(EditForm):
    """ Edit timeline view
    """
    label = u"Timeline view settings"
    form_fields = Fields(IExhibitTimelineEdit)
