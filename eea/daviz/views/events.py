# -*- coding: utf-8 -*-
""" Views events
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

import logging
from zope.component import queryAdapter
from eea.daviz.interfaces import IDavizConfig
logger = logging.getLogger('eea.daviz.views.events')

def create_default_views(obj, evt):
    """ Create default views
    """
    mutator = queryAdapter(obj, IDavizConfig)
    if not mutator:
        logger.warn("Couldn't find any IDavizConfig adapter for %s",
                    obj.absolute_url(1))
        return

    if evt.cleanup:
        # Remove all views
        mutator.delete_views()

        # Add default view: Tabular view
        mutator.add_view(name=u'daviz.tabular')


def facet_deleted(obj, evt, daviz_view):
    """ Cleanup removed facet from view properties
    """
    facet = evt.facet
    mutator = queryAdapter(obj, IDavizConfig)
    if not mutator:
        logger.warn("Couldn't find any IDavizConfig adapter for %s",
                    obj.absolute_url(1))
        return

    view = mutator.view(daviz_view)
    if not view:
        return

    changed = False
    properties = dict(view)
    for key, value in properties.items():
        if isinstance(value, (unicode, str)):
            if value == facet:
                properties.pop(key)
                changed = True
        elif isinstance(value, (list, tuple)):
            if facet in value:
                value = list(item for item in value if item != facet)
                properties[key] = value
                changed = True

    if changed:
        mutator.edit_view(daviz_view, **properties)
