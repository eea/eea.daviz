""" Upgrade scripts to version 4.3
"""

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from eea.daviz.interfaces import IDavizSettings


def update_registry(context):
    """update the registry
    """
    registry = getUtility(IRegistry)
    registry.registerInterface(IDavizSettings)
