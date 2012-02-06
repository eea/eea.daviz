""" Module to enable or disable Exhibit support
"""
import logging
import json as simplejson
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO

from zope.component import queryAdapter, queryUtility
from zope.event import notify
from zope.interface import alsoProvides, noLongerProvides, implements
from zope.publisher.interfaces import NotFound

from eea.daviz.converter.interfaces import IExhibitJsonConverter
from eea.daviz.events import DavizEnabledEvent
from eea.daviz.interfaces import IDavizConfig, IExhibitJson
from eea.daviz.subtypes.interfaces import IDavizSubtyper
from eea.daviz.browser.app.view import JSONView
from eea.daviz.cache import ramcache, cacheJsonKey

logger = logging.getLogger('eea.daviz.converter')

class DavizPublicSupport(BrowserView):
    """ Public support for subtyping objects
        view for non IPossibleExhibitJson objects
    """
    implements(IDavizSubtyper)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg = '', to = ''):
        """ Redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(
                    str(msg), type='info')
            if to:
                self.request.response.redirect(self.context.absolute_url() + to)
            else:
                self.request.response.redirect(self.context.absolute_url()
                                                                + "/view")
        return msg

    @property
    def can_enable(self):
        """ See IDavizSubtyper
        """
        return False

    @property
    def can_disable(self):
        """ See IDavizSubtyper
        """
        return False

    @property
    def is_exhibit(self):
        """ Is exhibit?
        """
        return False


    def enable(self):
        """ See IDavizSubtyper
        """
        raise NotFound(self.context, 'enable', self.request)

    def disable(self):
        """ See IDavizSubtyper
        """
        raise NotFound(self.context, 'disable', self.request)


class DavizSupport(DavizPublicSupport):
    """ Enable/Disable Exhibit
    """

    def _redirect(self, msg='', to='/daviz-edit.html'):
        """ Return or redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(
                    str(msg), type='info')
            if to:
                self.request.response.redirect(self.context.absolute_url() + to)
            else:
                self.request.response.redirect(self.context.absolute_url()
                                                                + "/view")
        return msg

    @property
    def can_enable(self):
        """ See IDavizSubtyper
        """
        return not self.is_exhibit

    @property
    def can_disable(self):
        """ See IDavizSubtyper
        """
        return self.is_exhibit

    @property
    def is_exhibit(self):
        """ Is exhibit viewable?
        """
        return IExhibitJson.providedBy(self.context)

    def enable(self):
        """ Enable Exhibit
        """
        datafile = StringIO(self.context.getFile().data)
        converter = queryUtility(IExhibitJsonConverter)
        try:
            columns, json = converter(datafile)
        except Exception, err:
            logger.exception(err)
            return self._redirect(('An error occured while trying to convert '
                                   'attached file. Please ensure you provided '
                                   'a valid CSV file'), '/view')

        if not IExhibitJson.providedBy(self.context):
            alsoProvides(self.context, IExhibitJson)

        # Update annotations
        mutator = queryAdapter(self.context, IDavizConfig)
        mutator.json = json
        notify(DavizEnabledEvent(self.context, columns=columns))
        return self._redirect('Enabled Exhibit view')

    def disable(self):
        """ Disable Exhibit
        """
        noLongerProvides(self.context, IExhibitJson)
        return self._redirect('Removed Exhibit view', to='')


class TSVFileJSONView(JSONView):
    """ daviz-view.json for Tab separated files which is not daviz enabled
    """
    @ramcache(cacheJsonKey, dependencies=['eea.daviz'])
    def json(self):
        """ Convert file to JSON
        """
        datafile = StringIO(self.context.getFile().data)
        converter = queryUtility(IExhibitJsonConverter)
        try:
            _cols, json = converter(datafile)
        except Exception, err:
            logger.debug(err)
            return super(TSVFileJSONView, self).json()
        return simplejson.dumps(json)
