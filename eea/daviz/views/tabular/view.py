from zope.interface import implements
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig
from interfaces import IExhibitTabularView

class View(BrowserView):
    """ Tabular view
    """
    implements(IExhibitTabularView)

    @property
    def columns(self):
        adapter = queryAdapter(self.context, IDavizConfig)
        json = adapter.json
        if(len(json)):
            res = json[0].keys()
        else:
            res = []
        res = ['.%s' % item for item in res]
        return ', '.join(res)
