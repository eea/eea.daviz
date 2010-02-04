import simplejson
from zope.component import queryAdapter, queryMultiAdapter
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig

class View(BrowserView):
    """ Default view
    """
    def json(self):
        adapter = queryAdapter(self.context, IDavizConfig)
        res = {'items': adapter.json}
        return simplejson.dumps(res)

    @property
    def facets(self):
        adapter = queryAdapter(self.context, IDavizConfig)
        json = adapter.json
        if(len(json)):
            return json[0].keys()
        return []

    @property
    def views(self):
        return ['daviz.tabular.view']

    def get_facet(self, name):
        view = queryMultiAdapter((self.context, self.request),
                                 name=u'daviz.list.facet')
        view.data = {'name': name}
        return view

    def get_view(self, name):
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        view = queryMultiAdapter((self.context, self.request), name=name)
        return view
