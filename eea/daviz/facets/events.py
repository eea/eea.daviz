# -*- coding: utf-8 -*-
""" Facets events module
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

import logging
from zope.component import queryAdapter
from eea.daviz.interfaces import IDavizConfig
logger = logging.getLogger('eea.daviz.facets.events')

def create_default_facets(obj, evt):
    """ Create default facets
    """
    columns = evt.columns
    if not len(columns):
        logger.warn('Empty json for %s', obj.absolute_url(1))
        return

    mutator = queryAdapter(obj, IDavizConfig)
    if not mutator:
        logger.warn("Couldn't find any IDavizConfig adapter for %s",
                    obj.absolute_url(1))
        return

    # Remove all facets
    mutator.delete_facets()

    # Add new facets
    for facet in columns:
        if facet in ['id', 'label']:
            continue
        mutator.add_facet(name=facet, label=facet, show=True)
