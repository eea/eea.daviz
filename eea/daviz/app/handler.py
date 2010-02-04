from zope.interface import implements
from interfaces import IDavizConfig
try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.interfaces import IAnnotations

from persistent.dict import PersistentDict
from persistent.list import PersistentList

ANNO = 'eea.daviz.config'

class Configure(object):
    """ Get daviz configuration
    """
    implements(IDavizConfig)

    def __init__(self, context):
        self.context = context

    def _config(self):
        anno = IAnnotations(self.context)
        config = anno.get(ANNO, None)
        if not config:
            config = anno[ANNO] = PersistentDict({
                'views': PersistentList(),
                'facets': PersistentList()
            })
        return config
    #
    # Accessors
    #
    @property
    def views(self):
        """ Return daviz enabled views
        """
        anno = IAnnotations(self.context)
        config = anno.get(ANNO, {})
        return config.get('views', [])

    @property
    def facets(self):
        """ Return daviz enabled facets
        """
        anno = IAnnotations(self.context)
        config = anno.get(ANNO, {})
        return config.get('facets', [])

    def view(self, key, default=None):
        """ Return view by given key
        """
        for view in self.views:
            if view.get('name', None) == key:
                return view
            return default

    def facet(self, key, default=None):
        """ Return facet by given key
        """
        for facet in self.facets:
            if facet.get('name', None) == key:
                return facet
            return default
    #
    # Mutators
    #
    def add_view(self, name, **kwargs):
        """ Add view
        """
        config = self._config()
        view = PersistentDict({
            'name': name
        })
        config['views'].append(view)
        config._p_changed = 1
        return view.get('name', '')

    def delete_view(self, key):
        """ Delete view by given key
        """
        config = self._config()
        for index, view in enumerate(config['views']):
            if view.get('name', '') == key:
                config['views'].pop(index)
                config._p_changed = 1
                return
        raise KeyError, key

    def add_facet(self, name, **kwargs):
        """ Add facet
        """
        config = self._config()
        facet = PersistentDict({
            'name': name
        })
        config['facets'].append(facet)

        config._p_changed = 1
        return facet.get('name', '')

    def delete_facet(self, key):
        """ Delete facet by given key
        """
        config = self._config()
        for index, facet in enumerate(config['facets']):
            if facet.get('name', '') == key:
                config['facets'].pop(index)
                config._p_changed = 1
                return
        raise KeyError, key
