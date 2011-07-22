# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

import logging
from zope.component import queryUtility
from zope.component import queryAdapter, queryMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig
logger = logging.getLogger('eea.daviz')

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

    def get_facet_form(self, facet):
        ftype = facet.get('type', '')
        if not isinstance(ftype, unicode):
            ftype = ftype.decode('utf-8')
        ftype += u'.edit'

        form = queryMultiAdapter((self.context, self.request), name=ftype)
        if form:
            name = facet.get('name', '')
            form.prefix = name

        return form

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
        """ Update facets position
        """
        mutator = queryAdapter(self.context, IDavizConfig)
        order = kwargs.get('order', [])
        if not order:
            return self._redirect(
                'Exhibit facets settings not saved: Nothing to do', to=None)

        if not isinstance(order, list):
            return self._redirect(
                'Exhibit facets settings not saved: Nothing to do', to=None)

        if len(order) == 1:
            return self._redirect(
                'Exhibit facets settings not saved: Nothing to do', to=None)

        facets = mutator.facets
        facets = dict((facet.get('name'), dict(facet)) for facet in facets)
        mutator.delete_facets()

        for name in order:
            properties = facets.get(name, {})
            if not properties:
                logger.exception('Unknown facet id: %s', name)
                continue
            mutator.add_facet(**properties)

        if kwargs.get('daviz.facets.save') == 'ajax':
            return self._redirect('Exhibit facets settings saved', to=None)
        return self._redirect('Exhibit facets settings saved')


    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        if kwargs.get('daviz.facets.save', None):
            return self.handle_facets(**kwargs)

        return self._redirect('Invalid action provided')
