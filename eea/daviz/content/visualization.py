""" Daviz Visualization
"""
from zope.interface import implements
from plone.app.folder.folder import ATFolder
from eea.daviz.content.interfaces import IDavizVisualization
from eea.daviz.content import schema as daviz_schema

class DavizVisualization(ATFolder):
    """ Daviz Visualization
    """
    implements(IDavizVisualization)

    meta_type = 'DavizVisualization'
    portal_type = 'DavizVisualization'
    archetype_name = 'DavizVisualization'

    schema = daviz_schema.DAVIZ_SCHEMA
