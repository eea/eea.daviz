""" Upgrade scripts to version 7.5
"""
import logging
from Products.CMFCore.utils import getToolByName
from eea.app.visualization.interfaces import IVisualizationConfig

logger = logging.getLogger('eea.daviz')

def cleanup_exhibit(context):
    """ Cleanup eea.exhibit views
    """
    exhibit = set(['daviz.map', 'daviz.tabular', 'daviz.tile', 'daviz.timeline'])

    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(object_provides="eea.app.visualization.subtypes.interfaces.IVisualizationEnabled")

    count = 0
    total = len(brains)
    logger.info(('Searching eea.exhibit views within %s Daviz Visualizations'), total)
    for brain in brains:
        obj = brain.getObject()
        config = IVisualizationConfig(obj)
        views = [view.get('name') for view in config.views()]
        if not exhibit.intersection(views):
            continue

        url = brain.getURL()
        logger.warn("%s: removing exhibit views: %s", url, views)
        for view in views:
            config.delete_view(view)
            count += 1

    logger.warn('Removed exhibit views on %s objects', count)
