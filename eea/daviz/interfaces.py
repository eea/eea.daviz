# -*- coding: utf-8 -*-
""" Daviz interfaces module
"""

from zope import schema
from zope.interface import Interface

# BBB Subtypes
from eea.app.visualization.interfaces import \
     IPossibleVisualization as IPossibleExhibitJson
from eea.app.visualization.interfaces import \
     IVisualizationEnabled as IExhibitJson

# Events
from eea.daviz.events.interfaces import IDavizRelationsChangedEvent

__all__ = [
    IPossibleExhibitJson.__name__,
    IExhibitJson.__name__,
    IDavizRelationsChangedEvent.__name__,
]


class IDavizSettings(Interface):
    defaultFolder = schema.Choice(
        title=u"Default Folder",
        description=u"Default Folder for creating Visualizations",
        required=True,
        vocabulary='eea.daviz.vocabularies.DefaultFolderVocabulary',
        )
