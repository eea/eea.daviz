""" Daviz Presentation
"""
#BBB
import warnings

from eea.daviz.content.visualization import DavizVisualization
DavizPresentation = DavizVisualization

warnings.warn("eea.daviz.content.presentation is deprecated. "
              "Please use eea.daviz.content.visualization instead",
              DeprecationWarning)
