try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.interfaces import IAnnotations

try:
    from zope.annotation.attribute import AttributeAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.attribute import AttributeAnnotations

from zope.interface import Interface

class IPossibleExhibitJson(Interface):
    """ Objects which can have Exhibit Json exported data.
    """

class IExhibitJson(Interface):
    """ Objects which have Exhibit Json exported data.
    """
