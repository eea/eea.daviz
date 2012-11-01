""" Browser
"""
from zope import event
from zope.lifecycleevent import ObjectModifiedEvent
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

class CacheView(BrowserView):
    """ Caching for sparql query results
    """
    def __call__(self):
        if not "submit" in self.request.form:
            return self.index()

        event.notify(ObjectModifiedEvent(self.context))
        IStatusMessage(self.request).addStatusMessage("Cache invalidated")
        return self.index()
