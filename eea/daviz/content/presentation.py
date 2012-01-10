""" Daviz Presentation
"""
from zope.interface import implements
from plone.app.folder.folder import ATFolder
from eea.daviz.content.interfaces import IDavizPresentation

class DavizPresentation(ATFolder):
    """ Daviz Presentation
    """
    implements(IDavizPresentation)

    meta_type = 'DavizPresentation'
    portal_type = 'DavizPresentation'
    archetype_name = 'DavizPresentation'

    schema = ATFolder.schema.copy()
