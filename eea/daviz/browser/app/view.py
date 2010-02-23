# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

import simplejson
from zope.component import queryAdapter, queryMultiAdapter
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig

class View(BrowserView):
    """ Default view
    """
    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.accessor = queryAdapter(self.context, IDavizConfig)

    def json(self):
        res = self.accessor.json
        return simplejson.dumps(dict(res))

    @property
    def facets(self):
        facets = self.accessor.facets
        for facet in facets:
            if not facet.get('show', False):
                continue
            yield facet.get('name')

    @property
    def views(self):
        views = self.accessor.views
        for view in views:
            yield view.get('name')

    def get_facet(self, name):
        facet = self.accessor.facet(key=name)
        facet_type = facet.get('type')
        if not isinstance(facet_type, unicode):
            facet_type = facet_type.decode('utf-8')
        view = queryMultiAdapter((self.context, self.request), name=facet_type)
        view.data = facet
        return view

    def get_view(self, name):
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        view = queryMultiAdapter((self.context, self.request), name=name)
        return view
