""" Upgrade scripts to version 7.5
"""
import logging
from zope.annotation.interfaces import IAnnotations
from persistent.mapping import PersistentMapping
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('eea.daviz.upgrades')

def migrate_daviz_annotations(context):
    """ Migrate Data Provenance from Visualization to Source Data
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type='AssessmentPart')

    total = len(brains)
    logger.info(('Migrating annotations of %s AssessmentParts'), total)
    for brain in brains:
        obj = brain.getObject()
        annot = IAnnotations(obj).get('DAVIZ_CHARTS', {})
        if annot != {}:
            for vis in annot.values():
                for key in vis.keys():
                    embed_type = vis[key]
                    if isinstance(embed_type, str):
                        chart_settings = PersistentMapping()
                        chart_settings['type'] = embed_type
                        vis[key] = chart_settings

    logger.info('Migration finished')

