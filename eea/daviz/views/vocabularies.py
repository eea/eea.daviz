# -*- coding: utf-8 -*-

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
        adapters = getAdapters((context, context.request), Interface)
        for name, adapter in adapters:
            if not IExhibitView.providedBy(adapter):
                continue
            yield name, getattr(adapter, 'label', name)

    def __call__(self, context=None):
        """ See IVocabularyFactory interface
        """
        views = [(name, label) for name, label in self._adapters(context)]
        views.sort(key=operator.itemgetter(1))

        return SimpleVocabulary([
            SimpleTerm(name2, name2, label2) for name2, label2 in views])

ViewsVocabularyFactory = ViewsVocabulary()
