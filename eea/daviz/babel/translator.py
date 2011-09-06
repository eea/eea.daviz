""" Babel translator
"""
import logging
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from eea.daviz.babel.interfaces import IBabelReader, IBabelWriter

logger = logging.getLogger('eea.daviz.babel')

class Translator(BrowserView):
    """ Translate
    """
    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        url = kwargs.get('url', '')
        if not url:
            logger.exception('Invalid URL: %s', url)
            return ""

        reader = kwargs.get('reader', '')
        reader = queryUtility(IBabelReader, name=reader)
        if not reader:
            logger.exception('Unknown babel reader: %s', reader)
            return ""

        write = kwargs.get('writer', '')
        writer = queryUtility(IBabelWriter, name=write)
        if not writer:
            logger.exception('Unknown babel writer: %s', writer)
            return ""

        try:
            items = reader(url)
        except Exception, err:
            logger.exception(err)
            return ""

        try:
            output = writer(items)
        except Exception, err:
            logger.exception(err)
            return ""

        callback = kwargs.get('callback', '')
        if not callback or callback == '?':
            return output

        if self.request and 'jsonp' in write:
            self.request.response.setHeader('Content-Type', 'application/jsonp')
        return "%s(%s)" % (callback, output)
