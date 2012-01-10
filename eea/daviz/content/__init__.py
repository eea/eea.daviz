""" Custom content
"""
from Products.ATContentTypes.content.base import registerATCT
from eea.daviz.content.presentation import DavizPresentation
from eea.daviz.config import PACKAGE

def register():
    """ Register custom content-types
    """
    registerATCT(DavizPresentation, PACKAGE)
