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

    #TODO: Migration 

    logger.info(('Finish migration of %s instances of '
                 'Daviz Visualization data provenance'), total)
