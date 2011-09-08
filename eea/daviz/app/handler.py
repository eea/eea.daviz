# -*- coding: utf-8 -*-
""" Handler module containing configure logic
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from eea.daviz.app.interfaces import IDavizConfig
from zope.annotation.interfaces import IAnnotations

from persistent.dict import PersistentDict
from persistent.list import PersistentList
from eea.daviz.config import ANNO_VIEWS, ANNO_FACETS, ANNO_JSON, ANNO_SOURCES

class Configure(object):
    """ Get daviz configuration
    """
    implements(IDavizConfig)

    def __init__(self, context):
        self.context = context

    def _views(self):
        """ Returns views from ANNO_VIEWS config
        """
        anno = IAnnotations(self.context)
        views = anno.get(ANNO_VIEWS, None)
        if views is None:
            views = anno[ANNO_VIEWS] = PersistentList()
        return views

    def _facets(self):
        """ Returns facets from ANNO_FACETS config
        """
        anno = IAnnotations(self.context)
        facets = anno.get(ANNO_FACETS, None)
        if facets is None:
            facets = anno[ANNO_FACETS] = PersistentList()
        return facets

    def _sources(self):
        """ External sources
        """
        anno = IAnnotations(self.context)
        sources = anno.get(ANNO_SOURCES, None)
        if sources is None:
            sources = anno[ANNO_SOURCES] = PersistentList()
        return sources

    def _json(self):
        """ Returns json from ANNO_JSON config
        """
        anno = IAnnotations(self.context)
        json = anno.get(ANNO_JSON, None)
        if json is None:
            json = anno[ANNO_JSON] = PersistentDict()
        return json
    #
    # Accessors
    #
    @property
    def views(self):
        """ Return daviz enabled views
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_VIEWS, [])

    @property
    def facets(self):
        """ Return daviz enabled facets
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_FACETS, [])

    @property
    def sources(self):
        """ Return daviz external sources
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_SOURCES, [])

    def set_json(self, value):
        """ Set json dict
        """
        anno = IAnnotations(self.context)
        anno[ANNO_JSON] = PersistentDict(value)

    def get_json(self):
        """ Return json from annotations
        """
        anno = IAnnotations(self.context)
        json = anno.get(ANNO_JSON, {})
        return json
    json = property(get_json, set_json)

    def view(self, key, default=None):
        """ Return view by given key
        """
        for view in self.views:
            if view.get('name', None) != key:
                continue
            return view
        return default

    def facet(self, key, default=None):
        """ Return facet by given key
        """
        for facet in self.facets:
            if facet.get('name') != key:
                continue
            return facet
        return default

    def source(self, key, default=None):
        """ Return source by given key
        """
        for source in self.sources:
            if source.get('name') != key:
                continue
            return source
        return default
    #
    # View mutators
    #
    def add_view(self, name, **kwargs):
        """ Add view
        """
        config = self._views()
        kwargs.update({'name': name})
        view = PersistentDict(kwargs)
        config.append(view)
        return view.get('name', '')

    def delete_view(self, key):
        """ Delete view by given key
        """
        config = self._views()
        for index, view in enumerate(config):
            if view.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def edit_view(self, key, **kwargs):
        """ Edit view properties
        """
        view = self.view(key)
        if not view:
            raise KeyError, key
        view.update(kwargs)

    def delete_views(self):
        """ Reset views
        """
        anno = IAnnotations(self.context)
        anno[ANNO_VIEWS] = PersistentList()
    #
    # Facet mutators
    #
    def add_facet(self, name, **kwargs):
        """ Add facet
        """
        config = self._facets()
        kwargs.update({'name': name})
        kwargs.setdefault('type', u'daviz.list.facet')
        facet = PersistentDict(kwargs)
        config.append(facet)
        return facet.get('name', '')

    def delete_facet(self, key):
        """ Delete facet by given key
        """
        config = self._facets()
        for index, facet in enumerate(config):
            if facet.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def edit_facet(self, key, **kwargs):
        """ Edit facet properties
        """
        facet = self.facet(key)
        if not facet:
            raise KeyError, key
        facet.update(kwargs)

    def delete_facets(self):
        """ Remove all facets
        """
        anno = IAnnotations(self.context)
        anno[ANNO_FACETS] = PersistentList()
    #
    # Source mutators
    #
    def add_source(self, name, **kwargs):
        """ Add source
        """
        config = self._sources()
        kwargs.update({'name': name})
        kwargs.setdefault('type', u'json')
        source = PersistentDict(kwargs)
        config.append(source)
        return source.get('name', '')

    def delete_source(self, key):
        """ Delete source by given key
        """
        config = self._sources()
        for index, source in enumerate(config):
            if source.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def edit_source(self, key, **kwargs):
        """ Edit source properties
        """
        source = self.source(key)
        if not source:
            raise KeyError, key
        source.update(kwargs)

    def delete_sources(self):
        """ Remove all sources
        """
        anno = IAnnotations(self.context)
        anno[ANNO_SOURCES] = PersistentList()
