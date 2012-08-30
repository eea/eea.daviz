from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from eea.daviz.interfaces import IDavizSettings


def update_registry(context):
    registry = getUtility(IRegistry)
    registry.registerInterface(IDavizSettings)
