""" Browser
"""
from zope import event
from Products.Five.browser import BrowserView
from eea.daviz.cache import InvalidateCacheEvent

class InvalidateCache(BrowserView):
    """ Utils view to invalidate eea.daviz cache
    """
    def __call__(self, **kwargs):
        event.notify(InvalidateCacheEvent(
            raw=True, dependencies=['eea.daviz']
        ))
