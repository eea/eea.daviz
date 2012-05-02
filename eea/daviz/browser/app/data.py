""" Data controllers
"""
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView

class Info(BrowserView):
    """ Data source info
    """
    def __init__(self, context, request):
        super(Info, self).__init__(context, request)
        self._info = {}

    @property
    def info(self):
        if not self._info:
            self._info = info = {
                'data': {
                    'title': '',
                    'url': '',
                    },
                'owner': {
                    'title': '',
                    'url': ''
                }
            }
        return self._info

    def fallback(self):
        """ Try to get data info from relatedItems
        """
        relatedItems = self.context.getRelatedItems()
        for item in relatedItems:
            info = queryMultiAdapter((self.context, self.request),
                                     name=u'data.info')
            if not info:
                continue

            self.info.update(info())
            break
        return self.info

    def __call__(self, **kwargs):
        field = self.context.getField('dataTitle')
        if field:
            self.info['data']['title'] = field.getAccessor(self.context)()


        field = self.context.getField('dataLink')
        if field:
            self.info['data']['url'] = field.getAccessor(self.context)()

        field = self.context.getField('dataOwner')
        if field:
            vocab = field.Vocabulary(self.context)
            url = field.getAccessor(self.context)()
            title = self.context.displayValue(vocab, url)
            self.info['owner']['title'] = title
            self.info['owner']['url'] = url

        if self.info['data']['title'] or self.info['data']['url']:
            return self.info
        return self.fallback()
