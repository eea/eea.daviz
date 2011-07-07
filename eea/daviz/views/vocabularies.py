# -*- coding: utf-8 -*-
""" Vocabularies for views
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

import operator
from zope.component import getUtility, queryMultiAdapter
from zope.interface import implements
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from eea.daviz.views.interfaces import IDavizViews

class ViewsVocabulary(object):
    """ Available registered exhibit views
    """
    implements(IVocabularyFactory)

    def _adapters(self, context):
        """ Return adapters
        """
        views = getUtility(IDavizViews)
        for view in views():
            browser = queryMultiAdapter((context, context.REQUEST), name=view)
            yield view, getattr(browser, 'label', view)

    def __call__(self, context=None):
        """ See IVocabularyFactory interface

        views = [
          (u'daviz.map', 'Map View'),
          (u'daviz.timeline', 'Timeline View'),
          (u'daviz.tile', 'Tile View'),
          (u'daviz.tabular', 'Tabular View')
        ]
        """
        views = [(name, label) for name, label in self._adapters(context)]
        views.sort(key=operator.itemgetter(1))
        views = [SimpleTerm(key, key, val) for key, val in views]
        return SimpleVocabulary(views)

ViewsVocabularyFactory = ViewsVocabulary()
