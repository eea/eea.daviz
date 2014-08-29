""" Custom converters to JSON
"""
import logging
import json as simplejson
from zope.component import queryMultiAdapter, queryAdapter
from eea.app.visualization.interfaces import IMultiDataProvenance
from eea.app.visualization.data.browser import JSON
from eea.app.visualization.cache import ramcache, cacheJsonKey
logger = logging.getLogger('eea.daviz')

class DavizJSON(JSON):
    """ Merged JSON from related items
    """
    @ramcache(cacheJsonKey, dependencies=['eea.daviz'])
    def json(self, **kwargs):
        """ JSON
        """
        my_json = super(DavizJSON, self).json(
            column_types=kwargs.get('column_types'),
            annotations=kwargs.get('annotations')
        )
        my_json = simplejson.loads(my_json)

        column_types = kwargs.get('column_types',
                                  None) or self.column_types(my_json)
        annotations = kwargs.get('annotations',
                                 None) or self.annotations(my_json)

        relatedItems = getattr(self.context, 'getRelatedItems', ())
        if relatedItems:
            relatedItems = relatedItems()

        new_json = {'items': [], 'properties': {}}
        for item in relatedItems:
            #fix for #20869 if related item has provenance info with a link
            #to this visualization, skip it
            provenances = queryAdapter(item, IMultiDataProvenance).provenances
            is_provenance_info = False
            for provenance in provenances:
                if provenance['link'] == self.context.absolute_url():
                    is_provenance_info = True
            if is_provenance_info:
                continue
            #end of fix for #20869
            daviz_json = queryMultiAdapter(
                (item, self.request), name=u'daviz.json')

            if not daviz_json:
                continue

            try:
                daviz_json = simplejson.loads(daviz_json(
                    column_types=column_types, annotations=annotations))
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
