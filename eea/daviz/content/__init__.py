""" Custom content
"""
from Products.validation.config import validation
from eea.daviz.content.validators import CSVFileValidator
from eea.daviz.content.validators import ExternalDataValidator
validation.register(CSVFileValidator('csvfile'))
validation.register(ExternalDataValidator('externalURL'))


from Products.ATContentTypes.content.base import registerATCT
from eea.daviz.content.visualization import DavizVisualization
from eea.daviz.config import PACKAGE

def register():
    """ Register custom content-types
    """
    registerATCT(DavizVisualization, PACKAGE)
