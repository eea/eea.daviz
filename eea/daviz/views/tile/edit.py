""" Edit
"""
from zope.formlib.form import Fields
from eea.daviz.views.tile.interfaces import IExhibitTileEdit
from eea.daviz.views.edit import EditForm

class Edit(EditForm):
    """ Edit tabular view
    """
    label = u"Tile view settings"
    form_fields = Fields(IExhibitTileEdit)
