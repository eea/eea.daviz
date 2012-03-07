""" App daviz interfaces
"""
#BBB
from eea.app.visualization.interfaces import \
     IVisualizationConfig as IDavizConfig

import warnings
warnings.warn("eea.daviz.app.interfaces are deprecated. "
              "Please use eea.app.visualization.interfaces instead",
              DeprecationWarning)
