# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.component import queryUtility
from zope.component import queryAdapter, queryMultiAdapter
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
    def facets_vocabulary(self):
        """ Return facets
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        for facet in accessor.facets:
            yield facet

    @property
    def enabled_views(self):
        """ Return saved views
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        return [view.get('name') for view in accessor.views]

    def get_view(self, name):
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        return queryMultiAdapter((self.context, self.request), name=name)

    def get_edit(self, name):
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        name += u'.edit'
        return queryMultiAdapter((self.context, self.request), name=name)

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

    def handle_facets(self, **kwargs):
        columns = kwargs.get('daviz.facets.columns', [])
        labels = kwargs.get('daviz.facets.labels', [])

        mutator = queryAdapter(self.context, IDavizConfig)
        for index, facet in enumerate(mutator.facets):
            name = facet.get('name')
            properties = {
                'label': len(labels) > index and labels[index] or name,
                'show': name in columns
            }
            mutator.edit_facet(name, **properties)

        if kwargs.get('daviz.facets.save') == 'ajax':
            return self._redirect('Exhibit facets settings saved', to=None)
        return self._redirect('Exhibit facets settings saved')

    def handle_views(self, **kwargs):
        views = kwargs.get('daviz.views', [])

        mutator = queryAdapter(self.context, IDavizConfig)
        existing = [view.get('name') for view in mutator.views]

        for view in existing:
            if view not in views:
                mutator.delete_view(view)

        for view in views:
            if view not in existing:
                mutator.add_view(view)

        if kwargs.get('daviz.views.save') == 'ajax':
            return self._redirect('Exhibit views settings saved', to=None)
        return self._redirect('Exhibit views settings saved')

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        if kwargs.get('daviz.views.save', None):
            return self.handle_views(**kwargs)
        elif kwargs.get('daviz.facets.save', None):
            return self.handle_facets(**kwargs)
        return self._redirect('Invalid action provided')
