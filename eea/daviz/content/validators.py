""" Custom AT Validators
"""
from eea.app.visualization.converter.interfaces import IExhibitJsonConverter
from zope.component import queryUtility
from zope.component import getUtility
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements
from eea.daviz.config import EEAMessageFactory as _
from eea.app.visualization.interfaces import IExternalData

class CSVFileValidator(object):
    """ Validator
    """
    implements(IValidator)

    def __init__(self, name, title='CSV File',
                 description='CSV valid file or text'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        """ Check if provided file or data is a valid csv """
        converter = getUtility(IExhibitJsonConverter)
        _cols, csv2json = converter(value)
        if len(csv2json.get('items', [])) == 0:
            return _('You should provide data in a valid CSV format'
                     '(.csv, .tsv, etc)')
        return 1

class ExternalDataValidator(object):
    """ Validator
    """
    implements(IValidator)

    def __init__(self, name, title='External Data for Daviz',
                 description="Valid external data URL"):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        """ Check if provided URL is a valid and supported data
        """
        external = queryUtility(IExternalData)
        data = external.test(value)
        if not data:
            return _(
                u"Provided URL doesn't provide valid data for "
                "visualization or this type of data is not supported, yet.")
        return 1
