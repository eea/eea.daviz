""" Upgrade scripts to version 6.0
"""
import logging
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.daviz.upgrades')

def migrate_data_provenance(context):
    """ Migrate Data Provenance from Visualization to Source Data
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type='DavizVisualization')

    total = len(brains)
    logger.info(('Migrating data provenance of %s DavizVisualizations'), total)

    for index, brain in enumerate(brains[:]):
        try:
            doc = brain.getObject()
            logger.info('\t Migration status: %s/%s %s',
                        index+1, total, brain.getURL())

            title = getattr(doc, 'dataTitle', None)
            if title is not None:
                delattr(doc, 'dataTitle')
                doc.getField('dataTitle').getMutator(doc)(title)

            link = getattr(doc, 'dataLink', None)
            if link is not None:
                delattr(doc, 'dataLink')
                doc.getField('dataLink').getMutator(doc)(link)

            owner = getattr(doc, 'dataOwner', None)
            if owner is not None:
                delattr(doc, 'dataOwner')
                doc.getField('dataOwner').getMutator(doc)(owner)

            doc.reindexObject()
        except Exception, err:
            logger.exception(err)

    logger.info(('Finish migration of %s instances of '
                 'Daviz Visualization data provenance'), total)
