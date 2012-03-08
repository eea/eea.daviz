""" Daviz config module
"""
#BBB
from eea.app.visualization import config
ANNO_VIEWS = config.ANNO_VIEWS
ANNO_FACETS = config.ANNO_FACETS
ANNO_JSON = config.ANNO_JSON
ANNO_SOURCES = config.ANNO_SOURCES

PACKAGE = 'eea.daviz'
ADD_PERMISSION = "eea.daviz: Add presentation"

from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')
