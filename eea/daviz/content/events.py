""" Events
"""
from StringIO import StringIO
from zope.event import notify
import logging
import json
from eea.app.visualization.events import VisualizationEnabledEvent
from eea.app.visualization.cache import InvalidateCacheEvent
from zope.component import queryMultiAdapter, queryAdapter, queryUtility
from eea.app.visualization.converter.interfaces import IExhibitJsonConverter
from eea.app.visualization.interfaces import IVisualizationConfig
logger = logging.getLogger('eea.daviz.events')

def onRelationsChanged(obj, evt):
    """ Handle relations changed event
    """
    relatedItems = evt.relatedItems
    request = getattr(obj, 'REQUEST', None)
    if not request:
        return

    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        return

    new_json = {'items': [], 'properties': {}}
    new_json['items'].extend(mutator.json.get('items', []))
    new_json['properties'].update(mutator.json.get('properties', {}))

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

    notify(VisualizationEnabledEvent(obj, columns=columns, cleanup=False))
    notify(InvalidateCacheEvent(raw=True, dependencies=['eea.daviz']))

def onSpreadSheetChanged(obj, evt):
    """ Handle spreadsheet
    """
    request = getattr(obj, 'REQUEST', None)
    if not request:
        return

    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        return

    new_json = {'items': [], 'properties': {}}
    new_json['properties'].update(mutator.json.get('properties', {}))

    datafile = StringIO(evt.spreadsheet)
    converter = queryUtility(IExhibitJsonConverter)
    try:
        columns, data = converter(datafile)
    except Exception, err:
        logger.exception(err)
        return

    new_json['items'] = data.get('items', [])
    new_json['properties'].update(data.get('properties', {}))
    mutator.json = new_json

    notify(VisualizationEnabledEvent(obj, columns=columns, cleanup=False))
    notify(InvalidateCacheEvent(raw=True, dependencies=['eea.daviz']))
