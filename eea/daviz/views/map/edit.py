# -*- coding: utf-8 -*-
""" Edit map view module
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.formlib.form import Fields
from eea.daviz.views.map.interfaces import IExhibitMapEdit
from eea.daviz.views.edit import EditForm

class Edit(EditForm):
    """ Edit map view
    """
    label = u"Map view settings"
    form_fields = Fields(IExhibitMapEdit)
