""" Custom converters to JSON
"""
import logging
import json as simplejson
from zope.component import queryMultiAdapter
from eea.app.visualization.data.browser import JSON
from eea.app.visualization.cache import ramcache, cacheJsonKey
logger = logging.getLogger('eea.daviz')

class DavizJSON(JSON):
    """ Merged JSON from related items
    """
    @ramcache(cacheJsonKey, dependencies=['eea.daviz'])
    def json(self, column_types=None):
        """ JSON
        """
        my_json = super(DavizJSON, self).json(column_types)
        my_json = simplejson.loads(my_json)

        relatedItems = getattr(self.context, 'getRelatedItems', ())
        if relatedItems:
            relatedItems = relatedItems()

        new_json = {'items': [], 'properties': {}}
        for item in relatedItems:
            daviz_json = queryMultiAdapter(
                (item, self.request), name=u'daviz.json')

            if not daviz_json:
                continue

            try:
                column_types = dict(
                    (key, value.get('columnType',
                                    value.get('valueType', 'text'))
                     if isinstance(value, dict) else value)
                    for key, value in my_json.get('properties', {}).items()
                )
                daviz_json = simplejson.loads(
                    daviz_json(column_types=column_types))
            except Exception, err:
                logger.exception(err)
                continue

            new_json['items'].extend(daviz_json.get('items', []))
            self.merge(
                new_json['properties'],
                daviz_json.get('properties', {})
            )

        # Also add my own JSON
        new_json['items'].extend(my_json.get('items', []))
        self.merge(
            new_json['properties'],
            my_json.get('properties', {})
        )
        return self.sortProperties(simplejson.dumps(new_json))
