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

    # Remove all views
    mutator.delete_views()

    # Add default view: Tabular view
    mutator.add_view(name=u'daviz.tabular')
