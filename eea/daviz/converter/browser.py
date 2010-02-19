# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

import logging
from StringIO import StringIO
from zope.event import notify
from zope.interface import alsoProvides
from zope.component import queryAdapter
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from interfaces import IExhibitJsonConverter
from eea.daviz.interfaces import IExhibitJson
from eea.daviz.interfaces import IDavizConfig
from eea.daviz.events import DavizEnabledEvent

logger = logging.getLogger('eea.daviz.converter')

class DavizSupport(BrowserView):
    """ Enable/Disable Exhibit
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
                                   'a valid CSV file'), 'view')

        if not IExhibitJson.providedBy(self.context):
            alsoProvides(self.context, IExhibitJson)

        # Update annotations
        mutator = queryAdapter(self.context, IDavizConfig)
        mutator.json = json
        notify(DavizEnabledEvent(self.context, columns=columns))
        return self._redirect('Converted to Exhibit view')

    def disable(self):
        """ Disable Exhibit
        """
        raise NotImplementedError
