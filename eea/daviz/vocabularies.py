from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName

class DefaultFolder(object):
    implements(IVocabularyFactory)

    def __call__(self, context=None):
#        import pdb; pdb.set_trace()
#        cat = getToolByName(context, 'portal_catalog')

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

