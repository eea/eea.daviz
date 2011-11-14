""" Module for Edit logic of browser/app package
"""
import logging
from zope import event
from zope.component import queryUtility
from zope.component import queryAdapter, queryMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage
from zope.schema.interfaces import IVocabularyFactory
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig
from eea.daviz.events import DavizFacetDeletedEvent
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
        """ Return given view
        """
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        return queryMultiAdapter((self.context, self.request), name=name)

    def get_edit(self, name):
        """ Return edit page
        """
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        name += u'.edit'
        return queryMultiAdapter((self.context, self.request), name=name)

    def get_facet_form(self, facet):
        """ Edit form for facet
        """
        ftype = facet.get('type', '')
        if not isinstance(ftype, unicode):
            ftype = ftype.decode('utf-8')
        ftype += u'.edit'

        form = queryMultiAdapter((self.context, self.request), name=ftype)
        if form:
            name = facet.get('name', '')
            form.prefix = name

        return form

    def get_facet_add(self, facetname):
        """ Add form for facet
        """
        form = queryMultiAdapter((self.context, self.request), name=facetname)
        if form:
            form.prefix = facetname.replace('.', '-')
        return form

class Configure(BrowserView):
    """ Edit controller
    """
    def _redirect(self, msg='', ajax=False, to='daviz-edit.html'):
        """ Return or redirect
        """
        if ajax:
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
        ajax = (kwargs.get('daviz.facets.save') == 'ajax')

        if not order:
            return self._redirect(
                'Exhibit facets settings not saved: Nothing to do', ajax)

        if not isinstance(order, list):
            return self._redirect(
                'Exhibit facets settings not saved: Nothing to do', ajax)

        if len(order) == 1:
            return self._redirect(
                'Exhibit facets settings not saved: Nothing to do', ajax)

        facets = mutator.facets
        facets = dict((facet.get('name'), dict(facet)) for facet in facets)
        mutator.delete_facets()

        for name in order:
            properties = facets.get(name, {})
            if not properties:
                logger.exception('Unknown facet id: %s', name)
                continue
            mutator.add_facet(**properties)

        return self._redirect('Exhibit facets settings saved', ajax)

    def handle_facetDelete(self, **kwargs):
        """ Delete facet
        """
        mutator = queryAdapter(self.context, IDavizConfig)
        name = kwargs.get('name', '')
        ajax = (kwargs.get('daviz.facet.delete') == 'ajax')
        try:
            mutator.delete_facet(name)
        except KeyError, err:
            logger.exception(err)
            return self._redirect(err, ajax)
        else:
            event.notify(DavizFacetDeletedEvent(self.context, facet=name))

        return self._redirect('Exhibit facet deleted', ajax)

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        if kwargs.get('daviz.facets.save', None):
            return self.handle_facets(**kwargs)
        elif kwargs.get('daviz.facet.delete', None):
            return self.handle_facetDelete(**kwargs)

        return self._redirect('Invalid action provided')
