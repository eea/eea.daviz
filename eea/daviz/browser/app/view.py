# -*- coding: utf-8 -*-
""" Module that contains default view
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

try:
    import json as simplejson
    simplejson = simplejson
except ImportError:
    import simplejson
from zope.component import queryAdapter, queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig

class View(BrowserView):
    """ Default view
    """
    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.accessor = queryAdapter(self.context, IDavizConfig)

    def json(self):
        """ Returns json dump of result
        """
        res = self.accessor.json
        return simplejson.dumps(dict(res))

    @property
    def facets(self):
        """ Returns facets
        """
        facets = self.accessor.facets
        for facet in facets:
            if not facet.get('show', False):
                continue
            yield facet.get('name')

    @property
    def views(self):
        """ Returns views
        """
        views = self.accessor.views
        for view in views:
            yield view.get('name')

    @property
    def sources(self):
        """ External sources
        """
        sources = self.accessor.sources
        for source in sources:
            yield source

    @property
    def gmapkey(self):
        """ Get Google Maps key from
            portal_properties.geographical_properties.google_key
        """
        ptool = getToolByName(self.context, 'portal_properties')
        props = getattr(ptool, 'geographical_properties', '')
        return getattr(props, 'google_key', '')

    def get_facet(self, name):
        """ Get faceted by name
        """
        facet = self.accessor.facet(key=name)
        facet_type = facet.get('type')
        if not isinstance(facet_type, unicode):
            facet_type = facet_type.decode('utf-8')
        view = queryMultiAdapter((self.context, self.request), name=facet_type)
        view.data = facet
        return view

    def get_view(self, name):
        """ Get view by name
        """
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        view = queryMultiAdapter((self.context, self.request), name=name)
        return view
