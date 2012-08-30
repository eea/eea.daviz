"""Daviz Vocabularies
"""
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

class DefaultFolder(object):
    """Default Settings Vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        cat = getToolByName(getSite(), 'portal_catalog')
        brains = cat.searchResults(is_folderish=True)
        folders = []
        for brain in brains:
            folder = brain.getObject()
            found = False
            try:
                allowedContentTypes = folder.allowedContentTypes()
            except AttributeError:
                continue
            for allowedContentType in allowedContentTypes:
                if allowedContentType.id == "DavizVisualization":
                    found = True
            if found:
                folders.append(folder)

        terms = []
        terms.append(
            SimpleTerm(
                value='x1',
                token='x1',
                title='x1'))
        terms.append(
            SimpleTerm(
                value='x2',
                token='x2',
                title='x2'))
        terms.append(
            SimpleTerm(
                value='x3',
                token='x3',
                title='x3'))
        return SimpleVocabulary(terms)


DefaultFolderVocabularyFactory = DefaultFolder()