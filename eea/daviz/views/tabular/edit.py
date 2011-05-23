# -*- coding: utf-8 -*-
""" Edit tabular views
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.formlib.form import Fields
from eea.daviz.views.tabular.interfaces import IExhibitTabularEdit
from eea.daviz.views.edit import EditForm

class Edit(EditForm):
    """ Edit tabular view
    """
    label = u"Tabular view settings"
    form_fields = Fields(IExhibitTabularEdit)
