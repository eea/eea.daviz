# -*- coding: utf-8 -*-
""" Vocabularies for views
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

import operator
from zope.component import getAdapters
from zope.interface import implements
from zope.interface import Interface
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from eea.daviz.views.interfaces import IExhibitView

class ViewsVocabulary(object):
    """ Available registered exhibit views
    """
    implements(IVocabularyFactory)

    def _adapters(self, context):
        """ Return adapters
        """
        adapters = getAdapters((context, context.REQUEST), Interface)
        for name, adapter in adapters:
            if not IExhibitView.providedBy(adapter):
                continue
            yield name, getattr(adapter, 'label', name)

    def __call__(self, context=None):
        """ See IVocabularyFactory interface
        """
        # TODO plone4 FIXME this code fails with the message:
        # TypeError: argument 2 to map() must support iteration
        #views = [(name, label) for name, label in self._adapters(context)]
        views = [(u'daviz.map', 'Map View'), (u'daviz.timeline',
                 'Timeline View'), (u'daviz.tile', 'Tile View'),
                             (u'daviz.tabular', 'Tabular View')]
        views.sort(key=operator.itemgetter(1))

        return SimpleVocabulary([
            SimpleTerm(name2, name2, label2) for name2, label2 in views])

ViewsVocabularyFactory = ViewsVocabulary()
