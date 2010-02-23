# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.component import queryAdapter
from zope.interface import implements
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from eea.daviz.interfaces import IDavizConfig

class FacetsVocabulary(object):
    """ Available registered exhibit views
    """
    implements(IVocabularyFactory)

    def _facets(self, context):
        accessor = queryAdapter(context, IDavizConfig)
        for facet in accessor.facets:
            yield facet

    def __call__(self, context=None):
        """ See IVocabularyFactory interface
        """
        return SimpleVocabulary([
            SimpleTerm(facet.get('name'),
                       facet.get('name'),
                       facet.get('label', facet.get('name')))
            for facet in self._facets(context)])

FacetsVocabularyFactory = FacetsVocabulary()
