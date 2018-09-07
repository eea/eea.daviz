""" Upgrade scripts to version 12.0
"""
import logging
from Products.CMFCore.utils import getToolByName
from eea.app.visualization.interfaces import IVisualizationConfig
logger = logging.getLogger('eea.daviz')


def cleanup_exhibit(context):
    """ Cleanup eea.exhibit views
    """
    exhibit_views = set([
        'daviz.map',
        'daviz.tabular',
        'daviz.tile',
        'daviz.timeline'
    ])

    exhibit_facets = set([
        'daviz.alpharange.facet',
        'daviz.cloud.facet',
        'daviz.hierarchical.facet',
        'daviz.numeric.facet',
        'daviz.slider.facet',
        'daviz.text.facet'
    ])

    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(object_provides=[
             "eea.app.visualization.subtypes.interfaces.IVisualizationEnabled"])

    count = 0
    total = len(brains)
    logger.info('Searching exhibit within %s Daviz Visualizations', total)
    for brain in brains:
        obj = brain.getObject()
        config = IVisualizationConfig(obj)
        views = [view.get('name') for view in config.views]
        facets = [facet.get('type') for facet in config.facets]
        ex_views = exhibit_views.intersection(views)
        ex_facets = exhibit_facets.intersection(facets)
        if not (ex_views or ex_facets):
            continue

        count += 1
        url = brain.getURL()
        for view in ex_views:
            logger.warn("%s: removing exhibit view: %s", url, view)
            config.delete_view(view)

        for facet in ex_facets:
            logger.warn("%s: removing exhibit facet: %s", url, facet)
            config.delete_facet(facet)

    logger.warn('Cleanup exhibit views/facets on %s objects', count)
