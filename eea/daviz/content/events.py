""" Events
"""
from StringIO import StringIO
from eea.app.visualization.cache import InvalidateCacheEvent
from eea.app.visualization.events import VisualizationEnabledEvent
from eea.app.visualization.interfaces import IExternalData
from eea.app.visualization.interfaces import ITable2JsonConverter
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationJsonUtils
from zope.component import queryMultiAdapter, queryAdapter, queryUtility
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent
from zope.event import notify
from zope.interface import Attribute
from zope.interface import implements
import json
import logging

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

    utils = queryUtility(IVisualizationJsonUtils)

    for item in relatedItems:
        daviz_json = queryMultiAdapter((item, request), name=u'daviz.json')
        if not daviz_json:
            continue

        try:
            daviz_json = json.loads(daviz_json())
        except Exception, err:
            logger.exception(err)
            continue

        utils.merge(new_json['properties'], daviz_json.get('properties', {}))

    mutator.json = new_json
    properties = new_json.get('properties', {})
    columns = []
    def_order = 0
    for key, val in properties.items():
        if isinstance(val, dict):
            typo = val.get('valueType', 'text')
            order = val.get('order', def_order)
        else:
            typo = 'text'
            order = def_order
        def_order += 1
        columns.append((order, key, typo))
    columns.sort()
    final_columns = []
    for val in columns:
        final_columns.append((val[1], val[2]))
    notify(VisualizationEnabledEvent(obj, columns=final_columns, cleanup=False))
    notify(InvalidateCacheEvent(raw=True, dependencies=['eea.daviz']))

def onSpreadSheetChanged(obj, evt):
    """ Handle spreadsheet
    """
    if not evt.spreadsheet:
        return

    request = getattr(obj, 'REQUEST', None)
    if not request:
        return

    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        return

    new_json = {'items': [], 'properties': {}}
    new_json['properties'].update(mutator.json.get('properties', {}))

    datafile = StringIO(evt.spreadsheet)
    converter = queryUtility(ITable2JsonConverter)
    try:
        columns, data = converter(datafile)
    except Exception, err:
        logger.exception(err)
        return

    new_json['items'] = data.get('items', [])

    utils = queryUtility(IVisualizationJsonUtils)
    utils.merge(new_json['properties'], data.get('properties', {}))
    mutator.json = new_json

    notify(VisualizationEnabledEvent(obj, columns=columns, cleanup=False))
    notify(InvalidateCacheEvent(raw=True, dependencies=['eea.daviz']))

def onExternalChanged(obj, evt):
    """ Handle external URL
    """
    if not evt.external:
        return

    request = getattr(obj, 'REQUEST', None)
    if not request:
        return

    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        return

    new_json = {'items': [], 'properties': {}}
    new_json['properties'].update(mutator.json.get('properties', {}))

    data = queryUtility(IExternalData)
    if not data:
        return

    datafile = StringIO(data(evt.external))
    converter = queryUtility(ITable2JsonConverter)
    try:
        columns, data = converter(datafile)
    except Exception, err:
        logger.exception(err)
        return

    new_json['items'] = data.get('items', [])

    utils = queryUtility(IVisualizationJsonUtils)
    utils.merge(new_json['properties'], data.get('properties', {}))
    mutator.json = new_json

    notify(VisualizationEnabledEvent(obj, columns=columns, cleanup=False))
    notify(InvalidateCacheEvent(raw=True, dependencies=['eea.daviz']))


class IDavizWillBeRemovedEvent(IObjectEvent):
    """A daviz will be removed."""
    oldParent = Attribute("The old location parent for the object.")
    oldName = Attribute("The old location name for the object.")


class DavizWillBeRemovedEvent(ObjectEvent):
    """A daviz will be removed from a container.
    """
    implements(IDavizWillBeRemovedEvent)

    def __init__(self, obj, oldParent=None, oldName=None):
        ObjectEvent.__init__(self, obj)
        self.oldParent = oldParent
        self.oldName = oldName
