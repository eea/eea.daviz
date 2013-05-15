""" Upgrade scripts to version 7.5
"""
import logging
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.daviz.upgrades')

def migrate_data_provenance_to_multiple_data_provenances(context):
    """ Migrate Data Provenance from Visualization to Source Data
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type='DavizVisualization')

    total = len(brains)
    logger.info(('Migrating data provenance of %s DavizVisualizations'), total)

    with_related = 0
    without_provenance_info = 0
    migrated = 0
    for index, brain in enumerate(brains[:]):
        try:
            logger.info('\t Migration status: %s/%s %s',
                        index+1, total, brain.getURL())
            doc = brain.getObject()
            if len(doc.getRelatedItems()) == 0:
                title = doc['dataTitle']
                owner = doc['dataOwner']
                link = doc['dataLink']
                if title != u'' or owner != u'' or link != u'':
                    logger.info(
                        '\t\t Migrating provenance info for visualization')
                    provenance = (
                        {'title' : title,
                        'owner' : owner,
                        'link' : link},
                    )
                    doc.getField('provenances').getMutator(doc)(provenance)
                    doc.reindexObject()
                    migrated = migrated + 1
                else:
                    logger.info('\t\t No provenance info')
                    without_provenance_info = without_provenance_info + 1
            else:
                logger.info('\t\t Provenance info stored in related item')
                with_related = with_related + 1
        except Exception, err:
            logger.exception(err)

    logger.info(('Finish migration of %s instances of '
                 'Daviz Visualization data provenance'), total)

    logger.info('\t Migrated %s: ', migrated)
    logger.info('\t No provenance info: %s ', without_provenance_info)
    logger.info('\t Provenance info from related: %s ', with_related)

