""" Handle events
"""
from eea.daviz.views.events import facet_deleted

def timeline_facet_deleted(obj, evt):
    """ Cleanup removed facet from view properties
    """
    return facet_deleted(obj, evt, 'daviz.timeline')
