""" Subtypes exhibit interfaces
"""
# BBB
from eea.app.visualization.interfaces import IPossibleVisualization as IPossibleExhibitJson
from eea.app.visualization.interfaces import IVisualizationSubtyper as IDavizSubtyper
from eea.app.visualization.interfaces import IVisualizationEnabled as IExhibitJson

import warnings
warnings.warn("eea.daviz.subtypes.interfaces are deprecated. "
              "Please use eea.app.visualization.interfaces instead",
              DeprecationWarning)
