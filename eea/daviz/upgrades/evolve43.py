""" Upgrade scripts to version 4.3
"""
import logging
from Products.CMFCore.utils import getToolByName
from Products.contentmigration.archetypes import InplaceATFolderMigrator
logger = logging.getLogger('eea.daviz.upgrades')

class InplaceDavizVisualizationMigrator(InplaceATFolderMigrator):
    """ Migrate DavizPresentation to DavizVisualization
    """
    dst_meta_type = 'DavizVisualization'
    dst_portal_type = 'DavizVisualization'

def presentation2visualization(context):
    """ Migrate DavizPresentation instances to DavizVisualization
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type='DavizPresentation')

    total = len(brains)
    logger.info(('Migrating %s instances of '
                 'DavizPresentation to DavizVisualization'), total)

    for index, brain in enumerate(brains[:]):
        logger.info('\t Migration status: %s/%s', index+1, total)
        try:
            doc = brain.getObject()
            migrator = InplaceDavizVisualizationMigrator(doc)
            migrator.migrate()
            migrator.new.reindexObject()
        except Exception, err:
            logger.exception(err)

    logger.info(('Finish migration of %s instances of '
                 'DavizPresentation to DavizVisualization'), total)
