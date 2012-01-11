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
    mutator = queryAdapter(obj, IDavizConfig)
    if not mutator:
        logger.warn("Couldn't find any IDavizConfig adapter for %s",
                    obj.absolute_url(1))
        return

    if evt.cleanup:
        # Remove all facets
        mutator.delete_facets()

    # Add new facets or edit existing
    for facet, typo in evt.columns:
        if not mutator.facet(facet):
            show = ('label' not in facet) or ('id' not in facet)
            mutator.add_facet(
                name=facet, label=facet, show=show, item_type=typo)
        else:
            mutator.edit_facet(facet, item_type=typo)
