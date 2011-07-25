""" Edit facet
"""
from zope.formlib.form import Fields
from eea.daviz.facets.list.interfaces import IExhibitListFacetEdit
from eea.daviz.facets.edit import EditForm

class Edit(EditForm):
    """ Edit list facet
    """
    form_fields = Fields(IExhibitListFacetEdit)
