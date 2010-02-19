# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.component import queryUtility
from zope.component import queryAdapter
from Products.statusmessages.interfaces import IStatusMessage
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig

class Edit(BrowserView):
    """ Edit page
    """
    @property
    def views_vocabulary(self):
        """ Views vocabulary
        """
        voc = queryUtility(IVocabularyFactory,
                           name=u'eea.daviz.vocabularies.ViewsVocabulary')
        return voc(self.context)

    @property
    def enabled_views(self):
        """ Return saved views
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        return [view.get('name') for view in accessor.views]

class Configure(BrowserView):
    """ Edit controller
    """
    def _redirect(self, msg='', to='daviz-edit.html'):
        """ Return or redirect
        """
        if not to:
            return msg

        if not self.request:
            return msg

        if msg:
            IStatusMessage(self.request).addStatusMessage(str(msg), type='info')
        self.request.response.redirect(to)
        return msg

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        views = kwargs.get('views', [])

        mutator = queryAdapter(self.context, IDavizConfig)

        mutator.delete_views()
        for view in views:
            mutator.add_view(view)

        return self._redirect('Changes saved')
