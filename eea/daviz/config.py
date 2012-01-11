# -*- coding: utf-8 -*-
""" Daviz config module
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

ANNO_VIEWS = 'eea.daviz.config.views'
ANNO_FACETS = 'eea.daviz.config.facets'
ANNO_JSON = 'eea.daviz.config.json'
ANNO_SOURCES = 'eea.daviz.config.sources'

PACKAGE = 'eea.daviz'
ADD_PERMISSION = "eea.daviz: Add presentation"

from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')
