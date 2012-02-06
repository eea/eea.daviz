""" Events
"""
from zope.event import notify
import logging
import json
from eea.daviz.events import DavizEnabledEvent
from eea.daviz.cache import InvalidateCacheEvent
from zope.component import queryMultiAdapter, queryAdapter
from eea.daviz.interfaces import IDavizConfig
logger = logging.getLogger('eea.daviz.events')

def onRelationsChanged(obj, evt):
    """ Handle relations changed event
    """
    relatedItems = evt.relatedItems
    request = getattr(obj, 'REQUEST', None)
    if not request:
        return

    mutator = queryAdapter(obj, IDavizConfig)
    if not mutator:
        return

    new_json = {'items': [], 'properties': {}}
    for item in relatedItems:
        daviz_json = queryMultiAdapter((item, request), name=u'daviz-view.json')
        if not daviz_json:
            continue

        try:
            daviz_json = json.loads(daviz_json())
        except Exception, err:
            logger.exception(err)
            continue

        new_json['properties'].update(daviz_json.get('properties', {}))

    mutator.json = new_json
    properties = new_json.get('properties', {})
    columns = []
    for key, val in properties.items():
        if isinstance(val, dict):
            typo = val.get('valueType', 'text')
        else:
            typo = 'text'
        columns.append((key, typo))

    notify(DavizEnabledEvent(obj, columns=columns, cleanup=False))
    notify(InvalidateCacheEvent(raw=True, dependencies=['eea.daviz']))
