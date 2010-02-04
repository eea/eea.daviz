import simplejson
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IExhibitJsonConverter

class View(BrowserView):
    """ Default view
    """
    def json(self):
        adapter = queryAdapter(self.context, IExhibitJsonConverter)
        if not adapter:
            return simplejson.dumps({})
        return adapter.getJsonData()
