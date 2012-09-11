""" Daviz Presentation
"""
#BBB
from eea.daviz.content.visualization import DavizVisualization
DavizPresentation = DavizVisualization

import warnings
warnings.warn("eea.daviz.content.presentation is deprecated. "
              "Please use eea.daviz.content.visualization instead",
              DeprecationWarning)
