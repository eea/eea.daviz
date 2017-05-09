""" Subtypes exhibit interfaces
"""
# BBB
import warnings
from eea.app.visualization.interfaces import \
    IPossibleVisualization as IPossibleExhibitJson
from eea.app.visualization.interfaces import \
     IVisualizationEnabled as IExhibitJson

warnings.warn("eea.daviz.subtypes.interfaces are deprecated. "
              "Please use eea.app.visualization.interfaces instead",
              DeprecationWarning)

__all__ = (
    IPossibleExhibitJson.__name__,
    IExhibitJson.__name__,
)
